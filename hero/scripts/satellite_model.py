"""Procedural generic Earth-observation satellite and orbital trail for the hero scene (WEB-005A R2).

Blender-only. Imported by ``build_scene.py`` and dispatched from its object/material vocabulary, so
``scene.json`` stays the single source of scene truth: every dimension, material and timing below
is read from the object spec, and nothing here names a public-site path.

Why a second procedural model rather than an external asset: the accepted WEB-HERO-001B satellite
was a bus, two flat panels and a cone -- enough to stand in for "a spacecraft" at 20 px, and
rejected by Product at review size as a flat cutout. The R2 lock asks for a volumetric body,
panels with visible thickness and segmentation, physically coherent material separation, and
restrained antenna/sensor detail, with no claim to a specific operational spacecraft. Building it
from primitives inside the lane keeps it rights-clean by construction (OrbGSS original, no
downloaded model to clear), keeps it configurable, and keeps its geometry generic: a boxy bus in
MLI, a nadir instrument deck, two three-segment arrays on yokes, a small dish, star trackers and a
thruster are the vocabulary of every civil EO platform and the signature of none.

Scale is a hero-scale fiction, exactly as it was in the accepted lane (the accepted bus was 220 km
long): nothing in space gives absolute scale away, so ``wingspan_bu`` is chosen for legibility at
the acquisition distance and recorded as such.

Self-shadowing is what makes a body read as volumetric, but a hero-scale model must never print
its shadow on the planet -- that reads as a marker. Cycles light linking solves both at once: the
primary sun stops shadowing from the satellite entirely, and a satellite-only sun of the same
direction and energy lights it with its own parts as the only blockers.
"""

from __future__ import annotations

import math

import bmesh
import bpy
from mathutils import Vector

import hero_common as hc
import orbit_plan as op


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def _rgba(color):
    return (float(color[0]), float(color[1]), float(color[2]), 1.0)


def _set_input(node, name, value):
    if name in node.inputs:
        node.inputs[name].default_value = value
        return True
    return False


def _link_new(name: str, mesh) -> bpy.types.Object:
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def _box(name, size, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), material=None,
         bevel=0.0, bevel_segments=3):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= size[0]
        v.co.y *= size[1]
        v.co.z *= size[2]
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = _link_new(name, mesh)
    obj.location = location
    obj.rotation_euler = rotation
    if material is not None:
        mesh.materials.append(material)
    if bevel > 0.0:
        mod = obj.modifiers.new("bevel", "BEVEL")
        mod.width = bevel
        mod.segments = int(bevel_segments)
        mod.limit_method = "ANGLE"
        mod.harden_normals = True
        for polygon in mesh.polygons:
            polygon.use_smooth = True
        _smooth_by_angle(obj, 35.0)
    return obj


def _cylinder(name, radius, depth, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0),
              material=None, vertices=32, radius_top=None, smooth=True):
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=int(vertices),
        radius1=float(radius), radius2=float(radius if radius_top is None else radius_top),
        depth=float(depth),
    )
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = _link_new(name, mesh)
    obj.location = location
    obj.rotation_euler = rotation
    if material is not None:
        mesh.materials.append(material)
    if smooth:
        for polygon in mesh.polygons:
            polygon.use_smooth = True
        _smooth_by_angle(obj, 40.0)
    return obj


def _smooth_by_angle(obj, angle_deg: float) -> None:
    """Sharp caps, smooth sides: an edge-split at the given angle, robust across 4.x."""
    mod = obj.modifiers.new("edge_split", "EDGE_SPLIT")
    mod.split_angle = math.radians(angle_deg)
    mod.use_edge_sharp = True


