"""WEB-005A R3: scan fan, persistent lock-frame morph and the DEM-relief analytical reveal.

Authority (docs/web-005-polish-authority):
  946cd8b  tasks/WEB-005A_R3_FIXED_CAMERA_GLOBE_DRAPE_REVISION.md   (phases A-G, A-HERO-15..19)
  db4605a  tasks/WEB-005A_R3_ANALYTICAL_ASSET_HANDOFF.md            (geometry / display-asset contract)
  473b48a  tasks/WEB-005A_R3_REVIEW_37152222.md                     (review disposition, preview gate)

Three things live here, and all three are built from the one resolved AOI description so nothing
can be registered to anything but the fixture:

``scan fan``
    Secondary support for the four sensing lines: a faint veil on the four faces of the pyramid
    they span, plus a *light curtain* -- a stack of translucent slices from the platform down to a
    north-south ground line, lit only near the keyed sweep position. The curtain and the ground
    band read the same keyed value, so they cross the footprint together by construction. Every
    apex vertex is hooked to the satellite, every ground vertex rides the Earth, exactly like the
    lines themselves: nothing is keyframed into place.

``lock-frame morph``
    The frame the viewer is shown is sized in screen space; the footprint it belongs to is not
    touched. Each ribbon is built at the true footprint (its basis) and carries a ``presented``
    shape key at the acquisition presentation. A straight blend between two points on a sphere
    cuts a chord under the surface, so a ``sag_comp`` key lifts every vertex by exactly the
    chord's sagitta, weighted 4m(1-m); the frame therefore stays on the globe while it tightens.

``relief``
    The footprint raised into terrain from the governed ``top-dem.tif`` -- and only from it. The
    coloured display textures are material on that geometry; none of them displaces anything.
    The lock frame gets a ``drape`` key from the same DEM samples, so it settles onto the rim of
    the relief instead of being buried by it.
"""

from __future__ import annotations

import math

import bpy
import numpy as np
from mathutils import Matrix

import aoi_system as ax
import hero_common as hc

METRES_PER_BU = ax.KM_PER_BLENDER_UNIT * 1000.0
# Transient clearance carried by the sagitta key (weight 4m(1-m): zero at both ends of the morph).
# The weight offset is linear in k while a rail's drop below its tangent plane is quadratic, and a
# tangent measured at the presentation tilts as the frame travels; both are tens of metres on a
# 56 km halo ribbon that only has 190 m of clearance. 200 m mid-morph is a tenth of a pixel.
MORPH_LIFT_BU = 200.0 / METRES_PER_BU


# ---------------------------------------------------------------------------
# Lock-frame morph
# ---------------------------------------------------------------------------

def add_morph_keys(obj, presented_verts, weighted_verts) -> None:
    """Give a ribbon built at the true footprint its presentation shape, sagitta lift and weight.

    ``presented_verts`` is the ribbon at the presentation span in its *settled* width;
    ``weighted_verts`` is the same ribbon, same place, in its *acquisition* width. Shape keys add,
    so ``presented`` moves the frame and ``weight`` only thickens it -- and the thickening offset
    is taken where the frame is heavy (at the presentation), not at the footprint: a tangent
    offset measured 300 km away picks up a radial component and pushes a rail under the globe.
    With both keys at 1 the ribbon is exactly the acquisition ribbon, on the sphere.
    """
    basis = obj.shape_key_add(name="Basis", from_mix=False)
    presented = obj.shape_key_add(name="presented", from_mix=False)
    sag = obj.shape_key_add(name="sag_comp", from_mix=False)
    weight = obj.shape_key_add(name="weight", from_mix=False)
    if len(presented_verts) != len(basis.data) or len(weighted_verts) != len(basis.data):
        raise ValueError(obj.name + ": presentation and footprint ribbons differ in vertex count")
    for index, (moved, heavy) in enumerate(zip(presented_verts, weighted_verts)):
        weight.data[index].co = basis.data[index].co + (_vec(heavy) - _vec(moved))
    weight.value = 1.0
    for index, target in enumerate(presented_verts):
        origin = basis.data[index].co
        presented.data[index].co = target
        chord = (origin - _vec(target)).length
        radius = origin.length
        sagitta = radius - math.sqrt(max(0.0, radius * radius - 0.25 * chord * chord))
        direction = (origin + _vec(target)).normalized()
        sag.data[index].co = origin + direction * (sagitta + MORPH_LIFT_BU)
    presented.value = 1.0
    sag.value = 0.0


