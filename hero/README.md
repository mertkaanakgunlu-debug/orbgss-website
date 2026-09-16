# OrbGSS cinematic hero production workspace

This folder is the isolated source workspace for `WEB-HERO-001` and later accepted hero-production phases.

Canonical authority: `docs/WEB_HERO_001_AUTHORITY.md` and the linked Drive CURRENT authority.

## Current state

`WEB-HERO-001` is pre-data. Build the scene, Earth, satellite, orbit, AOI geometry, scan system and continuous animatic here. Do not integrate the live homepage or fabricate scientific layers.

`WEB-HERO-001A` established the scaffold below. `WEB-HERO-001B` added the Earth, atmosphere, satellite, starfield and establishing camera move. `WEB-HERO-001C` added the surface-conforming AOI acquisition system described under [AOI system](#aoi-system). `WEB-HERO-001D` assembled all of it into the continuous animatic described under [The continuous animatic](#the-continuous-animatic).

Scenes, in the order they were built:

| scene | phase | frames | what it is |
| --- | --- | --- | --- |
| `benchmark_neutral` | 001A | 1 | neutral pipeline benchmark; measures throughput, expresses no art direction |
| `hero_earth_orbit` | 001B | 1–120 | Earth, atmosphere, satellite, starfield, establishing move |
| `hero_aoi_acquisition` | 001C | 1–240 | `extends` the above, continues the same move into acquisition and regional approach, adds the AOI system |
| `hero_predata_animatic` | 001D | 1–240 | `extends` the above; the full pre-data sequence, re-timed, with the Phase-C quality-gate items closed |

Each scene inherits its predecessor through `extends` rather than copying it, so the accepted Earth/satellite/camera system has exactly one definition and a later phase cannot quietly diverge from the one it continues. `hero_aoi_acquisition` reuses the 001B camera keyframes verbatim for frames 1–120; `hero_predata_animatic` replays the same three accepted establish camera *states* verbatim, re-timed onto its own beat map.

The earlier scenes are not superseded. They stay buildable and are re-rendered as the reproducibility control every phase (see [Reproducibility of renders](#reproducibility-of-renders)).

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
    shot_plan.py          plain Python: derive camera keyframes from shot intent; measure framing
    audit_shot.py         Blender: measure the evaluated camera per frame (continuity contract)
    render_animatic.py    Blender: whole frame range from one build, as video or stills
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

## The continuous animatic

`hero_predata_animatic` is the WEB-HERO-001D deliverable: **Earth establish → satellite entrance
→ AOI acquisition and scan → continuous camera approach → stable regional hold**, 240 frames at
24 fps, as one scene and one uncut camera move.

```powershell
# the whole sequence as a review animatic -> hero/renders/animatic/ (ignored)
& $env:BLENDER -b -P hero/scripts/render_animatic.py -- --scene hero_predata_animatic

# a subset as stills, same build, for iteration
& $env:BLENDER -b -P hero/scripts/render_animatic.py -- --scene hero_predata_animatic --frames 24,140,236 --out $PWD/hero/renders/work/iter
```

The animatic is a **review** artifact. Container, bitrate, poster frame and reduced-motion
packaging are deliberately not decided here; they belong to the later hero/`WEB-005` media task.
Pass absolute paths to `--out`: Blender resolves a relative render path against its own working
directory, not the repository.

### The camera is derived, not typed

Camera coordinates entered by eye are how a move ends up with the footprint drifting off centre,
the limb leaving frame, or the headline area filling with planet. So `camera.shot_intent` in
`scene.json` states the shot in the terms the shot is actually about — *at frame 240, be 13° off
the AOI at a geocentric radius of 7.55 BU on a 44 mm lens* — and `shot_plan.py` converts that into
world keyframes, resolving the AOI centre through `aoi_system.py` and rotating it by the Earth's
own animated rotation at that frame.

```powershell
py -3.14 hero/scripts/shot_plan.py --scene hero_predata_animatic --derive    # intent -> keyframes
py -3.14 hero/scripts/shot_plan.py --scene hero_predata_animatic --analyze   # keyframes -> framing report
```

The keyframes stay committed literally in `scene.json`, because a reviewable diff of a camera path
is worth more than a clever indirection. The validator re-derives them and fails if they have
drifted from their intent, so the two cannot silently disagree.

The establish keyframes are `mode: world` and pass through untouched. That is how the accepted
Phase-B camera states stay bit-identical while being re-timed.

### The aim is locked by constraint

An authored keyframe can only be correct *at* that keyframe. Between keys the footprint travels an
arc on a rotating planet while an interpolated camera aims along a chord, so it drifts in frame. A
`TRACK_TO` constraint on `aoi_target_center` removes that residual by construction — the same move
the Phase-C beams make when they derive their endpoints instead of baking them.

Its influence is keyframed: 0 through the establish, where the planet deliberately sits off-axis so
a headline has somewhere to live, and 1 from frame 136 on. The derived keyframes past the handover
already aim at the AOI centre, so the blend has nothing to correct and cannot swing the camera.
Measured AOI centre error after handover is 0.0 frame widths.

### Headline-safe space

Website copy is never baked into the render, so what the opening owes the later integration task is
empty sky. `camera.composition.headline_safe_region` is that reservation: a left-aligned column at
x 0.05–0.38, y 0.16–0.78. It was measured rather than guessed — widened until the planet first
intruded, then stepped back to the last width that stays completely clear through frame 96.
`shot_plan.py` ray-casts a 28×28 grid of it against the Earth sphere at every establish keyframe,
and the validator fails on any intrusion.

The satellite does transit that column during its entrance. That is deliberate and recorded in the
shot audit: a small hard-surface silhouette behind a headline is a detail, not a legibility
problem, and the check is about the planet's mass.

### Shot audit

`validate_hero.py` checks the sequence *contract* from configuration. `audit_shot.py` checks the
other half — what Blender actually evaluates on every frame, after F-curve interpolation, Earth
rotation, satellite animation and the track constraint:

```powershell
& $env:BLENDER -b -P hero/scripts/audit_shot.py -- --scene hero_predata_animatic --out hero/evidence/shot_audit_predata_animatic.json
```

It turns the cinematography contract into eight measured series with explicit thresholds: AOI
centre lock, apparent-size monotonicity, screen-orientation continuity, camera jerk, focal-length
rate, a cut ratio, AOI presence in frame, and headline-safe occupancy. Subjective questions — is
the palette right, does it feel premium — are deliberately left to the stills and the animatic.

### Atmosphere

The Phase-B/C shell drove its brightness from the Fresnel factor, which is a property of the shell
*surface*, not of the air a view ray crosses. That is why it kept producing a graphic rather than
atmosphere: Fresnel is monotonic, so the glow was brightest exactly at the shell silhouette and
ended on a hard geometric line. Shaping it into a band only moved that line, a second shell added a
second one, and because a Mix Shader *replaces* what is behind it, the shell painted a solid teal
band across the sky as soon as the camera was low enough to see it nearly edge-on.

`profile: "limb_airmass"` drives the glow from the quantity that actually governs limb brightness:
the perigee altitude of each view ray. The camera position is recovered in the shader as the
shading point plus `Incoming × View Distance`, the ray's perigee radius `h` follows, and

```text
glow = exp(-max(0, h - R) / H) · min(1/cos i, sqrt(2πR/H)),   sin i = min(h, R) / R
```

decays exponentially above the limb and carries the real relative air mass across the disc. It is
combined with **Add Shader**, not Mix Shader, because air does not occlude what is behind it. The
result has no visible edge at any distance, and the planet is hazy at its horizon and clean at
nadir.

`strength` is therefore brightness *per air mass*, not a free gain. `max_airmass` is derived from
the scale height rather than authored, so the two cannot drift apart, and the shell radius must
clear several scale heights or the exponential has not decayed by the silhouette and the edge comes
back — the validator checks exactly that.

The accepted Phase-B/C shells are untouched. The legacy Fresnel path is still there and is taken
whenever a spec declares no `profile`, and `hero_predata_animatic` leaves the inherited
`atmosphere_shell` material defined but unreferenced so the accepted material is visibly not edited
in place.

### Earth resolution

The 2048 px albedo magnifies about fourteen times at the regional approach and visibly softens —
an accepted Phase-C limitation and a Phase-D gate item. The Earth material now reads the
8192×4096 member of the *same* NASA Visible Earth record (57735): same scene, same clouds, same
equirectangular projection, same geography, four times the linear resolution, so the accepted
world-coordinate convention and the AOI's configured longitude offset carry over unchanged.
Magnification at the hold drops to about 3.9× at evidence resolution. `day_texture_interpolation`
selects Cubic sampling, since at that magnification the reconstruction filter is visible.

The 2048 px asset stays materialized and recorded: the accepted Phase-B and Phase-C scenes still
reference it and have to stay reproducible.

### What the closest approach costs

Pushing the camera closer makes the footprint bigger and the surface softer, and takes the limb out
of frame. There is no setting that wins all three, so the approach was tuned against numbers rather
than against how a render happened to look. At the hold: 1 179 km altitude, 1 963 km slant range,
44 mm, AOI at 26.1 % of frame width, 59.9° incidence, limb crossing the top edge, 3.9× texture
magnification. `shot_plan.py --analyze` reports all of these per keyframe.

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

Measure instead. `compare_renders.py` reports pixel differences in 8-bit channel levels. Two
things make that measurement trustworthy, and WEB-HERO-001D learned both the hard way:

**Render the old code, now.** Comparing against a PNG committed in an earlier session confounds a
code change with the renderer's own session-to-session variation. Extract the accepted tree whole
and render it in the *same* session as the current one, so the pair differs in exactly one thing:

```powershell
git archive <accepted-commit> hero | tar -x -C <scratch>
# copy hero/assets/source/* into the scratch tree, then render from its own scripts
& $env:BLENDER -b -P <scratch>/hero/scripts/render_still.py -- --scene hero_earth_orbit --frame 120 ...
```

**Measure the floor more than once.** A single repeat pair underestimates it. `hero_earth_orbit`
frame 120 first measured a floor of 3.0 / 0.012 %, which made an accepted-versus-current result of
9.0 / 0.087 % look like a regression. Rendering that frame three times per tree and cross-comparing
every pairing showed the real floor is 9.0 / 0.086 % — including the accepted tree disagreeing with
*itself* by exactly the amount it disagreed with the new tree. The low reading was the outlier.
Keep that accepted-versus-accepted control in the record; it is what makes the result conclusive.

`hero/evidence/phase_abc_reproducibility.json` records the check for WEB-HERO-001D;
`phase_ab_reproducibility.json` is the accepted WEB-HERO-001C record and is left in place. Do not
replace either with a checksum comparison.

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

It also enforces the WEB-HERO-001D sequence contract: exactly one AOI system in the animatic,
a beat map whose beats start in narrative order and lie inside the frame range, an approach that
begins before the establish ends, a regional hold long enough to receive a later data reveal, a
duration inside the hero envelope, a camera that closes monotonically and never reverses its focal
length during the approach, committed keyframes that still match their `shot_intent` derivation, a
headline-safe region the Earth does not intrude into, and an atmosphere shell whose radius clears
several scale heights of its own falloff.

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
- The camera path is derived from the AOI through `shot_intent`, and its aim is held by constraint rather than by hand-matched keyframes.
- Atmosphere is additive and driven by view-ray perigee, so it never occludes and never ends on an edge.
- Continuity, registration and composition claims are measured (`audit_shot.py`, `shot_plan.py`), not asserted.

See the task contracts under `tasks/WEB-HERO-001*.md` for exact phase scope and acceptance.
