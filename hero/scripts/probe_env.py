"""Record the production environment Blender actually exposes on this machine.

    blender -b -P hero/scripts/probe_env.py -- --out hero/evidence/environment.json

Reports the Blender build, the Python it embeds, every Cycles compute backend
and device visible, and which engine identifiers exist for the logical engine
names used by the render profiles. This is evidence, not configuration: it is
regenerated per machine and is expected to differ between operators.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bpy  # noqa: E402

import hero_common as hc  # noqa: E402
import render_core  # noqa: E402


def probe() -> dict:
    render_config = hc.load_render_config()

    engines = {}
    for logical in render_config.get("engine_aliases", {}):
        try:
            engines[logical] = render_core.resolve_engine(logical, render_config)
        except render_core.RenderProfileError as error:
            engines[logical] = "UNAVAILABLE: " + str(error)

    inventory = render_core.device_inventory()
    selection = render_core.select_cycles_device(render_config, prefer_gpu=True)

    return {
        "blender": {
            "version": bpy.app.version_string,
            "build_hash": bpy.app.build_hash.decode()
            if isinstance(bpy.app.build_hash, bytes)
            else str(bpy.app.build_hash),
            "build_date": bpy.app.build_date.decode()
            if isinstance(bpy.app.build_date, bytes)
            else str(bpy.app.build_date),
            "binary_path": bpy.app.binary_path,
        },
        "python": {
            "version": sys.version.split()[0],
            "full_version": sys.version.replace("\n", " "),
        },
        "host": {
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "engines_resolved": engines,
        "cycles_device_inventory": inventory,
        "cycles_device_selection": selection,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe the Blender production environment.")
    parser.add_argument("--out", default=str(hc.EVIDENCE_DIR / "environment.json"))
    args = parser.parse_args(hc.argv_after_double_dash())

    report = probe()
    print(json.dumps(report, indent=2))

    out = Path(args.out)
    hc.ensure_dir(out.parent)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("[hero] environment -> " + hc.relpath(out))


if __name__ == "__main__":
    main()
