#!/usr/bin/env python3
"""Responsive hero delivery ladder (MER-216 Phase 2): WebM/VP9 + MP4/H.264 at two sizes.

    py -3.14 hero/scripts/encode_responsive_media.py [--bench] [--ffmpeg PATH] [--work-dir DIR]

Input is the accepted production master and nothing else: the 276 rendered 2304 x 1296 PNG frames in
hero/renders/production/frame.png, which are checked against their per-frame SHA-256 in the render
records before a single frame is encoded. Nothing is re-rendered and nothing in the scene, camera,
choreography or content changes; this only re-encodes the same frames for delivery.

Why this exists next to encode_production_media.py, and why it does not use Blender's encoder:
Blender's bundled FFmpeg can only run one-pass average-bitrate VP9 and gives no control of keyframe
placement or MP4 atom order. The measurements in tasks/MER-216_EVIDENCE.md show the accepted files
were the product of that limit (the MP4 puts its `moov` atom after 4.2 MB of media, so a browser
must make a second range request before it can start, and the VP9 file is 6 VMAF points below what
the same byte budget buys with two-pass encoding). FFmpeg is local production tooling exactly as the
hero lane already treats Blender: nothing here is a site dependency, the published site stays static
HTML, CSS and vanilla JavaScript. The exact FFmpeg build and every argument list are recorded.

Outputs (assets/hero/, immutable-cached by the host (a one-year immutable Cache-Control on /assets/), so each file name carries the first eight
hex digits of its own SHA-256 and a re-encode can never be served stale):

    orbgss-hero-<w>-<hash8>.webm | .mp4

Tiers (WEB-004 / WEB-005 binding media envelope: WebM <= 3.0 MiB, MP4 <= 4.5 MiB at the 1920 tier;
the 1280 tier gets proportionally smaller ceilings because it exists to cost less):

    sm   1280 x 720    VP9 two-pass       H.264 CRF + maxrate
    md   1920 x 1080   VP9 two-pass       H.264 CRF + maxrate

A 2304 x 1296 tier (the master's own size) was built and benchmarked and is deliberately not
published: at the same 3.3 MiB it scored 95.5 VMAF against the 1920 tier's 94.5 on the 2304 reference,
and inside the 3.0 MiB envelope it cannot beat the 1920 tier at all. See the evidence document.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
FRAMES_DIR = ROOT / "hero" / "renders" / "production" / "frame.png"
FRAME_PATTERN = "hero_production_kizildere_production_f%d.png"
RECORDS = ["render_record.json", "render_record_pass2.json", "render_record_pass3.json"]
OUT_DIR = ROOT / "assets" / "hero"
RECORD = ROOT / "hero" / "evidence" / "responsive_media.json"
FRAME_COUNT = 276
FPS = 24
MIB = 1024 * 1024
TAGS = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]

TIERS = [
    {"id": "sm", "width": 1280,
     "webm": {"kbps": 1100, "ceiling_mib": 2.0}, "mp4": {"crf": 22, "maxkbps": 2000, "ceiling_mib": 3.0},
     "codecs": {"webm": "vp09.00.31.08", "mp4": "avc1.64001f"}},
    {"id": "md", "width": 1920,
     "webm": {"kbps": 1950, "ceiling_mib": 3.0}, "mp4": {"crf": 22, "maxkbps": 3300, "ceiling_mib": 4.5},
     "codecs": {"webm": "vp09.00.40.08", "mp4": "avc1.640028"}},
]


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def find_ffmpeg(explicit: str | None) -> str:
    if explicit:
        return explicit
    found = shutil.which("ffmpeg")
    if found:
        return found
    try:
        import imageio_ffmpeg  # local tooling only
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:  # noqa: BLE001
        raise SystemExit("no ffmpeg: pass --ffmpeg PATH (a build with libvpx-vp9, libx264 and libvmaf)")


def verify_master() -> dict:
    """The accepted master: every frame must match the latest render record's SHA-256."""
    latest: dict[int, str] = {}
    for name in RECORDS:
        rec = json.loads((ROOT / "hero" / "renders" / "production" / name).read_text(encoding="utf-8"))
        for fr in rec["frames"]:
            latest[int(fr["frame"])] = fr["sha256"]
    digest = hashlib.sha256()
    for n in range(1, FRAME_COUNT + 1):
        p = FRAMES_DIR / (FRAME_PATTERN % n)
        if not p.exists():
            raise SystemExit(f"master frame missing: {p}")
        h = sha256(p)
        if h != latest.get(n):
            raise SystemExit(f"master frame {n} does not match its render record")
        digest.update(f"{n}:{h}\n".encode())
    return {"frames": FRAME_COUNT, "resolution": [2304, 1296], "directory": "hero/renders/production/frame.png",
            "frame_set_sha256": digest.hexdigest(),
            "verified_against": ["hero/renders/production/" + r for r in RECORDS]}