def _vec(values):
    from mathutils import Vector
    return Vector(values)


def key_morph(obj, morph_keyframes, weight_keyframes=()) -> None:
    """Key ``presented`` = m, ``sag_comp`` = 4m(1-m) and ``weight`` = k, linearly between frames."""
    keys = obj.data.shape_keys
    if keys is None:
        return
    weight = keys.key_blocks["weight"]
    for frame, k in weight_keyframes:
        weight.value = float(k)
        weight.keyframe_insert(data_path="value", frame=int(frame))
    presented = keys.key_blocks["presented"]
    sag = keys.key_blocks["sag_comp"]
    for frame, m in morph_keyframes:
        presented.value = float(m)
        sag.value = 4.0 * float(m) * (1.0 - float(m))
        presented.keyframe_insert(data_path="value", frame=int(frame))
        sag.keyframe_insert(data_path="value", frame=int(frame))
    _linearize(keys)


def _linearize(datablock) -> None:
    animation = getattr(datablock, "animation_data", None)
    action = getattr(animation, "action", None) if animation else None
    if not action:
        return
    curves = list(getattr(action, "fcurves", []) or [])
    if not curves:
        for layer in getattr(action, "layers", []):
            for strip in getattr(layer, "strips", []):
                for bag in getattr(strip, "channelbags", []):
                    curves.extend(bag.fcurves)
    for fcurve in curves:
        for point in fcurve.keyframe_points:
            point.interpolation = "LINEAR"


# ---------------------------------------------------------------------------
# Scan fan
# ---------------------------------------------------------------------------

def build_scan_curtain_material(name: str, spec: dict, scene_config: dict, helpers):
    """Light curtain: alpha peaks at the sweep position, trails off behind it, thins toward the apex.

    UV.x is the slice's AOI-local u, UV.y runs 0 at the platform to 1 on the ground. The material
    carries no data and encodes nothing: it is a moving highlight, in the accepted cyan.
    """
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    helpers.set_blend_method(material)
    nt = material.node_tree
    nodes, links = nt.nodes, nt.links
    nodes.clear()

    def math_node(operation, a=None, b=None, clamp=False):
        node = nodes.new("ShaderNodeMath")
        node.operation = operation
        node.use_clamp = clamp
        for index, value in enumerate((a, b)):
            if value is None:
                continue
            if isinstance(value, (int, float)):
                node.inputs[index].default_value = float(value)
            else:
                links.new(value, node.inputs[index])
        return node.outputs[0]

    def ramp(value, from_max, to_min, to_max, kind="SMOOTHSTEP"):
        node = nodes.new("ShaderNodeMapRange")
        node.interpolation_type = kind
        node.clamp = True
        node.inputs["From Min"].default_value = 0.0
        node.inputs["From Max"].default_value = float(from_max)
        node.inputs["To Min"].default_value = float(to_min)
        node.inputs["To Max"].default_value = float(to_max)
        links.new(value, node.inputs["Value"])
        return node.outputs["Result"]

    output = nodes.new("ShaderNodeOutputMaterial")
    tex_coord = nodes.new("ShaderNodeTexCoord")
    separate = nodes.new("ShaderNodeSeparateXYZ")
    links.new(tex_coord.outputs["UV"], separate.inputs["Vector"])

    sweep = nodes.new("ShaderNodeValue")
    sweep.name = sweep.label = "aoi_sweep_position"
    sweep.outputs[0].default_value = -1.0
    presence = nodes.new("ShaderNodeValue")
    presence.name = presence.label = "aoi_presence"
    presence.outputs[0].default_value = 0.0

    delta = math_node("SUBTRACT", separate.outputs["X"], sweep.outputs[0])
    band = ramp(math_node("ABSOLUTE", delta), spec.get("band_width", 0.04), 1.0, 0.0)
    behind = math_node("MULTIPLY", delta, -1.0)
    tail = math_node(
        "MULTIPLY",
        ramp(behind, spec.get("tail_width", 0.25), 1.0, 0.0),
        math_node("GREATER_THAN", behind, 0.0),
    )
    lit = math_node(
        "ADD",
        math_node("MULTIPLY", band, float(spec.get("band_alpha", 0.2))),
        math_node("MULTIPLY", tail, float(spec.get("tail_alpha", 0.03))),
    )
    height = ramp(separate.outputs["Y"], 1.0, float(spec.get("root_alpha_factor", 0.12)), 1.0, "SMOOTHERSTEP")
    alpha = math_node("MULTIPLY", math_node("MULTIPLY", lit, height), presence.outputs[0], clamp=True)

    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = helpers.rgba(
        hc.palette_color(scene_config, spec["emission_color_ref"])
    )
    strength = float(spec.get("emission_strength", 4.5))
    links.new(ramp(band, 1.0, 0.55 * strength, strength, "LINEAR"), emission.inputs["Strength"])
    transparent = nodes.new("ShaderNodeBsdfTransparent")
    mix = nodes.new("ShaderNodeMixShader")
    links.new(alpha, mix.inputs["Fac"])
    links.new(transparent.outputs["BSDF"], mix.inputs[1])
    links.new(emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], output.inputs["Surface"])
    return material


