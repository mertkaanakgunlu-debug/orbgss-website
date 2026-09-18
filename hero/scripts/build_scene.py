"""Build a hero scene from committed configuration inside Blender.

Configuration in ``hero/config/scene.json`` is the source of scene truth; this
module only translates it. Run it standalone to materialize a working .blend:

    blender -b -P hero/scripts/build_scene.py -- --scene benchmark_neutral --save

Later phases add scene definitions to scene.json and, where a definition needs
procedural geometry beyond the primitive vocabulary here, extend ``_add_object``
rather than hard-coding values in a render script.

Scene inheritance (``extends``) is resolved by ``hero_common.resolve_scene_spec``
rather than here, so the validator can resolve exactly the same scene without
importing bpy.

WEB-HERO-001B adds: image-textured materials (``earth_day_night``), a Fresnel
rim shell (``atmosphere_shell``), a procedural panel-grid material
(``solar_panel``), a compound procedurally-modelled ``satellite`` object type,
a procedural Voronoi starfield in the world shader, and keyframed animation
for objects and the camera. All of it stays declarative in scene.json; this
module only knows how to translate each spec shape into Blender calls.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bmesh  # noqa: E402
import bpy  # noqa: E402  (Blender-only import, after sys.path bootstrap)
from mathutils import Matrix, Vector  # noqa: E402

import aoi_system as ax  # noqa: E402
import analysis_reveal as ar  # noqa: E402
import hero_common as hc  # noqa: E402
import orbit_plan as op  # noqa: E402
import satellite_model as sm  # noqa: E402


def _clear_scene() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)


def _euler_from_deg(values) -> tuple:
    return tuple(math.radians(v) for v in values)


def _look_at_euler(location, target) -> tuple:
    direction = Vector(target) - Vector(location)
    if direction.length == 0.0:
        return (0.0, 0.0, 0.0)
    return tuple(direction.to_track_quat("-Z", "Y").to_euler())


def _rgba(color) -> tuple:
    return (float(color[0]), float(color[1]), float(color[2]), 1.0)


def _set_input(node, name: str, value) -> bool:
    """Set a node input if this Blender build/version exposes it; else no-op.

    Principled BSDF and a few other node sockets have been renamed across
    Blender 4.x releases (``Emission`` -> ``Emission Color`` +
    ``Emission Strength``, ``Specular`` -> ``Specular IOR Level``). Guarding
    every optional socket this way keeps one script working across builds.
    """
    if name in node.inputs:
        node.inputs[name].default_value = value
        return True
    return False


def _smooth_fcurves(obj) -> None:
    if not obj.animation_data or not obj.animation_data.action:
        return
    for fcurve in obj.animation_data.action.fcurves:
        for point in fcurve.keyframe_points:
            point.interpolation = "BEZIER"
            point.handle_left_type = "AUTO_CLAMPED"
            point.handle_right_type = "AUTO_CLAMPED"


def _smooth_data_fcurves(datablock) -> None:
    """Bezier / auto-clamped smoothing for keys on a data-block (camera lens and shift)."""
    animation = getattr(datablock, "animation_data", None)
    action = getattr(animation, "action", None) if animation else None
    if not action:
        return
    for fcurve in _action_fcurves(action):
        for point in fcurve.keyframe_points:
            point.interpolation = "BEZIER"
            point.handle_left_type = "AUTO_CLAMPED"
            point.handle_right_type = "AUTO_CLAMPED"


def _load_image(filename: str):
    path = hc.SOURCE_DIR / filename
    if not path.is_file():
        raise FileNotFoundError(
            "texture asset " + repr(filename) + " not found at " + hc.relpath(path)
            + "; materialize it under hero/assets/source/ and record it in "
            + hc.relpath(hc.ASSET_MANIFEST) + " first"
        )
    existing = bpy.data.images.get(path.name)
    if existing is not None:
        return existing
    return bpy.data.images.load(str(path))


# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------

def _apply_rim_light(nt, spec: dict, scene_config: dict, base_shader_socket):
    """Mix a thin Fresnel-gated edge light on top of an existing shader
    output, and rewire Material Output to the result. A small hard-surface
    prop (the satellite) needs this to keep a crisp, legible silhouette
    against both deep space and a bright sunlit Earth at hero scale; a bare
    Principled BSDF alone reads as a flat dark blob at that size. No-op
    (returns the input unchanged) when the spec has no rim_light_color_ref.
    """
    rim_ref = spec.get("rim_light_color_ref")
    if not rim_ref:
        return base_shader_socket

    nodes, links = nt.nodes, nt.links
    output = nodes.get("Material Output")
    rim_color = hc.palette_color(scene_config, rim_ref)

    fresnel = nodes.new("ShaderNodeFresnel")
    fresnel.location = (-250, -450)
    fresnel.inputs["IOR"].default_value = float(spec.get("rim_light_ior", 2.2))

    sharpen = nodes.new("ShaderNodeMapRange")
    sharpen.location = (-50, -450)
    sharpen.inputs["From Min"].default_value = float(spec.get("rim_light_falloff_min", 0.55))
    sharpen.inputs["From Max"].default_value = 1.0
    sharpen.clamp = True
    links.new(fresnel.outputs["Fac"], sharpen.inputs["Value"])

    rim_emission = nodes.new("ShaderNodeEmission")
    rim_emission.location = (150, -450)
    rim_emission.inputs["Color"].default_value = _rgba(rim_color)
    rim_emission.inputs["Strength"].default_value = float(spec.get("rim_light_strength", 1.2))

    rim_mix = nodes.new("ShaderNodeMixShader")
    rim_mix.location = (550, -200)
    links.new(sharpen.outputs["Result"], rim_mix.inputs["Fac"])
    links.new(base_shader_socket, rim_mix.inputs[1])
    links.new(rim_emission.outputs["Emission"], rim_mix.inputs[2])
    links.new(rim_mix.outputs["Shader"], output.inputs["Surface"])
    return rim_mix.outputs["Shader"]


def _build_principled_material(name: str, spec: dict, scene_config: dict):
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    nt = material.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    if bsdf is None:
        return material

    base = hc.palette_color(scene_config, spec["base_color_ref"])
    bsdf.inputs["Base Color"].default_value = _rgba(base)
    bsdf.inputs["Roughness"].default_value = float(spec.get("roughness", 0.5))
    bsdf.inputs["Metallic"].default_value = float(spec.get("metallic", 0.0))

    emission_ref = spec.get("emission_color_ref")
    if emission_ref:
        emission = hc.palette_color(scene_config, emission_ref)
        if not _set_input(bsdf, "Emission Color", _rgba(emission)):
            _set_input(bsdf, "Emission", _rgba(emission))
        _set_input(bsdf, "Emission Strength", float(spec.get("emission_strength", 1.0)))

    _apply_rim_light(nt, spec, scene_config, bsdf.outputs["BSDF"])
    return material


def _build_earth_material(name: str, spec: dict, scene_config: dict, sun_direction):
    """Day/night Earth material: a real day-map albedo lit normally, blended
    to an emissive night-lights map on the unlit hemisphere. The blend factor
    is the dot product of the surface normal with a fixed sun-direction
    vector baked in from the scene's authored sun light, not a raytraced
    shadow test -- cheap, stable under rotation, and standard practice for
    this look.
    """
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    nt = material.node_tree
    nodes, links = nt.nodes, nt.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (900, 0)

    mix_shader = nodes.new("ShaderNodeMixShader")
    mix_shader.location = (650, 0)

    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (300, 250)
    bsdf.inputs["Roughness"].default_value = float(spec.get("roughness", 0.6))

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (300, -250)
    emission.inputs["Strength"].default_value = float(spec.get("night_emission_strength", 1.6))

    day_tex_node = nodes.new("ShaderNodeTexImage")
    day_tex_node.location = (-150, 300)
    day_tex_node.image = _load_image(spec["day_texture"])
    # At the regional approach the albedo is magnified several times over, so
    # the reconstruction filter is visible. Cubic keeps magnified detail
    # rounded instead of showing bilinear diamonds; the default is kept when a
    # scene does not ask, so accepted phases rebuild unchanged.
    interpolation = spec.get("day_texture_interpolation")
    if interpolation:
        try:
            day_tex_node.interpolation = interpolation
        except TypeError:
            print("[hero] texture interpolation " + interpolation + " unavailable; default kept")

    night_tex_node = nodes.new("ShaderNodeTexImage")
    night_tex_node.location = (-150, -300)
    night_tex_node.image = _load_image(spec["night_texture"])
    try:
        night_tex_node.image.colorspace_settings.name = "Non-Color"
    except TypeError:
        pass

    # A longitude shift on an equirectangular map is a horizontal WRAP,
    # i.e. a translation of U with Repeat extension -- not a 2D rotation of
    # the UV square (which would mix U/V and fold the map near the poles).
    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (-450, 0)
    longitude_shift = float(spec.get("texture_rotation_deg", 0.0)) / 360.0
    mapping.inputs["Location"].default_value = (longitude_shift, 0.0, 0.0)

    tex_coord = nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-650, 0)

    geometry = nodes.new("ShaderNodeNewGeometry")
    geometry.location = (-450, 500)

    sun_vec = nodes.new("ShaderNodeCombineXYZ")
    sun_vec.location = (-450, 650)
    sun_vec.inputs[0].default_value = float(sun_direction[0])
    sun_vec.inputs[1].default_value = float(sun_direction[1])
    sun_vec.inputs[2].default_value = float(sun_direction[2])

    dot = nodes.new("ShaderNodeVectorMath")
    dot.operation = "DOT_PRODUCT"
    dot.location = (-200, 550)

    terminator = nodes.new("ShaderNodeMapRange")
    terminator.location = (50, 550)
    terminator.inputs["From Min"].default_value = float(spec.get("terminator_night_edge", -0.12))
    terminator.inputs["From Max"].default_value = float(spec.get("terminator_day_edge", 0.08))
    terminator.inputs["To Min"].default_value = 1.0
    terminator.inputs["To Max"].default_value = 0.0
    terminator.clamp = True

    links.new(tex_coord.outputs["UV"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], day_tex_node.inputs["Vector"])
    links.new(mapping.outputs["Vector"], night_tex_node.inputs["Vector"])

    albedo_socket = _earth_albedo_layers(nt, spec, scene_config, mapping, day_tex_node, interpolation)
    links.new(albedo_socket, bsdf.inputs["Base Color"])
    links.new(night_tex_node.outputs["Color"], emission.inputs["Color"])

    links.new(geometry.outputs["Normal"], dot.inputs[0])
    links.new(sun_vec.outputs["Vector"], dot.inputs[1])
    links.new(dot.outputs["Value"], terminator.inputs["Value"])

    links.new(terminator.outputs["Result"], mix_shader.inputs["Fac"])
    links.new(bsdf.outputs["BSDF"], mix_shader.inputs[1])
    links.new(emission.outputs["Emission"], mix_shader.inputs[2])
    links.new(mix_shader.outputs["Shader"], output.inputs["Surface"])
    return material


def _earth_albedo_layers(nt, spec: dict, scene_config: dict, mapping, day_tex_node, interpolation):
    """WEB-005A R2 albedo stack: global basemap -> regional 500 m detail window -> cloud layer.

    The mapped UV is an equirectangular coordinate (u = lon/360 + 0.5, v = lat/180 + 0.5), so a
    longitude/latitude window converts directly into a second texture lookup: inside the window
    the detail crop is sampled through its own normalized coordinates, and a feathered mask in
    degrees blends the two so the resolution step never shows as an edge. The cloud composite is
    a separate greyscale map mixed toward a near-white on top, which is exactly how the accepted
    land_ocean_ice_cloud composite was itself assembled -- so the global look is preserved while
    the land underneath gains four to sixteen times the texel density where the camera goes.

    Every stage is optional and absent from the accepted scenes, which therefore rebuild exactly
    as reviewed.
    """
    nodes, links = nt.nodes, nt.links
    current = day_tex_node.outputs["Color"]

    # --- shared geographic coordinate nodes (longitude / latitude in degrees) ---------------
    # The mapped UV is equirectangular, so longitude and latitude are two Map Range nodes away.
    # Built once, lazily, and shared by every window below.
    geo = {}

    def _geographic():
        if geo:
            return geo["lon"], geo["lat"]
        separate = nodes.new("ShaderNodeSeparateXYZ")
        separate.location = (-300, 900)
        links.new(mapping.outputs["Vector"], separate.inputs["Vector"])
        u_wrapped = nodes.new("ShaderNodeMath")
        u_wrapped.operation = "WRAP"
        u_wrapped.location = (-120, 980)
        u_wrapped.inputs[1].default_value = 0.0
        u_wrapped.inputs[2].default_value = 1.0
        links.new(separate.outputs["X"], u_wrapped.inputs[0])
        lon = nodes.new("ShaderNodeMapRange")
        lon.location = (60, 980)
        lon.inputs["From Min"].default_value = 0.0
        lon.inputs["From Max"].default_value = 1.0
        lon.inputs["To Min"].default_value = -180.0
        lon.inputs["To Max"].default_value = 180.0
        lon.clamp = False
        links.new(u_wrapped.outputs[0], lon.inputs["Value"])
        lat = nodes.new("ShaderNodeMapRange")
        lat.location = (60, 780)
        lat.inputs["From Min"].default_value = 0.0
        lat.inputs["From Max"].default_value = 1.0
        lat.inputs["To Min"].default_value = -90.0
        lat.inputs["To Max"].default_value = 90.0
        lat.clamp = False
        links.new(separate.outputs["Y"], lat.inputs["Value"])
        geo["lon"], geo["lat"] = lon.outputs["Result"], lat.outputs["Result"]
        return geo["lon"], geo["lat"]

    def _window_mask(lon_socket, lat_socket, lon0, lon1, lat0, lat1, feather, y):
        """0 outside a lon/lat rectangle, 1 inside, smooth-stepped over ``feather`` degrees."""
        def _edge(value_socket, low, high, yy):
            a = nodes.new("ShaderNodeMath")
            a.operation = "SUBTRACT"
            a.location = (260, yy)
            a.inputs[1].default_value = low
            links.new(value_socket, a.inputs[0])
            b = nodes.new("ShaderNodeMath")
            b.operation = "SUBTRACT"
            b.location = (260, yy - 120)
            b.inputs[0].default_value = high
            links.new(value_socket, b.inputs[1])
            m = nodes.new("ShaderNodeMath")
            m.operation = "MINIMUM"
            m.location = (440, yy - 60)
            links.new(a.outputs[0], m.inputs[0])
            links.new(b.outputs[0], m.inputs[1])
            return m.outputs[0]

        edge_lon = _edge(lon_socket, lon0, lon1, y)
        edge_lat = _edge(lat_socket, lat0, lat1, y - 240)
        edge = nodes.new("ShaderNodeMath")
        edge.operation = "MINIMUM"
        edge.location = (620, y - 120)
        links.new(edge_lon, edge.inputs[0])
        links.new(edge_lat, edge.inputs[1])
        mask = nodes.new("ShaderNodeMapRange")
        mask.location = (800, y - 120)
        mask.interpolation_type = "SMOOTHSTEP"
        mask.clamp = True
        mask.inputs["From Min"].default_value = 0.0
        mask.inputs["From Max"].default_value = max(1e-3, feather)
        mask.inputs["To Min"].default_value = 0.0
        mask.inputs["To Max"].default_value = 1.0
        links.new(edge.outputs[0], mask.inputs["Value"])
        return mask.outputs["Result"]

    def _window_uv(lon_socket, lat_socket, lon0, lon1, lat0, lat1, y):
        """Normalized (u, v) inside a lon/lat rectangle, clamped, for a window texture lookup."""
        u = nodes.new("ShaderNodeMapRange")
        u.location = (260, y)
        u.inputs["From Min"].default_value = lon0
        u.inputs["From Max"].default_value = lon1
        u.inputs["To Min"].default_value = 0.0
        u.inputs["To Max"].default_value = 1.0
        u.clamp = True
        links.new(lon_socket, u.inputs["Value"])
        v = nodes.new("ShaderNodeMapRange")
        v.location = (260, y - 180)
        v.inputs["From Min"].default_value = lat0
        v.inputs["From Max"].default_value = lat1
        v.inputs["To Min"].default_value = 0.0
        v.inputs["To Max"].default_value = 1.0
        v.clamp = True
        links.new(lat_socket, v.inputs["Value"])
        combine = nodes.new("ShaderNodeCombineXYZ")
        combine.location = (440, y - 90)
        links.new(u.outputs["Result"], combine.inputs["X"])
        links.new(v.outputs["Result"], combine.inputs["Y"])
        return combine.outputs["Vector"]

    window = spec.get("detail_window")
    detail_file = spec.get("detail_texture")
    if window and detail_file:
        lon0, lon1 = float(window["lon0"]), float(window["lon1"])
        lat0, lat1 = float(window["lat0"]), float(window["lat1"])
        feather = float(window.get("feather_deg", 2.0))
        lon_socket, lat_socket = _geographic()
        mask = _window_mask(lon_socket, lat_socket, lon0, lon1, lat0, lat1, feather, 1000)
        uv = _window_uv(lon_socket, lat_socket, lon0, lon1, lat0, lat1, 560)

        detail_node = nodes.new("ShaderNodeTexImage")
        detail_node.location = (620, 470)
        detail_node.image = _load_image(detail_file)
        detail_node.extension = "EXTEND"
        if interpolation:
            try:
                detail_node.interpolation = interpolation
            except TypeError:
                pass
        links.new(uv, detail_node.inputs["Vector"])

        blend = nodes.new("ShaderNodeMixRGB")
        blend.location = (1000, 600)
        blend.blend_type = "MIX"
        links.new(mask, blend.inputs["Fac"])
        links.new(current, blend.inputs["Color1"])
        links.new(detail_node.outputs["Color"], blend.inputs["Color2"])
        current = blend.outputs["Color"]

    # --- WEB-005A R3: regional detail multiplier -------------------------------------------
    # A greyscale ratio texture (materialize_earth_sharpen.py) that carries 30 m ground structure
    # without carrying any colour: inside its window the albedo is multiplied by
    # 1 + (ratio - 1) * strength, so the 500 m mean is preserved and no seam can form. Loaded
    # Non-Color because the values are ratios, not colours.
    sharpen = spec.get("detail_sharpen")
    if sharpen and sharpen.get("texture"):
        s_window = sharpen["window"]
        lon0, lon1 = float(s_window["lon0"]), float(s_window["lon1"])
        lat0, lat1 = float(s_window["lat0"]), float(s_window["lat1"])
        lon_socket, lat_socket = _geographic()
        mask = _window_mask(lon_socket, lat_socket, lon0, lon1, lat0, lat1,
                            float(s_window.get("feather_deg", 0.05)), 200)
        uv = _window_uv(lon_socket, lat_socket, lon0, lon1, lat0, lat1, -240)

        ratio_node = nodes.new("ShaderNodeTexImage")
        ratio_node.location = (620, -330)
        ratio_node.image = _load_image(sharpen["texture"])
        ratio_node.extension = "EXTEND"
        try:
            ratio_node.image.colorspace_settings.name = "Non-Color"
        except TypeError:
            pass
        try:
            ratio_node.interpolation = "Cubic"
        except TypeError:
            pass
        links.new(uv, ratio_node.inputs["Vector"])

        decode = nodes.new("ShaderNodeMath")
        decode.operation = "MULTIPLY"
        decode.location = (820, -330)
        decode.inputs[1].default_value = float(sharpen.get("encode_scale", 2.0))
        links.new(ratio_node.outputs["Color"], decode.inputs[0])

        # ratio_s = 1 + (ratio - 1) * strength  ==  ratio * strength + (1 - strength)
        strength = float(sharpen.get("strength", 1.0))
        scaled = nodes.new("ShaderNodeMath")
        scaled.operation = "MULTIPLY_ADD"
        scaled.location = (1000, -330)
        scaled.inputs[1].default_value = strength
        scaled.inputs[2].default_value = 1.0 - strength
        links.new(decode.outputs[0], scaled.inputs[0])

        # gate by the window mask: outside the window the multiplier is exactly 1
        gated = nodes.new("ShaderNodeMapRange")
        gated.location = (1180, -330)
        gated.clamp = False
        gated.inputs["From Min"].default_value = 0.0
        gated.inputs["From Max"].default_value = 1.0
        gated.inputs["To Min"].default_value = 1.0
        links.new(scaled.outputs[0], gated.inputs["To Max"])
        links.new(mask, gated.inputs["Value"])

        multiplied = nodes.new("ShaderNodeMixRGB")
        multiplied.location = (1360, -200)
        multiplied.blend_type = "MULTIPLY"
        multiplied.inputs["Fac"].default_value = 1.0
        links.new(current, multiplied.inputs["Color1"])
        links.new(gated.outputs["Result"], multiplied.inputs["Color2"])
        current = multiplied.outputs["Color"]

    sea = spec.get("sea_tint")
    if sea:
        # Optional: pull open water toward the accepted darker navy. The mask is derived from
        # the albedo itself (blue dominance), so no geography is painted by hand.
        separate_rgb = nodes.new("ShaderNodeSeparateColor")
        separate_rgb.location = (1000, 300)
        links.new(current, separate_rgb.inputs["Color"])
        rg = nodes.new("ShaderNodeMath")
        rg.operation = "MAXIMUM"
        rg.location = (1180, 300)
        links.new(separate_rgb.outputs[0], rg.inputs[0])
        links.new(separate_rgb.outputs[1], rg.inputs[1])
        blue_excess = nodes.new("ShaderNodeMath")
        blue_excess.operation = "SUBTRACT"
        blue_excess.location = (1360, 300)
        links.new(separate_rgb.outputs[2], blue_excess.inputs[0])
        links.new(rg.outputs[0], blue_excess.inputs[1])
        sea_mask = nodes.new("ShaderNodeMapRange")
        sea_mask.location = (1540, 300)
        sea_mask.interpolation_type = "SMOOTHSTEP"
        sea_mask.clamp = True
        sea_mask.inputs["From Min"].default_value = float(sea.get("mask_start", 0.02))
        sea_mask.inputs["From Max"].default_value = float(sea.get("mask_end", 0.12))
        sea_mask.inputs["To Min"].default_value = 0.0
        sea_mask.inputs["To Max"].default_value = float(sea.get("amount", 0.5))
        links.new(blue_excess.outputs[0], sea_mask.inputs["Value"])
        tinted = nodes.new("ShaderNodeMixRGB")
        tinted.location = (1540, 100)
        tinted.blend_type = "MULTIPLY"
        tinted.inputs["Fac"].default_value = 1.0
        tinted.inputs["Color2"].default_value = _rgba(hc.palette_color(scene_config, sea["tint_color_ref"]))
        links.new(current, tinted.inputs["Color1"])
        sea_mix = nodes.new("ShaderNodeMixRGB")
        sea_mix.location = (1740, 200)
        links.new(sea_mask.outputs["Result"], sea_mix.inputs["Fac"])
        links.new(current, sea_mix.inputs["Color1"])
        links.new(tinted.outputs["Color"], sea_mix.inputs["Color2"])
        current = sea_mix.outputs["Color"]

    cloud_file = spec.get("cloud_texture")
    if cloud_file:
        cloud_node = nodes.new("ShaderNodeTexImage")
        cloud_node.location = (1000, -200)
        cloud_node.image = _load_image(cloud_file)
        try:
            cloud_node.image.colorspace_settings.name = "Non-Color"
        except TypeError:
            pass
        links.new(mapping.outputs["Vector"], cloud_node.inputs["Vector"])
        cloud_amount = nodes.new("ShaderNodeMath")
        cloud_amount.operation = "MULTIPLY"
        cloud_amount.location = (1200, -200)
        cloud_amount.use_clamp = True
        cloud_amount.inputs[1].default_value = float(spec.get("cloud_strength", 1.0))
        links.new(cloud_node.outputs["Color"], cloud_amount.inputs[0])
        # WEB-005A R3: a clear acquisition window. The 8192 px cloud composite is about 5 km per
        # texel; smeared over a 170 km hold it reads as a milky veil, not as cloud. Inside the
        # detail window the cloud amount is scaled down over a wide feather, so the target region
        # is acquired under the clear sky the Sentinel-2 detail was itself observed under.
        sharpen_cfg = spec.get("detail_sharpen") or {}
        clear = float(sharpen_cfg.get("clear_clouds", 0.0))
        if clear > 0.0 and sharpen_cfg.get("window"):
            w = sharpen_cfg["window"]
            lon_socket, lat_socket = _geographic()
            clear_mask = _window_mask(
                lon_socket, lat_socket, float(w["lon0"]), float(w["lon1"]), float(w["lat0"]), float(w["lat1"]),
                float(sharpen_cfg.get("clear_feather_deg", 0.6)), -600,
            )
            keep = nodes.new("ShaderNodeMapRange")
            keep.location = (1200, -420)
            keep.clamp = True
            keep.inputs["From Min"].default_value = 0.0
            keep.inputs["From Max"].default_value = 1.0
            keep.inputs["To Min"].default_value = 1.0
            keep.inputs["To Max"].default_value = 1.0 - clear
            links.new(clear_mask, keep.inputs["Value"])
            cleared = nodes.new("ShaderNodeMath")
            cleared.operation = "MULTIPLY"
            cleared.location = (1300, -300)
            cleared.use_clamp = True
            links.new(cloud_amount.outputs[0], cleared.inputs[0])
            links.new(keep.outputs["Result"], cleared.inputs[1])
            cloud_amount = cleared
        cloud_mix = nodes.new("ShaderNodeMixRGB")
        cloud_mix.location = (1400, -100)
        cloud_mix.inputs["Color2"].default_value = _rgba(
            hc.palette_color(scene_config, spec.get("cloud_color_ref", "neutral_light"))
        )
        links.new(cloud_amount.outputs[0], cloud_mix.inputs["Fac"])
        links.new(current, cloud_mix.inputs["Color1"])
        current = cloud_mix.outputs["Color"]

    return current


def _build_atmosphere_material(name: str, spec: dict, scene_config: dict, sun_direction):
    """Fresnel rim-glow shell: transparent facing the camera, emissive at
    grazing angles, so the atmosphere reads as a limb glow that visibly
    follows the globe instead of a flat neon outline.

    The grazing-angle (Fresnel) factor alone made every previous version of
    this shell glow at an equally uniform, thick, all-the-way-round
    brightness regardless of where the sun was -- exactly the "detached
    graphic outline" look this was flagged for. A real limb glow is
    sunlight scattering in the atmosphere, so it must fade out on the night
    side: the emission's *strength* (not the transparent/emissive mix
    itself, which stays a pure viewing-angle effect) is additionally scaled
    by the same dot(normal, sun_direction) term the Earth material uses,
    remapped so the day limb stays bright and the night limb only keeps a
    faint terminator-adjacent hint rather than going fully dark.
    """
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    nt = material.node_tree
    nodes, links = nt.nodes, nt.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (750, 0)

    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (0, -150)

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (150, 150)
    color = hc.palette_color(scene_config, spec.get("rim_color_ref", "atmosphere_cyan"))
    emission.inputs["Color"].default_value = _rgba(color)

    day_gate = nodes.new("ShaderNodeMath")
    day_gate.operation = "MULTIPLY"
    day_gate.location = (-50, 300)
    day_gate.inputs[0].default_value = float(spec.get("strength", 1.6))
    links.new(day_gate.outputs["Value"], emission.inputs["Strength"])

    geometry = nodes.new("ShaderNodeNewGeometry")
    geometry.location = (-450, 400)
    sun_vec = nodes.new("ShaderNodeCombineXYZ")
    sun_vec.location = (-450, 550)
    sun_vec.inputs[0].default_value = float(sun_direction[0])
    sun_vec.inputs[1].default_value = float(sun_direction[1])
    sun_vec.inputs[2].default_value = float(sun_direction[2])
    sun_dot = nodes.new("ShaderNodeVectorMath")
    sun_dot.operation = "DOT_PRODUCT"
    sun_dot.location = (-250, 450)
    links.new(geometry.outputs["Normal"], sun_dot.inputs[0])
    links.new(sun_vec.outputs["Vector"], sun_dot.inputs[1])

    night_hint = float(spec.get("night_hint", 0.12))
    day_night_gate = nodes.new("ShaderNodeMapRange")
    day_night_gate.location = (-50, 450)
    day_night_gate.inputs["From Min"].default_value = -0.6
    day_night_gate.inputs["From Max"].default_value = 0.3
    day_night_gate.inputs["To Min"].default_value = night_hint
    day_night_gate.inputs["To Max"].default_value = 1.0
    day_night_gate.clamp = True
    links.new(sun_dot.outputs["Value"], day_night_gate.inputs["Value"])
    links.new(day_night_gate.outputs["Result"], day_gate.inputs[1])

    fresnel = nodes.new("ShaderNodeFresnel")
    fresnel.location = (-250, 0)
    fresnel.inputs["IOR"].default_value = float(spec.get("fresnel_ior", 1.2))

    if str(spec.get("profile", "")) == "limb_airmass":
        # WEB-HERO-001D atmosphere.
        #
        # Every earlier version of this shell drove its brightness from the
        # Fresnel factor, which is a property of the *shell surface*, not of
        # the air a view ray travels through. That is why it kept producing
        # graphics rather than atmosphere: monotonic Fresnel is brightest
        # exactly at the shell silhouette, so the glow ended on a hard
        # geometric line -- the hoop this phase had to remove -- and shaping it
        # into a band only moved that line and added a second one wherever a
        # second shell began.
        #
        # The quantity that actually governs limb brightness is how high above
        # the surface the line of sight passes: its perigee. That is
        # recoverable in the shader. The camera position is the shading point
        # plus its incoming vector times the view distance, and the perigee
        # radius of the ray through that point is
        #
        #     h = sqrt(|C|^2 - (C . d)^2),   d = -Incoming
        #
        # from which the glow is
        #
        #     glow = exp(-max(0, h - R) / H) * (min(h, R) / R)^k
        #
        # The first factor decays the glow exponentially with altitude above
        # the limb, so it reaches zero well inside the shell own silhouette and
        # the shell has no visible edge at any distance. The second confines
        # on-disc haze to near-grazing sightlines, so the planet is hazy at its
        # horizon and clean at nadir, the way it is from orbit.
        #
        # It is combined with Add Shader rather than Mix Shader because air
        # does not occlude what is behind it, it adds light. A mix made the
        # shell paint a solid band across the sky once the camera was low
        # enough to see it nearly edge-on, which is exactly the
        # regional-approach case this phase had to fix.
        # The planet radius is scene truth, not a material parameter: read it
        # from world_coordinate_convention so the shell can never disagree with
        # the globe it wraps.
        radius_bu = float(
            spec.get(
                "earth_radius_bu",
                ax.earth_radius_km(scene_config) / ax.KM_PER_BLENDER_UNIT,
            )
        )
        scale_height_km = float(spec.get("scale_height_km", 55.0))
        scale_height_bu = scale_height_km / ax.KM_PER_BLENDER_UNIT
        # Tangent-path air mass through an exponential atmosphere, the standard
        # sqrt(2 pi R / H). Derived rather than authored so it cannot drift away
        # from the scale height it belongs to.
        max_airmass = float(
            spec.get(
                "max_airmass",
                math.sqrt(2.0 * math.pi * radius_bu * ax.KM_PER_BLENDER_UNIT / scale_height_km),
            )
        )

        view_distance = nodes.new("ShaderNodeCameraData")
        view_distance.location = (-900, -150)

        incoming_scaled = nodes.new("ShaderNodeVectorMath")
        incoming_scaled.operation = "SCALE"
        incoming_scaled.location = (-700, -150)
        links.new(geometry.outputs["Incoming"], incoming_scaled.inputs[0])
        links.new(view_distance.outputs["View Distance"], incoming_scaled.inputs["Scale"])

        camera_position = nodes.new("ShaderNodeVectorMath")
        camera_position.operation = "ADD"
        camera_position.location = (-520, -150)
        links.new(geometry.outputs["Position"], camera_position.inputs[0])
        links.new(incoming_scaled.outputs["Vector"], camera_position.inputs[1])

        view_direction = nodes.new("ShaderNodeVectorMath")
        view_direction.operation = "SCALE"
        view_direction.location = (-700, -330)
        view_direction.inputs["Scale"].default_value = -1.0
        links.new(geometry.outputs["Incoming"], view_direction.inputs[0])

        along = nodes.new("ShaderNodeVectorMath")
        along.operation = "DOT_PRODUCT"
        along.location = (-330, -250)
        links.new(camera_position.outputs["Vector"], along.inputs[0])
        links.new(view_direction.outputs["Vector"], along.inputs[1])

        along_squared = nodes.new("ShaderNodeMath")
        along_squared.operation = "MULTIPLY"
        along_squared.location = (-150, -320)
        links.new(along.outputs["Value"], along_squared.inputs[0])
        links.new(along.outputs["Value"], along_squared.inputs[1])

        camera_squared = nodes.new("ShaderNodeVectorMath")
        camera_squared.operation = "DOT_PRODUCT"
        camera_squared.location = (-330, -430)
        links.new(camera_position.outputs["Vector"], camera_squared.inputs[0])
        links.new(camera_position.outputs["Vector"], camera_squared.inputs[1])

        perigee_squared = nodes.new("ShaderNodeMath")
        perigee_squared.operation = "SUBTRACT"
        perigee_squared.location = (30, -380)
        links.new(camera_squared.outputs["Value"], perigee_squared.inputs[0])
        links.new(along_squared.outputs["Value"], perigee_squared.inputs[1])

        non_negative = nodes.new("ShaderNodeMath")
        non_negative.operation = "MAXIMUM"
        non_negative.location = (190, -380)
        non_negative.inputs[1].default_value = 0.0
        links.new(perigee_squared.outputs["Value"], non_negative.inputs[0])

        perigee = nodes.new("ShaderNodeMath")
        perigee.operation = "SQRT"
        perigee.location = (350, -380)
        links.new(non_negative.outputs["Value"], perigee.inputs[0])

        # Outward term: exp(-max(0, h - R) / H).
        above = nodes.new("ShaderNodeMath")
        above.operation = "SUBTRACT"
        above.location = (520, -260)
        above.inputs[1].default_value = radius_bu
        links.new(perigee.outputs["Value"], above.inputs[0])

        above_clamped = nodes.new("ShaderNodeMath")
        above_clamped.operation = "MAXIMUM"
        above_clamped.location = (680, -260)
        above_clamped.inputs[1].default_value = 0.0
        links.new(above.outputs["Value"], above_clamped.inputs[0])

        decay = nodes.new("ShaderNodeMath")
        decay.operation = "DIVIDE"
        decay.location = (840, -260)
        decay.inputs[1].default_value = max(1e-6, scale_height_bu)
        links.new(above_clamped.outputs["Value"], decay.inputs[0])

        negated = nodes.new("ShaderNodeMath")
        negated.operation = "MULTIPLY"
        negated.location = (1000, -260)
        negated.inputs[1].default_value = -1.0
        links.new(decay.outputs["Value"], negated.inputs[0])

        outward = nodes.new("ShaderNodeMath")
        outward.operation = "EXPONENT"
        outward.location = (1160, -260)
        links.new(negated.outputs["Value"], outward.inputs[0])

        # Inward term: the relative air mass along the sightline.
        #
        # A sightline with incidence i through an exponential atmosphere
        # traverses roughly 1 / cos(i) times as much air as one straight down,
        # saturating at the tangent value sqrt(2 pi R / H) -- about 27 air
        # masses for this planet and scale height. Since sin(i) = h / R for a
        # ray that reaches the surface, cos(i) falls straight out of the
        # perigee we already have, and one expression then covers the whole
        # frame: a faint even tint at nadir, thickening smoothly toward the
        # horizon, saturating at the limb, decaying exponentially above it.
        #
        # This is why the brightness parameter is per air mass rather than a
        # free gain. Tuning a gain is how the previous profile ended up washing
        # the planet out: it had no notion of how much air a ray had crossed.
        capped = nodes.new("ShaderNodeMath")
        capped.operation = "MINIMUM"
        capped.location = (520, -520)
        capped.inputs[1].default_value = radius_bu
        links.new(perigee.outputs["Value"], capped.inputs[0])

        normalized = nodes.new("ShaderNodeMath")
        normalized.operation = "DIVIDE"
        normalized.location = (680, -520)
        normalized.inputs[1].default_value = radius_bu
        links.new(capped.outputs["Value"], normalized.inputs[0])

        sine_squared = nodes.new("ShaderNodeMath")
        sine_squared.operation = "MULTIPLY"
        sine_squared.location = (840, -520)
        links.new(normalized.outputs["Value"], sine_squared.inputs[0])
        links.new(normalized.outputs["Value"], sine_squared.inputs[1])

        cosine_squared = nodes.new("ShaderNodeMath")
        cosine_squared.operation = "SUBTRACT"
        cosine_squared.location = (1000, -520)
        cosine_squared.inputs[0].default_value = 1.0
        links.new(sine_squared.outputs["Value"], cosine_squared.inputs[1])

        cosine_floor = nodes.new("ShaderNodeMath")
        cosine_floor.operation = "MAXIMUM"
        cosine_floor.location = (1160, -520)
        cosine_floor.inputs[1].default_value = 1.0e-6
        links.new(cosine_squared.outputs["Value"], cosine_floor.inputs[0])

        cosine = nodes.new("ShaderNodeMath")
        cosine.operation = "SQRT"
        cosine.location = (1320, -520)
        links.new(cosine_floor.outputs["Value"], cosine.inputs[0])

        secant = nodes.new("ShaderNodeMath")
        secant.operation = "DIVIDE"
        secant.location = (1480, -520)
        secant.inputs[0].default_value = 1.0
        links.new(cosine.outputs["Value"], secant.inputs[1])

        inward = nodes.new("ShaderNodeMath")
        inward.operation = "MINIMUM"
        inward.location = (1640, -520)
        inward.inputs[1].default_value = max_airmass
        links.new(secant.outputs["Value"], inward.inputs[0])

        airmass = nodes.new("ShaderNodeMath")
        airmass.operation = "MULTIPLY"
        airmass.location = (1800, -380)
        links.new(outward.outputs["Value"], airmass.inputs[0])
        links.new(inward.outputs["Value"], airmass.inputs[1])

        # A closed shell is crossed twice by a limb ray and once by a ray that
        # ends on the planet, so letting both faces emit would double the limb
        # alone. The saturating air-mass term above already stands for the
        # whole tangent path, so the back face is suppressed instead.
        front_only = nodes.new("ShaderNodeMath")
        front_only.operation = "SUBTRACT"
        front_only.location = (1800, -600)
        front_only.inputs[0].default_value = 1.0
        links.new(geometry.outputs["Backfacing"], front_only.inputs[1])

        single_pass = nodes.new("ShaderNodeMath")
        single_pass.operation = "MULTIPLY"
        single_pass.location = (1960, -460)
        links.new(airmass.outputs["Value"], single_pass.inputs[0])
        links.new(front_only.outputs["Value"], single_pass.inputs[1])
        airmass = single_pass

        # day_gate already carries strength * the day/night falloff.
        shaped = nodes.new("ShaderNodeMath")
        shaped.operation = "MULTIPLY"
        shaped.location = (1480, -180)
        links.new(day_gate.outputs["Value"], shaped.inputs[0])
        links.new(airmass.outputs["Value"], shaped.inputs[1])
        links.new(shaped.outputs["Value"], emission.inputs["Strength"])

        add = nodes.new("ShaderNodeAddShader")
        add.location = (1640, 0)
        links.new(transparent.outputs["BSDF"], add.inputs[0])
        links.new(emission.outputs["Emission"], add.inputs[1])
        links.new(add.outputs["Shader"], output.inputs["Surface"])
        try:
            material.blend_method = "BLEND"
            material.show_transparent_back = True
        except (AttributeError, TypeError):
            pass
        return material

    if str(spec.get("profile", "")) == "soft_band":
        # WEB-HERO-001D limb profile.
        #
        # Two things were wrong with the inherited shell at Phase-D distances.
        #
        # First, its opacity is monotonic in the Fresnel factor, so it is
        # *brightest* exactly at its own silhouette and ends on a hard
        # geometric line. That is what made the accepted Phase-B/C atmosphere
        # read as a bright hoop drawn around the planet. Real limb brightness
        # peaks a little inside the top of the atmosphere and decays to nothing
        # at it, so opacity here is a band in Fresnel space -- a smoothstep up
        # followed by a smoothstep back down to zero before grazing -- and the
        # shell therefore ends in air.
        #
        # Second, and worse close in, a Mix Shader between Transparent and
        # Emission *replaces* what is behind the shell. Seen nearly edge-on
        # from low altitude a shell covers a large part of the frame, so the
        # glow stopped being a glow and became a solid teal band painted over
        # the sky and the planet. Air does not occlude; it adds. So the two
        # shaders are combined with Add Shader instead: the shell stays fully
        # transmissive at every angle and only ever contributes light.
        #
        # Only taken when a scene asks for it, so the accepted Phase-B and
        # Phase-C atmosphere shells rebuild exactly as reviewed.
        rise = nodes.new("ShaderNodeMapRange")
        rise.location = (-50, 90)
        rise.interpolation_type = "SMOOTHSTEP"
        rise.clamp = True
        rise.inputs["From Min"].default_value = float(spec.get("band_rise_start", 0.05))
        rise.inputs["From Max"].default_value = float(spec.get("band_rise_end", 0.5))
        rise.inputs["To Min"].default_value = 0.0
        rise.inputs["To Max"].default_value = 1.0
        links.new(fresnel.outputs["Fac"], rise.inputs["Value"])

        fade = nodes.new("ShaderNodeMapRange")
        fade.location = (-50, -160)
        fade.interpolation_type = "SMOOTHSTEP"
        fade.clamp = True
        fade.inputs["From Min"].default_value = float(spec.get("band_fade_start", 0.75))
        fade.inputs["From Max"].default_value = float(spec.get("band_fade_end", 1.0))
        fade.inputs["To Min"].default_value = 1.0
        fade.inputs["To Max"].default_value = 0.0
        links.new(fresnel.outputs["Fac"], fade.inputs["Value"])

        band = nodes.new("ShaderNodeMath")
        band.operation = "MULTIPLY"
        band.location = (170, -30)
        links.new(rise.outputs["Result"], band.inputs[0])
        links.new(fade.outputs["Result"], band.inputs[1])

        floor_glow = nodes.new("ShaderNodeMath")
        floor_glow.operation = "ADD"
        floor_glow.location = (300, -30)
        floor_glow.use_clamp = True
        floor_glow.inputs[1].default_value = float(spec.get("base_glow", 0.0))
        links.new(band.outputs["Value"], floor_glow.inputs[0])

        # day_gate already carries strength * day/night falloff; the band then
        # shapes it across the limb.
        shaped = nodes.new("ShaderNodeMath")
        shaped.operation = "MULTIPLY"
        shaped.location = (450, 200)
        links.new(day_gate.outputs["Value"], shaped.inputs[0])
        links.new(floor_glow.outputs["Value"], shaped.inputs[1])
        links.new(shaped.outputs["Value"], emission.inputs["Strength"])

        add = nodes.new("ShaderNodeAddShader")
        add.location = (600, 0)
        links.new(transparent.outputs["BSDF"], add.inputs[0])
        links.new(emission.outputs["Emission"], add.inputs[1])
        links.new(add.outputs["Shader"], output.inputs["Surface"])
        try:
            material.blend_method = "BLEND"
            material.show_transparent_back = True
        except (AttributeError, TypeError):
            pass
        return material

    falloff = nodes.new("ShaderNodeMapRange")
    falloff.location = (-50, 0)
    falloff.inputs["From Min"].default_value = float(spec.get("falloff_min", 0.3))
    falloff.inputs["From Max"].default_value = float(spec.get("falloff_max", 1.0))
    falloff.inputs["To Min"].default_value = 0.0
    falloff.inputs["To Max"].default_value = 1.0
    falloff.clamp = True

    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (450, 0)

    links.new(fresnel.outputs["Fac"], falloff.inputs["Value"])

    # Optional outer-silhouette fade.
    #
    # The Fresnel ramp is monotonic, so opacity is highest exactly at the
    # shell's own silhouette and the limb ends on a hard geometric line. From
    # WEB-HERO-001B's distances that line is a sub-pixel sliver and invisible;
    # from WEB-HERO-001C's approach distances it becomes a straight-edged teal
    # wedge across the frame. Fading the outermost sliver back to transparent
    # lets the glow end in air instead of on an edge.
    #
    # Off unless a scene asks for it, so the accepted WEB-HERO-001B shell
    # rebuilds exactly as before.
    opacity_socket = falloff.outputs["Result"]
    fade_start = spec.get("silhouette_fade_start")
    if fade_start is not None:
        outer_fade = nodes.new("ShaderNodeMapRange")
        outer_fade.location = (-50, -230)
        outer_fade.inputs["From Min"].default_value = float(fade_start)
        outer_fade.inputs["From Max"].default_value = 1.0
        outer_fade.inputs["To Min"].default_value = 1.0
        outer_fade.inputs["To Max"].default_value = 0.0
        outer_fade.clamp = True
        outer_fade.interpolation_type = "SMOOTHSTEP"
        links.new(fresnel.outputs["Fac"], outer_fade.inputs["Value"])

        faded = nodes.new("ShaderNodeMath")
        faded.operation = "MULTIPLY"
        faded.location = (200, -120)
        links.new(falloff.outputs["Result"], faded.inputs[0])
        links.new(outer_fade.outputs["Result"], faded.inputs[1])
        opacity_socket = faded.outputs["Value"]

    links.new(opacity_socket, mix.inputs["Fac"])
    links.new(transparent.outputs["BSDF"], mix.inputs[1])
    links.new(emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], output.inputs["Surface"])

    try:
        material.blend_method = "BLEND"
        material.show_transparent_back = False
    except (AttributeError, TypeError):
        pass
    return material


def _build_solar_panel_material(name: str, spec: dict, scene_config: dict):
    """Principled base panel colour with a procedural brick-pattern grid
    mixed in as a faint emissive cell/bus-bar line -- no image texture.
    """
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    nt = material.node_tree
    nodes, links = nt.nodes, nt.links

    bsdf = nodes.get("Principled BSDF")
    output = nodes.get("Material Output")
    base = hc.palette_color(scene_config, spec.get("base_color_ref", "satellite_panel"))
    bsdf.inputs["Base Color"].default_value = _rgba(base)
    bsdf.inputs["Roughness"].default_value = float(spec.get("roughness", 0.22))
    bsdf.inputs["Metallic"].default_value = float(spec.get("metallic", 0.55))

    grid_color = hc.palette_color(scene_config, spec.get("grid_color_ref", "scan_ice_blue"))

    tex_coord = nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-700, -200)

    brick = nodes.new("ShaderNodeTexBrick")
    brick.location = (-450, -200)
    _set_input(brick, "Color1", _rgba(base))
    _set_input(brick, "Color2", _rgba(base))
    _set_input(brick, "Mortar", _rgba(grid_color))
    _set_input(brick, "Scale", float(spec.get("cell_scale", 7.0)))
    _set_input(brick, "Mortar Size", float(spec.get("grid_line_width", 0.015)))
    _set_input(brick, "Row Height", 1.0)

    grid_emission = nodes.new("ShaderNodeEmission")
    grid_emission.location = (-150, -350)
    grid_emission.inputs["Color"].default_value = _rgba(grid_color)
    grid_emission.inputs["Strength"].default_value = float(spec.get("grid_emission_strength", 0.5))

    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (150, -100)

    links.new(tex_coord.outputs["Object"], brick.inputs["Vector"])
    links.new(brick.outputs["Fac"], mix.inputs["Fac"])
    links.new(bsdf.outputs["BSDF"], mix.inputs[1])
    links.new(grid_emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], output.inputs["Surface"])

    _apply_rim_light(nt, spec, scene_config, mix.outputs["Shader"])
    return material


def _build_material(name: str, spec: dict, scene_config: dict, sun_direction=(0.0, 0.0, 1.0)):
    kind = spec.get("type", "principled")
    if kind == "principled":
        return _build_principled_material(name, spec, scene_config)
    if kind == "earth_day_night":
        return _build_earth_material(name, spec, scene_config, sun_direction)
    if kind == "atmosphere_shell":
        return _build_atmosphere_material(name, spec, scene_config, sun_direction)
    if kind == "solar_panel":
        return _build_solar_panel_material(name, spec, scene_config)
    if kind == "aoi_emission":
        return _build_aoi_emission_material(name, spec, scene_config)
    if kind == "aoi_scan_fill":
        return _build_aoi_scan_fill_material(name, spec, scene_config)
    if kind == "aoi_beam":
        return _build_aoi_beam_material(name, spec, scene_config)
    # WEB-005A R2 vocabulary: the generic EO satellite, its orbital trail, and the glow/draw
    # treatments that give the acquisition frame a visible lock event.
    if kind == "mli":
        return sm.build_mli_material(name, spec, scene_config)
    if kind == "surface":
        return sm.build_surface_material(name, spec, scene_config)
    if kind == "solar_cells":
        return sm.build_solar_cell_material(name, spec, scene_config)
    if kind == "orbit_trail":
        return sm.build_trail_material(name, spec, scene_config)
    if kind == "aoi_glow_ribbon":
        return _build_aoi_glow_ribbon_material(name, spec, scene_config)
    if kind == "aoi_lock_draw":
        return _build_aoi_lock_draw_material(name, spec, scene_config)
    # WEB-005A R3 preview gate: the scan curtain and the DEM-relief display layers.
    if kind == "aoi_scan_curtain":
        return ar.build_scan_curtain_material(name, spec, scene_config, _ar_helpers())
    if kind == "aoi_relief_layers":
        return ar.build_relief_layers_material(name, spec, scene_config, _ar_helpers())
    raise ValueError("unsupported material type " + repr(kind) + " for " + name)


def _ar_helpers():
    """The builder helpers ``analysis_reveal`` shares, handed over rather than imported back."""
    from types import SimpleNamespace

    return SimpleNamespace(
        rgba=_rgba,
        set_input=_set_input,
        set_blend_method=_set_blend_method,
        keyframe_socket=_keyframe_socket,
        load_image=_load_image,
        mesh_object=_mesh_object,
        animate_presence=_animate_presence,
        node_named=_node_named,
    )


def _primary_light_direction(spec: dict):
    """Direction *toward* the scene's primary sun, from its authored
    location/look_at pair. A Blender SUN lamp only shines along its
    rotation, but we author suns as (location, look_at) like everything
    else, so the equivalent light-arrival direction is location - look_at.
    """
    lights = spec.get("lights", [])
    ref_id = spec.get("lighting_reference", {}).get("primary_light_id")
    chosen = None
    if ref_id:
        chosen = next((l for l in lights if l.get("id") == ref_id), None)
    if chosen is None:
        chosen = next((l for l in lights if l.get("type") == "SUN"), None)
    if chosen is None or "look_at" not in chosen:
        return (0.0, 0.0, 1.0)
    location = Vector(chosen.get("location", (0.0, 0.0, 0.0)))
    look_at = Vector(chosen["look_at"])
    direction = location - look_at
    if direction.length == 0.0:
        return (0.0, 0.0, 1.0)
    direction.normalize()
    return (direction.x, direction.y, direction.z)


# ---------------------------------------------------------------------------
# Objects
# ---------------------------------------------------------------------------

def _build_satellite(spec: dict, materials: dict):
    """A small procedurally-modelled Earth-observation satellite: a bus,
    two solar panel wings, a nadir dish and a short instrument boom, all
    parented to an empty so the whole assembly can be positioned, scaled
    and animated as one rigid body.
    """
    root = bpy.data.objects.new(spec["id"], None)
    root.empty_display_size = 0.05
    bpy.context.collection.objects.link(root)
    root.location = tuple(spec.get("location", (0.0, 0.0, 0.0)))

    bus_size = spec.get("bus_size", [0.22, 0.14, 0.14])
    panel_size = spec.get("panel_size", [0.55, 0.16])
    dish_radius = float(spec.get("dish_radius", 0.10))
    bus_material = materials.get(spec.get("bus_material"))
    panel_material = materials.get(spec.get("panel_material"))
    dish_material = materials.get(spec.get("dish_material"), bus_material)

    # This lane is pre-data: a satellite silhouette cast onto Earth as a real
    # shadow reads, at review size, like a stray AOI/placement marker rather
    # than an intentional camera-framing beauty detail. Suppress shadow rays
    # from every satellite part so the satellite still looks correctly lit
    # itself but never marks the surface below it.
    def _no_cast_shadow(obj):
        try:
            obj.visible_shadow = False
        except AttributeError:
            pass

    bpy.ops.mesh.primitive_cube_add(size=1.0)
    bus = bpy.context.active_object
    bus.name = spec["id"] + "_bus"
    bus.scale = (bus_size[0] / 2, bus_size[1] / 2, bus_size[2] / 2)
    bus.parent = root
    for polygon in bus.data.polygons:
        polygon.use_smooth = False
    if bus_material:
        bus.data.materials.append(bus_material)
    _no_cast_shadow(bus)

    for side, sign in (("pos", 1.0), ("neg", -1.0)):
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        panel = bpy.context.active_object
        panel.name = spec["id"] + "_panel_" + side
        panel.scale = (panel_size[0] / 2, panel_size[1] / 2, 0.006)
        panel.parent = root
        panel.location = (sign * (bus_size[0] / 2 + panel_size[0] / 2 + 0.015), 0.0, 0.0)
        if panel_material:
            panel.data.materials.append(panel_material)
        _no_cast_shadow(panel)

    bpy.ops.mesh.primitive_cone_add(
        radius1=dish_radius, radius2=dish_radius * 0.12, depth=dish_radius * 0.55, vertices=28
    )
    dish = bpy.context.active_object
    dish.name = spec["id"] + "_dish"
    dish.parent = root
    # Local -Z is nadir once the root's TRACK_TO constraint aims -Z at Earth,
    # so the dish's wide (base) opening sits on -Z, facing the target.
    dish.location = (0.0, 0.0, -(bus_size[2] / 2 + dish_radius * 0.5))
    for polygon in dish.data.polygons:
        polygon.use_smooth = True
    if dish_material:
        dish.data.materials.append(dish_material)
    _no_cast_shadow(dish)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=bus_size[2] * 1.6, vertices=10)
    boom = bpy.context.active_object
    boom.name = spec["id"] + "_boom"
    boom.parent = root
    boom.rotation_euler = (0.0, math.radians(90.0), 0.0)
    boom.location = (bus_size[0] / 2 + bus_size[2] * 0.8, 0.0, 0.0)
    if bus_material:
        boom.data.materials.append(bus_material)
    _no_cast_shadow(boom)

    scale = float(spec.get("scale", 1.0))
    root.scale = (scale, scale, scale)
    return root


# ---------------------------------------------------------------------------
# AOI acquisition system (WEB-HERO-001C)
# ---------------------------------------------------------------------------

def _cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _rotate_on_sphere(unit, side, angle):
    """Rotate a unit vector by ``angle`` within the plane it spans with ``side``.

    ``side`` must be a unit vector tangent at ``unit``. The result is exactly a
    unit vector, so widening a border this way keeps every generated vertex on
    the sphere instead of lifting it off the surface.
    """
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    return (
        unit[0] * cos_a + side[0] * sin_a,
        unit[1] * cos_a + side[1] * sin_a,
        unit[2] * cos_a + side[2] * sin_a,
    )


def _orient_faces(mesh, outward_of) -> None:
    """Flip any face whose normal points the wrong way.

    Generated strips and tubes have no inherent winding, and a blended material
    with back faces hidden renders a wrongly-wound face as nothing at all --
    geometry that is present, correct and invisible. Rather than hand-tuning
    each loop's index order, derive the answer: compare every face normal with
    the direction that face should be looking and reverse the ones that
    disagree.
    """
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.normal_update()
    wrong = [
        face
        for face in bm.faces
        if face.normal.dot(outward_of(face.calc_center_median())) < 0.0
    ]
    if wrong:
        bmesh.ops.reverse_faces(bm, faces=wrong)
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()


def _radially_outward(point):
    """Outward for geometry generated on the globe: away from the Earth centre."""
    return Vector(point)


def _tube_outward(point):
    """Outward for a beam tube: away from its own +Y axis."""
    return Vector((point[0], 0.0, point[2]))


def _mesh_object(name: str, verts, faces, material, uvs=None, outward_of=None):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces])
    mesh.update()
    if outward_of is not None:
        _orient_faces(mesh, outward_of)
    if uvs is not None:
        uv_layer = mesh.uv_layers.new(name="aoi")
        for loop_index, loop in enumerate(mesh.loops):
            uv_layer.data[loop_index].uv = uvs[loop.vertex_index]
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    if material:
        mesh.materials.append(material)
    # AOI geometry sits a few hundred metres above the surface it describes.
    # Letting it cast real shadows would print a hard copy of the footprint
    # onto the Earth beside it, which reads as a modelling error.
    try:
        obj.visible_shadow = False
    except AttributeError:
        pass
    return obj


def _ribbon_on_sphere(name, units, radius_bu, width_km, earth_radius_km, closed, material):
    """Build a thin quad strip that follows a polyline across the sphere.

    Both rails are generated by rotating each sample sideways within its own
    tangent plane, so the ribbon is a band lying *on* the sphere rather than a
    flat strip stretched over it. Used for the footprint border and the corner
    locks alike.
    """
    verts, uvs = _ribbon_vertices(units, radius_bu, width_km, earth_radius_km, closed)
    count = len(units)
    faces = []
    last = count if closed else count - 1
    for index in range(last):
        a = 2 * index
        b = 2 * index + 1
        c = 2 * ((index + 1) % count)
        d = 2 * ((index + 1) % count) + 1
        faces.append((a, b, d, c))
    return _mesh_object(name, verts, faces, material, uvs=uvs, outward_of=_radially_outward)


def _ribbon_vertices(units, radius_bu, width_km, earth_radius_km, closed):
    """Rail vertices and UVs of a ribbon; shared by the mesh and by its presentation shape key."""
    half_angle = (float(width_km) / float(earth_radius_km)) / 2.0
    count = len(units)
    verts = []
    uvs = []
    for index, point in enumerate(units):
        if closed:
            previous = units[(index - 1) % count]
            following = units[(index + 1) % count]
        else:
            previous = units[max(index - 1, 0)]
            following = units[min(index + 1, count - 1)]

        along = (
            following[0] - previous[0],
            following[1] - previous[1],
            following[2] - previous[2],
        )
        radial = sum(a * b for a, b in zip(along, point))
        along = (
            along[0] - point[0] * radial,
            along[1] - point[1] * radial,
            along[2] - point[2] * radial,
        )
        along = ax.normalize(along)
        side = ax.normalize(_cross(point, along))

        verts.append(ax.scale(_rotate_on_sphere(point, side, -half_angle), radius_bu))
        verts.append(ax.scale(_rotate_on_sphere(point, side, half_angle), radius_bu))
        # u runs along the strip, v across it: what a glow falloff or a draw-in mask reads.
        along_u = index / float(max(1, count - 1))
        uvs.append((along_u, 0.0))
        uvs.append((along_u, 1.0))
    return verts, uvs


def _fill_on_sphere(name, rows, radius_bu, material):
    """Interior footprint surface, carrying AOI-local (u, v) in its UV layer.

    The UV layer is what makes the scan sweep surface-following: the sweep is a
    band in this parameter space, painted on a mesh that is itself on the
    sphere, so it cannot detach from the globe however the camera moves.
    """
    height = len(rows)
    width = len(rows[0])
    verts, uvs = [], []
    for j, row in enumerate(rows):
        for i, unit in enumerate(row):
            verts.append(ax.scale(unit, radius_bu))
            uvs.append((i / float(width - 1), j / float(height - 1)))

    faces = []
    for j in range(height - 1):
        for i in range(width - 1):
            a = j * width + i
            faces.append((a, a + 1, a + width + 1, a + width))
    return _mesh_object(name, verts, faces, material, uvs=uvs, outward_of=_radially_outward)


def _beam_mesh_object(name, root_radius_bu, tip_radius_bu, sides, material):
    """An open tapered tube spanning y = 0 (source) to y = 1 (target).

    Length 1 along +Y is what lets a Stretch To constraint span the real
    satellite-to-corner distance at every frame without the beam ever being
    re-authored: the constraint supplies the aim and the length, so the
    endpoints stay registered to whatever the AOI is doing.
    """
    verts, uvs = [], []
    for radius, v in ((root_radius_bu, 0.0), (tip_radius_bu, 1.0)):
        for index in range(sides):
            angle = 2.0 * math.pi * index / sides
            verts.append((radius * math.cos(angle), v, radius * math.sin(angle)))
            uvs.append((index / float(sides), v))
    faces = [
        (i, (i + 1) % sides, sides + (i + 1) % sides, sides + i) for i in range(sides)
    ]
    return _mesh_object(name, verts, faces, material, uvs=uvs, outward_of=_tube_outward)


def _action_fcurves(action):
    """F-curves of an action across both the legacy and slotted layouts."""
    curves = list(getattr(action, "fcurves", []) or [])
    if curves:
        return curves
    for layer in getattr(action, "layers", []):
        for strip in getattr(layer, "strips", []):
            for channelbag in getattr(strip, "channelbags", []):
                curves.extend(channelbag.fcurves)
    return curves


def _keyframe_socket(node_tree, socket, keys, interpolation="LINEAR"):
    """Keyframe a shader socket and force a chosen interpolation.

    Appearance ramps and the scan sweep are authored on material sockets rather
    than on object transforms, so nothing about the AOI's *position* is ever
    animated -- only how much of it is visible. Position stays owned by the
    Earth parent and the beam constraints.
    """
    data_path = socket.path_from_id("default_value")
    for frame, value in keys:
        socket.default_value = value
        socket.keyframe_insert(data_path="default_value", frame=int(frame))
    animation = getattr(node_tree, "animation_data", None)
    action = getattr(animation, "action", None) if animation else None
    if not action:
        return
    for fcurve in _action_fcurves(action):
        if fcurve.data_path == data_path:
            for point in fcurve.keyframe_points:
                point.interpolation = interpolation


def _set_blend_method(material, show_back: bool = True) -> None:
    """Ask EEVEE for real alpha blending, across 4.x naming.

    ``show_back`` stays on for the beams: letting a viewer see both walls of the
    tube is what gives a hollow beam its soft, denser-at-the-silhouette falloff
    instead of a flat cutout.
    """
    for attribute, value in (
        ("surface_render_method", "BLENDED"),
        ("blend_method", "BLEND"),
    ):
        try:
            setattr(material, attribute, value)
        except (AttributeError, TypeError):
            continue
    try:
        material.show_transparent_back = show_back
    except AttributeError:
        pass


def _build_aoi_emission_material(name: str, spec: dict, scene_config: dict):
    """Flat emissive ribbon material for the border and the corner locks."""
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    nt = material.node_tree
    nodes, links = nt.nodes, nt.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (400, 0)
    emission = nodes.new("ShaderNodeEmission")
    emission.location = (150, 0)
    emission.inputs["Color"].default_value = _rgba(
        hc.palette_color(scene_config, spec["emission_color_ref"])
    )
    emission.inputs["Strength"].default_value = float(spec.get("emission_strength", 8.0))
    # WEB-005A R3: a presence gate. An emission ribbon at strength zero is a black ribbon, which
    # is invisible while it is sub-pixel and a dark line the moment the camera is close -- so a
    # frame that has to appear, or vanish under the dive, is switched through a transparent mix
    # instead of only dimmed. Default 1 keeps every accepted scene rendering exactly as reviewed.
    _set_blend_method(material, show_back=False)
    presence = nodes.new("ShaderNodeValue")
    presence.name = "aoi_presence"
    presence.label = "aoi_presence"
    presence.location = (150, -200)
    presence.outputs[0].default_value = 1.0
    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (150, 200)
    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (300, 0)
    links.new(presence.outputs[0], mix.inputs["Fac"])
    links.new(transparent.outputs["BSDF"], mix.inputs[1])
    links.new(emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], output.inputs["Surface"])
    return material


def _build_aoi_scan_fill_material(name: str, spec: dict, scene_config: dict):
    """Neutral interior treatment: a faint cyan glass plus a travelling band.

    Deliberately carries no data. Alpha is built from three scalars -- a base
    presence, a slightly denser "already swept" region behind the band, and the
    band itself -- so the footprint communicates scan progress and nothing more.
    No gradient here encodes a measured quantity, and there is no legend, scale
    or classification anywhere in it.
    """
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    _set_blend_method(material)
    nt = material.node_tree
    nodes, links = nt.nodes, nt.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (1100, 0)

    tex_coord = nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-900, 0)
    separate = nodes.new("ShaderNodeSeparateXYZ")
    separate.location = (-700, 0)
    links.new(tex_coord.outputs["UV"], separate.inputs["Vector"])

    axis_socket = "Y" if str(spec.get("axis", "v")).lower() in ("v", "y") else "X"

    sweep = nodes.new("ShaderNodeValue")
    sweep.name = "aoi_sweep_position"
    sweep.label = "aoi_sweep_position"
    sweep.location = (-700, -220)
    sweep.outputs[0].default_value = -1.0

    delta = nodes.new("ShaderNodeMath")
    delta.operation = "SUBTRACT"
    delta.location = (-480, -80)
    links.new(separate.outputs[axis_socket], delta.inputs[0])
    links.new(sweep.outputs[0], delta.inputs[1])

    distance = nodes.new("ShaderNodeMath")
    distance.operation = "ABSOLUTE"
    distance.location = (-280, -40)
    links.new(delta.outputs[0], distance.inputs[0])

    band = nodes.new("ShaderNodeMapRange")
    band.location = (-80, -40)
    band.interpolation_type = "SMOOTHSTEP"
    band.clamp = True
    band.inputs["From Min"].default_value = 0.0
    band.inputs["From Max"].default_value = float(spec.get("band_width", 0.13))
    band.inputs["To Min"].default_value = 1.0
    band.inputs["To Max"].default_value = 0.0
    links.new(distance.outputs[0], band.inputs["Value"])

    # "Already swept" is the region the band has passed, i.e. negative delta.
    behind = nodes.new("ShaderNodeMath")
    behind.operation = "MULTIPLY"
    behind.location = (-280, -260)
    behind.inputs[1].default_value = -1.0
    links.new(delta.outputs[0], behind.inputs[0])

    acquired = nodes.new("ShaderNodeMapRange")
    acquired.location = (-80, -260)
    acquired.clamp = True
    acquired.inputs["From Min"].default_value = 0.0
    acquired.inputs["From Max"].default_value = 0.02
    acquired.inputs["To Min"].default_value = 0.0
    acquired.inputs["To Max"].default_value = 1.0
    links.new(behind.outputs[0], acquired.inputs["Value"])

    acquired_alpha = nodes.new("ShaderNodeMath")
    acquired_alpha.operation = "MULTIPLY"
    acquired_alpha.location = (160, -260)
    acquired_alpha.inputs[1].default_value = float(spec.get("acquired_alpha", 0.11))
    links.new(acquired.outputs["Result"], acquired_alpha.inputs[0])

    band_alpha = nodes.new("ShaderNodeMath")
    band_alpha.operation = "MULTIPLY"
    band_alpha.location = (160, -40)
    band_alpha.inputs[1].default_value = float(spec.get("band_alpha", 0.62))
    links.new(band.outputs["Result"], band_alpha.inputs[0])

    sum_a = nodes.new("ShaderNodeMath")
    sum_a.operation = "ADD"
    sum_a.location = (380, -150)
    links.new(band_alpha.outputs[0], sum_a.inputs[0])
    links.new(acquired_alpha.outputs[0], sum_a.inputs[1])

    sum_b = nodes.new("ShaderNodeMath")
    sum_b.operation = "ADD"
    sum_b.location = (560, -150)
    sum_b.inputs[1].default_value = float(spec.get("base_alpha", 0.045))
    links.new(sum_a.outputs[0], sum_b.inputs[0])

    presence = nodes.new("ShaderNodeValue")
    presence.name = "aoi_presence"
    presence.label = "aoi_presence"
    presence.location = (560, -360)
    presence.outputs[0].default_value = 1.0

    alpha = nodes.new("ShaderNodeMath")
    alpha.operation = "MULTIPLY"
    alpha.location = (760, -150)
    alpha.use_clamp = True
    links.new(sum_b.outputs[0], alpha.inputs[0])
    links.new(presence.outputs[0], alpha.inputs[1])

    color = nodes.new("ShaderNodeMixRGB")
    color.location = (380, 220)
    color.inputs["Color1"].default_value = _rgba(
        hc.palette_color(scene_config, spec["base_color_ref"])
    )
    color.inputs["Color2"].default_value = _rgba(
        hc.palette_color(scene_config, spec["band_color_ref"])
    )
    links.new(band.outputs["Result"], color.inputs["Fac"])

    strength = nodes.new("ShaderNodeMapRange")
    strength.location = (380, 40)
    strength.clamp = True
    strength.inputs["From Min"].default_value = 0.0
    strength.inputs["From Max"].default_value = 1.0
    strength.inputs["To Min"].default_value = float(spec.get("base_emission_strength", 1.1))
    strength.inputs["To Max"].default_value = float(spec.get("band_emission_strength", 7.0))
    links.new(band.outputs["Result"], strength.inputs["Value"])

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (760, 120)
    links.new(color.outputs["Color"], emission.inputs["Color"])
    links.new(strength.outputs["Result"], emission.inputs["Strength"])

    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (760, 320)

    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (940, 0)
    links.new(alpha.outputs[0], mix.inputs["Fac"])
    links.new(transparent.outputs["BSDF"], mix.inputs[1])
    links.new(emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], output.inputs["Surface"])
    return material


def _build_aoi_beam_material(name: str, spec: dict, scene_config: dict):
    """Acquisition beam: near-invisible at the satellite, denser at the ground.

    A beam that is uniformly opaque reads as a solid plastic tube. Ramping
    alpha along the beam's own length keeps it as a suggestion of directed
    attention rather than a literal depiction of sensor physics.
    """
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    _set_blend_method(material)
    nt = material.node_tree
    nodes, links = nt.nodes, nt.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (700, 0)

    tex_coord = nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-600, 0)
    separate = nodes.new("ShaderNodeSeparateXYZ")
    separate.location = (-420, 0)
    links.new(tex_coord.outputs["UV"], separate.inputs["Vector"])

    along = nodes.new("ShaderNodeMapRange")
    along.location = (-220, 0)
    along.clamp = True
    along.interpolation_type = "SMOOTHSTEP"
    along.inputs["From Min"].default_value = 0.0
    along.inputs["From Max"].default_value = 1.0
    along.inputs["To Min"].default_value = float(spec.get("root_alpha", 0.03))
    along.inputs["To Max"].default_value = float(spec.get("tip_alpha", 0.22))
    links.new(separate.outputs["Y"], along.inputs["Value"])

    presence = nodes.new("ShaderNodeValue")
    presence.name = "aoi_presence"
    presence.label = "aoi_presence"
    presence.location = (-220, -220)
    presence.outputs[0].default_value = 0.0

    alpha = nodes.new("ShaderNodeMath")
    alpha.operation = "MULTIPLY"
    alpha.location = (40, -80)
    alpha.use_clamp = True
    links.new(along.outputs["Result"], alpha.inputs[0])
    links.new(presence.outputs[0], alpha.inputs[1])

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (300, 120)
    emission.inputs["Color"].default_value = _rgba(
        hc.palette_color(scene_config, spec["emission_color_ref"])
    )
    emission.inputs["Strength"].default_value = float(spec.get("emission_strength", 3.4))

    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (300, 320)

    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (520, 0)
    links.new(alpha.outputs[0], mix.inputs["Fac"])
    links.new(transparent.outputs["BSDF"], mix.inputs[1])
    links.new(emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], output.inputs["Surface"])
    return material


def _build_aoi_glow_ribbon_material(name: str, spec: dict, scene_config: dict):
    """Soft emissive halo for the frame: a wider ribbon whose alpha falls off across its width.

    The crisp border keeps its own thin ribbon; this one sits beside it and gives the "controlled
    outer glow" the R2 lock asks for at every distance, because it is geometry on the sphere
    rather than a screen-space blur that would change size with the camera.
    """
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    _set_blend_method(material, show_back=False)
    nt = material.node_tree
    nodes, links = nt.nodes, nt.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (800, 0)

    tex_coord = nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-700, 0)
    separate = nodes.new("ShaderNodeSeparateXYZ")
    separate.location = (-500, 0)
    links.new(tex_coord.outputs["UV"], separate.inputs["Vector"])
    centred = nodes.new("ShaderNodeMath")
    centred.operation = "SUBTRACT"
    centred.location = (-320, 0)
    centred.inputs[1].default_value = 0.5
    links.new(separate.outputs["Y"], centred.inputs[0])
    distance = nodes.new("ShaderNodeMath")
    distance.operation = "ABSOLUTE"
    distance.location = (-140, 0)
    links.new(centred.outputs[0], distance.inputs[0])
    falloff = nodes.new("ShaderNodeMapRange")
    falloff.location = (40, 0)
    falloff.interpolation_type = "SMOOTHSTEP"
    falloff.clamp = True
    falloff.inputs["From Min"].default_value = float(spec.get("core_fraction", 0.0))
    falloff.inputs["From Max"].default_value = 0.5
    falloff.inputs["To Min"].default_value = 1.0
    falloff.inputs["To Max"].default_value = 0.0
    links.new(distance.outputs[0], falloff.inputs["Value"])
    shaped = nodes.new("ShaderNodeMath")
    shaped.operation = "POWER"
    shaped.location = (220, 0)
    shaped.inputs[1].default_value = float(spec.get("falloff_power", 1.6))
    links.new(falloff.outputs["Result"], shaped.inputs[0])

    presence = nodes.new("ShaderNodeValue")
    presence.name = "aoi_presence"
    presence.label = "aoi_presence"
    presence.location = (220, -220)
    presence.outputs[0].default_value = 1.0
    alpha = nodes.new("ShaderNodeMath")
    alpha.operation = "MULTIPLY"
    alpha.location = (400, -100)
    alpha.use_clamp = True
    links.new(shaped.outputs[0], alpha.inputs[0])
    links.new(presence.outputs[0], alpha.inputs[1])
    alpha_scaled = nodes.new("ShaderNodeMath")
    alpha_scaled.operation = "MULTIPLY"
    alpha_scaled.location = (560, -100)
    alpha_scaled.inputs[1].default_value = float(spec.get("alpha", 0.35))
    links.new(alpha.outputs[0], alpha_scaled.inputs[0])

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (400, 150)
    emission.inputs["Color"].default_value = _rgba(
        hc.palette_color(scene_config, spec["emission_color_ref"])
    )
    emission.inputs["Strength"].default_value = float(spec.get("emission_strength", 3.0))
    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (400, 320)
    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (620, 60)
    links.new(alpha_scaled.outputs[0], mix.inputs["Fac"])
    links.new(transparent.outputs["BSDF"], mix.inputs[1])
    links.new(emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], output.inputs["Surface"])
    return material


def _build_aoi_lock_draw_material(name: str, spec: dict, scene_config: dict):
    """Corner-lock bracket that draws itself in from the corner outward.

    The lock ribbon runs arm -> apex -> arm, so its U is 0 at one arm tip, 0.5 at the corner and
    1 at the other tip. A keyframed ``aoi_lock_draw`` value d reveals |u - 0.5| <= d / 2, which is
    the two arms growing out of the corner: the registration marks resolve into place instead of
    fading up as a finished glyph.
    """
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    _set_blend_method(material, show_back=False)
    nt = material.node_tree
    nodes, links = nt.nodes, nt.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (800, 0)

    tex_coord = nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-700, 0)
    separate = nodes.new("ShaderNodeSeparateXYZ")
    separate.location = (-500, 0)
    links.new(tex_coord.outputs["UV"], separate.inputs["Vector"])
    centred = nodes.new("ShaderNodeMath")
    centred.operation = "SUBTRACT"
    centred.location = (-320, 0)
    centred.inputs[1].default_value = 0.5
    links.new(separate.outputs["X"], centred.inputs[0])
    distance = nodes.new("ShaderNodeMath")
    distance.operation = "ABSOLUTE"
    distance.location = (-140, 0)
    links.new(centred.outputs[0], distance.inputs[0])
    doubled = nodes.new("ShaderNodeMath")
    doubled.operation = "MULTIPLY"
    doubled.location = (40, 0)
    doubled.inputs[1].default_value = 2.0
    links.new(distance.outputs[0], doubled.inputs[0])

    draw = nodes.new("ShaderNodeValue")
    draw.name = "aoi_lock_draw"
    draw.label = "aoi_lock_draw"
    draw.location = (40, -200)
    draw.outputs[0].default_value = 1.0
    reveal = nodes.new("ShaderNodeMath")
    reveal.operation = "SUBTRACT"
    reveal.location = (220, -100)
    links.new(draw.outputs[0], reveal.inputs[0])
    links.new(doubled.outputs[0], reveal.inputs[1])
    edge = nodes.new("ShaderNodeMapRange")
    edge.location = (400, -100)
    edge.interpolation_type = "SMOOTHSTEP"
    edge.clamp = True
    edge.inputs["From Min"].default_value = -0.04
    edge.inputs["From Max"].default_value = 0.04
    edge.inputs["To Min"].default_value = 0.0
    edge.inputs["To Max"].default_value = 1.0
    links.new(reveal.outputs[0], edge.inputs["Value"])

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (400, 150)
    emission.inputs["Color"].default_value = _rgba(
        hc.palette_color(scene_config, spec["emission_color_ref"])
    )
    emission.inputs["Strength"].default_value = float(spec.get("emission_strength", 8.0))
    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (400, 320)
    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (620, 60)
    links.new(edge.outputs["Result"], mix.inputs["Fac"])
    links.new(transparent.outputs["BSDF"], mix.inputs[1])
    links.new(emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], output.inputs["Surface"])
    return material


def _node_named(material, name):
    if material is None or not material.use_nodes:
        return None
    return material.node_tree.nodes.get(name)


def _animate_presence(material, keys) -> None:
    """Ramp a material's ``aoi_presence`` value node over the given keyframes."""
    node = _node_named(material, "aoi_presence")
    if node is None:
        return
    _keyframe_socket(material.node_tree, node.outputs[0], keys, interpolation="BEZIER")


