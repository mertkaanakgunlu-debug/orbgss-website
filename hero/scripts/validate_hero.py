"""Validate the hero production workspace without launching Blender.

    py -3.14 hero/scripts/validate_hero.py

Fails loudly on broken production assumptions: missing scaffold, unparseable or
inconsistent configuration, a structurally invalid rights manifest, a scientific
layer smuggled into this pre-data phase, generated output treated as source
authority, or public-site contamination from the hero lane.

This is a contract checker, not a build system. Keep it that way.
"""

from __future__ import annotations

import json
import math
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import aoi_system as aoi  # noqa: E402
import hero_common as hc  # noqa: E402
import orbit_plan  # noqa: E402
import shot_plan  # noqa: E402

MAX_TRACKED_BYTES = 4 * 1024 * 1024

# AOI geometry contract (WEB-HERO-001C).
# The radius tolerance is a float64 sanity bound: this module generates the
# points itself in plain Python, so anything above millimetres means the
# implementation drifted, not that arithmetic did.
AOI_RADIUS_TOLERANCE_M = 0.001
# "A very small visual offset only to prevent z-fighting" -- an AOI that sits
# kilometres above its own ground is hovering, not conforming.
AOI_MAX_SURFACE_OFFSET_M = 2000.0
# Each footprint edge must carry at least this many samples' worth of density,
# expressed as span / spacing, so the border bends instead of reading as a
# polygon at the phase's shot scale.
AOI_MIN_SAMPLES_PER_EDGE_SPAN = 24.0
# How far a drawn chord may fall beneath the spherical arc it stands in for.
AOI_MAX_SAGITTA_KM = 0.05
AOI_ALLOWED_BEAM_TARGETS = {"corners", "corners_and_center", "center"}
SELF_NAME = Path(__file__).name
HEX64 = re.compile(r"^[0-9a-f]{64}$")

# Populated by check_pre_data_boundary from the manifest, then reused by the
# AOI checks so there is a single declared vocabulary of forbidden layers.
FORBIDDEN_CACHE = {"classes": set()}


class Report:
    def __init__(self) -> None:
        self.checks = 0
        self.failures = []

    def check(self, ok: bool, label: str, detail: str = "") -> bool:
        self.checks += 1
        if ok:
            print("  PASS  " + label)
        else:
            message = label + ((" — " + detail) if detail else "")
            print("  FAIL  " + message)
            self.failures.append(message)
        return ok

    def section(self, title: str) -> None:
        print("\n" + title)


def tokens(value: str):
    return {token for token in re.split(r"[^a-zA-Z0-9]+", str(value).lower()) if token}


def check_scaffold(report: Report) -> None:
    report.section("scaffold")
    for path in (
        hc.CONFIG_DIR,
        hc.ASSETS_DIR,
        hc.SOURCE_DIR,
        hc.BLEND_DIR,
        hc.RENDERS_DIR,
        hc.EVIDENCE_DIR,
    ):
        report.check(path.is_dir(), "directory present: " + hc.relpath(path))

    for path in (
        hc.SCENE_CONFIG,
        hc.RENDER_CONFIG,
        hc.LANE_CONFIG,
        hc.ASSET_MANIFEST,
        hc.HERO_ROOT / "README.md",
    ):
        report.check(path.is_file(), "file present: " + hc.relpath(path))

    for name in (
        "hero_common.py",
        "build_scene.py",
        "render_core.py",
        "render_preview.py",
        "render_still.py",
        "probe_env.py",
        "validate_hero.py",
    ):
        path = hc.HERO_ROOT / "scripts" / name
        report.check(path.is_file(), "entrypoint present: " + hc.relpath(path))


def load_configs(report: Report):
    report.section("configuration parses")
    loaded = {}
    for key, path in (
        ("scene", hc.SCENE_CONFIG),
        ("render", hc.RENDER_CONFIG),
        ("lane", hc.LANE_CONFIG),
        ("manifest", hc.ASSET_MANIFEST),
    ):
        try:
            loaded[key] = hc.load_json(path)
            report.check(True, "parseable JSON: " + hc.relpath(path))
        except (OSError, json.JSONDecodeError) as error:
            loaded[key] = None
            report.check(False, "parseable JSON: " + hc.relpath(path), str(error))
    return loaded


def check_render_profiles(report: Report, render_config) -> None:
    report.section("render profile consistency")
    if not render_config:
        report.check(False, "render profiles loaded")
        return

    profiles = render_config.get("profiles", {})
    aliases = render_config.get("engine_aliases", {})
    aspect = render_config.get("aspect_ratio", {})

    report.check(bool(profiles), "at least one render profile is defined")
    report.check(
        bool(aspect.get("width")) and bool(aspect.get("height")),
        "a working aspect ratio is configured",
    )

    required = ("role", "engine", "resolution_x", "resolution_y", "samples", "file_format")
    for name, profile in profiles.items():
        missing = [key for key in required if key not in profile]
        report.check(
            not missing,
            "profile " + name + " declares required keys",
            "missing " + repr(missing),
        )
        report.check(
            profile.get("engine") in aliases,
            "profile " + name + " uses a known logical engine",
            repr(profile.get("engine")) + " not in " + repr(sorted(aliases)),
        )
        if aspect and "resolution_x" in profile and "resolution_y" in profile:
            matches = (
                profile["resolution_x"] * aspect["height"]
                == profile["resolution_y"] * aspect["width"]
            )
            report.check(
                matches,
                "profile " + name + " matches the configured aspect ratio",
                str(profile["resolution_x"]) + "x" + str(profile["resolution_y"]),
            )

    roles = {profile.get("role") for profile in profiles.values()}
    report.check("fast_iteration" in roles, "a fast iteration profile exists")
    report.check("high_quality" in roles, "a high quality profile exists")

    high_quality = [p for p in profiles.values() if p.get("role") == "high_quality"]
    report.check(
        all(p.get("engine") == "CYCLES" for p in high_quality),
        "every high quality profile targets Cycles",
    )

    for key in ("default_preview_profile", "default_still_profile"):
        report.check(
            render_config.get(key) in profiles,
            "configured " + key + " resolves to a defined profile",
            repr(render_config.get(key)),
        )

    report.check(
        bool(render_config.get("device_preference")),
        "a GPU device preference order is configured",
    )
    report.check(
        "allow_cpu_fallback" in render_config,
        "CPU fallback policy is stated explicitly",
    )


def check_scene_config(report: Report, scene_config, render_config) -> None:
    report.section("scene configuration")
    if not scene_config:
        report.check(False, "scene configuration loaded")
        return

    palette = scene_config.get("palette", {})
    scenes = scene_config.get("scenes", {})
    report.check(bool(palette), "a palette is defined")
    report.check(bool(scenes), "at least one scene is defined")

    for scene_id, spec in scenes.items():
        refs = []
        for material in spec.get("materials", {}).values():
            refs.append(material.get("base_color_ref"))
            if material.get("emission_color_ref"):
                refs.append(material["emission_color_ref"])
        for light in spec.get("lights", []):
            if light.get("color_ref"):
                refs.append(light["color_ref"])
        world_ref = scene_config.get("world", {}).get("background_color_ref")
        if world_ref:
            refs.append(world_ref)

        unknown = sorted({ref for ref in refs if ref and ref not in palette})
        report.check(
            not unknown,
            "scene " + scene_id + " resolves every palette reference",
            "unknown " + repr(unknown),
        )

        materials = set(spec.get("materials", {}))
        dangling = sorted(
            {
                obj.get("material")
                for obj in spec.get("objects", [])
                if obj.get("material") and obj["material"] not in materials
            }
        )
        report.check(
            not dangling,
            "scene " + scene_id + " resolves every material reference",
            "undefined " + repr(dangling),
        )
        report.check(
            bool(hc.resolve_scene_spec(scene_id, scenes).get("camera")), "scene " + scene_id + " defines a camera"
        )

    interface = scene_config.get("aoi_injection_interface")
    report.check(
        isinstance(interface, dict),
        "a configuration-driven AOI/data injection interface is declared",
    )


def check_aoi_system(report: Report, scene_config) -> None:
    """WEB-HERO-001C: the AOI must be configuration-driven and on the sphere.

    Everything here is derived from ``aoi_system``, the same module the scene
    builder uses, so this checks the real geometry contract rather than a
    restatement of it. Whether the result *looks* attached to the planet is not
    decidable here and is left to the rendered evidence; what is decidable --
    that every emitted point lies on the configured sphere, that the border is
    sampled densely enough to read as a curve, that four corners resolve, that
    beams aim at the AOI system instead of at constants, and that a second
    fixture flows through the same code path -- is checked.
    """
    report.section("AOI acquisition system (WEB-HERO-001C)")
    if not scene_config:
        report.check(False, "scene configuration loaded")
        return

    try:
        interface = aoi.interface_of(scene_config)
    except aoi.AOIFixtureError as error:
        report.check(False, "AOI injection interface is declared", str(error))
        return

    fixtures = interface.get("fixtures", {})
    report.check(bool(fixtures), "AOI interface declares at least one fixture")
    report.check(
        interface.get("active_fixture") in fixtures,
        "AOI interface names an active fixture that resolves",
        repr(interface.get("active_fixture")),
    )
    # Configurability is a contract, not a demo: a second fixture must exist so
    # a footprint cannot be quietly hand-fitted to one shot.
    report.check(
        len(fixtures) >= 2,
        "a second AOI fixture exists, so the system is provably configurable",
        "only " + repr(sorted(fixtures)),
    )
    report.check(
        bool(interface.get("schema")),
        "AOI interface documents its configuration schema",
    )

    earth_radius_km = aoi.earth_radius_km(scene_config)
    descriptions = {}

    for fixture_id in sorted(fixtures):
        label = "AOI fixture " + fixture_id
        try:
            description = aoi.describe(scene_config, fixture_id)
        except (aoi.AOIFixtureError, KeyError, ValueError) as error:
            report.check(False, label + " resolves to geometry", str(error))
            continue
        descriptions[fixture_id] = description
        fixture = description["fixture"]

        # 1. every emitted point sits on the configured sphere.
        worst, mean, count = aoi.radius_deviation_bu(description)
        worst_m = worst * aoi.KM_PER_BLENDER_UNIT * 1000.0
        report.check(
            worst_m <= AOI_RADIUS_TOLERANCE_M,
            label + " keeps all " + str(count) + " generated points on the configured sphere",
            "worst radial deviation " + str(round(worst_m, 6)) + " m > "
            + str(AOI_RADIUS_TOLERANCE_M) + " m",
        )

        # 2. the offset is a z-fighting guard, not a hovering altitude.
        offset_m = float(fixture["surface_offset_m"])
        report.check(
            0.0 < offset_m <= AOI_MAX_SURFACE_OFFSET_M,
            label + " lifts off the surface only enough to avoid z-fighting",
            str(offset_m) + " m is outside (0, " + str(AOI_MAX_SURFACE_OFFSET_M) + "] m",
        )

        # 3. four corners, named once each, resolving to real coordinates.
        corners = description["corner_geographic"]
        report.check(
            len(corners) == 4 and len(set(description["corner_order"])) == 4,
            label + " resolves exactly four uniquely named corners",
            repr(description["corner_order"]),
        )
        report.check(
            all(
                -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0 for lat, lon in corners
            ),
            label + " corner coordinates are geographically well-formed",
            repr(corners),
        )

        # 4. the footprint really is the configured size on the sphere.
        span_km = float(fixture["span_km"])
        units = description["corner_units"]
        edges = []
        for index in range(4):
            a = units[index]
            b = units[(index + 1) % 4]
            dot = max(-1.0, min(1.0, sum(x * y for x, y in zip(a, b))))
            edges.append(math.acos(dot) * earth_radius_km)
        error_km = max(abs(edge - span_km) for edge in edges)
        report.check(
            error_km <= span_km * 0.002,
            label + " footprint edges measure the configured span on the sphere",
            "worst edge error " + str(round(error_km, 4)) + " km against span "
            + str(span_km) + " km",
        )

        # 5. boundary sampling density: dense enough to follow curvature.
        expected_samples = 4 * int(fixture["edge_samples"])
        report.check(
            len(description["boundary_units"]) == expected_samples,
            label + " samples its boundary at the configured density",
            str(len(description["boundary_units"])) + " != " + str(expected_samples),
        )
        spacing_km = aoi.boundary_sample_spacing_km(description)
        report.check(
            spacing_km <= span_km / AOI_MIN_SAMPLES_PER_EDGE_SPAN,
            label + " boundary samples are closely spaced relative to the footprint",
            str(round(spacing_km, 3)) + " km spacing on a " + str(span_km) + " km span",
        )
        # The number that actually decides "does the border detach from the
        # globe": how far a drawn chord falls beneath the arc it replaces.
        sagitta_km = aoi.max_chord_sagitta_km(description)
        report.check(
            sagitta_km <= AOI_MAX_SAGITTA_KM,
            label + " boundary chords stay within "
            + str(AOI_MAX_SAGITTA_KM) + " km of the true spherical arc",
            "worst sagitta " + str(round(sagitta_km, 6)) + " km",
        )

        # 6. interior conforms to the same sphere and carries a usable sweep space.
        grid = int(fixture["fill_grid"])
        rows = description["fill_rows"]
        report.check(
            len(rows) == grid + 1 and all(len(row) == grid + 1 for row in rows),
            label + " interior footprint is sampled on the configured grid",
            str(len(rows)) + " rows",
        )

        # 7. pre-data: nothing in the fixture names a scientific layer.
        forbidden_hits = sorted(
            {
                token
                for value in list(fixture.values()) + [fixture_id]
                if isinstance(value, str)
                for token in tokens(value) & FORBIDDEN_CACHE["classes"]
            }
        )
        report.check(
            not forbidden_hits,
            label + " declares no scientific layer vocabulary",
            repr(forbidden_hits),
        )

    # 8. fixtures must actually produce different geometry. Two fixtures that
    #    resolved to the same footprint would satisfy every check above while
    #    proving nothing about configurability.
    if len(descriptions) >= 2:
        ids = sorted(descriptions)
        first, second = descriptions[ids[0]], descriptions[ids[1]]
        moved_km = None
        dot = max(
            -1.0,
            min(1.0, sum(x * y for x, y in zip(first["center_unit"], second["center_unit"]))),
        )
        moved_km = math.acos(dot) * earth_radius_km
        report.check(
            moved_km > 100.0,
            "AOI fixtures resolve to genuinely different footprints",
            "centres only " + str(round(moved_km, 1)) + " km apart",
        )

    check_aoi_scene_wiring(report, scene_config, descriptions)


