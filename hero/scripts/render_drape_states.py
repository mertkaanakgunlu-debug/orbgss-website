"""Render the analytical drape states as lossless, colour-faithful overlays.

    blender -b -P hero/scripts/render_drape_states.py -- --scene hero_r3_preview_gate \
        --profile preview_gate --out hero/renders/preview_r3gate2/drape

Product decision docs/web-005-polish-authority@c7c6cb1 sections 3-4: the hero video carries the
motion and settles on one held geometry; Terrain, THM-01, ALT-01 and priority are delivered as
losslessly encoded rendered drape states aligned to that geometry and cross-faded by the page, so
no governed thematic pixel is ever inside a lossy encode -- and scene light and the AgX view
transform may not re-author thematic colour on the way.

So each state is rendered on its own, from the same scene build and the same held camera:

* only the relief is visible; the crisp lines that stand in front of it (true outline, reticle
  brackets) are holdouts, so the overlay has the right holes and the held frame shows through;
* the film is transparent and the file is RGBA PNG (lossless);
* the view transform is ``Standard`` with no look, exposure 0, gamma 1. THM-01, ALT-01 and
  priority are fully emissive in the relief material, so a texel's display colour reaches the PNG
  as delivered (up to texture filtering); only Terrain, which is context, takes scene light.

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


def main() -> None:
    parser = argparse.ArgumentParser(description="Render lossless colour-faithful drape states.")
    parser.add_argument("--scene", default="hero_r3_preview_gate")
    parser.add_argument("--profile", default="preview_gate")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(hc.argv_after_double_dash())

    scene_config = hc.load_scene_config()
    spec = build_scene.build(args.scene, scene_config)
    applied = render_core.apply_profile(args.profile, hc.load_render_config())
    scene = bpy.context.scene

    relief = bpy.data.objects["aoi_relief"]
    for obj in scene.objects:
        if obj == relief or obj.type in ("CAMERA", "LIGHT", "EMPTY"):
            continue
        if obj.name == "aoi_border" or obj.name.startswith("aoi_lock_"):
            # The crisp lines cut the overlay; the soft halo does not (a holdout ignores its alpha
            # and would punch its whole width out of the rim).
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
    if scene.use_nodes and scene.node_tree:
        # The bloom belongs to the cinematic frame; on a data overlay it would smear colour.
        scene.use_nodes = False

    out_dir = Path(args.out)
    if not out_dir.is_absolute():
        out_dir = hc.REPO_ROOT / out_dir
    hc.ensure_dir(out_dir)

    states = []
    for layer_id, frame in state_frames(spec).items():
        scene.frame_set(frame)
        path = out_dir / ("drape_" + layer_id + "_f" + str(frame) + ".png")
        scene.render.filepath = str(path.with_suffix(""))
        bpy.ops.render.render(write_still=True)
        states.append({"layer": layer_id, "frame": frame, "output_path": hc.relpath(path),
                       "output_bytes": path.stat().st_size, "sha256": hc.sha256_file(path)})

    record = {
        "scene": args.scene,
        "profile": args.profile,
        "resolution": applied.get("resolution"),
        "view_transform": "Standard",
        "film_transparent": True,
        "encoding": "PNG RGBA 8-bit (lossless)",
        "holdouts": "true outline and reticle brackets (the soft halo is omitted from the overlay pass)",
        "states": states,
    }
    (out_dir / "drape_record.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
