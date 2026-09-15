"""Bounded high-quality still / evidence render entrypoint.

    blender -b -P hero/scripts/render_still.py -- --scene benchmark_neutral --evidence

Without --evidence the still lands in the ignored hero/renders/still/ directory.
With --evidence it is written to hero/evidence/, which is deliberately small and
reviewable: publish a still here only when a task asks for bounded evidence, and
never a render sequence.
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
    default_profile = render_config.get("default_still_profile", "master")

    parser = argparse.ArgumentParser(description="Render a high-quality still.")
    parser.add_argument("--scene", default="benchmark_neutral")
    parser.add_argument("--profile", default=default_profile)
    parser.add_argument("--out", default=None)
    parser.add_argument(
        "--evidence",
        action="store_true",
        help="write into hero/evidence/ as a bounded, committed review artifact",
    )
    parser.add_argument("--record", default=None, help="write the render record as JSON")
    args = parser.parse_args(hc.argv_after_double_dash())

    if args.out:
        out = Path(args.out)
    elif args.evidence:
        out = hc.EVIDENCE_DIR / (args.scene + "_" + args.profile + ".png")
    else:
        out = hc.RENDERS_DIR / "still" / (args.scene + "_" + args.profile + ".png")

    record = render_core.render_still(args.scene, args.profile, out)
    print(json.dumps(record, indent=2))

    if args.record:
        record_path = Path(args.record)
        hc.ensure_dir(record_path.parent)
        record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        print("[hero] record -> " + hc.relpath(record_path))


if __name__ == "__main__":
    main()
