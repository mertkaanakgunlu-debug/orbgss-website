"""Build a hero scene from committed configuration inside Blender.

Configuration in ``hero/config/scene.json`` is the source of scene truth; this
module only translates it. Run it standalone to materialize a working .blend:

    blender -b -P hero/scripts/build_scene.py -- --scene benchmark_neutral --save

Later phases add scene definitions to scene.json and, where a definition needs
procedural geometry beyond the primitive vocabulary here, extend ``_add_object``
rather than hard-coding values in a render script.
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


def _build_material(name: str, spec: dict, scene_config: dict):
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
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = _rgba(emission)
        elif "Emission" in bsdf.inputs:
            bsdf.inputs["Emission"].default_value = _rgba(emission)
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = float(
                spec.get("emission_strength", 1.0)
            )
    return material


def _add_object(spec: dict, materials: dict):
    kind = spec["type"]
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
    camera_object.location = tuple(spec.get("location", (0.0, -10.0, 2.0)))
    camera_object.rotation_euler = _look_at_euler(
        camera_object.location, spec.get("look_at", (0.0, 0.0, 0.0))
    )
    bpy.context.scene.camera = camera_object
    return camera_object


def _build_world(scene_config: dict) -> None:
    world_spec = scene_config.get("world", {})
    world = bpy.data.worlds.new("hero_world")
    world.use_nodes = True
    background = world.node_tree.nodes.get("Background")
    if background is not None:
        color = hc.palette_color(
            scene_config, world_spec.get("background_color_ref", "space_deep")
        )
        background.inputs["Color"].default_value = _rgba(color)
        background.inputs["Strength"].default_value = float(
            world_spec.get("background_strength", 1.0)
        )
    bpy.context.scene.world = world


def build(scene_id: str, scene_config=None):
    """Build ``scene_id`` into the current Blender session and return its spec."""
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
    bpy.context.scene.frame_set(int(spec.get("frame", 1)))
    _build_world(scene_config)

    materials = {
        name: _build_material(name, material_spec, scene_config)
        for name, material_spec in spec.get("materials", {}).items()
    }
    for object_spec in spec.get("objects", []):
        _add_object(object_spec, materials)
    for light_spec in spec.get("lights", []):
        _add_light(light_spec, scene_config)
    _add_camera(spec.get("camera", {}), scene_config)

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
    parser.add_argument("--save", action="store_true", help="save a working .blend")
    parser.add_argument(
        "--out",
        default=None,
        help="working .blend path (default: hero/renders/work/<scene>.blend)",
    )
    args = parser.parse_args(hc.argv_after_double_dash())

    build(args.scene)
    print("[hero] built scene " + args.scene)

    if args.save:
        out = Path(args.out) if args.out else hc.RENDERS_DIR / "work" / (args.scene + ".blend")
        hc.ensure_dir(out.parent)
        bpy.ops.wm.save_as_mainfile(filepath=str(out))
        print("[hero] saved working file -> " + hc.relpath(out))


if __name__ == "__main__":
    _main()
