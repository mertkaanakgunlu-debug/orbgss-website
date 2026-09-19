#!/usr/bin/env python3
"""WEB-005B Act 2: natural-colour re-render of the accepted Kizildere context scene.

Same USGS product (LC08_L2SP_179034_20250505_02_T1) as the GEO-WEB-002 context master
(`geo_web_002.context_scenes[kizildere-aoi-context-2025]`), fetched and warped at native 30 m by the
unchanged `scripts/build_imagery.py` code. Two things differ:

1. The frame. WEB-005B shows Act 2 full-bleed. A 2400 px master cannot fill a 1440 CSS px band on a
   2x display without browser upscaling, so the frame is widened in the same product, not
   stretched: 3200 x 1800 px (96 x 54 km) at native 30 m, centred exactly on the analysis-grid
   centre, so the 36 km AOI sits at a known, centred position (recorded as `aoi_in_frame`).
2. The tone rendering, which is the point of the change:

The GEO-WEB-002 render stretched each band to its OWN 1-99 percentile range and then applied a
1.65 gamma and 1.2 saturation. Per-band stretching throws away the scene's colour balance
(each channel is forced to the same range, so whatever colour dominates is neutralised and
the rest is pushed into casts), which is what made the photograph read as a processed raster.
This render keeps the bands in ONE common reflectance scale, so relative colour is the sensor's:

  surface reflectance (USGS C2 L2 scaling)
  -> uniform haze offset (one value, the scene's dark-object reflectance, subtracted from all bands)
  -> one white point for all three bands (a high percentile of the band maximum)
  -> sRGB transfer (display encoding of linear reflectance)
  -> gentle global S-curve and mild luminance-preserving saturation, fixed parameters

Global, deterministic operations only: no local contrast, no sharpening, no per-band stretch, no
generative step. The pixels remain USGS Landsat public-domain data.

Usage (needs the build_imagery.py requirements):
    python scripts/build_web005b_context.py --cache <dir>            # fetch once, cache the SR stack
    python scripts/build_web005b_context.py --cache <dir> --record   # write files + sources.json
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import io
import json
import pathlib
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_imagery as bi  # noqa: E402  (the recorded pipeline's own fetch/warp code)

ROOT = bi.ROOT
MANIFEST = bi.MANIFEST
SCENE_ID = "kizildere-aoi-context-2025"
STEM = "kizildere-aoi-context-2025-natural"
TONE = {
    "haze_percentile": 0.1,       # dark-object reflectance, one value for all bands
    "haze_keep": 0.0,             # fraction of that offset kept (0 = full dark-object subtraction)
    "white_percentile": 99.5,     # of max(R, G, B) reflectance after the haze offset
    "transfer": "sRGB OETF",
    "s_curve_strength": 0.35,     # global, centred at mid-grey
    "saturation": 1.15,           # luminance-preserving, global
}
WIDTHS = (3200, 2400, 1600, 1200, 800)
PIXEL_M = 30.0
# Analysis grid (MER-113 kizildere_mvp_v2): origin (639270, 4223040), 1200 x 1200 cells at 30 m.
AOI = {"left": 639270.0, "top": 4223040.0, "size_m": 36000.0}
# Snapped to the analysis grid's 30 m lattice. Centring on the AOI put the frame's west edge past
# the edge of the single Landsat scene (93 % coverage), and a second acquisition date is not mixed
# in, so the frame is shifted east until it lies wholly inside LC08 179/034: the AOI sits in its
# left third, with the graben running east toward Denizli.
FRAME = {"width_px": 3200, "height_px": 1800,
         "left_utm": AOI["left"] - 541 * PIXEL_M, "top_utm": AOI["top"] + 300 * PIXEL_M}
JPEG_QUALITY = 90
WEBP_QUALITY = 82


def rel(path: pathlib.Path) -> str:
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.as_posix()


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def srgb_oetf(x: np.ndarray) -> np.ndarray:
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(np.maximum(x, 0), 1 / 2.4) - 0.055)


def tone(stack: np.ndarray) -> tuple[np.ndarray, dict]:
    valid = np.all(stack > 0, axis=0)
    refl = np.clip(stack.astype(np.float64) * bi.SR_SCALE + bi.SR_OFFSET, 0.0, 1.0)
    allv = refl[:, valid]
    haze = float(np.percentile(allv.min(axis=0), TONE["haze_percentile"])) * (1 - TONE["haze_keep"])
    refl = np.clip(refl - haze, 0.0, 1.0)
    white = float(np.percentile(refl[:, valid].max(axis=0), TONE["white_percentile"]))
    lin = np.clip(refl / white, 0.0, 1.0)
    rgb = srgb_oetf(lin)
    k = TONE["s_curve_strength"]
    rgb = rgb + k * rgb * (1 - rgb) * (2 * rgb - 1)  # symmetric S around 0.5: more mid-tone contrast
    rgb = np.clip(rgb, 0, 1)
    lum = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
    rgb = np.clip(lum + (rgb - lum) * TONE["saturation"], 0.0, 1.0)
    rgb[:, ~valid] = 0.0
    out = (rgb * 255.0 + 0.5).astype(np.uint8).transpose(1, 2, 0)
    return out, {"haze_offset_reflectance": round(haze, 6), "white_point_reflectance": round(white, 6),
                 "valid_coverage": round(float(valid.mean()), 4)}


def frame_grid():
    w, h = FRAME["width_px"], FRAME["height_px"]
    left, top = FRAME["left_utm"], FRAME["top_utm"]
    return bi.from_origin(left, top, PIXEL_M, PIXEL_M), w, h


def frame_record(crs: str) -> dict:
    w, h = FRAME["width_px"], FRAME["height_px"]
    left, top = FRAME["left_utm"], FRAME["top_utm"]
    right, bottom = left + w * PIXEL_M, top - h * PIXEL_M
    to_wgs = bi.Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
    west, south = to_wgs.transform(left, bottom)
    east, north = to_wgs.transform(right, top)
    fx = lambda x: round((x - left) / (right - left), 6)  # noqa: E731
    fy = lambda y: round((top - y) / (top - bottom), 6)  # noqa: E731
    return {"crs": crs, "bounds_utm": [left, bottom, right, top],
            "bounds_wgs84": [round(west, 4), round(south, 4), round(east, 4), round(north, 4)],
            "size_px": [w, h], "resolution_m": PIXEL_M, "extent_km": f"{w * PIXEL_M / 1000:g} x {h * PIXEL_M / 1000:g}",
            "placement": "on the analysis grid's 30 m lattice; shifted east of AOI-centred so the frame lies wholly inside the single Landsat scene",
            "aoi_in_frame": {"x0": fx(AOI["left"]), "x1": fx(AOI["left"] + AOI["size_m"]),
                             "y0": fy(AOI["top"]), "y1": fy(AOI["top"] - AOI["size_m"]),
                             "basis": "36 x 36 km MER-113 analysis grid bounds, as fractions of the frame"}}


def fetch(scene: dict, cache: pathlib.Path) -> np.ndarray:
    prod = scene["production"]
    cached = cache / f"{SCENE_ID}-{FRAME['width_px']}x{FRAME['height_px']}-sr.npy"
    if cached.exists():
        return np.load(cached)
    catalog = bi.Client.open(bi.STAC, modifier=bi.pc.sign_inplace)
    items = bi.fetch_items(catalog, prod["product_ids"])
    with bi.rasterio.Env(**bi.GDAL_ENV):
        with bi.rasterio.open(items[0].assets["red"].href) as ref:
            crs = ref.crs
        if str(crs) != prod["render"]["crs"]:
            raise SystemExit(f"scene CRS {crs} differs from the recorded {prod['render']['crs']}")
        transform, width, height = frame_grid()
        stack = np.stack([bi.read_band(items, b, crs, transform, width, height) for b in bi.BANDS])
    cache.mkdir(parents=True, exist_ok=True)
    np.save(cached, stack)
    return stack


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cache", type=pathlib.Path, required=True, help="directory for the cached SR stack (outside the repo)")
    ap.add_argument("--out", type=pathlib.Path, default=ROOT / "assets" / "imagery")
    ap.add_argument("--record", action="store_true", help="write sources.json -> web_005b.context")
    args = ap.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    scene = next(s for s in manifest["geo_web_002"]["context_scenes"] if s["id"] == SCENE_ID)
    stack = fetch(scene, args.cache)
    rgb, resolved = tone(stack)
    if resolved["valid_coverage"] < 1.0:
        raise SystemExit(f"frame is not fully inside the scene: valid coverage {resolved['valid_coverage']}")
    args.out.mkdir(parents=True, exist_ok=True)
    master = args.out / f"{STEM}.jpg"
    Image.fromarray(rgb, "RGB").save(master, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True, subsampling=0)
    img = Image.fromarray(rgb, "RGB")
    derivs = []
    for w in WIDTHS:
        h = round(w * rgb.shape[0] / rgb.shape[1])
        path = args.out / f"{STEM}-{w}.webp"
        px = img if w == rgb.shape[1] else img.resize((w, h), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        px.save(buf, "WEBP", quality=WEBP_QUALITY, method=6)
        path.write_bytes(buf.getvalue())
        derivs.append({"path": rel(path), "role": "act2-context-responsive",
                       "width": w, "height": h, "format": "image/webp",
                       "operation": ("WebP quality %d encode of the rendered frame at native %d px; no resize" % (WEBP_QUALITY, w))
                       if w == rgb.shape[1] else
                       ("lanczos3 downscale of the rendered frame to %d px, then WebP quality %d; no crop, colour or tone change" % (w, WEBP_QUALITY)),
                       "bytes": path.stat().st_size, "sha256": sha(path)})
    record = {
        "id": "act2-context-natural",
        "supersedes_on_homepage": "geo_web_002.assets[act2-context] (same product, wider frame at the same 30 m; retained, no longer placed)",
        "context_scene_id": SCENE_ID,
        "public_role": "context",
        "asset_class": "A - OrbGSS natural-colour Landsat composite",
        "source": {k: scene["production"][k] for k in ("product_ids",)} | {
            "data": "USGS Landsat Collection 2 Level-2 Science Products (surface reflectance, OLI bands 4/3/2)",
            "acquired": scene["acquired"], "sensor": scene["sensor"],
            "access": "Microsoft Planetary Computer STAC API, collection 'landsat-c2-l2', anonymous read",
            "fetch_and_warp": "scripts/build_imagery.py fetch_items / read_band (cubic warp onto the 30 m frame grid), unchanged"},
        "frame": frame_record(scene["production"]["render"]["crs"]),
        "derivation": {"pipeline": "scripts/build_web005b_context.py", "tone": TONE, "resolved": resolved,
                       "operations_not_used": ["per-band stretch", "local contrast", "sharpening", "generative or AI step"]},
        "master": {"file": rel(master), "format": "image/jpeg", "dimensions": [rgb.shape[1], rgb.shape[0]],
                   "jpeg_quality": JPEG_QUALITY, "chroma_subsampling": "4:4:4", "bytes": master.stat().st_size, "sha256": sha(master)},
        "derivatives": derivs,
        "max_safe_rendered_px": {"device_px": FRAME["width_px"], "basis": "native 30 m Landsat at %d px; nothing is upscaled at or below that many device px" % FRAME["width_px"]},
        "rights_basis": "USGS Landsat data are in the public domain; permission is not required and there are no restrictions on use or redistribution. Only the crop, tone rendering and encoding are OrbGSS work.",
        "attribution_requirement": "Landsat data courtesy of the U.S. Geological Survey.",
        "mandatory_warning_i18n_key": "act.context.note",
        "rendered_on": datetime.date.today().isoformat(),
    }
    if args.record:
        manifest.setdefault("web_005b", {})["context"] = record
        MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    json.dump(record, sys.stdout, indent=1, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