def check_aoi_scene_wiring(report: Report, scene_config, descriptions) -> None:
    """Every scene that renders an AOI must wire it to the AOI system.

    The point of these checks is that a beam endpoint must be *derived* from the
    AOI, never a coordinate that happens to match it today. A literal position
    anywhere in an aoi_system spec would survive the geometry checks above and
    then silently detach the moment the Earth rotated, so it fails here instead.
    """
    scenes = scene_config.get("scenes", {})
    aoi_scenes = []
    for scene_id in sorted(scenes):
        try:
            spec = hc.resolve_scene_spec(scene_id, scenes)
        except (KeyError, ValueError) as error:
            report.check(False, "scene " + scene_id + " resolves its inheritance", str(error))
            continue
        if any(obj.get("type") == "aoi_system" for obj in spec.get("objects", [])):
            aoi_scenes.append((scene_id, spec))

    report.check(bool(aoi_scenes), "at least one scene renders the AOI system")

    for scene_id, spec in aoi_scenes:
        label = "scene " + scene_id
        object_ids = {obj.get("id") for obj in spec.get("objects", [])}
        materials = set(spec.get("materials", {}))

        for obj in spec.get("objects", []):
            if obj.get("type") != "aoi_system":
                continue

            fixture_id = obj.get("fixture")
            report.check(
                fixture_id is None or fixture_id in descriptions,
                label + " AOI names a defined fixture",
                repr(fixture_id),
            )
            report.check(
                obj.get("parent_id") in object_ids,
                label + " AOI is parented to a scene object, so it rides the globe",
                repr(obj.get("parent_id")),
            )

            missing_materials = sorted(
                {
                    obj.get(key)
                    for key in (
                        "border_material",
                        "fill_material",
                        "corner_lock_material",
                        "beam_material",
                    )
                    if obj.get(key) and obj[key] not in materials
                }
            )
            report.check(
                not missing_materials,
                label + " AOI resolves every material it references",
                repr(missing_materials),
            )

            beams = obj.get("beams", {})
            if obj.get("beam_material") or beams:
                report.check(
                    beams.get("source_object_id") in object_ids,
                    label + " AOI beams originate at a real scene object",
                    repr(beams.get("source_object_id")),
                )
                report.check(
                    beams.get("target") in AOI_ALLOWED_BEAM_TARGETS,
                    label + " AOI beams target the AOI system, not a fixed point",
                    repr(beams.get("target")) + " not in " + repr(sorted(AOI_ALLOWED_BEAM_TARGETS)),
                )
            else:
                # WEB-005A R3: the analysis frame draws no sensing lines of its own -- it is the
                # frame the dive resolves onto, not a second acquisition.
                report.check(
                    True, label + " AOI " + str(obj.get("id")) + " is a frame without sensing lines",
                )

            literal = _literal_coordinates(obj)
            report.check(
                not literal,
                label + " AOI spec hard-codes no endpoint coordinates",
                "; ".join(literal),
            )

            ramps = _ramp_offenders(obj)
            report.check(
                not ramps,
                label + " AOI animation ramps are well-formed [frame, factor] pairs",
                "; ".join(ramps),
            )

            sweep = obj.get("sweep", {})
            report.check(
                int(sweep.get("end_frame", 0)) > int(sweep.get("start_frame", 0)),
                label + " AOI scan sweep declares a forward-travelling range",
                repr(sweep),
            )


# Keys whose lists are animation ramps -- [[frame, factor], ...] -- rather than geometry. They are
# exempt from the coordinate scan below but not unchecked: _ramp_offenders proves their shape, so
# the exemption cannot be used to smuggle a hand-typed position through a timing field.
# WEB-005A R3 adds "morph_keyframes": [frame, m] with m in 0..1 -- how far the persistent lock frame
# is from the true footprint. A presentation parameter of the fixture, never a position.
AOI_RAMP_KEYS = ("emphasis", "settle", "morph_keyframes", "weight_keyframes")
# Frame ranges -- [start, end] -- that a WEB-005A R3 frame may carry: the regional frame vanishes
# under the dive. Two integers, ordered; still never a position.
AOI_RANGE_KEYS = ("vanish", "morph_frames")


def _ramp_offenders(spec, path="aoi"):
    """Check that every animation ramp really is [[frame, factor], ...] and nothing else."""
    offenders = []
    if isinstance(spec, dict):
        for key, value in spec.items():
            where = path + "." + str(key)
            if key in AOI_RANGE_KEYS:
                ok_range = (
                    isinstance(value, list) and len(value) == 2
                    and all(isinstance(v, int) and not isinstance(v, bool) for v in value)
                    and 1 <= value[0] < value[1]
                )
                if not ok_range:
                    offenders.append(where + " is not an ordered [start, end] frame range: " + repr(value))
                continue
            if key not in AOI_RAMP_KEYS:
                offenders.extend(_ramp_offenders(value, where))
                continue
            if not isinstance(value, list) or not value:
                offenders.append(where + " is not a ramp: " + repr(value))
                continue
            for index, pair in enumerate(value):
                at = where + "[" + str(index) + "]"
                ok_shape = (
                    isinstance(pair, list) and len(pair) == 2
                    and isinstance(pair[0], int) and not isinstance(pair[0], bool)
                    and isinstance(pair[1], (int, float)) and not isinstance(pair[1], bool)
                )
                if not ok_shape:
                    offenders.append(at + " is not [frame, factor]: " + repr(pair))
                    continue
                frame, factor = pair
                if frame < 1:
                    offenders.append(at + " frame out of range: " + repr(frame))
                if not 0.0 <= float(factor) <= 8.0:
                    offenders.append(at + " factor out of range: " + repr(factor))
    return offenders


def _literal_coordinates(spec, path="aoi"):
    """Find numeric triples/lists in an AOI spec that look like baked geometry.

    An aoi_system spec should contain only scalars, frame numbers, names and animation ramps --
    its positions come from the fixture. A list of numbers in here is a
    coordinate someone typed, which is exactly the failure mode this phase is
    meant to eliminate. Ramp keys are skipped here because their pairs are frames and
    multipliers, never positions; ``_ramp_offenders`` proves that separately.
    """
    offenders = []
    if isinstance(spec, dict):
        for key, value in spec.items():
            if key in AOI_RAMP_KEYS or key in AOI_RANGE_KEYS:
                continue
            offenders.extend(_literal_coordinates(value, path + "." + str(key)))
    elif isinstance(spec, list):
        numeric = [item for item in spec if isinstance(item, (int, float))]
        if len(numeric) >= 2:
            offenders.append(path + " = " + repr(spec))
        else:
            for index, item in enumerate(spec):
                offenders.extend(_literal_coordinates(item, path + "[" + str(index) + "]"))
    return offenders


# The four scenes accepted at WEB-HERO-001D. They were accepted as pre-data and must stay that
# way even after WEB-005 opens the gate: a later phase may add a scene, never quietly reclassify
# one that Product already signed off as carrying no scientific layer.
ACCEPTED_PRE_DATA_SCENES = (
    "benchmark_neutral",
    "hero_earth_orbit",
    "hero_aoi_acquisition",
    "hero_predata_animatic",
)

# Every field a populated layer slot must carry before it may name accepted science. This is the
# WEB-005 replacement for "layer_slots must be empty": the gate is no longer emptiness, it is a
# complete, checkable provenance and presentation contract.
REQUIRED_LAYER_SLOT_FIELDS = (
    "id",
    "beat",
    "accepted_asset",
    "asset_class",
    "public_label",
    "mandatory_warning",
    "render_surface",
    "render_surface_reason",
    "delivered_file",
    "max_safe_rendered_px",
)

ALLOWED_DATA_STATES = ("pre_data", "accepted_data")
ALLOWED_FIXTURE_CLASSIFICATIONS = ("design_fixture", "production_regional_frame", "production_analysis_aoi")
ANALYSIS_AOI_SPAN_KM = 36.0


