#!/usr/bin/env python3
"""Build the responsive derivatives of the three "other place" Landsat scenes and record them.

    py -3.14 scripts/build_m6_context_scenes.py            # write the files and sources.json -> web_m6.context_scenes
    py -3.14 scripts/build_m6_context_scenes.py --check    # exit 1 if the files or the record differ from a fresh build

Local production tooling (Pillow), never a site runtime dependency; nothing runs on Vercel.

What it makes. The About page, the Partner page and the Marine panel of /solutions/ each show a public-domain
Landsat scene of a place that is not the Kizildere pilot area (the missing-visuals plan, 2026-10-25; MER-238
visual need V4 for Marine). The masters are built by `scripts/build_imagery.py` from USGS Landsat Collection 2
Level-2 products recorded in `assets/imagery/sources.json` -> `web_m6.context_scenes[].production`. This script
turns each master into responsive WebP derivatives, one Lanczos3 downscale and one WebP encode per width and
nothing else: no crop, no tone or colour change, no sharpening, no upscaling, no generative step.

File names carry the first 8 hex digits of a hash of the master's pixels and the encode settings, because
`/assets/` is served immutable for a year: a re-rendered master is a new name, never a silent overwrite.
"""
from __future__ import annotations

import hashlib
import io
import json
import pathlib
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "imagery" / "sources.json"
WEBP_QUALITY = 82  # the same encode as every other WebP derivative on the site
ROLE = "context-scene-responsive"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build(root: pathlib.Path = ROOT) -> tuple[dict[str, bytes], list[dict]]:
    manifest = json.loads((root / "assets" / "imagery" / "sources.json").read_text(encoding="utf-8"))
    files: dict[str, bytes] = {}
    records: list[dict] = []
    for scene in manifest["web_m6"]["context_scenes"]:
        master_path = root / scene["local_file"]
        master_bytes = master_path.read_bytes()
        master = Image.open(io.BytesIO(master_bytes)).convert("RGB")
        prod = scene["production"]
        if list(master.size) != [prod["width_px"], prod["height_px"]]:
            raise SystemExit(f"{scene['id']}: {scene['local_file']} is {master.size}, the record says "
                             f"{prod['width_px']} x {prod['height_px']}; run scripts/build_imagery.py first")
        pixel_hash = sha256_bytes(master.tobytes() + f"|webp|{WEBP_QUALITY}|m6c".encode())[:8]
        derivatives = []
        for width in scene["widths"]:
            if width > master.width:
                raise SystemExit(f"{scene['id']}: {width} px would upscale a {master.width} px master")
            height = round(master.height * width / master.width)
            image = master if width == master.width else master.resize((width, height), Image.LANCZOS)
            buf = io.BytesIO()
            image.save(buf, "WEBP", quality=WEBP_QUALITY, method=6)
            data = buf.getvalue()
            rel = f"assets/imagery/{scene['id']}-{pixel_hash}-{width}.webp"
            files[rel] = data
            derivatives.append({
                "path": rel,
                "role": ROLE,
                "width_px": width,
                "height_px": height,
                "format": "image/webp",
                "operation": (f"WebP quality {WEBP_QUALITY} encode of the master at its native {width} px; no resize"
                              if width == master.width else
                              f"Lanczos3 downscale of {scene['local_file']} to {width} px, then WebP quality {WEBP_QUALITY}"),
                "bytes": len(data),
                "sha256": sha256_bytes(data),
            })
        record = dict(scene)
        record["master"] = {
            "path": scene["local_file"],
            "sha256": sha256_bytes(master_bytes),
            "bytes": len(master_bytes),
            "size_px": [master.width, master.height],
            "ground_resolution_m": 30.0,
        }
        record["pixel_hash8"] = pixel_hash
        record["operations"] = ["Lanczos3 downscale where a derivative is narrower than the master", "WebP encode"]
        record["operations_not_used"] = ["crop", "tone or colour change", "sharpening", "upscaling", "generative or AI step"]
        record["derivatives"] = derivatives
        record["max_safe_rendered_px"] = {
            "device_px": master.width,
            "basis": "native 30 m Landsat at the master's own pixel width; nothing is upscaled at or below that many device px",
        }
        record["label_point"] = {
            "lat": prod["center_lat"],
            "lon": prod["center_lon"],
            "basis": "the centre of the scene, which the caption names",
        }
        # The measured placement is written by scripts/measure_interior_renders.py after a browser run.
        record["rendered"] = scene.get("rendered")
        records.append(record)
    return files, records


def merged_manifest(records: list[dict], root: pathlib.Path) -> dict:
    manifest = json.loads((root / "assets" / "imagery" / "sources.json").read_text(encoding="utf-8"))
    manifest["web_m6"]["context_scenes"] = records
    return manifest


def main(argv: list[str]) -> int:
    check = "--check" in argv
    files, records = build()
    manifest = merged_manifest(records, ROOT)
    text = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    drift = []
    for rel, data in files.items():
        path = ROOT / rel
        if not path.is_file() or path.read_bytes() != data:
            drift.append(rel)
    if MANIFEST.read_text(encoding="utf-8") != text:
        drift.append("assets/imagery/sources.json")
    if check:
        for rel in drift:
            print(f"differs from a fresh build: {rel}")
        print("build_m6_context_scenes --check: " + ("OK" if not drift else "DRIFT"))
        return 1 if drift else 0
    for rel, data in files.items():
        (ROOT / rel).write_bytes(data)
    MANIFEST.write_text(text, encoding="utf-8")
    for rel in sorted(files):
        print(f"{rel}  {len(files[rel]) / 1024:.0f} KiB")
    print("sources.json -> web_m6.context_scenes updated")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
