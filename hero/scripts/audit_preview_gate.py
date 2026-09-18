"""Measure the WEB-005A R3 preview-gate scene as Blender actually evaluates it.

    blender -b -P hero/scripts/audit_preview_gate.py -- --scene hero_r3_preview_gate \
        --out hero/evidence/web005a_r3_preview/preview_gate_audit.json

``validate_hero.py`` proves what configuration can prove. This proves the rest, per frame, after
F-curves, constraints, hooks, shape keys and Earth rotation -- the gates the R3 review
(docs/web-005-polish-authority@473b48a, tasks/WEB-005A_R3_REVIEW_37152222.md) asks to see
numerically before any further long render:

A-HERO-15  the camera does not move, turn, zoom or shift before the scan has retired
A-HERO-12/13  the platform is unclipped, right of the hero copy column and readable while acquiring
A-HERO-16  exactly four lines, each ending on its corner anchor and starting on the platform;
           the anchors lie on the true footprint's own diagonals
(refined)  lines, fan and ground band are gone before the first camera motion
(refined)  one lock frame: never under the surface while it tightens, line weight inside a
           screen-space band, landing on the true corners
A-HERO-17  the settled footprint sits in the right-middle zone, clear of the copy column
A-HERO-18  the relief, every display layer and the frame share one registered footprint
A-HERO-19  the last frame shows the priority layer alone

Whether it *looks* right is for the stills and the animatic. Nothing here renders.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bpy  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402
from mathutils import Vector  # noqa: E402

import aoi_system as ax  # noqa: E402
import build_scene  # noqa: E402
import hero_common as hc  # noqa: E402

REFERENCE_WIDTH_PX = 1920.0
# EPSG:32635 (WGS84 / UTM zone 35N) inverse, Snyder 1987 eq. 8-17 .. 8-25.
_A, _F, _K0, _LON0 = 6378137.0, 1.0 / 298.257223563, 0.9996, math.radians(27.0)


def utm35n_inverse(easting, northing):
    e2 = _F * (2.0 - _F)
    ep2 = e2 / (1.0 - e2)
    mu = (northing / _K0) / (_A * (1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256))
    e1 = (1 - math.sqrt(1 - e2)) / (1 + math.sqrt(1 - e2))
    phi = (mu + (3 * e1 / 2 - 27 * e1 ** 3 / 32) * math.sin(2 * mu)
           + (21 * e1 ** 2 / 16 - 55 * e1 ** 4 / 32) * math.sin(4 * mu)
           + (151 * e1 ** 3 / 96) * math.sin(6 * mu) + (1097 * e1 ** 4 / 512) * math.sin(8 * mu))
    c1, t1 = ep2 * math.cos(phi) ** 2, math.tan(phi) ** 2
    n1 = _A / math.sqrt(1 - e2 * math.sin(phi) ** 2)
    r1 = _A * (1 - e2) / (1 - e2 * math.sin(phi) ** 2) ** 1.5
    d = (easting - 500000.0) / (n1 * _K0)
    lat = phi - (n1 * math.tan(phi) / r1) * (
        d ** 2 / 2 - (5 + 3 * t1 + 10 * c1 - 4 * c1 ** 2 - 9 * ep2) * d ** 4 / 24
        + (61 + 90 * t1 + 298 * c1 + 45 * t1 ** 2 - 252 * ep2 - 3 * c1 ** 2) * d ** 6 / 720)
    lon = _LON0 + (d - (1 + 2 * t1 + c1) * d ** 3 / 6
                   + (5 - 2 * c1 + 28 * t1 - 3 * c1 ** 2 + 8 * ep2 + 24 * t1 ** 2) * d ** 5 / 120) / math.cos(phi)
    return math.degrees(lat), math.degrees(lon)


def check(ok, label, measured, threshold, unit=""):
    return {"ok": bool(ok), "label": label, "measured": measured, "threshold": threshold, "unit": unit}


def screen(scene, camera, point):
    v = world_to_camera_view(scene, camera, Vector(point))
    return (v.x, v.y, v.z)


def occluded(camera_location, point, radius_bu):
    direction = Vector(point) - camera_location
    distance = direction.length
    direction.normalize()
    b = 2.0 * camera_location.dot(direction)
    c = camera_location.dot(camera_location) - radius_bu * radius_bu
    disc = b * b - 4.0 * c
    if disc < 0.0:
        return False
    t = (-b - math.sqrt(disc)) / 2.0
    return 0.0 < t < distance


def value_node(material_name, node_name):
    material = bpy.data.materials.get(material_name)
    node = material.node_tree.nodes.get(node_name) if material else None
    return None if node is None else node.outputs[0]


def evaluated_socket(material_name, node_name, depsgraph):
    material = bpy.data.materials.get(material_name)
    if material is None:
        return None
    node = material.evaluated_get(depsgraph).node_tree.nodes.get(node_name)
    return None if node is None else float(node.outputs[0].default_value)


def audit(scene_id):
    scene_config = hc.load_scene_config()
    spec = build_scene.build(scene_id, scene_config)
    scene = bpy.context.scene
    scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
    camera = scene.camera
    objects = {o["id"]: o for o in spec["objects"]}
    aoi = objects["aoi"]
    materials = spec["materials"]
    animation = spec["animation"]
    start, end = int(animation["frame_start"]), int(animation["frame_end"])
    fixed_end = int(spec["camera"]["fixed_through_frame"])
    beat = spec["camera"]["composition"]["acquisition_beat"]
    copy_edge = float(spec["camera"]["composition"]["copy_safe_region_1440"]["x1"])
    radius_bu = ax.earth_radius_km(scene_config) / ax.KM_PER_BLENDER_UNIT
    corner_ids = list(ax.CORNER_IDS)

    satellite = bpy.data.objects["satellite"]
    sat_meshes = [o for o in satellite.children_recursive if o.type == "MESH"] or [satellite]
    border = bpy.data.objects["aoi_border"]
    glow = bpy.data.objects.get("aoi_border_glow")
    relief = bpy.data.objects.get("aoi_relief")
    beams = sorted(o.name for o in bpy.data.objects if o.name.startswith("aoi_beam_"))
    samples_per_edge = len(border.data.vertices) // 8
    ribbons = [o for o in bpy.data.objects if o.name == "aoi_border_glow" or o.name.startswith("aoi_lock_")]

    reference = None
    rows = []
    for frame in range(start, end + 1):
        scene.frame_set(frame)
        depsgraph = bpy.context.evaluated_depsgraph_get()
        cam = camera.evaluated_get(depsgraph)
        matrix = cam.matrix_world.copy()
        state = [matrix.translation.copy(), matrix.to_quaternion(), cam.data.lens, cam.data.shift_x, cam.data.shift_y]
        if reference is None:
            reference = state
        row = {
            "frame": frame,
            "camera_move_m": (state[0] - reference[0]).length * 1.0e6,
            "camera_turn_deg": math.degrees(state[1].rotation_difference(reference[1]).angle),
            "lens_delta_mm": abs(state[2] - reference[2]),
            "shift_delta": max(abs(state[3] - reference[3]), abs(state[4] - reference[4])),
        }

        # platform
        xs, ys = [], []
        for mesh in sat_meshes:
            world = mesh.evaluated_get(depsgraph).matrix_world
            for corner in mesh.bound_box:
                sx, sy, sz = screen(scene, camera, world @ Vector(corner))
                if sz > 0:
                    xs.append(sx)
                    ys.append(sy)
        centre = satellite.evaluated_get(depsgraph).matrix_world.translation
        row["sat"] = {
            "centre": [round(v, 4) for v in screen(scene, camera, centre)[:2]],
            "bbox": [round(min(xs), 4), round(min(ys), 4), round(max(xs), 4), round(max(ys), 4)] if xs else None,
            "occluded": occluded(matrix.translation, centre, radius_bu),
        }

        # sensing lines
        row["beam_presence"] = evaluated_socket("aoi_beam", "aoi_presence", depsgraph)
        row["fan_presence"] = max(
            evaluated_socket("aoi_fan_veil", "aoi_presence", depsgraph) or 0.0,
            evaluated_socket("aoi_scan_curtain", "aoi_presence", depsgraph) or 0.0,
        )
        row["fill_presence"] = evaluated_socket("aoi_fill", "aoi_presence", depsgraph)
        row["sweep"] = evaluated_socket("aoi_fill", "aoi_sweep_position", depsgraph)
        row["curtain_sweep"] = evaluated_socket("aoi_scan_curtain", "aoi_sweep_position", depsgraph)
        tips, roots = [], []
        for corner_id in corner_ids:
            beam = bpy.data.objects["aoi_beam_" + corner_id].evaluated_get(depsgraph)
            target = bpy.data.objects["aoi_target_" + corner_id].evaluated_get(depsgraph)
            tips.append(((beam.matrix_world @ Vector((0, 1, 0))) - target.matrix_world.translation).length * 1.0e6)
            roots.append((beam.matrix_world.translation - centre).length * 1.0e6)
        row["beam_tip_error_m"], row["beam_root_error_m"] = max(tips), max(roots)

        # lock frame, as evaluated
        mesh = border.evaluated_get(depsgraph)
        verts = [mesh.matrix_world @ v.co for v in mesh.to_mesh().vertices]
        mesh.to_mesh_clear()
        centres = [(verts[2 * i] + verts[2 * i + 1]) / 2.0 for i in range(len(verts) // 2)]
        frame_corners = [centres[k * samples_per_edge] for k in range(4)]
        projected = [screen(scene, camera, p) for p in frame_corners]
        row["frame_width_fraction"] = max(p[0] for p in projected) - min(p[0] for p in projected)
        row["frame_bbox"] = [round(min(p[0] for p in projected), 4), round(min(p[1] for p in projected), 4),
                             round(max(p[0] for p in projected), 4), round(max(p[1] for p in projected), 4)]
        mid = samples_per_edge // 2  # middle of the north edge
        a, b = screen(scene, camera, verts[2 * mid]), screen(scene, camera, verts[2 * mid + 1])
        row["border_px"] = math.hypot((a[0] - b[0]) * REFERENCE_WIDTH_PX, (a[1] - b[1]) * REFERENCE_WIDTH_PX * 9 / 16)
        lowest = min(v.length for v in verts)
        for ribbon in ribbons:
            rm = ribbon.evaluated_get(depsgraph)
            lowest = min([lowest] + [(rm.matrix_world @ v.co).length for v in rm.to_mesh().vertices])
            rm.to_mesh_clear()
        row["frame_min_clearance_m"] = (lowest - radius_bu) * 1.0e6
        true_corners = [bpy.data.objects["aoi_true_" + c].evaluated_get(depsgraph).matrix_world.translation
                        for c in corner_ids]
        order = spec_corner_order(scene_config)
        row["frame_to_true_corner_m"] = max(
            angular_m(frame_corners[order.index(c)], true_corners[i], radius_bu) for i, c in enumerate(corner_ids)
        )
        if glow is not None:
            gm = glow.evaluated_get(depsgraph)
            gv = [gm.matrix_world @ v.co for v in gm.to_mesh().vertices]
            gm.to_mesh_clear()
            a, b = screen(scene, camera, gv[2 * mid]), screen(scene, camera, gv[2 * mid + 1])
            row["glow_px"] = math.hypot((a[0] - b[0]) * REFERENCE_WIDTH_PX, (a[1] - b[1]) * REFERENCE_WIDTH_PX * 9 / 16)

        row["layers"] = {
            layer: evaluated_socket("aoi_relief_layers", "layer_weight_" + layer, depsgraph)
            for layer in materials["aoi_relief_layers"]["layer_order"]
        }
        rows.append(row)

    by_frame = {r["frame"]: r for r in rows}
    fixed = [r for r in rows if r["frame"] <= fixed_end]
    acquiring = [r for r in rows if beat[0] <= r["frame"] <= beat[1]]
    checks = []

    # --- A-HERO-15 -------------------------------------------------------------------------
    checks.append(check(max(r["camera_move_m"] for r in fixed) <= 1.0, "A-HERO-15 camera translation, frames 1-"
                        + str(fixed_end), round(max(r["camera_move_m"] for r in fixed), 6), 1.0, "m"))
    checks.append(check(max(r["camera_turn_deg"] for r in fixed) <= 1.0e-4, "A-HERO-15 camera rotation",
                        round(max(r["camera_turn_deg"] for r in fixed), 8), 1.0e-4, "deg"))
    checks.append(check(max(r["lens_delta_mm"] for r in fixed) <= 1.0e-4, "A-HERO-15 focal length",
                        round(max(r["lens_delta_mm"] for r in fixed), 8), 1.0e-4, "mm"))
    checks.append(check(max(r["shift_delta"] for r in fixed) <= 1.0e-6, "A-HERO-15 lens shift",
                        round(max(r["shift_delta"] for r in fixed), 9), 1.0e-6, "sensor widths"))
    first_motion = next((r["frame"] for r in rows if r["camera_move_m"] > 1.0), None)
    checks.append(check(first_motion == fixed_end + 1, "first frame with any camera motion",
                        first_motion, fixed_end + 1, "frame"))

    # --- retirement before motion ------------------------------------------------------------
    at_release = by_frame[fixed_end]
    checks.append(check((at_release["beam_presence"] or 0.0) <= 1.0e-4, "sensing lines fully retired at frame "
                        + str(fixed_end), at_release["beam_presence"], 0.0, "presence"))
    checks.append(check(at_release["fan_presence"] <= 1.0e-4, "scan fan fully retired at frame " + str(fixed_end),
                        at_release["fan_presence"], 0.0, "presence"))
    checks.append(check((at_release["fill_presence"] or 0.0) <= 1.0e-4, "ground scan wash retired at frame "
                        + str(fixed_end), at_release["fill_presence"], 0.0, "presence"))
    moving = [r for r in rows if r["frame"] > fixed_end]
    checks.append(check(max((r["beam_presence"] or 0.0) for r in moving) <= 1.0e-4 and
                        max(r["fan_presence"] for r in moving) <= 1.0e-4,
                        "no line or fan is visible on any frame in which the camera moves", 0.0, 0.0, "presence"))

    # --- sweep: west to east, fan and ground in step ------------------------------------------
    sweep = aoi["sweep"]
    sweeping = [r for r in rows if sweep["start_frame"] <= r["frame"] <= sweep["end_frame"]]
    monotonic = all(b["sweep"] > a["sweep"] for a, b in zip(sweeping, sweeping[1:]))
    in_step = max(abs(r["sweep"] - r["curtain_sweep"]) for r in sweeping)
    checks.append(check(monotonic and materials["aoi_fill"].get("axis") == "u",
                        "sweep travels west to east (AOI u, screen left to right) and never reverses",
                        [round(sweeping[0]["sweep"], 3), round(sweeping[-1]["sweep"], 3)], "increasing", "u"))
    checks.append(check(in_step <= 1.0e-6, "light curtain and ground band read one sweep value", in_step, 1.0e-6, "u"))
    checks.append(check(sweep["end_frame"] <= fixed_end and sweep["start_frame"] >= beat[0],
                        "whole sweep happens while the camera is fixed",
                        [sweep["start_frame"], sweep["end_frame"]], [beat[0], fixed_end], "frames"))

    # --- A-HERO-16 -------------------------------------------------------------------------------
    checks.append(check(len(beams) == 4, "A-HERO-16 exactly four primary sensing lines", beams, 4, "objects"))
    checks.append(check(max(r["beam_tip_error_m"] for r in acquiring) <= 25.0,
                        "A-HERO-16 every line ends on its corner anchor, every acquisition frame",
                        round(max(r["beam_tip_error_m"] for r in acquiring), 3), 25.0, "m"))
    checks.append(check(max(r["beam_root_error_m"] for r in acquiring) <= 25.0,
                        "every line starts on the platform", round(max(r["beam_root_error_m"] for r in acquiring), 3),
                        25.0, "m"))
    scene.frame_set(int(beat[0]))
    depsgraph = bpy.context.evaluated_depsgraph_get()
    centre = bpy.data.objects["aoi_target_center"].evaluated_get(depsgraph).matrix_world.translation
    diagonal_error, scales = 0.0, []
    for corner_id in corner_ids:
        anchor = bpy.data.objects["aoi_target_" + corner_id].evaluated_get(depsgraph).matrix_world.translation - centre
        true = bpy.data.objects["aoi_true_" + corner_id].evaluated_get(depsgraph).matrix_world.translation - centre
        # compare directions in the tangent plane at the centre
        normal = centre.normalized()
        anchor_t, true_t = anchor - normal * anchor.dot(normal), true - normal * true.dot(normal)
        diagonal_error = max(diagonal_error, angle_deg(anchor_t, true_t))
        scales.append(anchor_t.length / true_t.length)
    checks.append(check(diagonal_error <= 0.05, "line anchors lie on the true footprint's own diagonals",
                        round(diagonal_error, 5), 0.05, "deg"))

    # --- platform readability on the integrated page ------------------------------------------------
    clipped = [r["frame"] for r in acquiring if r["sat"]["bbox"] is None or r["sat"]["bbox"][0] < 0.0
               or r["sat"]["bbox"][2] > 1.0 or r["sat"]["bbox"][1] < 0.0 or r["sat"]["bbox"][3] > 1.0]
    checks.append(check(not clipped, "A-HERO-12 platform unclipped through the acquisition beat", clipped, [], "frames"))
    left_edge = min(r["sat"]["bbox"][0] for r in acquiring)
    checks.append(check(left_edge >= copy_edge, "A-HERO-13 platform silhouette stays right of the hero copy column "
                        "(1440 x 900 page)", round(left_edge, 4), copy_edge, "frame x"))
    widths = [r["sat"]["bbox"][2] - r["sat"]["bbox"][0] for r in acquiring]
    checks.append(check(0.08 <= min(widths) and max(widths) <= 0.25, "platform on-screen width while acquiring",
                        [round(min(widths), 4), round(max(widths), 4)], [0.08, 0.25], "frame widths"))
    drift = max(math.dist(r["sat"]["centre"], acquiring[0]["sat"]["centre"]) for r in acquiring)
    checks.append(check(drift <= 0.04, "platform holds its place while acquiring", round(drift, 4), 0.04, "frame widths"))
    emerge = next((r for a, r in zip(rows, rows[1:]) if a["sat"]["occluded"] and not r["sat"]["occluded"]), None)
    checks.append(check(bool(emerge) and rows[0]["sat"]["occluded"] and emerge["sat"]["centre"][0] < 0.45,
                        "platform is hidden at the open and comes round the left limb",
                        None if not emerge else {"frame": emerge["frame"], "at": emerge["sat"]["centre"]},
                        "x < 0.45", "frame x"))
    after = [r for r in rows if r["frame"] >= int(spec["camera"]["composition"]["analysis_hold"]["frame"])]
    checks.append(check(all(r["sat"]["bbox"] is None or r["sat"]["bbox"][2] < 0.0 or r["sat"]["bbox"][3] < 0.0
                            or r["sat"]["bbox"][0] > 1.0 for r in after),
                        "platform has left the frame before the hold", True, True, ""))

    # --- one persistent lock frame --------------------------------------------------------------
    shown = [r for r in rows if r["frame"] >= int(aoi["border"]["appear_end_frame"])]
    checks.append(check(min(r["frame_min_clearance_m"] for r in shown) >= 50.0,
                        "no lock-frame ribbon (border, halo, corner locks) dips under the surface while it tightens",
                        round(min(r["frame_min_clearance_m"] for r in shown), 1), 50.0, "m above the sphere"))
    checks.append(check(1.2 <= min(r["border_px"] for r in shown) and max(r["border_px"] for r in shown) <= 3.2,
                        "frame line weight stays inside its screen-space band",
                        [round(min(r["border_px"] for r in shown), 2), round(max(r["border_px"] for r in shown), 2)],
                        [1.2, 3.2], "px at 1920, most foreshortened edge"))
    if glow is not None:
        checks.append(check(7.0 <= min(r["glow_px"] for r in shown) and max(r["glow_px"] for r in shown) <= 22.0,
                            "frame halo stays inside its screen-space band",
                            [round(min(r["glow_px"] for r in shown), 2), round(max(r["glow_px"] for r in shown), 2)],
                            [7.0, 22.0], "px at 1920"))
    steps = [abs(b["frame_width_fraction"] - a["frame_width_fraction"]) for a, b in zip(shown, shown[1:])]
    checks.append(check(max(steps) <= 0.012, "frame size changes continuously: no swap, no pop",
                        round(max(steps), 5), 0.012, "frame widths per frame"))
    settled = by_frame[int(spec["camera"]["composition"]["analysis_hold"]["frame"])]
    checks.append(check(settled["frame_to_true_corner_m"] <= 5.0 and rows[-1]["frame_to_true_corner_m"] <= 5.0,
                        "settled lock frame sits on the true footprint corners",
                        round(max(settled["frame_to_true_corner_m"], rows[-1]["frame_to_true_corner_m"]), 3), 5.0, "m"))

    # --- A-HERO-17 ----------------------------------------------------------------------------------
    box = rows[-1]["frame_bbox"]
    lo, hi = spec["camera"]["composition"]["analysis_hold"]["width_fraction"]
    checks.append(check(box[0] >= copy_edge + 0.05 and box[2] <= 0.92 and 0.25 <= (box[1] + box[3]) / 2 <= 0.75,
                        "A-HERO-17 settled footprint is right-middle and clear of the copy column", box,
                        "x0 >= " + str(copy_edge + 0.05) + ", x1 <= 0.92, centre y 0.25-0.75", "frame"))
    checks.append(check(lo <= box[2] - box[0] <= hi, "settled footprint width", round(box[2] - box[0], 4), [lo, hi],
                        "frame widths"))

    # --- A-HERO-18 / 19 -----------------------------------------------------------------------------
    relief_record = {}
    if relief is not None:
        scene.frame_set(end)
        depsgraph = bpy.context.evaluated_depsgraph_get()
        n = int(objects["aoi_relief"]["grid"])
        evaluated = relief.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        index = {"nw": 0, "ne": n - 1, "se": n * n - 1, "sw": n * (n - 1)}
        worst = 0.0
        for corner_id in corner_ids:
            point = evaluated.matrix_world @ mesh.vertices[index[corner_id]].co
            true = bpy.data.objects["aoi_true_" + corner_id].evaluated_get(depsgraph).matrix_world.translation
            worst = max(worst, angular_m(point, true, radius_bu))
        heights = [(evaluated.matrix_world @ v.co).length for v in mesh.vertices[: n * n]]
        uv_layers = len(mesh.uv_layers)
        evaluated.to_mesh_clear()
        relief_record = {
            "corner_registration_m": round(worst, 3),
            "lift_km": [round((min(heights) - radius_bu) * 1000.0, 3), round((max(heights) - radius_bu) * 1000.0, 3)],
            "uv_layers": uv_layers,
            "vertical_exaggeration": objects["aoi_relief"]["vertical_exaggeration"],
            "geometry_source": objects["aoi_relief"]["dem"],
        }
        checks.append(check(worst <= 5.0, "A-HERO-18 relief corners sit on the true footprint corners",
                            round(worst, 3), 5.0, "m"))
        checks.append(check(uv_layers == 1, "A-HERO-18 every display layer reads one shared UV", uv_layers, 1, "layers"))
        checks.append(check(relief_record["lift_km"][1] - relief_record["lift_km"][0] >= 3.0,
                            "A-HERO-18 DEM relief is present in the geometry", relief_record["lift_km"], 3.0, "km"))
    order = materials["aoi_relief_layers"]["layer_order"]
    sequence = []
    for r in rows:
        lead = max(order, key=lambda name: r["layers"][name] or 0.0)
        if (r["layers"][lead] or 0.0) > 0.5 and (not sequence or sequence[-1] != lead):
            sequence.append(lead)
    checks.append(check(sequence == order, "A-HERO-18 layers lead in the locked order", sequence, order, ""))
    final = rows[-1]["layers"]
    checks.append(check(abs(final["priority"] - 1.0) <= 1.0e-4 and
                        all((final[name] or 0.0) <= 1.0e-4 for name in order if name != "priority"),
                        "A-HERO-19 final frame shows the priority layer alone", final,
                        {"priority": 1.0, "others": 0.0}, "weight"))
    hold = [r for r in rows if abs((r["layers"]["priority"] or 0.0) - 1.0) <= 1.0e-4]
    checks.append(check(len(hold) >= 18, "A-HERO-19 priority-only hold is long enough to read", len(hold), 18, "frames"))

    # --- governed grid vs the fixture the hero draws from --------------------------------------------
    ingest = hc.EVIDENCE_DIR / "web005a_r3_preview" / "analytical_asset_ingest.json"
    residual = None
    if ingest.is_file():
        grid = hc.load_json(ingest).get("grid") or {}
        if grid:
            x0, y1 = float(grid["origin_x"]), float(grid["origin_y"])
            x1 = x0 + float(grid["width"]) * float(grid["resolution_x"])
            y0 = y1 - float(grid["height"]) * float(grid["resolution_y"])
            governed = {"nw": (x0, y1), "ne": (x1, y1), "se": (x1, y0), "sw": (x0, y0)}
            description = ax.describe(scene_config, aoi["fixture"], spec)
            fixture_geo = dict(zip(description["corner_order"], description["corner_geographic"]))
            residual = {}
            for corner_id, (easting, northing) in governed.items():
                a = ax.geographic_to_unit(*utm35n_inverse(easting, northing))
                b = ax.geographic_to_unit(*fixture_geo[corner_id])
                residual[corner_id] = round(angular_m(a, b, radius_bu), 1)
            checks.append(check(max(residual.values()) <= 90.0,
                                "fixture corners agree with the governed EPSG:32635 grid corners to under three cells",
                                residual, 90.0, "m"))

    keep = sorted({start, 24, 60, 104, 140, 152, 172, 186, 202, fixed_end, fixed_end + 1, 214, 230, 246, 262, 276,
                   316, 350, 378, 400, end})
    return {
        "scene": scene_id,
        "authority": "docs/web-005-polish-authority@473b48a00bfe85d3dbe1cfe7219105c2b5ec7574:"
                     "tasks/WEB-005A_R3_REVIEW_37152222.md",
        "frames_measured": len(rows),
        "fixed_through_frame": fixed_end,
        "anchor_scale_vs_true_footprint": [round(s, 4) for s in scales],
        "relief": relief_record,
        "governed_grid_residual_m": residual,
        "checks": checks,
        "passed": sum(1 for c in checks if c["ok"]),
        "failed": sum(1 for c in checks if not c["ok"]),
        "frames": [compact(by_frame[f]) for f in keep if f in by_frame],
    }


def spec_corner_order(scene_config):
    return list(scene_config.get("aoi_injection_interface", {}).get("corner_order", ax.CORNER_IDS))


def angular_m(a, b, radius_bu):
    """Surface separation of two points in metres, in double precision.

    ``Vector.angle`` is single precision and goes through acos near 1, which cannot resolve a
    kilometre at planetary radius, let alone a metre. Put both points on the sphere and measure
    the chord with Python floats instead.
    """
    pa, pb = [float(v) for v in a], [float(v) for v in b]
    la, lb = math.sqrt(sum(v * v for v in pa)), math.sqrt(sum(v * v for v in pb))
    return math.sqrt(sum((x / la - y / lb) ** 2 for x, y in zip(pa, pb))) * radius_bu * 1.0e6


def angle_deg(a, b):
    """Angle between two vectors in degrees via atan2(|a x b|, a . b), in double precision."""
    ax_, ay, az = (float(v) for v in a)
    bx, by, bz = (float(v) for v in b)
    cross = math.sqrt((ay * bz - az * by) ** 2 + (az * bx - ax_ * bz) ** 2 + (ax_ * by - ay * bx) ** 2)
    return math.degrees(math.atan2(cross, ax_ * bx + ay * by + az * bz))


def compact(row):
    out = {}
    for key, value in row.items():
        if isinstance(value, float):
            out[key] = round(value, 5)
        elif isinstance(value, dict):
            out[key] = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in value.items()}
        else:
            out[key] = value
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit the WEB-005A R3 preview-gate scene.")
    parser.add_argument("--scene", default="hero_r3_preview_gate")
    parser.add_argument("--out", default=None)
    args = parser.parse_args(hc.argv_after_double_dash())
    report = audit(args.scene)
    for item in report["checks"]:
        print(("  PASS  " if item["ok"] else "  FAIL  ") + item["label"] + "  ->  " + json.dumps(item["measured"]))
    print("[hero] preview gate audit: " + str(report["passed"]) + " passed, " + str(report["failed"]) + " failed")
    if args.out:
        out = Path(args.out)
        if not out.is_absolute():
            out = hc.REPO_ROOT / out
        hc.ensure_dir(out.parent)
        out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print("[hero] -> " + hc.relpath(out))


if __name__ == "__main__":
    main()