def build_scan_fan(spec: dict, fan: dict, root, presented: dict, materials: dict, context: dict, helpers):
    """Veil + light curtain between the four sensing lines; returns the objects it built."""
    source = context["objects"].get(fan.get("source_object_id"))
    if source is None:
        raise KeyError("scan fan needs source object " + repr(fan.get("source_object_id")))
    radius_bu = presented["surface_radius_bu"]
    order = presented["corner_order"]
    corners = {cid: presented["corner_units"][order.index(cid)] for cid in ax.CORNER_IDS}
    built = []

    def finish(obj, apex_indices):
        obj.parent = root
        obj.matrix_parent_inverse = Matrix.Identity(4)
        hook = obj.modifiers.new(name="apex_follows_platform", type="HOOK")
        hook.object = source
        hook.falloff_type = "NONE"
        hook.strength = 1.0
        hook.vertex_indices_set(apex_indices)
        # Apex vertices sit at the local origin and the hook's parent-inverse is identity, so the
        # modifier maps them to world_to_object @ platform_world @ 0: the platform, in this
        # object's Earth-riding space, on every frame.
        hook.matrix_inverse = Matrix.Identity(4)
        built.append(obj)
        return obj

    veil_material = materials.get(fan.get("veil_material"))
    if veil_material is not None:
        ring = presented["boundary_units"]
        verts, faces, uvs = [], [], []
        for index, unit in enumerate(ring):
            following = ring[(index + 1) % len(ring)]
            base = len(verts)
            verts += [(0.0, 0.0, 0.0), ax.scale(unit, radius_bu), ax.scale(following, radius_bu)]
            along = index / float(len(ring))
            uvs += [(along, 0.0), (along, 1.0), (along, 1.0)]
            faces.append((base, base + 1, base + 2))
        veil = helpers.mesh_object(spec["id"] + "_fan_veil", verts, faces, veil_material, uvs=uvs)
        finish(veil, list(range(0, len(verts), 3)))

    curtain_material = materials.get(fan.get("curtain_material"))
    if curtain_material is not None:
        slices = max(4, int(fan.get("slices", 48)))
        segments = max(1, int(fan.get("slice_segments", 8)))
        verts, faces, uvs, apexes = [], [], [], []
        for k in range(slices):
            u = (k + 0.5) / float(slices)
            north = ax.slerp(corners["nw"], corners["ne"], u)
            south = ax.slerp(corners["sw"], corners["se"], u)
            apex = len(verts)
            apexes.append(apex)
            verts.append((0.0, 0.0, 0.0))
            uvs.append((u, 0.0))
            for j in range(segments + 1):
                verts.append(ax.scale(ax.slerp(north, south, j / float(segments)), radius_bu))
                uvs.append((u, 1.0))
            for j in range(segments):
                faces.append((apex, apex + 1 + j, apex + 2 + j))
        curtain = helpers.mesh_object(spec["id"] + "_fan_curtain", verts, faces, curtain_material, uvs=uvs)
        finish(curtain, apexes)

    keys = [
        (int(fan["appear_start_frame"]), 0.0), (int(fan["appear_end_frame"]), 1.0),
        (int(fan["retire_start_frame"]), 1.0), (int(fan["retire_end_frame"]), 0.0),
    ]
    helpers.animate_presence(veil_material, keys)
    helpers.animate_presence(curtain_material, keys)
    return built


