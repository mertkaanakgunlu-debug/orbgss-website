"""Package the rendered analytical drape states for the page: copy, verify, checksum. No processing.

    py -3.14 hero/scripts/package_drape_states.py

``render_drape_states.py --frame-lines`` writes the four production states (Terrain, THM-01, ALT-01,
priority) as lossless full-frame RGBA PNGs. This copies them byte for byte to ``assets/hero/drape``
under their delivery names and writes the evidence record the site manifest is filled from: for
every state its delivered checksum, the frame and render settings it came from, and the checksum of
the prepared 4K display texture it was draped with, taken from the ingest record rather than
re-read, so a texture that changed since ingest shows up as a mismatch instead of being absorbed.

Plain Python on purpose: nothing here touches a pixel. A state is refused if it is not an 8-bit
RGBA PNG at the delivered frame size, because anything else means it did not come from the
production profile.
"""

from __future__ import annotations

import argparse
import json
import shutil
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import hero_common as hc  # noqa: E402

LAYER_ORDER = ("terrain", "thm01", "alt01", "priority")
DELIVERED_SIZE = (1920, 1080)


def png_header(path: Path):
    """(width, height, bit depth, colour type) from the IHDR chunk."""
    with path.open("rb") as handle:
        head = handle.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        raise SystemExit(hc.relpath(path) + " is not a PNG")
    width, height, depth, colour = struct.unpack(">IIBB", head[16:26])
    return width, height, depth, colour


def main() -> int:
    parser = argparse.ArgumentParser(description="Package the production drape states for the page.")
    parser.add_argument("--record", default="hero/renders/production/drape/drape_record.json")
    parser.add_argument("--out-dir", default="assets/hero/drape")
    parser.add_argument("--evidence", default="hero/evidence/production_drape_states.json")
    args = parser.parse_args()

    record = hc.load_json(hc.REPO_ROOT / args.record)
    if (not record.get("frame_lines") or not record.get("ground_shadow") or record.get("denoise")
            or record.get("view_transform") != "Standard"):
        raise SystemExit("drape record is not a production run (needs --frame-lines and --ground-shadow, no denoiser, "
                         "Standard view)")
    states = {state["layer"]: state for state in record["states"]}
    if tuple(states) != LAYER_ORDER:
        raise SystemExit("drape record lists " + repr(tuple(states)) + ", expected " + repr(LAYER_ORDER))

    scene_config = hc.load_scene_config()
    spec = hc.resolve_scene_spec(record["scene"], scene_config["scenes"])
    material = spec["materials"]["aoi_relief_layers"]
    relief = next(o for o in spec["objects"] if o.get("type") == "aoi_relief")
    ingest = hc.load_json(hc.EVIDENCE_DIR / "web005a_r3_preview" / "analytical_asset_ingest.json")
    ingested = {entry["materialized"]: entry for entry in ingest["files"]}

    out_dir = hc.ensure_dir(hc.REPO_ROOT / args.out_dir)
    delivered = []
    for layer_id in LAYER_ORDER:
        state = states[layer_id]
        source = hc.REPO_ROOT / state["output_path"]
        if hc.sha256_file(source) != state["sha256"]:
            raise SystemExit(state["output_path"] + " no longer matches its render record")
        width, height, depth, colour = png_header(source)
        if (width, height) != DELIVERED_SIZE or depth != 8 or colour != 6:
            raise SystemExit(state["output_path"] + " is not an 8-bit RGBA PNG at " + repr(DELIVERED_SIZE))
        texture = material["layers"][layer_id]["texture"]
        texture_path = hc.SOURCE_DIR / texture
        if texture_path.is_file() and hc.sha256_file(texture_path) != ingested[texture]["sha256"]:
            raise SystemExit(texture + " differs from its ingest checksum")
        target = out_dir / ("hero-drape-" + layer_id + "-" + str(width) + ".png")
        shutil.copyfile(source, target)
        delivered.append({
            "layer": layer_id,
            "path": hc.relpath(target),
            "bytes": target.stat().st_size,
            "sha256": hc.sha256_file(target),
            "width": width,
            "height": height,
            "encoding": "PNG, 8-bit RGBA, lossless",
            "rendered_frame": state["frame"],
            "display_texture": texture,
            "display_texture_sha256": ingested[texture]["sha256"],
            "display_texture_size": [4096, 4096],
            "lit": float(material["layers"][layer_id].get("emission_mix", 0.0)) < 1.0,
        })

    evidence = {
        "task": "WEB-005A / MER-107 final production",
        "scene": record["scene"],
        "profile": record["profile"],
        "samples": record["samples"],
        "denoise": record["denoise"],
        "view_transform": record["view_transform"],
        "frame_lines": record["frame_lines"],
        "ground_shadow": record["ground_shadow"],
        "holdouts": record["holdouts"],
        "relief_geometry": {
            "dem": relief["dem"],
            "dem_sha256": ingested[relief["dem"]]["sha256"],
            "grid": relief["grid"],
            "vertical_exaggeration": relief["vertical_exaggeration"],
            "fixture": relief["fixture"],
        },
        "masked_support": "underlay_layer = " + str(material.get("underlay_layer")) + ": where a layer's own alpha is below 1 "
                          "the Terrain context shows through, lit as context; the alpha is used as delivered",
        "source_package": {key: ingest.get(key) for key in ("export_id", "project_id", "config_hash")},
        "ingest_record": hc.relpath(hc.EVIDENCE_DIR / "web005a_r3_preview" / "analytical_asset_ingest.json"),
        "states": delivered,
        "total_bytes": sum(item["bytes"] for item in delivered),
    }
    out = hc.REPO_ROOT / args.evidence
    out.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for item in delivered:
        print("[drape] " + item["path"] + "  " + str(item["bytes"]) + " bytes  " + item["sha256"][:16] + "  <- "
              + item["display_texture"])
    print("[drape] record -> " + hc.relpath(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
