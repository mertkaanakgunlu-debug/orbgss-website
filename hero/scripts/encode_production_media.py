"""Encode the production hero media package from a rendered frame sequence.

    blender -b -P hero/scripts/encode_production_media.py -- --scene hero_production_kizildere

WEB-HERO-001D deliberately stopped at a review animatic and left container, bitrate, poster frame
and reduced-motion packaging to WEB-005. This is that step.

It takes the PNG sequence rendered by ``render_animatic.py --frames`` and produces the three files
the site ships, inside the media envelope WEB-004 set and WEB-005 inherits:

    WebM / VP9   <= 3.0 MiB      the encode a modern browser takes
    MP4  / H.264 <= 4.5 MiB      the fallback for everything else
    poster WebP  <= 180 KiB      the LCP element, and the hero in every static state

Two things are worth knowing about how it works.

*Encoding goes through Blender's own bundled FFmpeg*, via the sequencer, so the lane still depends
on nothing beyond Blender itself — there is no system ffmpeg on the production workstation and
adding one would be a new runtime dependency for a static site.

*The bitrate is found, not guessed.* A budget in bytes does not translate to a bitrate you can
type: it depends on the content, and this content is a slow camera move over a mostly smooth
sphere, which VP9 compresses far better than a rate table would predict. So each encode is
measured and re-encoded against its own result until it fits with headroom, and the search is
recorded in the evidence rather than hidden.

Colour management matters here and is easy to get wrong: the rendered PNGs already have the
scene's view transform baked in, so the sequencer scene is forced to Standard/None. Transforming
them a second time would shift every pixel of the hero.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bpy  # noqa: E402

import hero_common as hc  # noqa: E402

MIB = 1024 * 1024

# role -> (hard ceiling in bytes, the fraction of it we aim for). The headroom is not timidity:
# the ceiling is a contract, and an encode that lands at 99.6% of it would fail the next time the
# frame sequence changed by a hair.
BUDGETS = {
    "hero-webm": (3.0 * MIB, 0.88),
    "hero-mp4": (4.5 * MIB, 0.88),
}
POSTER_CEILING = 180 * 1024

ENCODES = {
    "hero-webm": {"container": "WEBM", "codec": "WEBM", "suffix": ".webm",
                  "mime": "video/webm", "codec_name": "VP9", "start_kbps": 1900},
    "hero-mp4": {"container": "MPEG4", "codec": "H264", "suffix": ".mp4",
                 "mime": "video/mp4", "codec_name": "H.264", "start_kbps": 2800},
}


def frame_sequence(directory: Path, scene_id: str, profile: str):
    """The rendered stills, in frame order rather than the filesystem's lexical order."""
    prefix = scene_id + "_" + profile + "_f"
    found = []
    for path in directory.glob(prefix + "*.png"):
        try:
            found.append((int(path.stem[len(prefix):]), path))
        except ValueError:
            continue
    found.sort()
    return [path for _, path in found]


def _neutral_color_management(scene) -> None:
    """The stills already carry the render's view transform; do not apply it twice."""
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = 0.0
    scene.view_settings.gamma = 1.0
    scene.display_settings.display_device = "sRGB"
    scene.sequencer_colorspace_settings.name = "sRGB"


def build_sequencer_scene(frames, rate: int, width: int, height: int):
    # Blender runs headless here, so bpy.context.window is None and there is no window whose scene
    # could be switched. Configure the context scene itself instead of creating a second one.
    scene = bpy.context.scene
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.fps = rate
    scene.render.fps_base = 1.0
    scene.frame_start = 1
    scene.frame_end = len(frames)
    _neutral_color_management(scene)

    editor = scene.sequence_editor_create()
    # Blender 4.5 exposes this collection as `sequences`; later versions renamed it to `strips`.
    # Ask for whichever exists rather than pinning the encoder to one Blender release.
    collection = getattr(editor, "strips", None) or editor.sequences
    strip = collection.new_image(
        name="hero", filepath=str(frames[0]), channel=1, frame_start=1, fit_method="FIT",
    )
    for path in frames[1:]:
        strip.elements.append(path.name)
    strip.colorspace_settings.name = "sRGB"
    return scene


