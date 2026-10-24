#!/usr/bin/env python3
"""Build the self-hosted fonts (Atlas redesign, MER-275).

OrbGSS Sans 300 / 400 and OrbGSS Mono 400 are Latin + Latin-1 + Turkish subsets of IBM Plex Sans Light,
IBM Plex Sans Regular and IBM Plex Mono Regular, taken unmodified from IBM's npm releases
(@ibm/plex-sans 1.1.0, @ibm/plex-mono 1.1.0; SIL Open Font License 1.1). IBM reserves the font name
"Plex", so the name table of every subset is renamed to "OrbGSS Sans" / "OrbGSS Mono"; the copyright,
trademark and licence strings stay (assets/fonts/OFL.txt carries the full licence).

    python scripts/build_fonts.py            # download (cdn.jsdelivr.net), verify, subset, write
    python scripts/build_fonts.py --check    # rebuild into memory and compare with the committed record

Local tooling only (fontTools + brotli); nothing here runs on the site. The encodes are hash-named
because /assets/ is served immutable. The result is recorded in assets/fonts/fonts.json, which
scripts/validate_site.py recomputes on every run.
"""
from __future__ import annotations

import hashlib
import io
import json
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "fonts"
RECORD = OUT / "fonts.json"

CDN = "https://cdn.jsdelivr.net/npm/"
# Upstream files and their SHA-256 as published in the npm releases (verified on download).
UPSTREAM = {
    "sans-300": ("@ibm/plex-sans@1.1.0/fonts/complete/woff2/IBMPlexSans-Light.woff2",
                 "769209c2a0dbf2e3f012c22e4c604100cb3f1e7b8beb0ef77bc7d982d85509cc"),
    "sans-400": ("@ibm/plex-sans@1.1.0/fonts/complete/woff2/IBMPlexSans-Regular.woff2",
                 "ba711a3085ff9f27440b6b9c4550cfc47c97bf36591d5da958b975bb3add8c1a"),
    "mono-400": ("@ibm/plex-mono@1.1.0/fonts/complete/woff2/IBMPlexMono-Regular.woff2",
                 "49ce58b41a0e1cb921c0f58d9a5b8b96a2cc21437c7066f3ba4f24873076d131"),
}
# family, style, full name, PostScript name, weight
FACES = {
    "sans-300": ("OrbGSS Sans", "Light", "OrbGSS Sans Light", "OrbGSSSans-Light", 300),
    "sans-400": ("OrbGSS Sans", "Regular", "OrbGSS Sans Regular", "OrbGSSSans-Regular", 400),
    "mono-400": ("OrbGSS Mono", "Regular", "OrbGSS Mono Regular", "OrbGSSMono-Regular", 400),
}
# The design package's Latin-TR range plus the four diagonal arrows (U+2196-2199) that the Sources
# page draws as an external-link mark. One subset serves English and Turkish alike.
RANGE = ("U+0020-007E, U+00A0-00FF, U+011E-011F, U+0130-0131, U+0152-0153, U+015E-015F, U+2007, U+2009, "
         "U+2011, U+2013-2014, U+2018-201A, U+201C-201E, U+2022, U+2026, U+2030, U+2032-2033, U+2039-203A, "
         "U+2070, U+2074-2079, U+20AC, U+2122, U+2190-2193, U+2196-2199, U+2212, U+2248, U+2260, "
         "U+2264-2265, U+FFFD")


def codepoints(spec: str) -> list[int]:
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()[2:]
        if "-" in part:
            lo, hi = part.split("-")
            out += range(int(lo, 16), int(hi, 16) + 1)
        else:
            out.append(int(part, 16))
    return out


def fetch(path: str) -> bytes:
    with urllib.request.urlopen(CDN + path, timeout=60) as resp:  # noqa: S310 - fixed https host
        return resp.read()


def subset_face(data: bytes, family: str, style: str, full: str, ps: str) -> bytes:
    from fontTools import subset
    from fontTools.ttLib import TTFont

    opts = subset.Options()
    opts.layout_features = ["*"]      # keep kerning, ligatures, tabular and Turkish locl features
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    opts.glyph_names = False
    opts.hinting = True               # IBM's autohinted outlines read better at the 10 px caption size on Windows
    opts.flavor = "woff2"
    font = TTFont(io.BytesIO(data), recalcTimestamp=False)  # keep the build reproducible
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=codepoints(RANGE))
    sub.subset(font)
    for rec in font["name"].names:
        if rec.nameID in (1, 16):
            rec.string = family
        elif rec.nameID in (2, 17):
            rec.string = style
        elif rec.nameID == 4:
            rec.string = full
        elif rec.nameID == 6:
            rec.string = ps
        elif rec.nameID == 3:
            rec.string = ps + ";subset"
    font.flavor = "woff2"
    buf = io.BytesIO()
    font.save(buf)
    return buf.getvalue()


def build() -> dict:
    record = {"unicode_range": RANGE, "upstream_licence": "SIL OFL 1.1", "faces": {}}
    files: dict[str, bytes] = {}
    for key, (path, upstream_sha) in UPSTREAM.items():
        data = fetch(path)
        got = hashlib.sha256(data).hexdigest()
        if got != upstream_sha:
            raise SystemExit(f"{path}: upstream SHA-256 {got} != pinned {upstream_sha}")
        family, style, full, ps, weight = FACES[key]
        out = subset_face(data, family, style, full, ps)
        sha = hashlib.sha256(out).hexdigest()
        name = f"orbgss-{key}.{sha[:8]}.woff2"
        files[name] = out
        record["faces"][key] = {
            "file": name, "family": family, "weight": weight, "bytes": len(out), "sha256": sha,
            "upstream": {"package_file": path, "sha256": upstream_sha},
        }
    return {"record": record, "files": files}


def main() -> int:
    check = "--check" in sys.argv
    built = build()
    text = json.dumps(built["record"], indent=2, ensure_ascii=False) + "\n"
    if check:
        committed = json.loads(RECORD.read_text(encoding="utf-8"))
        same = committed == built["record"]
        print("fonts.json " + ("matches a fresh build" if same else "DIFFERS from a fresh build"))
        return 0 if same else 1
    OUT.mkdir(parents=True, exist_ok=True)
    for stale in OUT.glob("orbgss-*.woff2"):
        stale.unlink()
    for name, data in built["files"].items():
        (OUT / name).write_bytes(data)
    RECORD.write_text(text, encoding="utf-8")
    total = sum(len(d) for d in built["files"].values())
    print(f"wrote {len(built['files'])} fonts, {total} bytes ({total / 1024:.1f} KiB) and {RECORD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