class Tool:
    def __init__(self, ffmpeg: str, work: pathlib.Path):
        self.ffmpeg = ffmpeg
        self.work = work
        self.log: list[list[str]] = []

    def run(self, args: list[str], record: bool = True, cwd=None) -> str:
        cmd = [self.ffmpeg, "-hide_banner", "-nostats"] + args
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
        if p.returncode != 0:
            raise SystemExit(p.stderr[-2000:])
        return p.stderr

    def version(self) -> str:
        out = subprocess.run([self.ffmpeg, "-version"], capture_output=True, text=True).stdout
        return out.splitlines()[0]

    def source(self, width: int) -> list[str]:
        h = width * 9 // 16
        return ["-y", "-framerate", str(FPS), "-start_number", "1", "-i", str(FRAMES_DIR / FRAME_PATTERN),
                "-vf", f"scale={width}:{h}:flags=lanczos+accurate_rnd+full_chroma_int:out_color_matrix=bt709:out_range=tv,format=yuv420p",
                "-frames:v", str(FRAME_COUNT), "-r", str(FPS)]

    def vp9(self, tier: dict, out: pathlib.Path) -> list[list[str]]:
        kbps = tier["webm"]["kbps"]
        log = str(self.work / f"vp9_{tier['width']}")
        common = ["-c:v", "libvpx-vp9", "-pix_fmt", "yuv420p"] + TAGS + [
            "-g", "48", "-keyint_min", "48", "-quality", "good", "-cpu-used", "2", "-row-mt", "1",
            "-tile-columns", "2", "-auto-alt-ref", "1", "-lag-in-frames", "25", "-an", "-passlogfile", log,
            "-b:v", f"{kbps}k", "-minrate", f"{int(kbps * 0.5)}k", "-maxrate", f"{int(kbps * 1.6)}k"]
        p1 = self.source(tier["width"]) + common + ["-pass", "1", "-f", "null", "-"]
        p2 = self.source(tier["width"]) + common + ["-pass", "2", str(out)]
        self.run(p1)
        self.run(p2)
        return [p1, p2]

    def h264(self, tier: dict, out: pathlib.Path) -> list[list[str]]:
        s = tier["mp4"]
        args = self.source(tier["width"]) + [
            "-c:v", "libx264", "-preset", "slower", "-crf", str(s["crf"]), "-profile:v", "high",
            "-level", "4.0" if tier["width"] > 1280 else "3.1", "-pix_fmt", "yuv420p"] + TAGS + [
            "-g", "48", "-keyint_min", "48", "-bf", "3", "-refs", "4", "-an", "-movflags", "+faststart",
            "-maxrate", f"{s['maxkbps']}k", "-bufsize", f"{s['maxkbps'] * 2}k", str(out)]
        self.run(args)
        return [args]

    # ---- objective fidelity: cfr-safe, lossless intermediates, paired by frame index ----------
    def reference(self, width: int) -> pathlib.Path:
        out = self.work / f"ref_{width}.mkv"
        if not out.exists():
            self.run(self.source(width) + ["-c:v", "ffv1", "-level", "3", str(out)])
        return out

    def bench(self, video: pathlib.Path, width: int, subsample: int = 4) -> dict:
        ref = self.reference(width)
        h = width * 9 // 16
        dist = self.work / (video.stem + f"_dist{width}.mkv")
        self.run(["-y", "-i", str(video), "-vf", f"scale={width}:{h}:flags=lanczos+accurate_rnd,format=yuv420p",
                  "-r", str(FPS), "-frames:v", str(FRAME_COUNT), "-c:v", "ffv1", "-level", "3", str(dist)])
        res: dict = {"reference_width": width}
        err = self.run(["-i", str(dist), "-i", str(ref), "-lavfi", "psnr=stats_file=-", "-f", "null", "-"])
        m = re.search(r"PSNR y:([\d.]+) u:([\d.]+) v:([\d.]+) average:([\d.]+) min:([\d.]+)", err)
        if m:
            res.update(psnr_y=float(m.group(1)), psnr_avg=float(m.group(4)), psnr_min_frame=float(m.group(5)))
        err = self.run(["-i", str(dist), "-i", str(ref), "-lavfi", "ssim", "-f", "null", "-"])
        m = re.search(r"All:([\d.]+)", err)
        if m:
            res["ssim_all"] = float(m.group(1))
        vj = self.work / "vmaf.json"
        subprocess.run([self.ffmpeg, "-hide_banner", "-nostats", "-i", str(dist), "-i", str(ref), "-lavfi",
                        f"libvmaf=n_subsample={subsample}:log_fmt=json:log_path={vj.name}", "-f", "null", "-"],
                       capture_output=True, text=True, cwd=str(self.work))
        if vj.exists():
            pm = json.loads(vj.read_text()).get("pooled_metrics", {}).get("vmaf", {})
            res.update(vmaf_mean=round(pm.get("mean", 0), 3), vmaf_min_frame=round(pm.get("min", 0), 3),
                       vmaf_subsample=subsample)
            vj.unlink()
        dist.unlink(missing_ok=True)
        return res