def _dish(name, radius, depth, thickness, material=None, steps=48):
    """A parabolic reflector with real thickness, by spinning a two-rail profile.

    The reflector opens toward local +Z; the feed sits at the focus above it.
    """
    bm = bmesh.new()
    k = depth / (radius * radius)
    rail = 14
    outer = []
    inner = []
    for index in range(rail + 1):
        r = radius * index / rail
        z = k * r * r
        outer.append(bm.verts.new((r, 0.0, z)))
    for index in range(rail, -1, -1):
        r = max(0.0, radius * index / rail - (thickness if index == rail else 0.0))
        z = k * r * r - thickness
        inner.append(bm.verts.new((r, 0.0, z)))
    profile = outer + inner
    edges = [bm.edges.new((profile[i], profile[i + 1])) for i in range(len(profile) - 1)]
    bmesh.ops.spin(
        bm, geom=profile + edges, cent=(0.0, 0.0, 0.0), axis=(0.0, 0.0, 1.0),
        dvec=(0.0, 0.0, 0.0), angle=2.0 * math.pi, steps=int(steps), use_merge=True,
    )
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = _link_new(name, mesh)
    if material is not None:
        mesh.materials.append(material)
    for polygon in mesh.polygons:
        polygon.use_smooth = True
    _smooth_by_angle(obj, 50.0)
    return obj


def _parent(child, parent):
    child.parent = parent
    return child


# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------

def build_mli_material(name: str, spec: dict, scene_config: dict):
    """Multi-layer-insulation foil: metallic, warm, with a fine crinkle in the normal.

    The crinkle is a Noise texture driven into a Bump node in object space, so it is a surface
    response to light rather than a painted pattern -- what makes foil read as foil when the sun
    rakes across it.
    """
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    nt = material.node_tree
    nodes, links = nt.nodes, nt.links
    bsdf = nodes.get("Principled BSDF")
    base = hc.palette_color(scene_config, spec["base_color_ref"])
    bsdf.inputs["Base Color"].default_value = _rgba(base)
    bsdf.inputs["Roughness"].default_value = float(spec.get("roughness", 0.38))
    bsdf.inputs["Metallic"].default_value = float(spec.get("metallic", 0.55))
    _set_input(bsdf, "Specular IOR Level", float(spec.get("specular", 0.7)))

    tex_coord = nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-900, -200)
    noise = nodes.new("ShaderNodeTexNoise")
    noise.location = (-650, -200)
    _set_input(noise, "Scale", float(spec.get("crinkle_scale", 60.0)))
    _set_input(noise, "Detail", 6.0)
    _set_input(noise, "Roughness", 0.65)
    links.new(tex_coord.outputs["Object"], noise.inputs["Vector"])
    bump = nodes.new("ShaderNodeBump")
    bump.location = (-350, -250)
    bump.inputs["Strength"].default_value = float(spec.get("crinkle_strength", 0.18))
    bump.inputs["Distance"].default_value = float(spec.get("crinkle_distance", 0.02))
    fac = "Fac" if "Fac" in noise.outputs else noise.outputs[0].name
    links.new(noise.outputs[fac], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

    # A very faint roughness variation so the foil is not one uniform mirror.
    rough_noise = nodes.new("ShaderNodeTexNoise")
    rough_noise.location = (-650, -500)
    _set_input(rough_noise, "Scale", 9.0)
    links.new(tex_coord.outputs["Object"], rough_noise.inputs["Vector"])
    rough_range = nodes.new("ShaderNodeMapRange")
    rough_range.location = (-400, -500)
    rough_range.inputs["From Min"].default_value = 0.3
    rough_range.inputs["From Max"].default_value = 0.7
    rough_range.inputs["To Min"].default_value = float(spec.get("roughness", 0.32)) * 0.8
    rough_range.inputs["To Max"].default_value = float(spec.get("roughness", 0.32)) * 1.25
    rough_range.clamp = True
    links.new(rough_noise.outputs[fac], rough_range.inputs["Value"])
    links.new(rough_range.outputs["Result"], bsdf.inputs["Roughness"])
    return material


def build_surface_material(name: str, spec: dict, scene_config: dict):
    """Plain dielectric/metal surface (radiator, composite structure, optics, silver)."""
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    base = hc.palette_color(scene_config, spec["base_color_ref"])
    bsdf.inputs["Base Color"].default_value = _rgba(base)
    bsdf.inputs["Roughness"].default_value = float(spec.get("roughness", 0.5))
    bsdf.inputs["Metallic"].default_value = float(spec.get("metallic", 0.0))
    _set_input(bsdf, "Specular IOR Level", float(spec.get("specular", 0.5)))
    if spec.get("coat_weight"):
        _set_input(bsdf, "Coat Weight", float(spec["coat_weight"]))
        _set_input(bsdf, "Coat Roughness", float(spec.get("coat_roughness", 0.08)))
    return material


def build_solar_cell_material(name: str, spec: dict, scene_config: dict):
    """Segmented photovoltaic surface: deep-blue cells under a glossy cover glass, with a fine
    cell grid and a coarser bus-bar grid. Segmentation is real geometry in the model; the grids
    here are what a viewer reads as cells at review size.
    """
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    nt = material.node_tree
    nodes, links = nt.nodes, nt.links
    bsdf = nodes.get("Principled BSDF")
    output = nodes.get("Material Output")
    base = hc.palette_color(scene_config, spec["base_color_ref"])
    grid_color = hc.palette_color(scene_config, spec.get("grid_color_ref", "satellite_busbar"))
    bsdf.inputs["Roughness"].default_value = float(spec.get("roughness", 0.16))
    bsdf.inputs["Metallic"].default_value = float(spec.get("metallic", 0.3))
    _set_input(bsdf, "Coat Weight", float(spec.get("coat_weight", 0.7)))
    _set_input(bsdf, "Coat Roughness", float(spec.get("coat_roughness", 0.06)))
    _set_input(bsdf, "Specular IOR Level", 0.7)

    tex_coord = nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-900, 0)
    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (-700, 0)
    mapping.inputs["Scale"].default_value = (
        float(spec.get("cells_across", 6.0)), float(spec.get("cells_along", 14.0)), 1.0
    )
    links.new(tex_coord.outputs["UV"], mapping.inputs["Vector"])

    fine = nodes.new("ShaderNodeTexBrick")
    fine.location = (-450, 100)
    _set_input(fine, "Color1", _rgba(base))
    _set_input(fine, "Color2", _rgba([c * 0.85 for c in base]))
    _set_input(fine, "Mortar", _rgba(grid_color))
    _set_input(fine, "Scale", 1.0)
    _set_input(fine, "Mortar Size", float(spec.get("grid_line_width", 0.035)))
    _set_input(fine, "Row Height", 1.0)
    _set_input(fine, "Bias", 0.0)
    fine.offset = 0.0
    fine.squash = 1.0
    links.new(mapping.outputs["Vector"], fine.inputs["Vector"])
    links.new(fine.outputs["Color"], bsdf.inputs["Base Color"])

    # Bus bars: a very faint emissive trace so the array keeps structure in shadow.
    emission = nodes.new("ShaderNodeEmission")
    emission.location = (-150, -300)
    emission.inputs["Color"].default_value = _rgba(grid_color)
    emission.inputs["Strength"].default_value = float(spec.get("grid_emission_strength", 0.12))
    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (150, -100)
    links.new(fine.outputs["Fac"], mix.inputs["Fac"])
    links.new(bsdf.outputs["BSDF"], mix.inputs[1])
    links.new(emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], output.inputs["Surface"])
    return material