def _animate_emission_strength(material, base_strength, keys) -> None:
    if material is None:
        return
    node = next(
        (n for n in material.node_tree.nodes if n.type == "EMISSION"), None
    )
    if node is None:
        return
    _keyframe_socket(
        material.node_tree,
        node.inputs["Strength"],
        [(frame, base_strength * factor) for frame, factor in keys],
        interpolation="BEZIER",
    )


def _build_aoi_system(spec: dict, materials: dict, context: dict):
    """Build the whole surface-conforming AOI acquisition system.

    Everything is generated from the resolved fixture through
    ``aoi_system.describe``: border, interior, corner locks, per-corner target
    empties and the satellite beams that lock onto them. The footprint and its
    targets are parented to the Earth, and the beams reach them through
    constraints, so a single build serves every frame of the shot and nothing
    has to be re-registered as the camera or the planet moves.
    """
    scene_config = context["scene_config"]
    scene_spec = context["scene_spec"]
    fixture_id = context.get("aoi_fixture") or spec.get("fixture")

    description = ax.describe(scene_config, fixture_id, scene_spec)
    context["aoi_description"] = description

    # WEB-005A R3 persistent lock frame. ``description`` stays the authoritative footprint. With a
    # presentation block, the ribbons are built at that footprint in their settled dimensions and
    # carry a shape key at the acquisition presentation; ``presented`` is the same fixture
    # re-described at that scale (same centre, bearing and corner order), which is also where the
    # scan fill, the fan and the sensing-line anchors live while the observer is fixed.
    presentation = (spec.get("presentation") or {}).get("derived")
    if spec.get("presentation") and not presentation:
        raise KeyError(
            "AOI " + spec["id"] + " declares a presentation intent with no derived block; run "
            "hero/scripts/shot_plan.py --derive-presentation"
        )
    presented = description
    if presentation:
        settled = {k: v for k, v in presentation["settled"].items() if k != "span_km"}
        description = ax.describe(scene_config, fixture_id, scene_spec, settled)
        presented = ax.describe(scene_config, fixture_id, scene_spec, presentation["acquisition"])
        context["aoi_presented_description"] = presented
    fixture = description["fixture"]
    radius_bu = description["surface_radius_bu"]
    earth_radius_km = description["earth_radius_km"]
    frame_objects = context.setdefault("aoi_frame_objects", {}).setdefault(spec["id"], [])

    def morphing(obj, true_units, units, ribbon_radius, settled_km, acquisition_km, closed):
        """Register a frame ribbon; give it its presentation and weight keys when the frame morphs."""
        if presentation:
            moved, _ = _ribbon_vertices(units, ribbon_radius, settled_km, earth_radius_km, closed)
            heavy, _ = _ribbon_vertices(units, ribbon_radius, acquisition_km, earth_radius_km, closed)
            ar.add_morph_keys(obj, moved, heavy)
            ar.key_morph(obj, presentation["morph_keyframes"], presentation.get("weight_keyframes", ()))
            frame_objects.append(obj)
        return obj

    root = bpy.data.objects.new(spec["id"], None)
    root.empty_display_size = 0.08
    bpy.context.collection.objects.link(root)

    parent_id = spec.get("parent_id")
    if parent_id:
        parent = context["objects"].get(parent_id)
        if parent is None:
            raise KeyError(
                "AOI system " + spec["id"] + " requires object " + repr(parent_id)
                + ", which is not defined before it in this scene"
            )
        root.parent = parent
        root.matrix_parent_inverse = Matrix.Identity(4)

    def attach(obj):
        obj.parent = root
        obj.matrix_parent_inverse = Matrix.Identity(4)
        return obj

    # --- interior footprint -------------------------------------------------
    fill_material = materials.get(spec.get("fill_material"))
    attach(
        _fill_on_sphere(
            spec["id"] + "_fill", presented["fill_rows"], radius_bu, fill_material
        )
    )

    # --- border ------------------------------------------------------------
    border_material = materials.get(spec.get("border_material"))
    morphing(
        attach(
            _ribbon_on_sphere(
                spec["id"] + "_border",
                description["boundary_units"],
                radius_bu,
                fixture["border_width_km"],
                earth_radius_km,
                True,
                border_material,
            )
        ),
        description["boundary_units"], presented["boundary_units"], radius_bu,
        fixture["border_width_km"], presented["fixture"]["border_width_km"], True,
    )

    # --- border glow (WEB-005A R2) ----------------------------------------
    # A second, wider ribbon just beneath the crisp border carrying the soft halo. Geometry on
    # the sphere, so the glow scales with the frame at every camera distance.
    glow_cfg = spec.get("border_glow", {})
    glow_material = materials.get(glow_cfg.get("material"))
    if glow_material is not None:
        glow_radius = ax.surface_radius_bu(
            fixture, earth_radius_km, extra_offset_m=float(glow_cfg.get("offset_m", -60.0))
        )
        morphing(
            attach(
                _ribbon_on_sphere(
                    spec["id"] + "_border_glow",
                    description["boundary_units"],
                    glow_radius,
                    float(glow_cfg.get("width_km", 12.0)),
                    earth_radius_km,
                    True,
                    glow_material,
                )
            ),
            description["boundary_units"], presented["boundary_units"], glow_radius,
            float(glow_cfg.get("width_km", 12.0)),
            float((presentation or {}).get("acquisition", {}).get("glow_width_km", 0.0)), True,
        )

    # --- corner locks ------------------------------------------------------
    lock_material = materials.get(spec.get("corner_lock_material"))
    lock_radius = ax.surface_radius_bu(
        fixture, earth_radius_km, extra_offset_m=fixture["corner_lock_offset_m"]
    )
    for lock, shown in zip(description["corner_locks"], presented["corner_locks"]):
        morphing(
            attach(
                _ribbon_on_sphere(
                    spec["id"] + "_lock_" + lock["corner_id"],
                    [lock["arms"][0], lock["apex"], lock["arms"][1]],
                    lock_radius,
                    fixture["corner_lock_width_km"],
                    earth_radius_km,
                    False,
                    lock_material,
                )
            ),
            [lock["arms"][0], lock["apex"], lock["arms"][1]],
            [shown["arms"][0], shown["apex"], shown["arms"][1]], lock_radius,
            fixture["corner_lock_width_km"], presented["fixture"]["corner_lock_width_km"], False,
        )

    # --- per-corner beam targets -------------------------------------------
    # Real empties rather than baked coordinates: the beams aim at these, the
    # empties ride the Earth, so a beam endpoint is by construction the AOI
    # corner at every frame instead of a constant that happens to match on one.
    # WEB-005A R3: while the observer is fixed the lines lock the corners of the *presented* frame
    # (``beams.anchor: presented``) -- the true footprint is a few pixels across at that range and
    # four lines onto it read as one. Those corners lie on the footprint's own diagonals, the lines
    # retire before the frame starts to tighten, and the true corners are always built as
    # ``_true_<corner>`` empties, so the audit can measure both against each other.
    anchor_description = presented if spec.get("beams", {}).get("anchor") == "presented" else description
    targets = []
    for index, corner_id in enumerate(description["corner_order"]):
        target = bpy.data.objects.new(spec["id"] + "_target_" + corner_id, None)
        target.empty_display_type = "PLAIN_AXES"
        target.empty_display_size = 0.04
        bpy.context.collection.objects.link(target)
        target.location = tuple(anchor_description["corner_positions_bu"][index])
        attach(target)
        targets.append((corner_id, target))
        if presentation:
            true_corner = bpy.data.objects.new(spec["id"] + "_true_" + corner_id, None)
            true_corner.empty_display_type = "PLAIN_AXES"
            true_corner.empty_display_size = 0.02
            bpy.context.collection.objects.link(true_corner)
            true_corner.location = tuple(description["corner_positions_bu"][index])
            attach(true_corner)

    center_target = bpy.data.objects.new(spec["id"] + "_target_center", None)
    center_target.empty_display_type = "PLAIN_AXES"
    center_target.empty_display_size = 0.05
    bpy.context.collection.objects.link(center_target)
    center_target.location = tuple(description["center_position_bu"])
    attach(center_target)

    # --- beams -------------------------------------------------------------
    beam_spec = spec.get("beams", {})
    beam_material = materials.get(spec.get("beam_material"))
    source_id = beam_spec.get("source_object_id")
    source = context["objects"].get(source_id) if source_id else None
    if source_id and source is None:
        raise KeyError(
            "AOI beams reference source object " + repr(source_id)
            + ", which this scene does not define"
        )

    beams = []
    if source is not None and beam_material is not None:
        root_radius = float(beam_spec.get("root_radius_km", 9.0)) / ax.KM_PER_BLENDER_UNIT
        tip_radius = float(beam_spec.get("tip_radius_km", 30.0)) / ax.KM_PER_BLENDER_UNIT
        sides = int(beam_spec.get("sides", 14))
        beam_targets = list(targets)
        target_mode = str(beam_spec.get("target", "corners"))
        if target_mode == "center":
            beam_targets = [("center", center_target)]
        elif target_mode == "corners_and_center":
            beam_targets = list(targets) + [("center", center_target)]

        def _constrained_beam(name, root_r, tip_r, material, target):
            beam = _beam_mesh_object(name, root_r, tip_r, sides, material)
            copy_location = beam.constraints.new(type="COPY_LOCATION")
            copy_location.target = source
            stretch = beam.constraints.new(type="STRETCH_TO")
            stretch.target = target
            stretch.rest_length = 1.0
            stretch.volume = "NO_VOLUME"
            return beam

        for corner_id, target in beam_targets:
            beams.append(_constrained_beam(
                spec["id"] + "_beam_" + corner_id, root_radius, tip_radius, beam_material, target
            ))
            # WEB-005A R2 sensing lines: each thin core line carries a wider, fainter glow tube
            # around it, so the satellite-target link is legible at review size without ever
            # becoming a slab.
            glow_material = materials.get(beam_spec.get("glow_material"))
            if glow_material is not None:
                factor = float(beam_spec.get("glow_radius_factor", 4.0))
                beams.append(_constrained_beam(
                    spec["id"] + "_beamglow_" + corner_id, root_radius * factor,
                    tip_radius * factor, glow_material, target
                ))

        # Optional secondary support: one broad, very faint cone to the centre.
        cone_cfg = beam_spec.get("cone")
        cone_material = materials.get((cone_cfg or {}).get("material"))
        if cone_cfg and cone_material is not None:
            beams.append(_constrained_beam(
                spec["id"] + "_cone",
                float(cone_cfg.get("root_radius_km", 2.0)) / ax.KM_PER_BLENDER_UNIT,
                float(cone_cfg.get("tip_radius_km", 200.0)) / ax.KM_PER_BLENDER_UNIT,
                cone_material, center_target,
            ))

    # --- appearance / release timing ---------------------------------------
    scene_materials = scene_spec.get("materials", {})

    def _extra_keys(cfg, key_name):
        """Optional post-appearance ramp, authored in configuration as [[frame, factor], ...].

        An appear ramp alone can only say "this is here now". A shot needs to be able to say "this
        is resolved" as well, which is a second gesture after the first: the frame firming up once
        the scan has finished, the corner locks settling once they have landed. Without it the tail
        of the shot has nothing to do and reads as a pause rather than an ending.
        """
        extra = cfg.get(key_name)
        if not extra:
            return []
        return [(int(frame), float(factor)) for frame, factor in extra]

    def _presence_keys(cfg):
        """Transparent before it appears; optionally fades out over cfg["vanish"] = [start, end]."""
        if "appear_start_frame" not in cfg:
            return []
        keys = [(int(cfg["appear_start_frame"]) - 1, 0.0), (int(cfg["appear_start_frame"]), 1.0)]
        vanish = cfg.get("vanish")
        if vanish:
            keys += [(int(vanish[0]), 1.0), (int(vanish[1]), 0.0)]
        return keys

    border_cfg = spec.get("border", {})
    if "appear_start_frame" in border_cfg:
        _animate_emission_strength(
            border_material,
            float(scene_materials.get(spec.get("border_material"), {}).get("emission_strength", 11.0)),
            [
                (int(border_cfg["appear_start_frame"]), 0.0),
                (int(border_cfg["appear_end_frame"]), 1.0),
            ] + _extra_keys(border_cfg, "emphasis"),
        )
        _animate_presence(border_material, _presence_keys(border_cfg))

    lock_cfg = spec.get("corner_locks", {})
    if "appear_start_frame" in lock_cfg:
        _animate_emission_strength(
            lock_material,
            float(scene_materials.get(spec.get("corner_lock_material"), {}).get("emission_strength", 16.0)),
            [
                (int(lock_cfg["appear_start_frame"]), 0.0),
                (int(lock_cfg["appear_end_frame"]), 1.0),
            ] + _extra_keys(lock_cfg, "emphasis"),
        )
        _animate_presence(lock_material, _presence_keys(lock_cfg))

    fill_cfg = spec.get("fill", {})
    if "appear_start_frame" in fill_cfg:
        vanish = fill_cfg.get("vanish")
        _animate_presence(
            fill_material,
            [
                (int(fill_cfg["appear_start_frame"]), 0.0),
                (int(fill_cfg["appear_end_frame"]), 1.0),
            ] + _extra_keys(fill_cfg, "settle")
            + ([(int(vanish[0]), 1.0), (int(vanish[1]), 0.0)] if vanish else []),
        )

    if "appear_start_frame" in beam_spec:
        keys = [
            (int(beam_spec["appear_start_frame"]), 0.0),
            (int(beam_spec["appear_end_frame"]), 1.0),
        ]
        if "release_start_frame" in beam_spec:
            keys.append((int(beam_spec["release_start_frame"]), 1.0))
            keys.append((int(beam_spec["release_end_frame"]), 0.0))
        _animate_presence(beam_material, keys)
        _animate_presence(materials.get(beam_spec.get("glow_material")), keys)
        cone_cfg = beam_spec.get("cone") or {}
        _animate_presence(materials.get(cone_cfg.get("material")), keys)

    # border glow follows the border's own appearance/emphasis ramps
    glow_cfg = spec.get("border_glow", {})
    glow_material = materials.get(glow_cfg.get("material"))
    if glow_material is not None and "appear_start_frame" in border_cfg:
        glow_base = float(scene_materials.get(glow_cfg.get("material"), {}).get("emission_strength", 3.0))
        _animate_emission_strength(
            glow_material, glow_base,
            [
                (int(border_cfg["appear_start_frame"]), 0.0),
                (int(border_cfg["appear_end_frame"]), 1.0),
            ] + _extra_keys(border_cfg, "emphasis"),
        )
        _animate_presence(glow_material, _presence_keys(border_cfg))

    # corner locks: draw-in from the corner outward (R2 lock event)
    draw_node = _node_named(lock_material, "aoi_lock_draw")
    if draw_node is not None and "draw_start_frame" in lock_cfg:
        _keyframe_socket(
            lock_material.node_tree,
            draw_node.outputs[0],
            [
                (int(lock_cfg["draw_start_frame"]), 0.0),
                (int(lock_cfg["draw_end_frame"]), 1.0),
            ],
            interpolation="BEZIER",
        )

    # --- scan fan (WEB-005A R3) ---------------------------------------------
    fan_cfg = spec.get("scan_fan")
    if fan_cfg:
        for fan_object in ar.build_scan_fan(spec, fan_cfg, root, presented, materials, context, _ar_helpers()):
            beams.append(fan_object)

    # --- scan sweep --------------------------------------------------------
    # The ground band and the light curtain read the same keys, so they cross the footprint
    # together by construction rather than by matching two timings.
    sweep_cfg = spec.get("sweep", {})
    sweep_materials = [fill_material, materials.get((fan_cfg or {}).get("curtain_material"))]
    if "start_frame" in sweep_cfg:
        band = float(
            scene_materials.get(spec.get("fill_material"), {}).get("band_width", 0.13)
        )
        for sweep_material in sweep_materials:
            sweep_node = _node_named(sweep_material, "aoi_sweep_position")
            if sweep_node is None:
                continue
            _keyframe_socket(
                sweep_material.node_tree,
                sweep_node.outputs[0],
                [
                    (int(sweep_cfg["start_frame"]), -band),
                    (int(sweep_cfg["end_frame"]), 1.0 + band),
                ],
                interpolation="LINEAR",
            )

    print(
        "[hero] AOI fixture " + repr(description["fixture_id"])
        + ": centre (" + str(fixture["center_lat_deg"]) + ", " + str(fixture["center_lon_deg"])
        + "), span " + str(fixture["span_km"]) + " km, "
        + str(len(description["boundary_units"])) + " border samples, "
        + str(len(targets)) + " corner targets, " + str(len(beams)) + " beams"
    )
    return root


