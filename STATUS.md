# OrbGSS Website — WEB-HERO-001 branch status

**Date:** 2026-09-15  
**Branch:** `feat/web-hero-001-predata-scene`  
**Baseline:** accepted canonical `main@677bfa7672ac18c2c808ddaaf235ff12863de443`  
**Authority-publication HEAD before implementation:** `0e572e9cfd1709a4e3eb6d3ca110390c79cc6668`  
**Stage:** `WEB-HERO-001B — REVIEW_READY` (Earth/space/satellite/orbit cinematography implemented; WEB-HERO-001A accepted)  
**Tracking:** parent `MER-97`; active phase `MER-99`  
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

`tasks/WEB-HERO-001B_EARTH_SATELLITE_CINEMATOGRAPHY.md` — implemented, `REVIEW_READY`, awaiting review.

`WEB-HERO-001C` may start once this phase's accepted scene state is confirmed.

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
