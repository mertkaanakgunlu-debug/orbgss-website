"""Render a scene's frame range as a review animatic, inside one Blender session.

    blender -b -P hero/scripts/render_animatic.py -- --scene hero_predata_animatic
    blender -b -P hero/scripts/render_animatic.py -- --scene hero_predata_animatic --frames 1,140,240

WEB-HERO-001D's first deliverable is a preview of the whole pre-data sequence,
because continuity is the thing under review and no still can show it. This is
a *review* artifact: it deliberately does not decide production container,
bitrate, poster frame or reduced-motion packaging, all of which belong to the
later hero/WEB-005 media task.

Two things it does that a bare ``bpy.ops.render.render(animation=True)`` does
not:

* it builds the scene once and renders every frame from that one build, which
  is what makes a 240-frame range affordable when the Earth albedo is an 8K
  image that costs seconds to decode;
* it reports a full evidence record -- engine, device, duration, resolution,
  byte size and SHA-256 of what it actually wrote -- so the animatic can be
  cited by pointer and hash rather than committed.

``--frames`` renders an arbitrary subset to stills instead, which is the
iteration path: same build, same profile, no video muxing.

Video is written through Blender's own bundled FFmpeg, so the lane still
depends on nothing beyond Blender itself.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bpy  # noqa: E402

import build_scene  # noqa: E402
import hero_common as hc  # noqa: E402
import render_core  # noqa: E402


def _configure_video(scene, container: str, codec: str, quality: str) -> dict:
    scene.render.image_settings.file_format = "FFMPEG"
    ffmpeg = scene.render.ffmpeg
    ffmpeg.format = container
    ffmpeg.codec = codec
    ffmpeg.constant_rate_factor = quality
    ffmpeg.ffmpeg_preset = "GOOD"
    ffmpeg.gopsize = 12
    try:
        ffmpeg.audio_codec = "NONE"
    except TypeError:
        pass
    return {
        "container": ffmpeg.format,
        "codec": ffmpeg.codec,
        "constant_rate_factor": ffmpeg.constant_rate_factor,
        "preset": ffmpeg.ffmpeg_preset,
        "gop_size": ffmpeg.gopsize,
    }


def _written(path: Path, scene) -> Path:
    """Resolve what Blender actually wrote for a video output.

    Blender appends the rendered frame range to a movie filename, so the path
    handed to it is a prefix, not a result. Report the file that exists.
    """
    if path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    candidates = sorted(path.parent.glob(stem + "*" + suffix))
    return candidates[-1] if candidates else path


def render_animatic(
    scene_id: str,
    profile_name: str,
    out_path: Path,
    aoi_fixture=None,
    frame_start=None,
    frame_end=None,
    frame_step=1,
    container="MPEG4",
    codec="H264",
    quality="HIGH",
) -> dict:
    scene_config = hc.load_scene_config()
    render_config = hc.load_render_config()

    spec = build_scene.build(scene_id, scene_config, aoi_fixture=aoi_fixture)
    applied = render_core.apply_profile(profile_name, render_config)

    scene = bpy.context.scene
    animation = spec.get("animation", {})
    start = int(frame_start if frame_start is not None else animation.get("frame_start", 1))
    end = int(frame_end if frame_end is not None else animation.get("frame_end", start))
    rate = int(animation.get("frame_rate", 24))

    scene.frame_start = start
    scene.frame_end = end
    scene.frame_step = int(frame_step)
    scene.render.fps = rate
    # A stepped animatic must still play in real time: rendering every Nth frame at the full
    # rate would run the review N times too fast, which is exactly what a motion review cannot
    # afford. fps / fps_base is the effective rate.
    scene.render.fps_base = float(max(1, int(frame_step)))

    video = _configure_video(scene, container, codec, quality)
    out_path = Path(out_path)
    hc.ensure_dir(out_path.parent)
    scene.render.filepath = str(out_path.with_suffix(""))

    started = time.perf_counter()
    bpy.ops.render.render(animation=True)
    elapsed = time.perf_counter() - started

    written = _written(out_path, scene)
    frames = len(range(start, end + 1, int(frame_step)))

    record = dict(applied)
    record.update(
        {
            "scene": scene_id,
            "aoi_fixture": aoi_fixture,
            "frame_start": start,
            "frame_end": end,
            "frame_step": int(frame_step),
            "frames_rendered": frames,
            "frame_rate": rate,
            "duration_seconds": round(frames * int(frame_step) / float(rate), 4),
            "video": video,
            "wall_clock_seconds": round(elapsed, 3),
            "seconds_per_frame": round(elapsed / frames, 4) if frames else None,
            "output_path": hc.relpath(written),
            "output_exists": written.exists(),
            "output_bytes": written.stat().st_size if written.exists() else 0,
            "sha256": hc.sha256_file(written) if written.exists() else None,
            "blender_version": bpy.app.version_string,
            "python_version": sys.version.split()[0],
            "artifact_class": "review_animatic",
            "note": (
                "Review artifact for continuity judgement. Production container, bitrate, poster "
                "frame and reduced-motion packaging are deliberately out of scope here and belong "
                "to the later hero/WEB-005 media task."
            ),
        }
    )
    return record


def render_frames(scene_id, profile_name, frames, out_dir: Path, aoi_fixture=None) -> dict:
    """Render a list of frames as stills from a single scene build."""
    scene_config = hc.load_scene_config()
    render_config = hc.load_render_config()

    build_scene.build(scene_id, scene_config, aoi_fixture=aoi_fixture)
    applied = render_core.apply_profile(profile_name, render_config)

    scene = bpy.context.scene
    out_dir = Path(out_dir)
    hc.ensure_dir(out_dir)

    written = []
    started = time.perf_counter()
    for frame in frames:
        scene.frame_set(int(frame))
        path = out_dir / (scene_id + "_" + profile_name + "_f" + str(int(frame)) + ".png")
        scene.render.filepath = str(path.with_suffix(""))
        bpy.ops.render.render(write_still=True)
        resolved = path if path.exists() else path.with_suffix(".png")
        written.append(
            {
                "frame": int(frame),
                "output_path": hc.relpath(resolved),
                "output_bytes": resolved.stat().st_size if resolved.exists() else 0,
                "sha256": hc.sha256_file(resolved) if resolved.exists() else None,
            }
        )
    elapsed = time.perf_counter() - started

    record = dict(applied)
    record.update(
        {
            "scene": scene_id,
            "aoi_fixture": aoi_fixture,
            "frames": written,
            "wall_clock_seconds": round(elapsed, 3),
            "seconds_per_frame": round(elapsed / len(frames), 4) if frames else None,
            "blender_version": bpy.app.version_string,
            "python_version": sys.version.split()[0],
        }
    )
    return record


def main() -> None:
    render_config = hc.load_render_config()

    parser = argparse.ArgumentParser(description="Render a review animatic or a set of stills.")
    parser.add_argument("--scene", default="hero_predata_animatic")
    parser.add_argument("--profile", default=render_config.get("default_preview_profile", "preview"))
    parser.add_argument("--aoi-fixture", default=None)
    parser.add_argument("--frame-start", type=int, default=None)
    parser.add_argument("--frame-end", type=int, default=None)
    parser.add_argument("--frame-step", type=int, default=1)
    parser.add_argument("--frames", default=None, help="comma-separated frames; renders stills instead of video")
    parser.add_argument("--out", default=None)
    parser.add_argument("--container", default="MPEG4")
    parser.add_argument("--codec", default="H264")
    parser.add_argument("--quality", default="HIGH")
    parser.add_argument("--record", default=None, help="write the render record as JSON")
    args = parser.parse_args(hc.argv_after_double_dash())

    # Blender resolves a relative render path against its own working directory,
    # not the repository, so every output path is made absolute here. A caller
    # passing "hero/renders/..." otherwise gets a silent write somewhere else.
    if args.frames:
        frames = [int(v) for v in args.frames.split(",") if v.strip()]
        out_dir = Path(args.out).resolve() if args.out else hc.RENDERS_DIR / "preview" / args.scene
        record = render_frames(args.scene, args.profile, frames, out_dir, args.aoi_fixture)
    else:
        out = Path(args.out).resolve() if args.out else (
            hc.RENDERS_DIR / "animatic" / (args.scene + "_" + args.profile + ".mp4")
        )
        record = render_animatic(
            args.scene,
            args.profile,
            out,
            aoi_fixture=args.aoi_fixture,
            frame_start=args.frame_start,
            frame_end=args.frame_end,
            frame_step=args.frame_step,
            container=args.container,
            codec=args.codec,
            quality=args.quality,
        )

    print(json.dumps(record, indent=2))
    if args.record:
        record_path = Path(args.record)
        hc.ensure_dir(record_path.parent)
        record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        print("[hero] record -> " + hc.relpath(record_path))


if __name__ == "__main__":
    main()