def build_trail_material(name: str, spec: dict, scene_config: dict):
    """Orbital trail: emissive ribbon visible only for a window of arc behind the moving head.

    The ribbon carries the orbit angle as U (0..1 around the full circle). A keyframed value
    node ``trail_head`` holds the satellite's angle in the same units, so the visible segment
    is (head - u) mod 1 within ``window``, fading to nothing at its tail and clear of the head
    so it never overlaps the spacecraft itself.
    """
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    for attribute, value in (("surface_render_method", "BLENDED"), ("blend_method", "BLEND")):
        try:
            setattr(material, attribute, value)
        except (AttributeError, TypeError):
            pass
    nt = material.node_tree
    nodes, links = nt.nodes, nt.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (900, 0)

    tex_coord = nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-900, 0)
    separate = nodes.new("ShaderNodeSeparateXYZ")
    separate.location = (-700, 0)
    links.new(tex_coord.outputs["UV"], separate.inputs["Vector"])

    head = nodes.new("ShaderNodeValue")
    head.name = "trail_head"
    head.label = "trail_head"
    head.location = (-700, -200)
    head.outputs[0].default_value = 0.0

    behind = nodes.new("ShaderNodeMath")
    behind.operation = "SUBTRACT"
    behind.location = (-500, -100)
    links.new(head.outputs[0], behind.inputs[0])
    links.new(separate.outputs["X"], behind.inputs[1])
    wrapped = nodes.new("ShaderNodeMath")
    wrapped.operation = "WRAP"
    wrapped.location = (-320, -100)
    wrapped.inputs[1].default_value = 0.0
    wrapped.inputs[2].default_value = 1.0
    links.new(behind.outputs[0], wrapped.inputs[0])

    window = float(spec.get("window_turns", 0.09))
    gap = float(spec.get("head_gap_turns", 0.004))
    fade = nodes.new("ShaderNodeMapRange")
    fade.location = (-120, -100)
    fade.interpolation_type = "SMOOTHSTEP"
    fade.clamp = True
    fade.inputs["From Min"].default_value = gap
    fade.inputs["From Max"].default_value = window
    fade.inputs["To Min"].default_value = 1.0
    fade.inputs["To Max"].default_value = 0.0
    links.new(wrapped.outputs[0], fade.inputs["Value"])

    # Soft across the ribbon width too, so it is a line of light rather than a tape.
    across = nodes.new("ShaderNodeMath")
    across.operation = "SUBTRACT"
    across.location = (-500, -320)
    across.inputs[1].default_value = 0.5
    links.new(separate.outputs["Y"], across.inputs[0])
    across_abs = nodes.new("ShaderNodeMath")
    across_abs.operation = "ABSOLUTE"
    across_abs.location = (-320, -320)
    links.new(across.outputs[0], across_abs.inputs[0])
    across_fade = nodes.new("ShaderNodeMapRange")
    across_fade.location = (-120, -320)
    across_fade.interpolation_type = "SMOOTHSTEP"
    across_fade.clamp = True
    across_fade.inputs["From Min"].default_value = 0.1
    across_fade.inputs["From Max"].default_value = 0.5
    across_fade.inputs["To Min"].default_value = 1.0
    across_fade.inputs["To Max"].default_value = 0.0
    links.new(across_abs.outputs[0], across_fade.inputs["Value"])

    profile = nodes.new("ShaderNodeMath")
    profile.operation = "MULTIPLY"
    profile.location = (100, -200)
    links.new(fade.outputs["Result"], profile.inputs[0])
    links.new(across_fade.outputs["Result"], profile.inputs[1])

    presence = nodes.new("ShaderNodeValue")
    presence.name = "aoi_presence"
    presence.label = "aoi_presence"
    presence.location = (100, -400)
    presence.outputs[0].default_value = 1.0
    alpha = nodes.new("ShaderNodeMath")
    alpha.operation = "MULTIPLY"
    alpha.location = (300, -250)
    alpha.use_clamp = True
    links.new(profile.outputs[0], alpha.inputs[0])
    links.new(presence.outputs[0], alpha.inputs[1])
    alpha_scaled = nodes.new("ShaderNodeMath")
    alpha_scaled.operation = "MULTIPLY"
    alpha_scaled.location = (480, -250)
    alpha_scaled.inputs[1].default_value = float(spec.get("alpha", 0.55))
    links.new(alpha.outputs[0], alpha_scaled.inputs[0])

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (480, 100)
    emission.inputs["Color"].default_value = _rgba(
        hc.palette_color(scene_config, spec["emission_color_ref"])
    )
    emission.inputs["Strength"].default_value = float(spec.get("emission_strength", 3.0))
    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (480, 300)
    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (700, 0)
    links.new(alpha_scaled.outputs[0], mix.inputs["Fac"])
    links.new(transparent.outputs["BSDF"], mix.inputs[1])
    links.new(emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], output.inputs["Surface"])
    return material


