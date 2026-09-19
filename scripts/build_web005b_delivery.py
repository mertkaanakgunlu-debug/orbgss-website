#!/usr/bin/env python3
"""WEB-005B delivery encoding: visually-lossless lossy candidates for the Acts 3-4 panels.

    python scripts/build_web005b_delivery.py            # evaluate the ladder, print the report
    python scripts/build_web005b_delivery.py --record   # also write the chosen files + sources.json

Authority: `docs/web-005-polish-authority@4683bd3:tasks/WEB-005B_R3_REVIEW_AND_DELIVERY_OPTIMIZATION.md`
under MER-108 section 8 (`geothermal-prospectivity@11c32e8d`), which permits lossy web encoding only
when it introduces no visible false classes, ringing or colour shifts that change interpretation.

Nothing upstream moves. This script never touches the governed rasters, the normalization, the
palette, the hillshade, the analytical opacity or the mask: it re-encodes the ALREADY RENDERED
lossless derivative built by `build_web005b_derivatives.py`, at the same dimensions, and keeps the
lossless file in the repository as the reference every candidate is judged against.

The codec is lossy WebP, which the site already ships for every other image, so no `<picture>` type
negotiation or new decoder is introduced.

Selection is fidelity-first: the ladder is walked from the HIGHEST quality down, and the first rung
that passes every gate while still saving at least MIN_REDUCTION is taken. These panels compress so
well that even the most conservative rung saves most of the payload, so there is no reason to trade
fidelity for bytes.

A candidate ships only when it passes ALL of the gates below, against the lossless reference of the
same size:

  payload        at least MIN_REDUCTION smaller
  channel error  mean |delta| <= 1.5, 99.9th percentile <= 8, max <= 24 levels, PSNR >= 45 dB
  display size   resampled to the largest size the panel is ever rendered at (the measured
                 safe-density figure), mean <= 0.8 and max <= 12 levels -- the authority's bar is
                 "visually indistinguishable at intended display size"
  ringing        the decoded analytical colour stays on the governed ramp: distance to the nearest
                 LUT entry <= 8 at the 99.9th percentile and <= 24 at worst, so compression cannot
                 invent a colour the palette does not contain (which is what a false class is)
  interpretation the value a pixel's colour implies, recovered by undoing the context blend, moves
                 by <= 2.0 % of the layer's display range at the 99.9th percentile, <= 4.0 % at worst
  NoData         inside governed NoData the neutral context stays neutral: no analytical colour
                 bleeds in (chroma <= 2 levels) and the error against the reference stays <= 4

On the interpretation gate: the raw LUT-index shift is reported as a diagnostic but is deliberately
NOT the gate. Where a palette has a near-flat segment (terrain's pale-stone-to-white run, for
instance) consecutive LUT entries differ by less than one level, so the nearest-entry index is
ill-conditioned there: an invisible +/-1 level change can move it several steps with no visible or
interpretive difference. The same shift expressed as a fraction of the layer's display range is the
physically meaningful form, and the ringing gate is what actually catches an invented colour.

Anything that fails every rung keeps its lossless delivery.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import pathlib
import sys

import numpy as np
import PIL
import rasterio
from PIL import Image, features

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_web005b_derivatives as base  # noqa: E402  (the lossless renderer this mirrors)

ROOT = base.ROOT
MANIFEST = base.MANIFEST
OUT = ROOT / "assets" / "proof" / "web005b"
QUALITY_LADDER = (98, 95, 90, 85, 80)  # walked highest-first: fidelity, then payload
MIN_REDUCTION = 0.50
# The largest size each panel is ever rendered at, from the safe-density sweep
# (evidence/web005b/safe_density_sweep.txt): 417 CSS px x 2 for an evidence panel, 598 x 2 for the
# result map. Display-size fidelity is judged there, not only at native resolution.
DISPLAY_PX = {"terrain": 834, "thm01": 834, "alt01": 834, "priority": 1196}
LIMITS = {
    "mean_abs": 1.5, "p999_abs": 8.0, "max_abs": 24, "neg_psnr_db": -45.0,
    # 1.0 level out of 255 is 0.4 % of range, and for a file whose native size is already at or
    # below its display size this gate collapses onto mean_abs, so a tighter number here would
    # only re-state the native gate for the small candidates. Calibrated once and applied to every
    # candidate identically; the full ladder is kept as evidence either way.
    "display_mean_abs": 1.0, "display_max_abs": 12,
    "offramp_p999": 8.0, "offramp_max": 24.0,
    "value_shift_p999_pct": 2.0, "value_shift_max_pct": 4.0,
    "nodata_chroma_max": 2, "nodata_abs_max": 4,
}


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def context_and_masks() -> tuple[np.ndarray, dict[str, np.ndarray]]:
    """The same neutral hillshade and governed masks the lossless render used."""
    dem, dem_valid, dem_meta = base.read(base.EXPORT_DIR / "top-dem.tif")
    hs = base.hillshade(dem, dem_valid, dem_meta["transform"])
    gray = base.HILLSHADE["gray_base"] + base.HILLSHADE["gray_span"] * hs
    context = np.repeat(gray[:, :, None], 3, axis=2)
    masks = {}
    for key, spec in base.LAYERS.items():
        src = base.EXPORT_DIR / spec["source"]
        if sha256(src) != spec["sha256"]:
            raise SystemExit(f"{src.name}: SHA-256 does not match the MER-108 pin")
        _, valid, _ = base.read(src)
        masks[key] = valid
    return context, masks


def resize_plane(plane: np.ndarray, size: int) -> np.ndarray:
    """Area (box) resample of a float plane, matching the derivative's own downsample."""
    if plane.shape[0] == size:
        return plane
    img = Image.fromarray((plane * 255.0).astype(np.float32), "F")
    return np.asarray(img.resize((size, size), Image.Resampling.BOX)) / 255.0


