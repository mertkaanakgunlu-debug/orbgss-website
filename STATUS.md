# OrbGSS Website — WEB-HERO-001 branch status

**Date:** 2026-09-16  
**Branch:** `feat/web-hero-001-predata-scene`  
**Baseline:** accepted canonical `main@677bfa7672ac18c2c808ddaaf235ff12863de443`  
**Authority-publication HEAD before implementation:** `0e572e9cfd1709a4e3eb6d3ca110390c79cc6668`  
**Stage:** `WEB-HERO-001D — REVIEW_READY` (continuous pre-data animatic assembled and quality gate closed; WEB-HERO-001A/B/C accepted)  
**Tracking:** parent `MER-97`; active phase `MER-101`  
**Execution channel:** Claude Code Desktop

## Branch-specific authority override

This branch is the deliberately approved **pre-data cinematic hero production lane**. Read `docs/WEB_HERO_001_AUTHORITY.md` immediately after this file and before applying the older hero-defer language in `docs/WEB_VNEXT_AUTHORITY.md`.

For this branch only, `docs/WEB_HERO_001_AUTHORITY.md` and the linked Drive `CURRENT — OrbGSS Hero Visual & Production Authority v1.0` supersede the older rule that all cinematic-hero production must wait for WEB-004/WEB-005. The override is narrow:

- pre-data Blender scene work may proceed now under `hero/`;
- no live homepage integration is authorized;
- no invented or real scientific layer is authorized in WEB-HERO-001;
- `WEB-005` remains the final real-data/media/site integration and release gate.

All other still-valid website, rights, claim, deployment and safety rules remain in force.

## Active exact task

`tasks/WEB-HERO-001A_PRODUCTION_SCAFFOLD.md` — **ACCEPTED** at `81a0b892a355a22d24c78193506ea138de1db017`.

`tasks/WEB-HERO-001B_EARTH_SATELLITE_CINEMATOGRAPHY.md` — **ACCEPTED** at `e35bb168f9b08300fac23bfc4148c3bbfa2a9874`.

`tasks/WEB-HERO-001C_AOI_SCAN_SYSTEM.md` — **ACCEPTED / TERMINAL_PRODUCT_ACCEPTANCE** at `6593a80`.

`tasks/WEB-HERO-001D_PREDATA_ANIMATIC_GATE.md` — implemented, `REVIEW_READY`, awaiting review.

WEB-HERO-001D is the last phase of the pre-data lane. Nothing further starts on this branch without
a new published task. Acceptance of this phase makes the scene an input to the later real-data hero
phase and the `WEB-005` integration and release gate; it does **not** authorize live hero
integration, production media packaging, deployment or DNS work.

## WEB-HERO-001D outcome

`hero_predata_animatic` is the assembled pre-data sequence: **Earth establish, satellite entrance,
AOI acquisition and scan, continuous camera approach, stable regional AOI hold**, 240 frames at
24 fps (10.0 s), as one scene and one uncut camera move. It `extends` the accepted Phase-C scene, so
the Earth, satellite, starfield and the whole surface-conforming AOI system are consumed rather than
redesigned; the three accepted scene definitions are byte-identical in `scene.json` to the versions
accepted at `6593a80`.

Phase D did three kinds of work.

**Assembly and timing.** Frames 1-96 replay the three accepted Phase-B establish camera states
verbatim, re-timed onto a beat map that starts acquisition earlier so the sequence can end on a real
1.7 s regional hold. That hold is where the later phase injects real layers.

**Closing the accepted Phase-C quality gate.** The 2048 px albedo was replaced by the 8192 px member
of the same already-cleared NASA Visible Earth record, dropping texture magnification at the
closest approach from about 14x to 3.9x. The atmosphere was rebuilt from the physical parameter that
actually governs limb brightness - the perigee altitude of each view ray - and made additive rather
than a mix, so it no longer ends on a hard edge and no longer paints over the sky at regional
scale. Beam and footprint appearance were judged on Cycles, not EEVEE.

