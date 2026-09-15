"""Run the full production benchmark in one Blender session.

    blender -b -P hero/scripts/run_benchmark.py -- --scene benchmark_neutral

Renders every profile listed under ``benchmark_profiles`` in the render
configuration, routes each output by its own ``publish_evidence`` flag, and
writes a consolidated record to hero/evidence/benchmark.json.

The benchmark measures this machine's pipeline throughput for production
planning. It is not a quality target and not an art-direction reference.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import hero_common as hc  # noqa: E402
import probe_env  # noqa: E402
import render_core  # noqa: E402


def destination(scene_id: str, profile_name: str, profile: dict) -> Path:
    stem = scene_id + "_" + profile_name + ".png"
    if profile.get("publish_evidence"):
        return hc.EVIDENCE_DIR / stem
    return hc.RENDERS_DIR / "benchmark" / stem


def main() -> None:
    render_config = hc.load_render_config()
    profiles = render_config.get("profiles", {})
    default_order = render_config.get("benchmark_profiles", sorted(profiles))

    parser = argparse.ArgumentParser(description="Benchmark the hero render pipeline.")
    parser.add_argument("--scene", default="benchmark_neutral")
    parser.add_argument("--profiles", nargs="*", default=default_order)
    parser.add_argument("--out", default=str(hc.EVIDENCE_DIR / "benchmark.json"))
    args = parser.parse_args(hc.argv_after_double_dash())

    runs = []
    for profile_name in args.profiles:
        if profile_name not in profiles:
            raise SystemExit("unknown render profile: " + profile_name)
        out = destination(args.scene, profile_name, profiles[profile_name])
        print("\n[hero] benchmarking profile " + profile_name + " -> " + hc.relpath(out))
        runs.append(render_core.render_still(args.scene, profile_name, out))

    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "phase": hc.load_lane_config().get("phase"),
        "scene": args.scene,
        "purpose": (
            "Production planning benchmark for the hero pipeline on this machine. "
            "Not a quality target; supersede it whenever the scene or hardware changes."
        ),
        "environment": probe_env.probe(),
        "runs": runs,
    }

    out = Path(args.out)
    hc.ensure_dir(out.parent)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print("\n[hero] benchmark summary")
    for run in runs:
        device = run.get("device") or {}
        print(
            "  {profile:<15} {engine:<20} {w}x{h} {samples:>5} spp  "
            "{secs:>8.2f}s  {backend:<18} {bytes:>10} B".format(
                profile=run["profile"],
                engine=run["engine"],
                w=run["resolution"][0],
                h=run["resolution"][1],
                samples=run["samples"],
                secs=run["wall_clock_seconds"],
                backend=str(device.get("backend")),
                bytes=run["output_bytes"],
            )
        )
    print("[hero] benchmark -> " + hc.relpath(out))


if __name__ == "__main__":
    main()