def check_pre_data_boundary(report: Report, scene_config, manifest) -> None:
    """The scientific boundary, in whichever state the lane is in.

    WEB-HERO-001A..D were pre-data: the check was simply that no scientific layer was named
    anywhere. WEB-005 is the authorized integration gate, so the question changes. It is no
    longer "is anything scientific named here" but "is everything scientific named here accepted,
    fully attributed, and rendered on a surface that cannot alter it".

    The pre-data guarantee does not disappear, it narrows: the four accepted scenes must still be
    clean, and a production scene may only reference accepted assets through a complete layer slot.
    """
    report.section("scientific data boundary")
    if not scene_config or not manifest:
        report.check(False, "scene configuration and manifest loaded")
        return

    forbidden = set(manifest.get("policy", {}).get("forbidden_layer_classes", []))
    FORBIDDEN_CACHE["classes"] = forbidden
    report.check(bool(forbidden), "a forbidden scientific layer vocabulary is declared")

    data_state = scene_config.get("data_state")
    report.check(
        data_state in ALLOWED_DATA_STATES,
        "scene configuration declares a known data state",
        repr(data_state),
    )
    pre_data = data_state == "pre_data"

    # The accepted scenes are scanned in every state; a scene added later is scanned only while
    # the lane is still pre-data, because after the gate it is allowed to name accepted science.
    scenes = scene_config.get("scenes", {})
    identifiers = []
    for scene_id, spec in scenes.items():
        if not pre_data and scene_id not in ACCEPTED_PRE_DATA_SCENES:
            continue
        identifiers.append(("scene id", scene_id))
        for obj in spec.get("objects", []):
            identifiers.append(("object id", obj.get("id", "")))
        for name in spec.get("materials", {}):
            identifiers.append(("material", name))
        for light in spec.get("lights", []):
            identifiers.append(("light id", light.get("id", "")))

    interface = scene_config.get("aoi_injection_interface", {})
    if pre_data:
        for slot in interface.get("layer_slots", []):
            identifiers.append(("aoi layer slot", json.dumps(slot)))

    for asset in manifest.get("assets", []):
        for field in ("id", "role", "layer_class", "local_path"):
            if asset.get(field):
                identifiers.append(("asset " + field, asset[field]))

    hits = [
        (kind, value, sorted(tokens(value) & forbidden))
        for kind, value in identifiers
        if tokens(value) & forbidden
    ]
    report.check(
        not hits,
        "the accepted pre-data scenes still declare no scientific layer",
        "; ".join(k + " " + repr(v) + " matches " + repr(m) for k, v, m in hits),
    )

    missing_accepted = [s for s in ACCEPTED_PRE_DATA_SCENES if s not in scenes]
    report.check(
        not missing_accepted,
        "every scene accepted at WEB-HERO-001D is still present",
        repr(missing_accepted),
    )

    fixtures = interface.get("fixtures", {})
    if pre_data:
        report.check(
            not interface.get("layer_slots"),
            "the AOI interface declares no populated layer slot while pre-data",
        )
        report.check(
            interface.get("classification") == "design_fixture",
            "AOI placeholder geometry is classified as a design fixture",
            repr(interface.get("classification")),
        )
    else:
        # WEB-005 gate. Both accepted design fixtures must survive unreclassified, so the
        # configurability proof from Phase C still stands on placeholders rather than on real
        # geometry that happens to differ.
        for fixture_id in ("design_primary", "design_secondary"):
            spec = fixtures.get(fixture_id, {})
            report.check(
                spec.get("classification") == "design_fixture",
                "accepted fixture " + fixture_id + " is still classified a design fixture",
                repr(spec.get("classification")),
            )
        unknown = sorted(
            fid for fid, spec in fixtures.items()
            if spec.get("classification") not in ALLOWED_FIXTURE_CLASSIFICATIONS
        )
        report.check(
            not unknown,
            "every AOI fixture declares a known classification",
            repr(unknown),
        )
        # A production framing extent is not the analysis AOI, and must never be published as
        # one: the hero frames a region, the accepted score covers 36 x 36 km inside it.
        for fixture_id, spec in sorted(fixtures.items()):
            if spec.get("classification") != "production_regional_frame":
                continue
            label = "production fixture " + fixture_id
            report.check(
                spec.get("is_analysis_aoi") is False,
                label + " explicitly disclaims being the analysis AOI",
                repr(spec.get("is_analysis_aoi")),
            )
            report.check(
                bool(spec.get("geometry_source")) and bool(spec.get("centre_provenance")),
                label + " records where its real geometry came from",
            )
        # WEB-005A R3: the analysis AOI may be drawn as a frame, and only as the accepted one --
        # the accepted 36 x 36 km extent on the accepted centre, declared as what it is.
        regional = next(
            (s for s in fixtures.values() if s.get("classification") == "production_regional_frame"), {}
        )
        for fixture_id, spec in sorted(fixtures.items()):
            if spec.get("classification") != "production_analysis_aoi":
                continue
            label = "analysis fixture " + fixture_id
            report.check(
                spec.get("is_analysis_aoi") is True,
                label + " declares itself the analysis AOI",
                repr(spec.get("is_analysis_aoi")),
            )
            report.check(
                abs(float(spec.get("span_km", 0.0)) - ANALYSIS_AOI_SPAN_KM) < 1e-9,
                label + " spans exactly the accepted 36 km analysis extent",
                repr(spec.get("span_km")),
            )
            report.check(
                bool(regional)
                and abs(float(spec.get("center_lat_deg", 0.0)) - float(regional.get("center_lat_deg", 1.0))) < 1e-9
                and abs(float(spec.get("center_lon_deg", 0.0)) - float(regional.get("center_lon_deg", 1.0))) < 1e-9,
                label + " sits on the same accepted centre as the regional frame",
            )
            report.check(
                bool(spec.get("geometry_source")) and bool(spec.get("centre_provenance")),
                label + " records where its geometry came from",
            )
            report.check(
                abs(float(spec.get("bearing_deg", 0.0))) <= 2.0 and bool(spec.get("bearing_note")),
                label + " bearing is a documented grid-convergence registration, not a re-orientation",
                repr(spec.get("bearing_deg")),
            )

        slots = interface.get("layer_slots", [])
        report.check(bool(slots), "the AOI interface declares the accepted handoff layer slots")
        for index, slot in enumerate(slots):
            label = "layer slot " + repr(slot.get("id", index))
            missing = [f for f in REQUIRED_LAYER_SLOT_FIELDS if not slot.get(f)]
            report.check(
                not missing,
                label + " carries the full provenance and presentation contract",
                "missing " + repr(missing),
            )
            report.check(
                str(slot.get("accepted_asset", "")).startswith("geo_web_002."),
                label + " names an accepted GEO-WEB-002 asset",
                repr(slot.get("accepted_asset")),
            )
            # The core WEB-005 science guarantee. A governed raster that is baked into a video
            # frame has been through chroma subsampling and quantisation, which is exactly the
            # colour/value change the package forbids. Declaring the surface makes that checkable
            # instead of a matter of trust.
            report.check(
                slot.get("render_surface") == "html_overlay",
                label + " is composited in the page, never baked into a rendered frame",
                repr(slot.get("render_surface")),
            )
            delivered = str(slot.get("delivered_file", ""))
            report.check(
                bool(delivered) and (hc.REPO_ROOT / delivered).exists(),
                label + " delivers a file that exists in the repository",
                repr(delivered),
            )


def check_continuous_sequence(report: Report, scene_config) -> None:
    """WEB-HERO-001D: the pre-data animatic must be one continuous shot.

    Everything here is a *structural* claim that can be settled from
    configuration alone, without Blender and without rendering. The visual
    claims -- does the move feel premium, does the limb read as air -- belong
    to the stills and the animatic, and the numerical motion claims belong to
    ``audit_shot.py``, which measures the evaluated camera.

    What configuration can prove is that the shot is not secretly two shots:
    one scene, one AOI system present across the whole range, one monotonic
    camera path, and beats that are actually ordered the way the narrative
    claims.
    """
    report.section("continuous pre-data sequence")
    scenes = (scene_config or {}).get("scenes", {})
    animatic_ids = [
        scene_id
        for scene_id, spec in scenes.items()
        if spec.get("role") == "hero_predata_animatic"
    ]
    if not animatic_ids:
        return

    for scene_id in sorted(animatic_ids):
        spec = hc.resolve_scene_spec(scene_id, scenes)
        label = "scene " + scene_id + " "

        animation = spec.get("animation", {})
        start = int(animation.get("frame_start", 0))
        end = int(animation.get("frame_end", 0))
        rate = int(animation.get("frame_rate", 0))
        duration = (end - start + 1) / rate if rate else 0.0
        report.check(
            end > start and rate > 0,
            label + "declares a frame range and rate",
            "start " + str(start) + " end " + str(end) + " rate " + str(rate),
        )
        # The task envelope: the pre-data portion has to fit inside an
        # approximately 8-12 second complete hero without forcing rushed
        # motion, and has to leave the later layer reveal somewhere to live.
        report.check(
            6.0 <= duration <= 12.0,
            label + "duration fits the hero envelope",
            str(round(duration, 3)) + " s",
        )

        # One AOI system, present for the whole range. Two would be a cut
        # dressed up as a move.
        aoi_objects = [o for o in spec.get("objects", []) if o.get("type") == "aoi_system"]
        report.check(
            len(aoi_objects) == 1,
            label + "carries exactly one AOI system",
            str(len(aoi_objects)) + " found",
        )

        beats = animation.get("beats", {})
        # Narrative order, which is the order the beats must *start* in. The
        # approach begins while acquisition is still resolving and runs under
        # the scan, so these overlap heavily; only their starts are ordered.
        required_beats = (
            "earth_establish",
            "satellite_entrance",
            "aoi_acquisition",
            "camera_approach",
            "scan_sweep",
            "regional_hold",
        )
        missing = [beat for beat in required_beats if beat not in beats]
        report.check(
            not missing,
            label + "declares the full narrative beat map",
            "missing " + repr(missing),
        )

        if not missing:
            ordered = all(
                beats[a][0] <= beats[b][0]
                for a, b in zip(required_beats, required_beats[1:])
            )
            report.check(ordered, label + "beats start in narrative order")
            in_range = all(
                start <= beats[beat][0] <= beats[beat][1] <= end for beat in required_beats
            )
            report.check(in_range, label + "every beat lies inside the frame range")
            # A hold that is shorter than this is a stop, not a hold: the later
            # phase has to be able to reveal real layers into it.
            hold = beats["regional_hold"]
            hold_seconds = (hold[1] - hold[0]) / rate if rate else 0.0
            report.check(
                hold_seconds >= 1.0,
                label + "ends on a regional hold long enough to receive data",
                str(round(hold_seconds, 3)) + " s",
            )
            # Overlapping establish and approach is what makes it one move
            # rather than two shots joined end to end.
            report.check(
                beats["camera_approach"][0] <= beats["earth_establish"][1],
                label + "camera approach begins before the establish ends",
            )

        camera = spec.get("camera", {})
        keyframes = sorted(camera.get("keyframes", []), key=lambda k: int(k["frame"]))
        report.check(
            len(keyframes) >= 4, label + "authors a multi-keyframe camera path"
        )
        if keyframes:
            report.check(
                int(keyframes[0]["frame"]) == start and int(keyframes[-1]["frame"]) == end,
                label + "camera path spans the whole frame range",
            )
            radii = [
                math.sqrt(sum(component * component for component in k["location"]))
                for k in keyframes
            ]
            report.check(
                all(b <= a + 1e-9 for a, b in zip(radii, radii[1:])),
                label + "camera closes monotonically, never backing off",
                "radii " + repr([round(r, 3) for r in radii]),
            )
            # Focal length is checked only from the AOI handover onward. The
            # establish before it replays accepted Phase-B camera states
            # verbatim, and those ease the lens back once (35 mm to 33 mm) as
            # part of a move Product already accepted; re-authoring them to
            # satisfy a checker here would change accepted work. That the lens
            # never *snaps* anywhere in the shot is a rate question, and
            # audit_shot.py measures it on the evaluated camera.
            handover = min(
                (
                    int(k["frame"])
                    for k in camera.get("track", {}).get("influence_keyframes", [])
                    if float(k["value"]) >= 1.0
                ),
                default=start,
            )
            lenses = [
                float(k["focal_length_mm"]) for k in keyframes if int(k["frame"]) >= handover
            ]
            report.check(
                all(b >= a - 1e-9 for a, b in zip(lenses, lenses[1:])),
                label + "focal length never reverses during the approach",
                "lenses from frame " + str(handover) + " " + repr(lenses),
            )

        # Intent and authored keyframes must agree, or the committed path is no
        # longer the one the shot plan describes and the derivation is a story.
        intent = camera.get("shot_intent")
        report.check(bool(intent), label + "records the shot intent it was derived from")
        if intent and keyframes:
            derived = shot_plan.derive(scene_config, scene_id)
            drift = 0.0
            for authored, expected in zip(keyframes, derived):
                if int(authored["frame"]) != int(expected["frame"]):
                    drift = float("inf")
                    break
                for a, b in zip(authored["location"], expected["location"]):
                    drift = max(drift, abs(float(a) - float(b)))
                for a, b in zip(authored["look_at"], expected["look_at"]):
                    drift = max(drift, abs(float(a) - float(b)))
            report.check(
                drift <= 1.0e-3,
                label + "authored camera keyframes match their derivation",
                "worst component drift " + str(drift) + " BU",
            )

        composition = camera.get("composition", {})
        region = composition.get("headline_safe_region")
        report.check(
            isinstance(region, dict),
            label + "reserves a headline-safe region for later HTML copy",
        )
        if isinstance(region, dict) and keyframes:
            through = int(composition.get("headline_safe_through_frame", start))
            defaults = scene_config.get("camera_defaults", {})
            sensor = float(defaults.get("sensor_width_mm", 36.0))
            radius_bu = aoi.earth_radius_km(scene_config) / aoi.KM_PER_BLENDER_UNIT
            worst = 0.0
            for keyframe in keyframes:
                if int(keyframe["frame"]) > through:
                    continue
                metrics = shot_plan._headline_safe_metrics(
                    tuple(keyframe["location"]), tuple(keyframe["look_at"]),
                    float(keyframe["focal_length_mm"]), radius_bu, sensor,
                    (1920, 1080), region,
                )
                worst = max(worst, metrics["occupancy"])
            report.check(
                worst == 0.0,
                label + "keeps the headline-safe region clear of the Earth",
                "worst occupancy " + str(worst),
            )

        # An atmosphere refined for this phase must not have been refined into
        # an occluder: the whole point of the additive limb profile is that air
        # adds light rather than painting over what is behind it.
        for name, material in spec.get("materials", {}).items():
            if material.get("type") != "atmosphere_shell":
                continue
            if not material.get("profile"):
                continue
            report.check(
                material["profile"] in ("limb_airmass", "soft_band"),
                label + "atmosphere " + name + " uses a known limb profile",
                repr(material["profile"]),
            )
            if material["profile"] == "limb_airmass":
                height = float(material.get("scale_height_km", 55.0))
                report.check(
                    5.0 <= height <= 200.0,
                    label + "atmosphere " + name + " has a physical scale height",
                    str(height) + " km",
                )
                shell = next(
                    (
                        o for o in spec.get("objects", [])
                        if o.get("material") == name and o.get("radius")
                    ),
                    None,
                )
                if shell:
                    radius_km = aoi.earth_radius_km(scene_config)
                    headroom_km = float(shell["radius"]) * aoi.KM_PER_BLENDER_UNIT - radius_km
                    # Below a few scale heights the exponential has not decayed
                    # and the shell silhouette becomes a visible edge again --
                    # the exact defect this phase removed.
                    report.check(
                        headroom_km >= 5.0 * height,
                        label + "atmosphere " + name + " shell clears its own falloff",
                        str(round(headroom_km, 1)) + " km headroom vs "
                        + str(round(5.0 * height, 1)) + " km needed",
                    )