**Making the cinematography claims measurable.** The camera path is derived from the AOI by
`hero/scripts/shot_plan.py` from a committed `shot_intent`, and the validator re-derives it and
fails on drift. The camera's aim is held by a keyframed Track To constraint on the AOI centre rather
than by hand-matched keyframes, so registration is exact between keys and not only at them.
`hero/scripts/audit_shot.py` measures the evaluated camera every frame and turns the continuity
contract into eight numbers, all passing: AOI centre lock 0.0 frame widths, worst apparent-size
reversal -0.000276, worst orientation step 0.215 deg/frame, camera jerk ratio 0.137, lens rate
0.206 mm/frame, cut ratio 2.48, zero frames with the AOI out of shot, headline-safe occupancy 0.0.

Phase-C geometry validation re-run on the new scene stays green: worst radial deviation 0.726 m,
worst beam tip error 2.249 m, beam root error 0.0 m, footprint edge spread 0.019 km. The secondary
fixture passes unchanged. `validate_hero.py` grew 117 to 151 checks and was verified against eight
deliberate regressions, all caught.

Reproducibility of the accepted phases was proven by extracting the Phase-C tree whole from
`6593a80` and rendering it in the same session as the current tree, with an
accepted-versus-accepted control: every difference sits at the renderer's own noise floor.

Evidence under `hero/evidence/`: six Cycles stills at the named beats, a 16-frame Cycles continuity
sheet, both AOI geometry audits, the shot audit, the shot-plan framing report, the reproducibility
record and the animatic pointer with its SHA-256. The 4.8 MB animatic itself stays out of Git by
lane policy.

No fabricated scientific layer, no real-data visualization, no homepage integration, no production
media packaging, no deployment and no DNS change.

## WEB-HERO-001A outcome

The `hero/` workspace is a reproducible Blender production environment. Configuration under
`hero/config/` is the source of scene truth: `lane.json` pins the lane boundary and protected
public-site paths, `scene.json` holds the palette, camera defaults, scene definitions and the AOI
data-injection interface, and `render_profiles.json` holds the render profiles, the 16:9 aspect
contract and the GPU preference order.

Blender-Python entrypoints under `hero/scripts/` build a scene from configuration, render a fast
preview, render a bounded high-quality still, run the whole benchmark in one session and record the
environment. `validate_hero.py` runs without Blender and is the workspace contract checker.

Measured on this machine — Blender 4.5.10 LTS, embedded Python 3.11.11, Cycles on OptiX with an
NVIDIA GeForce RTX 4070 Laptop GPU, warm shader cache:

| profile | engine | resolution | samples | device | wall clock |
| --- | --- | --- | --- | --- | --- |
| `preview` | EEVEE Next | 1280×720 | 32 | Blender GPU context | 1.68 s |
| `master` | Cycles | 1920×1080 | 256 + OptiX denoise | OptiX / RTX 4070 | 4.72 s |
| `evidence_still` | Cycles | 1280×720, 8-bit | 256 + OptiX denoise | OptiX / RTX 4070 | 1.97 s |

The benchmark is production-planning data on a neutral test scene, not a quality target and not
hero art direction. The first EEVEE render of a cold session cost about 31 s in shader compilation;
steady-state iteration is the number above.

`hero/assets/manifest.json` declares the rights policy and an empty asset list: the benchmark scene
is fully procedural, so WEB-HERO-001A introduces no external asset. No scientific layer exists in
this lane, and the validator fails if one is declared while the lane is pre-data.

Do not implement 001C/001D before the predecessor output required by their contracts exists and the task progression condition is satisfied.

## WEB-HERO-001B outcome

