"""Shared, Blender-independent helpers for the OrbGSS hero production workspace.

This module must stay importable by a plain CPython interpreter so the validator
can run without Blender. Nothing here may import ``bpy``.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERO_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = HERO_ROOT.parent

CONFIG_DIR = HERO_ROOT / "config"
ASSETS_DIR = HERO_ROOT / "assets"
SOURCE_DIR = ASSETS_DIR / "source"
BLEND_DIR = HERO_ROOT / "blender"
RENDERS_DIR = HERO_ROOT / "renders"
EVIDENCE_DIR = HERO_ROOT / "evidence"

SCENE_CONFIG = CONFIG_DIR / "scene.json"
RENDER_CONFIG = CONFIG_DIR / "render_profiles.json"
LANE_CONFIG = CONFIG_DIR / "lane.json"
ASSET_MANIFEST = ASSETS_DIR / "manifest.json"

# Directories whose contents are generated and must never be treated as source
# authority. Each needs a local ignore policy that keeps the directory present
# but its payload untracked.
GENERATED_DIRS = (RENDERS_DIR, SOURCE_DIR)


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def load_scene_config() -> dict:
    return load_json(SCENE_CONFIG)


def load_render_config() -> dict:
    return load_json(RENDER_CONFIG)


def load_lane_config() -> dict:
    return load_json(LANE_CONFIG)


def load_asset_manifest() -> dict:
    return load_json(ASSET_MANIFEST)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def palette_color(scene_config: dict, ref: str) -> list:
    """Resolve a palette reference to a linear RGB triplet."""
    palette = scene_config.get("palette", {})
    if ref not in palette:
        raise KeyError(f"palette reference '{ref}' is not defined in scene.json")
    return list(palette[ref])


def argv_after_double_dash(argv=None) -> list:
    """Return the arguments Blender passes through after ``--``."""
    argv = list(sys.argv if argv is None else argv)
    if "--" in argv:
        return argv[argv.index("--") + 1:]
    return []


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def relpath(path: Path) -> str:
    """Repository-relative POSIX path, for stable evidence records."""
    try:
        return Path(path).resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return Path(path).as_posix()