def _add_object(spec: dict, materials: dict, context: dict | None = None):
    kind = spec["type"]

    if kind == "satellite":
        return _build_satellite(spec, materials)

    if kind == "eo_satellite":
        if context is None:
            raise ValueError("object type 'eo_satellite' needs the build context")
        return sm.build_eo_satellite(spec, materials, context)

    if kind == "orbit_trail":
        if context is None:
            raise ValueError("object type 'orbit_trail' needs the build context")
        return sm.build_orbit_trail(spec, materials, context)

    if kind == "aoi_system":
        if context is None:
            raise ValueError(
                "object type 'aoi_system' needs the build context; call _add_object from build()"
            )
        return _build_aoi_system(spec, materials, context)

    if kind == "aoi_relief":
        if context is None:
            raise ValueError("object type 'aoi_relief' needs the build context")
        return ar.build_aoi_relief(spec, materials, context, _ar_helpers())

    location = tuple(spec.get("location", (0.0, 0.0, 0.0)))

    if kind == "uv_sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=float(spec.get("radius", 1.0)),
            segments=int(spec.get("segments", 32)),
            ring_count=int(spec.get("rings", 16)),
            location=location,
        )
    elif kind == "plane":
        bpy.ops.mesh.primitive_plane_add(
            size=float(spec.get("size", 2.0)), location=location
        )
    elif kind == "cube":
        bpy.ops.mesh.primitive_cube_add(
            size=float(spec.get("size", 2.0)), location=location
        )
    else:
        raise ValueError("unsupported object type " + repr(kind) + " for " + spec["id"])

    obj = bpy.context.active_object
    obj.name = spec["id"]

    if "rotation_euler_deg" in spec:
        obj.rotation_euler = _euler_from_deg(spec["rotation_euler_deg"])

    if spec.get("shade_smooth"):
        for polygon in obj.data.polygons:
            polygon.use_smooth = True

    material_name = spec.get("material")
    if material_name:
        if material_name not in materials:
            raise KeyError(
                "object " + spec["id"] + " references undefined material " + material_name
            )
        obj.data.materials.append(materials[material_name])

    # A nested transparent envelope is lighting decoration, not an occluder;
    # letting one cast shadow rays darkens the very limb it is meant to lift.
    if spec.get("cast_shadow") is False:
        try:
            obj.visible_shadow = False
        except AttributeError:
            pass
    return obj