The `hero_earth_orbit` scene (`hero/config/scene.json`) is a true-3D-geometry establishing sequence:
Earth (a 256×128-segment sphere), a Fresnel-driven atmosphere shell, a procedural Voronoi
starfield, and a procedurally-modelled Earth-observation satellite (bus, twin solar panels, a
nadir dish, an instrument boom) on a keyframed orbital-entrance path. `build_scene.py` gained
image-textured materials, a compound `satellite` object type, and object/camera keyframe
animation, all still declarative in `scene.json`.

The Earth material blends a NASA Blue Marble day/cloud composite against a NASA Black Marble
night-lights composite through a terminator factor — `dot(normal, fixed_sun_direction)` computed
once at shader-build time from the scene's own authored sun light — so lighting is stable
regardless of texture placement. Longitude placement uses a Mapping-node **translation** on the
U axis (Repeat wrap); an initial rotation-based approach silently folded the map near the UV seam
and was replaced.

A `world_coordinate_convention` block in `scene.json` is now the shared frame for every later
phase: 1 Blender unit = 1000 km, Earth centred at the world origin, world +Z is Earth's rotation
axis, and longitude 0°/latitude 0° sits on +X at frame 1 of `hero_earth_orbit`. The satellite's
`TRACK_TO` constraint keeps it nadir-pointing at Earth across the whole path without per-frame
orientation math, so Phase C/D can extend the same camera/object path without a scene reset.

Two NASA public-domain Earth composites are recorded in `hero/assets/manifest.json` with source
URL, publisher, license and SHA-256 (`land_ocean_ice_cloud_2048.jpg`,
`dnb_land_ocean_ice.2012.3600x1800.jpg`); the satellite, atmosphere and starfield remain fully
procedural and introduce no further external asset. Three representative Cycles stills
(establish / satellite-entrance / pre-acquisition) are committed under `hero/evidence/`.

No AOI footprint, scan geometry or scientific layer was introduced. The Phase A benchmark scene
and validator (81 checks) were re-run clean after these changes.

**Visual-acceptance revision (2026-09-16):** satellite no longer casts a shadow onto Earth (read as
a stray planning-marker in review); satellite hull/panels gained a shared Fresnel rim-light for a
cleaner hero-scale silhouette; the atmosphere rim is thinner and now scales with the same
sun-direction term the Earth terminator uses, instead of glowing at a uniform detached strength;
the starfield is two brightness-varied Voronoi layers plus a faint large-scale depth drift instead
of one uniform-threshold layer. No composition, geography, camera-path or scope change; the three
representative stills were re-rendered and replaced. See `CHANGELOG.md`.

## WEB-HERO-001C outcome

**Implementation HEAD:** `9a79a03e742d007b8abba2e4c6ec572e20df0155`

The `hero_aoi_acquisition` scene `extends` the accepted `hero_earth_orbit` rather than copying it,
so the Earth/atmosphere/satellite/starfield/lighting system has exactly one definition. Frames
1–120 reuse the WEB-HERO-001B camera keyframes verbatim and the shot continues, in one move, to
frame 240 through acquisition and regional approach. `hero_common.resolve_scene_spec` performs the
inheritance and holds no `bpy` import, so the validator resolves exactly the scene the renderer
builds.

`hero/scripts/aoi_system.py` owns all AOI geometry and, like the resolver, imports no `bpy`, so
the validator checks the same numbers the renderer uses. Corners come from the spherical
destination formula applied to the configured centre, span and bearing; edges and the interior are
sampled by slerp between unit vectors and scaled by one radius, so conformance to the sphere is
true by construction rather than by tuning. Border and corner-lock ribbons widen by rotating each
sample within its own tangent plane, keeping both rails on the sphere. Measured worst-case radial
deviation across the built scene is 0.68 m on a 6 371 km radius — single-precision transform
error, not approximation.

Registration is structural, not keyframed. The AOI is parented to the Earth, so footprint, corner
locks and per-corner target empties ride the globe's rotation. Each beam is a unit-length tapered
tube driven by a Copy Location constraint on the satellite and a Stretch To constraint on its
corner empty, so a beam endpoint is *derived* from the AOI at every frame instead of being a
constant that happens to match on one; measured tip-to-corner error stays at 2.2 m on beams up to
11 000 km long. The scan sweep is a band in the interior mesh's own AOI-local UV space, so it
cannot detach from the surface. The validator rejects any literal coordinate inside an
`aoi_system` spec for the same reason.