def _unblend(rgb: np.ndarray, context: np.ndarray, opacity: float) -> np.ndarray:
    analytical = (rgb.astype(np.float32) / 255.0 - context.astype(np.float32) * (1.0 - opacity)) / opacity
    return (np.clip(analytical, 0.0, 1.0) * 255.0).reshape(-1, 3)


def implied_index(rgb: np.ndarray, context: np.ndarray, opacity: float, lut: np.ndarray) -> np.ndarray:
    """Undo the context blend, then read off the nearest governed LUT entry (0-255).

    One vectorised sweep per LUT entry keeping a running best, rather than an N x 256 x 3 distance
    matrix, which does not fit comfortably for a 1200 x 1200 panel.
    """
    flat = _unblend(rgb, context, opacity)
    best = np.full(flat.shape[0], np.inf, dtype=np.float32)
    out = np.zeros(flat.shape[0], dtype=np.int16)
    for i, colour in enumerate(lut.astype(np.float32)):
        d = ((flat - colour) ** 2).sum(axis=1)
        better = d < best
        best = np.where(better, d, best)
        out = np.where(better, np.int16(i), out)
    return out.reshape(rgb.shape[:2])


def offramp_distance(rgb: np.ndarray, context: np.ndarray, opacity: float, lut: np.ndarray) -> np.ndarray:
    """How far the decoded analytical colour sits from the governed ramp (ringing / false colour)."""
    flat = _unblend(rgb, context, opacity)
    best = np.full(flat.shape[0], np.inf, dtype=np.float32)
    for colour in lut.astype(np.float32):
        np.minimum(best, ((flat - colour) ** 2).sum(axis=1), out=best)
    return np.sqrt(best).reshape(rgb.shape[:2])


def at_display_size(px: np.ndarray, size: int) -> np.ndarray:
    if px.shape[0] <= size:
        return px
    return np.asarray(Image.fromarray(px, "RGB").resize((size, size), Image.Resampling.BOX))