# ---------------------------------------------------------------------------
# The satellite
# ---------------------------------------------------------------------------

def build_eo_satellite(spec: dict, materials: dict, context: dict):
    """Generic EO platform, parented to one root empty; local -Z is nadir, +X the array axis.

    Proportions are relative to ``wingspan_bu`` (tip to tip). Every part is a real solid with
    thickness, so silhouettes have edges and faces catch light differently -- the two things a
    flat cutout cannot do.
    """
    root = bpy.data.objects.new(spec["id"], None)
    root.empty_display_size = 0.05
    bpy.context.collection.objects.link(root)
    root.location = tuple(spec.get("location", (0.0, 0.0, 0.0)))

    # Attitude about nadir. The root carries the animation and the nadir/aim constraints; the body
    # empty adds a fixed yaw about the nadir axis (and an optional roll) so the array axis can be
    # oriented for the shot -- real platforms fly with the array axis perpendicular to the orbit
    # plane, which for this pass would point the wings straight at the camera and collapse the
    # silhouette to a dot. Parts hang from the body, so the audit reads the wing tips from it.
    body = bpy.data.objects.new(spec["id"] + "_body", None)
    body.empty_display_size = 0.04
    bpy.context.collection.objects.link(body)
    body.rotation_euler = (
        math.radians(float(spec.get("roll_deg", 0.0))),
        0.0,
        math.radians(float(spec.get("yaw_deg", 0.0))),
    )
    body.parent = root
    assembly_root = root
    root = body

    wingspan = float(spec.get("wingspan_bu", 0.8))
    p = dict(spec.get("proportions", {}))

    def prop(key, default):
        return float(p.get(key, default)) * wingspan

    mat = {key: materials.get(spec.get(key + "_material")) for key in
           ("hull", "structure", "radiator", "panel", "panel_frame", "antenna", "optics")}

    parts = []

    # --- bus -------------------------------------------------------------
    bus_x, bus_y, bus_z = prop("bus_x", 0.15), prop("bus_y", 0.11), prop("bus_z", 0.13)
    bus = _box(spec["id"] + "_bus", (bus_x, bus_y, bus_z), material=mat["hull"],
               bevel=bus_y * 0.07)
    parts.append(_parent(bus, root))

    # structural end frames (dark composite) top and bottom of the bus: material separation
    for sign, name in ((1.0, "top"), (-1.0, "deck")):
        frame = _box(spec["id"] + "_" + name + "_frame", (bus_x * 1.04, bus_y * 1.04, bus_z * 0.09),
                     location=(0.0, 0.0, sign * bus_z * 0.5), material=mat["structure"],
                     bevel=bus_y * 0.02)
        parts.append(_parent(frame, root))

    # radiator plate on the +Y face
    radiator = _box(spec["id"] + "_radiator", (bus_x * 0.62, bus_y * 0.03, bus_z * 0.55),
                    location=(0.0, bus_y * 0.515, bus_z * 0.05), material=mat["radiator"],
                    bevel=bus_y * 0.008)
    parts.append(_parent(radiator, root))

    # electronics box + omni antenna on the -Y face
    ebox = _box(spec["id"] + "_ebox", (bus_x * 0.28, bus_y * 0.12, bus_z * 0.24),
                location=(bus_x * 0.18, -bus_y * 0.56, -bus_z * 0.12), material=mat["hull"],
                bevel=bus_y * 0.012)
    parts.append(_parent(ebox, root))
    omni = _cylinder(spec["id"] + "_omni", bus_y * 0.012, bus_y * 0.55,
                     location=(-bus_x * 0.28, -bus_y * 0.75, bus_z * 0.2),
                     rotation=(math.radians(90.0), 0.0, 0.0), material=mat["antenna"], vertices=12)
    parts.append(_parent(omni, root))

    # --- nadir instrument deck ------------------------------------------
    deck_z = -bus_z * 0.5
    main_r = prop("instrument_radius", 0.032)
    main_len = prop("instrument_length", 0.075)
    telescope = _cylinder(spec["id"] + "_instrument", main_r, main_len,
                          location=(-bus_x * 0.12, bus_y * 0.05, deck_z - main_len * 0.5),
                          material=mat["structure"], vertices=40)
    parts.append(_parent(telescope, root))
    baffle = _cylinder(spec["id"] + "_baffle", main_r * 1.12, main_len * 0.12,
                       location=(-bus_x * 0.12, bus_y * 0.05, deck_z - main_len * 0.97),
                       material=mat["antenna"], vertices=40)
    parts.append(_parent(baffle, root))
    aperture = _cylinder(spec["id"] + "_aperture", main_r * 0.86, main_len * 0.02,
                         location=(-bus_x * 0.12, bus_y * 0.05, deck_z - main_len * 1.03),
                         material=mat["optics"], vertices=40)
    parts.append(_parent(aperture, root))
    # a second, smaller instrument (box housing with a short barrel)
    second = _box(spec["id"] + "_instrument2", (bus_x * 0.22, bus_y * 0.22, bus_z * 0.2),
                  location=(bus_x * 0.26, -bus_y * 0.18, deck_z - bus_z * 0.1),
                  material=mat["hull"], bevel=bus_y * 0.012)
    parts.append(_parent(second, root))
    barrel = _cylinder(spec["id"] + "_barrel", main_r * 0.42, main_len * 0.45,
                       location=(bus_x * 0.26, -bus_y * 0.18, deck_z - bus_z * 0.2 - main_len * 0.22),
                       material=mat["structure"], vertices=28)
    parts.append(_parent(barrel, root))

    # --- solar arrays ----------------------------------------------------
    segments = int(p.get("panel_segments", 3))
    seg_len = prop("panel_segment_length", 0.115)
    seg_w = prop("panel_width", 0.12)
    seg_t = prop("panel_thickness", 0.006)
    gap = prop("panel_gap", 0.006)
    yoke_len = prop("yoke_length", 0.05)
    tilt = math.radians(float(spec.get("array_tilt_deg", 0.0)))
    for sign, side in ((1.0, "pos"), (-1.0, "neg")):
        pivot = bpy.data.objects.new(spec["id"] + "_array_" + side, None)
        pivot.empty_display_size = 0.02
        bpy.context.collection.objects.link(pivot)
        pivot.location = (sign * bus_x * 0.5, 0.0, bus_z * 0.12)
        pivot.rotation_euler = (tilt, 0.0, 0.0)
        _parent(pivot, root)

        yoke = _cylinder(spec["id"] + "_yoke_" + side, seg_w * 0.035, yoke_len,
                         location=(sign * yoke_len * 0.5, 0.0, 0.0),
                         rotation=(0.0, math.radians(90.0), 0.0), material=mat["antenna"], vertices=14)
        parts.append(_parent(yoke, pivot))
        hinge = _box(spec["id"] + "_hinge_" + side, (seg_w * 0.08, seg_w * 0.14, seg_w * 0.1),
                     location=(sign * yoke_len, 0.0, 0.0), material=mat["structure"],
                     bevel=seg_w * 0.006)
        parts.append(_parent(hinge, pivot))

        x = yoke_len
        for index in range(segments):
            centre = sign * (x + seg_len * 0.5)
            frame = _box(spec["id"] + "_panelframe_" + side + str(index),
                         (seg_len, seg_w, seg_t),
                         location=(centre, 0.0, 0.0), material=mat["panel_frame"],
                         bevel=seg_t * 0.3)
            parts.append(_parent(frame, pivot))
            cells = _box(spec["id"] + "_cells_" + side + str(index),
                         (seg_len * 0.93, seg_w * 0.92, seg_t * 0.5),
                         location=(centre, 0.0, seg_t * 0.42), material=mat["panel"])
            parts.append(_parent(cells, pivot))
            # back face: pale substrate plate plus a dark spar, so the wing reads from both sides
            back = _box(spec["id"] + "_panelback_" + side + str(index),
                        (seg_len * 0.93, seg_w * 0.92, seg_t * 0.3),
                        location=(centre, 0.0, -seg_t * 0.5), material=mat["radiator"])
            parts.append(_parent(back, pivot))
            spar = _box(spec["id"] + "_spar_" + side + str(index),
                        (seg_len * 0.98, seg_w * 0.05, seg_t * 0.9),
                        location=(centre, 0.0, -seg_t * 0.7), material=mat["structure"])
            parts.append(_parent(spar, pivot))
            if index < segments - 1:
                link = _box(spec["id"] + "_hingelink_" + side + str(index),
                            (gap * 1.6, seg_w * 0.18, seg_t * 1.4),
                            location=(sign * (x + seg_len + gap * 0.5), 0.0, 0.0),
                            material=mat["structure"])
                parts.append(_parent(link, pivot))
            x += seg_len + gap

    # --- antenna dish, star trackers, thruster ---------------------------
    dish_r = prop("dish_radius", 0.03)
    dish = _dish(spec["id"] + "_dish", dish_r, dish_r * 0.32, dish_r * 0.05, material=mat["antenna"])
    dish.location = (bus_x * 0.3, bus_y * 0.62, bus_z * 0.34)
    dish.rotation_euler = (math.radians(-118.0), 0.0, math.radians(-12.0))
    parts.append(_parent(dish, root))
    feed = _cylinder(spec["id"] + "_feed", dish_r * 0.07, dish_r * 0.9,
                     location=(0.0, 0.0, dish_r * 0.45), material=mat["antenna"], vertices=10)
    parts.append(_parent(feed, dish))
    horn = _cylinder(spec["id"] + "_horn", dish_r * 0.1, dish_r * 0.12,
                     location=(0.0, 0.0, dish_r * 0.9), material=mat["structure"], vertices=12,
                     radius_top=dish_r * 0.16)
    parts.append(_parent(horn, dish))
    mount = _cylinder(spec["id"] + "_dishmount", dish_r * 0.16, bus_y * 0.24,
                      location=(bus_x * 0.3, bus_y * 0.5, bus_z * 0.34),
                      rotation=(math.radians(90.0), 0.0, 0.0), material=mat["structure"], vertices=12)
    parts.append(_parent(mount, root))

    for index, (dx, ang) in enumerate(((-0.34, 28.0), (-0.22, 42.0))):
        tracker = _cylinder(spec["id"] + "_tracker" + str(index), bus_y * 0.045, bus_y * 0.2,
                            location=(bus_x * dx, -bus_y * 0.42, bus_z * 0.44),
                            rotation=(math.radians(ang), math.radians(18.0), 0.0),
                            material=mat["structure"], vertices=18)
        parts.append(_parent(tracker, root))
        cap = _cylinder(spec["id"] + "_trackercap" + str(index), bus_y * 0.032, bus_y * 0.01,
                        location=(0.0, 0.0, bus_y * 0.105), material=mat["optics"], vertices=18)
        parts.append(_parent(cap, tracker))

    nozzle = _cylinder(spec["id"] + "_thruster", bus_y * 0.05, bus_z * 0.14,
                       location=(bus_x * 0.12, bus_y * 0.12, bus_z * 0.5 + bus_z * 0.07),
                       material=mat["antenna"], vertices=20, radius_top=bus_y * 0.09)
    parts.append(_parent(nozzle, root))

    # --- assembly-level settings --------------------------------------
    scale = float(spec.get("scale", 1.0))
    assembly_root.scale = (scale, scale, scale)
    context.setdefault("satellite_parts", {})[spec["id"]] = parts
    return assembly_root


