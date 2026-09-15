# OrbGSS cinematic hero production workspace

This folder is the isolated source workspace for `WEB-HERO-001` and later accepted hero-production phases.

Canonical authority: `docs/WEB_HERO_001_AUTHORITY.md` and the linked Drive CURRENT authority.

## Current state

`WEB-HERO-001` is pre-data. Build the scene, Earth, satellite, orbit, AOI geometry, scan system and continuous animatic here. Do not integrate the live homepage or fabricate scientific layers.

`WEB-HERO-001A` established the scaffold below. `WEB-HERO-001B` added the Earth, atmosphere, satellite, starfield and establishing camera move. `WEB-HERO-001C` added the surface-conforming AOI acquisition system described under [AOI system](#aoi-system).

Scenes, in the order they were built:

| scene | phase | frames | what it is |
| --- | --- | --- | --- |
| `benchmark_neutral` | 001A | 1 | neutral pipeline benchmark; measures throughput, expresses no art direction |
| `hero_earth_orbit` | 001B | 1–120 | Earth, atmosphere, satellite, starfield, establishing move |
| `hero_aoi_acquisition` | 001C | 1–240 | `extends` the above, continues the same move into acquisition and regional approach, adds the AOI system |

`hero_aoi_acquisition` inherits `hero_earth_orbit` through `extends` rather than copying it, so the accepted Earth/satellite/camera system has exactly one definition. Frames 1–120 reuse the 001B camera keyframes verbatim.

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
    hero_common.py        paths, config loading, scene inheritance, hashing (no bpy)
    aoi_system.py         AOI coordinate math and sampling (no bpy; shared by builder and validator)
    build_scene.py        Blender: build a scene from scene.json
    render_core.py        Blender: profile application + truthful device selection
    render_preview.py     Blender: fast iteration render entrypoint
    render_still.py       Blender: bounded high-quality / evidence still entrypoint
    run_benchmark.py      Blender: all benchmark profiles in one session
    probe_env.py          Blender: record version, Python, render devices
    validate_hero.py      plain Python: workspace contract validation
    audit_aoi.py          Blender: measure built AOI geometry in world space, per frame
    compare_renders.py    Blender: pixel-difference two renders (reproducibility evidence)
    contact_sheet.py      Blender: tile frames into one reviewable sheet
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

## AOI system

The AOI is configuration-driven and surface-conforming. It is generated entirely from
`aoi_injection_interface` in `scene.json`; no footprint coordinate is modelled by hand.

`hero/scripts/aoi_system.py` owns every coordinate conversion and holds no `bpy` import, so
the validator checks the same numbers the renderer uses without launching Blender.

**Geometry.** Corners come from the spherical destination formula applied to the configured
centre, span and bearing. Edges and the interior are sampled by slerp between unit vectors and
scaled by one radius, so conformance to the sphere is true by construction rather than by
tuning — measured worst-case radial deviation is sub-metre, and that residual is single-precision
transform error, not approximation. Border and corner-lock ribbons are widened by rotating each
sample *within its own tangent plane*, which keeps both rails on the sphere.

**Registration.** The AOI is parented to the Earth, so footprint, corner locks and per-corner
target empties ride the globe's rotation. Beams are not keyframed: each beam is a unit-length
tapered tube with a Copy Location constraint on the satellite and a Stretch To constraint on its
corner empty. A beam endpoint is therefore *derived* from the AOI at every frame rather than being
a constant that happens to match on one. The validator rejects any literal coordinate inside an
`aoi_system` spec for exactly this reason.

**Scan sweep.** The interior mesh carries AOI-local `(u, v)` in its UV layer, and the sweep is a
band travelling through that parameter space on a mesh that is itself on the sphere. It cannot
detach from the globe however the camera moves.

**Configurability.** `active_fixture` selects a fixture; `--aoi-fixture` overrides it on any
build or render entrypoint. Two design fixtures ship, deliberately differing in centre,
hemisphere, span, bearing and sampling density:

```powershell
& $env:BLENDER -b -P hero/scripts/render_preview.py -- --scene hero_aoi_acquisition --aoi-fixture design_secondary --frame 130
& $env:BLENDER -b -P hero/scripts/audit_aoi.py -- --scene hero_aoi_acquisition --aoi-fixture design_secondary
```

**Pre-data.** Both fixtures are neutral design placeholders carrying no measurement meaning. The
footprint interior shows only a faint cyan wash, a slightly denser already-swept region and the
sweep band. Nothing in it encodes a measured quantity, and there is no legend, scale or
classification anywhere in the scene.

## Geometry audit

`validate_hero.py` checks the AOI *contract* from configuration. `audit_aoi.py` checks the other
half — that the geometry Blender actually evaluates, after parenting, Earth rotation, satellite
animation and the beam constraints, still sits where the configuration says:

```powershell
& $env:BLENDER -b -P hero/scripts/audit_aoi.py -- --scene hero_aoi_acquisition --out hero/evidence/aoi_geometry_audit_design_primary.json
```

It reports, per frame: worst radial deviation of every AOI vertex from the configured sphere,
each beam's tip-to-corner and root-to-satellite error, measured footprint edge lengths, surface
clearance and sweep position. Its tolerances are an absolute floor plus a relative term sized to
single-precision transform error at planetary scale — an absolute sub-metre bound would be testing
float32, not the implementation, and the tolerances still sit three or more orders of magnitude
below any real registration defect.

## Reproducibility of renders

The Cycles + OptiX-denoise GPU path is **not** bit-reproducible on this machine: two renders of
one unchanged scene, from the same commit, produce different file hashes. A checksum therefore
cannot answer "did this change alter an earlier phase's render?".

Measure instead. `compare_renders.py` reports pixel differences in 8-bit channel levels; compare
a rebuild-versus-committed difference against the renderer's own noise floor (one unchanged scene
rendered twice). `hero/evidence/phase_ab_reproducibility.json` records that check for
WEB-HERO-001C. Do not replace it with a checksum comparison.

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

It also enforces the WEB-HERO-001C AOI contract: every generated point on the configured sphere,
a surface offset small enough to be a z-fighting guard rather than an altitude, four uniquely
named corners, footprint edges measuring the configured span, boundary sampling dense enough that
a drawn chord stays within 50 m of the arc it replaces, beams that target the AOI system instead
of a fixed point, no literal coordinate inside an `aoi_system` spec, and at least two fixtures
that resolve to genuinely different footprints.

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