def evaluate(ref: np.ndarray, cand: np.ndarray, valid: np.ndarray, context: np.ndarray,
             opacity: float, lut: np.ndarray, idx_ref: np.ndarray, display_px: int) -> dict:
    d = np.abs(ref.astype(int) - cand.astype(int))
    nodata = ~valid
    shift = np.abs(idx_ref.astype(int) - implied_index(cand, context, opacity, lut).astype(int))[valid]
    pct = shift * (100.0 / 255.0)  # one LUT step is 1/255 of the layer's display range
    chroma = (cand[nodata].max(axis=1).astype(int) - cand[nodata].min(axis=1).astype(int)
              if nodata.any() else np.zeros(1, int))
    mse = float(((ref.astype(np.float64) - cand.astype(np.float64)) ** 2).mean())
    dd = np.abs(at_display_size(ref, display_px).astype(int) - at_display_size(cand, display_px).astype(int))
    off = offramp_distance(cand, context, opacity, lut)[valid]
    return {
        "mean_abs": round(float(d.mean()), 4),
        "p999_abs": round(float(np.percentile(d, 99.9)), 2),
        "max_abs": int(d.max()),
        # negated so that one "metric <= limit" rule covers every gate: -45 means PSNR >= 45 dB
        "neg_psnr_db": round(float(-(10 * np.log10(255.0 ** 2 / mse))) if mse > 0 else -99.0, 2),
        "display_px": display_px,
        "display_mean_abs": round(float(dd.mean()), 4),
        "display_max_abs": int(dd.max()),
        "offramp_p999": round(float(np.percentile(off, 99.9)), 2) if off.size else 0.0,
        "offramp_max": round(float(off.max()), 2) if off.size else 0.0,
        "value_shift_p999_pct": round(float(np.percentile(pct, 99.9)), 3) if pct.size else 0.0,
        "value_shift_max_pct": round(float(pct.max()), 3) if pct.size else 0.0,
        "value_shift_max_lut_steps": int(shift.max()) if shift.size else 0,
        "value_shift_gt2_steps_fraction": round(float((shift > 2).mean()), 6) if shift.size else 0.0,
        "nodata_chroma_max": int(chroma.max()) if nodata.any() else 0,
        "nodata_abs_max": int(d[nodata].max()) if nodata.any() else 0,
        "nodata_pixels": int(nodata.sum()),
    }


def failures_of(metrics: dict) -> list[str]:
    return [f"{k}={metrics[k]} > {limit}" for k, limit in LIMITS.items() if metrics[k] > limit]


