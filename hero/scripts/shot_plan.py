"""Derive and measure the hero camera path against the AOI it is framing.

    py -3.14 hero/scripts/shot_plan.py --scene hero_predata_animatic --analyze
    py -3.14 hero/scripts/shot_plan.py --scene hero_predata_animatic --derive

WEB-HERO-001D assembles Phase A-C into one continuous move. The hard part is
not the keyframes, it is knowing whether a keyframe actually frames the thing
the shot is about. Typing camera coordinates by eye and judging the result from
a render is how a move ends up with the AOI drifting off centre, the limb
leaving frame, or the headline area filling up with planet.

So the camera path is authored *relative to the AOI*. This module holds both
halves of that:

``derive``
    Convert a high-level shot intent -- "at frame 176 be 34 degrees off the AOI
    at a geocentric radius of 9.4 BU on a 46 mm lens" -- into the world-space
    location/look_at keyframes that go into ``scene.json``. The AOI centre is
    resolved through ``aoi_system`` and rotated by the Earth's own animated
    rotation at that frame, so a derived camera is registered to the footprint
    by construction rather than by tuning.

``analyze``
    Measure the authored keyframes back: where the AOI sits in frame, how much
    of the frame width it fills, whether the Earth limb is still in shot, and
    whether the opening keeps the headline-safe region clear of the planet.

Both halves are Blender-independent on purpose -- they are geometry, and the
validator runs them without launching Blender. What this module deliberately
does *not* do is judge motion: the authored keyframes are interpolated by
Blender's own F-curves, so speed, acceleration and focal-length rate are
measured from the evaluated camera in ``audit_shot.py`` instead of predicted
here.
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

WORLD_UP = (0.0, 0.0, 1.0)


# ---------------------------------------------------------------------------
# Small vector helpers (tuples; this module stays dependency-free)
# ---------------------------------------------------------------------------

def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _rotate_z(vector, angle_deg):
    angle = math.radians(angle_deg)
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    return (
        vector[0] * cos_a - vector[1] * sin_a,
        vector[0] * sin_a + vector[1] * cos_a,
        vector[2],
    )


# ---------------------------------------------------------------------------
# Scene interrogation
# ---------------------------------------------------------------------------

def _object_spec(scene_spec: dict, object_id: str):
    for spec in scene_spec.get("objects", []):
        if spec.get("id") == object_id:
            return spec
    return None


def _aoi_spec(scene_spec: dict):
    for spec in scene_spec.get("objects", []):
        if spec.get("type") == "aoi_system":
            return spec
    return None


def earth_rotation_deg(scene_spec: dict, frame: float) -> float:
    """Earth's animated Z rotation at ``frame``, by linear interpolation.

    Blender interpolates these keys as smoothed Beziers, so this is an
    approximation *between* keys. Every derived camera keyframe is placed on a
    frame that is also an Earth rotation key wherever it matters, and
    ``audit_shot.py`` re-measures the real evaluated rotation, so the
    approximation never reaches the published geometry.
    """
    earth = _object_spec(scene_spec, "earth")
    keys = sorted(
        (int(k["frame"]), float(k["rotation_euler_deg"][2]))
        for k in (earth or {}).get("rotation_keyframes", [])
    )
    if not keys:
        return 0.0
    if frame <= keys[0][0]:
        return keys[0][1]
    if frame >= keys[-1][0]:
        return keys[-1][1]
    for (f0, v0), (f1, v1) in zip(keys, keys[1:]):
        if f0 <= frame <= f1:
            if f1 == f0:
                return v1
            return v0 + (v1 - v0) * (frame - f0) / (f1 - f0)
    return keys[-1][1]


def aoi_center_at(scene_config: dict, scene_spec: dict, frame: float, fixture_id=None):
    """World position of the AOI centre at ``frame``, Earth rotation included."""
    spec = _aoi_spec(scene_spec)
    description = ax.describe(
        scene_config, fixture_id or (spec or {}).get("fixture"), scene_spec
    )
    return _rotate_z(
        description["center_position_bu"], earth_rotation_deg(scene_spec, frame)
    ), description


# ---------------------------------------------------------------------------
# Camera basis and projection
# ---------------------------------------------------------------------------

def camera_basis(location, look_at):
    """Right/up/forward for Blender's ``to_track_quat('-Z', 'Y')`` look-at.

    The scene builder aims every camera that way, so reproducing that basis
    here is what makes a projected screen position mean the same thing as the
    rendered frame.
    """
    forward = ax.normalize(_sub(look_at, location))
    right = _cross(forward, WORLD_UP)
    if ax.length(right) < 1e-9:
        right = _cross(forward, (0.0, 1.0, 0.0))
    right = ax.normalize(right)
    up = _cross(right, forward)
    return right, up, forward


def field_of_view(focal_mm: float, sensor_mm: float, resolution):
    """Horizontal and vertical FOV in radians for Blender's AUTO sensor fit.

    AUTO fits the sensor width to the *larger* image dimension, which for every
    profile in this lane is the horizontal one.
    """
    width, height = resolution
    fov_x = 2.0 * math.atan(sensor_mm / (2.0 * focal_mm))
    fov_y = 2.0 * math.atan(math.tan(fov_x / 2.0) * height / width)
    return fov_x, fov_y


def project(point, location, look_at, focal_mm, sensor_mm, resolution):
    """Project a world point to normalized frame coordinates.

    Frame coordinates run 0..1 left-to-right and bottom-to-top, matching how a
    reviewer describes a composition. ``in_frame`` is False for anything behind
    the camera or outside the frustum.
    """
    right, up, forward = camera_basis(location, look_at)
    offset = _sub(point, location)
    depth = _dot(offset, forward)
    if depth <= 1e-9:
        return {"in_frame": False, "behind_camera": True, "x": None, "y": None, "distance_bu": ax.length(offset)}
    fov_x, fov_y = field_of_view(focal_mm, sensor_mm, resolution)
    ndc_x = (_dot(offset, right) / depth) / math.tan(fov_x / 2.0)
    ndc_y = (_dot(offset, up) / depth) / math.tan(fov_y / 2.0)
    x = 0.5 + 0.5 * ndc_x
    y = 0.5 + 0.5 * ndc_y
    return {
        "in_frame": -0.0 <= x <= 1.0 and 0.0 <= y <= 1.0,
        "behind_camera": False,
        "x": round(x, 5),
        "y": round(y, 5),
        "distance_bu": ax.length(offset),
    }


# ---------------------------------------------------------------------------
# Framing metrics
# ---------------------------------------------------------------------------

def frame_metrics(
    location,
    look_at,
    focal_mm,
    aoi_center,
    aoi_span_km,
    earth_radius_bu,
    sensor_mm,
    resolution,
    headline_safe=None,
):
    """Everything a reviewer would otherwise have to judge from a still."""
    width, _height = resolution
    fov_x, fov_y = field_of_view(focal_mm, sensor_mm, resolution)
    screen = project(aoi_center, location, look_at, focal_mm, sensor_mm, resolution)

    slant_km = ax.length(_sub(aoi_center, location)) * ax.KM_PER_BLENDER_UNIT
    frame_width_km = 2.0 * slant_km * math.tan(fov_x / 2.0)
    aoi_fraction = aoi_span_km / frame_width_km if frame_width_km > 0 else 0.0

    # Earth disc and limb, seen from the camera.
    camera_radius = ax.length(location)
    to_center = ax.normalize(_sub((0.0, 0.0, 0.0), location))
    disc_half_angle = (
        math.asin(min(1.0, earth_radius_bu / camera_radius))
        if camera_radius > earth_radius_bu
        else math.pi / 2.0
    )
    _, _, forward = camera_basis(location, look_at)
    center_offset_angle = math.acos(max(-1.0, min(1.0, _dot(to_center, forward))))

    # The limb ring sits ``disc_half_angle`` from the Earth-centre direction in
    # every azimuth, so its closest approach to the optical axis is the
    # difference of the two angles, and its furthest is the sum.
    limb_nearest_angle = abs(disc_half_angle - center_offset_angle)
    limb_furthest_angle = disc_half_angle + center_offset_angle
    half_diagonal = math.atan(
        math.hypot(math.tan(fov_x / 2.0), math.tan(fov_y / 2.0))
    )
    limb_in_frame = limb_nearest_angle < half_diagonal < limb_furthest_angle
    earth_fills_frame = limb_nearest_angle >= half_diagonal and center_offset_angle < disc_half_angle

    # A limb clipping one corner is not the same evidence as a limb arcing
    # across the top of frame, so the two are reported separately. The vertical
    # half-FOV is the test for the second.
    limb_crosses_frame_edge = limb_nearest_angle < fov_y / 2.0

    # Incidence of the sightline at the AOI: 0 is straight down, 90 is
    # tangential. It decides how flat the footprint reads, so the approach is
    # tuned against it rather than against how a still happens to look.
    aoi_radius = ax.length(aoi_center)
    to_camera = ax.normalize(_sub(location, aoi_center))
    incidence = math.degrees(
        math.acos(max(-1.0, min(1.0, _dot(ax.normalize(aoi_center), to_camera))))
    ) if aoi_radius > 0 else None

    metrics = {
        "focal_length_mm": focal_mm,
        "fov_x_deg": round(math.degrees(fov_x), 4),
        "fov_y_deg": round(math.degrees(fov_y), 4),
        "camera_radius_bu": round(camera_radius, 5),
        "camera_altitude_km": round(
            (camera_radius - earth_radius_bu) * ax.KM_PER_BLENDER_UNIT, 2
        ),
        "aoi_slant_range_km": round(slant_km, 2),
        "frame_width_at_aoi_km": round(frame_width_km, 2),
        "aoi_fraction_of_frame_width": round(aoi_fraction, 5),
        "aoi_screen": screen,
        "earth_disc_half_angle_deg": round(math.degrees(disc_half_angle), 4),
        "optical_axis_to_earth_centre_deg": round(math.degrees(center_offset_angle), 4),
        "limb_in_frame": bool(limb_in_frame),
        "limb_crosses_frame_edge": bool(limb_crosses_frame_edge),
        "limb_clearance_deg": round(math.degrees(half_diagonal - limb_nearest_angle), 4),
        "earth_fills_frame": bool(earth_fills_frame),
        "aoi_incidence_deg": round(incidence, 4) if incidence is not None else None,
        "earth_metres_per_render_pixel": round(frame_width_km * 1000.0 / width, 2),
    }

    if headline_safe:
        metrics["headline_safe"] = _headline_safe_metrics(
            location, look_at, focal_mm, earth_radius_bu, sensor_mm, resolution, headline_safe
        )
    return metrics


def _headline_safe_metrics(
    location, look_at, focal_mm, earth_radius_bu, sensor_mm, resolution, region
):
    """How much of the reserved copy region the Earth disc intrudes into.

    Website copy is never baked into the render, so the only thing this phase
    owes the later integration task is *space*: a region of the opening frames
    where the planet is not, so a headline can sit on near-empty sky. Sampling
    the region on a grid and asking, per sample, whether the ray through it
    hits the Earth answers that without rendering anything.
    """
    x0, y0 = float(region["x0"]), float(region["y0"])
    x1, y1 = float(region["x1"]), float(region["y1"])
    steps = int(region.get("samples", 24))
    fov_x, fov_y = field_of_view(focal_mm, sensor_mm, resolution)
    right, up, forward = camera_basis(location, look_at)
    tan_x, tan_y = math.tan(fov_x / 2.0), math.tan(fov_y / 2.0)

    hits = 0
    total = 0
    for i in range(steps):
        for j in range(steps):
            x = x0 + (x1 - x0) * (i / float(steps - 1)) if steps > 1 else (x0 + x1) / 2
            y = y0 + (y1 - y0) * (j / float(steps - 1)) if steps > 1 else (y0 + y1) / 2
            ndc_x = (x - 0.5) * 2.0
            ndc_y = (y - 0.5) * 2.0
            direction = ax.normalize(
                (
                    forward[0] + right[0] * ndc_x * tan_x + up[0] * ndc_y * tan_y,
                    forward[1] + right[1] * ndc_x * tan_x + up[1] * ndc_y * tan_y,
                    forward[2] + right[2] * ndc_x * tan_x + up[2] * ndc_y * tan_y,
                )
            )
            total += 1
            if _ray_hits_sphere(location, direction, earth_radius_bu):
                hits += 1

    return {
        "region": {"x0": x0, "y0": y0, "x1": x1, "y1": y1},
        "samples": total,
        "earth_hits": hits,
        "occupancy": round(hits / float(total), 5) if total else 0.0,
        "clear": hits == 0,
    }


def _ray_hits_sphere(origin, direction, radius, center=(0.0, 0.0, 0.0)) -> bool:
    offset = _sub(origin, center)
    b = 2.0 * _dot(offset, direction)
    c = _dot(offset, offset) - radius * radius
    discriminant = b * b - 4.0 * c
    if discriminant < 0.0:
        return False
    root = math.sqrt(discriminant)
    return (-b - root) / 2.0 > 0.0 or (-b + root) / 2.0 > 0.0


# ---------------------------------------------------------------------------
# Derivation: shot intent -> world keyframes
# ---------------------------------------------------------------------------

def derive_keyframe(scene_config: dict, scene_spec: dict, intent: dict, fixture_id=None):
    """One shot-intent entry -> one world-space camera keyframe.

    ``mode: world`` passes an explicitly authored keyframe through untouched;
    that is how the accepted Phase-B establish states stay bit-identical while
    being re-timed. ``mode: aoi_relative`` places the camera by geocentric
    radius and an angular offset from the AOI, and aims it at the AOI, so
    everything after the establish is registered to the footprint by
    construction.
    """
    frame = int(intent["frame"])
    mode = intent.get("mode", "aoi_relative")

    if mode == "world":
        return {
            "frame": frame,
            "location": [float(v) for v in intent["location"]],
            "look_at": [float(v) for v in intent["look_at"]],
            "focal_length_mm": float(intent["focal_length_mm"]),
        }

    if mode != "aoi_relative":
        raise ValueError("unknown shot-intent mode " + repr(mode))

    center, _description = aoi_center_at(scene_config, scene_spec, frame, fixture_id)
    center_unit = ax.normalize(center)

    # Build a local frame at the AOI: north is the component of world +Z
    # perpendicular to the radial, east completes the right-handed set. An
    # angular offset along a bearing then means the same thing at any latitude.
    north = _sub(WORLD_UP, ax.scale(center_unit, _dot(WORLD_UP, center_unit)))
    north = ax.normalize(north) if ax.length(north) > 1e-9 else (1.0, 0.0, 0.0)
    east = ax.normalize(_cross(north, center_unit))

    offset_angle = math.radians(float(intent.get("offset_deg", 0.0)))
    bearing = math.radians(float(intent.get("bearing_deg", 0.0)))
    tangent = _add(
        ax.scale(north, math.cos(bearing)), ax.scale(east, math.sin(bearing))
    )
    direction = _add(
        ax.scale(center_unit, math.cos(offset_angle)),
        ax.scale(tangent, math.sin(offset_angle)),
    )
    location = ax.scale(ax.normalize(direction), float(intent["radius_bu"]))

    look_at = list(center)
    for axis, key in enumerate(("aim_offset_x", "aim_offset_y", "aim_offset_z")):
        look_at[axis] += float(intent.get(key, 0.0))

    return {
        "frame": frame,
        "location": [round(v, 4) for v in location],
        "look_at": [round(v, 4) for v in look_at],
        "focal_length_mm": float(intent["focal_length_mm"]),
    }


def derive(scene_config: dict, scene_id: str, fixture_id=None):
    scenes = scene_config.get("scenes", {})
    scene_spec = hc.resolve_scene_spec(scene_id, scenes)
    intent = scene_spec.get("camera", {}).get("shot_intent")
    if not intent:
        raise SystemExit(
            "scene " + repr(scene_id) + " declares no camera.shot_intent to derive from"
        )
    return [
        derive_keyframe(scene_config, scene_spec, entry, fixture_id)
        for entry in sorted(intent, key=lambda e: int(e["frame"]))
    ]


# ---------------------------------------------------------------------------
# Analysis: authored keyframes -> framing report
# ---------------------------------------------------------------------------

def analyze(scene_config: dict, scene_id: str, render_config: dict, fixture_id=None):
    scenes = scene_config.get("scenes", {})
    scene_spec = hc.resolve_scene_spec(scene_id, scenes)
    camera = scene_spec.get("camera", {})
    keyframes = sorted(camera.get("keyframes", []), key=lambda k: int(k["frame"]))
    if not keyframes:
        raise SystemExit("scene " + repr(scene_id) + " has no camera keyframes")

    aoi_spec = _aoi_spec(scene_spec)
    description = ax.describe(
        scene_config, fixture_id or (aoi_spec or {}).get("fixture"), scene_spec
    )
    span_km = float(description["fixture"]["span_km"])
    earth_radius_bu = description["earth_radius_bu"]

    defaults = scene_config.get("camera_defaults", {})
    sensor_mm = float(defaults.get("sensor_width_mm", 36.0))
    profile = render_config["profiles"][render_config.get("default_still_profile", "master")]
    resolution = (int(profile["resolution_x"]), int(profile["resolution_y"]))

    composition = camera.get("composition", {})
    headline_safe = composition.get("headline_safe_region")
    headline_frames = composition.get("headline_safe_through_frame")

    entries = []
    for keyframe in keyframes:
        frame = int(keyframe["frame"])
        center, _ = aoi_center_at(scene_config, scene_spec, frame, fixture_id)
        wants_safe = headline_safe and (
            headline_frames is None or frame <= int(headline_frames)
        )
        entry = {"frame": frame}
        entry.update(
            frame_metrics(
                tuple(keyframe["location"]),
                tuple(keyframe["look_at"]),
                float(keyframe["focal_length_mm"]),
                center,
                span_km,
                earth_radius_bu,
                sensor_mm,
                resolution,
                headline_safe=headline_safe if wants_safe else None,
            )
        )
        entries.append(entry)

    return {
        "scene": scene_id,
        "fixture": description["fixture_id"],
        "resolution": list(resolution),
        "sensor_width_mm": sensor_mm,
        "aoi_span_km": span_km,
        "keyframes": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Derive or analyze the hero camera path.")
    parser.add_argument("--scene", default="hero_predata_animatic")
    parser.add_argument("--aoi-fixture", default=None)
    parser.add_argument("--derive", action="store_true", help="print derived world keyframes")
    parser.add_argument("--analyze", action="store_true", help="print the framing report")
    parser.add_argument("--out", default=None, help="write the framing report as JSON")
    args = parser.parse_args()

    scene_config = hc.load_scene_config()
    if args.derive:
        print(json.dumps(derive(scene_config, args.scene, args.aoi_fixture), indent=2))
    if args.analyze or args.out:
        report = analyze(
            scene_config, args.scene, hc.load_render_config(), args.aoi_fixture
        )
        print(json.dumps(report, indent=2))
        if args.out:
            out = Path(args.out)
            hc.ensure_dir(out.parent)
            out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            print("[hero] shot plan -> " + hc.relpath(out))
    if not (args.derive or args.analyze or args.out):
        parser.error("choose --derive and/or --analyze")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
