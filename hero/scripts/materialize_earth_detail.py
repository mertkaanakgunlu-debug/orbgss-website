"""Cut the regional detail window out of a Blue Marble Next Generation 500 m tile, inside Blender.

    blender -b -P hero/scripts/materialize_earth_detail.py -- --window 12 46 26 50

WEB-005A R2 replaces the cinematic Earth albedo with the NASA Blue Marble Next Generation global
composite (21600 x 10800, about 2 km per texel) and, inside a configured longitude/latitude window
around the Kizildere regional frame, with a crop of the full-resolution 500 m tile that covers it.
The crop is what the regional hold actually looks at, so it is the asset that fixes the softness
the rejected checkpoint measured -- and it is a plain sub-rectangle of the NASA tile: no resampling,
no colour change, no re-projection. Provenance is the tile's own record plus the window recorded here.

Why Blender rather than an image library: the workstation deliberately has no Pillow/numpy in its
CPython, and this lane already treats Blender as the one production tool. Blender's bundled numpy
does the slicing; the 21600 x 21600 tile is read into memory once, sliced, and the crop written as
PNG so nothing is re-encoded lossily on the way to the renderer.

The tile's geography is fixed by its name: tile C1 covers longitude 0..90 E and latitude 90 N..0
at exactly 240 texels per degree, so a window in degrees converts to texel offsets without any
guesswork, and the writer records the exact texel rectangle it cut.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bpy  # noqa: E402
import numpy as np  # noqa: E402  (Blender's bundled numpy)

import hero_common as hc  # noqa: E402

TILE_DEG = 90.0
TILE_PX = 21600
TEXELS_PER_DEG = TILE_PX / TILE_DEG  # 240

# Longitude/latitude origin of each BMNG 21600 x 21600 tile (west edge, north edge).
TILE_ORIGINS = {
    "A1": (-180.0, 90.0), "B1": (-90.0, 90.0), "C1": (0.0, 90.0), "D1": (90.0, 90.0),
    "A2": (-180.0, 0.0), "B2": (-90.0, 0.0), "C2": (0.0, 0.0), "D2": (90.0, 0.0),
}


def texel_window(tile: str, lon0: float, lon1: float, lat0: float, lat1: float):
    west, north = TILE_ORIGINS[tile]
    x0 = int(round((lon0 - west) * TEXELS_PER_DEG))
    x1 = int(round((lon1 - west) * TEXELS_PER_DEG))
    y0 = int(round((north - lat1) * TEXELS_PER_DEG))  # image rows run north -> south
    y1 = int(round((north - lat0) * TEXELS_PER_DEG))
    if not (0 <= x0 < x1 <= TILE_PX and 0 <= y0 < y1 <= TILE_PX):
        raise SystemExit("window " + repr((lon0, lon1, lat0, lat1)) + " does not lie inside tile " + tile)
    return x0, x1, y0, y1


def main() -> None:
    parser = argparse.ArgumentParser(description="Crop the Earth detail window from a BMNG tile.")
    parser.add_argument("--tile", default="C1")
    parser.add_argument("--source", default="world.topo.bathy.200407.3x21600x21600.C1.jpg")
    parser.add_argument("--window", nargs=4, type=float, metavar=("LON0", "LON1", "LAT0", "LAT1"),
                        default=[12.0, 46.0, 26.0, 50.0])
    parser.add_argument("--out", default="world.topo.bathy.200407.C1.crop.png")
    parser.add_argument("--record", default="hero/evidence/earth_detail_crop.json")
    args = parser.parse_args(hc.argv_after_double_dash())

    source = hc.SOURCE_DIR / args.source
    if not source.is_file():
        raise SystemExit("source tile not materialized: " + hc.relpath(source))

    lon0, lon1, lat0, lat1 = args.window
    x0, x1, y0, y1 = texel_window(args.tile, lon0, lon1, lat0, lat1)
    width, height = x1 - x0, y1 - y0
    print("[hero] window lon " + str(lon0) + ".." + str(lon1) + " lat " + str(lat0) + ".." + str(lat1)
          + " -> texels x " + str(x0) + ".." + str(x1) + " y " + str(y0) + ".." + str(y1)
          + " (" + str(width) + " x " + str(height) + ")", flush=True)

    image = bpy.data.images.load(str(source))
    if tuple(image.size) != (TILE_PX, TILE_PX):
        raise SystemExit("tile is " + str(tuple(image.size)) + ", expected " + str((TILE_PX, TILE_PX)))
    image.colorspace_settings.name = "sRGB"

    # Blender exposes pixels bottom-up, RGBA float. Read once, slice, release.
    buffer = np.empty(TILE_PX * TILE_PX * 4, dtype=np.float32)
    image.pixels.foreach_get(buffer)
    tile = buffer.reshape(TILE_PX, TILE_PX, 4)
    # Row 0 in Blender is the BOTTOM of the image, so the north edge (row y0 in image terms)
    # is row TILE_PX - y0 - 1 in the buffer.
    rows_lo = TILE_PX - y1
    rows_hi = TILE_PX - y0
    crop = np.ascontiguousarray(tile[rows_lo:rows_hi, x0:x1, :])
    del tile
    del buffer
    bpy.data.images.remove(image)

    out_image = bpy.data.images.new("earth_detail_crop", width=width, height=height, alpha=False)
    out_image.colorspace_settings.name = "sRGB"
    out_image.pixels.foreach_set(crop.reshape(-1))
    out_path = hc.SOURCE_DIR / args.out
    out_image.filepath_raw = str(out_path)
    out_image.file_format = "PNG"
    out_image.save()

    record = {
        "task": "WEB-005A R2 / MER-107",
        "derived_from": hc.relpath(source).replace("\\", "/"),
        "source_sha256": hc.sha256_file(source),
        "tile": args.tile,
        "tile_origin_lon_lat": list(TILE_ORIGINS[args.tile]),
        "texels_per_degree": TEXELS_PER_DEG,
        "window_deg": {"lon0": lon0, "lon1": lon1, "lat0": lat0, "lat1": lat1},
        "texel_rectangle": {"x0": x0, "x1": x1, "y0": y0, "y1": y1},
        "crop_size": [width, height],
        "metres_per_texel_at_equator": 1000.0 * 111.32 / TEXELS_PER_DEG,
        "operation": "axis-aligned sub-rectangle copy; no resampling, no colour change, PNG (lossless) output",
        "output": hc.relpath(out_path).replace("\\", "/"),
        "output_sha256": hc.sha256_file(out_path),
        "output_bytes": out_path.stat().st_size,
        "blender_version": bpy.app.version_string,
    }
    record_path = hc.REPO_ROOT / args.record
    hc.ensure_dir(record_path.parent)
    record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))
    print("[hero] crop -> " + hc.relpath(out_path))


if __name__ == "__main__":
    main()
