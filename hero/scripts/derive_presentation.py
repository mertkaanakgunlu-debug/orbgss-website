"""Derive the lock-frame presentation from the *evaluated* camera and write it into scene.json.

    blender -b -P hero/scripts/derive_presentation.py -- --scene hero_r3_preview_gate

``shot_plan.derive_presentation`` holds the rule: the presented span is
``max(true span, on-screen width x ground scale)``. The only thing it cannot know without Blender
is the ground scale between camera keys, because the camera is interpolated by Blender's own
F-curves. This measures that scale on every frame of the morph -- distance from the evaluated
camera to the AOI centre, evaluated focal length -- hands it to the same rule, and commits the
result, exactly as ``audit_shot.py`` measures the handoff anchor the page is then bound to.

The camera does not depend on the presentation, so whatever derived block is already committed is
good enough to build from; a scene with none is built from the planned (linear) scale first.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bpy  # noqa: E402

import aoi_system as ax  # noqa: E402
import build_scene  # noqa: E402
import hero_common as hc  # noqa: E402
import shot_plan as sp  # noqa: E402


def _aoi_object(scene: dict):
    return next(o for o in scene["objects"] if o.get("type") == "aoi_system" and "presentation" in o)


def main() -> None:
    parser = argparse.ArgumentParser(description="Derive the lock-frame presentation from the evaluated camera.")
    parser.add_argument("--scene", default="hero_r3_preview_gate")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(hc.argv_after_double_dash())

    raw = hc.SCENE_CONFIG.read_bytes().decode("utf-8")
    config = json.loads(raw)
    aoi = _aoi_object(config["scenes"][args.scene])
    if "derived" not in aoi["presentation"]:
        aoi["presentation"]["derived"] = sp.derive_presentation(config, args.scene)

    build_scene.build(args.scene, config)
    scene = bpy.context.scene
    camera = scene.camera
    target = bpy.data.objects[aoi["id"] + "_target_center"]
    start, end = aoi["presentation"]["screen_intent"]["morph_frames"]
    measured = {}
    for frame in range(int(start), int(end) + 1):
        scene.frame_set(frame)
        depsgraph = bpy.context.evaluated_depsgraph_get()
        cam = camera.evaluated_get(depsgraph)
        distance = (cam.matrix_world.translation - target.evaluated_get(depsgraph).matrix_world.translation).length
        measured[frame] = 2.0 * distance * ax.KM_PER_BLENDER_UNIT * (cam.data.sensor_width / (2.0 * cam.data.lens))

    derived = sp.derive_presentation(config, args.scene, measured)
    print(json.dumps({k: v for k, v in derived.items() if not k.endswith("_keyframes")}, indent=2))
    print("[hero] morph keys: " + str(len(derived["morph_keyframes"])) + ", "
          + str(derived["morph_keyframes"][:3]) + " ... " + str(derived["morph_keyframes"][-3:]))
    if args.dry_run:
        return
    aoi["presentation"]["derived"] = derived
    if "border_glow" in aoi:
        aoi["border_glow"]["width_km"] = derived["settled"]["glow_width_km"]
    text = json.dumps(config, indent=2, ensure_ascii=False) + "\n"
    newline = "\r\n" if "\r\n" in raw else "\n"
    hc.SCENE_CONFIG.write_bytes(text.replace("\n", newline).encode("utf-8"))
    print("[hero] presentation -> " + hc.relpath(hc.SCENE_CONFIG))


if __name__ == "__main__":
    main()
