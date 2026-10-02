#!/usr/bin/env python3
"""MER-216 Phase 1 independent conformance check.

Does NOT import or call scripts/build_web005b_presentation.py. It re-derives, with its own
implementation of the recorded pipeline, what every published lossless native-grid derivative must
contain, straight from the governed MER-113 export, and compares pixel for pixel. It also checks
the NoData/mask semantics and the palette directly against sources.json, and that the downsampled
rungs are exact box downsamples of the native rung.

    python verify_phase1_independent.py <repo_root> <export_dir> <out.json>
"""
import hashlib
import json
import pathlib
import sys

import numpy as np
import rasterio
from PIL import Image

repo = pathlib.Path(sys.argv[1])
export = pathlib.Path(sys.argv[2])
man = json.loads((repo / "assets/imagery/sources.json").read_text(encoding="utf-8"))["web_005b"]["analytical"]
H = man["hillshade"]
report = {"layers": {}, "failures": []}


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def read(p):
    with rasterio.open(p) as ds:
        b = ds.read(1, masked=True)
        a = b.filled(np.nan).astype(np.float64)
        v = np.isfinite(a) & ~np.ma.getmaskarray(b)
        return a, v, list(ds.transform)[:6], str(ds.crs), ds.width, ds.height


def lut_from_hex(stops):
    arr = np.array([[int(s.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)] for s in stops], dtype=np.float64)
    xp = np.linspace(0, 1, len(arr))
    x = np.linspace(0, 1, 256)
    return np.stack([np.clip(np.interp(x, xp, arr[:, c]), 0, 255).astype(np.uint8) for c in range(3)], axis=1)


def fail(msg):
    report["failures"].append(msg)
    print("FAIL", msg)


dem, dem_valid, tr, crs, W, Hh = read(export / "top-dem.tif")
assert (W, Hh) == (1200, 1200) and crs == "EPSG:32635"
if [float(t) for t in tr] != [float(t) for t in man["grid"]["transform"]]:
    fail("DEM transform differs from recorded grid")
filled = np.where(dem_valid, dem, np.nanmedian(dem[dem_valid]))
dy, dx = np.gradient(filled * H["z_factor"], abs(tr[4]), abs(tr[0]))
slope = np.pi / 2 - np.arctan(np.hypot(dx, dy))
aspect = np.arctan2(-dx, dy)
az, alt = np.deg2rad(H["azimuth_deg"]), np.deg2rad(H["altitude_deg"])
hs = np.clip(np.sin(alt) * np.sin(slope) + np.cos(alt) * np.cos(slope) * np.cos(az - aspect), 0, 1)
gray = H["gray_base"] + H["gray_span"] * hs