def build_orbit_trail(spec: dict, materials: dict, context: dict):
    """Thin emissive ribbon around the followed object's orbit circle, in world space.

    The circle comes from the followed object's ``orbit_intent`` through ``orbit_plan``, so the
    trail cannot disagree with the pass it decorates. U runs 0..1 around the circle from the
    anchor; ``trail_head`` is keyframed to the satellite's angle at every keyframe frame with
    LINEAR interpolation, which is exact for a constant-rate pass.
    """
    scene_config = context["scene_config"]
    scene_spec = context["scene_spec"]
    followed = op._object_spec(scene_spec, spec["follow_object_id"]) or {}
    intent = followed.get("orbit_intent")
    if not intent:
        raise KeyError("orbit_trail " + spec["id"] + " follows " + repr(spec.get("follow_object_id"))
                       + ", which declares no orbit_intent")
    u_axis, v_axis, radius_bu = op.orbit_basis(scene_config, scene_spec, intent)
    samples = int(spec.get("samples", 720))
    width_bu = float(spec.get("width_km", 5.0)) / 1000.0
    normal = Vector(u_axis).cross(Vector(v_axis)).normalized()

    verts, uvs = [], []
    for index in range(samples + 1):
        turn = index / float(samples)
        theta = 2.0 * math.pi * turn
        point = (Vector(u_axis) * math.cos(theta) + Vector(v_axis) * math.sin(theta)) * radius_bu
        # widen in the orbit plane's normal and radial directions: a flat band facing outward
        # reads the same from any camera side, so widen along the plane normal.
        for k, v_uv in ((-0.5, 0.0), (0.5, 1.0)):
            verts.append(point + normal * (k * width_bu))
            uvs.append((turn, v_uv))
    faces = []
    for index in range(samples):
        a = 2 * index
        faces.append((a, a + 1, a + 3, a + 2))
    mesh = bpy.data.meshes.new(spec["id"])
    mesh.from_pydata([tuple(v) for v in verts], [], faces)
    mesh.update()
    uv_layer = mesh.uv_layers.new(name="trail")
    for loop_index, loop in enumerate(mesh.loops):
        uv_layer.data[loop_index].uv = uvs[loop.vertex_index]
    obj = _link_new(spec["id"], mesh)
    material = materials.get(spec.get("material"))
    if material is not None:
        mesh.materials.append(material)
        node = material.node_tree.nodes.get("trail_head")
        if node is not None:
            socket = node.outputs[0]
            data_path = socket.path_from_id("default_value")
            for frame in sorted({int(f) for f in intent["keyframe_frames"]}):
                socket.default_value = op.orbit_angle_deg(intent, frame) / 360.0
                socket.keyframe_insert(data_path="default_value", frame=frame)
            animation = material.node_tree.animation_data
            action = animation.action if animation else None
            if action:
                for fcurve in _fcurves(action):
                    if fcurve.data_path == data_path:
                        for point in fcurve.keyframe_points:
                            point.interpolation = "LINEAR"
        presence = material.node_tree.nodes.get("aoi_presence")
        if presence is not None and spec.get("presence_keyframes"):
            socket = presence.outputs[0]
            for frame, value in spec["presence_keyframes"]:
                socket.default_value = float(value)
                socket.keyframe_insert(data_path="default_value", frame=int(frame))
    try:
        obj.visible_shadow = False
    except AttributeError:
        pass
    return obj