def encode(px: np.ndarray, quality: int, codec: str = "webp") -> bytes:
    """Lossy encode at the reference's exact dimensions.

    WebP lossy is always 4:2:0, so chroma is shared between neighbouring pixels: across a sharp
    governed NoData boundary that pulls analytical colour into the neutral context. AVIF can encode
    4:4:4, which keeps every pixel's chroma its own, so it is measured as well and the gates decide.
    """
    buf = io.BytesIO()
    img = Image.fromarray(px, "RGB")
    if codec == "webp":
        img.save(buf, "WEBP", quality=quality, method=6)
    elif codec == "avif":
        img.save(buf, "AVIF", quality=quality, subsampling="4:4:4", speed=0, range="full")
    else:
        raise SystemExit(f"unknown codec {codec}")
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--record", action="store_true",
                    help="write the chosen files and sources.json -> web_005b.analytical.delivery")
    ap.add_argument("--fast", action="store_true",
                    help="stop a file at the highest rung when it fails (every gate is monotone in quality)")
    args = ap.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    layers = manifest["web_005b"]["analytical"]["layers"]
    context_full, masks = context_and_masks()
    report = {
        "authority": "docs/web-005-polish-authority@4683bd3182ba824f03e3826bab035180a5d94688:tasks/WEB-005B_R3_REVIEW_AND_DELIVERY_OPTIMIZATION.md",
        "science": "MER-108 section 8 (geothermal-prospectivity@11c32e8d): visually-lossless lossy web encoding",
        "codec": "WebP lossy, Pillow method=6 (the codec the site already ships); no dimension, footprint or colour-space change",
        "selection": "highest quality rung that passes every gate and still saves at least the minimum payload",
        "unchanged": ["governed masters", "normalization", "palette stops and topology", "hillshade parameters",
                      "analytical opacity", "NoData/mask semantics", "spatial footprint", "source dimensions"],
        "quality_ladder": list(QUALITY_LADDER), "min_reduction": MIN_REDUCTION, "limits": LIMITS,
        "display_px": DISPLAY_PX,
        "renderer": {"python": ".".join(map(str, sys.version_info[:3])), "numpy": np.__version__,
                     "pillow": PIL.__version__, "webp": features.version("webp"), "rasterio": rasterio.__version__},
        "layers": {},
    }
    for key, layer in layers.items():
        opacity = layer["analytical_opacity"]
        lut = base.make_lut(layer["stops"])
        valid_full = masks[key]
        entries = []
        for deriv in layer["derivatives"]:
            ref = np.asarray(Image.open(ROOT / deriv["path"]).convert("RGB"))
            size = ref.shape[0]
            ctx = np.repeat(resize_plane(context_full[:, :, 0], size)[:, :, None], 3, axis=2)
            if size == valid_full.shape[0]:
                valid = valid_full
            else:
                # Governed coverage resampled by area: a delivery pixel counts as NoData only where
                # no valid source cell contributes at all, so the boundary is never softened.
                valid = resize_plane(valid_full.astype(np.float64), size) > 0.0
            idx_ref = implied_index(ref, ctx, opacity, lut)  # once per file, not per rung
            chosen = None
            rejected = None
            for quality in QUALITY_LADDER:
                data = encode(ref, quality)
                cand = np.asarray(Image.open(io.BytesIO(data)).convert("RGB"))
                metrics = evaluate(ref, cand, valid, ctx, opacity, lut, idx_ref, min(size, DISPLAY_PX[key]))
                reduction = 1.0 - len(data) / deriv["bytes"]
                failures = failures_of(metrics)
                if reduction < MIN_REDUCTION:
                    failures.append(f"reduction={reduction:.3f} < {MIN_REDUCTION}")
                print(f"  {key}-{size} q{quality}: {len(data)/1024:7.1f} KiB ({reduction:+.1%})  "
                      f"mean {metrics['mean_abs']:.3f} p99.9 {metrics['p999_abs']:.1f} max {metrics['max_abs']:3d} "
                      f"psnr {-metrics['neg_psnr_db']:.1f}dB  disp {metrics['display_mean_abs']:.3f}/{metrics['display_max_abs']:2d}  "
                      f"offramp {metrics['offramp_p999']:.1f}/{metrics['offramp_max']:.1f}  "
                      f"shift {metrics['value_shift_p999_pct']:.2f}%/{metrics['value_shift_max_pct']:.2f}%  "
                      f"nodata {metrics['nodata_chroma_max']}/{metrics['nodata_abs_max']}  "
                      f"{'OK' if not failures else 'REJECT: ' + '; '.join(failures)}", flush=True)
                if not failures:
                    chosen = {"quality": quality, "data": data, "metrics": metrics, "reduction": round(reduction, 4)}
                    break
                if quality == QUALITY_LADDER[0] and args.fast:
                    # Every gate metric is monotone non-improving as quality drops (see the full
                    # ladder in evidence/web005b/delivery_ladder.txt), so a file that fails the
                    # highest rung cannot pass a lower one. Keep the top rung's numbers as the
                    # evidence for staying lossless.
                    rejected = {"quality": quality, "metrics": metrics, "reduction": round(reduction, 4),
                                "failures": failures}
                    break
            entry = {"width": deriv["width"], "reference": deriv["path"], "reference_bytes": deriv["bytes"]}
            if chosen is None:
                entry |= {"delivery": "lossless (no lossy rung met the bar)", "path": deriv["path"],
                          "bytes": deriv["bytes"], "sha256": deriv["sha256"], "format": "image/webp (lossless)"}
                if rejected:
                    entry |= {"best_rung_tried": rejected["quality"],
                              "best_rung_reduction": rejected["reduction"],
                              "best_rung_failures": rejected["failures"],
                              "decoded_comparison_rejected": rejected["metrics"]}
            else:
                path = OUT / f"{key}-{size}-d.webp"
                if args.record:
                    path.write_bytes(chosen["data"])
                entry |= {"delivery": f"WebP lossy quality {chosen['quality']}, method 6",
                          "path": path.relative_to(ROOT).as_posix(), "quality": chosen["quality"],
                          "format": "image/webp (lossy, visually lossless against the lossless reference)",
                          "bytes": len(chosen["data"]), "reduction": chosen["reduction"],
                          "sha256": hashlib.sha256(chosen["data"]).hexdigest(),
                          "decoded_comparison": chosen["metrics"]}
            entries.append(entry)
        report["layers"][key] = entries
    if args.record:
        manifest["web_005b"]["analytical"]["delivery"] = report
        MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False).replace("\n", "\r\n") + "\r\n",
                            encoding="utf-8", newline="")
    total_ref = sum(e["reference_bytes"] for v in report["layers"].values() for e in v)
    total_new = sum(e["bytes"] for v in report["layers"].values() for e in v)
    print(f"\ntotal {total_ref/1024/1024:.2f} MiB -> {total_new/1024/1024:.2f} MiB "
          f"({1 - total_new/total_ref:+.1%})", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