for key, L in man["layers"].items():
    src = export / L["source"]
    if sha(src) != L["source_sha256"]:
        fail(f"{key}: governed source SHA-256 mismatch")
    data, valid, t2, c2, w2, h2 = read(src)
    if (t2, c2, w2, h2) != (tr, crs, W, Hh):
        fail(f"{key}: grid differs from the DEM grid")
    v = data[valid]
    norm = L["normalization"]
    if norm == "linear_min_max":
        lo, hi = float(v.min()), float(v.max())
        n = (data - lo) / max(hi - lo, 1e-9)
        signed = False
        if (lo, hi) != (L["resolved"]["vmin"], L["resolved"]["vmax"]):
            fail(f"{key}: resolved vmin/vmax differ from record")
    elif norm == "diverging_symmetric_from_data":
        m = max(abs(float(v.min())), abs(float(v.max())))
        n = data / m
        signed = True
        if m != L["resolved"]["M"]:
            fail(f"{key}: resolved M differs from record")
    elif norm == "fixed_range_0_100":
        n = data / 100.0
        signed = False
    else:
        raise SystemExit(norm)
    dw = L["display_window"]
    nv = n[valid]
    if dw != "disabled":
        if dw["kind"] == "quantile":
            lo, hi = float(np.quantile(nv, dw["q_low"])), float(np.quantile(nv, dw["q_high"]))
            n = np.clip((n - lo) / max(hi - lo, 1e-12), 0, 1)
        else:
            m = float(np.quantile(np.abs(nv), dw["q_abs"]))
            n = np.clip(n / m, -1, 1)
    g = L["gamma"]
    if g != "disabled":
        gm = g["gamma"]
        n = np.sign(n) * np.power(np.abs(n), gm) if signed else np.power(np.clip(n, 0, 1), gm)
    unit = (n + 1) / 2 if signed else n
    unit = np.where(valid, np.clip(unit, 0, 1), 0)
    lut = lut_from_hex(L["stops"])
    if hashlib.sha256(lut.tobytes()).hexdigest() != L["lut_sha256"]:
        fail(f"{key}: LUT SHA-256 differs from record")
    idx = np.clip(np.round(unit * 255), 0, 255).astype(np.uint8)
    rgb = lut[idx].astype(np.float64) / 255
    a = np.where(valid, L["analytical_opacity"], 0.0)
    exp = np.clip(np.round((rgb * a[:, :, None] + np.repeat(gray[:, :, None], 3, axis=2) * (1 - a[:, :, None])) * 255), 0, 255).astype(np.uint8)

    rec = {"valid_fraction": round(float(valid.mean()), 6), "native": {}, "box": []}
    native_path = repo / [d for d in L["derivatives"] if d["width"] == 1200][0]["path"]
    got = np.asarray(Image.open(native_path).convert("RGB"))
    diff = int(np.count_nonzero(np.any(got != exp, axis=2)))
    rec["native"] = {"path": native_path.relative_to(repo).as_posix(), "pixels_differing_from_independent_rederivation": diff}
    if diff:
        fail(f"{key}: native derivative differs from independent re-derivation in {diff} pixels")
    # NoData semantics: outside the governed mask the pixel must be the neutral hillshade only
    nd = ~valid
    ndn = int(nd.sum())
    neutral = np.clip(np.round(np.repeat(gray[:, :, None], 3, axis=2) * 255), 0, 255).astype(np.uint8)
    nd_bad = int(np.count_nonzero(np.any(got[nd] != neutral[nd], axis=1))) if ndn else 0
    ch = got[nd].astype(int)
    chroma = int((ch.max(axis=1) - ch.min(axis=1)).max()) if ndn else 0
    rec["nodata"] = {"cells": ndn, "pixels_not_pure_neutral_hillshade": nd_bad, "max_chroma": chroma}
    if nd_bad or chroma:
        fail(f"{key}: NoData cells are not pure neutral hillshade")
    # every valid pixel's analytical colour is on the governed ramp (alpha-blend inverse)
    # box rungs are exact area downsamples of the native rung
    for d in L["derivatives"]:
        if d["width"] == 1200:
            continue
        box = np.asarray(Image.fromarray(got, "RGB").resize((d["width"], d["width"]), Image.Resampling.BOX))
        pub = np.asarray(Image.open(repo / d["path"]).convert("RGB"))
        nd_ = int(np.count_nonzero(np.any(box != pub, axis=2)))
        rec["box"].append({"path": d["path"], "pixels_differing_from_box_of_native": nd_})
        if nd_:
            fail(f"{key}: {d['path']} is not the box downsample of the native rung")
    for d in L["derivatives"]:
        if sha(repo / d["path"]) != d["sha256"]:
            fail(f"{key}: {d['path']} SHA-256 differs from record")
    if key == "priority":
        lg = repo / L["legend"]["path"]
        ramp = np.asarray(Image.open(lg).convert("RGB"))
        if not np.array_equal(ramp[0], lut) or sha(lg) != L["legend"]["sha256"]:
            fail("priority legend ramp is not the unblended 256-entry LUT")
        rec["legend_ramp_equals_lut"] = bool(np.array_equal(ramp[0], lut))
    report["layers"][key] = rec
    print(key, "native diff px:", diff, "| nodata cells:", ndn, "bad:", nd_bad, "chroma:", chroma)

report["result"] = "PASS" if not report["failures"] else "FAIL"
json.dump(report, open(sys.argv[3], "w", encoding="utf-8"), indent=1)
print("RESULT", report["result"])