# WEB-005A R2 sensing-FX envelope (A-HERO-04). The core line must be thin enough never to read as
# a slab and opaque enough to be legible at review size; the glow sheath must stay a sheath.
FX_MAX_CORE_TIP_RADIUS_KM = 8.0
FX_MIN_CORE_ROOT_ALPHA = 0.6
FX_MIN_CORE_TIP_ALPHA = 0.35
FX_MIN_CORE_EMISSION = 3.0
FX_MAX_GLOW_ROOT_ALPHA = 0.3
FX_MAX_CONE_TIP_ALPHA = 0.06
# Sensing lines are attention, not physics: no copy anywhere in the hero configuration may claim
# an instrument. Tokens are matched whole, lower-cased.
SENSOR_PHYSICS_CLAIMS = {
    "radar", "lidar", "sar", "hyperspectral", "multispectral", "spectrometer", "swath",
    "wavelength", "backscatter", "radiometer", "microwave", "thermal-infrared", "resolution-m",
}


def check_r2_visual_contract(report: Report, scene_config, manifest) -> None:
    """WEB-005A R2: derived orbit, readable satellite, legible-but-restrained sensing FX, lock event.

    Like the camera, the satellite's committed keyframes must match their intent; like the AOI, the
    acquisition FX must sit inside a checkable envelope; and the production scene must actually
    carry the elements the R2 lock names -- a volumetric satellite type, a border halo, a lock
    draw-in, a lock pulse -- rather than the accepted placeholders. Whether it *looks* right is
    decided by the stills and the audit; what configuration can prove is checked here.
    """
    report.section("WEB-005A R2 visual-fidelity contract")
    scenes = (scene_config or {}).get("scenes", {})
    production = [sid for sid, spec in scenes.items() if spec.get("role") == "hero_production"]
    if not production:
        report.check(False, "a production hero scene exists")
        return
    for scene_id in sorted(production):
        spec = hc.resolve_scene_spec(scene_id, scenes)
        label = "scene " + scene_id + " "
        objects = {o.get("id"): o for o in spec.get("objects", [])}
        materials = spec.get("materials", {})

        # --- satellite: volumetric type, derived orbit, readability gates ---------------------
        satellite = objects.get("satellite", {})
        report.check(
            satellite.get("type") == "eo_satellite",
            label + "satellite is the volumetric generic EO platform, not the accepted placeholder",
            repr(satellite.get("type")),
        )
        intent = satellite.get("orbit_intent")
        report.check(bool(intent), label + "satellite pass is stated as an orbit intent")
        if intent:
            try:
                derived = orbit_plan.derive(scene_config, scene_id)
                committed = sorted(satellite.get("location_keyframes", []), key=lambda k: int(k["frame"]))
                drift = 0.0
                if len(derived) != len(committed):
                    drift = float("inf")
                else:
                    for a, b in zip(committed, derived):
                        if int(a["frame"]) != int(b["frame"]):
                            drift = float("inf")
                            break
                        for x, y in zip(a["location"], b["location"]):
                            drift = max(drift, abs(float(x) - float(y)))
                report.check(
                    drift <= 1.0e-3,
                    label + "committed satellite keyframes match their orbit derivation",
                    "worst component drift " + str(drift) + " BU",
                )
                radius_bu = orbit_plan.orbit_basis(scene_config, spec, intent)[2]
                radii = [
                    math.sqrt(sum(float(c) * float(c) for c in k["location"]))
                    for k in satellite.get("location_keyframes", [])
                ]
                report.check(
                    bool(radii) and max(abs(r - radius_bu) for r in radii) <= 1.0e-3,
                    label + "every satellite keyframe lies on one circular orbit",
                    "radii " + repr([round(r, 4) for r in radii[:6]]) + " vs " + str(round(radius_bu, 4)),
                )
                altitude = float(intent.get("altitude_km", 0.0))
                report.check(
                    300.0 <= altitude <= 1200.0,
                    label + "orbit altitude is a low-Earth EO altitude",
                    str(altitude) + " km",
                )
            except (KeyError, ValueError, SystemExit) as error:
                report.check(False, label + "orbit intent derives", str(error))
        readability = spec.get("camera", {}).get("composition", {}).get("satellite_readability", {})
        report.check(
            0.05 <= float(readability.get("min_width_fraction", 0.0)) <= 0.15
            and 0.15 <= float(readability.get("max_width_fraction", 1.0)) <= 0.3,
            label + "declares satellite readability bounds the shot audit enforces",
            repr(readability),
        )
        report.check(
            bool(spec.get("camera", {}).get("composition", {}).get("acquisition_beat")),
            label + "declares the acquisition beat the shot audit gates",
        )
        report.check(
            bool(spec.get("lighting_isolation")),
            label + "isolates satellite lighting so a hero-scale body never shadows the planet",
        )
        for token in ("specific", "landsat", "sentinel", "worldview", "spot", "pleiades", "terrasar", "modis"):
            pass
        identity = [
            key for key, value in satellite.items()
            if isinstance(value, str) and any(
                name in value.lower() for name in ("landsat", "sentinel", "worldview", "pleiades", "terrasar", "spot ", "modis", "viirs")
            )
        ]
        report.check(
            not identity,
            label + "satellite spec claims no specific operational spacecraft or sensor",
            repr(identity),
        )

        # --- sensing FX envelope -------------------------------------------------------------
        aoi_spec = next((o for o in spec.get("objects", []) if o.get("type") == "aoi_system"), {})
        beams = aoi_spec.get("beams", {})
        core = materials.get(aoi_spec.get("beam_material"), {})
        report.check(
            beams.get("target") == "corners",
            label + "sensing lines target the footprint corners (a frustum, not one cone)",
            repr(beams.get("target")),
        )
        report.check(
            float(beams.get("tip_radius_km", 99.0)) <= FX_MAX_CORE_TIP_RADIUS_KM
            and float(beams.get("root_radius_km", 99.0)) <= FX_MAX_CORE_TIP_RADIUS_KM,
            label + "sensing-line core is thin (no slab)",
            "radii " + str(beams.get("root_radius_km")) + " -> " + str(beams.get("tip_radius_km")) + " km",
        )
        report.check(
            float(core.get("root_alpha", 0.0)) >= FX_MIN_CORE_ROOT_ALPHA
            and float(core.get("tip_alpha", 0.0)) >= FX_MIN_CORE_TIP_ALPHA
            and float(core.get("emission_strength", 0.0)) >= FX_MIN_CORE_EMISSION,
            label + "sensing-line core is legible (alpha and emission above the floor)",
            "root " + str(core.get("root_alpha")) + " tip " + str(core.get("tip_alpha"))
            + " emission " + str(core.get("emission_strength")),
        )
        glow = materials.get(beams.get("glow_material"), {})
        report.check(
            bool(glow) and float(glow.get("root_alpha", 1.0)) <= FX_MAX_GLOW_ROOT_ALPHA,
            label + "sensing-line glow is a sheath, not a second slab",
            repr(glow.get("root_alpha")),
        )
        cone = materials.get((beams.get("cone") or {}).get("material"), {})
        report.check(
            not beams.get("cone") or float(cone.get("tip_alpha", 1.0)) <= FX_MAX_CONE_TIP_ALPHA,
            label + "support cone stays secondary",
            repr(cone.get("tip_alpha")),
        )
        for ref in ("beam_core", "beam_glow", "aoi_frame"):
            report.check(ref in scene_config.get("palette", {}), label + "palette carries the R2 FX colour " + ref)
        # The R2 FX lock, or the restrained scan cyan / teal Product accepted through the R3 preview
        # gates after the R2 colours rendered near-white (b9579ef section 6).
        report.check(
            (core.get("emission_color_ref"), glow.get("emission_color_ref"))
            in (("beam_core", "beam_glow"), ("scan_cyan", "scan_teal")),
            label + "sensing lines use an accepted core/glow colour pair",
            repr((core.get("emission_color_ref"), glow.get("emission_color_ref"))),
        )

        # --- lock event ------------------------------------------------------------------
        border_cfg = aoi_spec.get("border", {})
        lock_cfg = aoi_spec.get("corner_locks", {})
        report.check(
            bool(aoi_spec.get("border_glow")) and materials.get(aoi_spec["border_glow"].get("material"), {}).get("type") == "aoi_glow_ribbon",
            label + "target frame carries a controlled halo ribbon",
        )
        emphasis = border_cfg.get("emphasis", [])
        peak = max((float(f) for _, f in emphasis), default=1.0)
        report.check(
            peak >= 1.8,
            label + "target frame has a visible lock intensification",
            "peak emphasis " + str(peak),
        )
        report.check(
            "draw_start_frame" in lock_cfg and "draw_end_frame" in lock_cfg
            and materials.get(aoi_spec.get("corner_lock_material"), {}).get("type") == "aoi_lock_draw",
            label + "corner locks draw into place",
        )
        beat = spec.get("camera", {}).get("composition", {}).get("acquisition_beat") or [0, 0]
        pulse_frame = aoi_spec.get("lock_pulse_frame")
        if isinstance(pulse_frame, int):
            # Accepted R3 order (Product review of preview gate 2): the target resolves first so it
            # never "appears afterwards"; the lock is the pulse after the lines have landed.
            report.check(
                int(beat[0]) <= pulse_frame <= int(beat[1]),
                label + "lock event lands inside the acquisition beat",
                "pulse at " + str(pulse_frame) + " beat " + repr(beat),
            )
            report.check(
                int(beams.get("appear_end_frame", 999)) <= pulse_frame,
                label + "sensing lines connect before the frame locks",
            )
        else:
            report.check(
                int(beat[0]) <= int(lock_cfg.get("draw_start_frame", -1)) <= int(beat[1]),
                label + "lock event lands inside the acquisition beat",
                "draw at " + str(lock_cfg.get("draw_start_frame")) + " beat " + repr(beat),
            )
            report.check(
                int(beams.get("appear_start_frame", 999)) <= int(lock_cfg.get("draw_start_frame", 0)),
                label + "sensing lines connect before the frame locks",
            )

        # --- no sensor-physics claim anywhere in the production configuration --------------
        text_blobs = [json.dumps(spec)]
        found = sorted(
            token for token in SENSOR_PHYSICS_CLAIMS
            if re.search(r"(?<![a-z0-9-])" + re.escape(token) + r"(?![a-z0-9-])", " ".join(text_blobs).lower())
        )
        report.check(not found, label + "makes no sensing-physics claim", repr(found))

        # --- Earth albedo provenance (A-HERO-11) -------------------------------------------
        earth = materials.get("earth_surface", {})
        assets = {a.get("local_path", "").split("/")[-1]: a for a in (manifest or {}).get("assets", [])}
        for key in ("day_texture", "detail_texture", "cloud_texture", "night_texture"):
            filename = earth.get(key)
            if not filename:
                continue
            asset = assets.get(filename)
            report.check(
                asset is not None and asset.get("rights_status") == "cleared" and bool(HEX64.match(str(asset.get("sha256", "")))),
                label + "Earth " + key + " is a cleared, checksummed manifest asset",
                repr(filename),
            )
            if asset is not None:
                path = hc.REPO_ROOT / asset["local_path"]
                report.check(
                    path.is_file() and hc.sha256_file(path) == asset["sha256"],
                    label + "Earth " + key + " on disk matches its recorded SHA-256",
                    repr(filename),
                )
        window = earth.get("detail_window")
        if window and earth.get("detail_texture"):
            asset = assets.get(earth["detail_texture"], {})
            recorded = asset.get("window", {})
            report.check(
                all(abs(float(window[k]) - float(recorded.get(k, 1e9))) < 1e-6 for k in ("lon0", "lon1", "lat0", "lat1")),
                label + "detail window in the material matches the crop's recorded window",
                repr(window) + " vs " + repr(recorded),
            )
            fixture = aoi.resolve_fixture(scene_config, aoi_spec.get("fixture"))
            report.check(
                float(window["lon0"]) < float(fixture["center_lon_deg"]) < float(window["lon1"])
                and float(window["lat0"]) < float(fixture["center_lat_deg"]) < float(window["lat1"]),
                label + "detail window contains the accepted target centre",
            )
            report.check(
                bool(asset.get("derived_from")) and asset.get("derived_from") in {a.get("id") for a in (manifest or {}).get("assets", [])},
                label + "detail crop records the manifest asset it was cut from",
                repr(asset.get("derived_from")),
            )

        # --- WEB-005A R3: settled pass, analysis frame, dive and hold, detail multiplier ---------
        _check_r3_contract(report, scene_config, spec, label, manifest, assets, aoi_spec, beams, intent)