def encode_once(scene, spec: dict, kbps: int, out_path: Path, crf: str = "NONE") -> Path:
    settings = scene.render.image_settings
    settings.file_format = "FFMPEG"
    ffmpeg = scene.render.ffmpeg
    ffmpeg.format = spec["container"]
    ffmpeg.codec = spec["codec"]
    # Explicit bitrate, not a quality preset: the contract is a byte budget, so the knob has to be
    # the one that moves bytes predictably enough to converge.
    # Constrained quality when a CRF preset is given: the encoder is allowed to spend fewer bits on
    # the empty opening and more on the detailed close, instead of pouring a constant rate into both.
    # This shot's complexity varies enormously from frame 1 to frame 276, which is exactly where
    # target-bitrate CBR wastes the budget.
    ffmpeg.constant_rate_factor = crf
    # GOOD, not BEST, and the reason is measured rather than assumed. libvpx-vp9's "best" deadline
    # took roughly 20 minutes per attempt here -- and the bitrate search needs several attempts --
    # for a quality difference the format's own maintainers describe as negligible over "good".
    # The sharpness in this revision comes from supersampling the source, not from the deadline.
    ffmpeg.ffmpeg_preset = "GOOD"
    ffmpeg.gopsize = 24
    ffmpeg.video_bitrate = int(kbps)
    ffmpeg.minrate = 0
    ffmpeg.maxrate = int(kbps * 1.45)
    ffmpeg.buffersize = int(kbps * 2)
    try:
        ffmpeg.audio_codec = "NONE"
    except TypeError:
        pass

    hc.ensure_dir(out_path.parent)
    for stale in out_path.parent.glob(out_path.stem + "*" + spec["suffix"]):
        stale.unlink()
    scene.render.filepath = str(out_path.with_suffix(""))
    bpy.ops.render.render(animation=True)

    if out_path.exists():
        return out_path
    produced = sorted(out_path.parent.glob(out_path.stem + "*" + spec["suffix"]))
    if not produced:
        raise RuntimeError("no file produced for " + str(out_path))
    final = produced[-1]
    final.replace(out_path)
    return out_path


def fit_encode(scene, role: str, spec: dict, out_path: Path, attempts: int = 5) -> dict:
    ceiling, aim = BUDGETS[role]
    target_bytes = ceiling * aim
    kbps = spec["start_kbps"]
    search = []
    best = None

    for attempt in range(1, attempts + 1):
        started = time.perf_counter()
        written = encode_once(scene, spec, kbps, out_path)
        elapsed = time.perf_counter() - started
        size = written.stat().st_size
        search.append({
            "attempt": attempt,
            "video_bitrate_kbps": int(kbps),
            "bytes": size,
            "mib": round(size / MIB, 3),
            "ceiling_mib": round(ceiling / MIB, 3),
            "within_ceiling": size <= ceiling,
            "wall_clock_seconds": round(elapsed, 2),
        })
        print("[web005] " + role + " attempt " + str(attempt) + ": " + str(int(kbps))
              + " kbps -> " + str(round(size / MIB, 3)) + " MiB")

        if size <= ceiling and (best is None or size > best["bytes"]):
            # Inside the ceiling, prefer the LARGEST such encode: it is the best-looking one that
            # still honours the contract. Quality is the point; the budget is the constraint.
            best = {"bytes": size, "kbps": int(kbps), "path": written}
        if size <= ceiling and size >= target_bytes * 0.82:
            break
        # Straight proportional correction. The relationship is close enough to linear over the
        # range that matters, and clamping keeps one bad measurement from running away.
        ratio = target_bytes / float(size)
        kbps = max(350, min(int(kbps * max(0.45, min(2.0, ratio))), 9000))
        if any(abs(kbps - s["video_bitrate_kbps"]) < 25 for s in search):
            break

    if best is None:
        raise RuntimeError(role + " never fit inside its ceiling; search: " + json.dumps(search))
    if best["kbps"] != search[-1]["video_bitrate_kbps"] or not out_path.exists():
        encode_once(scene, spec, best["kbps"], out_path)

    size = out_path.stat().st_size
    return {
        "role": role,
        "path": hc.relpath(out_path).replace("\\", "/"),
        "container": "WebM" if spec["container"] == "WEBM" else "MP4",
        "mime_type": spec["mime"],
        "codec": spec["codec_name"],
        "video_bitrate_kbps": best["kbps"],
        "bytes": size,
        "mib": round(size / MIB, 3),
        "ceiling_mib": round(ceiling / MIB, 3),
        "within_ceiling": size <= ceiling,
        "sha256": hc.sha256_file(out_path),
        "bitrate_search": search,
    }