# ---------------------------------------------------------------------------
# DEM relief
# ---------------------------------------------------------------------------

def load_dem(filename: str):
    """The governed DEM as a north-up float32 array, read without touching a value."""
    image = helpers_load_image(filename)
    image.colorspace_settings.name = "Non-Color"
    width, height = image.size
    if not image.is_float:
        raise ValueError(filename + " did not load as a float raster; refusing a quantised DEM")
    pixels = np.empty(width * height * image.channels, dtype=np.float32)
    image.pixels.foreach_get(pixels)
    array = pixels.reshape(height, width, image.channels)[:, :, 0]
    if not np.isfinite(array).all():
        raise ValueError(filename + " carries non-finite cells; the relief needs a complete DEM")
    # Blender image rows run bottom-to-top; a north-up GeoTIFF's first row is its north edge.
    return np.ascontiguousarray(array[::-1, :])


def helpers_load_image(filename: str):
    path = hc.SOURCE_DIR / filename
    if not path.is_file():
        raise FileNotFoundError(
            "analytical asset " + repr(filename) + " is not materialized; run "
            "hero/scripts/materialize_analytical_assets.py"
        )
    existing = bpy.data.images.get(path.name)
    return existing if existing is not None else bpy.data.images.load(str(path))


def sample_dem(dem, u, v):
    """Bilinear DEM sample at AOI-local (u, v); v = 0 is the north edge. Cell-centre registered."""
    rows, cols = dem.shape
    x = np.clip(np.asarray(u, dtype=np.float64) * cols - 0.5, 0.0, cols - 1.0)
    y = np.clip(np.asarray(v, dtype=np.float64) * rows - 0.5, 0.0, rows - 1.0)
    x0 = np.floor(x).astype(np.int64)
    y0 = np.floor(y).astype(np.int64)
    x1 = np.minimum(x0 + 1, cols - 1)
    y1 = np.minimum(y0 + 1, rows - 1)
    fx, fy = x - x0, y - y0
    top = dem[y0, x0] * (1.0 - fx) + dem[y0, x1] * fx
    bottom = dem[y1, x0] * (1.0 - fx) + dem[y1, x1] * fx
    return top * (1.0 - fy) + bottom * fy


def _corner_array(description):
    order = description["corner_order"]
    return {cid: np.array(description["corner_units"][order.index(cid)], dtype=np.float64)
            for cid in ax.CORNER_IDS}


def footprint_units(description, u, v):
    """Unit vectors for AOI-local (u, v): the fixture's own corner interpolation, vectorised.

    Normalised bilinear interpolation of the four corner directions. Over a 36 km footprint it
    agrees with the double slerp the lock frame and the scan fill use to well under a millimetre,
    so relief, textures and frame share one mapping.
    """
    c = _corner_array(description)
    u = np.asarray(u, dtype=np.float64)[..., None]
    v = np.asarray(v, dtype=np.float64)[..., None]
    point = (c["nw"] * (1 - u) + c["ne"] * u) * (1 - v) + (c["sw"] * (1 - u) + c["se"] * u) * v
    return point / np.linalg.norm(point, axis=-1, keepdims=True)


def footprint_uv(description, points):
    """Inverse of :func:`footprint_units` for points near the footprint (least squares, clamped)."""
    c = _corner_array(description)
    radius = np.linalg.norm(points, axis=-1, keepdims=True)
    units = points / radius
    basis = np.stack([c["ne"] - c["nw"], c["sw"] - c["nw"]], axis=1)  # 3 x 2
    solution, *_ = np.linalg.lstsq(basis, (units - c["nw"]).T, rcond=None)
    return np.clip(solution[0], 0.0, 1.0), np.clip(solution[1], 0.0, 1.0)