def _check_r3_contract(report, scene_config, spec, label, manifest, assets, aoi_spec, beams, intent):
    """WEB-005A R3: what configuration can prove about the re-reviewed visual outcome.

    The satellite must *settle* (a time-remapped pass whose slow section holds the acquisition
    composition), the lines must release before the dive, the accepted analysis AOI must be drawn
    as the frame the dive resolves onto -- with its own lock event, after the regional frame has
    been told to vanish -- and the hold must frame that AOI at a size the page can register the
    governed rasters into without breaching their ceiling. The detail multiplier under the hold
    must be a cleared, checksummed manifest asset whose window contains the target.
    """
    objects = {o.get("id"): o for o in spec.get("objects", [])}
    materials = spec.get("materials", {})
    interface = scene_config.get("aoi_injection_interface", {})
    fixtures = interface.get("fixtures", {})

    # settled pass
    profile = (intent or {}).get("rate_profile")
    report.check(bool(profile), label + "satellite pass is time-remapped (rate_profile)")
    if profile:
        rates = [float(r) for _, r in profile]
        report.check(min(rates) > 0.0, label + "orbit never stops or reverses", repr(rates))
        report.check(
            min(rates) <= 0.35 * max(rates),
            label + "pass has a settled section at most 35 percent of its fastest rate",
            "rates " + repr(rates),
        )
        beat = spec.get("camera", {}).get("composition", {}).get("acquisition_beat") or [0, 0]
        slow_frames = [float(f) for f, r in profile if float(r) <= 0.35 * max(rates)]
        report.check(
            bool(slow_frames) and min(slow_frames) <= int(beat[0]) + 12 and max(slow_frames) >= int(beat[1]),
            label + "settled section covers the acquisition beat",
            "slow at " + repr(slow_frames) + " beat " + repr(beat),
        )

    # lines release before the dive, while the satellite still has the beat
    beat = spec.get("camera", {}).get("composition", {}).get("acquisition_beat") or [0, 0]
    report.check(
        int(beams.get("release_end_frame", 0)) <= int(beat[1]),
        label + "sensing lines release inside the acquisition beat (satellite still in frame)",
        "release ends " + str(beams.get("release_end_frame")) + " beat " + repr(beat),
    )

    # the analysis frame
    analysis_objects = [
        o for o in spec.get("objects", [])
        if o.get("type") == "aoi_system"
        and fixtures.get(o.get("fixture"), {}).get("classification") == "production_analysis_aoi"
    ]
    report.check(len(analysis_objects) == 1, label + "draws exactly one analysis AOI frame", str(len(analysis_objects)))
    hold = spec.get("camera", {}).get("composition", {}).get("analysis_hold", {})
    report.check(
        bool(hold) and isinstance(hold.get("width_fraction"), list) and len(hold["width_fraction"]) == 2
        and 0.15 <= float(hold["width_fraction"][0]) < float(hold["width_fraction"][1]) <= 0.30,
        label + "declares the analysis hold the audit gates (width fraction 0.15-0.30)",
        repr(hold),
    )
    if analysis_objects:
        frame = analysis_objects[0]
        report.check(
            hold.get("fixture") == frame.get("fixture"),
            label + "analysis hold names the analysis frame's fixture",
        )
        border = frame.get("border", {})
        locks = frame.get("corner_locks", {})
        # 946cd8b / c7c6cb1: one visually persistent adaptive lock presentation replaced the regional
        # frame that vanished and the analysis frame that appeared. With a presentation block the
        # acquired frame IS the analysis frame, so the three rules that kept the pair apart do not
        # apply; what replaces them is the preview-gate contract below, which runs on this scene too.
        persistent = bool(frame.get("presentation"))
        report.check(
            persistent or int(border.get("appear_start_frame", 0)) >= int(beams.get("release_end_frame", 999)),
            label + "analysis frame appears only after the sensing lines have released, or is the one persistent reticle",
            "appears " + str(border.get("appear_start_frame")) + " release ends " + str(beams.get("release_end_frame")),
        )
        peak = max((float(f) for _, f in border.get("emphasis", [])), default=1.0)
        report.check(peak >= 1.8, label + "analysis frame has its own lock intensification", "peak " + str(peak))
        report.check(
            "draw_start_frame" in locks and "draw_end_frame" in locks
            and materials.get(frame.get("corner_lock_material"), {}).get("type") == "aoi_lock_draw",
            label + "analysis frame corner locks draw into place",
        )
        report.check(
            int(locks.get("draw_end_frame", 999)) <= int(hold.get("frame", 0)),
            label + "analysis frame locks land before the hold",
        )
        aoi_systems = [o for o in spec.get("objects", []) if o.get("type") == "aoi_system"]
        report.check(
            (persistent and len(aoi_systems) == 1) or (not frame.get("beam_material") and not frame.get("beams")),
            label + "there is one acquisition: a single persistent reticle, or an analysis frame with no lines of its own",
        )
        vanish = aoi_spec.get("border", {}).get("vanish")
        report.check(
            persistent or (bool(vanish) and int(vanish[1]) <= int(hold.get("frame", 0))
                           and int(vanish[0]) >= int(beams.get("release_end_frame", 999))),
            label + "regional frame vanishes under the dive, or there is no separate regional frame",
            repr(vanish),
        )
        # Blender-free re-derivation of the hold framing from the committed camera keyframes.
        try:
            camera_spec = spec.get("camera", {})
            defaults = scene_config.get("camera_defaults", {})
            sensor = float(defaults.get("sensor_width_mm", 36.0))
            description = aoi.describe(scene_config, frame.get("fixture"), spec)
            last = sorted(camera_spec.get("keyframes", []), key=lambda k: int(k["frame"]))[-1]
            camera, look_at, lens, shift = orbit_plan.camera_state(camera_spec, int(last["frame"]))
            rotation = shot_plan.earth_rotation_deg(spec, int(last["frame"]))
            corners = [
                orbit_plan.project_shifted(shot_plan._rotate_z(c, rotation), camera, look_at, lens, sensor,
                                           (1920, 1080), shift)
                for c in description["corner_positions_bu"]
            ]
            xs = [c["x"] for c in corners]
            width = max(xs) - min(xs) if all(x is not None for x in xs) else None
            lo, hi = (float(v) for v in hold.get("width_fraction", [0, 0]))
            report.check(
                width is not None and lo <= width <= hi,
                label + "committed camera frames the analysis AOI inside the declared hold width",
                "width " + repr(width) + " bounds " + repr((lo, hi)),
            )
            centre = orbit_plan.project_shifted(
                shot_plan._rotate_z(description["center_position_bu"], rotation), camera, look_at, lens, sensor,
                (1920, 1080), shift)
            report.check(
                centre["x"] is not None and 0.45 <= centre["x"] <= 0.78 and 0.35 <= centre["y"] <= 0.72,
                label + "analysis AOI lands right of centre with room for the page-layer caption",
                repr((centre["x"], centre["y"])),
            )
        except (KeyError, ValueError, IndexError) as error:
            report.check(False, label + "hold framing re-derives from configuration", str(error))

    # detail multiplier under the hold
    earth = materials.get("earth_surface", {})
    sharpen = earth.get("detail_sharpen")
    report.check(bool(sharpen), label + "Earth carries a regional detail multiplier under the hold")
    if sharpen:
        asset = assets.get(str(sharpen.get("texture", "")))
        report.check(
            asset is not None and asset.get("rights_status") == "cleared" and bool(HEX64.match(str(asset.get("sha256", "")))),
            label + "detail multiplier is a cleared, checksummed manifest asset",
            repr(sharpen.get("texture")),
        )
        if asset is not None:
            path = hc.REPO_ROOT / asset["local_path"]
            report.check(
                path.is_file() and hc.sha256_file(path) == asset["sha256"],
                label + "detail multiplier on disk matches its recorded SHA-256",
            )
            recorded = asset.get("window", {})
            window = sharpen.get("window", {})
            report.check(
                all(abs(float(window.get(k, 1e9)) - float(recorded.get(k, -1e9))) < 1e-6 for k in ("lon0", "lon1", "lat0", "lat1")),
                label + "detail multiplier window in the material matches the manifest record",
                repr(window) + " vs " + repr(recorded),
            )
            report.check(
                bool(asset.get("attribution")) and "Copernicus" in str(asset.get("attribution")),
                label + "detail multiplier carries the Copernicus attribution it requires",
            )
        fixture = aoi.resolve_fixture(scene_config, aoi_spec.get("fixture"))
        window = sharpen.get("window", {})
        report.check(
            float(window.get("lon0", 1e9)) < float(fixture["center_lon_deg"]) < float(window.get("lon1", -1e9))
            and float(window.get("lat0", 1e9)) < float(fixture["center_lat_deg"]) < float(window.get("lat1", -1e9)),
            label + "detail multiplier window contains the accepted target centre",
        )
        report.check(
            0.0 < float(sharpen.get("strength", 0.0)) <= 1.2,
            label + "detail multiplier strength stays a structure gain, not a re-colour",
            repr(sharpen.get("strength")),
        )


