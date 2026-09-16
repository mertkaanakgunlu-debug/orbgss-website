"""Derive and measure the satellite's orbital pass against the AOI and the camera.

    py -3.14 hero/scripts/orbit_plan.py --scene hero_production_kizildere --analyze
    py -3.14 hero/scripts/orbit_plan.py --scene hero_production_kizildere --derive

WEB-005A turned the satellite's eight hand-typed waypoints into one circular orbit. WEB-005A R2
goes one step further and makes that orbit *derived*, the way the camera already is: the scene
states the pass in the terms the pass is actually about -- "at frame 146 be directly over
24 N 14 E at 705 km, heading 040, moving 0.95 degrees of arc per frame" -- and this module
converts that into the world keyframes that go into ``scene.json``. The validator re-derives them
and fails if the committed keys have drifted from their intent, exactly as it does for the camera.

Why derive rather than type: the pass has to satisfy several things at once that no single still
can show. It must be hidden behind the planet at the open and emerge around the limb, it must sit
lower-left of the target with the Earth right-dominant through the acquisition beat, it must never
clip the frame while the sensing lines are live, and it must never swing so close to the camera
that a hero-scale model fills the foreground -- the failure the rejected checkpoint's predecessor
actually had. ``analyze`` measures every one of those per frame from configuration alone.

Blender-independent on purpose: the camera between keys is interpolated linearly here, which is an
approximation of Blender's Bezier F-curves. It is good enough to *plan* a pass; the published
numbers come from ``audit_shot.py``, which measures the evaluated scene.
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

WORLD_UP = (0.0, 0.0, 1.0)


# ---------------------------------------------------------------------------
# Orbit geometry
# ---------------------------------------------------------------------------

def _object_spec(scene_spec: dict, object_id: str):
    for spec in scene_spec.get("objects", []):
        if spec.get("id") == object_id:
            return spec
    return None


def orbit_basis(scene_config: dict, scene_spec: dict, intent: dict):
    """Unit vectors (u, v) spanning the orbit plane, plus the orbit radius in BU.

    ``u`` points at the sub-satellite anchor at the anchor frame (Earth rotation at that frame
    included, so "over this point at this frame" is literally true), and ``v`` is the unit
    tangent at that point along the requested heading. The orbit is then
    ``r * (cos(theta) u + sin(theta) v)``.
    """
    lon_offset = ax.longitude_offset_deg(scene_config, scene_spec)
    anchor_frame = int(intent["anchor_frame"])
    rotation = sp.earth_rotation_deg(scene_spec, anchor_frame)

    anchor = ax.geographic_to_unit(
        float(intent["anchor_lat_deg"]), float(intent["anchor_lon_deg"]), lon_offset
    )
    anchor = sp._rotate_z(anchor, rotation)

    north = sp._sub(WORLD_UP, ax.scale(anchor, sp._dot(WORLD_UP, anchor)))
    north = ax.normalize(north) if ax.length(north) > 1e-9 else (1.0, 0.0, 0.0)
    east = ax.normalize(sp._cross(north, anchor))
    heading = math.radians(float(intent.get("heading_deg", 0.0)))
    tangent = ax.normalize(
        sp._add(ax.scale(north, math.cos(heading)), ax.scale(east, math.sin(heading)))
    )

    radius_bu = (ax.earth_radius_km(scene_config) + float(intent["altitude_km"])) / ax.KM_PER_BLENDER_UNIT
    return anchor, tangent, radius_bu


def orbit_position(basis, intent: dict, frame: float):
    u, v, radius_bu = basis
    theta = math.radians(
        float(intent.get("rate_deg_per_frame", 1.0)) * (float(frame) - float(intent["anchor_frame"]))
    )
    return ax.scale(
        sp._add(ax.scale(u, math.cos(theta)), ax.scale(v, math.sin(theta))), radius_bu
    )


def orbit_angle_deg(intent: dict, frame: float) -> float:
    return float(intent.get("rate_deg_per_frame", 1.0)) * (float(frame) - float(intent["anchor_frame"]))


def derive(scene_config: dict, scene_id: str, object_id: str = "satellite"):
    scenes = scene_config.get("scenes", {})
    scene_spec = hc.resolve_scene_spec(scene_id, scenes)
    spec = _object_spec(scene_spec, object_id) or {}
    intent = spec.get("orbit_intent")
    if not intent:
        raise SystemExit(
            "object " + repr(object_id) + " in scene " + repr(scene_id)
            + " declares no orbit_intent to derive from"
        )
    basis = orbit_basis(scene_config, scene_spec, intent)
    frames = sorted({int(f) for f in intent["keyframe_frames"]})
    return [
        {"frame": frame, "location": [round(c, 4) for c in orbit_position(basis, intent, frame)]}
        for frame in frames
    ]


# ---------------------------------------------------------------------------
# Camera interpolation (planning approximation of Blender's F-curves)
# ---------------------------------------------------------------------------

def _lerp(a, b, t):
    return a + (b - a) * t


def camera_state(camera_spec: dict, frame: float):
    """Location, look_at, focal length and shift at ``frame`` by linear interpolation."""
    keys = sorted(camera_spec.get("keyframes", []), key=lambda k: int(k["frame"]))
    shifts = sorted(camera_spec.get("shift_keyframes", []), key=lambda k: int(k["frame"]))

    def interp(track, extract):
        if not track:
            return None
        if frame <= int(track[0]["frame"]):
            return extract(track[0])
        if frame >= int(track[-1]["frame"]):
            return extract(track[-1])
        for k0, k1 in zip(track, track[1:]):
            f0, f1 = int(k0["frame"]), int(k1["frame"])
            if f0 <= frame <= f1:
                t = (frame - f0) / float(f1 - f0) if f1 > f0 else 0.0
                a, b = extract(k0), extract(k1)
                if isinstance(a, (list, tuple)):
                    return [_lerp(float(x), float(y), t) for x, y in zip(a, b)]
                return _lerp(float(a), float(b), t)
        return extract(track[-1])

    location = interp(keys, lambda k: list(k["location"]))
    look_at = interp(keys, lambda k: list(k["look_at"]))
    lens = interp(keys, lambda k: float(k["focal_length_mm"]))
    shift = interp(shifts, lambda k: [float(k.get("shift_x", 0.0)), float(k.get("shift_y", 0.0))]) or [0.0, 0.0]
    return location, look_at, lens, shift


# ---------------------------------------------------------------------------
# Visibility helpers
# ---------------------------------------------------------------------------

def occluded_by_earth(camera, point, radius_bu) -> bool:
    """True when the segment camera -> point crosses the Earth sphere before reaching point."""
    direction = sp._sub(point, camera)
    distance = ax.length(direction)
    if distance < 1e-9:
        return False
    direction = ax.scale(direction, 1.0 / distance)
    b = 2.0 * sp._dot(camera, direction)
    c = sp._dot(camera, camera) - radius_bu * radius_bu
    disc = b * b - 4.0 * c
    if disc < 0.0:
        return False
    root = math.sqrt(disc)
    t_near = (-b - root) / 2.0
    return 0.0 < t_near < distance


def earth_screen_extent(camera, look_at, lens, sensor, resolution, shift, radius_bu, samples=720):
    """Bounding box of the visible planet in frame coordinates, from its projected silhouette.

    The silhouette of a sphere seen from outside is the circle of points whose radius vector is
    perpendicular to the view ray; sampling that circle and projecting each point gives the exact
    on-screen disc bounds without rendering anything.
    """
    camera_radius = ax.length(camera)
    if camera_radius <= radius_bu:
        return None
    to_centre = ax.normalize(ax.scale(camera, -1.0))
    # Silhouette circle: the horizon points P satisfy P . C = R^2 (the view ray is tangent), so
    # seen from the planet's centre they sit at angle alpha from the camera direction with
    # cos(alpha) = R / |C| -- offset R cos(alpha) toward the camera, ring radius R sin(alpha).
    cos_a = radius_bu / camera_radius
    sin_a = math.sqrt(max(0.0, 1.0 - cos_a * cos_a))
    axis = ax.scale(to_centre, -1.0)  # from centre toward camera
    helper = (0.0, 0.0, 1.0) if abs(axis[2]) < 0.9 else (1.0, 0.0, 0.0)
    e1 = ax.normalize(sp._cross(axis, helper))
    e2 = ax.normalize(sp._cross(axis, e1))
    xs, ys = [], []
    for index in range(samples):
        phi = 2.0 * math.pi * index / samples
        ring = sp._add(ax.scale(e1, math.cos(phi)), ax.scale(e2, math.sin(phi)))
        point = ax.scale(sp._add(ax.scale(axis, cos_a), ax.scale(ring, sin_a)), radius_bu)
        screen = project_shifted(point, camera, look_at, lens, sensor, resolution, shift)
        if screen["behind_camera"]:
            continue
        xs.append(screen["x"])
        ys.append(screen["y"])
    if not xs:
        return None
    return {"x0": round(min(xs), 4), "x1": round(max(xs), 4), "y0": round(min(ys), 4), "y1": round(max(ys), 4)}


def project_shifted(point, camera, look_at, lens, sensor, resolution, shift):
    """``shot_plan.project`` with Blender's lens shift applied.

    Measured convention (Blender 4.5, AUTO sensor fit, landscape frame): a shift of +s along x
    moves the optical axis to frame x = 0.5 - s, and a shift of +s along y moves it to
    y = 0.5 - s * (width / height), because shift is expressed in units of the larger sensor
    dimension.
    """
    screen = sp.project(point, camera, look_at, lens, sensor, resolution)
    if screen["x"] is None:
        return screen
    width, height = resolution
    x = screen["x"] - float(shift[0])
    y = screen["y"] - float(shift[1]) * (width / float(height))
    screen = dict(screen)
    screen["x"] = round(x, 5)
    screen["y"] = round(y, 5)
    screen["in_frame"] = 0.0 <= x <= 1.0 and 0.0 <= y <= 1.0
    return screen


def pixels_per_radian(lens, sensor, resolution):
    width = resolution[0]
    fov_x = 2.0 * math.atan(sensor / (2.0 * lens))
    return width / (2.0 * math.tan(fov_x / 2.0))


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyze(scene_config: dict, scene_id: str, render_config: dict, object_id="satellite",
            frames=None, extent_bu=None):
    scenes = scene_config.get("scenes", {})
    scene_spec = hc.resolve_scene_spec(scene_id, scenes)
    spec = _object_spec(scene_spec, object_id) or {}
    intent = spec.get("orbit_intent")
    if not intent:
        raise SystemExit("object " + repr(object_id) + " declares no orbit_intent")
    basis = orbit_basis(scene_config, scene_spec, intent)

    camera_spec = scene_spec.get("camera", {})
    defaults = scene_config.get("camera_defaults", {})
    sensor = float(defaults.get("sensor_width_mm", 36.0))
    profile = render_config["profiles"][render_config.get("default_still_profile", "master")]
    resolution = (int(profile["resolution_x"]), int(profile["resolution_y"]))
    earth_radius_bu = ax.earth_radius_km(scene_config) / ax.KM_PER_BLENDER_UNIT

    aoi_spec = sp._aoi_spec(scene_spec)
    description = ax.describe(scene_config, (aoi_spec or {}).get("fixture"), scene_spec)
    span_km = float(description["fixture"]["span_km"])
    # Physical extent used for the on-screen size estimate: the wingspan when the object
    # declares one, else the caller's override, else a bus-sized guess.
    if extent_bu is None:
        extent_bu = float(spec.get("visual_extent_bu", intent.get("visual_extent_bu", 0.6)))

    animation = scene_spec.get("animation", {})
    start = int(animation.get("frame_start", 1))
    end = int(animation.get("frame_end", start))
    frames = list(frames) if frames else list(range(start, end + 1))

    rows = []
    for frame in frames:
        camera, look_at, lens, shift = camera_state(camera_spec, frame)
        position = orbit_position(basis, intent, frame)
        screen = project_shifted(position, camera, look_at, lens, sensor, resolution, shift)
        distance = ax.length(sp._sub(position, camera))
        size_px = extent_bu / max(distance, 1e-9) * pixels_per_radian(lens, sensor, resolution)
        hidden = occluded_by_earth(camera, position, earth_radius_bu)

        aoi_centre, _ = sp.aoi_center_at(scene_config, scene_spec, frame)
        aoi_screen = project_shifted(aoi_centre, camera, look_at, lens, sensor, resolution, shift)
        corners = [
            project_shifted(sp._rotate_z(c, sp.earth_rotation_deg(scene_spec, frame)),
                            camera, look_at, lens, sensor, resolution, shift)
            for c in description["corner_positions_bu"]
        ]
        aoi_extent = None
        if all(c["x"] is not None for c in corners):
            xs = [c["x"] for c in corners]
            ys = [c["y"] for c in corners]
            aoi_extent = round(max(max(xs) - min(xs), max(ys) - min(ys)), 5)

        disc = earth_screen_extent(camera, look_at, lens, sensor, resolution, shift, earth_radius_bu)
        rows.append({
            "frame": int(frame),
            "orbit_angle_deg": round(orbit_angle_deg(intent, frame), 3),
            "satellite_world": [round(c, 4) for c in position],
            "satellite_screen": [screen["x"], screen["y"]],
            "satellite_in_frame": bool(screen["in_frame"]) and not hidden,
            "satellite_occluded": bool(hidden),
            "satellite_visible": bool(screen["in_frame"]) and not hidden,
            "satellite_distance_km": round(distance * ax.KM_PER_BLENDER_UNIT, 1),
            "satellite_size_px": round(size_px, 1),
            "satellite_size_fraction": round(size_px / resolution[0], 4),
            "aoi_screen": [aoi_screen["x"], aoi_screen["y"]],
            "aoi_extent_fraction": aoi_extent,
            "earth_disc": disc,
            "camera_radius_bu": round(ax.length(camera), 4),
            "focal_length_mm": round(lens, 3),
            "shift": [round(shift[0], 4), round(shift[1], 4)],
        })
    return {
        "scene": scene_id,
        "object": object_id,
        "intent": intent,
        "orbit_radius_bu": round(basis[2], 5),
        "orbit_altitude_km": float(intent["altitude_km"]),
        "resolution": list(resolution),
        "visual_extent_bu": extent_bu,
        "aoi_span_km": span_km,
        "frames": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Derive or analyze the satellite orbital pass.")
    parser.add_argument("--scene", default="hero_production_kizildere")
    parser.add_argument("--object", default="satellite")
    parser.add_argument("--derive", action="store_true")
    parser.add_argument("--analyze", action="store_true")
    parser.add_argument("--step", type=int, default=1)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    scene_config = hc.load_scene_config()
    if args.derive:
        print(json.dumps(derive(scene_config, args.scene, args.object), indent=2))
    if args.analyze or args.out:
        report = analyze(scene_config, args.scene, hc.load_render_config(), args.object)
        if args.step > 1:
            report["frames"] = [r for r in report["frames"] if r["frame"] % args.step == 0 or r["frame"] == 1]
        print(json.dumps(report, indent=2))
        if args.out:
            out = Path(args.out)
            hc.ensure_dir(out.parent)
            out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            print("[hero] orbit plan -> " + hc.relpath(out))
    if not (args.derive or args.analyze or args.out):
        parser.error("choose --derive and/or --analyze")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