def build_relief_layers_material(name: str, spec: dict, scene_config: dict, helpers):
    """The prepared display textures on the relief, cross-faded by keyed weights.

    Colours are consumed as delivered: no ramp, no curve, no hue/contrast node touches them. The
    surface is part lit (so the DEM relief is visible as light and shadow) and part emissive (so
    a thematic layer stays legible on a slope facing away from the sun); ``emission_mix`` is that
    split per layer. NoData -- transparent in the delivered texture -- is shown as a neutral
    dark surface rather than a hole, so the relief stays one continuous piece of ground.
    """
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    helpers.set_blend_method(material, show_back=False)
    nt = material.node_tree
    nodes, links = nt.nodes, nt.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    tex_coord = nodes.new("ShaderNodeTexCoord")

    def math_node(operation, a, b, clamp=False):
        node = nodes.new("ShaderNodeMath")
        node.operation = operation
        node.use_clamp = clamp
        for index, value in enumerate((a, b)):
            if isinstance(value, (int, float)):
                node.inputs[index].default_value = float(value)
            else:
                links.new(value, node.inputs[index])
        return node.outputs[0]

    colour = alpha = total = glow = None
    for layer_id in spec["layer_order"]:
        layer = spec["layers"][layer_id]
        texture = nodes.new("ShaderNodeTexImage")
        texture.name = texture.label = "layer_" + layer_id
        texture.image = helpers.load_image(layer["texture"])
        texture.interpolation = "Cubic"
        texture.extension = "EXTEND"
        links.new(tex_coord.outputs["UV"], texture.inputs["Vector"])
        weight = nodes.new("ShaderNodeValue")
        weight.name = weight.label = "layer_weight_" + layer_id
        weight.outputs[0].default_value = 0.0

        add = nodes.new("ShaderNodeMixRGB")
        add.blend_type = "ADD"
        links.new(weight.outputs[0], add.inputs["Fac"])
        if colour is None:
            add.inputs["Color1"].default_value = (0.0, 0.0, 0.0, 1.0)
        else:
            links.new(colour, add.inputs["Color1"])
        links.new(texture.outputs["Color"], add.inputs["Color2"])
        colour = add.outputs["Color"]

        weighted_alpha = math_node("MULTIPLY", weight.outputs[0], texture.outputs["Alpha"])
        alpha = weighted_alpha if alpha is None else math_node("ADD", alpha, weighted_alpha)
        total = weight.outputs[0] if total is None else math_node("ADD", total, weight.outputs[0])
        weighted_glow = math_node("MULTIPLY", weight.outputs[0], float(layer.get("emission_mix", 0.5)))
        glow = weighted_glow if glow is None else math_node("ADD", glow, weighted_glow)

    safe_total = math_node("MAXIMUM", total, 1.0e-4)
    normalise = nodes.new("ShaderNodeVectorMath")
    normalise.operation = "DIVIDE"
    links.new(colour, normalise.inputs[0])
    spread = nodes.new("ShaderNodeCombineXYZ")
    for axis in ("X", "Y", "Z"):
        links.new(safe_total, spread.inputs[axis])
    links.new(spread.outputs["Vector"], normalise.inputs[1])

    shown = nodes.new("ShaderNodeMixRGB")
    shown.blend_type = "MIX"
    links.new(math_node("DIVIDE", alpha, safe_total, clamp=True), shown.inputs["Fac"])
    shown.inputs["Color1"].default_value = tuple(spec.get("nodata_color", (0.012, 0.016, 0.02))) + (1.0,)
    links.new(normalise.outputs["Vector"], shown.inputs["Color2"])

    lit = nodes.new("ShaderNodeBsdfPrincipled")
    links.new(shown.outputs["Color"], lit.inputs["Base Color"])
    lit.inputs["Roughness"].default_value = float(spec.get("roughness", 0.85))
    helpers.set_input(lit, "Specular IOR Level", 0.15)
    emission = nodes.new("ShaderNodeEmission")
    links.new(shown.outputs["Color"], emission.inputs["Color"])
    emission.inputs["Strength"].default_value = float(spec.get("emission_strength", 1.0))
    surface = nodes.new("ShaderNodeMixShader")
    links.new(math_node("DIVIDE", glow, safe_total, clamp=True), surface.inputs["Fac"])
    links.new(lit.outputs["BSDF"], surface.inputs[1])
    links.new(emission.outputs["Emission"], surface.inputs[2])

    transparent = nodes.new("ShaderNodeBsdfTransparent")
    present = nodes.new("ShaderNodeMixShader")
    links.new(math_node("MINIMUM", total, 1.0, clamp=True), present.inputs["Fac"])
    links.new(transparent.outputs["BSDF"], present.inputs[1])
    links.new(surface.outputs["Shader"], present.inputs[2])
    links.new(present.outputs["Shader"], output.inputs["Surface"])
    return material