def write_poster(source: Path, out_path: Path, width: int, height: int,
                 ceiling: int = POSTER_CEILING) -> dict:
    """The poster is the LCP element, so it gets the same treatment as the encodes: find the
    highest quality that fits, rather than picking a number and hoping."""
    scene = bpy.context.scene
    _neutral_color_management(scene)
    settings = scene.render.image_settings
    settings.file_format = "WEBP"

    search = []
    chosen = None
    for quality in (88, 82, 76, 70, 64, 58, 50):
        image = bpy.data.images.load(str(source))
        image.colorspace_settings.name = "sRGB"
        image.scale(width, height)
        settings.quality = quality
        hc.ensure_dir(out_path.parent)
        image.save_render(filepath=str(out_path), scene=scene)
        bpy.data.images.remove(image)
        size = out_path.stat().st_size
        search.append({"quality": quality, "bytes": size, "kib": round(size / 1024, 1)})
        print("[web005] poster " + str(width) + " q" + str(quality) + " -> "
              + str(round(size / 1024, 1)) + " KiB", flush=True)
        if size <= ceiling:
            chosen = quality
            break

    if chosen is None:
        raise RuntimeError("poster never fit " + str(ceiling) + " bytes: " + json.dumps(search))

    size = out_path.stat().st_size
    return {
        "role": "hero-poster" if width >= 1600 else "hero-poster-narrow",
        "path": hc.relpath(out_path).replace("\\", "/"),
        "container": "WebP",
        "mime_type": "image/webp",
        "codec": "WebP (lossy)",
        "quality": chosen,
        "width": width,
        "height": height,
        "bytes": size,
        "kib": round(size / 1024, 1),
        "ceiling_kib": round(ceiling / 1024, 1),
        "within_ceiling": size <= ceiling,
        "source_frame": hc.relpath(source).replace("\\", "/"),
        "sha256": hc.sha256_file(out_path),
        "quality_search": search,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Encode the WEB-005 production hero media.")
    parser.add_argument("--scene", default="hero_production_kizildere")
    parser.add_argument("--profile", default="production")
    parser.add_argument("--frames-dir", default="hero/renders/production/frame.png")
    parser.add_argument("--out-dir", default="assets/hero")
    parser.add_argument("--stem", default="orbgss-hero")
    parser.add_argument("--record", default="hero/evidence/production_media.json")
    parser.add_argument("--width", type=int, default=None,
                        help="override the delivered encode width (the profile's render width "
                             "is the default; a smaller delivery buys bitrate per pixel)")
    parser.add_argument("--height", type=int, default=None)
    args = parser.parse_args(hc.argv_after_double_dash())

    scene_config = hc.load_scene_config()
    spec = hc.resolve_scene_spec(args.scene, scene_config["scenes"])
    animation = spec.get("animation", {})
    rate = int(animation.get("frame_rate", 24))

    render_config = hc.load_render_config()
    profile = render_config["profiles"][args.profile]
    width = int(args.width or profile["resolution_x"])
    height = int(args.height or profile["resolution_y"])

    frames_dir = hc.REPO_ROOT / args.frames_dir
    frames = frame_sequence(frames_dir, args.scene, args.profile)
    expected = int(animation.get("frame_end", 0)) - int(animation.get("frame_start", 1)) + 1
    if len(frames) != expected:
        raise SystemExit("expected " + str(expected) + " rendered frames in "
                         + str(frames_dir) + ", found " + str(len(frames)))
    if (width, height) != (int(profile["resolution_x"]), int(profile["resolution_y"])):
        print("[web005] supersampling: rendered at "
              + str(profile["resolution_x"]) + "x" + str(profile["resolution_y"])
              + ", delivering " + str(width) + "x" + str(height))

    out_dir = hc.REPO_ROOT / args.out_dir
    encode_scene = build_sequencer_scene(frames, rate, width, height)

    media = []
    for role, encode_spec in ENCODES.items():
        out_path = out_dir / (args.stem + encode_spec["suffix"])
        record = fit_encode(encode_scene, role, encode_spec, out_path)
        record.update({
            "width": width,
            "height": height,
            "frame_rate": rate,
            "frame_count": len(frames),
            "duration_seconds": round(len(frames) / float(rate), 4),
        })
        media.append(record)

    # The poster is the LAST frame, not the first: the shot ends on the stable hold, so the still
    # a visitor sees before playback is the same composition playback settles into. Starting on
    # frame 1 would show a distant Earth that the copy does not describe.
    poster_source = frames[-1]
    encode_scene.render.image_settings.file_format = "PNG"
    media.append(write_poster(poster_source, out_dir / "hero-poster-1600.webp", 1600, 900))
    media.append(write_poster(poster_source, out_dir / "hero-poster-900.webp", 900, 506))

    record = {
        "task": "WEB-005 / MER-93",
        "revision": "WEB-005A R3 / MER-107 hero visual revision",
        "scene": args.scene,
        "profile": args.profile,
        "consumed_hero_evidence_head": "e95fdcac7cac82e597d40dab4cdc96ce1a6b319e",
        "source_frames": {
            "directory": hc.relpath(frames_dir).replace("\\", "/"),
            "count": len(frames),
            "first": hc.relpath(frames[0]).replace("\\", "/"),
            "last": hc.relpath(frames[-1]).replace("\\", "/"),
        },
        "colour_management": {
            "view_transform": "Standard",
            "look": "None",
            "sequencer_colorspace": "sRGB",
            "note": "The stills already carry the render view transform; the encoder must not "
                    "apply it a second time.",
        },
        "render_resolution": [int(profile["resolution_x"]), int(profile["resolution_y"])],
        "motion_blur_shutter": profile.get("motion_blur_shutter"),
        "delivered_resolution": [width, height],
        "blender_version": bpy.app.version_string,
        "python_version": sys.version.split()[0],
        "media": media,
    }

    record_path = hc.REPO_ROOT / args.record
    hc.ensure_dir(record_path.parent)
    record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))
    print("[web005] record -> " + hc.relpath(record_path))


if __name__ == "__main__":
    main()
