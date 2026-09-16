"""Measure the evaluated hero camera, frame by frame, inside Blender.

    blender -b -P hero/scripts/audit_shot.py -- --scene hero_predata_animatic

``shot_plan.py`` reasons about camera *keyframes* as geometry. This script
measures what Blender actually evaluates on every frame in between -- after
F-curve interpolation, the Earth's rotation, the satellite animation and the
camera's AOI track constraint -- and turns the WEB-HERO-001D cinematography
contract into numbers.

The contract asks for things a still cannot show and an opinion should not
settle:

* the AOI must not drift, jump scale or change orientation between acquisition
  and the regional hold;
* the move must be continuous, with no hidden cut;
* camera motion must be controlled, with no sudden acceleration or focal-length
  snap;
* the opening must keep the headline-safe region clear of the planet.

Each of those becomes a measured series with an explicit threshold here.
Subjective questions -- is the palette right, does it feel premium -- are
deliberately left to the rendered stills and the animatic.

Thresholds are stated as fractions of the frame or as per-frame rates relative
to the move's own scale, not as absolute world units, because what a reviewer
sees is screen-space behaviour.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

import aoi_system as ax  # noqa: E402
import build_scene  # noqa: E402
import hero_common as hc  # noqa: E402
import shot_plan as sp  # noqa: E402

# The AOI is locked to frame centre from the handover frame on; anything beyond
# this fraction of the frame is a registration drift a viewer would see.
AOI_CENTRE_TOLERANCE = 0.02
# Apparent AOI size may grow as the camera closes but must never reverse by
# more than measurement noise: a shrink is a scale discontinuity.
AOI_SCALE_REVERSAL_TOLERANCE = 0.0015
# Screen-space rotation of the footprint between adjacent frames. A continuous
# approach rolls the footprint slowly; a cut or a re-registration snaps it.
AOI_ORIENTATION_STEP_DEG = 2.0
# Camera speed may change smoothly; a spike is a jerk. Expressed as the ratio
# of the largest single-frame speed change to the mean speed.
CAMERA_JERK_RATIO = 0.35
# Focal length may ramp but must not snap, in millimetres per frame.
LENS_RATE_MM_PER_FRAME = 0.6
# A cut would show up as a camera displacement far outside the run of the move.
CAMERA_CUT_RATIO = 4.0


def _basis(matrix):
    """Right, up, forward for a Blender camera: local -Z looks forward."""
    right = matrix.to_3x3() @ Vector((1.0, 0.0, 0.0))
    up = matrix.to_3x3() @ Vector((0.0, 1.0, 0.0))
    forward = matrix.to_3x3() @ Vector((0.0, 0.0, -1.0))
    return right.normalized(), up.normalized(), forward.normalized()


def _project(point, matrix, lens_mm, sensor_mm, resolution):
    right, up, forward = _basis(matrix)
    offset = Vector(point) - matrix.translation
    depth = offset.dot(forward)
    if depth <= 1e-9:
        return None
    fov_x, fov_y = sp.field_of_view(lens_mm, sensor_mm, resolution)
    x = 0.5 + 0.5 * (offset.dot(right) / depth) / math.tan(fov_x / 2.0)
    y = 0.5 + 0.5 * (offset.dot(up) / depth) / math.tan(fov_y / 2.0)
    return (x, y)


def _in_frame(screen):
    return screen is not None and 0.0 <= screen[0] <= 1.0 and 0.0 <= screen[1] <= 1.0


def _series_check(ok: bool, label: str, measured, threshold, unit: str) -> dict:
    return {
        "check": label,
        "passed": bool(ok),
        "measured": measured,
        "threshold": threshold,
        "unit": unit,
    }


def audit(scene_id: str, fixture_id, frames) -> dict:
    spec = build_scene.build(scene_id, frame=None, aoi_fixture=fixture_id)
    scene_config = hc.load_scene_config()
    render_config = hc.load_render_config()

    profile = render_config["profiles"][render_config.get("default_still_profile", "master")]
    resolution = (int(profile["resolution_x"]), int(profile["resolution_y"]))
    sensor_mm = float(scene_config.get("camera_defaults", {}).get("sensor_width_mm", 36.0))

    aoi_spec = sp._aoi_spec(spec)
    description = ax.describe(scene_config, fixture_id or aoi_spec.get("fixture"), spec)
    corner_ids = list(description["corner_order"])
    prefix = aoi_spec["id"]

    camera = bpy.context.scene.camera
    earth = bpy.data.objects.get("earth")
    satellite = bpy.data.objects.get(
        aoi_spec.get("beams", {}).get("source_object_id", "satellite")
    )
    centre_target = bpy.data.objects.get(prefix + "_target_center")
    corner_targets = [bpy.data.objects.get(prefix + "_target_" + cid) for cid in corner_ids]
    if centre_target is None or any(t is None for t in corner_targets):
        raise SystemExit("scene " + repr(scene_id) + " did not build the AOI target empties")

    camera_composition = spec.get("camera", {}).get("composition", {})
    headline_region = camera_composition.get("headline_safe_region")
    headline_through = camera_composition.get("headline_safe_through_frame")
    track = spec.get("camera", {}).get("track", {})
    # The handover is the *first* frame at which the lock is fully engaged;
    # everything from there on is what the registration checks are about.
    handover_frame = min(
        (int(k["frame"]) for k in track.get("influence_keyframes", []) if float(k["value"]) >= 1.0),
        default=None,
    )

    earth_radius_bu = description["earth_radius_bu"]
    per_frame = []
    for frame in frames:
        bpy.context.scene.frame_set(int(frame))
        depsgraph = bpy.context.evaluated_depsgraph_get()
        evaluated_camera = camera.evaluated_get(depsgraph)
        matrix = evaluated_camera.matrix_world.copy()
        lens = float(evaluated_camera.data.lens)
        location = matrix.translation.copy()

        centre_world = centre_target.evaluated_get(depsgraph).matrix_world.translation.copy()
        corner_world = [
            t.evaluated_get(depsgraph).matrix_world.translation.copy() for t in corner_targets
        ]

        centre_screen = _project(centre_world, matrix, lens, sensor_mm, resolution)
        corner_screen = [
            _project(position, matrix, lens, sensor_mm, resolution) for position in corner_world
        ]

        # Apparent footprint size and orientation, straight off the projected
        # corners: the two things a scale or registration discontinuity moves.
        extent = None
        orientation = None
        if all(point is not None for point in corner_screen):
            xs = [point[0] for point in corner_screen]
            ys = [point[1] for point in corner_screen]
            extent = max(max(xs) - min(xs), max(ys) - min(ys))
            first, second = corner_screen[0], corner_screen[1]
            orientation = math.degrees(
                math.atan2(second[1] - first[1], second[0] - first[0])
            )

        satellite_world = satellite.evaluated_get(depsgraph).matrix_world.translation.copy()
        satellite_screen = _project(satellite_world, matrix, lens, sensor_mm, resolution)

        entry = {
            "frame": int(frame),
            "camera_location": [round(v, 5) for v in location],
            "camera_radius_bu": round(location.length, 5),
            "camera_altitude_km": round(
                (location.length - earth_radius_bu) * ax.KM_PER_BLENDER_UNIT, 2
            ),
            "focal_length_mm": round(lens, 4),
            "earth_rotation_z_deg": round(math.degrees(earth.rotation_euler.z), 5) if earth else None,
            "aoi_slant_range_km": round(
                (centre_world - location).length * ax.KM_PER_BLENDER_UNIT, 2
            ),
            "aoi_screen_x": round(centre_screen[0], 5) if centre_screen else None,
            "aoi_screen_y": round(centre_screen[1], 5) if centre_screen else None,
            "aoi_screen_extent": round(extent, 6) if extent is not None else None,
            "aoi_screen_orientation_deg": round(orientation, 4) if orientation is not None else None,
            "aoi_in_frame": _in_frame(centre_screen),
            "satellite_screen_x": round(satellite_screen[0], 5) if satellite_screen else None,
            "satellite_screen_y": round(satellite_screen[1], 5) if satellite_screen else None,
            "satellite_in_frame": _in_frame(satellite_screen),
        }

        if headline_region and (headline_through is None or frame <= int(headline_through)):
            look_at = location + _basis(matrix)[2]
            entry["headline_safe"] = sp._headline_safe_metrics(
                tuple(location), tuple(look_at), lens, earth_radius_bu,
                sensor_mm, resolution, headline_region,
            )
        per_frame.append(entry)

    # ---- derived motion series -------------------------------------------
    positions = [Vector(e["camera_location"]) for e in per_frame]
    speeds = [(positions[i + 1] - positions[i]).length for i in range(len(positions) - 1)]
    for index, entry in enumerate(per_frame):
        entry["camera_speed_bu_per_frame"] = round(speeds[index], 6) if index < len(speeds) else None
    mean_speed = sum(speeds) / len(speeds) if speeds else 0.0
    speed_steps = [abs(speeds[i + 1] - speeds[i]) for i in range(len(speeds) - 1)]
    max_speed_step = max(speed_steps) if speed_steps else 0.0
    max_speed = max(speeds) if speeds else 0.0

    lens_steps = [
        abs(per_frame[i + 1]["focal_length_mm"] - per_frame[i]["focal_length_mm"])
        for i in range(len(per_frame) - 1)
    ]
    max_lens_step = max(lens_steps) if lens_steps else 0.0

    locked = [e for e in per_frame if handover_frame is None or e["frame"] >= handover_frame]
    centre_error = max(
        (
            math.hypot(e["aoi_screen_x"] - 0.5, e["aoi_screen_y"] - 0.5)
            for e in locked
            if e["aoi_screen_x"] is not None
        ),
        default=0.0,
    )

    extents = [e["aoi_screen_extent"] for e in locked if e["aoi_screen_extent"] is not None]
    worst_shrink = max(
        (a - b for a, b in zip(extents, extents[1:])), default=0.0
    )

    orientations = [
        e["aoi_screen_orientation_deg"] for e in locked if e["aoi_screen_orientation_deg"] is not None
    ]
    orientation_steps = [
        abs((b - a + 180.0) % 360.0 - 180.0) for a, b in zip(orientations, orientations[1:])
    ]
    max_orientation_step = max(orientation_steps) if orientation_steps else 0.0

    headline_entries = [e for e in per_frame if "headline_safe" in e]
    headline_clear = all(e["headline_safe"]["clear"] for e in headline_entries)
    headline_worst = max(
        (e["headline_safe"]["occupancy"] for e in headline_entries), default=0.0
    )

    checks = [
        _series_check(
            centre_error <= AOI_CENTRE_TOLERANCE,
            "aoi stays locked to frame centre after handover",
            round(centre_error, 6), AOI_CENTRE_TOLERANCE, "fraction of frame",
        ),
        _series_check(
            worst_shrink <= AOI_SCALE_REVERSAL_TOLERANCE,
            "aoi apparent size never reverses",
            round(worst_shrink, 6), AOI_SCALE_REVERSAL_TOLERANCE, "fraction of frame per frame",
        ),
        _series_check(
            max_orientation_step <= AOI_ORIENTATION_STEP_DEG,
            "aoi screen orientation changes continuously",
            round(max_orientation_step, 5), AOI_ORIENTATION_STEP_DEG, "degrees per frame",
        ),
        _series_check(
            mean_speed > 0 and (max_speed_step / mean_speed) <= CAMERA_JERK_RATIO,
            "camera speed changes without a jerk",
            round(max_speed_step / mean_speed, 5) if mean_speed else None,
            CAMERA_JERK_RATIO, "max speed step / mean speed",
        ),
        _series_check(
            max_lens_step <= LENS_RATE_MM_PER_FRAME,
            "focal length ramps without a snap",
            round(max_lens_step, 5), LENS_RATE_MM_PER_FRAME, "mm per frame",
        ),
        _series_check(
            mean_speed > 0 and (max_speed / mean_speed) <= CAMERA_CUT_RATIO,
            "no hidden cut in the camera path",
            round(max_speed / mean_speed, 5) if mean_speed else None,
            CAMERA_CUT_RATIO, "max step / mean step",
        ),
        _series_check(
            all(e["aoi_in_frame"] for e in locked),
            "aoi stays in frame from handover to the end",
            sum(1 for e in locked if not e["aoi_in_frame"]), 0, "frames out of frame",
        ),
        _series_check(
            headline_clear,
            "headline-safe region stays clear of the Earth through the establish",
            round(headline_worst, 6), 0.0, "occupancy fraction",
        ),
    ]

    satellite_frames = [e["frame"] for e in per_frame if e["satellite_in_frame"]]
    return {
        "scene": scene_id,
        "fixture": description["fixture_id"],
        "resolution": list(resolution),
        "frame_range": [per_frame[0]["frame"], per_frame[-1]["frame"]],
        "frames_audited": len(per_frame),
        "handover_frame": handover_frame,
        "summary": {
            "camera_radius_bu": [per_frame[0]["camera_radius_bu"], per_frame[-1]["camera_radius_bu"]],
            "camera_altitude_km": [
                per_frame[0]["camera_altitude_km"], per_frame[-1]["camera_altitude_km"],
            ],
            "focal_length_mm": [per_frame[0]["focal_length_mm"], per_frame[-1]["focal_length_mm"]],
            "aoi_slant_range_km": [
                per_frame[0]["aoi_slant_range_km"], per_frame[-1]["aoi_slant_range_km"],
            ],
            "aoi_screen_extent": [extents[0], extents[-1]] if extents else None,
            "mean_camera_speed_bu_per_frame": round(mean_speed, 6),
            "satellite_in_frame_from": min(satellite_frames) if satellite_frames else None,
            "satellite_in_frame_until": max(satellite_frames) if satellite_frames else None,
            "headline_safe_worst_occupancy": round(headline_worst, 6),
        },
        "thresholds": {
            "aoi_centre_tolerance": AOI_CENTRE_TOLERANCE,
            "aoi_scale_reversal_tolerance": AOI_SCALE_REVERSAL_TOLERANCE,
            "aoi_orientation_step_deg": AOI_ORIENTATION_STEP_DEG,
            "camera_jerk_ratio": CAMERA_JERK_RATIO,
            "lens_rate_mm_per_frame": LENS_RATE_MM_PER_FRAME,
            "camera_cut_ratio": CAMERA_CUT_RATIO,
        },
        "checks": checks,
        "passed": all(check["passed"] for check in checks),
        "frames": per_frame,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit the evaluated hero camera per frame.")
    parser.add_argument("--scene", default="hero_predata_animatic")
    parser.add_argument("--aoi-fixture", default=None)
    parser.add_argument("--frame-start", type=int, default=None)
    parser.add_argument("--frame-end", type=int, default=None)
    parser.add_argument("--step", type=int, default=1)
    parser.add_argument("--out", default=None)
    parser.add_argument(
        "--full-frames",
        action="store_true",
        help="include the per-frame series in the written record (large)",
    )
    args = parser.parse_args(hc.argv_after_double_dash())

    scene_config = hc.load_scene_config()
    spec = hc.resolve_scene_spec(args.scene, scene_config["scenes"])
    animation = spec.get("animation", {})
    start = args.frame_start if args.frame_start is not None else int(animation.get("frame_start", 1))
    end = args.frame_end if args.frame_end is not None else int(animation.get("frame_end", start))

    record = audit(args.scene, args.aoi_fixture, range(start, end + 1, max(1, args.step)))

    printable = dict(record)
    if not args.full_frames:
        printable["frames"] = "omitted; pass --full-frames to include"
    print(json.dumps(printable, indent=2))

    if args.out:
        out = Path(args.out)
        hc.ensure_dir(out.parent)
        written = dict(record)
        if not args.full_frames:
            # Keep a bounded, reviewable sample rather than 240 dense entries.
            written["frames"] = [e for e in record["frames"] if e["frame"] % 8 == 0 or e["frame"] == 1]
            written["frames_note"] = (
                "every eighth frame plus frame 1; all checks above were computed over the full "
                "per-frame series, not this sample"
            )
        out.write_text(json.dumps(written, indent=2) + "\n", encoding="utf-8")
        print("[hero] shot audit -> " + hc.relpath(out))

    print("[hero] shot audit " + ("PASSED" if record["passed"] else "FAILED"))
    for check in record["checks"]:
        if not check["passed"]:
            print(
                "  FAIL  " + check["check"] + ": measured " + str(check["measured"])
                + " vs threshold " + str(check["threshold"]) + " " + check["unit"]
            )
    if not record["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