def mp4_atoms(path: pathlib.Path) -> list[str]:
    import struct
    out, size, pos = [], path.stat().st_size, 0
    with open(path, "rb") as f:
        while pos < size:
            f.seek(pos)
            h = f.read(8)
            if len(h) < 8:
                break
            s, t = struct.unpack(">I4s", h)
            if s == 1:
                s = struct.unpack(">Q", f.read(8))[0]
            out.append(t.decode("latin1"))
            pos += s if s else size - pos
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ffmpeg")
    ap.add_argument("--work-dir")
    ap.add_argument("--bench", action="store_true", help="also measure PSNR/SSIM/VMAF against the master")
    ap.add_argument("--record", default=str(RECORD))
    a = ap.parse_args()

    master = verify_master()
    work = pathlib.Path(a.work_dir or tempfile.mkdtemp(prefix="orbgss-hero-"))
    work.mkdir(parents=True, exist_ok=True)
    tool = Tool(find_ffmpeg(a.ffmpeg), work)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    media = []
    for tier in TIERS:
        for codec, ext in (("webm", ".webm"), ("mp4", ".mp4")):
            tmp = work / f"orbgss-hero-{tier['width']}{ext}"
            tmp.unlink(missing_ok=True)
            started = time.time()
            cmds = tool.vp9(tier, tmp) if codec == "webm" else tool.h264(tier, tmp)
            digest = sha256(tmp)
            final = OUT_DIR / f"orbgss-hero-{tier['width']}-{digest[:8]}{ext}"
            shutil.copyfile(tmp, final)
            size = final.stat().st_size
            ceiling = tier[codec]["ceiling_mib"] * MIB
            entry = {
                "role": f"hero-{codec}-{tier['id']}", "tier": tier["id"], "codec_family": codec,
                "path": final.relative_to(ROOT).as_posix(),
                "container": "WebM" if codec == "webm" else "MP4",
                "mime_type": "video/webm" if codec == "webm" else "video/mp4",
                "codec": "VP9" if codec == "webm" else "H.264", "codec_string": tier["codecs"][codec],
                "width": tier["width"], "height": tier["width"] * 9 // 16, "frame_rate": FPS,
                "frame_count": FRAME_COUNT, "duration_seconds": round(FRAME_COUNT / FPS, 4),
                "bytes": size, "mib": round(size / MIB, 3), "ceiling_mib": tier[codec]["ceiling_mib"],
                "within_ceiling": size <= ceiling, "sha256": digest,
                "average_kbps": round(size * 8 / (FRAME_COUNT / FPS) / 1000),
                "encode_seconds": round(time.time() - started, 1),
                "ffmpeg_arguments": cmds,
            }
            if codec == "mp4":
                atoms = mp4_atoms(final)
                entry["atom_order"] = atoms
                entry["faststart"] = atoms.index("moov") < atoms.index("mdat")
            if not entry["within_ceiling"]:
                raise SystemExit(f"{final.name} is {entry['mib']} MiB, over its {tier[codec]['ceiling_mib']} MiB ceiling")
            if a.bench:
                entry["fidelity"] = tool.bench(final, tier["width"])
            media.append(entry)
            print(f"{entry['role']:12s} {entry['mib']:6.3f} MiB  {final.name}", flush=True)
    record = {
        "task": "MER-216 Phase 2", "master": master, "ffmpeg": tool.version(),
        "colour": "bt709 / tv range, yuv420p, tagged in the stream; the master frames are sRGB and already carry the scene's view transform",
        "keyframe_interval_frames": 48, "frame_rate": FPS,
        "method": "FFmpeg two-pass VP9 (libvpx-vp9, good, cpu-used 2) and CRF + maxrate H.264 (libx264 slower, High), Lanczos resize from the 2304 x 1296 master",
        "media": media,
    }
    pathlib.Path(a.record).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("record ->", a.record)
    return 0


if __name__ == "__main__":
    sys.exit(main())