def _apply_object_animation(obj, spec: dict) -> None:
    location_keyframes = spec.get("location_keyframes")
    rotation_keyframes = spec.get("rotation_keyframes")
    if not location_keyframes and not rotation_keyframes:
        return

    frames = sorted(
        {int(kf["frame"]) for kf in (location_keyframes or []) + (rotation_keyframes or [])}
    )
    by_frame_location = {int(kf["frame"]): kf["location"] for kf in (location_keyframes or [])}
    by_frame_rotation = {
        int(kf["frame"]): kf["rotation_euler_deg"] for kf in (rotation_keyframes or [])
    }

    base_location = obj.location.copy()
    base_rotation = tuple(obj.rotation_euler)

    for frame in frames:
        bpy.context.scene.frame_set(frame)
        if frame in by_frame_location:
            obj.location = tuple(by_frame_location[frame])
            base_location = obj.location.copy()
        else:
            obj.location = base_location
        if frame in by_frame_rotation:
            obj.rotation_euler = _euler_from_deg(by_frame_rotation[frame])
            base_rotation = tuple(obj.rotation_euler)
        else:
            obj.rotation_euler = base_rotation
        obj.keyframe_insert(data_path="location", frame=frame)
        obj.keyframe_insert(data_path="rotation_euler", frame=frame)

    _smooth_fcurves(obj)


