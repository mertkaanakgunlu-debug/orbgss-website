"""Reproducible source-texel coverage of the Earth albedo at the hero's softest approved hold.

    py -3.14 hero/scripts/texel_coverage.py --scene hero_production_kizildere --out hero/evidence/texel_coverage.json

A-HERO-11 asks for a reproducible estimate of how many source texels the camera actually sees
across the frame at the regional hold, before and after the Earth-source change, so that "the
ground is sharper" is a measured statement rather than an impression.

The estimate is geometric and Blender-free: ``shot_plan.analyze`` gives the ground width the frame
spans at the AOI on the last camera keyframe (and metres per render pixel); each texture's texel
size at the AOI latitude follows from its equirectangular dimensions (east-west texels shrink with
cos(latitude); a tile crop keeps its tile's density). Magnification is metres-per-texel divided by
metres-per-delivered-pixel: above 1 each source texel is stretched across more than one screen
pixel (the texture is upscaled), below 1 the frame sees more source texels than it has pixels.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import aoi_system as ax  # noqa: E402
import hero_common as hc  # noqa: E402
import shot_plan as sp  # noqa: E402

EQUATOR_KM_PER_DEG = 111.32


def texel_metres(width_px: int, degrees_of_lon: float, lat_deg: float):
    """(east-west, north-south) metres per texel for an equirectangular texture."""
    per_deg = width_px / degrees_of_lon
    ns = EQUATOR_KM_PER_DEG * 1000.0 / per_deg
    ew = ns * math.cos(math.radians(lat_deg))
    return ew, ns


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", default="hero_production_kizildere")
    parser.add_argument("--delivered-width", type=int, default=1920)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    scene_config = hc.load_scene_config()
    render_config = hc.load_render_config()
    manifest = hc.load_asset_manifest()
    report = sp.analyze(scene_config, args.scene, render_config)
    hold = report["keyframes"][-1]
    scene_spec = hc.resolve_scene_spec(args.scene, scene_config["scenes"])
    aoi_spec = sp._aoi_spec(scene_spec)
    fixture = ax.resolve_fixture(scene_config, aoi_spec.get("fixture"))
    lat = float(fixture["center_lat_deg"])

    frame_width_km = float(hold["frame_width_at_aoi_km"])
    render_width = int(report["resolution"][0])
    metres_per_delivered_px = frame_width_km * 1000.0 / args.delivered_width
    metres_per_render_px = frame_width_km * 1000.0 / render_width

    assets = {a["id"]: a for a in manifest.get("assets", [])}
    earth = scene_spec.get("materials", {}).get("earth_surface", {})
    rows = []

    def add(label, asset_id, width_px, degrees, role):
        ew, ns = texel_metres(width_px, degrees, lat)
        rows.append({
            "label": label,
            "asset": asset_id,
            "role": role,
            "dimensions": assets.get(asset_id, {}).get("dimensions"),
            "metres_per_texel_east_west_at_aoi": round(ew, 1),
            "metres_per_texel_north_south": round(ns, 1),
            "source_texels_across_frame_width": round(frame_width_km * 1000.0 / ew, 0),
            "magnification_at_delivered_width": round(ew / metres_per_delivered_px, 3),
            "magnification_at_render_width": round(ew / metres_per_render_px, 3),
            "upscaled_on_screen": ew / metres_per_delivered_px > 1.0,
        })

    # Rejected checkpoint: the 8192 x 4096 composite (360 degrees of longitude).
    add("rejected checkpoint ffa2f29 (land_ocean_ice_cloud_8192)", "earth_day_composite_8k", 8192, 360.0,
        "global albedo, whole frame")
    # R2 global basemap and regional detail window.
    add("R2 global (BMNG 21600 x 10800)", "earth_bmng_global_2km", 21600, 360.0,
        "global albedo outside the detail window")
    crop = assets.get("earth_bmng_detail_crop", {})
    window = crop.get("window", {})
    if crop.get("dimensions") and window:
        add("R2 regional detail window (BMNG C1 crop)", "earth_bmng_detail_crop",
            int(crop["dimensions"][0]), float(window["lon1"]) - float(window["lon0"]),
            "albedo under the target: lon %s-%s E, lat %s-%s N" % (
                window["lon0"], window["lon1"], window["lat0"], window["lat1"]))

    before = rows[0]["magnification_at_delivered_width"]
    after = rows[-1]["magnification_at_delivered_width"]
    record = {
        "task": "WEB-005A R2 / MER-107 — A-HERO-11 source-resolution evidence",
        "scene": args.scene,
        "hold_keyframe": hold["frame"],
        "aoi_latitude_deg": lat,
        "frame_width_at_aoi_km": round(frame_width_km, 1),
        "camera_altitude_km": hold["camera_altitude_km"],
        "aoi_slant_range_km": hold["aoi_slant_range_km"],
        "render_width_px": render_width,
        "delivered_width_px": args.delivered_width,
        "metres_per_delivered_pixel": round(metres_per_delivered_px, 1),
        "metres_per_render_pixel": round(metres_per_render_px, 1),
        "textures": rows,
        "improvement": {
            "before_magnification": before,
            "after_magnification_under_target": after,
            "linear_texel_density_gain": round(before / after, 2) if after else None,
            "note": ("Magnification above 1.0 means the albedo is upscaled on screen. The rejected "
                     "checkpoint upscaled its source about %.1fx at the delivered width; under the "
                     "target the R2 detail window is sampled at %.2fx, i.e. the frame now sees more "
                     "source texels than delivered pixels." % (before, after)),
        },
        "method": ("Frame width at the AOI from shot_plan.analyze on the last camera keyframe; texel "
                   "size from each texture's equirectangular dimensions with the east-west size "
                   "scaled by cos(latitude); magnification = metres per texel / metres per delivered "
                   "pixel. The active texture under the target is the detail window wherever the "
                   "frame lies inside it, which it does at the hold by construction."),
    }
    print(json.dumps(record, indent=2))
    if args.out:
        out = Path(args.out)
        hc.ensure_dir(out.parent)
        out.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        print("[hero] texel coverage -> " + hc.relpath(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
