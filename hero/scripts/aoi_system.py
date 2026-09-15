"""Surface-conforming AOI geometry for the OrbGSS hero scene.

This module owns every coordinate conversion and sampling decision behind the
WEB-HERO-001C acquisition system. It is deliberately Blender-independent — it
must stay importable by a plain CPython interpreter so ``validate_hero.py`` can
check AOI geometry deterministically without launching Blender, and so the same
numbers the renderer uses are the numbers the validator audits.

Nothing here may import ``bpy`` or ``mathutils``.

World convention (see ``world_coordinate_convention`` in scene.json)
-------------------------------------------------------------------
1 Blender unit = 1000 km, Earth centre at the world origin, world +Z is
geographic north. A point's world azimuth (measured from +X, counter-clockwise
seen from +Z) relates to its geographic longitude through the Earth material's
equirectangular longitude shift::

    azimuth_deg = longitude_deg - texture_longitude_offset_deg

The offset exists because the Earth albedo/night maps are equirectangular
textures wrapped onto a Blender UV sphere whose seam does not sit at the
Greenwich meridian. The UV sphere convention was measured, not assumed:
``u = azimuth/360 + 0.5`` and ``v = latitude/180 + 0.5``, and an equirectangular
map places longitude 0 at ``u = 0.5``. Keeping the offset in configuration means
the AOI lands where its configured coordinates say it does on the actual
texture, instead of being nudged into place by eye.

Geometry contract
-----------------
Every point this module emits is produced by normalising a direction vector and
scaling it by one radius. Conformance to the sphere is therefore true by
construction rather than by tuning, and the validator's tolerance check exists
to catch an implementation regression, not to paper over an approximation.

Pre-data boundary: the fixtures this module reads are design placeholders. They
carry no measurement meaning, and nothing here derives, encodes or renders a
scientific quantity.
"""

from __future__ import annotations

import math

# Mean Earth radius in kilometres, matching world_coordinate_convention.
DEFAULT_EARTH_RADIUS_KM = 6371.0
KM_PER_BLENDER_UNIT = 1000.0

CORNER_IDS = ("nw", "ne", "se", "sw")

# Bearing (degrees clockwise from north) from the footprint centre toward each
# corner of an un-rotated square footprint.
CORNER_BEARINGS = {"nw": 315.0, "ne": 45.0, "se": 135.0, "sw": 225.0}


# ---------------------------------------------------------------------------
# Vector helpers (plain tuples; no external dependency)
# ---------------------------------------------------------------------------

def normalize(vector):
    x, y, z = vector
    length = math.sqrt(x * x + y * y + z * z)
    if length == 0.0:
        raise ValueError("cannot normalize a zero-length vector")
    return (x / length, y / length, z / length)


def scale(vector, factor):
    return (vector[0] * factor, vector[1] * factor, vector[2] * factor)


def length(vector):
    return math.sqrt(sum(component * component for component in vector))


def slerp(a, b, t):
    """Spherical linear interpolation between two unit vectors.

    Used for every AOI edge and interior sample. Because the result of a slerp
    between unit vectors is itself a unit vector, an edge sampled this way lies
    exactly on the sphere at every sample — it follows the globe's curvature
    instead of cutting a straight 3D chord across it.
    """
    dot = max(-1.0, min(1.0, sum(x * y for x, y in zip(a, b))))
    theta = math.acos(dot)
    if theta < 1e-9:
        return normalize(a)
    sin_theta = math.sin(theta)
    wa = math.sin((1.0 - t) * theta) / sin_theta
    wb = math.sin(t * theta) / sin_theta
    return normalize(
        (a[0] * wa + b[0] * wb, a[1] * wa + b[1] * wb, a[2] * wa + b[2] * wb)
    )


# ---------------------------------------------------------------------------
# Geographic <-> world conversion
# ---------------------------------------------------------------------------

def geographic_to_unit(lat_deg: float, lon_deg: float, longitude_offset_deg: float = 0.0):
    """Unit direction, in Earth-local world axes, for a geographic coordinate."""
    lat = math.radians(lat_deg)
    azimuth = math.radians(lon_deg - longitude_offset_deg)
    cos_lat = math.cos(lat)
    return (cos_lat * math.cos(azimuth), cos_lat * math.sin(azimuth), math.sin(lat))


