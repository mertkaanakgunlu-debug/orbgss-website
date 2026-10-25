#!/usr/bin/env python3
"""Build the deployed brand assets (Heat Trace identity, brand package Final_v3).

The CTO decided on this identity on 2026-10-25 (palette 6a "Heat Trace": Plum #371641, Magma #CD1B74, Amber #FFA323,
Glow #FEF1A1; dark-background values Violet #854AA6, Magma #E43386, Amber #FFAA2E, Glow #FFF4A5; ground Night #160A19,
wordmark Mist #F5EFF7). The supplied package ("OrbGSS Logo Tasarım4.zip", folder Final_v3/) is the source of every file
written here (it replaces the Agate package of MER-279):

    python scripts/build_brand_assets.py --source <unpacked Final_v3/ folder>           # write
    python scripts/build_brand_assets.py --source <unpacked Final_v3/ folder> --check   # compare with the record

What it does, and nothing more:
  * copies the horizontal logo for light grounds, the favicon tile, the 180 px touch icon and the 192 / 512 px
    manifest icons into assets/brand/, named <stem>.<first 8 of SHA-256>.<ext> because /assets/ is served
    immutable for a year (a changed logo must be a new file name);
  * copies favicon.ico to the site root byte for byte (browsers ask for /favicon.ico by that path);
  * removes the <metadata> element (an embedded C2PA provenance manifest, about 8 KB per SVG that no browser
    reads and that no longer verifies once the file is touched) and its xmlns:c2pa declaration from each SVG.
    The drawing is not changed: the validator checks that every colour in each shipped SVG is a brand colour;
  * records source path, source SHA-256, shipped path, shipped SHA-256 and bytes in assets/brand/brand.json,
    which scripts/validate_site.py recomputes on every run.

Local tooling, Python standard library only. Nothing here runs on the site.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "brand"
RECORD = OUT / "brand.json"

# role -> (source path inside final/, shipped stem, extension, what it is for)
FILES = {
    "logo-light": ("logo/orbgss-logo-light.svg", "orbgss-logo-light", "svg",
                   "horizontal logo for light grounds: header and footer on every page"),
    "favicon": ("favicon/favicon.svg", "orbgss-favicon", "svg",
                "favicon tile, Night with the dark-ground symbol (32 px design size)"),
    "apple-touch-icon": ("favicon/apple-touch-icon.png", "orbgss-apple-touch-icon", "png",
                         "180 px full-bleed touch icon"),
    "icon-192": ("favicon/icon-192.png", "orbgss-icon-192", "png", "192 px web-app manifest icon"),
    "icon-512": ("favicon/icon-512.png", "orbgss-icon-512", "png", "512 px web-app manifest icon"),
}
ICO = ("favicon/favicon.ico", "favicon.ico")  # shipped at the site root, unchanged

# The package the files were taken from (SHA-256 of the zip as supplied). The per-file source hashes in brand.json are
# what the validator pins; this one only names the delivery they came from.
PACKAGE = {"name": "OrbGSS Logo Tasarım4.zip", "sha256": "cc5f769be1007a4929618237203218b94319454325188b8ea409fd53ee625635"}

PALETTE = {
    "light": {"plum": "#371641", "magma": "#CD1B74", "amber": "#FFA323", "glow": "#FEF1A1"},
    "dark": {"violet": "#854AA6", "magma": "#E43386", "amber": "#FFAA2E", "glow": "#FFF4A5", "night": "#160A19", "mist": "#F5EFF7"},
}

METADATA = re.compile(r"<metadata>.*?</metadata>", re.S)
C2PA_NS = re.compile(r'\s+xmlns:c2pa="[^"]*"')


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def clean_svg(data: bytes) -> bytes:
    text = data.decode("utf-8")
    text = METADATA.sub("", text)
    text = C2PA_NS.sub("", text)
    return text.encode("utf-8")


def build(source: pathlib.Path) -> tuple[dict[pathlib.Path, bytes], dict]:
    files: dict[pathlib.Path, bytes] = {}
    entries: dict[str, dict] = {}
    for role, (rel, stem, ext, purpose) in FILES.items():
        raw = (source / rel).read_bytes()
        data = clean_svg(raw) if ext == "svg" else raw
        digest = sha256(data)
        name = f"{stem}.{digest[:8]}.{ext}"
        files[OUT / name] = data
        entries[role] = {
            "file": name,
            "purpose": purpose,
            "bytes": len(data),
            "sha256": digest,
            "source": {"path": f"Final_v3/{rel}", "bytes": len(raw), "sha256": sha256(raw)},
            "transform": ("metadata element and its xmlns:c2pa declaration removed; drawing unchanged"
                          if ext == "svg" else "none (byte for byte)"),
        }
    raw = (source / ICO[0]).read_bytes()
    files[ROOT / ICO[1]] = raw
    entries["favicon-ico"] = {
        "file": f"../../{ICO[1]}",
        "purpose": "multi-size favicon (16, 32, 48 px) at the site root, where browsers ask for it",
        "bytes": len(raw),
        "sha256": sha256(raw),
        "source": {"path": f"Final_v3/{ICO[0]}", "bytes": len(raw), "sha256": sha256(raw)},
        "transform": "none (byte for byte)",
    }
    record = {
        "identity": "Heat Trace",
        "approved": "CTO, 2026-10-25 (brand package Final_v3)",
        "package": f"{PACKAGE['name']}, folder Final_v3/ (Final_v2/ and the older Agate folder final/ are superseded and not used)",
        "package_sha256": PACKAGE["sha256"],
        "palette": PALETTE,
        "rules": {
            "magma": "the interactive accent: links, active navigation, focus",
            "amber": "a restrained highlight and a non-text mark; never a button fill and never body text on a light ground",
            "glow": "the logo's orb only; never a UI colour",
            "map": "the area of interest is a dashed Magma #E43386 callout with a Night halo; Amber and Glow are never drawn on a map",
            "minimum_sizes": "horizontal logo 120 px wide, symbol 32 px; below that the app icon",
        },
        "not_used": "Final_v3/assets/illustrative-map.jpg is a generated illustration and is not placed on any page",
        "files": entries,
    }
    files[RECORD] = (json.dumps(record, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    return files, record


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=pathlib.Path, help="the unpacked Final_v3/ folder of the brand package")
    ap.add_argument("--check", action="store_true", help="compare with the committed files instead of writing")
    args = ap.parse_args()
    files, _ = build(args.source)
    if args.check:
        bad = [str(p.relative_to(ROOT)) for p, data in files.items() if not p.is_file() or p.read_bytes() != data]
        if bad:
            print("brand assets differ from a fresh build:", *bad, sep="\n  ")
            return 1
        print(f"brand assets match a fresh build ({len(files)} files)")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    keep = {p.name for p in files if p.parent == OUT}
    for old in OUT.iterdir():
        if old.is_file() and old.name not in keep:
            old.unlink()
    for path, data in files.items():
        path.write_bytes(data)
        print("wrote", path.relative_to(ROOT), len(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