def check_r3_preview_gate(report: Report, scene_config) -> None:
    """WEB-005A R3 preview gate: what configuration can prove about the fixed-camera revision.

    Authority: docs/web-005-polish-authority@473b48a (review disposition) over 946cd8b and db4605a,
    as amended by c7c6cb1 (Product decision on the first preview) and the Product clarifications of
    2026-09-18: true-corner line anchors, a reticle that is separate from the true outline, the
    settle -> aim -> draw-on -> lock -> sweep -> retire -> approach order, thinner line language,
    a cyan / teal scan palette, a bounded platform exit and the approved timing envelope.

    Third preview. Product's human visual review of the second preview found that four lines onto
    the true 36 km footprint read as "beams go toward the middle, then the AOI appears", and
    overrode c7c6cb1 section 2 for the *visible* acquisition (chat, 2026-09-18): the four lines land
    on the four corners of a presentation reticle centred on the true AOI, the reticle is legible
    before any line exists, and it tightens onto the true AOI only after the lines have released.
    Everything analytical -- relief, drape, final hold -- stays on the true governed footprint.
    b9579ef adds: the platform may not cross the bottom-right caption, and masked analytical ground
    shows the Terrain context beneath rather than a dark neutral.
    ``audit_preview_gate.py`` measures the evaluated scene; this proves the contract those
    measurements rest on, without Blender -- the observer is locked off by construction, nothing
    that belongs to the scan survives into the camera move, the lock frame only ever tightens, and
    the relief is built from the governed DEM on the accepted analysis footprint and ends on the
    priority layer alone. It also keeps the gate a gate: until Product passes it, the shipped
    production scene may not pick up the relief, so the html_overlay rule on shipped media holds.
    """
    report.section("WEB-005A R3 preview gate")
    scenes = (scene_config or {}).get("scenes", {})
    gates = sorted(sid for sid, spec in scenes.items() if spec.get("role") == "hero_preview_gate")
    report.check(bool(gates), "a preview-gate scene exists")

    # Product passed the gate and moved WEB-005A to production. The accepted choreography now lives
    # in the production scene, the gate scene extends it unchanged, and this contract runs on both.
    # What replaces "no relief while the gate is open" is the rule the gate was protecting: nothing
    # analytical may reach a lossy encode, so the motion render has to end before the relief exists.
    production = sorted(sid for sid, spec in scenes.items() if spec.get("role") == "hero_production")
    for scene_id in production:
        resolved = hc.resolve_scene_spec(scene_id, scenes)
        relief = next((o for o in resolved.get("objects", []) if o.get("type") == "aoi_relief"), {})
        delivery = resolved.get("animation", {}).get("delivery", {})
        motion = delivery.get("motion_video_frames") or [0, 10 ** 9]
        first_analytical = min(
            [int(relief.get("rise_keyframes", [[10 ** 9]])[0][0])]
            + [int(keys[0][0]) for keys in (relief.get("layer_keyframes") or {}).values() if keys]
        )
        report.check(
            bool(relief) and int(motion[1]) <= first_analytical and int(delivery.get("held_frame", -1)) == int(motion[1]),
            "scene " + scene_id + " ends its lossy motion render on the held frame, before any analytical pixel exists",
            "motion " + repr(motion) + " first analytical frame " + str(first_analytical),
        )
        # docs/web-005-polish-authority@0e87675: the page shows the relief RISING between the held
        # frame and the Terrain state. The transition is the scene's own rise interval, delivered as
        # 6-12 lossless states strictly inside it, 0.45-0.70 s long -- not new choreography.
        rise_keys = sorted(int(f) for f, _ in relief.get("rise_keyframes", []))
        rise_frames = [int(f) for f in delivery.get("relief_rise_frames", [])]
        rate = float(resolved.get("animation", {}).get("frame_rate", 24))
        seconds = (rise_keys[-1] - rise_keys[0]) / rate if len(rise_keys) >= 2 else 0.0
        report.check(
            len(rise_keys) >= 2 and rise_keys[0] == int(motion[1]) and 6 <= len(rise_frames) <= 12
            and rise_frames == sorted(set(rise_frames))
            and rise_keys[0] < rise_frames[0] and rise_frames[-1] < rise_keys[-1]
            and 0.45 <= seconds <= 0.70,
            "scene " + scene_id + " delivers the relief rise as 6-12 states strictly inside its own rise interval, "
            "which starts on the held frame and lasts 0.45-0.70 s",
            repr({"rise_keyframes": rise_keys, "relief_rise_frames": rise_frames, "seconds": round(seconds, 3)}),
        )
        report.check(
            int(delivery.get("opening_frame", -1)) == int(motion[0]),
            "scene " + scene_id + " declares its startup poster as the first motion frame (the held frame is a separate base)",
            repr(delivery.get("opening_frame")),
        )
    for scene_id in gates:
        a = {k: v for k, v in hc.resolve_scene_spec(scene_id, scenes).items() if k not in ("role", "description")}
        parent = scenes[scene_id].get("extends")
        b = {k: v for k, v in hc.resolve_scene_spec(parent, scenes).items() if k not in ("role", "description")} if parent else None
        report.check(parent in production and a == b,
                     "scene " + scene_id + " is the production scene unchanged (one definition of the choreography)",
                     repr(parent))
    gates = gates + production

    interface = (scene_config or {}).get("aoi_injection_interface", {})
    for scene_id in gates:
        spec = hc.resolve_scene_spec(scene_id, scenes)
        label = "scene " + scene_id + " "
        camera = spec.get("camera", {})
        objects = {o.get("id"): o for o in spec.get("objects", [])}
        fixed = camera.get("fixed_through_frame")
        report.check(isinstance(fixed, int) and fixed > 1, label + "declares the frame the observer is fixed through",
                     repr(fixed))
        if not isinstance(fixed, int):
            continue

        # --- A-HERO-15: locked off by construction --------------------------------------------
        keys = sorted(camera.get("keyframes", []), key=lambda k: int(k["frame"]))
        try:
            derived = shot_plan.derive(scene_config, scene_id)
            drift = 0.0 if len(derived) == len(keys) else float("inf")
            for a, b in zip(keys, derived):
                if int(a["frame"]) != int(b["frame"]):
                    drift = float("inf")
                    break
                for field in ("location", "look_at"):
                    drift = max([drift] + [abs(float(x) - float(y)) for x, y in zip(a[field], b[field])])
                drift = max(drift, abs(float(a["focal_length_mm"]) - float(b["focal_length_mm"])))
            report.check(drift <= 1.0e-3, label + "committed camera keyframes match their shot intent",
                         "worst drift " + str(drift))
        except (KeyError, ValueError, SystemExit) as error:
            report.check(False, label + "camera derives from its shot intent", str(error))
        held = [k for k in keys if int(k["frame"]) <= fixed]
        states = {json.dumps([k["location"], k["look_at"], k["focal_length_mm"]]) for k in held}
        report.check(
            len(held) >= 2 and int(held[0]["frame"]) == int(spec["animation"]["frame_start"])
            and int(held[-1]["frame"]) == fixed and len(states) == 1,
            label + "every camera key from the first frame through " + str(fixed) + " is one identical state",
            str(len(states)) + " distinct states over " + str(len(held)) + " keys",
        )
        shifts = [k for k in camera.get("shift_keyframes", []) if int(k["frame"]) <= fixed]
        report.check(
            len({(k.get("shift_x"), k.get("shift_y")) for k in shifts}) == 1
            and any(int(k["frame"]) == fixed for k in shifts),
            label + "lens shift is constant while the observer is fixed",
        )
        influence = [k for k in camera.get("track", {}).get("influence_keyframes", []) if int(k["frame"]) <= fixed]
        report.check(
            bool(influence) and all(float(k["value"]) == 0.0 for k in influence)
            and any(int(k["frame"]) == fixed for k in influence),
            label + "the AOI track constraint is off while the observer is fixed",
        )

        # --- nothing of the scan survives into the move -----------------------------------------
        aoi_spec = objects.get("aoi", {})
        beams, fan, sweep = aoi_spec.get("beams", {}), aoi_spec.get("scan_fan", {}), aoi_spec.get("sweep", {})
        fill_vanish = (aoi_spec.get("fill", {}).get("vanish") or [None, None])[1]
        report.check(beams.get("target") == "corners" and not beams.get("cone"),
                     label + "draws four corner lines and no centre cone", repr(beams.get("target")))
        report.check(
            all(isinstance(v, int) and v <= fixed for v in
                (beams.get("release_end_frame"), fan.get("retire_end_frame"), fill_vanish, sweep.get("end_frame"))),
            label + "lines, fan, ground wash and sweep have all ended by frame " + str(fixed),
            repr([beams.get("release_end_frame"), fan.get("retire_end_frame"), fill_vanish, sweep.get("end_frame")]),
        )
        report.check(
            isinstance(sweep.get("start_frame"), int) and isinstance(fan.get("appear_end_frame"), int)
            and beams.get("appear_end_frame", 0) <= fan.get("appear_start_frame", -1)
            and fan["appear_end_frame"] <= sweep["start_frame"] + 4
            and sweep["end_frame"] <= fan.get("retire_start_frame", -1) <= beams.get("release_start_frame", -1),
            label + "orders the beat: lines lock, fan rises, sweep crosses, fan retires, lines release",
        )
        materials = spec.get("materials", {})
        report.check(materials.get(aoi_spec.get("fill_material"), {}).get("axis") == "u",
                     label + "sweeps along AOI u (west to east, left to right under this camera)")
        veil = materials.get(fan.get("veil_material"), {})
        curtain = materials.get(fan.get("curtain_material"), {})
        report.check(
            0.0 < float(veil.get("tip_alpha", 0.0)) <= 0.08 and 0.0 < float(curtain.get("band_alpha", 0.0)) <= 0.45
            and float(curtain.get("tail_alpha", 1.0)) <= 0.05,
            label + "keeps the fan secondary: a faint veil and a translucent curtain, never a slab",
            "veil " + repr(veil.get("tip_alpha")) + ", band " + repr(curtain.get("band_alpha")),
        )

        # --- Product override of 2026-09-18: visible acquisition on a presentation reticle ------------
        presentation = aoi_spec.get("presentation", {})
        report.check(beams.get("anchor") == "presented",
                     label + "lands the four visible lines on the four corners of the presentation reticle",
                     repr(beams.get("anchor")))
        report.check(sorted(presentation.get("reticle_parts", [])) == ["border", "border_glow", "corner_locks"],
                     label + "draws one reticle (frame, halo, brackets) that travels as a whole onto the true footprint",
                     repr(presentation.get("reticle_parts")))
        morph_start = presentation.get("screen_intent", {}).get("morph_frames", [0, 0])[0]
        report.check(isinstance(beams.get("release_end_frame"), int) and morph_start >= beams["release_end_frame"],
                     label + "never moves a line anchor while a line is attached (reticle tightens only after release)",
                     repr([beams.get("release_end_frame"), morph_start]))
        border_cfg, locks_cfg = aoi_spec.get("border", {}), aoi_spec.get("corner_locks", {})
        report.check(
            isinstance(beams.get("appear_start_frame"), int)
            and border_cfg.get("appear_start_frame", 10 ** 6) + 8 <= beams["appear_start_frame"]
            and locks_cfg.get("draw_start_frame", 10 ** 6) + 6 <= beams["appear_start_frame"]
            and locks_cfg.get("draw_end_frame", 10 ** 6) <= beams.get("appear_end_frame", -1),
            label + "resolves the reticle before the lines: the target is legible first, never 'appears afterwards'",
            repr([border_cfg.get("appear_start_frame"), locks_cfg.get("draw_start_frame"),
                  locks_cfg.get("draw_end_frame"), beams.get("appear_start_frame"), beams.get("appear_end_frame")]),
        )
        pulse_frame = aoi_spec.get("lock_pulse_frame")
        pulse = dict((int(f), float(v)) for f, v in border_cfg.get("emphasis", [])).get(pulse_frame, 0.0)
        report.check(
            isinstance(pulse_frame, int) and beams.get("appear_end_frame", 10 ** 6) <= pulse_frame <= sweep.get("start_frame", -1)
            and pulse >= 1.8,
            label + "makes the lock an event after all four lines have landed and before the sweep",
            repr([pulse_frame, pulse]),
        )
        report.check(bool((beams.get("emitter") or {}).get("object_id")),
                     label + "emits the lines from the instrument aperture")
        top = fan.get("top") or {}
        half = float((beams.get("emitter") or {}).get("half_side_km", -1.0))
        report.check(float(top.get("half_length_km", 0.0)) == half and float(top.get("half_depth_km", 0.0)) == half,
                     label + "builds the scan fan exactly between the four lines (its top is the emitter square)",
                     repr([top, half]))
        # A view ray can cross every curtain slice, a line tube and the reticle before it reaches the
        # ground. Past transparent_max_bounces Cycles ends the path BLACK -- and it does so whether or
        # not the slices are visible, so an exhausted budget prints a black line from the platform to a
        # reticle corner before the lines draw on and after they release (found in the first final
        # production render: slices went 64 -> 96 for smoothness under an unchanged budget of 96).
        slices = int(fan.get("slices", 0))
        budget = int((spec.get("render_overrides") or {}).get("transparent_max_bounces", 8))
        report.check(budget >= 2 * slices + 64,
                     label + "gives view rays a transparent-bounce budget that clears the whole curtain stack "
                             "(at least 2 x slices + 64), so invisible effects cannot print a black line",
                     repr({"slices": slices, "transparent_max_bounces": budget}))

        # --- Product clarifications 1-2: settle -> aim -> draw-on, and lines that propagate ---------
        satellite_spec = objects.get("satellite", {})
        profile = sorted((float(f), float(r)) for f, r in satellite_spec.get("orbit_intent", {}).get("rate_profile", []))
        aim_keys = sorted((int(k["frame"]), float(k["value"]))
                          for k in satellite_spec.get("aim", {}).get("influence_keyframes", []))
        draw_start, release_end = beams.get("appear_start_frame"), beams.get("release_end_frame")
        station = [f for f, r in profile if r <= 0.02]
        settled = min(station) if station else None
        aim_begin = aim_keys[0][0] if aim_keys else None
        aim_full = next((f for f, v in aim_keys if v >= 1.0), None)
        aim_release = next((f for f, v in reversed(aim_keys) if v >= 1.0), None)
        report.check(
            None not in (settled, aim_begin, aim_full, aim_release) and isinstance(draw_start, int)
            and settled <= aim_begin < aim_full < draw_start and aim_release >= release_end,
            label + "orders the acquisition: pass settles, platform slews, slew completes, only then do lines draw",
            repr({"settled": settled, "aim": [aim_begin, aim_full], "lines": [draw_start, release_end],
                  "aim_released": aim_release}),
        )
        # Evaluated per frame, not per key: a ramp that starts before the release has no key inside
        # the window but still moves the platform under an attached line.
        orbit_intent = satellite_spec.get("orbit_intent", {})
        report.check(
            isinstance(release_end, int) and settled is not None
            and all(orbit_plan.rate_at(orbit_intent, frame) <= 0.02 for frame in range(int(settled), release_end + 1)),
            label + "holds the platform at station-keeping rate for as long as any line is attached",
        )
        draw = beams.get("draw") or {}
        report.check(
            bool(draw) and isinstance(draw_start, int)
            and beams.get("appear_end_frame", 0) - draw_start - 3 * float(draw.get("stagger_frames", 0.0)) >= 8
            and all("draw_on" in materials.get(name, {}) for name in (aoi_spec.get("beam_material"), beams.get("glow_material"))),
            label + "draws each line on over at least 8 frames (core and glow both masked), never a fade-in",
            repr(draw),
        )

        # --- Product clarification 3: thinner line language ---------------------------------------------
        px = presentation.get("screen_intent", {}).get("acquisition_px", {})
        report.check(
            float(px.get("border_px", 99)) <= 1.6 and float(px.get("glow_px", 99)) <= 8.0
            and float(px.get("corner_lock_px", 99)) <= 2.6,
            label + "states the thinner outline / halo / bracket weights (first gate: 2.2 / 13 / 4.0 px)", repr(px),
        )
        report.check(
            float(beams.get("tip_radius_km", 99)) <= 2.0 and float(beams.get("root_radius_km", 99)) <= 2.0
            and float(beams.get("glow_radius_factor", 99)) <= 3.0,
            label + "states thinner sensing lines (first gate: 2.4 -> 4.2 km core, 4.5x glow)",
            repr([beams.get("root_radius_km"), beams.get("tip_radius_km"), beams.get("glow_radius_factor")]),
        )

        # --- Product clarification 4: cyan / teal, never milky white --------------------------------------
        palette = (scene_config or {}).get("palette", {})
        scan_refs = {
            name: materials.get(name, {}).get("emission_color_ref")
            for name in (aoi_spec.get("beam_material"), beams.get("glow_material"), fan.get("veil_material"),
                         fan.get("curtain_material"), aoi_spec.get("border_material"),
                         aoi_spec.get("corner_lock_material"))
        }
        report.check(set(scan_refs.values()) <= {"scan_cyan", "scan_teal"},
                     label + "draws every acquisition effect in the scan cyan / teal", repr(scan_refs))
        for ref in ("scan_cyan", "scan_teal"):
            colour = palette.get(ref) or [1.0, 1.0, 1.0]
            report.check(
                colour[0] <= 0.1 * max(colour) and min(colour[1], colour[2]) >= 0.5 * max(colour),
                label + "palette " + ref + " is a saturated cyan / teal (almost no red, green and blue together)",
                repr(colour),
            )
        curtain_spec = materials.get(fan.get("curtain_material"), {})
        report.check(
            float(curtain_spec.get("emission_strength", 99)) <= float(materials.get(aoi_spec.get("beam_material"), {}).get("emission_strength", 0)),
            label + "keeps the curtain dimmer than the four lines it supports",
        )

        # --- c7c6cb1 sections 6 and 8: bounded exit and timing envelope ----------------------------------
        exit_cfg = camera.get("composition", {}).get("satellite_exit", {})
        report.check(0.0 < float(exit_cfg.get("max_width_fraction", 9.9)) <= 0.22,
                     label + "declares the platform-exit fly-by bound at or under 22 percent", repr(exit_cfg.get("max_width_fraction")))
        region = camera.get("composition", {}).get("caption_safe_region_1440", {})
        box = region.get("caption_box", {})
        report.check(
            bool(box) and float(region.get("x0", 9.9)) <= float(box.get("x0", 0.0)) - 0.03
            and float(region.get("y1", 0.0)) >= float(box.get("y1", 9.9)) + 0.04
            and float(region.get("x1", 0.0)) >= 1.0 and float(region.get("y0", 9.9)) <= 0.0,
            label + "protects the bottom-right caption with a margin, out to the frame's right and bottom edges (b9579ef section 2)",
            repr({k: region.get(k) for k in ("x0", "x1", "y0", "y1")}),
        )
        envelope = spec.get("animation", {}).get("timing_envelope", {})
        rate = float(spec.get("animation", {}).get("frame_rate", 24))
        motion = envelope.get("motion_section_frames", [0, 0])
        reveal = envelope.get("analytical_sequence_frames", [0, 0])
        report.check(11.5 <= (motion[1] - motion[0] + 1) / rate <= 12.5 and 2.4 <= (reveal[1] - reveal[0]) / rate <= 3.2,
                     label + "declares a timing envelope inside the approved one (motion 11.5-12.5 s, reveal 2.4-3.2 s)",
                     repr([motion, reveal]))
        report.check(
            not any(o.get("type") in ("legend", "colorbar", "info_card", "text") for o in spec.get("objects", [])),
            label + "renders no colour bar, legend or information card into the hero (Product clarification 5)",
        )

        # --- one reticle that only tightens ---------------------------------------------------------
        derived = presentation.get("derived", {})
        morph = derived.get("morph_keyframes", [])
        window = presentation.get("screen_intent", {}).get("morph_frames", [0, 0])
        fixture = interface.get("fixtures", {}).get(aoi_spec.get("fixture"), {})
        report.check(fixture.get("is_analysis_aoi") is True,
                     label + "lock frame is drawn from the accepted analysis fixture", repr(aoi_spec.get("fixture")))
        report.check(
            bool(morph) and morph[0] == [window[0], 1.0] and morph[-1] == [window[1], 0.0]
            and window[0] >= fixed and all(b[1] <= a[1] and b[0] > a[0] for a, b in zip(morph, morph[1:])),
            label + "lock frame holds its presentation while fixed, then tightens monotonically onto the footprint",
        )
        weight = derived.get("weight_keyframes", [])
        report.check(
            bool(weight) and weight[0] == [window[0], 1.0] and weight[-1] == [window[1], 0.0]
            and all(b[1] <= a[1] and b[0] > a[0] for a, b in zip(weight, weight[1:])),
            label + "lock-frame line weight is its own ramp over the same window",
        )
        report.check(
            abs(float(derived.get("settled", {}).get("span_km", 0.0)) - float(fixture.get("span_km", -1.0))) < 1e-9,
            label + "settled lock frame is the fixture's own span", repr(derived.get("settled", {}).get("span_km")),
        )
        report.check(derived.get("ground_scale_source") == "evaluated_camera",
                     label + "morph was derived from the evaluated camera", repr(derived.get("ground_scale_source")))

        # --- satellite pass still derived ------------------------------------------------------------
        satellite = objects.get("satellite", {})
        try:
            planned = orbit_plan.derive(scene_config, scene_id)
            committed = sorted(satellite.get("location_keyframes", []), key=lambda k: int(k["frame"]))
            drift = 0.0 if len(planned) == len(committed) else float("inf")
            for a, b in zip(committed, planned):
                drift = max([drift] + [abs(float(x) - float(y)) for x, y in zip(a["location"], b["location"])])
            report.check(drift <= 1.0e-3, label + "committed satellite keyframes match their orbit derivation",
                         "worst drift " + str(drift))
        except (KeyError, ValueError, SystemExit) as error:
            report.check(False, label + "satellite pass derives from its orbit intent", str(error))

        # --- A-HERO-18 / 19: relief contract -----------------------------------------------------------
        relief = next((o for o in spec.get("objects", []) if o.get("type") == "aoi_relief"), None)
        report.check(relief is not None, label + "builds the AOI relief")
        if relief is None:
            continue
        report.check(relief.get("fixture") == aoi_spec.get("fixture") and relief.get("aoi_id") == "aoi",
                     label + "relief and lock frame share one fixture mapping")
        report.check(2.0 <= float(relief.get("vertical_exaggeration", 0.0)) <= 4.0,
                     label + "vertical exaggeration is inside the authorized 2-4x presentation band",
                     repr(relief.get("vertical_exaggeration")))
        ingest_path = hc.EVIDENCE_DIR / "web005a_r3_preview" / "analytical_asset_ingest.json"
        ingest = hc.load_json(ingest_path) if ingest_path.is_file() else {}
        recorded = {entry["materialized"]: entry for entry in ingest.get("files", [])}
        report.check(not ingest.get("problems") and bool(recorded),
                     label + "analytical asset ingest is recorded with no open problem", hc.relpath(ingest_path))
        report.check(recorded.get(relief.get("dem"), {}).get("use") == "relief_geometry_source",
                     label + "relief geometry comes from the governed DEM, not from a display texture",
                     repr(relief.get("dem")))
        layers = materials.get(relief.get("material"), {})
        order = layers.get("layer_order", [])
        report.check(layers.get("underlay_layer") == "terrain" and "terrain" in order,
                     label + "shows the Terrain context through masked analytical ground, never a dark neutral (b9579ef section 3)",
                     repr(layers.get("underlay_layer")))
        report.check(order == ["terrain", "thm01", "alt01", "priority"],
                     label + "reveals Terrain, THM-01, ALT-01, priority in the locked order", repr(order))
        for layer_id in order:
            texture = layers.get("layers", {}).get(layer_id, {}).get("texture")
            entry = recorded.get(texture, {})
            report.check(entry.get("use") == "display_texture",
                         label + "layer " + layer_id + " is a recorded display texture", repr(texture))
            path = hc.SOURCE_DIR / str(texture)
            if path.is_file() and entry.get("sha256"):
                report.check(hc.sha256_file(path) == entry["sha256"],
                             label + "materialized " + str(texture) + " matches its ingest checksum")
        end = int(spec["animation"]["frame_end"])
        ramps = relief.get("layer_keyframes", {})
        final = {layer_id: (ramps.get(layer_id) or [[0, 0.0]])[-1] for layer_id in order}
        report.check(
            bool(order) and final.get("priority") == [end, 1.0]
            and all(final[l][1] == 0.0 and final[l][0] < end for l in order if l != "priority"),
            label + "ends on the priority layer alone (A-HERO-19)", repr(final),
        )
        rise = relief.get("rise_keyframes", [])
        report.check(bool(rise) and rise[0][0] >= window[1],
                     label + "relief rises only after the approach has settled", repr(rise[:1]))
        priority_full = next((f for f, w in ramps.get("priority", []) if w >= 1.0), None)
        first_layer = min((keys[0][0] for keys in ramps.values() if keys), default=None)
        report.check(first_layer == reveal[0] and priority_full == reveal[1],
                     label + "layer ramps occupy exactly the declared analytical window",
                     repr([first_layer, priority_full]) + " vs " + repr(reveal))


