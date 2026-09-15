"""Fast-iteration preview render entrypoint.

    blender -b -P hero/scripts/render_preview.py -- --scene benchmark_neutral

Output defaults to hero/renders/preview/<scene>.png, which is ignored by Git.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import hero_common as hc  # noqa: E402
import render_core  # noqa: E402


def main() -> None:
    render_config = hc.load_render_config()
    default_profile = render_config.get("default_preview_profile", "preview")

    parser = argparse.ArgumentParser(description="Render a fast preview still.")
    parser.add_argument("--scene", default="benchmark_neutral")
    parser.add_argument("--profile", default=default_profile)
    parser.add_argument("--out", default=None)
    parser.add_argument("--record", default=None, help="write the render record as JSON")
    args = parser.parse_args(hc.argv_after_double_dash())

    out = Path(args.out) if args.out else hc.RENDERS_DIR / "preview" / (args.scene + ".png")
    record = render_core.render_still(args.scene, args.profile, out)
    print(json.dumps(record, indent=2))

    if args.record:
        record_path = Path(args.record)
        hc.ensure_dir(record_path.parent)
        record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        print("[hero] record -> " + hc.relpath(record_path))


if __name__ == "__main__":
    main()
