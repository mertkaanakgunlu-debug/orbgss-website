#!/usr/bin/env python3
"""MER-242 Geothermal-page presentation derivatives in the MER-151 family.

Two surfaces the homepage build (scripts/build_web005b_presentation.py) does not make, rendered
from the same governed MER-113 export through the same MER-151 pipeline and the same helper
functions, so a pixel here means what it means on the homepage:

  alt02   Pl. 06 of the Geothermal atlas: the ALT-02 ferric/iron alteration proxy.
  relief  The "priority over relief" figure (#relief): mvp_remote_sensing_priority_v1 over a
          neutral, vertically exaggerated hillshade of the governed DEM.

The relief ladder also carries the 160 / 320 px thumbnail used by the Sources register ("Evidence
and priority maps"): a box downsample of the native rendering, nothing new.

Science decisions this pass records (MER-242; the CTO assigned Science to this workstream):

  alt02 palette   ALT-02 shares the accepted renderer's style with ALT-01 (`alt_batlow_sequential`,
                  geothermal-prospectivity@215ef89d:src/geothermal/workbench/style_registry.py,
                  LAYER_ID_ALT01 and LAYER_ID_ALT02 map to the same style; the MER-113 export
                  manifest names that style for both). The MER-108 hero topology chosen for that
                  style, `alt_violet_blue_cyan_green_yellow_v1`, therefore carries over with the
                  exact ALT-01 stops and LUT. No new palette is selected.
  alt02 transfer  canonical linear_min_max (d3a163bd ALT semantics), then the ALT-01 window rule of
                  MER-151 section 3 with the ALT-01 values: q_low 0.02 / q_high 0.98, no gamma. The
                  governed raster is even more outlier-bound than ALT-01 (98 % of the valid cells
                  sit inside 0.17 % of the canonical range), so the window is what makes it
                  readable, and keeping ALT-01's exact rule keeps Pl. 05 and Pl. 06 comparable.
  alt02 context   the homepage family's own hillshade and opacity (0.90), so Pl. 06 sits in the
                  atlas exactly like Pl. 02, 04 and 05.
  relief          MER-108 11c32e8d section 6 composition, unchanged: ordinary source-over of the
                  unwindowed, ungamma'd priority LUT onto a neutral grayscale hillshade of the
                  governed DEM. Inside its bounds this surface takes the two values that let the
                  relief read: the lowest permitted priority opacity (0.90; range 0.90-1.00) and a
                  vertical exaggeration of 3.0 (the accepted WEB-005A hero relief uses 3.0), with
                  a dark neutral grey range (0.05-0.60) so the context stays below the priority
                  colours. No blend mode, no colourised or data-driven hillshade, no
                  data-dependent opacity.

Everything MER-151 section 4 prohibits stays unused: no AI/super-resolution, no scalar-space
interpolation, no smoothing or sharpening, no local tone mapping, no per-crop autoscaling, no mask
edit, no recolouring outside the frozen LUT, no hotspot emphasis. The scientific master stays
1200 x 1200 at 30 m, EPSG:32635.

Usage (needs rasterio, numpy, pillow; the homepage build's own environment):
    python scripts/build_mer242_presentation.py            # build + verify, print the record
    python scripts/build_mer242_presentation.py --record   # also write sources.json -> mer_242
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import platform
import sys

import numpy as np
import PIL
import rasterio
from PIL import Image, features

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_web005b_presentation as base  # noqa: E402  (shared MER-151 pipeline, one implementation)

ROOT = base.ROOT
MANIFEST = base.MANIFEST
OUT = ROOT / "assets" / "proof" / "mer242"

SCIENCE = dict(base.SCIENCE)
SCIENCE.update({
    "surface": "public website presentation only: /solutions/geothermal/ (Pl. 06 and the priority-over-relief "
               "figure) and thumbnails of at most 160 CSS px on /sources/; never a report, workbench, "
               "validation or quantitative-export surface",
    "task": "MER-242 (Science, assigned by the CTO to the website workstream on 2026-10-25)",
    "style_registry": "geothermal-prospectivity@215ef89d794cf6cbf98e94f8fc17184c859ebcd8:"
                      "src/geothermal/workbench/style_registry.py (ALT-01 and ALT-02 -> alt_batlow_sequential)",
    "acceptance": "accepted by the CTO on 2026-10-25 (S1-S7 of tasks/MER-242_EVIDENCE.md); no separate independent review was run",
})

PRIORITY_WARNING = ("AOI-relative experimental screening only. Not probability, reserve/resource estimation, discovery "
                    "likelihood, drilling-success likelihood, Full Prospectivity, or a calibrated cross-AOI score.")

# The relief surface's own neutral context. Every value is fixed for the asset family and none is driven
# by an analytical layer (MER-108 11c32e8d section 6, "Hillshade constraints").
RELIEF_HILLSHADE = {"source": "top-dem.tif", "azimuth_deg": 315.0, "altitude_deg": 45.0, "z_factor": 3.0,
                    "gray_base": 0.05, "gray_span": 0.55,
                    "nodata_fill": "median of valid DEM cells (DEM has no invalid cells here)",
                    "z_factor_note": "3.0 = the vertical exaggeration of the accepted WEB-005A hero relief "
                                     "(hero/evidence/production_drape_states.json relief_geometry)",
                    "resize": "built at the native grid; only box downsamples of the final RGB are published"}

SURFACES = {
    "alt02": {
        "source": "alt-alt02.tif",
        "sha256": "7b3aa4a7c7586503df805021063d497cca7e28a31acf31222314a38d69e9bb0a",
        "export_layer_id": "alt-alt02",
        "public_label": "ALT-02 Alteration Proxy - ferric/iron",
        "mandatory_warning": "Broad Sentinel-2 spectral alteration proxy; not mineral identification and not proof "
                             "of hydrothermal alteration.",
        "normalization": "linear_min_max",
        "topology_id": base.LAYERS["alt01"]["topology_id"],
        "stops": base.LAYERS["alt01"]["stops"],
        "stops_source": "webhero_publication_v4 alt01 (ALT-02 shares the renderer style alt_batlow_sequential)",
        "opacity": base.LAYERS["alt01"]["opacity"],
        "window": base.LAYERS["alt01"]["window"],
        "gamma": base.LAYERS["alt01"]["gamma"],
        "transfer_note": "the ALT-01 rule and values of MER-151 section 3: quantile window 0.02 / 0.98 (span 0.96) "
                         "resolved from all valid cells of the governed ALT-02 raster, no gamma",
        "context": base.HILLSHADE,
        "context_note": "the homepage family's hillshade, unchanged, so Pl. 06 matches Pl. 02, 04 and 05",
        "sizes": (600, 900, 1200),
        "legend": True,
        "placement": {"route": "solutions/geothermal/index.html", "slot": "Pl. 06 #iron (data-visual-slot=\"iron\")",
                      "design_cap_css_px": 600},
    },
    "relief": {
        "source": "score-mvp-remote-sensing-priority.tif",
        "sha256": base.LAYERS["priority"]["sha256"],
        "export_layer_id": "score-mvp-remote-sensing-priority",
        "public_label": "Remote-Sensing Relative Priority - Experimental Baseline, over shaded NASADEM relief",
        "mandatory_warning": PRIORITY_WARNING,
        "normalization": "fixed_range_0_100",
        "topology_id": base.LAYERS["priority"]["topology_id"],
        "stops": base.LAYERS["priority"]["stops"],
        "stops_source": base.LAYERS["priority"]["stops_source"],
        "opacity": 0.90,
        "window": None,   # prohibited for priority (MER-151 section 3)
        "gamma": None,
        "transfer_note": "no window (prohibited) and no gamma: the published 0-100 score keeps the colours of the "
                         "homepage result and of its legend ramp",
        "context": RELIEF_HILLSHADE,
        "context_note": "source-over at 0.90, the lowest priority opacity MER-108 section 6 permits, onto a dark "
                        "neutral hillshade exaggerated 3x; the relief reads fully where the score has no valid "
                        "cell and as a faint modulation (at most ~15 of 255 levels) under valid cells",
        "sizes": (160, 320, 600, 900, 1200),
        "legend": False,
        "placement": {"route": "solutions/geothermal/index.html", "slot": "#relief (data-visual-slot=\"relief\")",
                      "design_cap_css_px": 600,
                      "thumbnail": {"route": "sources/index.html", "row": "Evidence and priority maps",
                                    "css_px": 160, "derivatives": [160, 320]}},
    },
}


def shade(dem: np.ndarray, valid: np.ndarray, transform, p: dict) -> np.ndarray:
    """base.hillshade with the parameters passed in instead of read from the homepage constant."""
    filled = np.where(valid, dem, np.nanmedian(dem[valid]))
    xres, yres = abs(transform[0]), abs(transform[4])
    dy, dx = np.gradient(filled * p["z_factor"], yres, xres)
    slope = np.pi / 2.0 - np.arctan(np.hypot(dx, dy))
    aspect = np.arctan2(-dx, dy)
    az, alt = np.deg2rad(p["azimuth_deg"]), np.deg2rad(p["altitude_deg"])
    hs = np.sin(alt) * np.sin(slope) + np.cos(alt) * np.cos(slope) * np.cos(az - aspect)
    return np.clip(hs, 0.0, 1.0)


def build() -> dict:
    dem, dem_valid, dem_meta = base.read(base.EXPORT_DIR / "top-dem.tif")
    dem_sha = base.sha256(base.EXPORT_DIR / "top-dem.tif")
    if dem_sha != base.LAYERS["terrain"]["sha256"]:
        raise SystemExit(f"top-dem.tif: SHA-256 {dem_sha} does not match the MER-108 pin")
    # Guard: the parameterised hillshade must be the homepage one when given the homepage parameters.
    if not np.array_equal(shade(dem, dem_valid, dem_meta["transform"], base.HILLSHADE),
                          base.hillshade(dem, dem_valid, dem_meta["transform"])):
        raise SystemExit("the parameterised hillshade drifted from the homepage implementation")
    OUT.mkdir(parents=True, exist_ok=True)
    for stale in OUT.glob("*"):      # this directory belongs to this script alone
        stale.unlink()
    record = {
        "task": "MER-242", "export_id": base.EXPORT_ID, "project": "kizildere_mvp_v2", "science": SCIENCE,
        "scientific_master": {"crs": "EPSG:32635", "width": base.NATIVE_PX, "height": base.NATIVE_PX, "gsd_m": 30.0,
                              "statement": "unchanged and authoritative; the derivatives below are presentation "
                                           "renderings of it"},
        "pipeline": [
            "governed scalar + governed valid mask (MER-113 export, SHA-256 verified)",
            "canonical normalization per d3a163bd, resolved once over the whole raster's valid cells",
            "optional bounded display window (MER-151 section 3), resolved from the governed source",
            "optional bounded fixed monotonic gamma (MER-151 section 3)",
            "frozen MER-108 palette topology / exact approved LUT (256 entries, linear sRGB)",
            "governed mask to RGBA: NoData analytical alpha 0; no fill, dilation or erosion",
            "source-over onto the surface's fixed neutral grayscale DEM hillshade at a fixed analytical opacity",
            "native 1200 grid; smaller rungs are area (box) downsamples of the final RGB; no enlargement",
            "lossless WebP (exact), SHA-256 recorded",
        ],
        "not_used": ["ai_super_resolution", "scalar_space_interpolation", "gaussian smoothing", "unsharp",
                     "clahe_or_local_tone_mapping", "per_crop_autoscaling", "mask dilation/erosion/fill",
                     "hotspot emphasis", "blend modes or colourised hillshade", "data-dependent opacity",
                     "Lanczos3 enlargement (permitted by MER-151 section 2, not used)",
                     "CSS filter or blend on the page"],
        "resolution_claim": base.SCIENCE["resolution_claim"],
        "grid": dem_meta,
        "renderer": {"python": platform.python_version(), "numpy": np.__version__, "rasterio": rasterio.__version__,
                     "pillow": PIL.__version__, "webp": features.version("webp")},
        "encoder": "Pillow WebP lossless=True quality=100 method=6 exact=True; legend PNG optimize=True",
        "naming": "<surface>-<first 8 hex of SHA-256 of the native 1200 px RGB pixels>-<width>.webp: /assets/ is "
                  "served immutable for a year, so a changed rendering gets a new name",
        "surfaces": {},
    }
    for key, spec in SURFACES.items():
        src = base.EXPORT_DIR / spec["source"]
        digest = base.sha256(src)
        if digest != spec["sha256"]:
            raise SystemExit(f"{src.name}: SHA-256 {digest} does not match the pin {spec['sha256']}")
        data, valid, meta = base.read(src)
        if meta["transform"] != dem_meta["transform"] or meta["crs"] != dem_meta["crs"]:
            raise SystemExit(f"{src.name}: grid differs from the governed DEM grid")
        n, params, domain = base.normalize(spec["normalization"], data, valid)
        n, window_rec = base.apply_window(spec["window"], n, valid, domain)
        n, gamma_rec = base.apply_gamma(spec["gamma"], n, domain, key)
        if domain != "unit":
            raise SystemExit(f"{key}: expected a unit-domain layer")
        unit = np.where(valid, np.clip(n, 0.0, 1.0), 0.0)
        lut = base.make_lut(spec["stops"])
        idx = np.clip(np.round(unit * 255.0), 0, 255).astype(np.uint8)
        rgb = lut[idx].astype(np.float64) / 255.0
        alpha = np.where(valid, spec["opacity"], 0.0)
        ctx = spec["context"]
        gray = ctx["gray_base"] + ctx["gray_span"] * shade(dem, dem_valid, dem_meta["transform"], ctx)
        native = np.clip(np.round(
            (rgb * alpha[:, :, None] + np.repeat(gray[:, :, None], 3, axis=2) * (1.0 - alpha[:, :, None]))
            * 255.0), 0, 255).astype(np.uint8)
        hash8 = hashlib.sha256(native.tobytes()).hexdigest()[:8]

        surface = {
            "export_layer_id": spec["export_layer_id"], "source": spec["source"], "source_sha256": digest,
            "public_label": spec["public_label"], "mandatory_warning": spec["mandatory_warning"],
            "mandatory_warning_status": "wording of record; not rendered while public_warnings is retired "
                                        "(CTO, 2026-10-25)",
            "normalization": spec["normalization"], "resolved": params,
            "display_window": window_rec, "gamma": gamma_rec, "transfer_note": spec["transfer_note"],
            "topology_id": spec["topology_id"], "stops": spec["stops"], "stops_source": spec["stops_source"],
            "lut_sha256": hashlib.sha256(lut.tobytes()).hexdigest(),
            "analytical_opacity": spec["opacity"],
            "context": {k: v for k, v in ctx.items()}, "context_note": spec["context_note"],
            "valid_fraction": round(float(valid.mean()), 6),
            "mask": "governed valid mask, nearest at the native grid; NoData shows the neutral context, which is "
                    "not analysis",
            "native_pixels_sha256_8": hash8,
            "placement_intent": spec["placement"],
            "placement_status": "files delivered; not placed on any page by MER-242",
            "derivatives": [],
        }
        for size in spec["sizes"]:
            if size == base.NATIVE_PX:
                px, resize = native, "none (native 1200 grid)"
            else:
                px, resize = base.area_down(native, size), "area (box) downsample of the final RGB"
            path = OUT / f"{key}-{hash8}-{size}.webp"
            path.write_bytes(base.encode_webp(px))
            if not np.array_equal(np.asarray(Image.open(path).convert("RGB")), px):
                raise SystemExit(f"{path.name}: lossless round trip failed")
            surface["derivatives"].append({
                "path": path.relative_to(ROOT).as_posix(), "width": size, "height": size, "resize": resize,
                "presentation_scale": round(size / base.NATIVE_PX, 4), "format": "image/webp (lossless)",
                "bytes": path.stat().st_size, "sha256": base.sha256(path)})
        if spec["legend"]:
            ramp = np.repeat(lut[None, :, :], 8, axis=0)   # unblended canonical colours
            lpath = OUT / f"{key}-legend-{hashlib.sha256(lut.tobytes()).hexdigest()[:8]}.png"
            Image.fromarray(ramp, "RGB").save(lpath, optimize=True)
            surface["legend"] = {
                "path": lpath.relative_to(ROOT).as_posix(), "width": base.LEGEND_W, "height": 8,
                "content": "the unblended 256-entry LUT, low at left to high at right",
                "coupled_to": "the windowed canonical coordinate: the left end is the 2nd and the right end the "
                              "98th percentile of the governed valid cells; values beyond them sit on the end "
                              "colours. A dimensionless proxy, so the ramp carries words (lower / higher), not numbers",
                "bytes": lpath.stat().st_size, "sha256": base.sha256(lpath)}
        else:
            home = json.loads(MANIFEST.read_text(encoding="utf-8"))["web_005b"]["analytical"]["layers"]["priority"]
            if surface["lut_sha256"] != home["lut_sha256"]:
                raise SystemExit("relief: the priority LUT drifted from the homepage record")
            ramp = home["legend"]
            surface["legend"] = {
                "path": ramp["path"], "sha256": ramp["sha256"], "record": "web_005b.analytical.layers.priority.legend",
                "reuse": "the homepage's unblended 0-100 priority ramp: same LUT, no window, no gamma, so position "
                         "on the ramp is the score itself (MER-108 section 6: legends use unblended colours)"}
        record["surfaces"][key] = surface
    return record


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--record", action="store_true", help="write the record to sources.json -> mer_242")
    args = ap.parse_args()
    rec = build()
    if args.record:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        manifest["mer_242"] = rec
        # bytes, so the manifest keeps LF line endings on Windows too
        MANIFEST.write_bytes((json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    json.dump(rec, sys.stdout, indent=1, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