def unit_to_geographic(vector, longitude_offset_deg: float = 0.0):
    """Inverse of :func:`geographic_to_unit`, for audit and round-trip checks."""
    x, y, z = normalize(vector)
    lat_deg = math.degrees(math.asin(max(-1.0, min(1.0, z))))
    lon_deg = math.degrees(math.atan2(y, x)) + longitude_offset_deg
    while lon_deg > 180.0:
        lon_deg -= 360.0
    while lon_deg < -180.0:
        lon_deg += 360.0
    return (lat_deg, lon_deg)


def destination(lat_deg: float, lon_deg: float, bearing_deg: float, angular_distance: float):
    """Great-circle destination point.

    Standard spherical destination formula: travel ``angular_distance``
    (radians of arc) from (lat, lon) along a constant initial ``bearing_deg``
    measured clockwise from north. Corners derived this way sit on the sphere
    and stay correct at any latitude, including near the poles, which a naive
    "add degrees to lat/lon" box does not.
    """
    lat1 = math.radians(lat_deg)
    lon1 = math.radians(lon_deg)
    bearing = math.radians(bearing_deg)

    sin_lat2 = math.sin(lat1) * math.cos(angular_distance) + math.cos(lat1) * math.sin(
        angular_distance
    ) * math.cos(bearing)
    lat2 = math.asin(max(-1.0, min(1.0, sin_lat2)))
    lon2 = lon1 + math.atan2(
        math.sin(bearing) * math.sin(angular_distance) * math.cos(lat1),
        math.cos(angular_distance) - math.sin(lat1) * sin_lat2,
    )
    return (math.degrees(lat2), math.degrees(lon2))


# ---------------------------------------------------------------------------
# Fixture resolution
# ---------------------------------------------------------------------------

class AOIFixtureError(ValueError):
    """Raised when AOI configuration cannot be resolved into geometry."""


REQUIRED_FIXTURE_FIELDS = ("center_lat_deg", "center_lon_deg", "span_km")

FIXTURE_DEFAULTS = {
    "bearing_deg": 0.0,
    "surface_offset_m": 250.0,
    "edge_samples": 48,
    "fill_grid": 24,
    "border_width_km": 14.0,
    "corner_lock_arm_km": 70.0,
    "corner_lock_width_km": 9.0,
    "corner_lock_offset_m": 400.0,
}


def interface_of(scene_config: dict) -> dict:
    interface = scene_config.get("aoi_injection_interface")
    if not isinstance(interface, dict):
        raise AOIFixtureError(
            "scene.json declares no aoi_injection_interface; AOI geometry has no configuration source"
        )
    return interface


def fixture_ids(scene_config: dict):
    return sorted(interface_of(scene_config).get("fixtures", {}))


def resolve_fixture(scene_config: dict, fixture_id: str | None = None) -> dict:
    """Resolve a named AOI fixture into a fully defaulted configuration dict.

    ``fixture_id`` of ``None`` selects the interface's ``active_fixture``. This
    single entry point is what makes the AOI configurable: the scene builder,
    the validator and the geometry audit all resolve fixtures through here, so
    swapping fixtures never requires a code change anywhere downstream.
    """
    interface = interface_of(scene_config)
    fixtures = interface.get("fixtures", {})
    if not fixtures:
        raise AOIFixtureError("aoi_injection_interface declares no fixtures")

    chosen = fixture_id or interface.get("active_fixture")
    if not chosen:
        raise AOIFixtureError(
            "no fixture requested and aoi_injection_interface declares no active_fixture"
        )
    if chosen not in fixtures:
        raise AOIFixtureError(
            "AOI fixture " + repr(chosen) + " is not defined; available: " + repr(sorted(fixtures))
        )

    resolved = dict(FIXTURE_DEFAULTS)
    resolved.update(fixtures[chosen])
    resolved["id"] = chosen

    missing = [field for field in REQUIRED_FIXTURE_FIELDS if resolved.get(field) is None]
    if missing:
        raise AOIFixtureError(
            "AOI fixture " + repr(chosen) + " is missing required fields " + repr(missing)
        )
    if float(resolved["span_km"]) <= 0.0:
        raise AOIFixtureError("AOI fixture " + repr(chosen) + " has a non-positive span_km")

    resolved["corner_order"] = list(
        resolved.get("corner_order", interface.get("corner_order", CORNER_IDS))
    )
    unknown = [c for c in resolved["corner_order"] if c not in CORNER_IDS]
    if unknown:
        raise AOIFixtureError("AOI fixture " + repr(chosen) + " has unknown corners " + repr(unknown))
    if len(set(resolved["corner_order"])) != 4:
        raise AOIFixtureError(
            "AOI fixture " + repr(chosen) + " must name all four corners exactly once"
        )
    return resolved