def _apply_aim(obj, aim_spec: dict) -> None:
    """Blend a second Track To toward another target with keyframed influence.

    The satellite's base attitude is nadir (its track target is the Earth). During acquisition
    it slews toward the footprint centre and back -- the attitude an agile EO platform actually
    takes for an off-nadir collect -- and the influence ramp is what makes that a motion rather
    than a snap.
    """
    target = bpy.data.objects.get(aim_spec["target_id"])
    if target is None:
        raise KeyError("aim target " + repr(aim_spec["target_id"]) + " is not built")
    constraint = obj.constraints.new(type="TRACK_TO")
    constraint.name = "aim"
    constraint.target = target
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"
    keys = aim_spec.get("influence_keyframes", [])
    if not keys:
        constraint.influence = float(aim_spec.get("influence", 1.0))
        return
    for key in sorted(keys, key=lambda k: int(k["frame"])):
        constraint.influence = float(key["value"])
        constraint.keyframe_insert(data_path="influence", frame=int(key["frame"]))
    animation = obj.animation_data
    action = animation.action if animation else None
    if action:
        for fcurve in _action_fcurves(action):
            if fcurve.data_path.endswith('constraints["aim"].influence'):
                for point in fcurve.keyframe_points:
                    point.interpolation = "BEZIER"
                    point.handle_left_type = "AUTO_CLAMPED"
                    point.handle_right_type = "AUTO_CLAMPED"


