"""Ingest the pinned Kizildere analytical handoff into the hero workspace, by copy and checksum.

    py -3.14 hero/scripts/materialize_analytical_assets.py
    py -3.14 hero/scripts/materialize_analytical_assets.py --verify

Authority: docs/web-005-polish-authority@db4605abcb35be9ab0337deb6b15c80aab79b12b:
tasks/WEB-005A_R3_ANALYTICAL_ASSET_HANDOFF.md. That handoff pins two packages on the CTO
workstation and says how each may be used:

* ``top-dem.tif`` from the governed GEO-039 export ``20260917T161155Z-5e7a0e53`` is the ONLY
  geometry authority for the AOI relief. It is copied byte-for-byte and never written to.
* the four ``*_webhero_display_4k.png`` files are presentation-only display textures. They are
  material for the cinematic hero and nothing else: not analysis inputs, not displacement sources,
  and not the governed class-B derivatives the page ships under ``assets/proof/final``.

This script does no image processing at all. It copies, hashes and records, so what the builder
reads is provably what Product pinned. If an expected file is missing, or a materialized copy no
longer matches its recorded checksum, it stops the ingest and says which file -- the handoff's own
STOP rule -- instead of improvising a substitute.

Nothing here is a site runtime dependency, and nothing it copies is committed: hero/assets/source
is ignored, exactly like the Blue Marble and Sentinel-2 sources.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import hero_common as hc  # noqa: E402

AUTHORITY = (
    "docs/web-005-polish-authority@db4605abcb35be9ab0337deb6b15c80aab79b12b:"
    "tasks/WEB-005A_R3_ANALYTICAL_ASSET_HANDOFF.md"
)
SCIENCE_ROOT = Path("C:/Projects/geothermal-prospectivity/outputs")
EXPORT_ID = "20260917T161155Z-5e7a0e53"
EXPORT_DIR = SCIENCE_ROOT / "kizildere_mvp_v2" / "exports" / EXPORT_ID
DISPLAY_DIR = SCIENCE_ROOT / "webhero_display_final"
RECORD = hc.EVIDENCE_DIR / "web005a_r3_preview" / "analytical_asset_ingest.json"

# (source path, materialized name, use)
INGEST = (
    (EXPORT_DIR / "top-dem.tif", "kizildere_top_dem.tif", "relief_geometry_source"),
    (DISPLAY_DIR / "terrain_webhero_display_4k.png", "terrain_webhero_display_4k.png", "display_texture"),
    (DISPLAY_DIR / "thm01_webhero_display_4k.png", "thm01_webhero_display_4k.png", "display_texture"),
    (DISPLAY_DIR / "alt01_webhero_display_4k.png", "alt01_webhero_display_4k.png", "display_texture"),
    (DISPLAY_DIR / "priority_webhero_display_4k.png", "priority_webhero_display_4k.png", "display_texture"),
)
# Read for provenance only; never copied into the workspace.
CONTEXT = (
    EXPORT_DIR / "export_manifest.json",
    DISPLAY_DIR / "webhero_display_final_manifest.json",
)


def ingest(verify_only: bool) -> int:
    hc.ensure_dir(hc.SOURCE_DIR)
    previous = hc.load_json(RECORD) if RECORD.is_file() else {}
    known = {entry["materialized"]: entry for entry in previous.get("files", [])}
    files, problems = [], []

    for source, name, use in INGEST:
        target = hc.SOURCE_DIR / name
        if not source.is_file():
            problems.append("pinned source is missing: " + source.as_posix())
            continue
        source_sha = hc.sha256_file(source)
        recorded = known.get(name, {}).get("sha256")
        if recorded and recorded != source_sha:
            problems.append(
                name + ": pinned source no longer matches the recorded ingest checksum ("
                + source_sha[:12] + " vs " + recorded[:12] + ")"
            )
            continue
        if not verify_only and (not target.is_file() or hc.sha256_file(target) != source_sha):
            shutil.copyfile(source, target)
        if target.is_file() and hc.sha256_file(target) != source_sha:
            problems.append(name + ": materialized copy differs from its pinned source")
            continue
        files.append({
            "materialized": name,
            "use": use,
            "source": source.as_posix(),
            "sha256": source_sha,
            "bytes": source.stat().st_size,
            "present_in_workspace": target.is_file(),
        })

    context = [
        {"path": path.as_posix(), "sha256": hc.sha256_file(path)} for path in CONTEXT if path.is_file()
    ]
    export = hc.load_json(CONTEXT[0]) if CONTEXT[0].is_file() else {}
    record = {
        "authority": AUTHORITY,
        "export_id": export.get("export_id", EXPORT_ID),
        "project_id": export.get("project_id"),
        "grid": export.get("grid"),
        "config_hash": export.get("config_hash"),
        "processing": "none: byte-for-byte copy and SHA-256 only",
        "geometry_authority": "kizildere_top_dem.tif (governed top-dem.tif); never a coloured texture",
        "display_texture_boundary": (
            "presentation-only display derivatives per the handoff; analysis_use_allowed is false in "
            "their own manifest; they are not the governed class-B derivatives the page ships"
        ),
        "files": files,
        "provenance_context": context,
        "problems": problems,
    }
    if not verify_only:
        hc.ensure_dir(RECORD.parent)
        RECORD.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        print("[hero] analytical asset ingest -> " + hc.relpath(RECORD))
    for entry in files:
        print("  " + entry["sha256"][:16] + "  " + entry["materialized"])
    for problem in problems:
        print("  STOP  " + problem)
    return 1 if problems else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Copy and checksum the pinned analytical handoff.")
    parser.add_argument("--verify", action="store_true", help="check only; copy and record nothing")
    args = parser.parse_args()
    return ingest(args.verify)


if __name__ == "__main__":
    raise SystemExit(main())