def earth_radius_km(scene_config: dict) -> float:
    convention = scene_config.get("world_coordinate_convention", {})
    return float(convention.get("earth_radius_km", DEFAULT_EARTH_RADIUS_KM))


def longitude_offset_deg(scene_config: dict, scene_spec: dict | None = None) -> float:
    """Longitude offset that aligns configured coordinates with the Earth texture.

    Read from the Earth material's ``texture_rotation_deg`` when a scene is
    given, so the AOI automatically follows any future re-framing of the globe
    instead of silently drifting off its configured coordinates.
    """
    if scene_spec:
        for material in scene_spec.get("materials", {}).values():
            if material.get("type") == "earth_day_night":
                return float(material.get("texture_rotation_deg", 0.0))
    interface = scene_config.get("aoi_injection_interface", {})
    return float(interface.get("texture_longitude_offset_deg", 0.0))


# ---------------------------------------------------------------------------
# Derived geometry
# ---------------------------------------------------------------------------

def surface_radius_bu(fixture: dict, radius_km: float, extra_offset_m: float = 0.0) -> float:
    """Sphere radius, in Blender units, that AOI geometry is generated on.

    Earth radius plus a very small visual offset whose only job is to stop the
    AOI z-fighting with the Earth surface it is drawn on.
    """
    offset_km = (float(fixture["surface_offset_m"]) + float(extra_offset_m)) / 1000.0
    return (radius_km + offset_km) / KM_PER_BLENDER_UNIT


def corner_geographic(fixture: dict, radius_km: float):
    """Geographic (lat, lon) of each footprint corner, in configured order."""
    half_diagonal = (float(fixture["span_km"]) * math.sqrt(2.0) / 2.0) / radius_km
    bearing_offset = float(fixture["bearing_deg"])
    return [
        destination(
            float(fixture["center_lat_deg"]),
            float(fixture["center_lon_deg"]),
            CORNER_BEARINGS[corner] + bearing_offset,
            half_diagonal,
        )
        for corner in fixture["corner_order"]
    ]


def corner_units(fixture: dict, radius_km: float, lon_offset_deg: float):
    return [
        geographic_to_unit(lat, lon, lon_offset_deg)
        for lat, lon in corner_geographic(fixture, radius_km)
    ]


def center_unit(fixture: dict, lon_offset_deg: float):
    return geographic_to_unit(
        float(fixture["center_lat_deg"]), float(fixture["center_lon_deg"]), lon_offset_deg
    )


def boundary_units(fixture: dict, radius_km: float, lon_offset_deg: float):
    """Densely sampled closed boundary ring as unit vectors.

    Each edge is subdivided into ``edge_samples`` slerp steps, so the border
    traces the great-circle arc between corners and visibly bends with the
    globe rather than reading as four straight chords.
    """
    corners = corner_units(fixture, radius_km, lon_offset_deg)
    steps = max(2, int(fixture["edge_samples"]))
    ring = []
    for index in range(4):
        start = corners[index]
        end = corners[(index + 1) % 4]
        for step in range(steps):
            ring.append(slerp(start, end, step / float(steps)))
    return ring


def fill_units(fixture: dict, radius_km: float, lon_offset_deg: float):
    """Interior footprint samples as a (grid+1) x (grid+1) list of unit rows.

    Each sample is a double slerp — along the two opposing edges, then between
    those two points — so the interior lies on the same sphere as the border,
    and the grid indices double as the AOI-local (u, v) parameter space the
    scan sweep travels through.
    """
    corners = corner_units(fixture, radius_km, lon_offset_deg)
    nw, ne, se, sw = (corners[fixture["corner_order"].index(c)] for c in CORNER_IDS)
    grid = max(1, int(fixture["fill_grid"]))

    rows = []
    for j in range(grid + 1):
        v = j / float(grid)
        rows.append(
            [
                slerp(
                    slerp(nw, ne, i / float(grid)),
                    slerp(sw, se, i / float(grid)),
                    v,
                )
                for i in range(grid + 1)
            ]
        )
    return rows