def _apply_array_drive(object_id: str, pivot_spec: dict, lights: dict) -> None:
    """Point a solar-array pivot at a light about its own wing axis (a solar array drive)."""
    pivot = bpy.data.objects.get(object_id + "_array_" + pivot_spec["side"])
    target = lights.get(pivot_spec.get("target_id", "sun")) or bpy.data.objects.get(pivot_spec.get("target_id", "sun"))
    if pivot is None or target is None:
        return
    constraint = pivot.constraints.new(type="LOCKED_TRACK")
    constraint.target = target
    constraint.track_axis = pivot_spec.get("track_axis", "TRACK_Z")
    constraint.lock_axis = pivot_spec.get("lock_axis", "LOCK_X")


def _apply_post_processing(post: dict | None) -> None:
    """Compositor glare (bloom) so emissive acquisition elements carry a controlled halo.

    Threshold sits above anything sunlit on the planet, so only the emissive frame, lines and
    highlights bloom; the Earth itself is untouched.
    """
    scene = bpy.context.scene
    if not post or not post.get("glare"):
        scene.use_nodes = False
        return
    glare_spec = post["glare"]
    scene.use_nodes = True
    tree = scene.node_tree
    for node in list(tree.nodes):
        tree.nodes.remove(node)
    render_layers = tree.nodes.new("CompositorNodeRLayers")
    render_layers.location = (-400, 0)
    glare = tree.nodes.new("CompositorNodeGlare")
    glare.location = (0, 0)
    glare.glare_type = str(glare_spec.get("type", "BLOOM"))
    try:
        glare.quality = str(glare_spec.get("quality", "HIGH"))
    except TypeError:
        pass
    for name, key, default in (
        ("Threshold", "threshold", 1.6),
        ("Strength", "strength", 0.3),
        ("Size", "size", 6),
        ("Saturation", "saturation", 1.0),
    ):
        if name in glare.inputs:
            value = glare_spec.get(key, default)
            try:
                glare.inputs[name].default_value = type(glare.inputs[name].default_value)(value)
            except (TypeError, ValueError):
                pass
        elif hasattr(glare, key):
            try:
                setattr(glare, key, glare_spec.get(key, default))
            except (TypeError, ValueError):
                pass
    if "Tint" in glare.inputs and glare_spec.get("tint"):
        glare.inputs["Tint"].default_value = (*[float(c) for c in glare_spec["tint"]], 1.0)
    composite = tree.nodes.new("CompositorNodeComposite")
    composite.location = (400, 0)
    tree.links.new(render_layers.outputs["Image"], glare.inputs["Image"])
    tree.links.new(glare.outputs["Image"], composite.inputs["Image"])


