"""Render the analytical drape states as lossless, colour-faithful overlays.

    blender -b -P hero/scripts/render_drape_states.py -- --scene hero_r3_preview_gate \
        --profile preview_gate --coverage --out hero/renders/preview_r3gate3/drape

Product decision docs/web-005-polish-authority@c7c6cb1 sections 3-4: the hero video carries the
motion and settles on one held geometry; Terrain, THM-01, ALT-01 and priority are delivered as
losslessly encoded rendered drape states aligned to that geometry and cross-faded by the page, so
no governed thematic pixel is ever inside a lossy encode -- and scene light and the AgX view
transform may not re-author thematic colour on the way.

So each state is rendered on its own, from the same scene build and the same held camera:

* only the relief is visible; the crisp lines that stand in front of it (true outline, reticle
  brackets) are holdouts, so the overlay has the right holes;
* the film is transparent and the file is RGBA PNG (lossless);
* the view transform is ``Standard`` with no look, exposure 0, gamma 1. THM-01, ALT-01 and
  priority are fully emissive in the relief material, so a texel's display colour reaches the PNG
  as delivered (up to texture filtering); only Terrain, which is context, takes scene light.

``--frame-lines`` is the production form. The preview gates let the held frame show through those
holes, but in delivery the held video frame carries the outline *flat on the ground*, while the
state needs it *draped on the rim of the relief*. So the lines are rendered once more on their own
-- the relief's data surface as the holdout this time, through the scene's own view transform so they
keep exactly the look they have in the motion video -- and laid over every state. The glass sides of
the raised block go with the lines, not with the data: they are effects, and a saturated emitter
clips to neon under a Standard view. The two passes never share a pixel's colour: a thematic pixel
is Standard-exact or it is covered by an effect.

``--coverage`` adds one more pass per analytical state: the material's own per-pixel analytical
coverage (the delivered alpha, as the surface uses it) written as a linear grey image through the
``Raw`` view. Where it is below 1 the Terrain context shows through (Product decision b9579ef
section 3); the pass is what lets the governed mask be measured in screen space instead of assumed.

Nothing here is site media. The preview gate uses it to show the delivery concept and to measure
the colour path; the production states are rendered the same way at the production profile.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bpy  # noqa: E402

import build_scene  # noqa: E402
import hero_common as hc  # noqa: E402
import render_core  # noqa: E402


def state_frames(spec: dict) -> dict:
    """Frame at which each layer stands alone at full weight (the last such frame for priority)."""
    relief = next(o for o in spec["objects"] if o.get("type") == "aoi_relief")
    rise_done = max(int(f) for f, _ in relief["rise_keyframes"])
    frames = {}
    for layer_id, keys in relief["layer_keyframes"].items():
        full = [int(f) for f, w in keys if float(w) >= 1.0]
        frames[layer_id] = max(max(full), rise_done) if layer_id == "priority" else max(min(full), rise_done)
    return frames


def _render_coverage(scene, relief, out_dir: Path, layer_id: str, frame: int) -> Path:
    """The relief again, shaded by nothing but the material's ``analytical_coverage`` value."""
    material = relief.data.materials[0]
    tree = material.node_tree
    output = next(n for n in tree.nodes if n.type == "OUTPUT_MATERIAL")
    surface = output.inputs["Surface"].links[0].from_socket
    probe = tree.nodes.new("ShaderNodeEmission")
    tree.links.new(tree.nodes["analytical_coverage"].outputs[0], probe.inputs["Color"])
    tree.links.new(probe.outputs["Emission"], output.inputs["Surface"])
    view = scene.view_settings.view_transform
    scene.view_settings.view_transform = "Raw"
    path = out_dir / ("coverage_" + layer_id + "_f" + str(frame) + ".png")
    scene.render.filepath = str(path.with_suffix(""))
    try:
        bpy.ops.render.render(write_still=True)
    finally:
        scene.view_settings.view_transform = view
        tree.links.new(surface, output.inputs["Surface"])
        tree.nodes.remove(probe)
    return path


