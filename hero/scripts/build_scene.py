"""Build a hero scene from committed configuration inside Blender.

Configuration in ``hero/config/scene.json`` is the source of scene truth; this
module only translates it. Run it standalone to materialize a working .blend:

    blender -b -P hero/scripts/build_scene.py -- --scene benchmark_neutral --save

Later phases add scene definitions to scene.json and, where a definition needs
procedural geometry beyond the primitive vocabulary here, extend ``_add_object``
rather than hard-coding values in a render script.

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

import bpy  # noqa: E402  (Blender-only import, after sys.path bootstrap)
from mathutils import Vector  # noqa: E402

import hero_common as hc  # noqa: E402


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

def _build_principled_material(name: str, spec: dict, scene_config: dict):
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
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

    links.new(day_tex_node.outputs["Color"], bsdf.inputs["Base Color"])
    links.new(night_tex_node.outputs["Color"], emission.inputs["Color"])

    links.new(geometry.outputs["Normal"], dot.inputs[0])
    links.new(sun_vec.outputs["Vector"], dot.inputs[1])
    links.new(dot.outputs["Value"], terminator.inputs["Value"])

    links.new(terminator.outputs["Result"], mix_shader.inputs["Fac"])
    links.new(bsdf.outputs["BSDF"], mix_shader.inputs[1])
    links.new(emission.outputs["Emission"], mix_shader.inputs[2])
    links.new(mix_shader.outputs["Shader"], output.inputs["Surface"])
    return material


def _build_atmosphere_material(name: str, spec: dict, scene_config: dict):
    """Fresnel rim-glow shell: transparent facing the camera, emissive at
    grazing angles, so the atmosphere reads as a limb glow that visibly
    follows the globe instead of a flat neon outline.
    """
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    nt = material.node_tree
    nodes, links = nt.nodes, nt.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (600, 0)

    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (0, -150)

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (0, 150)
    color = hc.palette_color(scene_config, spec.get("rim_color_ref", "atmosphere_cyan"))
    emission.inputs["Color"].default_value = _rgba(color)
    emission.inputs["Strength"].default_value = float(spec.get("strength", 2.4))

    fresnel = nodes.new("ShaderNodeFresnel")
    fresnel.location = (-250, 0)
    fresnel.inputs["IOR"].default_value = float(spec.get("fresnel_ior", 1.2))

    falloff = nodes.new("ShaderNodeMapRange")
    falloff.location = (-50, 0)
    falloff.inputs["From Min"].default_value = float(spec.get("falloff_min", 0.3))
    falloff.inputs["From Max"].default_value = float(spec.get("falloff_max", 1.0))
    falloff.inputs["To Min"].default_value = 0.0
    falloff.inputs["To Max"].default_value = 1.0
    falloff.clamp = True

    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (300, 0)

    links.new(fresnel.outputs["Fac"], falloff.inputs["Value"])
    links.new(falloff.outputs["Result"], mix.inputs["Fac"])
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
    return material


def _build_material(name: str, spec: dict, scene_config: dict, sun_direction=(0.0, 0.0, 1.0)):
    kind = spec.get("type", "principled")
    if kind == "principled":
        return _build_principled_material(name, spec, scene_config)
    if kind == "earth_day_night":
        return _build_earth_material(name, spec, scene_config, sun_direction)
    if kind == "atmosphere_shell":
        return _build_atmosphere_material(name, spec, scene_config)
    if kind == "solar_panel":
        return _build_solar_panel_material(name, spec, scene_config)
    raise ValueError("unsupported material type " + repr(kind) + " for " + name)


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

    bpy.ops.mesh.primitive_cube_add(size=1.0)
    bus = bpy.context.active_object
    bus.name = spec["id"] + "_bus"
    bus.scale = (bus_size[0] / 2, bus_size[1] / 2, bus_size[2] / 2)
    bus.parent = root
    for polygon in bus.data.polygons:
        polygon.use_smooth = False
    if bus_material:
        bus.data.materials.append(bus_material)

    for side, sign in (("pos", 1.0), ("neg", -1.0)):
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        panel = bpy.context.active_object
        panel.name = spec["id"] + "_panel_" + side
        panel.scale = (panel_size[0] / 2, panel_size[1] / 2, 0.006)
        panel.parent = root
        panel.location = (sign * (bus_size[0] / 2 + panel_size[0] / 2 + 0.015), 0.0, 0.0)
        if panel_material:
            panel.data.materials.append(panel_material)

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

    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=bus_size[2] * 1.6, vertices=10)
    boom = bpy.context.active_object
    boom.name = spec["id"] + "_boom"
    boom.parent = root
    boom.rotation_euler = (0.0, math.radians(90.0), 0.0)
    boom.location = (bus_size[0] / 2 + bus_size[2] * 0.8, 0.0, 0.0)
    if bus_material:
        boom.data.materials.append(bus_material)

    scale = float(spec.get("scale", 1.0))
    root.scale = (scale, scale, scale)
    return root


def _add_object(spec: dict, materials: dict):
    kind = spec["type"]

    if kind == "satellite":
        return _build_satellite(spec, materials)

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
        tex_coord.location = (-900, -300)

        voronoi = nodes.new("ShaderNodeTexVoronoi")
        voronoi.location = (-650, -300)
        try:
            voronoi.voronoi_dimensions = "3D"
        except TypeError:
            pass
        _set_input(voronoi, "Scale", float(stars.get("scale", 260.0)))
        _set_input(voronoi, "Randomness", float(stars.get("randomness", 1.0)))

        star_ramp = nodes.new("ShaderNodeValToRGB")
        star_ramp.location = (-400, -300)
        threshold = float(stars.get("point_size", 0.045))
        star_color = hc.palette_color(scene_config, stars.get("color_ref", "neutral_light"))
        star_ramp.color_ramp.elements[0].position = 0.0
        star_ramp.color_ramp.elements[0].color = _rgba(star_color)
        star_ramp.color_ramp.elements[1].position = max(0.001, threshold)
        star_ramp.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0)

        star_emission = nodes.new("ShaderNodeBackground")
        star_emission.location = (-150, -300)
        star_emission.inputs["Strength"].default_value = float(stars.get("strength", 5.0))

        add_shader = nodes.new("ShaderNodeAddShader")
        add_shader.location = (200, 0)

        links.new(tex_coord.outputs["Generated"], voronoi.inputs["Vector"])
        distance_output = "Distance" if "Distance" in voronoi.outputs else voronoi.outputs[0].name
        links.new(voronoi.outputs[distance_output], star_ramp.inputs["Fac"])
        links.new(star_ramp.outputs["Color"], star_emission.inputs["Color"])
        links.new(background.outputs["Background"], add_shader.inputs[0])
        links.new(star_emission.outputs["Background"], add_shader.inputs[1])
        links.new(add_shader.outputs["Shader"], output.inputs["Surface"])
    else:
        links.new(background.outputs["Background"], output.inputs["Surface"])

    bpy.context.scene.world = world


def build(scene_id: str, scene_config=None, frame: int | None = None):
    """Build ``scene_id`` into the current Blender session and return its spec.

    ``frame`` overrides which frame the scene is left on after any keyframe
    animation is authored (default: the scene's own ``frame`` field, or 1).
    """
    scene_config = scene_config or hc.load_scene_config()
    scenes = scene_config.get("scenes", {})
    if scene_id not in scenes:
        raise KeyError(
            "scene " + repr(scene_id) + " is not defined in "
            + hc.relpath(hc.SCENE_CONFIG)
            + "; available: " + repr(sorted(scenes))
        )
    spec = scenes[scene_id]

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
    for object_spec in spec.get("objects", []):
        obj = _add_object(object_spec, materials)
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

    for light_spec in spec.get("lights", []):
        _add_light(light_spec, scene_config)
    _add_camera(spec.get("camera", {}), scene_config)

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
    parser.add_argument("--save", action="store_true", help="save a working .blend")
    parser.add_argument(
        "--out",
        default=None,
        help="working .blend path (default: hero/renders/work/<scene>.blend)",
    )
    args = parser.parse_args(hc.argv_after_double_dash())

    build(args.scene, frame=args.frame)
    print("[hero] built scene " + args.scene)

    if args.save:
        out = Path(args.out) if args.out else hc.RENDERS_DIR / "work" / (args.scene + ".blend")
        hc.ensure_dir(out.parent)
        bpy.ops.wm.save_as_mainfile(filepath=str(out))
        print("[hero] saved working file -> " + hc.relpath(out))


if __name__ == "__main__":
    _main()