def check_manifest(report: Report, manifest) -> None:
    report.section("asset rights manifest")
    if not manifest:
        report.check(False, "manifest loaded")
        return

    policy = manifest.get("policy", {})
    report.check("schema_version" in manifest, "manifest declares a schema version")
    report.check(bool(policy), "manifest declares a rights policy")
    report.check(isinstance(manifest.get("assets"), list), "manifest declares an asset list")

    required = policy.get("required_fields", [])
    allowed_licenses = set(policy.get("allowed_license_bases", []))
    status_values = set(policy.get("rights_status_values", []))
    publishable = set(policy.get("publishable_rights_status", []))
    report.check(bool(required), "manifest states its required asset fields")
    report.check(bool(allowed_licenses), "manifest states an allowed license basis set")

    for index, asset in enumerate(manifest.get("assets", [])):
        label = "asset[" + str(index) + "] " + str(asset.get("id", "<no id>"))
        missing = [
            field
            for field in required
            if field not in asset or asset[field] in (None, "")
        ]
        report.check(
            not missing, label + " declares every required field", "missing " + repr(missing)
        )
        report.check(
            asset.get("license") in allowed_licenses,
            label + " uses an allowed license basis",
            repr(asset.get("license")),
        )
        report.check(
            asset.get("rights_status") in status_values,
            label + " uses a known rights status",
            repr(asset.get("rights_status")),
        )
        if asset.get("rights_status") in publishable:
            digest = str(asset.get("sha256", ""))
            report.check(
                bool(HEX64.match(digest)),
                label + " records a SHA-256 for cleared material",
                repr(digest),
            )
            local = asset.get("local_path")
            if local:
                path = hc.REPO_ROOT / local
                report.check(
                    path.exists(),
                    label + " materialized local path exists",
                    hc.relpath(path),
                )