def _render_frame_lines(scene, relief, lines, wall_material, view_transform, out_dir: Path, frame: int) -> Path:
    """Outline, halo and brackets alone, draped, with the relief as their holdout, in the video's own look."""
    for obj in lines:
        obj.is_holdout = False
        obj.hide_render = False
    data_material = relief.data.materials[0]
    relief.data.materials[0] = _holdout_material()
    if wall_material is not None:
        relief.data.materials[1] = wall_material
    previous = scene.view_settings.view_transform
    scene.view_settings.view_transform = view_transform
    scene.frame_set(frame)
    path = out_dir / ("frame_lines_f" + str(frame) + ".png")
    scene.render.filepath = str(path.with_suffix(""))
    try:
        bpy.ops.render.render(write_still=True)
    finally:
        scene.view_settings.view_transform = previous
        relief.data.materials[0] = data_material
    return path


def _render_ground_shadow(scene, relief, catcher, out_dir: Path, frame: int) -> Path:
    """The block's contact shadow on the ground, alone: black with the shadow's density as alpha.

    The motion render ends before the block exists, so its held frame carries no shadow for it; a state
    rendered on transparent film carries none either, and the block would sit on the page like a sticker.
    The ground is a shadow catcher here and the block casts onto it without being seen itself, so the pass
    holds the shadow and nothing else. It goes UNDER the state: no data pixel is touched.
    """
    catcher.hide_render = False
    catcher.is_shadow_catcher = True
    relief.visible_camera = False
    scene.frame_set(frame)
    path = out_dir / ("ground_shadow_f" + str(frame) + ".png")
    scene.render.filepath = str(path.with_suffix(""))
    try:
        bpy.ops.render.render(write_still=True)
    finally:
        relief.visible_camera = True
        catcher.is_shadow_catcher = False
        catcher.hide_render = True
    return path


def _holdout_material():
    material = bpy.data.materials.get("drape_holdout")
    if material is None:
        material = bpy.data.materials.new("drape_holdout")
        material.use_nodes = True
        nodes, links = material.node_tree.nodes, material.node_tree.links
        nodes.clear()
        output = nodes.new("ShaderNodeOutputMaterial")
        links.new(nodes.new("ShaderNodeHoldout").outputs[0], output.inputs["Surface"])
    return material


