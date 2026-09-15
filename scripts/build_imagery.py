#!/usr/bin/env python3
"""Build OrbGSS production imagery from USGS Landsat Collection 2 Level-2 data.

Each production scene in ``assets/imagery/sources.json`` carries a
``production`` block that pins the exact Landsat product identifiers and the
crop used on the website. This script re-creates the natural-color (OLI bands
4/3/2) composites from those public-domain surface-reflectance products so the
live assets can always be traced back to their source data.

Data access: Microsoft Planetary Computer STAC mirror of the USGS Landsat
Collection 2 Level-2 archive (anonymous, read-only). The pixels are USGS
products; only the crop, contrast stretch and JPEG encoding are OrbGSS work.

Usage:
    python scripts/build_imagery.py                 # build every recorded scene
    python scripts/build_imagery.py crater-lake-2023
    python scripts/build_imagery.py --scale 3 --out preview/   # quick 90 m previews

Requires: rasterio, numpy, pillow, pystac-client, planetary-computer.
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import sys

import numpy as np
import planetary_computer as pc
import rasterio
from PIL import Image
from pyproj import Transformer
from pystac_client import Client
from rasterio.enums import Resampling
from rasterio.transform import from_origin
from rasterio.vrt import WarpedVRT

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "imagery" / "sources.json"
STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
COLLECTION = "landsat-c2-l2"
BANDS = ("red", "green", "blue")  # OLI bands 4, 3, 2
# USGS Collection 2 Level-2 surface reflectance scaling.
SR_SCALE, SR_OFFSET = 0.0000275, -0.2
PIXEL_M = 30.0

GDAL_ENV = dict(
    GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
    CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif,.TIF",
    GDAL_HTTP_MULTIRANGE="YES",
    GDAL_HTTP_MERGE_CONSECUTIVE_RANGES="YES",
    VSI_CACHE="TRUE",
    VSI_CACHE_SIZE="268435456",
)


def fetch_items(catalog: Client, product_ids: list[str]):
    search = catalog.search(collections=[COLLECTION], ids=product_ids)
    items = {item.id: item for item in search.items()}
    missing = [pid for pid in product_ids if pid not in items]
    if missing:
        raise SystemExit(f"STAC items not found in {COLLECTION}: {missing}")
    return [items[pid] for pid in product_ids]


def output_grid(prod: dict, crs: rasterio.crs.CRS, scale: float):
    """Return (transform, width, height, bounds) for the crop in the scene CRS."""
    width = int(round(prod["width_px"] / scale))
    height = int(round(prod["height_px"] / scale))
    res = PIXEL_M * scale
    to_utm = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
    cx, cy = to_utm.transform(prod["center_lon"], prod["center_lat"])
    # anchor_x/anchor_y say where (0..1) inside the frame the center point sits.
    ax = prod.get("anchor_x", 0.5)
    ay = prod.get("anchor_y", 0.5)
    left = cx - ax * width * res
    top = cy + ay * height * res
    transform = from_origin(left, top, res, res)
    bounds = (left, top - height * res, left + width * res, top)
    return transform, width, height, bounds


def read_band(items, band: str, crs, transform, width, height) -> np.ndarray:
    """Mosaic one band from the listed items onto the output grid (first valid wins)."""
    out = np.zeros((height, width), dtype=np.uint16)
    for item in items:
        href = item.assets[band].href
        with rasterio.open(href) as src:
            with WarpedVRT(
                src,
                crs=crs,
                transform=transform,
                width=width,
                height=height,
                resampling=Resampling.cubic,
                nodata=0,
            ) as vrt:
                data = vrt.read(1)
        fill = out == 0
        out[fill] = data[fill]
    return out


def to_rgb8(stack: np.ndarray, prod: dict) -> np.ndarray:
    """Surface reflectance -> display RGB with a documented, deterministic stretch."""
    valid = np.all(stack > 0, axis=0)
    refl = stack.astype(np.float32) * SR_SCALE + SR_OFFSET
    refl = np.clip(refl, 0.0, 1.0)

    lo_pct, hi_pct = prod.get("stretch_percentiles", [0.5, 99.5])
    gamma = prod.get("gamma", 1.3)
    sat = prod.get("saturation", 1.15)

    rgb = np.zeros_like(refl)
    for i in range(3):
        band = refl[i]
        vals = band[valid]
        if "stretch_range" in prod:
            # Fixed reflectance range (used for snow scenes where percentiles
            # would be dominated by snow and crush the land into gray).
            lo, hi = prod["stretch_range"]
        else:
            lo, hi = np.percentile(vals, [lo_pct, hi_pct])
        rgb[i] = np.clip((band - lo) / max(hi - lo, 1e-6), 0.0, 1.0)

    rgb = rgb ** (1.0 / gamma)
    # Mild saturation in a luminance-preserving way.
    lum = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
    rgb = np.clip(lum + (rgb - lum) * sat, 0.0, 1.0)
    rgb[:, ~valid] = 0.0
    return (rgb * 255.0 + 0.5).astype(np.uint8).transpose(1, 2, 0)


def build_scene(catalog: Client, scene: dict, scale: float, out_dir: pathlib.Path, quality: int) -> dict:
    prod = scene["production"]
    items = fetch_items(catalog, prod["product_ids"])
    with rasterio.open(items[0].assets["red"].href) as ref:
        crs = ref.crs
    transform, width, height, bounds = output_grid(prod, crs, scale)
    print(f"[{scene['id']}] {len(items)} product(s) -> {width}x{height} px, {crs}")
    stack = np.stack([read_band(items, b, crs, transform, width, height) for b in BANDS])
    coverage = float(np.mean(np.all(stack > 0, axis=0)))
    print(f"[{scene['id']}] valid coverage {coverage:.1%}")
    rgb = to_rgb8(stack, prod)

    target = out_dir / pathlib.Path(scene["local_file"]).name
    target.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgb, "RGB").save(target, "JPEG", quality=quality, optimize=True, progressive=True, subsampling=1)
    size_kb = target.stat().st_size / 1024
    print(f"[{scene['id']}] wrote {target.relative_to(ROOT) if target.is_relative_to(ROOT) else target} ({size_kb:,.0f} KB)")

    to_wgs = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
    west, south = to_wgs.transform(bounds[0], bounds[1])
    east, north = to_wgs.transform(bounds[2], bounds[3])
    return {
        "crs": str(crs),
        "bounds_utm": [round(v, 1) for v in bounds],
        "bounds_wgs84": [round(west, 4), round(south, 4), round(east, 4), round(north, 4)],
        "coverage": round(coverage, 4),
        "size_px": [width, height],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("scenes", nargs="*", help="scene ids to build (default: all)")
    parser.add_argument("--scale", type=float, default=1.0, help="pixel-size multiplier; 1 = native 30 m")
    parser.add_argument("--out", type=pathlib.Path, default=None, help="output directory (default: assets/imagery)")
    parser.add_argument("--quality", type=int, default=82, help="JPEG quality")
    parser.add_argument("--record", action="store_true", help="write render provenance back into sources.json")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    # GEO-WEB-002: the Kizildere AOI natural-colour context master is built by this same
    # pipeline from the same ``production`` grammar, but it lives in its own package block
    # because it is published for WEB-005 rather than placed on the homepage today.
    scenes = manifest["scenes"] + manifest.get("geo_web_002", {}).get("context_scenes", [])
    if args.scenes:
        scenes = [s for s in scenes if s["id"] in args.scenes]
        unknown = set(args.scenes) - {s["id"] for s in scenes}
        if unknown:
            raise SystemExit(f"unknown scene ids: {sorted(unknown)}")
    out_dir = args.out or (ROOT / "assets" / "imagery")

    catalog = Client.open(STAC, modifier=pc.sign_inplace)
    report = {}
    with rasterio.Env(**GDAL_ENV):
        for scene in scenes:
            if "production" not in scene:
                print(f"[{scene['id']}] no production block in manifest; skipping")
                continue
            report[scene["id"]] = build_scene(catalog, scene, args.scale, out_dir, args.quality)
            if args.record and args.scale == 1.0:
                scene["production"]["render"] = {
                    **report[scene["id"]],
                    "rendered_on": datetime.date.today().isoformat(),
                    "jpeg_quality": args.quality,
                    "pipeline": "scripts/build_imagery.py",
                }
    if args.record:
        MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"recorded render provenance in {MANIFEST.relative_to(ROOT)}")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
