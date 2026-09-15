# OrbGSS cinematic hero production workspace

This folder is the isolated source workspace for `WEB-HERO-001` and later accepted hero-production phases.

Canonical authority: `docs/WEB_HERO_001_AUTHORITY.md` and the linked Drive CURRENT authority.

## Current state

`WEB-HERO-001` is pre-data. Build the scene, Earth, satellite, orbit, AOI geometry, scan system and continuous animatic here. Do not integrate the live homepage or fabricate scientific layers.

`WEB-HERO-001A` established the scaffold below. There is no Earth, satellite or AOI geometry yet — only a neutral scene used to benchmark the pipeline.

## Isolation rule

Until a later Product authority explicitly joins this work into `WEB-005`, hero production must not modify the public-site HTML/CSS/JS, proof imagery, deployment configuration or DNS. `hero/config/lane.json` lists the protected paths, and the validator checks them against the pinned baseline commit on every run.

Nothing here is a website runtime dependency. Blender, FFmpeg and the Python in this folder are local production tooling only; the published site remains static HTML, CSS and vanilla JavaScript.

## Layout

```text
hero/
  config/
    lane.json             lane boundaries, pinned baseline, protected paths
    scene.json            palette, camera defaults, scene definitions, AOI injection interface
    render_profiles.json  render profiles, aspect contract, device preference order
  scripts/
    hero_common.py        paths, config loading, hashing (no bpy; importable by plain Python)
    build_scene.py        Blender: build a scene from scene.json
    render_core.py        Blender: profile application + truthful device selection
    render_preview.py     Blender: fast iteration render entrypoint
    render_still.py       Blender: bounded high-quality / evidence still entrypoint
    run_benchmark.py      Blender: all benchmark profiles in one session
    probe_env.py          Blender: record version, Python, render devices
    validate_hero.py      plain Python: workspace contract validation
  assets/
    manifest.json         asset rights/provenance/checksum record
    source/               materialized source assets (ignored)
  blender/                bounded source .blend files, when a task justifies one
  renders/                all generated output (ignored)
  evidence/               small committed review artifacts
```

Configuration is the source of scene truth. Add a scene by adding it to `scene.json`, not by hard-coding values in a render script.

## Reproducing the workspace

Requires Blender 4.5 LTS and any Python 3.11+ for the validator. Nothing else is installed into the repository; there is no virtualenv, lockfile or package manager.

Set the Blender path once per shell (PowerShell):

```powershell
$env:BLENDER = "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"
```

Then, from the repository root:

```powershell
# 1. validate the workspace contract (no Blender needed)
py -3.14 hero/scripts/validate_hero.py

# 2. record what Blender and this machine actually expose
& $env:BLENDER -b -P hero/scripts/probe_env.py -- --out hero/evidence/environment.json

# 3. fast iteration render -> hero/renders/preview/
& $env:BLENDER -b -P hero/scripts/render_preview.py -- --scene benchmark_neutral

# 4. high-quality still -> hero/renders/still/
& $env:BLENDER -b -P hero/scripts/render_still.py -- --scene benchmark_neutral --profile master

# 5. full benchmark across every profile -> hero/evidence/benchmark.json
& $env:BLENDER -b -P hero/scripts/run_benchmark.py -- --scene benchmark_neutral
```

To inspect a scene interactively, build a working `.blend` and open it:

```powershell
& $env:BLENDER -b -P hero/scripts/build_scene.py -- --scene benchmark_neutral --save
& $env:BLENDER hero/renders/work/benchmark_neutral.blend
```

The working `.blend` is generated output, not source authority: rebuild it rather than committing it.

## Render profiles

| profile | role | engine | resolution | samples | committed |
| --- | --- | --- | --- | --- | --- |
| `preview` | fast iteration | EEVEE | 1280×720 | 32 | no |
| `master` | high quality | Cycles | 1920×1080 | 256, OptiX denoise | no |
| `evidence_still` | bounded evidence | Cycles | 1280×720, 8-bit | 256, OptiX denoise | yes |

`master` is the real quality target and stays 16-bit and out of Git. `evidence_still` renders the same Cycles path at reviewable size so a still can be committed without putting a large binary in source control.

Device selection walks `device_preference` in `render_profiles.json` and falls back to CPU when no GPU backend has a device behind it. It reports what it actually used, never what was requested — see `cycles_device_selection` in `hero/evidence/environment.json`.

Blender's `render.engine`, `compute_device_type` and `cycles.denoiser` are dynamic enums whose contents `bl_rna` does not report. `render_core._can_set` probes them by assignment instead; do not "simplify" it back to reading `enum_items`.

## Validation

`py -3.14 hero/scripts/validate_hero.py` fails on a missing scaffold, unparseable or inconsistent configuration, a broken aspect or profile contract, a structurally invalid rights manifest, a scientific layer declared while the lane is pre-data, generated output promoted to source authority, and any drift in the protected public-site paths.

Run it before and after every change in this lane.

## Expected production properties

- Blender Python/configuration is the reproducible source of scene truth.
- Earth is true 3D spherical geometry.
- AOI geometry conforms to the sphere and is configuration-driven, injected through `aoi_injection_interface` in `scene.json`.
- Scan beams/corner locks target the actual 3D footprint.
- Global-to-regional shots preserve continuous AOI registration and scale.
- External source assets are rights/provenance recorded in `hero/assets/manifest.json`. An asset may not be rendered into published evidence until its `rights_status` is `cleared` with a recorded SHA-256.
- Large renders are local/ignored unless a task explicitly publishes bounded evidence. Never commit a frame sequence.

See the task contracts under `tasks/WEB-HERO-001*.md` for exact phase scope and acceptance.