def _apply_track_to(obj, target) -> None:
    constraint = obj.constraints.new(type="TRACK_TO")
    constraint.target = target
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"


def _add_light(spec: dict, scene_config: dict):
    light_data = bpy.data.lights.new(name=spec["id"], type=spec["type"])
    light_data.energy = float(spec.get("energy", 100.0))
    if spec.get("color_ref"):
        light_data.color = tuple(hc.palette_color(scene_config, spec["color_ref"]))
    if spec["type"] == "AREA" and "size" in spec:
        light_data.size = float(spec["size"])
    if spec["type"] == "SUN" and "angle_deg" in spec:
        light_data.angle = math.radians(float(spec["angle_deg"]))

    light_object = bpy.data.objects.new(name=spec["id"], object_data=light_data)
    bpy.context.collection.objects.link(light_object)
    light_object.location = tuple(spec.get("location", (0.0, 0.0, 0.0)))
    if "look_at" in spec:
        light_object.rotation_euler = _look_at_euler(
            light_object.location, spec["look_at"]
        )
    elif "rotation_euler_deg" in spec:
        light_object.rotation_euler = _euler_from_deg(spec["rotation_euler_deg"])
    return light_object


def _apply_camera_track(camera_object, track_spec):
    """Lock the camera's aim to a scene object through a blended Track To.

    WEB-HERO-001D needs two different things from one continuous camera. The
    establish is composed by hand -- the planet deliberately sits off-axis so a
    headline has somewhere to live -- while everything from acquisition onward
    must stay exactly registered to a footprint that is riding a rotating
    planet.

    Authored look-at keyframes alone can only be correct *at* a keyframe: the
    AOI travels along an arc between keys while an interpolated camera aims
    along a chord, so the footprint drifts in frame in between. A Track To
    constraint removes that residual by construction, the same way the Phase-C
    beams derive their endpoints instead of baking them.

    The constraint's influence is itself keyframed, so the establish keeps its
    authored composition at influence 0 and the shot hands over to the lock
    before acquisition. The derived keyframes on the far side of the handover
    already aim at the AOI centre, so the blend has nothing to correct and
    cannot swing the camera -- it only holds the aim exact between keys.
    """
    if not track_spec:
        return None
    target_name = track_spec["target_id"]
    target = bpy.data.objects.get(target_name)
    if target is None:
        raise KeyError(
            "camera tracks " + repr(target_name) + ", which this scene does not build"
        )
    constraint = camera_object.constraints.new(type="TRACK_TO")
    constraint.name = "aoi_lock"
    constraint.target = target
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"

    keys = track_spec.get("influence_keyframes")
    if not keys:
        constraint.influence = float(track_spec.get("influence", 1.0))
        return constraint

    for key in sorted(keys, key=lambda k: int(k["frame"])):
        constraint.influence = float(key["value"])
        constraint.keyframe_insert(data_path="influence", frame=int(key["frame"]))
    animation = camera_object.animation_data
    action = animation.action if animation else None
    if action:
        for fcurve in _action_fcurves(action):
            if fcurve.data_path.endswith('constraints["aoi_lock"].influence'):
                for point in fcurve.keyframe_points:
                    point.interpolation = "BEZIER"
                    point.handle_left_type = "AUTO_CLAMPED"
                    point.handle_right_type = "AUTO_CLAMPED"
    return constraint