def corner_lock_units(fixture: dict, radius_km: float, lon_offset_deg: float):
    """Inward-pointing arm endpoints for each corner-lock marker.

    Each lock is drawn as two short arms running from the corner along the two
    footprint edges that meet there, which keeps the marker attached to the
    footprint itself instead of floating as an unrelated glyph.
    """
    corners = corner_units(fixture, radius_km, lon_offset_deg)
    span_km = float(fixture["span_km"])
    arm_fraction = min(0.45, float(fixture["corner_lock_arm_km"]) / span_km)

    locks = []
    for index, corner in enumerate(corners):
        previous = corners[(index - 1) % 4]
        following = corners[(index + 1) % 4]
        locks.append(
            {
                "corner_id": fixture["corner_order"][index],
                "apex": corner,
                "arms": [
                    slerp(corner, following, arm_fraction),
                    slerp(corner, previous, arm_fraction),
                ],
            }
        )
    return locks


def describe(scene_config: dict, fixture_id: str | None = None, scene_spec: dict | None = None):
    """Full resolved AOI description: the one shape every consumer reads.

    Returned as plain data so the Blender builder, the validator and the
    geometry audit all work from an identical description of the same AOI.
    """
    fixture = resolve_fixture(scene_config, fixture_id)
    radius_km = earth_radius_km(scene_config)
    lon_offset = longitude_offset_deg(scene_config, scene_spec)
    radius_bu = surface_radius_bu(fixture, radius_km)

    corners = corner_units(fixture, radius_km, lon_offset)
    return {
        "fixture_id": fixture["id"],
        "fixture": fixture,
        "earth_radius_km": radius_km,
        "earth_radius_bu": radius_km / KM_PER_BLENDER_UNIT,
        "longitude_offset_deg": lon_offset,
        "surface_radius_bu": radius_bu,
        "surface_offset_m": float(fixture["surface_offset_m"]),
        "corner_order": list(fixture["corner_order"]),
        "corner_geographic": corner_geographic(fixture, radius_km),
        "corner_units": corners,
        "corner_positions_bu": [scale(unit, radius_bu) for unit in corners],
        "center_unit": center_unit(fixture, lon_offset),
        "center_position_bu": scale(center_unit(fixture, lon_offset), radius_bu),
        "boundary_units": boundary_units(fixture, radius_km, lon_offset),
        "fill_rows": fill_units(fixture, radius_km, lon_offset),
        "corner_locks": corner_lock_units(fixture, radius_km, lon_offset),
    }


def boundary_sample_spacing_km(description: dict) -> float:
    """Mean arc spacing between adjacent boundary samples, in kilometres.

    The validator uses this to prove the border is sampled densely enough to
    read as a curve at the phase's shot scale rather than as a polygon.
    """
    ring = description["boundary_units"]
    radius_km = description["earth_radius_km"]
    total = 0.0
    for index in range(len(ring)):
        a = ring[index]
        b = ring[(index + 1) % len(ring)]
        dot = max(-1.0, min(1.0, sum(x * y for x, y in zip(a, b))))
        total += math.acos(dot) * radius_km
    return total / len(ring)


def max_chord_sagitta_km(description: dict) -> float:
    """Largest gap between a sampled boundary chord and the true spherical arc.

    This is the number that actually answers "does the border detach from the
    globe": it measures how far the straight segment drawn between two adjacent
    samples falls beneath the surface it is meant to follow.
    """
    ring = description["boundary_units"]
    radius_km = description["earth_radius_km"]
    worst = 0.0
    for index in range(len(ring)):
        a = ring[index]
        b = ring[(index + 1) % len(ring)]
        dot = max(-1.0, min(1.0, sum(x * y for x, y in zip(a, b))))
        half_angle = math.acos(dot) / 2.0
        worst = max(worst, radius_km * (1.0 - math.cos(half_angle)))
    return worst


def radius_deviation_bu(description: dict):
    """(max, mean) deviation of every emitted point from the configured radius."""
    target = description["surface_radius_bu"]
    points = []
    points.extend(description["corner_positions_bu"])
    points.append(description["center_position_bu"])
    points.extend(scale(unit, target) for unit in description["boundary_units"])
    for row in description["fill_rows"]:
        points.extend(scale(unit, target) for unit in row)
    for lock in description["corner_locks"]:
        points.append(scale(lock["apex"], target))
        points.extend(scale(arm, target) for arm in lock["arms"])

    deviations = [abs(length(point) - target) for point in points]
    return (max(deviations), sum(deviations) / len(deviations), len(deviations))