Configurability is a contract, not a demo: `aoi_injection_interface` ships two design fixtures
differing in centre, hemisphere, span (420 km / 700 km), bearing (0° / 25°) and sampling density,
and `--aoi-fixture` switches any build or render entrypoint between them with no code change.
`hero/evidence/hero_aoi_fixture_comparison_f130.png` shows the same scene at the same frame with
only the fixture config changed.

`hero/scripts/audit_aoi.py` measures the built scene in world space per frame; both fixtures pass
all five checks. `validate_hero.py` grew from 81 to 117 checks and was verified against nine
deliberate regressions, each of which it caught.

The atmosphere shell gained an optional `silhouette_fade_start`, off unless a scene asks for it:
WEB-HERO-001B never flew close enough for the shell's hard outer edge to show, and at Phase C
approach distances it became a straight-edged wedge across frame. `hero_earth_orbit` does not set
it and rebuilds unchanged.

Pre-data throughout. Both fixtures are neutral design placeholders carrying no measurement
meaning; the footprint interior shows only a faint cyan wash, a denser already-swept region and
the sweep band, with no legend, scale or classification. No new external asset was introduced —
the whole AOI system is procedural. No public-site, imagery, deployment or DNS change.

**Known limitation carried to WEB-HERO-001D:** the Phase B Earth albedo map is 2 048 px wide, so a
420 km footprint spans roughly 27 texels and the surface is visibly soft at the closest approach.
The approach was moderated rather than swapping the accepted Phase B texture. A higher-resolution
NASA Blue Marble composite is the fix, and it belongs with Phase D's quality gate.

Phase graph:

`WEB-HERO-001A / MER-98` → `WEB-HERO-001B / MER-99` → `WEB-HERO-001C / MER-100` → `WEB-HERO-001D / MER-101`

All phases stay on this branch unless Product publishes a revision.

## Locked lane boundaries

- New production source belongs under `hero/` except bounded authority/status/ignore updates explicitly needed by the task.
- Do not modify `index.html`, `styles.css`, `script.js`, public proof imagery, Vercel/deployment configuration, DNS or production-domain state.
- Earth must be true 3D spherical geometry.
- Future AOI geometry must conform to the sphere; no flat pasted screen-space rectangle.
- Future scan beams/corner locks must register to the actual 3D AOI footprint.
- Global → acquisition → regional approach must preserve one AOI identity/orientation/scale continuously.
- Acquisition palette is restrained cyan / ice-blue / teal over deep navy/black.
- Do not fabricate DEM, thermal, alteration, fault, geology, structure, score/prospectivity or other scientific output.
- External production assets require explicit rights/provenance/checksum discipline under `hero/assets/manifest.json`.
- Paid/unclear-rights assets, credentials/admin, destructive action or commercial commitment are human gates.

## Parallel website state and checkout safety

The primary website workstream continues independently on its own branches. WEB-002 product-proof work may proceed in parallel. This hero branch must not absorb or merge that work merely to stay current.

If the ordinary repository checkout is currently occupied by WEB-002 or another Claude Code session, **do not switch/reset/clean that active checkout** to start WEB-HERO-001. Use a separate Git worktree or equivalent isolated checkout for `feat/web-hero-001-predata-scene`. Creating and maintaining that bounded worktree is routine implementer-owned Git hygiene, not a Product STOP.

## Terminal phase state

For WEB-HERO-001A, implement and revise within scope through `REVIEW_READY`, then report exact branch/HEAD, changed paths, commands/tool versions, validation, benchmark/render evidence, rights manifest status and known limitations. Routine Blender/Python/tooling/render issues are implementer-owned and are not Product STOPs.
