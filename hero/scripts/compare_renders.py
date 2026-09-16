"""Compare two rendered images pixel-wise, inside Blender.

    blender -b -P hero/scripts/compare_renders.py -- --pair label a.png b.png [...]

Why this exists: the Cycles + OptiX-denoise path on GPU is not bit-reproducible.
Two renders of the *same* scene, from the same commit, on the same machine,
produce different file hashes. So "did this change alter an earlier phase's
render?" cannot be answered with a checksum -- a checksum says "different"
either way.

The answer is to measure. Render the earlier phase again, compare it with the
committed still, and compare that difference against the renderer's own noise
floor (two consecutive renders of one unchanged scene). If the two differences
are the same size, the earlier phase still renders as it did; if the rebuild
differs by materially more, something real changed.

Uses Blender's own image loader, so it adds no Python dependency to the lane.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bpy  # noqa: E402

import hero_common as hc  # noqa: E402


def _load(path: Path):
    image = bpy.data.images.load(str(path))
    try:
        return list(image.pixels), (image.size[0], image.size[1])
    finally:
        bpy.data.images.remove(image)


def compare(a_path: Path, b_path: Path) -> dict:
    """Difference between two images, in 8-bit channel levels, ignoring alpha."""
    a, size_a = _load(a_path)
    b, size_b = _load(b_path)
    if size_a != size_b:
        return {"error": "size mismatch " + str(size_a) + " vs " + str(size_b)}

    worst = 0.0
    total = 0.0
    differing = 0
    counted = 0
    for index in range(len(a)):
        if index % 4 == 3:
            continue
        delta = abs(a[index] - b[index])
        counted += 1
        total += delta
        if delta > worst:
            worst = delta
        if delta > 1.0 / 255.0:
            differing += 1

    return {
        "a": hc.relpath(a_path),
        "b": hc.relpath(b_path),
        "resolution": list(size_a),
        "max_channel_delta_8bit": round(worst * 255.0, 4),
        "mean_channel_delta_8bit": round(total / counted * 255.0, 6),
        "channels_differing_by_more_than_one_level": differing,
        "channels_compared": counted,
        "percent_channels_differing": round(100.0 * differing / counted, 5),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare rendered images.")
    parser.add_argument(
        "--pair",
        nargs=3,
        action="append",
        metavar=("LABEL", "A", "B"),
        required=True,
        help="a labelled pair of images to compare; repeatable",
    )
    parser.add_argument("--out", default=None, help="write the comparison record as JSON")
    parser.add_argument(
        "--note",
        default=None,
        help="interpretation recorded alongside the comparisons, so the record explains itself",
    )
    args = parser.parse_args(hc.argv_after_double_dash())

    comparisons = {label: compare(Path(a), Path(b)) for label, a, b in args.pair}
    record = {"comparisons": comparisons}
    if args.note:
        record["note"] = args.note
    print(json.dumps(record, indent=2))

    if args.out:
        out = Path(args.out)
        hc.ensure_dir(out.parent)
        out.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        print("[hero] comparison -> " + hc.relpath(out))


if __name__ == "__main__":
    main()
