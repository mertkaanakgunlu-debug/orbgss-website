#!/usr/bin/env python3
"""Build the responsive WebP derivatives for the WEB-005B domain cards.

The three domain illustrations (geothermal, mineral, environmental) are locked
WEB-001 scenes that were retired from the homepage when WEB-002 replaced the
temporary gallery with real product proof. WEB-005B places them again, but as
explicitly illustrative photography beside a domain's status — never as
evidence — so they need the same responsive treatment crater-lake already has.

The operation is resize-and-encode only, exactly like the recorded crater-lake
derivatives: a Lanczos downscale of the recorded master followed by a WebP
encode. No crop, no colour, tone or gamma change. Every output is written back
into ``assets/imagery/sources.json`` under its scene's ``derivatives`` list with
its width, height, byte size and SHA-256, so scripts/validate_site.py can
recompute them on every run.

Usage:
    py -3.14 scripts/build_domain_derivatives.py
"""
from __future__ import annotations

import hashlib
import json
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "imagery" / "sources.json"

# Measured, not assumed (scratchpad measure.py, 19 widths x DPR 1 and 2). The lead card spans the
# full 1280 px shell and asks for 2560 px at 2x, so it needs a candidate at or above that: the
# 2880 px master width is the widest honest one. The two secondary cards sit at half the shell on
# desktop but stack to the full content width below 821 px, where they measure 728 CSS px and ask
# for 1456 at 2x — so 1400 is not enough for them and 1800 is.
WIDTHS = {
    "yellowstone-2013": (900, 1400, 1800, 2400, 2880),
    "chuquicamata-2024": (900, 1400, 1800),
    "ili-delta-2020": (900, 1400, 1800),
}
QUALITY = 82
ROLE = "domain-card-responsive"


def sha256_of(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    scenes = {scene["id"]: scene for scene in manifest["scenes"]}

    for scene_id, widths in WIDTHS.items():
        scene = scenes[scene_id]
        master = ROOT / scene["local_file"]
        source = Image.open(master)
        records = []
        for width in widths:
            if width > source.width:
                raise SystemExit(f"{scene_id}: {width} px would upscale the {source.width} px master")
            height = round(source.height * width / source.width)
            target = master.with_name(f"{master.stem}-{width}.webp")
            source.resize((width, height), Image.LANCZOS).save(
                target, "WEBP", quality=QUALITY, method=6
            )
            records.append({
                "path": target.relative_to(ROOT).as_posix(),
                "role": ROLE,
                "width_px": width,
                "height_px": height,
                "format": "image/webp",
                "operation": (
                    f"lanczos3 downscale of {scene['local_file']}, then WebP encode; "
                    f"no crop, no colour, tone or gamma change"
                ),
                "bytes": target.stat().st_size,
                "sha256": sha256_of(target),
            })
            print(f"  {target.relative_to(ROOT).as_posix()}  {width}x{height}  {records[-1]['bytes']} B")
        scene["derivatives"] = records

    # The manifest is committed with CRLF endings; round-tripping it any other way would
    # rewrite all 3 467 lines and bury the real change.
    MANIFEST.write_bytes(
        (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").replace("\n", "\r\n").encode("utf-8")
    )
    print(f"updated {MANIFEST.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