def _composite_over(state_path: Path, lines_path: Path, state_on_top: bool = False) -> None:
    """Straight-alpha "over" of a pass and a state, on the stored 8-bit values, written to the state.

    Done on the files' own bytes rather than through the compositor so that a state pixel the other
    pass does not touch is written back bit for bit. ``state_on_top`` puts the state over the pass
    (the ground shadow); otherwise the pass goes over the state (outline, halo, brackets, glass).
    """
    import numpy as np

    def load(path):
        image = bpy.data.images.load(str(path), check_existing=False)
        image.colorspace_settings.name = "Non-Color"  # the stored values, not a linearised copy
        image.alpha_mode = "STRAIGHT"
        width, height = image.size
        pixels = np.empty(width * height * 4, dtype=np.float32)
        image.pixels.foreach_get(pixels)
        bpy.data.images.remove(image)
        return pixels.reshape(height, width, 4), width, height

    under, width, height = load(state_path)
    over, _, _ = load(lines_path)
    if state_on_top:
        under, over = over, under
    a_over, a_under = over[..., 3:4], under[..., 3:4]
    alpha = a_over + a_under * (1.0 - a_over)
    safe = np.where(alpha > 0.0, alpha, 1.0)
    colour = (over[..., :3] * a_over + under[..., :3] * a_under * (1.0 - a_over)) / safe
    result = np.concatenate([colour, alpha], axis=-1)
    untouched = a_over[..., 0] <= 0.0
    result[untouched] = under[untouched]
    covered = a_over[..., 0] >= 1.0
    result[covered] = over[covered]

    image = bpy.data.images.new(state_path.stem, width=width, height=height, alpha=True, float_buffer=False)
    image.colorspace_settings.name = "Non-Color"
    image.alpha_mode = "STRAIGHT"
    image.pixels.foreach_set(result.astype(np.float32).ravel())
    image.filepath_raw = str(state_path)
    image.file_format = "PNG"
    image.save()
    bpy.data.images.remove(image)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render lossless colour-faithful drape states.")
    parser.add_argument("--scene", default="hero_r3_preview_gate")
    parser.add_argument("--profile", default="preview_gate")
    parser.add_argument("--out", required=True)
    parser.add_argument("--coverage", action="store_true", help="also render each state's analytical coverage")
    parser.add_argument("--frame-lines", action="store_true",
                        help="composite the draped outline, halo and brackets over every state (production delivery)")
    parser.add_argument("--ground-shadow", action="store_true",
                        help="composite the block's contact shadow on the ground under every state (production delivery)")
    args = parser.parse_args(hc.argv_after_double_dash())

    scene_config = hc.load_scene_config()
    spec = build_scene.build(args.scene, scene_config)
    applied = render_core.apply_profile(args.profile, hc.load_render_config())
    scene = bpy.context.scene

    relief = bpy.data.objects["aoi_relief"]
    scene_view = scene.view_settings.view_transform
    lines = []
    for obj in scene.objects:
        if obj == relief or obj.type in ("CAMERA", "LIGHT", "EMPTY"):
            continue
        if obj.name in ("aoi_border", "aoi_border_glow") or obj.name.startswith("aoi_lock_"):
            lines.append(obj)
            # The crisp lines cut the overlay; the soft halo does not (a holdout ignores its alpha
            # and would punch its whole width out of the rim).
            if obj.name == "aoi_border_glow":
                obj.hide_render = True
            else:
                obj.is_holdout = True
        else:
            obj.hide_render = True

    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "8"
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = 0.0
    scene.view_settings.gamma = 1.0
    scene.render.use_motion_blur = False
    if not applied.get("denoise"):
        # Fixed sample count for a no-denoise profile: adaptive sampling stops early on flat emissive colour
        # and leaves the texture minification under-sampled exactly where the thematic detail is.
        scene.cycles.use_adaptive_sampling = False
    if scene.use_nodes and scene.node_tree:
        # The bloom belongs to the cinematic frame; on a data overlay it would smear colour.
        scene.use_nodes = False

    out_dir = Path(args.out)
    if not out_dir.is_absolute():
        out_dir = hc.REPO_ROOT / out_dir
    hc.ensure_dir(out_dir)

    wall_material = relief.data.materials[1] if len(relief.data.materials) > 1 else None
    if args.frame_lines and wall_material is not None:
        relief.data.materials[1] = _holdout_material()

    states = []
    for layer_id, frame in state_frames(spec).items():
        scene.frame_set(frame)
        path = out_dir / ("drape_" + layer_id + "_f" + str(frame) + ".png")
        scene.render.filepath = str(path.with_suffix(""))
        bpy.ops.render.render(write_still=True)
        state = {"layer": layer_id, "frame": frame, "output_path": hc.relpath(path),
                 "output_bytes": path.stat().st_size, "sha256": hc.sha256_file(path)}
        if args.coverage and layer_id != "terrain":
            state["coverage_path"] = hc.relpath(_render_coverage(scene, relief, out_dir, layer_id, frame))
        states.append(state)

    shadow_record = None
    if args.ground_shadow:
        # Before the line pass, so the lines end up over the state and the state over the shadow.
        shadow_path = _render_ground_shadow(scene, relief, bpy.data.objects["earth"], out_dir,
                                            max(s["frame"] for s in states))
        for state in states:
            path = hc.REPO_ROOT / state["output_path"]
            _composite_over(path, shadow_path, state_on_top=True)
            state.update({"output_bytes": path.stat().st_size, "sha256": hc.sha256_file(path)})
        shadow_record = {"output_path": hc.relpath(shadow_path), "sha256": hc.sha256_file(shadow_path),
                         "method": "ground as shadow catcher, block invisible to the camera, transparent film",
                         "composited_under": [s["layer"] for s in states]}

    lines_record = None
    if args.frame_lines:
        lines_path = _render_frame_lines(scene, relief, lines, wall_material, scene_view, out_dir,
                                         max(s["frame"] for s in states))
        for state in states:
            path = hc.REPO_ROOT / state["output_path"]
            _composite_over(path, lines_path)
            state.update({"output_bytes": path.stat().st_size, "sha256": hc.sha256_file(path)})
        lines_record = {"output_path": hc.relpath(lines_path), "sha256": hc.sha256_file(lines_path),
                        "view_transform": scene_view, "composited_over": [s["layer"] for s in states]}

    record = {
        "scene": args.scene,
        "profile": args.profile,
        "resolution": applied.get("resolution"),
        "view_transform": "Standard",
        "film_transparent": True,
        "encoding": "PNG RGBA 8-bit (lossless)",
        "holdouts": "relief pass: true outline, reticle brackets and the block's glass sides; effects pass: the data surface",
        "frame_lines": lines_record,
        "ground_shadow": shadow_record,
        "samples": applied.get("samples"),
        "denoise": applied.get("denoise"),
        "states": states,
    }
    (out_dir / "drape_record.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