def _fcurves(action):
    curves = list(getattr(action, "fcurves", []) or [])
    if curves:
        return curves
    for layer in getattr(action, "layers", []):
        for strip in getattr(layer, "strips", []):
            for channelbag in getattr(strip, "channelbags", []):
                curves.extend(channelbag.fcurves)
    return curves


# ---------------------------------------------------------------------------
# Lighting isolation
# ---------------------------------------------------------------------------

def isolate_satellite_lighting(sun_object, satellite_ids, built_objects, spec: dict):
    """Light the satellite with its own copy of the sun so it self-shadows but never shadows Earth.

    Cycles light linking (4.0+): the primary sun keeps lighting everything except the satellite
    parts, with only the planet as a shadow blocker; a duplicate sun with the same direction and
    energy lights only the satellite parts, with only those parts as blockers.
    """
    if sun_object is None or not hasattr(sun_object, "light_linking"):
        return None
    parts = []
    for sat_id in satellite_ids:
        root = built_objects.get(sat_id)
        if root is None:
            continue
        stack = [root]
        while stack:
            obj = stack.pop()
            parts.append(obj)
            stack.extend(obj.children)
    part_set = {obj.name for obj in parts}

    sat_collection = bpy.data.collections.new("satellite_parts")
    bpy.context.scene.collection.children.link(sat_collection)
    for obj in parts:
        if obj.type == "MESH":
            sat_collection.objects.link(obj)

    world_receivers = bpy.data.collections.new("sun_receivers")
    bpy.context.scene.collection.children.link(world_receivers)
    world_blockers = bpy.data.collections.new("sun_blockers")
    bpy.context.scene.collection.children.link(world_blockers)
    for obj in bpy.context.scene.objects:
        if obj.type != "MESH" or obj.name in part_set:
            continue
        world_receivers.objects.link(obj)
        if getattr(obj, "visible_shadow", True):
            world_blockers.objects.link(obj)

    sun_object.light_linking.receiver_collection = world_receivers
    sun_object.light_linking.blocker_collection = world_blockers

    sat_sun_data = sun_object.data.copy()
    sat_sun_data.name = sun_object.data.name + "_satellite"
    sat_sun_data.energy = float(sun_object.data.energy) * float(spec.get("satellite_sun_gain", 1.0))
    sat_sun = bpy.data.objects.new(sun_object.name + "_satellite", sat_sun_data)
    bpy.context.collection.objects.link(sat_sun)
    sat_sun.location = sun_object.location
    sat_sun.rotation_euler = sun_object.rotation_euler
    sat_sun.light_linking.receiver_collection = sat_collection
    sat_sun.light_linking.blocker_collection = sat_collection
    return sat_sun
