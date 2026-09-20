#!/usr/bin/env python3
"""WEB-005B homepage presentation derivatives (Acts 3 and 4) under MER-151 / GEO-WEB-004.

Supersedes the rendering half of scripts/build_web005b_derivatives.py for the homepage Evidence,
Result and inspection surfaces. The governing contract is the Science parity authority, which names
WEB-005B / MER-109 as its consumer and is terminally accepted:

  geothermal-prospectivity@e8aa5d65f56556be928499c50936eb63db88a6ad:
      tasks/MER-151_GEO-WEB-004_HOMEPAGE_EVIDENCE_PRESENTATION_PARITY_AUTHORITY.md

What MER-151 adds over the MER-108 website-derivative profile this script inherits:

  * a BOUNDED display window on Terrain / ALT-01 (quantiles of the governed valid cells, span
    >= 0.94) and on THM-01 (symmetric |s| quantile, M >= 0.70, centre pinned at exactly 0);
  * one fixed monotonic gamma per layer family, inside the per-layer bounds;
  * ONE final RGBA Lanczos3 resize, per-axis scale 0.50-4.00, ceiling 4800 px per source axis,
    premultiplied and mask-aware, and forbidden from creating new valid support. Implemented and
    bounded here, and not used by the published ladder -- see the SIZES note below for why.

What it explicitly does NOT inherit from the hero amendment, and what this script therefore never
does (MER-151 section 4): AI/super-resolution, scalar-space interpolation, Gaussian smoothing or
denoising, sharpening/unsharp, CLAHE or any local/adaptive tone mapping, per-crop autoscaling, mask
dilation/erosion/fill, and any recolouring outside the frozen palette topology. A 4K derivative is
a PRESENTATION-resolution derivative: the scientific raster stays 1200 x 1200 at 30 m, EPSG:32635,
and nothing here implies finer ground resolution or extra evidence.

Ordered pipeline (MER-151 section 3):

  1. governed scalar + governed valid mask (MER-113 export, SHA-256 verified)
  2. canonical normalization under d3a163bd, resolved once over ALL valid cells of the whole raster
  3. optional bounded display window
  4. optional bounded fixed monotonic gamma
  5. frozen MER-108 palette topology / exact approved LUT
  6. governed mask -> RGBA (NoData alpha 0; no fill, dilation or erosion)
  7. optional single final RGBA Lanczos3 resize (premultiplied, mask-aware)
  8. authorized neutral context underlay (governed-DEM hillshade, composited after the resize)
  9. web encoding + deterministic checksum

Per-layer settings below are the ones this pass chose, and each is inside its MER-151 bound:

  terrain   window disabled, gamma disabled. The Terrain rendering is ALSO the display texture the
            accepted WEB-005A hero drape state was rendered from; changing its transfer would break
            the hero -> page continuity for a layer that already reads well across its full range.
  thm01     window q_abs = 0.998 (M = 0.7036, the smallest clean quantile that clears the mandatory
            M >= 0.70 floor; 0.21% of valid cells clip), gamma 0.85 on |s| with the centre fixed.
  alt01     window q_low = 0.02 / q_high = 0.98 (span 0.96), gamma disabled. This is the layer the
            authority exists for: 99.9% of the governed valid cells sit in the bottom 8.3% of the
            canonical range, so the unwindowed render spends the whole palette on outliers and the
            map reads as one flat violet field. The window is resolved from the governed raster's
            own valid cells, never from a crop or a viewport.
  priority  window PROHIBITED and not used; gamma disabled. Priority stays bound to the fixed
            scientific 0-100 domain and to the exact colours the hero payoff ends on.

Usage (needs rasterio, numpy, pillow):
    python scripts/build_web005b_presentation.py            # build + verify, print the record
    python scripts/build_web005b_presentation.py --record   # also write sources.json -> web_005b
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
NATIVE_PX = 1200
AXIS_CEILING_PX = 4800          # MER-151 section 2
SCALE_BOUNDS = (0.50, 4.00)     # MER-151 section 2

SCIENCE = {
    "presentation_authority": "geothermal-prospectivity@e8aa5d65f56556be928499c50936eb63db88a6ad:tasks/MER-151_GEO-WEB-004_HOMEPAGE_EVIDENCE_PRESENTATION_PARITY_AUTHORITY.md",
    "terminal_authority": "geothermal-prospectivity@30779547ced0cbf047cb51fb6c2c6ed178547d56:tasks/MER-108_TERMINAL_WEBSITE_HERO_DISPLAY_AMENDMENT.yaml",
    "website_derivative_authority": "geothermal-prospectivity@11c32e8d2d072aa709262e513c8888e6a745bb76:tasks/MER-108_PUBLIC_WEB_DISPLAY_DERIVATIVE_AUTHORITY.md",
    "normalization_authority": "geothermal-prospectivity@d3a163bd6c6b2fe6a1a73fe28e5acf23cd9d4e87:tasks/MER-108_NORMALIZATION_AUTHORITY_CORRECTION.md",
    "surface": "public website presentation only (homepage Acts 3 and 4 and the inspection aid); never a report, workbench, validation or quantitative-export surface",
    "resolution_claim": "presentation-resolution derivative of a 1200 x 1200 / 30 m / EPSG:32635 scientific raster; the enlarged files carry no finer ground sampling and no additional scientific evidence",
}

# Frozen stops of the CTO-approved hero asset family (unchanged from the MER-108 pass: the palette
# topology and the exact LUT are what MER-151 keeps frozen).
LAYERS = {
    "terrain": {
        "source": "top-dem.tif",
        "sha256": "590f74322c6ad942e0d36b79446934da7a0938c7d87c06ab8c9bd27da73fb694",
        "normalization": "linear_min_max",
        "topology_id": "terrain_natural_earth_relief_v1",
        "stops": ["#07131A", "#173C35", "#426447", "#80744D", "#B79B67", "#D9C7A0", "#F2E8D5", "#FFFFFF"],
        "stops_source": "webhero_publication_v1 terrain",
        "opacity": 0.90,
        "window": None,
        "gamma": None,
        "transfer_note": "disabled on purpose: this rendering is also the source of the accepted WEB-005A hero Terrain drape state, and its canonical range is already used end to end",
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
        "window": {"kind": "symmetric_abs_quantile", "q_abs": 0.998},
        "gamma": 0.85,
        "transfer_note": "signed window about a fixed 0 centre; independent positive/negative windows are prohibited and not used",
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
        "window": {"kind": "quantile", "q_low": 0.02, "q_high": 0.98},
        "gamma": None,
        "transfer_note": "quantile span 0.96, resolved from all valid cells of the governed source; no gamma on top of it",
    },
    "priority": {
        "source": "score-mvp-remote-sensing-priority.tif",
        "sha256": "15065152f6f21eaf66236d51d6814acfb32326c5698bc2433dcb69653d8a9d1e",
        "normalization": "fixed_range_0_100",
        "topology_id": "priority_deep_purple_red_orange_yellow_v1",
        "stops": ["#13001F", "#2B0A4A", "#54106F", "#8A176A", "#C52A55", "#E85B35", "#F89A2B", "#FFD84A", "#FFF3A0"],
        "stops_source": "webhero_publication_v1 priority",
        "opacity": 0.95,
        "window": None,   # MER-151 section 3: percentile/window clipping stays prohibited here
        "gamma": None,
        "transfer_note": "window prohibited by the authority; gamma deliberately unused so the published 0-100 score keeps exactly the colours the hero payoff ends on",
    },
}
# Neutral grayscale context from the governed DEM (MER-108 11c32e8d section 6, carried through
# MER-151 section 3 step 8): fixed for the family, never driven by an analytical layer.
HILLSHADE = {"source": "top-dem.tif", "azimuth_deg": 315.0, "altitude_deg": 45.0, "z_factor": 1.0,
             "gray_base": 0.07, "gray_span": 0.32,
             "nodata_fill": "median of valid DEM cells (DEM has no invalid cells here)",
             "resize": "the neutral underlay is built at the native grid and enlarged as an IMAGE "
                       "(Lanczos3) alongside the analytical RGBA; the DEM scalar itself is never interpolated"}

# The published ladder: the native grid and two MER-108 area (box) downsamples of the final opaque
# RGB. The MER-151 enlargement path above is implemented and bounded, and this pass deliberately
# does NOT publish a rung that uses it.
#
# The reason is payload, measured rather than assumed. MER-151 permits up to 4800 px per axis, and a
# 1800 px (1.50x) rung was built and weighed: 1.38 MB for Terrain, 3.34 MB for THM-01, 5.96 MB for
# ALT-01 and 5.65 MB for Priority, lossless. Three of the four cannot be re-encoded down either --
# the MER-108 section 8 delivery gates reject every rung of the ladder for them, because a block
# transform moves saturated palette colours off the governed ramp and pulls analytical chroma across
# the NoData boundary. So a 1800 rung would mean shipping 3-6 MB per panel to exactly the visitors
# on 2x displays. Meanwhile the homepage's analytical surfaces are capped at 600 CSS px, which the
# native 1200 grid already serves at a true 2x device pixel ratio. There is no density to gain and a
# great deal of weight to lose, so the enlargement stays unused and the layout stays inside native
# density. That is a delivery decision, not a Science one: nothing here needs re-approval to change.
SIZES = (600, 900, 1200)
LAYER_SIZES: dict[str, tuple[int, ...]] = {}
LEGEND_W = 256


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hex_rgb(h: str) -> np.ndarray:
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float64)


def make_lut(stops: list[str], size: int = 256) -> np.ndarray:
    """Unchanged from the MER-108 pass: evenly spaced stops, linear in sRGB, 256 entries."""
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
    """MER-108 d3a163bd canonical normalization. Terrain/ALT land in [0,1]; THM-01 is returned as
    the canonical SIGNED coordinate s in [-1,1] so the window and gamma can keep 0 exactly fixed."""
    v = data[valid]
    if kind == "linear_min_max":
        lo, hi = float(v.min()), float(v.max())
        span = max(hi - lo, 1e-9)
        n = (data - lo) / span
        return n, {"vmin": lo, "vmax": hi}, "unit"
    if kind == "diverging_symmetric_from_data":
        m = max(abs(float(v.min())), abs(float(v.max())), 1e-9)
        return data / m, {"center": 0.0, "M": m, "vmin": -m, "vmax": m}, "signed"
    if kind == "fixed_range_0_100":
        return data / 100.0, {"vmin": 0.0, "vmax": 100.0}, "unit"
    raise SystemExit(f"unknown normalization {kind}")


def apply_window(spec, n: np.ndarray, valid: np.ndarray, domain: str):
    """MER-151 section 3 display windows. Returns (values, record)."""
    if not spec:
        return n, "disabled"
    v = n[valid]
    if spec["kind"] == "quantile":
        q_low, q_high = float(spec["q_low"]), float(spec["q_high"])
        if not (0.0 <= q_low <= 0.02 and 0.98 <= q_high <= 1.0):
            raise SystemExit(f"quantile window {q_low}/{q_high} is outside the MER-151 bounds")
        if q_high - q_low < 0.94:
            raise SystemExit(f"quantile span {q_high - q_low} is below the mandatory 0.94")
        lo, hi = float(np.quantile(v, q_low)), float(np.quantile(v, q_high))
        out = np.clip((n - lo) / max(hi - lo, 1e-12), 0.0, 1.0)
        return out, {"kind": "quantile", "q_low": q_low, "q_high": q_high, "span": round(q_high - q_low, 6),
                     "resolved_low": lo, "resolved_high": hi,
                     "clipped_fraction": round(float(((v < lo) | (v > hi)).mean()), 6),
                     "resolved_over": "all valid cells of the governed source raster"}
    if spec["kind"] == "symmetric_abs_quantile":
        if domain != "signed":
            raise SystemExit("a symmetric window needs the canonical signed coordinate")
        q_abs = float(spec["q_abs"])
        if not 0.98 <= q_abs <= 1.0:
            raise SystemExit(f"q_abs {q_abs} is outside the MER-151 bounds")
        m = float(np.quantile(np.abs(v), q_abs))
        if m < 0.70:
            raise SystemExit(f"THM-01 window M={m:.4f} is below the mandatory 0.70 floor")
        out = np.clip(n / m, -1.0, 1.0)
        return out, {"kind": "symmetric_abs_quantile", "q_abs": q_abs, "resolved_M": m,
                     "center": 0.0, "clipped_fraction": round(float((np.abs(v) > m).mean()), 6),
                     "resolved_over": "all valid cells of the governed source raster",
                     "independent_signed_windows": False}
    raise SystemExit(f"unknown window kind {spec['kind']!r}")


def apply_gamma(gamma, n: np.ndarray, domain: str, key: str):
    """MER-151 section 3 fixed monotonic gamma. One value per layer family; never local/adaptive."""
    if gamma is None:
        return n, "disabled"
    g = float(gamma)
    lo, hi = (0.80, 1.25) if domain == "signed" else (0.75, 1.35)
    if not lo <= g <= hi:
        raise SystemExit(f"{key}: gamma {g} is outside the MER-151 bound {lo}-{hi}")
    if domain == "signed":
        out = np.sign(n) * np.power(np.abs(n), g)
        formula = "u = sign(s) * |s| ** gamma, with u(0) = 0 exactly"
    else:
        out = np.power(np.clip(n, 0.0, 1.0), g)
        formula = "u = n ** gamma"
    return out, {"gamma": g, "formula": formula, "bounds": [lo, hi], "adaptive": False}


def hillshade(dem: np.ndarray, valid: np.ndarray, transform) -> np.ndarray:
    filled = np.where(valid, dem, np.nanmedian(dem[valid]))
    xres, yres = abs(transform[0]), abs(transform[4])
    dy, dx = np.gradient(filled * HILLSHADE["z_factor"], yres, xres)
    slope = np.pi / 2.0 - np.arctan(np.hypot(dx, dy))
    aspect = np.arctan2(-dx, dy)
    az, alt = np.deg2rad(HILLSHADE["azimuth_deg"]), np.deg2rad(HILLSHADE["altitude_deg"])
    hs = np.sin(alt) * np.sin(slope) + np.cos(alt) * np.cos(slope) * np.cos(az - aspect)
    return np.clip(hs, 0.0, 1.0)


def lanczos_rgba(rgb: np.ndarray, alpha: np.ndarray, size: int):
    """MER-151 section 2: ONE final RGBA Lanczos3 enlargement, premultiplied and mask-aware.

    rgb is float 0..1 (H,W,3), alpha is float 0..1 (H,W). Returns (rgb, alpha) at size x size.
    Filtered alpha may not create new valid support, so the enlarged alpha is masked by a
    nearest-neighbour enlargement of the governed valid mask: ringing can feather the inside of a
    boundary, it can never invent coverage outside one.
    """
    src = rgb.shape[0]
    scale = size / src
    if not SCALE_BOUNDS[0] <= scale <= SCALE_BOUNDS[1]:
        raise SystemExit(f"per-axis scale {scale} is outside the MER-151 bound {SCALE_BOUNDS}")
    if size > AXIS_CEILING_PX:
        raise SystemExit(f"{size} px exceeds the MER-151 {AXIS_CEILING_PX} px per-axis ceiling")
    pre = rgb * alpha[:, :, None]                       # premultiply
    out = np.empty((size, size, 3), dtype=np.float64)
    for c in range(3):
        out[:, :, c] = np.asarray(Image.fromarray(pre[:, :, c].astype(np.float32), "F")
                                  .resize((size, size), Image.Resampling.LANCZOS), dtype=np.float64)
    a = np.asarray(Image.fromarray(alpha.astype(np.float32), "F")
                   .resize((size, size), Image.Resampling.LANCZOS), dtype=np.float64)
    support = np.asarray(Image.fromarray((alpha > 0).astype(np.uint8) * 255, "L")
                         .resize((size, size), Image.Resampling.NEAREST), dtype=np.float64) / 255.0
    a = np.clip(a, 0.0, 1.0) * support                  # no new valid support
    out = np.clip(out, 0.0, None)
    out = np.minimum(out, a[:, :, None])                # legal premultiplied range
    with np.errstate(divide="ignore", invalid="ignore"):
        un = np.where(a[:, :, None] > 1e-6, out / np.maximum(a[:, :, None], 1e-6), 0.0)
    return np.clip(un, 0.0, 1.0), a


def lanczos_gray(gray: np.ndarray, size: int) -> np.ndarray:
    """The neutral context underlay, enlarged as an image. Not an analytical channel."""
    return np.asarray(Image.fromarray(gray.astype(np.float32), "F")
                      .resize((size, size), Image.Resampling.LANCZOS), dtype=np.float64)


def area_down(rgb: np.ndarray, size: int) -> np.ndarray:
    """MER-108 3.3 area/box downsample of the opaque final RGB; unlike Lanczos it cannot ring."""
    return np.asarray(Image.fromarray(rgb, "RGB").resize((size, size), Image.Resampling.BOX))


def encode_webp(rgb: np.ndarray) -> bytes:
    buf = io.BytesIO()
    Image.fromarray(rgb, "RGB").save(buf, "WEBP", lossless=True, quality=100, method=6, exact=True)
    return buf.getvalue()


def build() -> dict:
    dem, dem_valid, dem_meta = read(EXPORT_DIR / "top-dem.tif")
    hs = hillshade(dem, dem_valid, dem_meta["transform"])
    gray = HILLSHADE["gray_base"] + HILLSHADE["gray_span"] * hs   # 0..1, neutral
    gray_at = {NATIVE_PX: gray}
    OUT.mkdir(parents=True, exist_ok=True)
    record = {
        "export_id": EXPORT_ID, "project": "kizildere_mvp_v2", "science": SCIENCE,
        "scientific_master": {"crs": "EPSG:32635", "width": NATIVE_PX, "height": NATIVE_PX,
                              "gsd_m": 30.0,
                              "statement": "unchanged and authoritative; the derivatives below are "
                                           "presentation renderings of it"},
        "pipeline": [
            "governed scalar + governed valid mask (MER-113 export, SHA-256 verified)",
            "canonical normalization per d3a163bd, resolved once over the whole raster's valid cells",
            "optional bounded display window (MER-151 section 3), resolved from the governed source",
            "optional bounded fixed monotonic gamma (MER-151 section 3)",
            "frozen MER-108 palette topology / exact approved LUT (256 entries, linear sRGB)",
            "governed mask to RGBA: NoData analytical alpha 0; no fill, dilation or erosion",
            "at most one final RGBA Lanczos3 resize, premultiplied and mask-aware (MER-151 section 2)",
            "source-over onto the neutral grayscale DEM hillshade at a fixed analytical opacity",
            "lossless WebP (exact), SHA-256 recorded",
        ],
        "not_used": ["ai_super_resolution", "scalar_space_interpolation", "gaussian smoothing",
                     "unsharp", "clahe_or_local_tone_mapping", "per_crop_autoscaling",
                     "mask dilation/erosion/fill", "hotspot emphasis",
                     "CSS filter or blend on the page"],
        "resolution_claim": SCIENCE["resolution_claim"],
        "hillshade": HILLSHADE,
        "grid": dem_meta,
        "renderer": {"python": platform.python_version(), "numpy": np.__version__,
                     "rasterio": rasterio.__version__, "pillow": PIL.__version__,
                     "webp": features.version("webp")},
        "encoder": "Pillow WebP lossless=True quality=100 method=6 exact=True",
        "layers": {},
    }
    for key, spec in LAYERS.items():
        src = EXPORT_DIR / spec["source"]
        digest = sha256(src)
        if digest != spec["sha256"]:
            raise SystemExit(f"{src.name}: SHA-256 {digest} does not match the MER-108 pin {spec['sha256']}")
        data, valid, meta = read(src)
        if meta["transform"] != dem_meta["transform"] or meta["crs"] != dem_meta["crs"]:
            raise SystemExit(f"{src.name}: grid differs from the governed DEM grid")
        n, params, domain = normalize(spec["normalization"], data, valid)
        n, window_rec = apply_window(spec["window"], n, valid, domain)
        n, gamma_rec = apply_gamma(spec["gamma"], n, domain, key)
        unit = (n + 1.0) / 2.0 if domain == "signed" else n       # signed -> LUT coordinate
        unit = np.where(valid, np.clip(unit, 0.0, 1.0), 0.0)
        lut = make_lut(spec["stops"])
        idx = np.clip(np.round(unit * 255.0), 0, 255).astype(np.uint8)
        rgb = lut[idx].astype(np.float64) / 255.0
        alpha = np.where(valid, spec["opacity"], 0.0)

        native_rgb8 = np.clip(np.round(
            (rgb * alpha[:, :, None] + np.repeat(gray[:, :, None], 3, axis=2) * (1.0 - alpha[:, :, None]))
            * 255.0), 0, 255).astype(np.uint8)

        layer = {
            "source": spec["source"], "source_sha256": digest,
            "normalization": spec["normalization"], "resolved": params,
            "display_window": window_rec, "gamma": gamma_rec,
            "transfer_note": spec["transfer_note"],
            "topology_id": spec["topology_id"], "stops": spec["stops"],
            "stops_source": spec["stops_source"],
            "lut_sha256": hashlib.sha256(lut.tobytes()).hexdigest(),
            "analytical_opacity": spec["opacity"],
            "valid_fraction": round(float(valid.mean()), 6),
            "mask": "governed valid mask; nearest at the native grid, and a Lanczos3 enlargement may "
                    "never create valid support the governed mask does not have",
            "derivatives": [],
        }
        for size in LAYER_SIZES.get(key, SIZES):
            if size == NATIVE_PX:
                px, resize = native_rgb8, "none (native 1200 grid)"
            elif size < NATIVE_PX:
                px, resize = area_down(native_rgb8, size), "area (box) downsample of the final RGB"
            else:
                up_rgb, up_a = lanczos_rgba(rgb, alpha, size)
                if size not in gray_at:
                    gray_at[size] = np.clip(lanczos_gray(gray, size), 0.0, 1.0)
                ctx = np.repeat(gray_at[size][:, :, None], 3, axis=2)
                comp = up_rgb * up_a[:, :, None] + ctx * (1.0 - up_a[:, :, None])
                px = np.clip(np.round(comp * 255.0), 0, 255).astype(np.uint8)
                resize = (f"single final RGBA Lanczos3 enlargement, premultiplied and mask-aware, "
                          f"{size / NATIVE_PX:.2f}x per axis (MER-151 section 2)")
            path = OUT / f"{key}-{size}.webp"
            path.write_bytes(encode_webp(px))
            back = np.asarray(Image.open(path).convert("RGB"))
            if not np.array_equal(back, px):
                raise SystemExit(f"{path.name}: lossless round trip failed")
            layer["derivatives"].append({
                "path": path.relative_to(ROOT).as_posix(), "width": size, "height": size,
                "resize": resize, "presentation_scale": round(size / NATIVE_PX, 4),
                "format": "image/webp (lossless)", "bytes": path.stat().st_size,
                "sha256": sha256(path)})
        if key == "priority":
            ramp = np.repeat(lut[None, :, :], 8, axis=0)   # unblended canonical colours
            lpath = OUT / "priority-legend-ramp.png"
            Image.fromarray(ramp, "RGB").save(lpath, optimize=True)
            layer["legend"] = {"path": lpath.relative_to(ROOT).as_posix(), "width": LEGEND_W, "height": 8,
                               "content": "the unblended 256-entry priority LUT, 0 at left to 100 at right",
                               "coupled_to": "the map's own transfer: priority carries no window and "
                                             "no gamma, so position on the ramp is the score itself",
                               "bytes": lpath.stat().st_size, "sha256": sha256(lpath)}
        record["layers"][key] = layer
    return record


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--record", action="store_true",
                    help="write the record to sources.json -> web_005b.analytical")
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
