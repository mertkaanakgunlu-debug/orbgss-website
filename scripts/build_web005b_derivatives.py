#!/usr/bin/env python3
"""WEB-005B homepage analytical derivatives (Acts 3 and 4) under MER-108.

Builds the Terrain, THM-01, ALT-01 and Priority panels the homepage shows after the hero, from
the governed MER-113 rasters, as MER-108 website display derivatives. The governing contract is
the Science website derivative authority, which names WEB-005B as a consumer:

  geothermal-prospectivity@11c32e8d:tasks/MER-108_PUBLIC_WEB_DISPLAY_DERIVATIVE_AUTHORITY.md
  geothermal-prospectivity@d3a163bd:tasks/MER-108_NORMALIZATION_AUTHORITY_CORRECTION.md
  geothermal-prospectivity@30779547:tasks/MER-108_TERMINAL_WEBSITE_HERO_DISPLAY_AMENDMENT.yaml

The terminal hero amendment widens the transforms (display windows, gamma, smoothing, unsharp,
Lanczos upsampling) for the hero surface ONLY. Nothing here uses them: every panel is

  governed scalar + mask -> canonical normalization (d3a163bd) -> selected palette LUT
  -> governed mask to RGBA (NoData alpha 0) -> source-over onto a neutral grayscale hillshade
  from the governed DEM at a fixed analytical opacity -> optional single area (box) DOWNSAMPLE
  -> lossless WebP.

The palette stops are the frozen CTO-approved hero asset family (the same stops the accepted
WEB-005A drape states were rendered from), so the homepage reads as one palette system from the
hero payoff to the result act. The legend ramp is the unblended LUT (11c32e8d section 6).

Usage (needs rasterio, numpy, pillow):
    python scripts/build_web005b_derivatives.py            # build + verify, print manifest
    python scripts/build_web005b_derivatives.py --record   # also write sources.json -> web_005b
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import pathlib
import platform
import sys

import numpy as np
import PIL
import rasterio
from PIL import Image, features

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "imagery" / "sources.json"
OUT = ROOT / "assets" / "proof" / "web005b"
EXPORT_DIR = pathlib.Path(
    r"C:\Projects\geothermal-prospectivity\outputs\kizildere_mvp_v2\exports\20260917T161155Z-5e7a0e53"
)
EXPORT_ID = "20260917T161155Z-5e7a0e53"
SCIENCE = {
    "terminal_authority": "geothermal-prospectivity@30779547ced0cbf047cb51fb6c2c6ed178547d56:tasks/MER-108_TERMINAL_WEBSITE_HERO_DISPLAY_AMENDMENT.yaml",
    "website_derivative_authority": "geothermal-prospectivity@11c32e8d2d072aa709262e513c8888e6a745bb76:tasks/MER-108_PUBLIC_WEB_DISPLAY_DERIVATIVE_AUTHORITY.md",
    "normalization_authority": "geothermal-prospectivity@d3a163bd6c6b2fe6a1a73fe28e5acf23cd9d4e87:tasks/MER-108_NORMALIZATION_AUTHORITY_CORRECTION.md",
    "surface": "website-only public renderer (homepage Acts 3 and 4); hero-only transforms not used",
}

# Frozen stops of the CTO-approved hero asset family. Terrain and Priority are the
# webhero_publication_v1 stops, THM-01 and ALT-01 the webhero_publication_v4 stops; those are the
# sources of the display textures the accepted WEB-005A drape states were rendered from.
LAYERS = {
    "terrain": {
        "source": "top-dem.tif",
        "sha256": "590f74322c6ad942e0d36b79446934da7a0938c7d87c06ab8c9bd27da73fb694",
        "normalization": "linear_min_max",
        "topology_id": "terrain_natural_earth_relief_v1",
        "stops": ["#07131A", "#173C35", "#426447", "#80744D", "#B79B67", "#D9C7A0", "#F2E8D5", "#FFFFFF"],
        "stops_source": "webhero_publication_v1 terrain",
        "opacity": 0.90,
    },
    "thm01": {
        "source": "thm-thm01.tif",
        "sha256": "6a2850f9915c08ed56ae2731d54881d55ca145db6cda11a21ed7e6191e629583",
        "normalization": "diverging_symmetric_from_data",
        "topology_id": "thm_cool_neutral_warm_red_v1",
        "stops": ["#15365F", "#235987", "#3E82AC", "#76AEC8", "#BAD3DC", "#E9E9DF",
                  "#F2D0B4", "#F3A070", "#ED704D", "#E34232", "#C51F24", "#98151D"],
        "stops_source": "webhero_publication_v4 thm01",
        "opacity": 0.90,
    },
    "alt01": {
        "source": "alt-alt01.tif",
        "sha256": "ac7f2dade5274d9fd81b7fdbc8bcf7ae828bb958de5c74b9847e6332675fbf14",
        "normalization": "linear_min_max",
        "topology_id": "alt_violet_blue_cyan_green_yellow_v1",
        "stops": ["#27104B", "#362061", "#3A377A", "#30578D", "#20799D", "#159BA8",
                  "#18B2A0", "#42C482", "#7BD05E", "#B7DC43", "#E2E53B", "#FFF05A"],
        "stops_source": "webhero_publication_v4 alt01",
        "opacity": 0.90,
    },
    "priority": {
        "source": "score-mvp-remote-sensing-priority.tif",
        "sha256": "15065152f6f21eaf66236d51d6814acfb32326c5698bc2433dcb69653d8a9d1e",
        "normalization": "fixed_range_0_100",
        "topology_id": "priority_deep_purple_red_orange_yellow_v1",
        "stops": ["#13001F", "#2B0A4A", "#54106F", "#8A176A", "#C52A55", "#E85B35", "#F89A2B", "#FFD84A", "#FFF3A0"],
        "stops_source": "webhero_publication_v1 priority",
        "opacity": 0.95,
    },
}
# Neutral grayscale context from the governed DEM (11c32e8d section 6): fixed for the family,
# never driven by an analytical layer. Gray = base + span * lambert(hs).
HILLSHADE = {"source": "top-dem.tif", "azimuth_deg": 315.0, "altitude_deg": 45.0, "z_factor": 1.0,
             "gray_base": 0.07, "gray_span": 0.32, "nodata_fill": "median of valid DEM cells (DEM has no invalid cells here)"}
SIZES = (1200, 900, 600)  # native grid, then one area (box) downsample each; never upsampled
LEGEND_W = 256


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hex_rgb(h: str) -> np.ndarray:
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float64)


def make_lut(stops: list[str], size: int = 256) -> np.ndarray:
    """Same LUT construction as the hero asset family: evenly spaced stops, linear in sRGB."""
    arr = np.array([hex_rgb(c) for c in stops])
    xp = np.linspace(0.0, 1.0, len(arr))
    x = np.linspace(0.0, 1.0, size)
    lut = np.zeros((size, 3), dtype=np.uint8)
    for c in range(3):
        lut[:, c] = np.clip(np.interp(x, xp, arr[:, c]), 0, 255).astype(np.uint8)
    return lut


def read(path: pathlib.Path):
    with rasterio.open(path) as ds:
        band = ds.read(1, masked=True)
        data = band.filled(np.nan).astype(np.float64)
        valid = np.isfinite(data) & ~np.ma.getmaskarray(band)
        meta = {"crs": str(ds.crs), "width": ds.width, "height": ds.height,
                "transform": list(ds.transform)[:6]}
    return data, valid, meta


def normalize(kind: str, data: np.ndarray, valid: np.ndarray):
    v = data[valid]
    if kind == "linear_min_max":
        lo, hi = float(v.min()), float(v.max())
        span = max(hi - lo, 1e-9)
        n = (data - lo) / span
        params = {"vmin": lo, "vmax": hi}
    elif kind == "diverging_symmetric_from_data":
        m = max(abs(float(v.min())), abs(float(v.max())), 1e-9)
        n = (data + m) / (2 * m)
        params = {"center": 0.0, "M": m, "vmin": -m, "vmax": m}
    elif kind == "fixed_range_0_100":
        n = data / 100.0
        params = {"vmin": 0.0, "vmax": 100.0}
    else:
        raise SystemExit(f"unknown normalization {kind}")
    n = np.where(valid, np.clip(n, 0.0, 1.0), 0.0)
    return n, params


def hillshade(dem: np.ndarray, valid: np.ndarray, transform) -> np.ndarray:
    filled = np.where(valid, dem, np.nanmedian(dem[valid]))
    xres, yres = abs(transform[0]), abs(transform[4])
    dy, dx = np.gradient(filled * HILLSHADE["z_factor"], yres, xres)
    slope = np.pi / 2.0 - np.arctan(np.hypot(dx, dy))
    aspect = np.arctan2(-dx, dy)
    az, alt = np.deg2rad(HILLSHADE["azimuth_deg"]), np.deg2rad(HILLSHADE["altitude_deg"])
    hs = np.sin(alt) * np.sin(slope) + np.cos(alt) * np.cos(slope) * np.cos(az - aspect)
    return np.clip(hs, 0.0, 1.0)


def area_down(rgb: np.ndarray, size: int) -> np.ndarray:
    """Single area (box) downsample of the opaque final RGB image (11c32e8d 3.3: area/box is
    allowed for downsampling; unlike Lanczos it cannot ring or overshoot)."""
    img = Image.fromarray(rgb, "RGB").resize((size, size), Image.Resampling.BOX)
    return np.asarray(img)


def encode_webp(rgb: np.ndarray) -> bytes:
    buf = io.BytesIO()
    Image.fromarray(rgb, "RGB").save(buf, "WEBP", lossless=True, quality=100, method=6, exact=True)
    return buf.getvalue()


def build() -> dict:
    dem, dem_valid, dem_meta = read(EXPORT_DIR / "top-dem.tif")
    hs = hillshade(dem, dem_valid, dem_meta["transform"])
    gray = HILLSHADE["gray_base"] + HILLSHADE["gray_span"] * hs  # 0..1, neutral
    context = np.repeat(gray[:, :, None], 3, axis=2)
    OUT.mkdir(parents=True, exist_ok=True)
    record = {"export_id": EXPORT_ID, "project": "kizildere_mvp_v2", "science": SCIENCE,
              "pipeline": [
                  "governed scalar + governed valid mask (MER-113 export, SHA-256 verified)",
                  "canonical normalization per d3a163bd, resolved once over the whole raster's valid cells",
                  "selected palette LUT (256 entries, evenly spaced frozen stops, linear sRGB)",
                  "governed mask to RGBA: NoData analytical alpha 0; no fill, dilation or erosion",
                  "source-over onto neutral grayscale DEM hillshade at a fixed analytical opacity",
                  "one area (box) downsample of the final opaque RGB per smaller candidate (never upsampled)",
                  "lossless WebP (exact), SHA-256 recorded"],
              "not_used": ["display window", "gamma / tone transfer", "gaussian smoothing", "unsharp",
                           "upsampling", "CSS filter or blend on the page"],
              "hillshade": HILLSHADE,
              "grid": dem_meta,
              "renderer": {"python": platform.python_version(), "numpy": np.__version__,
                           "rasterio": rasterio.__version__, "pillow": PIL.__version__,
                           "webp": features.version("webp")},
              "encoder": "Pillow WebP lossless=True quality=100 method=6 exact=True",
              "layers": {}}
    for key, spec in LAYERS.items():
        src = EXPORT_DIR / spec["source"]
        digest = sha256(src)
        if digest != spec["sha256"]:
            raise SystemExit(f"{src.name}: SHA-256 {digest} does not match the MER-108 pin {spec['sha256']}")
        data, valid, meta = read(src)
        if meta["transform"] != dem_meta["transform"] or meta["crs"] != dem_meta["crs"]:
            raise SystemExit(f"{src.name}: grid differs from the governed DEM grid")
        n, params = normalize(spec["normalization"], data, valid)
        lut = make_lut(spec["stops"])
        idx = np.clip(np.round(n * 255.0), 0, 255).astype(np.uint8)
        rgb = lut[idx].astype(np.float64) / 255.0
        a = np.where(valid, spec["opacity"], 0.0)[:, :, None]
        comp = rgb * a + context * (1.0 - a)
        comp8 = np.clip(np.round(comp * 255.0), 0, 255).astype(np.uint8)
        layer = {"source": spec["source"], "source_sha256": digest,
                 "normalization": spec["normalization"], "resolved": params,
                 "topology_id": spec["topology_id"], "stops": spec["stops"],
                 "stops_source": spec["stops_source"],
                 "lut_sha256": hashlib.sha256(lut.tobytes()).hexdigest(),
                 "analytical_opacity": spec["opacity"],
                 "valid_fraction": round(float(valid.mean()), 6),
                 "mask": "nearest (native grid); invalid cells show only the neutral context",
                 "derivatives": []}
        for size in SIZES:
            px = comp8 if size == comp8.shape[0] else area_down(comp8, size)
            path = OUT / f"{key}-{size}.webp"
            path.write_bytes(encode_webp(px))
            # lossless round-trip proof: the shipped file decodes to exactly the rendered pixels
            back = np.asarray(Image.open(path).convert("RGB"))
            if not np.array_equal(back, px):
                raise SystemExit(f"{path.name}: lossless round trip failed")
            layer["derivatives"].append({
                "path": path.relative_to(ROOT).as_posix(), "width": size, "height": size,
                "resize": "none (native 1200 grid)" if size == 1200 else "area (box) downsample of the final RGB",
                "format": "image/webp (lossless)", "bytes": path.stat().st_size, "sha256": sha256(path)})
        if key == "priority":
            ramp = np.repeat(lut[None, :, :], 8, axis=0)  # unblended canonical colours
            lpath = OUT / "priority-legend-ramp.png"
            Image.fromarray(ramp, "RGB").save(lpath, optimize=True)
            layer["legend"] = {"path": lpath.relative_to(ROOT).as_posix(), "width": LEGEND_W, "height": 8,
                               "content": "the unblended 256-entry priority LUT, 0 at left to 100 at right",
                               "bytes": lpath.stat().st_size, "sha256": sha256(lpath)}
        record["layers"][key] = layer
    return record


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--record", action="store_true", help="write the record to sources.json -> web_005b.analytical")
    args = ap.parse_args()
    rec = build()
    if args.record:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        manifest.setdefault("web_005b", {})["analytical"] = rec
        MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    json.dump(rec, sys.stdout, indent=1, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
