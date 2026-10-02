#!/usr/bin/env python3
"""Objective fidelity of a delivered hero encode against the accepted 2304x1296 master frames.

    python bench_video.py <video> [--ref-width 1920] [--vmaf-subsample 4] [--json out.json]

Method (cfr-safe: WebM carries millisecond timestamps, so pairing two streams by timestamp mis-pairs
frames during motion; both sides are therefore first written as lossless constant-24-fps files and
paired by frame index):
  reference = master PNG sequence resized (Lanczos) to --ref-width, bt709/tv yuv420p  (cached)
  distorted = decoded delivery file, resized (Lanczos) to --ref-width when it is a different size
Metrics: PSNR (Y/U/V avg + per-frame min), SSIM (All), VMAF (default model, subsampled).
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE.parent / "ref"
FRAMES = r"C:\Projects\website-orbgss\hero\renders\production\frame.png\hero_production_kizildere_production_f%d.png"


def ff(args, check=True):
    p = subprocess.run([FF, "-hide_banner", "-nostats"] + args, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(p.stderr[-1500:])
    return p.stderr


def reference(ref_w):
    CACHE.mkdir(exist_ok=True)
    out = CACHE / f"ref_{ref_w}.mkv"
    if not out.exists():
        h = ref_w * 9 // 16
        ff(["-y", "-framerate", "24", "-start_number", "1", "-i", FRAMES, "-vf",
            f"scale={ref_w}:{h}:flags=lanczos+accurate_rnd+full_chroma_int:out_color_matrix=bt709:out_range=tv,format=yuv420p",
            "-frames:v", "276", "-c:v", "ffv1", "-level", "3", str(out)])
    return out


def run(video, ref_w, subsample):
    ref = reference(ref_w)
    h = ref_w * 9 // 16
    video = pathlib.Path(video)
    dist = CACHE / (video.stem + f"_dist{ref_w}.mkv")
    ff(["-y", "-i", str(video), "-vf",
        f"scale={ref_w}:{h}:flags=lanczos+accurate_rnd,format=yuv420p", "-r", "24", "-frames:v", "276",
        "-c:v", "ffv1", "-level", "3", str(dist)])
    res = {"video": str(video), "bytes": video.stat().st_size, "ref_width": ref_w}
    err = ff(["-i", str(dist), "-i", str(ref), "-lavfi", "psnr=stats_file=NUL", "-f", "null", "-"])
    m = re.search(r"PSNR y:([\d.]+) u:([\d.]+) v:([\d.]+) average:([\d.]+) min:([\d.]+)", err)
    if m:
        res.update(psnr_y=float(m.group(1)), psnr_avg=float(m.group(4)), psnr_min=float(m.group(5)))
    err = ff(["-i", str(dist), "-i", str(ref), "-lavfi", "ssim=stats_file=NUL", "-f", "null", "-"])
    m = re.search(r"All:([\d.]+)", err)
    if m:
        res["ssim_all"] = float(m.group(1))
    vj = CACHE / "vmaf.json"
    ff(["-i", str(dist), "-i", str(ref), "-lavfi",
        f"libvmaf=n_subsample={subsample}:log_fmt=json:log_path={vj.name}", "-f", "null", "-"], check=True) if False else None
    p = subprocess.run([FF, "-hide_banner", "-nostats", "-i", str(dist), "-i", str(ref), "-lavfi",
                        f"libvmaf=n_subsample={subsample}:log_fmt=json:log_path=vmaf.json", "-f", "null", "-"],
                       capture_output=True, text=True, cwd=str(CACHE))
    if vj.exists():
        d = json.loads(vj.read_text())
        pm = d.get("pooled_metrics", {}).get("vmaf", {})
        res.update(vmaf_mean=round(pm.get("mean", 0), 3), vmaf_min=round(pm.get("min", 0), 3),
                   vmaf_harmonic=round(pm.get("harmonic_mean", 0), 3))
        vj.unlink()
    dist.unlink()
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--ref-width", type=int, default=1920)
    ap.add_argument("--vmaf-subsample", type=int, default=4)
    ap.add_argument("--json")
    a = ap.parse_args()
    r = run(a.video, a.ref_width, a.vmaf_subsample)
    print(json.dumps(r, indent=1))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(r, indent=1))
