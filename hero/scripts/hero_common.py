"""Shared, Blender-independent helpers for the OrbGSS hero production workspace.

This module must stay importable by a plain CPython interpreter so the validator
can run without Blender. Nothing here may import ``bpy``.
"""

from __future__ import annotations

import copy
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


def _merge_by_id(base_list, child_list):
    """Merge two lists of ``{"id": ...}`` specs: same id deep-merges, new ids append.

    This is what lets a derived scene adjust one object -- extend the Earth's
    rotation, extend the satellite's path -- without restating the objects it
    leaves alone, and without the base scene's definition drifting out of sync
    with the shot that inherits it.
    """
    merged = [dict(item) for item in base_list]
    index_of = {item.get("id"): position for position, item in enumerate(merged) if item.get("id")}
    for item in child_list:
        item_id = item.get("id")
        if item_id and item_id in index_of:
            merged[index_of[item_id]] = _merge_spec(merged[index_of[item_id]], item)
        else:
            merged.append(copy.deepcopy(item))
    return merged


def _merge_spec(base, child):
    """Deep-merge two scene fragments. Dicts merge; every other value replaces.

    Lists replace wholesale on purpose: a camera path or a keyframe track is a
    single authored unit, and silently interleaving two of them would produce a
    move nobody wrote.
    """
    merged = copy.deepcopy(base)
    for key, value in child.items():
        if key == "extends":
            continue
        if key in ("objects", "lights") and isinstance(value, list):
            merged[key] = _merge_by_id(merged.get(key, []), value)
        elif isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge_spec(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def resolve_scene_spec(scene_id: str, scenes: dict, _seen=None) -> dict:
    """Resolve a scene definition, following any ``extends`` chain.

    WEB-HERO-001C inherits the accepted WEB-HERO-001B scene rather than copying
    it, so the established Earth/satellite/camera system has exactly one
    definition and the acquisition shot cannot quietly diverge from the
    establish it continues.
    """
    if scene_id not in scenes:
        raise KeyError(
            "scene " + repr(scene_id) + " is not defined in "
            + hc.relpath(hc.SCENE_CONFIG)
            + "; available: " + repr(sorted(scenes))
        )
    _seen = _seen or []
    if scene_id in _seen:
        raise ValueError(
            "scene inheritance cycle: " + " -> ".join(_seen + [scene_id])
        )

    spec = scenes[scene_id]
    parent_id = spec.get("extends")
    if not parent_id:
        return copy.deepcopy(spec)
    parent = resolve_scene_spec(parent_id, scenes, _seen + [scene_id])
    return _merge_spec(parent, spec)

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