def check_generated_output_policy(report: Report) -> None:
    report.section("generated output is not source authority")
    for directory in hc.GENERATED_DIRS:
        ignore = directory / ".gitignore"
        if not report.check(
            ignore.is_file(), "ignore policy present: " + hc.relpath(ignore)
        ):
            continue
        lines = [line.strip() for line in ignore.read_text(encoding="utf-8").splitlines()]
        report.check(
            "*" in lines and "!.gitignore" in lines,
            hc.relpath(directory) + " ignores its payload but keeps the directory",
            repr(lines),
        )

    tracked = git_tracked_hero_files()
    if tracked is None:
        print("  SKIP  tracked-size audit (git unavailable)")
        return

    oversized = []
    sequences = []
    for rel in tracked:
        path = hc.REPO_ROOT / rel
        if path.is_file() and path.stat().st_size > MAX_TRACKED_BYTES:
            oversized.append(rel + " (" + str(path.stat().st_size) + " bytes)")
        if re.search(r"\d{4}\.(png|jpg|jpeg|exr|tif|tiff)$", rel, re.IGNORECASE):
            sequences.append(rel)

    report.check(
        not oversized,
        "no oversized binary is tracked under hero/",
        "; ".join(oversized),
    )
    report.check(
        not sequences,
        "no frame sequence is tracked under hero/",
        "; ".join(sequences),
    )
    report.check(
        not any(rel.startswith("hero/renders/") for rel in tracked if not rel.endswith(".gitignore")),
        "hero/renders/ has no tracked payload",
    )


def git_tracked_hero_files():
    try:
        output = subprocess.run(
            ["git", "-C", str(hc.REPO_ROOT), "ls-files", "hero"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return [line.strip() for line in output.splitlines() if line.strip()]


def git(*args):
    """Run a git command in the repository; return stdout, or None on failure."""
    try:
        return subprocess.run(
            ["git", "-C", str(hc.REPO_ROOT), *args],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None


def check_lane_isolation(report: Report, lane) -> None:
    """Lane boundary, in whichever mode the lane declares.

    Through WEB-HERO-001A..D the boundary was absolute: the hero lane could not touch the public
    site at all, and protected paths had to stay byte-identical to a pinned baseline. WEB-005 is
    the single integration gate that rule always named, so the lane declares ``integration`` mode
    and the boundary becomes a different, still-checkable claim: the hero lane may now be consumed
    by the site, but it still may not reach outside the surfaces the integration task owns.
    """
    report.section("lane boundary")
    if not lane:
        report.check(False, "lane configuration loaded")
        return

    protected = lane.get("protected_paths", [])
    baseline = lane.get("baseline_commit")
    mode = lane.get("mode", "isolated")
    report.check(bool(protected), "lane configuration lists protected public-site paths")
    report.check(bool(baseline), "lane configuration pins a baseline commit")
    report.check(
        mode in ("isolated", "integration"),
        "lane configuration declares a known mode",
        repr(mode),
    )
    integrating = mode == "integration"
    if integrating:
        report.check(
            bool(lane.get("integration_task")) and bool(lane.get("integration_authority")),
            "integration mode names the task and authority that opened the gate",
        )

    # While isolated, no hero source file may name a protected path: that lane builds no site
    # integration, so even a reference is a smell. While integrating, the hero config is allowed
    # to point at the accepted assets it binds -- but only through an explicit allowlist, so the
    # exemption stays narrow and visible rather than becoming a general licence.
    allowed_refs = set(lane.get("integration_reference_allowlist", [])) if integrating else set()
    offenders = []
    for path in sorted(hc.HERO_ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".py", ".json", ".md"}:
            continue
        if path.name == SELF_NAME or hc.CONFIG_DIR == path.parent and path.name == "lane.json":
            continue
        if hc.RENDERS_DIR in path.parents or hc.SOURCE_DIR in path.parents:
            continue
        if hc.relpath(path).replace("\\", "/") in allowed_refs:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name in protected:
            if name in text:
                offenders.append(hc.relpath(path) + " mentions " + name)
    report.check(
        not offenders,
        "no unallowlisted hero source file references a protected public-site path",
        "; ".join(offenders),
    )

    if not baseline:
        return

    if git("cat-file", "-e", baseline + "^{commit}") is None:
        print("  SKIP  baseline comparison (baseline commit not present locally)")
        return

    drift = git("diff", "--name-only", baseline, "HEAD", "--", *protected)
    if drift is None:
        print("  SKIP  baseline comparison (git diff unavailable)")
    elif integrating:
        # The point of the gate: the site is expected to change now. What must not happen is the
        # change reaching a path the integration task does not own.
        owned = set(lane.get("integration_write_surface", []))
        changed = [line for line in drift.splitlines() if line.strip()]
        stray = [line for line in changed if line not in owned]
        report.check(
            not stray,
            "public-site changes since the baseline stay inside the integration write surface",
            "; ".join(stray),
        )
    else:
        changed = [line for line in drift.splitlines() if line.strip()]
        report.check(
            not changed,
            "protected public-site paths are unchanged since the pinned baseline",
            "; ".join(changed),
        )

    if integrating:
        return

    dirty = git("status", "--porcelain", "--", *protected)
    if dirty is not None:
        entries = [line for line in dirty.splitlines() if line.strip()]
        report.check(
            not entries,
            "protected public-site paths have no uncommitted modification",
            "; ".join(entries),
        )


def main() -> int:
    print("OrbGSS hero workspace validation — " + hc.relpath(hc.HERO_ROOT))
    report = Report()

    check_scaffold(report)
    loaded = load_configs(report)
    check_render_profiles(report, loaded.get("render"))
    check_scene_config(report, loaded.get("scene"), loaded.get("render"))
    check_pre_data_boundary(report, loaded.get("scene"), loaded.get("manifest"))
    check_aoi_system(report, loaded.get("scene"))
    check_continuous_sequence(report, loaded.get("scene"))
    check_r2_visual_contract(report, loaded.get("scene"), loaded.get("manifest"))
    check_r3_preview_gate(report, loaded.get("scene"))
    check_manifest(report, loaded.get("manifest"))
    check_generated_output_policy(report)
    check_lane_isolation(report, loaded.get("lane"))

    print("\n" + str(report.checks) + " checks, " + str(len(report.failures)) + " failed")
    if report.failures:
        print("VALIDATION FAILED")
        return 1
    print("VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
