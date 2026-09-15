#!/usr/bin/env python3
"""Build the GEO-WEB-002 final homepage visual derivatives (task MER-102).

Two asset classes, two very different rules, one deterministic script:

* **Class A — Act-2 Kızıldere context.** ``scripts/build_imagery.py`` renders the natural-colour
  Landsat master from the pinned USGS Collection 2 Level-2 product; this script only resizes and
  re-encodes it to the responsive WebP candidates. No crop, no colour/tone/gamma change.

* **Class B — Acts 3 and 4 cartographic masters.** Each master is an accepted GEO-039 Workbench
  cartographic export of the persisted ``kizildere_mvp_v2`` project. This script verifies the
  master against the SHA-256 in its own ``export_manifest.json``, crops the rendered map panel and
  the compact in-frame legend, and downscales the panel to at most the project grid's native cell
  count. Crop, downscale and encode only: never a re-colour, re-projection, re-classification,
  value change or upscale.

The map panel of a 36 km x 36 km, 30 m project grid is 1200 x 1200 real cells. The renderer draws
it at ~1249 px, so 1200 px is the largest honest derivative width — anything wider would be
invented resolution. That ceiling is what ``max_safe_rendered_px`` in the manifest reports.

Usage::

    python scripts/build_final_visual_masters.py                 # build, print inventory
    python scripts/build_final_visual_masters.py --record        # also write sources.json
    python scripts/build_final_visual_masters.py --exports-root <dir>

Requires: pillow.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "imagery" / "sources.json"

#: Where the accepted GEO-039 exports of the persisted Kızıldere project live. These are read-only
#: inputs from the Science repository; nothing in this script writes there.
DEFAULT_EXPORTS_ROOT = (
    ROOT.parent / "geothermal-prospectivity" / "outputs" / "kizildere_mvp_v2" / "exports"
)

#: Interior of the rendered map axes in the 2338 x 1654 A4/200 dpi master, inset by the axes spine.
#: Identical to the accepted WEB-002 crop so both generations frame the same ground.
MAP_CROP_BOX = (179, 186, 1428, 1435)
#: The compact legend block: layer title with units, the governed colour ramp and its ticks. Cropped
#: at native master resolution and shipped lossless so WEB-005 can place a truthful legend *inside*
#: the map frame instead of a detached homepage colour bar.
LEGEND_CROP_BOX = (1552, 170, 2284, 292)

#: Native cell count of the accepted project grid: 36 km / 30 m. The real information content of
#: every class-B map panel, and the reason no derivative is ever widened past the master's panel.
NATIVE_GRID_PX = 1200
#: The largest derivative is the map panel at the master's own pixels: crop only, no resampling at
#: all. The card derivative is a plain downscale of the same crop.
PANEL_CARD_WIDTH = 800
PANEL_WEBP_QUALITY = 82

CONTEXT_WIDTHS = (2400, 1800, 1200, 900)
CONTEXT_WEBP_QUALITY = 76

PROOF_DIR = "assets/proof/final"

#: Class-B assets. ``layer_ids`` and ``public_label`` follow docs/WEB-002_SCIENCE_ASSET_PACKAGE.md
#: verbatim; the export ids are the accepted materialized masters for those recipes.
CARTOGRAPHIC_ASSETS = [
    {
        "id": "terrain",
        "export_id": "20260915T104731Z-00fae5eb",
        "layer_ids": ["top-dem"],
        "public_label": "Elevation — NASADEM context",
    },
    {
        "id": "thm01",
        "export_id": "20260915T104733Z-cfba9119",
        "layer_ids": ["thm-thm01"],
        "public_label": "THM-01 Thermal Anomaly",
    },
    {
        "id": "alt01",
        "export_id": "20260915T104801Z-eb1bc414",
        "layer_ids": ["alt-alt01"],
        "public_label": "ALT-01 Alteration Proxy — clay/hydroxyl",
    },
    {
        "id": "alt02",
        "export_id": "20260915T104804Z-1f837163",
        "layer_ids": ["alt-alt02"],
        "public_label": "ALT-02 Alteration Proxy — ferric/iron",
    },
    {
        "id": "priority",
        "export_id": "20260915T104736Z-55609249",
        "layer_ids": ["score-mvp-remote-sensing-priority"],
        "public_label": "Remote-Sensing Relative Priority — Experimental Baseline",
    },
]


def sha256_of(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def describe(rel: str, role: str, operation: str, size: tuple[int, int]) -> dict:
    path = ROOT / rel
    return {
        "path": rel,
        "role": role,
        "width": size[0],
        "height": size[1],
        "format": "image/webp" if rel.endswith(".webp") else "image/png",
        "operation": operation,
        "bytes": path.stat().st_size,
        "sha256": sha256_of(path),
    }


def build_context(scene: dict) -> list[dict]:
    """Resize-and-encode responsive WebP candidates from the natural-colour Landsat master."""
    master = ROOT / scene["local_file"]
    if not master.is_file():
        raise SystemExit(
            f"Act-2 context master is missing: {scene['local_file']}. Build it first with "
            f"scripts/build_imagery.py {scene['id']} --record"
        )
    stem = master.stem
    source = Image.open(master).convert("RGB")
    derivatives = []
    for width in CONTEXT_WIDTHS:
        height = round(source.height * width / source.width)
        rel = f"assets/imagery/{stem}-{width}.webp"
        out = ROOT / rel
        image = source if width == source.width else source.resize((width, height), Image.LANCZOS)
        image.save(out, "WEBP", quality=CONTEXT_WEBP_QUALITY, method=6)
        derivatives.append(
            describe(
                rel,
                "act2-context-responsive",
                f"lanczos3 downscale of {scene['local_file']} to {width} px, then WebP "
                f"quality {CONTEXT_WEBP_QUALITY}; no crop, no colour, tone or gamma change"
                if width != source.width
                else f"WebP quality {CONTEXT_WEBP_QUALITY} re-encode of {scene['local_file']} at "
                f"native {width} px; no resize, crop, colour, tone or gamma change",
                (width, height),
            )
        )
    return derivatives


def build_cartographic(asset: dict, exports_root: pathlib.Path) -> dict:
    """Verify one accepted master, then crop/downscale its map panel and legend for the web."""
    export_dir = exports_root / asset["export_id"]
    manifest_path = export_dir / "export_manifest.json"
    master_path = export_dir / "map.png"
    if not manifest_path.is_file() or not master_path.is_file():
        raise SystemExit(f"accepted GEO-039 export not found: {export_dir}")

    export_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    output = next(o for o in export_manifest["outputs"] if o["file_name"] == "map.png")
    recorded = str(output["checksum_sha256"])
    actual = sha256_of(master_path)
    if recorded != actual:
        raise SystemExit(
            f"{asset['id']}: master checksum mismatch against its own export manifest "
            f"({recorded[:12]}… != {actual[:12]}…) — refusing to derive from an altered master"
        )
    manifest_layers = [layer["layer_id"] for layer in export_manifest["layers"]]
    if manifest_layers != asset["layer_ids"]:
        raise SystemExit(
            f"{asset['id']}: export {asset['export_id']} renders {manifest_layers}, "
            f"expected {asset['layer_ids']}"
        )

    grid = export_manifest["grid"]
    if (grid["width"], grid["height"]) != (NATIVE_GRID_PX, NATIVE_GRID_PX):
        raise SystemExit(
            f"{asset['id']}: export grid is {grid['width']}x{grid['height']}, not the "
            f"{NATIVE_GRID_PX}x{NATIVE_GRID_PX} cells the recorded crop and resolution ceiling assume"
        )

    master = Image.open(master_path).convert("RGB")
    panel = master.crop(MAP_CROP_BOX)
    if PANEL_CARD_WIDTH > panel.width:
        raise SystemExit(
            f"{asset['id']}: refusing to upscale — panel is {panel.width} px, "
            f"card derivative asks for {PANEL_CARD_WIDTH} px"
        )

    out_dir = ROOT / PROOF_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    derivatives = []
    rel = f"{PROOF_DIR}/{asset['id']}-{panel.width}.webp"
    panel.save(ROOT / rel, "WEBP", quality=PANEL_WEBP_QUALITY, method=6)
    derivatives.append(
        describe(
            rel,
            f"panel-native-{panel.width}",
            f"presentation crop {list(MAP_CROP_BOX)} of the rendered map panel, WebP quality "
            f"{PANEL_WEBP_QUALITY}; crop and encode only, no resampling",
            (panel.width, panel.height),
        )
    )
    rel = f"{PROOF_DIR}/{asset['id']}-{PANEL_CARD_WIDTH}.webp"
    panel.resize((PANEL_CARD_WIDTH, PANEL_CARD_WIDTH), Image.LANCZOS).save(
        ROOT / rel, "WEBP", quality=PANEL_WEBP_QUALITY, method=6
    )
    derivatives.append(
        describe(
            rel,
            f"panel-{PANEL_CARD_WIDTH}",
            f"presentation crop {list(MAP_CROP_BOX)} of the rendered map panel ({panel.width} px), "
            f"lanczos3 downscale to {PANEL_CARD_WIDTH} px, WebP quality {PANEL_WEBP_QUALITY}; "
            f"crop and downscale only",
            (PANEL_CARD_WIDTH, PANEL_CARD_WIDTH),
        )
    )

    legend = master.crop(LEGEND_CROP_BOX)
    legend_rel = f"{PROOF_DIR}/{asset['id']}-legend.png"
    legend.save(ROOT / legend_rel, "PNG", optimize=True)
    derivatives.append(
        describe(
            legend_rel,
            "in-frame-legend",
            f"presentation crop {list(LEGEND_CROP_BOX)} of the master's governed legend block "
            f"at native resolution, lossless PNG; no resize, recolour or relabel",
            legend.size,
        )
    )

    return {
        "export": {
            "mechanism": "GEO-039 Workbench cartographic export (PNG master)",
            "export_id": asset["export_id"],
            "export_manifest": (
                f"geothermal-prospectivity/outputs/kizildere_mvp_v2/exports/"
                f"{asset['export_id']}/export_manifest.json"
            ),
            "master_file": (
                f"geothermal-prospectivity/outputs/kizildere_mvp_v2/exports/"
                f"{asset['export_id']}/map.png"
            ),
            "master_sha256": actual,
            "master_bytes": master_path.stat().st_size,
            "master_dimensions": [master.width, master.height],
            "master_format": "image/png",
            "rendered_title": export_manifest["title"],
            "renderer_revision": export_manifest["renderer_revision"],
            "plan_sha256": export_manifest["plan_sha256"],
            "config_hash": export_manifest["config_hash"],
            "attribution": export_manifest["attribution"],
        },
        "map_panel_px": [panel.width, panel.height],
        "derivatives": derivatives,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--exports-root", type=pathlib.Path, default=DEFAULT_EXPORTS_ROOT)
    parser.add_argument(
        "--record", action="store_true", help="write the built inventory back into sources.json"
    )
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    package = manifest.get("geo_web_002")
    if not package:
        raise SystemExit("sources.json has no geo_web_002 package block")

    built: dict[str, dict] = {}

    scene = package["context_scenes"][0]
    context_derivatives = build_context(scene)
    scene["derivatives"] = context_derivatives
    built["act2-context"] = {"derivatives": context_derivatives}

    for asset in CARTOGRAPHIC_ASSETS:
        built[asset["id"]] = build_cartographic(asset, args.exports_root)

    if args.record:
        recorded = 0
        for entry in package.get("assets", []):
            key = entry.get("id")
            if key not in built:
                continue
            payload = built[key]
            if "export" in payload:
                entry["export"] = {**entry.get("export", {}), **payload["export"]}
                entry["map_panel_px"] = payload["map_panel_px"]
            entry["derivatives"] = payload["derivatives"]
            recorded += 1
        MANIFEST.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"recorded {recorded} asset(s) in {MANIFEST.relative_to(ROOT)}")

    total = 0
    for key, payload in built.items():
        print(f"\n{key}")
        for deriv in payload["derivatives"]:
            total += deriv["bytes"]
            print(
                f"  {deriv['path']:<52} {deriv['width']:>5} x {deriv['height']:<5} "
                f"{deriv['bytes']:>9,} B  {deriv['sha256'][:16]}…"
            )
    print(f"\ntotal shipped bytes: {total:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