def build_aoi_relief(spec: dict, materials: dict, context: dict, helpers):
    """Raise the footprint into relief from the governed DEM and drape the lock frame onto it."""
    scene_config, scene_spec = context["scene_config"], context["scene_spec"]
    description = ax.describe(scene_config, context.get("aoi_fixture") or spec["fixture"], scene_spec)
    earth_radius_bu = description["earth_radius_bu"]
    dem = load_dem(spec["dem"])

    exaggeration = float(spec.get("vertical_exaggeration", 3.0))
    reference = spec.get("reference_elevation", "min")
    reference_m = float(dem.min()) if reference == "min" else float(reference)
    base_m = float(spec.get("base_offset_m", 120.0))

    def radius_bu(elevation_m):
        return earth_radius_bu + (base_m + exaggeration * (elevation_m - reference_m)) / METRES_PER_BU

    n = max(8, int(spec.get("grid", 600)))
    axis = np.linspace(0.0, 1.0, n)
    u, v = np.meshgrid(axis, axis)  # rows are v (north -> south), columns are u (west -> east)
    units = footprint_units(description, u, v)
    flat = units * (earth_radius_bu + base_m / METRES_PER_BU)
    raised = units * radius_bu(sample_dem(dem, u, v))[..., None]

    # Skirt: the rim again, held at the base, so the raised block has sides instead of a gap.
    rim = np.concatenate([
        np.arange(0, n), np.arange(1, n) * n + (n - 1),
        (n - 1) * n + np.arange(n - 2, -1, -1), np.arange(n - 2, 0, -1) * n,
    ])
    top_count = n * n
    verts_flat = np.concatenate([flat.reshape(-1, 3), flat.reshape(-1, 3)[rim]])
    verts_raised = np.concatenate([raised.reshape(-1, 3), flat.reshape(-1, 3)[rim]])

    index = np.arange(top_count).reshape(n, n)
    quads = np.stack([index[:-1, :-1], index[1:, :-1], index[1:, 1:], index[:-1, 1:]], axis=-1).reshape(-1, 4)
    skirt = top_count + np.arange(len(rim))
    walls = np.stack([rim, np.roll(rim, -1), np.roll(skirt, -1), skirt], axis=-1)
    faces = np.concatenate([quads, walls])

    mesh = bpy.data.meshes.new(spec["id"])
    mesh.vertices.add(len(verts_flat))
    mesh.vertices.foreach_set("co", verts_flat.astype(np.float32).ravel())
    mesh.loops.add(faces.size)
    mesh.loops.foreach_set("vertex_index", faces.astype(np.int32).ravel())
    mesh.polygons.add(len(faces))
    mesh.polygons.foreach_set("loop_start", np.arange(0, faces.size, 4, dtype=np.int32))
    mesh.polygons.foreach_set("loop_total", np.full(len(faces), 4, dtype=np.int32))
    material_index = np.zeros(len(faces), dtype=np.int32)
    material_index[len(quads):] = 1
    mesh.polygons.foreach_set("material_index", material_index)
    mesh.polygons.foreach_set("use_smooth", np.concatenate([np.ones(len(quads), bool), np.zeros(len(walls), bool)]))
    mesh.update(calc_edges=True)
    mesh.validate()

    # One UV for every layer: u east, image v north (image rows run bottom-to-top).
    uv = np.concatenate([np.stack([u, 1.0 - v], axis=-1).reshape(-1, 2),
                         np.stack([u, 1.0 - v], axis=-1).reshape(-1, 2)[rim]])
    loop_uv = uv[faces.ravel()].reshape(-1, 4, 2)
    # The sides are not data. Their UV is (distance round the rim, 0 at the globe .. 1 at the
    # rim), which is what lets the wall material fade to nothing where the block meets the ground.
    along = np.arange(len(rim)) / float(len(rim))
    nxt = np.roll(along, -1)
    nxt[-1] = 1.0
    loop_uv[len(quads):] = np.stack([
        np.stack([along, np.ones_like(along)], axis=-1),
        np.stack([nxt, np.ones_like(along)], axis=-1),
        np.stack([nxt, np.zeros_like(along)], axis=-1),
        np.stack([along, np.zeros_like(along)], axis=-1),
    ], axis=1)
    layer = mesh.uv_layers.new(name="aoi")
    layer.data.foreach_set("uv", loop_uv.astype(np.float32).ravel())

    obj = bpy.data.objects.new(spec["id"], mesh)
    bpy.context.collection.objects.link(obj)
    mesh.materials.append(materials[spec["material"]])
    mesh.materials.append(materials.get(spec.get("wall_material")) or materials[spec["material"]])
    parent = context["objects"].get(spec.get("parent_id"))
    if parent is None:
        raise KeyError("relief " + spec["id"] + " needs parent " + repr(spec.get("parent_id")))
    obj.parent = parent
    obj.matrix_parent_inverse = Matrix.Identity(4)
    obj.visible_shadow = True

    obj.shape_key_add(name="Basis", from_mix=False)
    rise = obj.shape_key_add(name="rise", from_mix=False)
    rise.data.foreach_set("co", verts_raised.astype(np.float32).ravel())
    rise_keys = [(int(f), float(value)) for f, value in spec.get("rise_keyframes", [])]
    for frame, value in rise_keys:
        rise.value = value
        rise.keyframe_insert(data_path="value", frame=frame)

    # Hidden until it starts to rise: a flat transparent patch is still a render cost and a
    # z-fighting risk a few metres above the Earth it sits on.
    if rise_keys:
        first = rise_keys[0][0]
        obj.hide_render = True
        obj.keyframe_insert(data_path="hide_render", frame=first - 1)
        obj.hide_render = False
        obj.keyframe_insert(data_path="hide_render", frame=first)

    # The glass sides exist exactly as much as the block has risen.
    if rise_keys:
        helpers.animate_presence(materials.get(spec.get("wall_material")), rise_keys)

    material = materials[spec["material"]]
    for layer_id, keys in (spec.get("layer_keyframes") or {}).items():
        node = helpers.node_named(material, "layer_weight_" + layer_id)
        if node is None:
            raise KeyError("relief material has no layer " + repr(layer_id))
        helpers.keyframe_socket(material.node_tree, node.outputs[0],
                                [(int(f), float(w)) for f, w in keys], interpolation="BEZIER")

    # Drape the lock frame onto the rim of the relief, from the same DEM samples.
    clearance = float(spec.get("frame_clearance_m", 140.0))
    border_radius = description["surface_radius_bu"]
    for ribbon in context.get("aoi_frame_objects", {}).get(spec.get("aoi_id"), []):
        keys = ribbon.data.shape_keys
        basis = keys.key_blocks["Basis"]
        points = np.empty(len(basis.data) * 3, dtype=np.float64)
        basis.data.foreach_get("co", points)
        points = points.reshape(-1, 3)
        ru, rv = footprint_uv(description, points)
        stacking = np.linalg.norm(points, axis=1) - border_radius
        target = radius_bu(sample_dem(dem, ru, rv)) + clearance / METRES_PER_BU + stacking
        drape = ribbon.shape_key_add(name="drape", from_mix=False)
        draped = points / np.linalg.norm(points, axis=1, keepdims=True) * target[:, None]
        drape.data.foreach_set("co", draped.astype(np.float32).ravel())
        for frame, value in rise_keys:
            drape.value = value
            drape.keyframe_insert(data_path="value", frame=frame)

    context.setdefault("relief_records", {})[spec["id"]] = {
        "dem": spec["dem"],
        "dem_shape": list(dem.shape),
        "dem_min_m": float(dem.min()),
        "dem_max_m": float(dem.max()),
        "reference_elevation_m": reference_m,
        "vertical_exaggeration": exaggeration,
        "grid": n,
        "max_lift_km": round(exaggeration * (float(dem.max()) - reference_m) / 1000.0, 3),
    }
    print("[hero] relief " + spec["id"] + ": " + str(n) + " x " + str(n) + " grid from " + spec["dem"]
          + ", " + str(exaggeration) + "x, lift 0-" + str(round(exaggeration * (dem.max() - reference_m))) + " m")
    return obj
