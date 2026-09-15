"""Render-profile application and truthful render-device selection.

Everything the renderer needs comes from ``hero/config/render_profiles.json``.
Device selection walks the configured preference order, falls back to CPU when
no compatible GPU backend is exposed, and reports what actually happened rather
than what was requested.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bpy  # noqa: E402

import hero_common as hc  # noqa: E402
import build_scene  # noqa: E402


KNOWN_BACKENDS = ("OPTIX", "CUDA", "HIP", "ONEAPI", "METAL")


class RenderProfileError(RuntimeError):
    pass


def _can_set(owner, prop_name: str, value: str) -> bool:
    """Probe a Blender enum by assignment.

    ``render.engine``, ``compute_device_type`` and ``cycles.denoiser`` are
    dynamic enums: their real item sets are built at runtime and ``bl_rna``
    reports an empty or partial list. Assignment is the only truthful probe.
    """
    try:
        setattr(owner, prop_name, value)
        return True
    except TypeError:
        return False


def resolve_engine(logical_engine: str, render_config: dict) -> str:
    """Map a logical engine name to an identifier this Blender build exposes."""
    candidates = render_config.get("engine_aliases", {}).get(
        logical_engine, [logical_engine]
    )
    render = bpy.context.scene.render
    previous = render.engine
    for candidate in candidates:
        if _can_set(render, "engine", candidate):
            render.engine = previous
            return candidate
    raise RenderProfileError(
        "no engine identifier for logical engine " + repr(logical_engine)
        + "; tried " + repr(candidates) + " and this Blender build accepted none"
    )


def device_inventory() -> dict:
    """Report every Cycles compute backend and device this build can see."""
    addon = bpy.context.preferences.addons.get("cycles")
    if addon is None:
        return {"cycles_addon": False, "settable_backends": [], "devices": []}

    prefs = addon.preferences
    settable = []
    seen = {}
    for backend in KNOWN_BACKENDS:
        if not _can_set(prefs, "compute_device_type", backend):
            continue
        settable.append(backend)
        prefs.get_devices()
        for device in prefs.devices:
            seen[(device.name, device.type)] = {
                "name": device.name,
                "type": device.type,
            }

    devices = sorted(seen.values(), key=lambda d: (d["type"], d["name"]))
    device_types = {device["type"] for device in devices}

    return {
        "cycles_addon": True,
        # A backend can be selectable while exposing no hardware, so the usable
        # set is the one that actually has a device behind it.
        "settable_backends": settable,
        "backends_with_devices": [b for b in settable if b in device_types],
        "devices": devices,
    }


def select_cycles_device(render_config: dict, prefer_gpu: bool) -> dict:
    """Enable the best available Cycles backend; fall back to CPU gracefully."""
    result = {
        "requested_gpu": bool(prefer_gpu),
        "backend": "NONE",
        "scene_device": "CPU",
        "gpu_active": False,
        "enabled_devices": [],
        "fallback_reason": None,
    }

    addon = bpy.context.preferences.addons.get("cycles")
    if addon is None:
        result["fallback_reason"] = "cycles addon not available in this Blender build"
        bpy.context.scene.cycles.device = "CPU"
        return result

    prefs = addon.preferences

    if not prefer_gpu:
        result["fallback_reason"] = "profile requested CPU rendering"
        bpy.context.scene.cycles.device = "CPU"
        return result

    for backend in render_config.get("device_preference", []):
        if not _can_set(prefs, "compute_device_type", backend):
            continue
        prefs.get_devices()
        matching = [d for d in prefs.devices if d.type == backend]
        if not matching:
            continue
        for device in prefs.devices:
            device.use = device.type == backend
        result["backend"] = backend
        result["scene_device"] = "GPU"
        result["gpu_active"] = True
        result["enabled_devices"] = [d.name for d in matching]
        bpy.context.scene.cycles.device = "GPU"
        return result

    if not render_config.get("allow_cpu_fallback", True):
        raise RenderProfileError(
            "no GPU backend from " + repr(render_config.get("device_preference"))
            + " is available and CPU fallback is disabled"
        )

    result["fallback_reason"] = (
        "no compatible GPU backend exposed by this Blender build/driver; using CPU"
    )
    bpy.context.scene.cycles.device = "CPU"
    result["enabled_devices"] = ["CPU"]
    return result


def _check_aspect(profile_name: str, profile: dict, render_config: dict) -> None:
    aspect = render_config.get("aspect_ratio")
    if not aspect:
        return
    width = profile["resolution_x"] * aspect["height"]
    height = profile["resolution_y"] * aspect["width"]
    if width != height:
        raise RenderProfileError(
            "profile " + profile_name + " resolution "
            + str(profile["resolution_x"]) + "x" + str(profile["resolution_y"])
            + " does not match the configured "
            + str(aspect["width"]) + ":" + str(aspect["height"]) + " aspect ratio"
        )


def apply_profile(profile_name: str, render_config=None) -> dict:
    """Apply a named render profile to the current scene; return what was used."""
    render_config = render_config or hc.load_render_config()
    profiles = render_config.get("profiles", {})
    if profile_name not in profiles:
        raise RenderProfileError(
            "render profile " + repr(profile_name) + " is not defined in "
            + hc.relpath(hc.RENDER_CONFIG)
            + "; available: " + repr(sorted(profiles))
        )

    profile = profiles[profile_name]
    _check_aspect(profile_name, profile, render_config)

    scene = bpy.context.scene
    engine = resolve_engine(profile["engine"], render_config)
    scene.render.engine = engine

    scene.render.resolution_x = int(profile["resolution_x"])
    scene.render.resolution_y = int(profile["resolution_y"])
    scene.render.resolution_percentage = int(profile.get("resolution_percentage", 100))

    image_settings = scene.render.image_settings
    image_settings.file_format = profile.get("file_format", "PNG")
    if image_settings.file_format == "PNG":
        image_settings.color_depth = str(profile.get("color_depth", "8"))
        image_settings.compression = int(profile.get("compression", 15))

    applied = {
        "profile": profile_name,
        "role": profile.get("role"),
        "logical_engine": profile["engine"],
        "engine": engine,
        "resolution": [scene.render.resolution_x, scene.render.resolution_y],
        "resolution_percentage": scene.render.resolution_percentage,
        "samples": int(profile.get("samples", 0)),
        "denoise": bool(profile.get("denoise", False)),
        "denoiser": None,
        "device": None,
    }

    if engine == "CYCLES":
        cycles = scene.cycles
        cycles.samples = int(profile.get("samples", 128))
        if "adaptive_threshold" in profile:
            cycles.use_adaptive_sampling = True
            cycles.adaptive_threshold = float(profile["adaptive_threshold"])
        if "max_bounces" in profile:
            cycles.max_bounces = int(profile["max_bounces"])

        device = select_cycles_device(render_config, profile.get("prefer_gpu", True))
        applied["device"] = device

        cycles.use_denoising = bool(profile.get("denoise", False))
        if cycles.use_denoising:
            for candidate in profile.get("denoiser_preference", []):
                if _can_set(cycles, "denoiser", candidate):
                    applied["denoiser"] = candidate
                    break
            else:
                applied["denoiser"] = cycles.denoiser
    else:
        eevee = scene.eevee
        if hasattr(eevee, "taa_render_samples"):
            eevee.taa_render_samples = int(profile.get("samples", 32))
        applied["device"] = {
            "requested_gpu": bool(profile.get("prefer_gpu", True)),
            "backend": "EEVEE_GPU_CONTEXT",
            "scene_device": "GPU",
            "gpu_active": True,
            "enabled_devices": ["blender gpu context"],
            "fallback_reason": None,
            "note": (
                "EEVEE always rasterizes through Blender's own GPU context; it does "
                "not use the Cycles device preference."
            ),
        }

    return applied


def render_still(scene_id: str, profile_name: str, output_path: Path) -> dict:
    """Build, configure and render one still; return a full evidence record."""
    scene_config = hc.load_scene_config()
    render_config = hc.load_render_config()

    build_scene.build(scene_id, scene_config)
    applied = apply_profile(profile_name, render_config)

    output_path = Path(output_path)
    hc.ensure_dir(output_path.parent)
    bpy.context.scene.render.filepath = str(output_path.with_suffix(""))

    started = time.perf_counter()
    bpy.ops.render.render(write_still=True)
    elapsed = time.perf_counter() - started

    written = output_path
    if not written.exists():
        candidate = output_path.with_suffix(".png")
        if candidate.exists():
            written = candidate

    record = dict(applied)
    record.update(
        {
            "scene": scene_id,
            "wall_clock_seconds": round(elapsed, 3),
            "output_path": hc.relpath(written),
            "output_exists": written.exists(),
            "output_bytes": written.stat().st_size if written.exists() else 0,
            "sha256": hc.sha256_file(written) if written.exists() else None,
            "blender_version": bpy.app.version_string,
            "python_version": sys.version.split()[0],
        }
    )
    return record
