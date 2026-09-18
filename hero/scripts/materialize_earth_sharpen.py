"""Build the regional Earth *detail multiplier* from Copernicus Sentinel-2 L2A tiles, inside Blender.

    blender -b -P hero/scripts/materialize_earth_sharpen.py -- --scene-dir <dir> --date 20250925

WEB-005A R3 ends on a regional hold whose frame is about 150 km wide, so the 36 km analysis AOI can
receive the page-layer result at a readable size. At that scale the 500 m Blue Marble window the R2
hold resolved is magnified about five times and goes soft. No rights-safe *colour* source at 30 m
covers the whole hold, and a second natural-colour composite would in any case bring its own
season, haze and colour vocabulary and show a seam against the global albedo.

So the R3 approach does not replace the colour at all. It keeps the Blue Marble colour everywhere
and multiplies it, inside a window around the target, by a *detail ratio* derived from Sentinel-2:
the broadband reflectance of the 10 m red and blue bands divided by the same reflectance blurred to
the Blue Marble's own resolution. Where the Sentinel-2 ground is brighter than its 500 m
neighbourhood the albedo is lifted, where it is darker it is lowered, and the mean over any 500 m
patch is unchanged by construction -- the same pan-sharpening idea every map viewer uses, applied
to a cinematic texture. There is no seam because the colour never changes, and no season because
only the structure of the ground -- valleys, ridges, field patterns, towns, coastline -- is carried.

What this is *not*: a measured layer. The ratio is a presentation texture with no units, no
classification and no palette; the validator's forbidden-layer vocabulary does not name it, and it
is never delivered to the page. Rights: Copernicus Sentinel data are free, full and open, with the
attribution the manifest records. The scene classification band masks cloud, shadow, snow and
missing pixels back to a ratio of 1 (i.e. Blue Marble alone), and open water is held close to 1.

Geometry: the tiles are EPSG:32635 (UTM zone 35N). The output is an equirectangular window, which
is what the Earth material samples, so each output texel is inverse-mapped through the UTM forward
projection (Snyder 1987, eq. 8-9 to 8-15, WGS84) and bilinearly sampled from the 30 m mosaic. The
mapping is verified against the accepted Kizildere centre before anything is written.

Blender's bundled numpy does the work; the lane has no other Python image stack, and Blender is
already its one production tool. Output is a 16-bit greyscale PNG, ratio encoded as value / 2.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bpy  # noqa: E402
import numpy as np  # noqa: E402  (Blender's bundled numpy)

import hero_common as hc  # noqa: E402

# WGS84 / UTM constants (Snyder 1987).
A_WGS84 = 6378137.0
F_WGS84 = 1.0 / 298.257223563
K0 = 0.9996
FALSE_EASTING = 500000.0

# Sentinel-2 L2A processing baseline >= 04.00: BOA reflectance = (DN + BOA_ADD_OFFSET) / 10000.
BOA_QUANT = 10000.0
BOA_OFFSET = -1000.0
# JP2 codestream precision of the 10 m bands (parsed from the SIZ marker, verified below).
S2_PREC = 15
# Scene classification classes (SCL): 0 no data, 1 saturated/defective, 2 dark, 3 cloud shadow,
# 4 vegetation, 5 not vegetated, 6 water, 7 unclassified, 8 cloud medium, 9 cloud high,
# 10 thin cirrus, 11 snow/ice.
SCL_MASKED = (0, 1, 3, 8, 9, 10, 11)
SCL_WATER = 6

RATIO_ENCODE = 2.0  # stored value = ratio / RATIO_ENCODE


def utm_forward(lat_deg, lon_deg, zone: int):
    """WGS84 geographic -> UTM (northern hemisphere) easting/northing, vectorised."""
    e2 = 2.0 * F_WGS84 - F_WGS84 * F_WGS84
    ep2 = e2 / (1.0 - e2)
    lat = np.radians(lat_deg)
    lon0 = math.radians((zone - 1) * 6 - 180 + 3)
    lon = np.radians(lon_deg)
    sin_lat, cos_lat, tan_lat = np.sin(lat), np.cos(lat), np.tan(lat)
    n = A_WGS84 / np.sqrt(1.0 - e2 * sin_lat * sin_lat)
    t = tan_lat * tan_lat
    c = ep2 * cos_lat * cos_lat
    a = (lon - lon0) * cos_lat
    m = A_WGS84 * (
        (1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256) * lat
        - (3 * e2 / 8 + 3 * e2 ** 2 / 32 + 45 * e2 ** 3 / 1024) * np.sin(2 * lat)
        + (15 * e2 ** 2 / 256 + 45 * e2 ** 3 / 1024) * np.sin(4 * lat)
        - (35 * e2 ** 3 / 3072) * np.sin(6 * lat)
    )
    x = K0 * n * (a + (1 - t + c) * a ** 3 / 6 + (5 - 18 * t + t * t + 72 * c - 58 * ep2) * a ** 5 / 120) + FALSE_EASTING
    y = K0 * (m + n * tan_lat * (a * a / 2 + (5 - t + 9 * c + 4 * c * c) * a ** 4 / 24
                                 + (61 - 58 * t + t * t + 600 * c - 330 * ep2) * a ** 6 / 720))
    return x, y


def jp2_precision(path: Path) -> int:
    head = path.read_bytes()[:8192]
    index = head.find(b"\xff\x51")
    if index < 0:
        raise SystemExit("no SIZ marker in " + str(path))
    return (head[index + 40] & 0x7F) + 1


def load_band(path: Path, expect_size: int) -> np.ndarray:
    """One JP2 band as float32 DN, row 0 = north (Blender's buffer is bottom-up, so flip)."""
    started = time.time()
    prec = jp2_precision(path)
    image = bpy.data.images.load(str(path))
    image.colorspace_settings.name = "Non-Color"
    if tuple(image.size) != (expect_size, expect_size):
        raise SystemExit(path.name + " is " + str(tuple(image.size)) + ", expected square " + str(expect_size))
    buffer = np.empty(expect_size * expect_size * image.channels, dtype=np.float32)
    image.pixels.foreach_get(buffer)
    band = buffer.reshape(expect_size, expect_size, image.channels)[:, :, 0].copy()
    del buffer
    bpy.data.images.remove(image)
    band *= float((1 << prec) - 1)  # OpenImageIO normalises by the codestream precision
    band = band[::-1, :]            # north up
    print("[hero] loaded " + path.name + " prec " + str(prec) + " in " + str(round(time.time() - started, 1)) + " s", flush=True)
    return np.ascontiguousarray(band)


def block_mean(array: np.ndarray, factor: int) -> np.ndarray:
    h, w = array.shape
    h2, w2 = h // factor, w // factor
    return array[:h2 * factor, :w2 * factor].reshape(h2, factor, w2, factor).mean(axis=(1, 3))


def box_blur(array: np.ndarray, radius: int) -> np.ndarray:
    """Separable box blur with edge replication, via cumulative sums."""
    def blur_axis(a, axis):
        pad = [(0, 0), (0, 0)]
        pad[axis] = (radius, radius)
        padded = np.pad(a, pad, mode="edge")
        cumsum = np.cumsum(padded, axis=axis, dtype=np.float64)
        cumsum = np.concatenate([np.zeros_like(np.take(cumsum, [0], axis=axis)), cumsum], axis=axis)
        width = 2 * radius + 1
        n = a.shape[axis]
        upper = np.take(cumsum, np.arange(width, width + n), axis=axis)
        lower = np.take(cumsum, np.arange(0, n), axis=axis)
        return ((upper - lower) / width).astype(np.float32)
    return blur_axis(blur_axis(array, 0), 1)


def tile_geometry(metadata_path: Path):
    text = metadata_path.read_text(encoding="utf-8", errors="replace")
    epsg = re.search(r"<HORIZONTAL_CS_CODE>([^<]+)", text).group(1).strip()
    ulx = float(re.search(r"<ULX>([^<]+)", text).group(1))
    uly = float(re.search(r"<ULY>([^<]+)", text).group(1))
    cloud = float(re.search(r"<CLOUDY_PIXEL_PERCENTAGE>([^<]+)", text).group(1))
    sensing = re.search(r"<SENSING_TIME[^>]*>([^<]+)", text).group(1).strip()
    return {"epsg": epsg, "ulx": ulx, "uly": uly, "cloudy_pixel_percentage": cloud, "sensing_time": sensing}


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize the Sentinel-2 detail multiplier window.")
    parser.add_argument("--scene-dir", required=True, help="directory holding the *_B02_10m.jp2 / *_B04_10m.jp2 / *_SCL_20m.jp2 files")
    parser.add_argument("--date", required=True, help="acquisition date token in the file names, e.g. 20250925")
    parser.add_argument("--tiles", nargs="+", default=["T35SPC", "T35SPB"], help="MGRS tiles, north to south")
    parser.add_argument("--zone", type=int, default=35)
    parser.add_argument("--blur-radius-px", type=int, default=8, help="box radius at 30 m; 8 -> 17 px = 510 m, the Blue Marble texel")
    parser.add_argument("--out", default="s2_kizildere_detail_30m.png")
    parser.add_argument("--record", default="hero/evidence/earth_detail_sharpen.json")
    parser.add_argument("--verify-lat", type=float, default=37.9794)
    parser.add_argument("--verify-lon", type=float, default=28.7907)
    parser.add_argument("--verify-easting", type=float, default=657268.9)
    parser.add_argument("--verify-northing", type=float, default=4205042.0)
    args = parser.parse_args(hc.argv_after_double_dash())

    scene_dir = Path(args.scene_dir)
    # --- verify the projection against the accepted Kizildere centre -------------------------
    ex, ny = utm_forward(np.array([args.verify_lat]), np.array([args.verify_lon]), args.zone)
    error_m = math.hypot(float(ex[0]) - args.verify_easting, float(ny[0]) - args.verify_northing)
    print("[hero] UTM check: " + str(round(float(ex[0]), 1)) + " E " + str(round(float(ny[0]), 1))
          + " N, error " + str(round(error_m, 2)) + " m", flush=True)
    if error_m > 2.0:
        raise SystemExit("UTM forward projection disagrees with the accepted centre by " + str(error_m) + " m")

    # --- per-tile pan reflectance at 30 m + masks -------------------------------------------
    tiles = []
    sources = []
    for tile in args.tiles:
        def find(pattern):
            matches = sorted(scene_dir.glob("*" + args.date + "*" + tile + "*" + pattern))
            if not matches:
                raise SystemExit("no " + pattern + " for " + tile + " " + args.date + " in " + str(scene_dir))
            return matches[0]
        red_path, blue_path, scl_path, meta_path = (find("_B04_10m.jp2"), find("_B02_10m.jp2"),
                                                    find("_SCL_20m.jp2"), find("_granule_metadata.xml"))
        geometry = tile_geometry(meta_path)
        if geometry["epsg"] != "EPSG:" + str(32600 + args.zone):
            raise SystemExit(tile + " is " + geometry["epsg"] + ", expected UTM zone " + str(args.zone))
        red = load_band(red_path, 10980)
        red = block_mean(red, 3)
        blue = load_band(blue_path, 10980)
        blue = block_mean(blue, 3)
        refl_red = np.clip((red + BOA_OFFSET) / BOA_QUANT, 0.0, 1.5)
        refl_blue = np.clip((blue + BOA_OFFSET) / BOA_QUANT, 0.0, 1.5)
        del red, blue
        pan = (0.6 * refl_red + 0.4 * refl_blue).astype(np.float32)
        del refl_red, refl_blue
        scl = load_band(scl_path, 5490)
        scl = np.rint(scl).astype(np.int16)
        # 20 m -> 30 m nearest: row r at 30 m samples 20 m row floor(r * 1.5)
        idx = np.minimum((np.arange(3660) * 1.5).astype(np.int64), 5489)
        scl30 = scl[idx][:, idx]
        del scl
        masked = np.isin(scl30, SCL_MASKED)
        water = scl30 == SCL_WATER
        tiles.append({"pan": pan, "masked": masked, "water": water, "geometry": geometry, "id": tile})
        for path in (red_path, blue_path, scl_path, meta_path):
            sources.append({"file": path.name, "bytes": path.stat().st_size, "sha256": hc.sha256_file(path)})
        print("[hero] tile " + tile + ": pan mean " + str(round(float(pan.mean()), 4)) + ", masked "
              + str(round(float(masked.mean()) * 100, 3)) + " %, water " + str(round(float(water.mean()) * 100, 2)) + " %", flush=True)

    # --- mosaic on one 30 m UTM grid (north tile first wins in the overlap) -------------------
    ulx = min(t["geometry"]["ulx"] for t in tiles)
    uly = max(t["geometry"]["uly"] for t in tiles)
    lower = min(t["geometry"]["uly"] - 3660 * 30.0 for t in tiles)
    rows = int(round((uly - lower) / 30.0))
    cols = 3660
    pan = np.zeros((rows, cols), dtype=np.float32)
    valid = np.zeros((rows, cols), dtype=bool)
    masked = np.zeros((rows, cols), dtype=bool)
    water = np.zeros((rows, cols), dtype=bool)
    for t in tiles:
        r0 = int(round((uly - t["geometry"]["uly"]) / 30.0))
        c0 = int(round((t["geometry"]["ulx"] - ulx) / 30.0))
        sl = (slice(r0, r0 + 3660), slice(c0, c0 + 3660))
        fill = ~valid[sl]
        pan[sl][fill] = t["pan"][fill]
        masked[sl][fill] = t["masked"][fill]
        water[sl][fill] = t["water"][fill]
        valid[sl] |= True
    del tiles

    # --- detail ratio ---------------------------------------------------------------------
    # Blur a mask-filled pan so clouds/nodata do not bleed into their neighbours' baseline.
    pan_filled = pan.copy()
    if masked.any():
        pan_filled[masked] = float(np.median(pan[~masked]))
    low = box_blur(pan_filled, args.blur_radius_px)
    low = box_blur(low, args.blur_radius_px // 2)  # two passes: closer to a Gaussian than one box
    ratio = pan_filled / np.maximum(low, 1e-3)
    ratio = np.clip(ratio, 0.45, 2.0)
    ratio[water] = np.clip(ratio[water], 0.85, 1.18)
    ratio[masked] = 1.0
    ratio[~valid] = 1.0
    del pan, pan_filled, low
    print("[hero] ratio stats: mean " + str(round(float(ratio.mean()), 4)) + ", p1 "
          + str(round(float(np.percentile(ratio, 1)), 3)) + ", p99 " + str(round(float(np.percentile(ratio, 99)), 3)), flush=True)

    # --- equirectangular window --------------------------------------------------------------
    # Window = the lon/lat bounding box of the mosaic, shrunk to what the projection can fill.
    corners_e = np.array([ulx, ulx + cols * 30.0, ulx, ulx + cols * 30.0])
    corners_n = np.array([uly, uly, lower, lower])
    # inverse corners by iteration on the forward projection (simple 2-D Newton on a plane is
    # overkill: the window only needs to be inside the mosaic, so bracket with a coarse search).
    lat_lo, lat_hi = 30.0, 45.0
    lon_lo, lon_hi = 20.0, 35.0
    for _ in range(40):
        mid = 0.5 * (lat_lo + lat_hi)
        _, n = utm_forward(np.array([mid]), np.array([args.verify_lon]), args.zone)
        lat_lo, lat_hi = (mid, lat_hi) if n[0] < lower else (lat_lo, mid)
    lat0 = lat_hi
    lat_lo, lat_hi = 30.0, 45.0
    for _ in range(40):
        mid = 0.5 * (lat_lo + lat_hi)
        _, n = utm_forward(np.array([mid]), np.array([args.verify_lon]), args.zone)
        lat_lo, lat_hi = (mid, lat_hi) if n[0] < uly else (lat_lo, mid)
    lat1 = lat_lo
    for _ in range(40):  # west edge at the northern latitude (widest offset), east edge likewise
        mid = 0.5 * (lon_lo + lon_hi)
        e, _ = utm_forward(np.array([lat1]), np.array([mid]), args.zone)
        lon_lo, lon_hi = (mid, lon_hi) if e[0] < ulx else (lon_lo, mid)
    lon0 = lon_hi
    lon_lo, lon_hi = 20.0, 35.0
    for _ in range(40):
        mid = 0.5 * (lon_lo + lon_hi)
        e, _ = utm_forward(np.array([lat1]), np.array([mid]), args.zone)
        lon_lo, lon_hi = (mid, lon_hi) if e[0] < ulx + cols * 30.0 else (lon_lo, mid)
    lon1 = lon_lo
    # round outward to 0.01 degree so the recorded window is a clean number the material can carry
    lon0, lon1 = math.floor(lon0 * 100) / 100.0, math.ceil(lon1 * 100) / 100.0
    lat0, lat1 = math.floor(lat0 * 100) / 100.0, math.ceil(lat1 * 100) / 100.0
    mid_lat = 0.5 * (lat0 + lat1)
    dlat = 30.0 / 111320.0
    dlon = 30.0 / (111320.0 * math.cos(math.radians(mid_lat)))
    out_w = int(math.ceil((lon1 - lon0) / dlon))
    out_h = int(math.ceil((lat1 - lat0) / dlat))
    print("[hero] window lon " + str(lon0) + ".." + str(lon1) + " lat " + str(lat0) + ".." + str(lat1)
          + " -> " + str(out_w) + " x " + str(out_h) + " texels at 30 m", flush=True)

    # inverse-map each output texel (row 0 = north) and sample bilinearly
    lons = lon0 + (np.arange(out_w) + 0.5) * (lon1 - lon0) / out_w
    lats = lat1 - (np.arange(out_h) + 0.5) * (lat1 - lat0) / out_h
    out = np.ones((out_h, out_w), dtype=np.float32)
    feather_px = 100.0  # 3 km: ratio eases to 1 toward the mosaic edge so no resolution edge shows
    chunk = 256
    for r0 in range(0, out_h, chunk):
        r1 = min(out_h, r0 + chunk)
        lat_grid = np.repeat(lats[r0:r1, None], out_w, axis=1)
        lon_grid = np.repeat(lons[None, :], r1 - r0, axis=0)
        e, n = utm_forward(lat_grid, lon_grid, args.zone)
        fx = (e - ulx) / 30.0 - 0.5
        fy = (uly - n) / 30.0 - 0.5
        inside = (fx >= 0) & (fy >= 0) & (fx <= cols - 1) & (fy <= rows - 1)
        x0 = np.clip(np.floor(fx), 0, cols - 2).astype(np.int64)
        y0 = np.clip(np.floor(fy), 0, rows - 2).astype(np.int64)
        tx = np.clip(fx - x0, 0.0, 1.0).astype(np.float32)
        ty = np.clip(fy - y0, 0.0, 1.0).astype(np.float32)
        sample = (ratio[y0, x0] * (1 - tx) * (1 - ty) + ratio[y0, x0 + 1] * tx * (1 - ty)
                  + ratio[y0 + 1, x0] * (1 - tx) * ty + ratio[y0 + 1, x0 + 1] * tx * ty)
        edge = np.minimum(np.minimum(fx, cols - 1 - fx), np.minimum(fy, rows - 1 - fy))
        feather = np.clip(edge / feather_px, 0.0, 1.0).astype(np.float32)
        block = 1.0 + (sample - 1.0) * feather
        block[~inside] = 1.0
        out[r0:r1, :] = block
    del ratio

    # --- write 16-bit greyscale PNG (ratio / RATIO_ENCODE), raw values -----------------------
    encoded = np.clip(out / RATIO_ENCODE, 0.0, 1.0)
    image = bpy.data.images.new("earth_detail_sharpen", width=out_w, height=out_h, alpha=False, float_buffer=True)
    image.colorspace_settings.name = "Non-Color"
    rgba = np.empty((out_h, out_w, 4), dtype=np.float32)
    rgba[:, :, 0] = encoded[::-1, :]  # Blender buffers are bottom-up
    rgba[:, :, 1] = rgba[:, :, 0]
    rgba[:, :, 2] = rgba[:, :, 0]
    rgba[:, :, 3] = 1.0
    image.pixels.foreach_set(rgba.reshape(-1))
    del rgba
    scene = bpy.context.scene
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "BW"
    scene.render.image_settings.color_depth = "16"
    scene.render.image_settings.compression = 30
    out_path = hc.SOURCE_DIR / args.out
    image.save_render(filepath=str(out_path), scene=scene)
    bpy.data.images.remove(image)

    # read back and verify the encoding round-trips (the material relies on raw values)
    check = bpy.data.images.load(str(out_path))
    check.colorspace_settings.name = "Non-Color"
    buffer = np.empty(out_w * out_h * check.channels, dtype=np.float32)
    check.pixels.foreach_get(buffer)
    back = buffer.reshape(out_h, out_w, check.channels)[::-1, :, 0]
    round_trip = float(np.abs(back - encoded).max())
    bpy.data.images.remove(check)
    print("[hero] round-trip max error " + str(round_trip) + " (16-bit step " + str(round(1 / 65535, 7)) + ")", flush=True)
    if round_trip > 4.0 / 65535:
        raise SystemExit("PNG round trip lost precision: " + str(round_trip))

    record = {
        "task": "WEB-005A R3 / MER-107 -- regional Earth detail multiplier",
        "method": ("Sentinel-2 L2A 10 m red (B04) and blue (B02) BOA reflectance -> 30 m block mean -> "
                   "broadband pan = 0.6 red + 0.4 blue -> ratio = pan / box-blurred pan (radius "
                   + str(args.blur_radius_px) + " px twice, about 510 m) -> clipped 0.45..2.0, water "
                   "0.85..1.18, SCL cloud/shadow/snow/nodata = 1.0 -> inverse-mapped from an "
                   "equirectangular grid through the WGS84 UTM forward projection and sampled "
                   "bilinearly -> 16-bit PNG, ratio / " + str(RATIO_ENCODE) + ". The Earth material "
                   "multiplies the Blue Marble albedo by this ratio inside the window; the 500 m mean "
                   "is preserved and no colour is introduced."),
        "classification": "presentation detail texture; no units, no palette, not a measured layer, never delivered to the page",
        "rights_basis": "Copernicus Sentinel data 2025, free full and open access; attribution: Contains modified Copernicus Sentinel data [2025]",
        "acquisition_date": args.date,
        "utm_zone": args.zone,
        "mosaic_grid": {"ulx": ulx, "uly": uly, "pixel_m": 30.0, "cols": cols, "rows": rows},
        "projection_check": {"lat": args.verify_lat, "lon": args.verify_lon, "easting": round(float(ex[0]), 2),
                             "northing": round(float(ny[0]), 2), "error_m": round(error_m, 3)},
        "window_deg": {"lon0": lon0, "lon1": lon1, "lat0": lat0, "lat1": lat1},
        "texels_per_degree": {"lon": round(out_w / (lon1 - lon0), 3), "lat": round(out_h / (lat1 - lat0), 3)},
        "metres_per_texel": 30.0,
        "ratio_encoding": "value * " + str(RATIO_ENCODE),
        "sources": sources,
        "output": hc.relpath(out_path).replace("\\", "/"),
        "output_dimensions": [out_w, out_h],
        "output_bytes": out_path.stat().st_size,
        "output_sha256": hc.sha256_file(out_path),
        "round_trip_max_error": round_trip,
        "blender_version": bpy.app.version_string,
    }
    record_path = hc.REPO_ROOT / args.record
    hc.ensure_dir(record_path.parent)
    record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in record.items() if k != "sources"}, indent=2))
    print("[hero] detail multiplier -> " + hc.relpath(out_path))


if __name__ == "__main__":
    main()
