"""Validate the hero production workspace without launching Blender.

    py -3.14 hero/scripts/validate_hero.py

Fails loudly on broken production assumptions: missing scaffold, unparseable or
inconsistent configuration, a structurally invalid rights manifest, a scientific
layer smuggled into this pre-data phase, generated output treated as source
authority, or public-site contamination from the hero lane.

This is a contract checker, not a build system. Keep it that way.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import hero_common as hc  # noqa: E402

MAX_TRACKED_BYTES = 4 * 1024 * 1024
SELF_NAME = Path(__file__).name
HEX64 = re.compile(r"^[0-9a-f]{64}$")


class Report:
    def __init__(self) -> None:
        self.checks = 0
        self.failures = []

    def check(self, ok: bool, label: str, detail: str = "") -> bool:
        self.checks += 1
        if ok:
            print("  PASS  " + label)
        else:
            message = label + ((" — " + detail) if detail else "")
            print("  FAIL  " + message)
            self.failures.append(message)
        return ok

    def section(self, title: str) -> None:
        print("\n" + title)


def tokens(value: str):
    return {token for token in re.split(r"[^a-zA-Z0-9]+", str(value).lower()) if token}


def check_scaffold(report: Report) -> None:
    report.section("scaffold")
    for path in (
        hc.CONFIG_DIR,
        hc.ASSETS_DIR,
        hc.SOURCE_DIR,
        hc.BLEND_DIR,
        hc.RENDERS_DIR,
        hc.EVIDENCE_DIR,
    ):
        report.check(path.is_dir(), "directory present: " + hc.relpath(path))

    for path in (
        hc.SCENE_CONFIG,
        hc.RENDER_CONFIG,
        hc.LANE_CONFIG,
        hc.ASSET_MANIFEST,
        hc.HERO_ROOT / "README.md",
    ):
        report.check(path.is_file(), "file present: " + hc.relpath(path))

    for name in (
        "hero_common.py",
        "build_scene.py",
        "render_core.py",
        "render_preview.py",
        "render_still.py",
        "probe_env.py",
        "validate_hero.py",
    ):
        path = hc.HERO_ROOT / "scripts" / name
        report.check(path.is_file(), "entrypoint present: " + hc.relpath(path))


def load_configs(report: Report):
    report.section("configuration parses")
    loaded = {}
    for key, path in (
        ("scene", hc.SCENE_CONFIG),
        ("render", hc.RENDER_CONFIG),
        ("lane", hc.LANE_CONFIG),
        ("manifest", hc.ASSET_MANIFEST),
    ):
        try:
            loaded[key] = hc.load_json(path)
            report.check(True, "parseable JSON: " + hc.relpath(path))
        except (OSError, json.JSONDecodeError) as error:
            loaded[key] = None
            report.check(False, "parseable JSON: " + hc.relpath(path), str(error))
    return loaded


def check_render_profiles(report: Report, render_config) -> None:
    report.section("render profile consistency")
    if not render_config:
        report.check(False, "render profiles loaded")
        return

    profiles = render_config.get("profiles", {})
    aliases = render_config.get("engine_aliases", {})
    aspect = render_config.get("aspect_ratio", {})

    report.check(bool(profiles), "at least one render profile is defined")
    report.check(
        bool(aspect.get("width")) and bool(aspect.get("height")),
        "a working aspect ratio is configured",
    )

    required = ("role", "engine", "resolution_x", "resolution_y", "samples", "file_format")
    for name, profile in profiles.items():
        missing = [key for key in required if key not in profile]
        report.check(
            not missing,
            "profile " + name + " declares required keys",
            "missing " + repr(missing),
        )
        report.check(
            profile.get("engine") in aliases,
            "profile " + name + " uses a known logical engine",
            repr(profile.get("engine")) + " not in " + repr(sorted(aliases)),
        )
        if aspect and "resolution_x" in profile and "resolution_y" in profile:
            matches = (
                profile["resolution_x"] * aspect["height"]
                == profile["resolution_y"] * aspect["width"]
            )
            report.check(
                matches,
                "profile " + name + " matches the configured aspect ratio",
                str(profile["resolution_x"]) + "x" + str(profile["resolution_y"]),
            )

    roles = {profile.get("role") for profile in profiles.values()}
    report.check("fast_iteration" in roles, "a fast iteration profile exists")
    report.check("high_quality" in roles, "a high quality profile exists")

    high_quality = [p for p in profiles.values() if p.get("role") == "high_quality"]
    report.check(
        all(p.get("engine") == "CYCLES" for p in high_quality),
        "every high quality profile targets Cycles",
    )

    for key in ("default_preview_profile", "default_still_profile"):
        report.check(
            render_config.get(key) in profiles,
            "configured " + key + " resolves to a defined profile",
            repr(render_config.get(key)),
        )

    report.check(
        bool(render_config.get("device_preference")),
        "a GPU device preference order is configured",
    )
    report.check(
        "allow_cpu_fallback" in render_config,
        "CPU fallback policy is stated explicitly",
    )


def check_scene_config(report: Report, scene_config, render_config) -> None:
    report.section("scene configuration")
    if not scene_config:
        report.check(False, "scene configuration loaded")
        return

    palette = scene_config.get("palette", {})
    scenes = scene_config.get("scenes", {})
    report.check(bool(palette), "a palette is defined")
    report.check(bool(scenes), "at least one scene is defined")

    for scene_id, spec in scenes.items():
        refs = []
        for material in spec.get("materials", {}).values():
            refs.append(material.get("base_color_ref"))
            if material.get("emission_color_ref"):
                refs.append(material["emission_color_ref"])
        for light in spec.get("lights", []):
            if light.get("color_ref"):
                refs.append(light["color_ref"])
        world_ref = scene_config.get("world", {}).get("background_color_ref")
        if world_ref:
            refs.append(world_ref)

        unknown = sorted({ref for ref in refs if ref and ref not in palette})
        report.check(
            not unknown,
            "scene " + scene_id + " resolves every palette reference",
            "unknown " + repr(unknown),
        )

        materials = set(spec.get("materials", {}))
        dangling = sorted(
            {
                obj.get("material")
                for obj in spec.get("objects", [])
                if obj.get("material") and obj["material"] not in materials
            }
        )
        report.check(
            not dangling,
            "scene " + scene_id + " resolves every material reference",
            "undefined " + repr(dangling),
        )
        report.check(
            bool(spec.get("camera")), "scene " + scene_id + " defines a camera"
        )

    interface = scene_config.get("aoi_injection_interface")
    report.check(
        isinstance(interface, dict),
        "a configuration-driven AOI/data injection interface is declared",
    )


def check_pre_data_boundary(report: Report, scene_config, manifest) -> None:
    report.section("pre-data scientific boundary")
    if not scene_config or not manifest:
        report.check(False, "scene configuration and manifest loaded")
        return

    forbidden = set(manifest.get("policy", {}).get("forbidden_layer_classes", []))
    report.check(bool(forbidden), "a forbidden scientific layer vocabulary is declared")

    pre_data = scene_config.get("data_state") == "pre_data"
    report.check(pre_data, "scene configuration declares the pre-data state")

    identifiers = []
    for scene_id, spec in scene_config.get("scenes", {}).items():
        identifiers.append(("scene id", scene_id))
        for obj in spec.get("objects", []):
            identifiers.append(("object id", obj.get("id", "")))
        for name in spec.get("materials", {}):
            identifiers.append(("material", name))
        for light in spec.get("lights", []):
            identifiers.append(("light id", light.get("id", "")))

    interface = scene_config.get("aoi_injection_interface", {})
    for slot in interface.get("layer_slots", []):
        identifiers.append(("aoi layer slot", json.dumps(slot)))

    for asset in manifest.get("assets", []):
        for field in ("id", "role", "layer_class", "local_path"):
            if asset.get(field):
                identifiers.append(("asset " + field, asset[field]))

    hits = [
        (kind, value, sorted(tokens(value) & forbidden))
        for kind, value in identifiers
        if tokens(value) & forbidden
    ]
    report.check(
        not hits,
        "no scientific layer is declared anywhere in this pre-data phase",
        "; ".join(k + " " + repr(v) + " matches " + repr(m) for k, v, m in hits),
    )

    if pre_data:
        report.check(
            not interface.get("layer_slots"),
            "the AOI interface declares no populated layer slot while pre-data",
        )
        report.check(
            interface.get("classification") == "design_fixture",
            "AOI placeholder geometry is classified as a design fixture",
            repr(interface.get("classification")),
        )


def check_manifest(report: Report, manifest) -> None:
    report.section("asset rights manifest")
    if not manifest:
        report.check(False, "manifest loaded")
        return

    policy = manifest.get("policy", {})
    report.check("schema_version" in manifest, "manifest declares a schema version")
    report.check(bool(policy), "manifest declares a rights policy")
    report.check(isinstance(manifest.get("assets"), list), "manifest declares an asset list")

    required = policy.get("required_fields", [])
    allowed_licenses = set(policy.get("allowed_license_bases", []))
    status_values = set(policy.get("rights_status_values", []))
    publishable = set(policy.get("publishable_rights_status", []))
    report.check(bool(required), "manifest states its required asset fields")
    report.check(bool(allowed_licenses), "manifest states an allowed license basis set")

    for index, asset in enumerate(manifest.get("assets", [])):
        label = "asset[" + str(index) + "] " + str(asset.get("id", "<no id>"))
        missing = [
            field
            for field in required
            if field not in asset or asset[field] in (None, "")
        ]
        report.check(
            not missing, label + " declares every required field", "missing " + repr(missing)
        )
        report.check(
            asset.get("license") in allowed_licenses,
            label + " uses an allowed license basis",
            repr(asset.get("license")),
        )
        report.check(
            asset.get("rights_status") in status_values,
            label + " uses a known rights status",
            repr(asset.get("rights_status")),
        )
        if asset.get("rights_status") in publishable:
            digest = str(asset.get("sha256", ""))
            report.check(
                bool(HEX64.match(digest)),
                label + " records a SHA-256 for cleared material",
                repr(digest),
            )
            local = asset.get("local_path")
            if local:
                path = hc.REPO_ROOT / local
                report.check(
                    path.exists(),
                    label + " materialized local path exists",
                    hc.relpath(path),
                )


def check_generated_output_policy(report: Report) -> None:
    report.section("generated output is not source authority")
    for directory in hc.GENERATED_DIRS:
        ignore = directory / ".gitignore"
        if not report.check(
            ignore.is_file(), "ignore policy present: " + hc.relpath(ignore)
        ):
            continue
        lines = [line.strip() for line in ignore.read_text(encoding="utf-8").splitlines()]
        report.check(
            "*" in lines and "!.gitignore" in lines,
            hc.relpath(directory) + " ignores its payload but keeps the directory",
            repr(lines),
        )

    tracked = git_tracked_hero_files()
    if tracked is None:
        print("  SKIP  tracked-size audit (git unavailable)")
        return

    oversized = []
    sequences = []
    for rel in tracked:
        path = hc.REPO_ROOT / rel
        if path.is_file() and path.stat().st_size > MAX_TRACKED_BYTES:
            oversized.append(rel + " (" + str(path.stat().st_size) + " bytes)")
        if re.search(r"\d{4}\.(png|jpg|jpeg|exr|tif|tiff)$", rel, re.IGNORECASE):
            sequences.append(rel)

    report.check(
        not oversized,
        "no oversized binary is tracked under hero/",
        "; ".join(oversized),
    )
    report.check(
        not sequences,
        "no frame sequence is tracked under hero/",
        "; ".join(sequences),
    )
    report.check(
        not any(rel.startswith("hero/renders/") for rel in tracked if not rel.endswith(".gitignore")),
        "hero/renders/ has no tracked payload",
    )


def git_tracked_hero_files():
    try:
        output = subprocess.run(
            ["git", "-C", str(hc.REPO_ROOT), "ls-files", "hero"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return [line.strip() for line in output.splitlines() if line.strip()]


def git(*args):
    """Run a git command in the repository; return stdout, or None on failure."""
    try:
        return subprocess.run(
            ["git", "-C", str(hc.REPO_ROOT), *args],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None


def check_lane_isolation(report: Report, lane) -> None:
    report.section("lane isolation")
    if not lane:
        report.check(False, "lane configuration loaded")
        return

    protected = lane.get("protected_paths", [])
    baseline = lane.get("baseline_commit")
    report.check(bool(protected), "lane configuration lists protected public-site paths")
    report.check(bool(baseline), "lane configuration pins a baseline commit")

    # No hero source file may name a protected path: this lane builds no site
    # integration, so even a reference is a smell. The validator itself is the
    # one file that legitimately holds these names.
    offenders = []
    for path in sorted(hc.HERO_ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".py", ".json", ".md"}:
            continue
        if path.name == SELF_NAME or hc.CONFIG_DIR == path.parent and path.name == "lane.json":
            continue
        if hc.RENDERS_DIR in path.parents or hc.SOURCE_DIR in path.parents:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name in protected:
            if name in text:
                offenders.append(hc.relpath(path) + " mentions " + name)
    report.check(
        not offenders,
        "no hero source file references a protected public-site path",
        "; ".join(offenders),
    )

    if not baseline:
        return

    if git("cat-file", "-e", baseline + "^{commit}") is None:
        print("  SKIP  baseline comparison (baseline commit not present locally)")
        return

    drift = git("diff", "--name-only", baseline, "HEAD", "--", *protected)
    if drift is None:
        print("  SKIP  baseline comparison (git diff unavailable)")
    else:
        changed = [line for line in drift.splitlines() if line.strip()]
        report.check(
            not changed,
            "protected public-site paths are unchanged since the pinned baseline",
            "; ".join(changed),
        )

    dirty = git("status", "--porcelain", "--", *protected)
    if dirty is not None:
        entries = [line for line in dirty.splitlines() if line.strip()]
        report.check(
            not entries,
            "protected public-site paths have no uncommitted modification",
            "; ".join(entries),
        )


def main() -> int:
    print("OrbGSS hero workspace validation — " + hc.relpath(hc.HERO_ROOT))
    report = Report()

    check_scaffold(report)
    loaded = load_configs(report)
    check_render_profiles(report, loaded.get("render"))
    check_scene_config(report, loaded.get("scene"), loaded.get("render"))
    check_pre_data_boundary(report, loaded.get("scene"), loaded.get("manifest"))
    check_manifest(report, loaded.get("manifest"))
    check_generated_output_policy(report)
    check_lane_isolation(report, loaded.get("lane"))

    print("\n" + str(report.checks) + " checks, " + str(len(report.failures)) + " failed")
    if report.failures:
        print("VALIDATION FAILED")
        return 1
    print("VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
