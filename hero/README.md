# OrbGSS cinematic hero production workspace

This folder is the isolated source workspace for `WEB-HERO-001` and later accepted hero-production phases.

Canonical authority: `docs/WEB_HERO_001_AUTHORITY.md` and the linked Drive CURRENT authority.

## Current state

`WEB-HERO-001` was pre-data and is accepted. `WEB-005` bound the accepted Kızıldere regional frame and shipped the production hero; `WEB-005A R2` revised its visual treatment (see [WEB-005A R2: the production hero](#web-005a-r2-the-production-hero)), and `WEB-005A R3` re-choreographed it after R2 did not pass the human visual gate (see [WEB-005A R3: settle, dive, analysis frame](#web-005a-r3-settle-dive-analysis-frame)). No scientific layer is baked into any frame.

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
    orbit_plan.py         plain Python: derive satellite keyframes from an orbit intent; plan a pass against the camera
    satellite_model.py    Blender: procedural generic EO satellite, orbital trail, satellite light isolation
    materialize_earth_detail.py  Blender: cut the 500 m regional detail window from a Blue Marble tile
    materialize_earth_sharpen.py Blender: derive the 30 m regional detail multiplier from Sentinel-2 L2A tiles (R3)
    encode_production_media.py   Blender: WebM / MP4 / poster inside the accepted media envelope
    materialize_analytical_assets.py  plain Python: ingest the pinned DEM + display textures by copy and SHA-256 (R3 gate)
    analysis_reveal.py    Blender: scan fan, persistent lock-frame morph, DEM relief and display-layer material (R3 gate)
    derive_presentation.py Blender: lock-frame span / line-weight ramps from the evaluated camera (R3 gate)
    audit_preview_gate.py Blender: per-frame proof of the R3 preview gate (fixed camera, sequence, draw-on, true-corner anchors, reticle, exit, relief, timing)
    render_drape_states.py Blender: the analytical drape states as lossless RGBA overlays through a Standard view (R3 gate 2)
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

## WEB-005A R2: the production hero

`hero_production_kizildere` is the scene the site ships. WEB-005A R2 revised its visual treatment
after Product rejected the first checkpoint; the world, the accepted establish and the AOI system
are unchanged, and everything below is configuration in `scene.json` translated by the builder.

### The satellite is derived, and volumetric

The accepted placeholder (a bus, two flat panels and a cone) is still used by the four accepted
scenes. The production scene uses `eo_satellite` from `hero/scripts/satellite_model.py`: a
bevelled bus in crinkled MLI with structural end frames and a radiator, a nadir instrument deck
with two apertures, two three-segment arrays with real thickness on yokes with pale backs, a spun
parabolic dish with feed and mount, star trackers and a thruster. It is procedural and OrbGSS
original, so it is rights-clean by construction and the signature of no operational spacecraft.
`wingspan_bu` is hero scale, chosen for legibility; `yaw_deg` turns the array axis across the
line of sight, because a wing axis normal to the orbit plane pointed straight at the camera and
collapsed the platform to a dot at review size.

Its pass is stated as an `orbit_intent` -- altitude, a sub-satellite anchor at an anchor frame, a
heading and an angular rate -- and `hero/scripts/orbit_plan.py` derives the committed
`location_keyframes` from it, exactly as `shot_plan.py` derives the camera. The validator
re-derives and fails on drift. `orbit_plan.py --analyze` plans a pass against the camera path
(screen position, occlusion by the planet, distance, on-screen size per frame) so the four
requirements the R2 lock names -- hidden at the open, emerging around the limb, lower-left and
unclipped through the acquisition beat, never a foreground fly-by -- are searched for, not tuned
by eye. The `orbit_trail` object is a ribbon on the same derived circle showing a fading window
of arc behind the satellite, so it cannot disagree with the pass it decorates.

Self-shadowing is what makes a body read as volumetric, and a hero-scale body must never print
its shadow on the planet. `lighting_isolation` uses Cycles light linking: the primary sun keeps
lighting everything but the satellite with only the planet as a blocker, and a duplicate sun
lights only the satellite with its own parts as blockers.

### Lens shift, not a re-aim

The AOI track constraint keeps the footprint on the optical axis. `camera.shift_keyframes` move
where that axis lands in the frame (`x = 0.5 - shift_x`, `y = 0.5 - shift_y * 16/9`), so the
target sits upper-right with the Earth right-dominant and the headline column clear, and the
page-layer result has the lower right to land in. `audit_shot.py` projects through Blender's own
`world_to_camera_view`, so the lock is checked against the shifted anchor per frame, and it now
also reports satellite width, occlusion and side against the declared `acquisition_beat` and
`satellite_readability` bounds, plus a `handoff_anchor` (AOI centre, extent and frame bounds on
the last frame) that the page's `data-hero-anchor` must match.

### Sensing lines and the lock event

`beams.target: corners` draws four thin core lines (`aoi_beam`, #7FEFFF) from the satellite to
the footprint corners, each inside a wider, fainter glow tube (`aoi_beam_glow`, #3CCBFF), with one
very faint support cone to the centre. Endpoints are still derived by constraint, so the lines
stay connected to satellite and footprint at every frame, including after the satellite has left
the frame. The border carries a soft halo ribbon (`aoi_glow_ribbon`), the corner locks draw in
from their corners (`aoi_lock_draw`, keyed by `draw_start_frame`/`draw_end_frame`), and the
`emphasis` ramps give the frame a lock pulse at 134-158 and a gentler settle at 232-262 that the
page hands off from. A compositor bloom (`post_processing.glare`) adds a controlled halo above a
threshold nothing sunlit on the planet reaches. The validator holds the lines inside a checkable
envelope: thin (core tip radius <= 8 km), legible (core alpha and emission floors), a glow that
stays a sheath, a cone that stays secondary, and no sensing-physics vocabulary anywhere in the
production configuration.

### Earth albedo stack

`earth_surface` layers three cleared NASA sources: the Blue Marble Next Generation July 2004
global composite with topography and bathymetry (21600 x 10800, about 1.5 km per texel at the
AOI) as the albedo, a lossless 8160 x 5520 crop of the 500 m C1 tile of the same dataset cut by
`hero/scripts/materialize_earth_detail.py` for longitude 12-46 E / latitude 27-50 N and blended in
over a 2.5 degree feather, and the Blue Marble 8192 cloud composite mixed on top -- which is how
the accepted `land_ocean_ice_cloud` texture was itself assembled, so the global look carries
over. `sea_tint` pulls open water toward the accepted darker navy from an albedo-derived mask.
`hero/evidence/earth_detail_crop.json` records the exact texel rectangle and checksums. None of
it is a measured layer and none of it moves the accepted target registration; the validator
checks every texture against the manifest and the detail window against the crop record.

## WEB-005A R3: settle, dive, analysis frame

R2 was technically green and did not pass the human visual gate. R3 keeps its satellite model, its
sensing-line envelope, its lock event and its Earth stack, and changes the choreography, the hold
and what the page does with it. Everything below is still configuration in `scene.json`.

### The pass is time-remapped, and the camera is locked off for the beat

`orbit_intent.rate_profile` is `[[frame, degrees of arc per frame], ...]`, linearly interpolated;
`orbit_plan.py` integrates it exactly, so the pass is still one circle at one altitude and the
validator still re-derives every committed keyframe. The R3 profile runs 2.4 deg/frame while the
platform is behind the planet and coming round the limb, eases over frames 60-110, and holds
0.03 deg/frame afterwards. That alone does not make a satellite *settle*: measured per frame, the
on-screen drift of a body this close to the camera is parallax from the camera's own dolly, not
orbital motion. So the camera is locked off from the handover (136) to the release (192) -- radius
14.4 to 14.0 BU, 37 to 38 mm -- and makes its whole approach afterwards. The anchor is then the
solution of "be at (0.25, 0.40) of the frame at frame 146", and the audit confirms the platform
stays within 0.01 of that point for 56 frames at 13 percent of the frame width.

The sensing lines release at 178-192, *inside* the acquisition beat, so they are never drawn from a
platform that has left the frame; the audit checks the satellite is still visible at the release
frame and gone before the hold.

### One dive, and a frame that can vanish

From 192 the camera makes one eased dive to a hold 166 km across (radius 7.1 BU, 729 km altitude,
176 mm, 27 degrees off nadir), reached at 262 and keyed again at 276 so the hold is genuinely
still. The audit's lens check is now relative (`d(f)/f` per frame, 5 percent ceiling), because a
zoom's perceived speed is fractional. The `production` render profile carries
`motion_blur_shutter: 0.5`; every other profile renders exactly as before.

`aoi_emission` materials now carry an `aoi_presence` gate through a transparent mix, keyed from the
object's `appear_start_frame` and an optional `vanish: [start, end]`. An emission ribbon at
strength zero is a black ribbon -- invisible while sub-pixel, a dark line once the camera is close
-- so the regional frame's border, halo and fill vanish (224-240) instead of being dimmed; its corner locks simply sweep out of frame with the dive.

### The analysis frame

`kizildere_analysis` is a second fixture, classification `production_analysis_aoi`,
`is_analysis_aoi: true`: the accepted centre, the accepted 36 km extent, turned 1.10 degrees for
UTM 35N grid convergence. The `aoi_analysis` object draws it with its own material datablocks (two
AOI systems keying one material would fight over its sockets), no sensing lines, a draw-in at
240-254 with a 2.4x lock pulse, and a sealing sweep. `audit_shot.py` publishes its last-frame centre
and four projected corners as `handoff_anchor`; the page registers the governed rasters onto those
corners as HTML, and `scripts/validate_site.py` checks the page against the audit. Nothing
scientific is rendered into the frame.

### Detail multiplier under the hold

At 166 km across, the 500 m Blue Marble window is magnified 4.2 times. `materialize_earth_sharpen.py`
derives a greyscale ratio from Sentinel-2 L2A (10 m red and blue BOA reflectance to 30 m, divided by
its own 510 m blur, SCL-masked, UTM 35N to equirectangular through a forward projection verified to
0.05 m against the accepted centre), and `earth_surface.detail_sharpen` multiplies the albedo by it
inside its window. The 500 m mean is preserved and no colour is introduced, so there is no seam and no
season; `clear_clouds` scales the 5 km cloud composite down over the same window, where it would
otherwise smear into a veil. The ratio is a presentation texture, recorded in the manifest with its
Copernicus attribution, checksummed by the validator, and never delivered to the page.

## WEB-005A R3 preview gate: fixed observer, scan fan, one lock frame, DEM relief

Product returned the R3 checkpoint `REVISION_REQUIRED` and asked for a low-cost preview before any
further long render (`tasks/WEB-005A_R3_PREVIEW_GATE.md`), then reviewed that preview and asked for a
corrected second one (`tasks/WEB-005A_R3_PREVIEW_GATE_2.md`). `hero_r3_preview_gate` is that preview, in
its second revision; the first is retained in git at `cd2018e` with its evidence under
`hero/evidence/web005a_r3_preview/`. It
`extends` the production scene, re-authors its AOI object (`"replace": true`), drops the separate
analysis frame (`"omit": true`) and leaves `hero_production_kizildere` and its shipped media alone.

**The observer is fixed by construction.** `{"frame": 1, "mode": "hold_of", "of_frame": 186}` copies the
derived acquisition state to the first frame, `camera.fixed_through_frame` makes the builder refuse any
channel that changes before that frame and hold the rest CONSTANT, and the AOI track constraint stays at zero
influence until then -- it would otherwise turn the camera with the Earth. The satellite pass is
re-solved against that one camera so the platform settles right of the hero copy column.

**The lock frame is sized in screen space; the footprint is not touched.** `presentation.screen_intent`
states on-screen width, line weight, halo and corner-arm length in pixels. `derive_presentation.py`
measures the evaluated camera's ground scale on every frame of the approach and writes
`presentation.derived`: acquisition and settled ground dimensions plus two ramps. Each ribbon is built
at the true footprint and carries shape keys -- `presented` (span), `sag_comp` (the chord's sagitta,
weighted 4m(1-m), so a straight blend never cuts under the sphere), `weight` (line weight, its own ramp
because ground scale falls hyperbolically under the dive) and `drape`.

**Ground geometry is true; only the reticle is presentation (second gate).** Product rejected the first
gate's `beams.anchor: presented` (`docs/web-005-polish-authority@c7c6cb1`, section 2). The gate now
declares `beams.anchor: true`: the line anchors, the scan fill and the fan's ground line are all the
governed 36 km footprint, and the validator refuses anything else. `presentation.reticle_parts:
["corner_locks"]` names the only ribbons that travel from the presented span onto the footprint; the
outline and its halo sit on the true corners for the whole shot and change nothing but line weight.
`aoi_true_<corner>` empties are still built, and the audit measures every line tip against them by name.

**The lines leave the aperture and draw on.** `beams.emitter` names the instrument aperture; one empty
rides the Earth's frame at that aperture (Copy Location: the platform's position, the Earth's
orientation) with four children on the rim, laid out along the footprint's own east and north, so line
k runs from rim point k to true corner k and no two cross. `beams.draw` turns the appearance into
propagation: one LINEAR-keyed `aoi_beam_draw` value, a per-line `beam_delay` object property for the
stagger, and a mask along the tube's own UV with the ease-out applied per line in the material, so all
four lines take the same number of frames. The geometry -- and so the endpoint -- stays owned by the
constraints.

**The order of events is a contract.** Pass settles (rate profile at station-keeping) -> platform slews
(`aim` influence) -> slew complete -> lines draw on -> outline and reticle lock -> fan and sweep -> fan,
wash and lines retire -> camera moves. The validator proves the order from configuration, evaluating the
orbit rate per frame; the audit proves it from the evaluated scene, including that the aiming beat is a
real slew that ends on the target. The platform resumes its own pass only at the release frame, and the
first part of the approach is almost purely optical, which is what keeps the exit inside the fly-by
bound: zooming about the AOI alone cannot, because the silhouette would need about 3.5x before it cleared
the frame.

**The scan fan is secondary by construction.** A veil and a light curtain: translucent slices down to a
north-south ground line, lit only near the sweep. With `scan_fan.top` the fan is broad in space and true
on the ground -- its upper edge is a rectangle on the aperture, long along the sweep axis, its foot is the
governed footprint -- so a sweep that is a few pixels of travel on the ground is tens of pixels aloft.
Top vertices are offsets about the local origin, hooked to the emitter root (a pure translation onto the
platform); ground vertices ride the Earth. Curtain and ground band read one keyed `aoi_sweep_position`.
The validator caps their alphas and keeps the curtain dimmer than the lines. Keep a faint emitter
brighter than sunlit ground: an alpha mix replaces a fraction of what is behind it, so a veil darker
than desert prints a grey wedge instead of a light one.

**Relief comes from the governed DEM and nothing else.** `aoi_relief` reads `kizildere_top_dem.tif` as
float32 (values verified identical to rasterio), displaces a grid on the fixture's own corner
interpolation, and gives the lock frame its `drape` key from the same samples. The four display
textures are material on one UV. `materialize_analytical_assets.py` records what was ingested.
THM-01, ALT-01 and priority are fully emissive (scene light may not re-author thematic colour); only
Terrain takes light. `render_drape_states.py` renders each state on its own -- relief only, transparent
film, `Standard` view, RGBA PNG, crisp frame lines as holdouts -- which is the lossless page-composited
delivery Product chose; no governed thematic pixel goes into a lossy encode. ALT-01 and priority carry a
feathered alpha mask (about 9 % transparent, 16 % partial) that the material blends toward the declared
NoData neutral; any colour check has to model that rule or it will misreport a quarter of the surface.

```powershell
py -3.14 hero/scripts/materialize_analytical_assets.py
& $env:BLENDER -b -P hero/scripts/derive_presentation.py -- --scene hero_r3_preview_gate
& $env:BLENDER -b -P hero/scripts/audit_preview_gate.py -- --scene hero_r3_preview_gate --out hero/evidence/web005a_r3_preview2/preview_gate_audit.json
& $env:BLENDER -b -P hero/scripts/render_animatic.py -- --scene hero_r3_preview_gate --profile preview_gate --frames 112,138,156,187,384 --out $PWD/hero/renders/preview_r3gate2/stills
& $env:BLENDER -b -P hero/scripts/render_drape_states.py -- --scene hero_r3_preview_gate --profile preview_gate --out hero/renders/preview_r3gate2/drape
```

Measure distances at planetary radius in double precision: `mathutils.Vector.angle` is single precision
through `acos` near 1 and cannot resolve a kilometre, let alone a metre.

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