def _lock_off_camera(camera_object, camera_data, fixed_through_frame) -> None:
    """WEB-005A R3 fixed observer (A-HERO-15): hold every camera channel constant up to a frame.

    A locked-off camera is not "two equal keys and a smooth curve between them" -- that leaves the
    result to the handle solver. Every key before ``fixed_through_frame`` must equal the key on it,
    which is checked here rather than assumed, and the segments between them are made CONSTANT, so
    location, rotation, focal length and lens shift cannot move by construction. The key on the
    frame itself keeps its smoothed handles: the approach eases out of a standstill.
    """
    if fixed_through_frame is None:
        return
    limit = int(fixed_through_frame)
    for datablock in (camera_object, camera_data):
        animation = getattr(datablock, "animation_data", None)
        action = getattr(animation, "action", None) if animation else None
        if not action:
            continue
        for fcurve in _action_fcurves(action):
            if "constraints" in fcurve.data_path:
                continue
            held = [p for p in fcurve.keyframe_points if p.co.x <= limit]
            if not held:
                continue
            reference = held[-1].co.y
            for point in held:
                if abs(point.co.y - reference) > 1.0e-6:
                    raise ValueError(
                        "camera channel " + fcurve.data_path + "[" + str(fcurve.array_index)
                        + "] changes before fixed_through_frame " + str(limit)
                    )
                if point.co.x < limit:
                    point.interpolation = "CONSTANT"


def _add_camera(spec: dict, scene_config: dict):
    defaults = scene_config.get("camera_defaults", {})
    camera_data = bpy.data.cameras.new(name="hero_camera")
    camera_data.type = defaults.get("type", "PERSP")
    camera_data.lens = float(
        spec.get("focal_length_mm", defaults.get("focal_length_mm", 50.0))
    )
    camera_data.sensor_width = float(defaults.get("sensor_width_mm", 36.0))
    camera_data.clip_start = float(defaults.get("clip_start", 0.1))
    camera_data.clip_end = float(defaults.get("clip_end", 1000.0))

    camera_object = bpy.data.objects.new(name="hero_camera", object_data=camera_data)
    bpy.context.collection.objects.link(camera_object)
    bpy.context.scene.camera = camera_object

    _apply_camera_track(camera_object, spec.get("track"))

    keyframes = spec.get("keyframes")
    if keyframes:
        for kf in sorted(keyframes, key=lambda k: k["frame"]):
            frame = int(kf["frame"])
            bpy.context.scene.frame_set(frame)
            camera_object.location = tuple(kf["location"])
            camera_object.rotation_euler = _look_at_euler(
                kf["location"], kf.get("look_at", spec.get("look_at", (0.0, 0.0, 0.0)))
            )
            if "focal_length_mm" in kf:
                camera_data.lens = float(kf["focal_length_mm"])
                camera_data.keyframe_insert(data_path="lens", frame=frame)
            camera_object.keyframe_insert(data_path="location", frame=frame)
            camera_object.keyframe_insert(data_path="rotation_euler", frame=frame)
        _smooth_fcurves(camera_object)
        # WEB-005A R2: lens shift moves the frame without moving the aim. The AOI track
        # constraint keeps the footprint on the optical axis; the shift decides where in the
        # frame that axis lands, so the target can sit right of centre while the lock holds.
        for kf in sorted(spec.get("shift_keyframes", []), key=lambda k: int(k["frame"])):
            frame = int(kf["frame"])
            camera_data.shift_x = float(kf.get("shift_x", 0.0))
            camera_data.shift_y = float(kf.get("shift_y", 0.0))
            camera_data.keyframe_insert(data_path="shift_x", frame=frame)
            camera_data.keyframe_insert(data_path="shift_y", frame=frame)
        _smooth_data_fcurves(camera_data)
        _lock_off_camera(camera_object, camera_data, spec.get("fixed_through_frame"))
    else:
        camera_object.location = tuple(spec.get("location", (0.0, -10.0, 2.0)))
        camera_object.rotation_euler = _look_at_euler(
            camera_object.location, spec.get("look_at", (0.0, 0.0, 0.0))
        )
    return camera_object


def _build_world(scene_config: dict, scene_spec: dict | None = None) -> None:
    world_spec = dict(scene_config.get("world", {}))
    if scene_spec:
        world_spec.update(scene_spec.get("world_overrides", {}))
    world = bpy.data.worlds.new("hero_world")
    world.use_nodes = True
    nt = world.node_tree
    nodes, links = nt.nodes, nt.links
    background = nodes.get("Background")
    output = nodes.get("World Output")

    color = hc.palette_color(scene_config, world_spec.get("background_color_ref", "space_deep"))
    background.inputs["Color"].default_value = _rgba(color)
    background.inputs["Strength"].default_value = float(world_spec.get("background_strength", 1.0))

    stars = world_spec.get("stars")
    if stars and stars.get("enabled", True):
        tex_coord = nodes.new("ShaderNodeTexCoord")
        tex_coord.location = (-1100, -300)
        star_color = hc.palette_color(scene_config, stars.get("color_ref", "neutral_light"))

        def _star_layer(y, scale, point_size, brightness_lo, brightness_hi):
            # A single uniform Voronoi threshold makes every point the same
            # size and brightness, which reads as an obvious repeating grid
            # ("procedural cheapness"/banding) rather than a real field. Each
            # layer instead pulls its own per-cell brightness from Voronoi's
            # Color output, so points vary the way real star magnitudes do.
            voronoi = nodes.new("ShaderNodeTexVoronoi")
            voronoi.location = (-850, y)
            try:
                voronoi.voronoi_dimensions = "3D"
            except TypeError:
                pass
            _set_input(voronoi, "Scale", float(scale))
            _set_input(voronoi, "Randomness", 1.0)

            ramp = nodes.new("ShaderNodeValToRGB")
            ramp.location = (-600, y)
            ramp.color_ramp.elements[0].position = 0.0
            ramp.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)
            ramp.color_ramp.elements[1].position = max(0.001, float(point_size))
            ramp.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0)
            distance_out = "Distance" if "Distance" in voronoi.outputs else voronoi.outputs[0].name
            links.new(voronoi.outputs[distance_out], ramp.inputs["Fac"])

            brightness = nodes.new("ShaderNodeMapRange")
            brightness.location = (-600, y - 130)
            brightness.inputs["From Min"].default_value = 0.0
            brightness.inputs["From Max"].default_value = 1.0
            brightness.inputs["To Min"].default_value = float(brightness_lo)
            brightness.inputs["To Max"].default_value = float(brightness_hi)
            color_out = "Color" if "Color" in voronoi.outputs else voronoi.outputs[-1].name
            separate = nodes.new("ShaderNodeSeparateColor")
            separate.location = (-750, y - 130)
            links.new(voronoi.outputs[color_out], separate.inputs["Color"])
            links.new(separate.outputs[0], brightness.inputs["Value"])

            point_mask = nodes.new("ShaderNodeMath")
            point_mask.operation = "MULTIPLY"
            point_mask.location = (-350, y)
            links.new(ramp.outputs["Color"], point_mask.inputs[0])
            links.new(brightness.outputs["Result"], point_mask.inputs[1])
            return point_mask

        bright_layer = _star_layer(-250, stars.get("scale", 190.0), stars.get("point_size", 0.05), 0.5, 1.0)
        dim_layer = _star_layer(-500, stars.get("scale", 190.0) * 2.4, stars.get("point_size", 0.05) * 0.55, 0.25, 0.55)

        combine = nodes.new("ShaderNodeMath")
        combine.operation = "MAXIMUM"
        combine.location = (-150, -350)
        links.new(bright_layer.outputs["Value"], combine.inputs[0])
        links.new(dim_layer.outputs["Value"], combine.inputs[1])

        star_emission = nodes.new("ShaderNodeBackground")
        star_emission.location = (250, -300)
        star_emission.inputs["Color"].default_value = _rgba(star_color)
        star_emission.inputs["Strength"].default_value = 0.0

        multiply_strength = nodes.new("ShaderNodeMath")
        multiply_strength.operation = "MULTIPLY"
        multiply_strength.location = (50, -450)
        multiply_strength.inputs[1].default_value = float(stars.get("strength", 4.0))
        links.new(combine.outputs["Value"], multiply_strength.inputs[0])

        # A large-scale, very-low-contrast brightness drift across the sky
        # ("restrained star/nebula depth") so the field doesn't look like a
        # flat, uniformly-lit decal.
        depth_noise = nodes.new("ShaderNodeTexNoise")
        depth_noise.location = (-850, -650)
        _set_input(depth_noise, "Scale", 1.4)
        _set_input(depth_noise, "Detail", 2.0)
        links.new(tex_coord.outputs["Generated"], depth_noise.inputs["Vector"])
        depth_range = nodes.new("ShaderNodeMapRange")
        depth_range.location = (-600, -650)
        depth_range.inputs["From Min"].default_value = 0.3
        depth_range.inputs["From Max"].default_value = 0.7
        depth_range.inputs["To Min"].default_value = 0.75
        depth_range.inputs["To Max"].default_value = 1.15
        depth_range.clamp = True
        fac_name = "Fac" if "Fac" in depth_noise.outputs else depth_noise.outputs[0].name
        links.new(depth_noise.outputs[fac_name], depth_range.inputs["Value"])

        depth_multiply = nodes.new("ShaderNodeMath")
        depth_multiply.operation = "MULTIPLY"
        depth_multiply.location = (250, -450)
        links.new(multiply_strength.outputs["Value"], depth_multiply.inputs[0])
        links.new(depth_range.outputs["Result"], depth_multiply.inputs[1])
        links.new(depth_multiply.outputs["Value"], star_emission.inputs["Strength"])

        # Wire each layer's own Voronoi vector input from the shared coord.
        for node in nodes:
            if node.bl_idname == "ShaderNodeTexVoronoi" and not node.inputs["Vector"].links:
                links.new(tex_coord.outputs["Generated"], node.inputs["Vector"])

        add_shader = nodes.new("ShaderNodeAddShader")
        add_shader.location = (450, 0)
        links.new(background.outputs["Background"], add_shader.inputs[0])
        links.new(star_emission.outputs["Background"], add_shader.inputs[1])
        links.new(add_shader.outputs["Shader"], output.inputs["Surface"])
    else:
        links.new(background.outputs["Background"], output.inputs["Surface"])

    bpy.context.scene.world = world


def build(scene_id: str, scene_config=None, frame: int | None = None, aoi_fixture: str | None = None):
    """Build ``scene_id`` into the current Blender session and return its spec.

    ``frame`` overrides which frame the scene is left on after any keyframe
    animation is authored (default: the scene's own ``frame`` field, or 1).

    ``aoi_fixture`` overrides which AOI fixture the scene's AOI system reads
    from ``aoi_injection_interface``. It exists so the same scene can be built
    against a different footprint from the command line, which is the whole
    point of the AOI being configuration-driven.
    """
    scene_config = scene_config or hc.load_scene_config()
    scenes = scene_config.get("scenes", {})
    spec = hc.resolve_scene_spec(scene_id, scenes)

    _clear_scene()
    _build_world(scene_config, spec)

    anim = spec.get("animation")
    if anim:
        bpy.context.scene.frame_start = int(anim.get("frame_start", 1))
        bpy.context.scene.frame_end = int(anim.get("frame_end", bpy.context.scene.frame_start))

    sun_direction = _primary_light_direction(spec)
    materials = {
        name: _build_material(name, material_spec, scene_config, sun_direction)
        for name, material_spec in spec.get("materials", {}).items()
    }

    built_objects = {}
    context = {
        "scene_id": scene_id,
        "scene_config": scene_config,
        "scene_spec": spec,
        "objects": built_objects,
        "aoi_fixture": aoi_fixture,
    }
    for object_spec in spec.get("objects", []):
        obj = _add_object(object_spec, materials, context)
        built_objects[object_spec["id"]] = obj
        _apply_object_animation(obj, object_spec)

    for object_spec in spec.get("objects", []):
        track_id = object_spec.get("track_target_id")
        if track_id:
            if track_id not in built_objects:
                raise KeyError(
                    "object " + object_spec["id"] + " tracks undefined object " + track_id
                )
            _apply_track_to(built_objects[object_spec["id"]], built_objects[track_id])
        aim = object_spec.get("aim")
        if aim:
            _apply_aim(built_objects[object_spec["id"]], aim)

    lights = {}
    for light_spec in spec.get("lights", []):
        lights[light_spec["id"]] = _add_light(light_spec, scene_config)
    _add_camera(spec.get("camera", {}), scene_config)

    # Solar array drives need the sun object, so they are wired after the lights exist.
    for object_spec in spec.get("objects", []):
        for pivot_spec in object_spec.get("array_drive", []):
            _apply_array_drive(object_spec["id"], pivot_spec, lights)

    isolation = spec.get("lighting_isolation")
    if isolation:
        sm.isolate_satellite_lighting(
            lights.get(isolation.get("sun_id", "sun")),
            isolation.get("satellite_ids", []),
            built_objects,
            isolation,
        )

    _apply_post_processing(spec.get("post_processing"))

    overrides = spec.get("render_overrides") or {}
    if "transparent_max_bounces" in overrides:
        bpy.context.scene.cycles.transparent_max_bounces = int(overrides["transparent_max_bounces"])

    target_frame = frame if frame is not None else int(spec.get("frame", 1))
    bpy.context.scene.frame_set(target_frame)

    view_transform = scene_config.get("view_transform")
    if view_transform:
        try:
            bpy.context.scene.view_settings.view_transform = view_transform
        except TypeError:
            print("[hero] view transform " + view_transform + " unavailable; default kept")
    return spec


def _main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Build a hero scene from configuration.")
    parser.add_argument("--scene", default="benchmark_neutral")
    parser.add_argument("--frame", type=int, default=None)
    parser.add_argument(
        "--aoi-fixture",
        default=None,
        help="override the AOI fixture named in aoi_injection_interface.active_fixture",
    )
    parser.add_argument("--save", action="store_true", help="save a working .blend")
    parser.add_argument(
        "--out",
        default=None,
        help="working .blend path (default: hero/renders/work/<scene>.blend)",
    )
    args = parser.parse_args(hc.argv_after_double_dash())

    build(args.scene, frame=args.frame, aoi_fixture=args.aoi_fixture)
    print("[hero] built scene " + args.scene)

    if args.save:
        out = Path(args.out) if args.out else hc.RENDERS_DIR / "work" / (args.scene + ".blend")
        hc.ensure_dir(out.parent)
        bpy.ops.wm.save_as_mainfile(filepath=str(out))
        print("[hero] saved working file -> " + hc.relpath(out))


if __name__ == "__main__":
    _main()
