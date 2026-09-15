# WEB-HERO-001B — Earth, space, satellite & orbit cinematography

**Linear:** `MER-99` (parent `MER-97`)  
**Blocked by:** `MER-98 / WEB-HERO-001A`  
**Authority:** `docs/WEB_HERO_001_AUTHORITY.md` + Drive CURRENT Hero Visual & Production Authority v1.0  
**Branch:** `feat/web-hero-001-predata-scene`  
**State:** `BLOCKED_BY_WEB-HERO-001A`

## Outcome

Build the premium global cinematic foundation that establishes OrbGSS visually before any scientific layer appears: true 3D Earth, atmosphere/cloud/lighting treatment, deep-space background, realistic Earth-observation satellite, plausible orbital entrance and a continuous global camera composition that preserves useful headline-safe negative space.

## Locked composition

- Earth begins large on the right side of a 16:9 frame, with Africa / Europe / Mediterranean / Middle East legible enough to support the later target-area story.
- Left side retains intentional negative space for future HTML headline/CTA and for the satellite entrance.
- Space is near-black/deep navy with restrained star/nebula depth; avoid over-dense star wallpaper.
- Atmosphere uses controlled cyan/blue rim light, physically coherent with the Earth lighting rather than a detached neon outline.
- Earth rotation is slow and calm.

## Earth system

Implement Earth as actual spherical geometry and establish a high-quality material/lighting system suitable for later close regional approach. The exact texture sourcing strategy is implementer-owned provided it complies with asset rights/provenance policy and does not lock the project to a paid service.

Requirements:
- coherent day-side lighting and terminator/limb behavior;
- atmosphere visibly follows the globe;
- cloud treatment, if used, remains registered to Earth and avoids a flat pasted appearance;
- texture/material resolution is sufficient for the approved global shots and does not visibly collapse during the pre-data regional approach target of this lane;
- asset provenance/checksums recorded.

## Satellite system

Create or source a rights-safe Earth-observation satellite with restrained realism. Prefer owned/procedurally modelled geometry if it achieves the quality target.

Requirements:
- recognizably Earth-observation/sensing oriented rather than a generic sci-fi spacecraft;
- physically plausible relative scale in composition (small compared with Earth);
- solar panels/instrument body read cleanly at hero resolution;
- lighting/rim treatment matches the scene;
- no logos or misleading real-mission branding unless the asset is intentionally generic and rights-safe.

## Orbit and camera

- Satellite enters along a plausible orbital arc, ideally emerging from behind/around Earth or from the left depending on the strongest continuous composition.
- Orbital trail, if used, is faint and secondary.
- Camera path must be authored as the beginning of the same continuous path that Phase C/D will use for AOI acquisition and regional approach; do not create isolated beauty shots that cannot connect.
- Preserve a stable world coordinate convention and document it for the AOI task.

## Look-dev quality

Target a premium realistic-but-slightly-stylized geospatial intelligence aesthetic. The render may enhance contrast/saturation modestly for website impact, but avoid game-like bloom, lens flare overload, chromatic aberration gimmicks or neon HUD framing.

## Out of scope

- AOI footprint or scan beams beyond optional non-functional placement markers used only to plan framing;
- scientific data layers, heatmaps or terrain-analysis overlays;
- final regional analysis look;
- website integration/encoding/deployment.

## Acceptance

Phase B is complete only when:

1. Earth is unquestionably 3D and physically coherent from the approved global camera range.
2. Atmosphere/cloud/lighting remain attached to the globe under rotation and camera motion.
3. Satellite reads as a credible Earth-observation asset at hero scale and has complete provenance/ownership notes.
4. Satellite entrance/orbit motion is plausible and visually premium.
5. Global composition reserves usable left-side text space without making Earth feel cramped.
6. Camera/orbit setup is designed to continue into the Phase C/D AOI sequence without a scene reset.
7. Preview and high-quality still evidence demonstrate the look from at least: establishing frame, satellite-entering frame, pre-acquisition frame.
8. No fake scientific imagery appears.
9. Phase A validator/build path remains green.

## Verification / evidence

Report at `REVIEW_READY`:

- exact branch/HEAD and changed paths;
- asset manifest additions with rights/checksums;
- render engine/device/settings for review stills;
- three representative stills (establish / satellite entrance / pre-acquisition) with hashes/pointers;
- short viewport or low-cost preview of Earth rotation + satellite entrance when practical;
- camera focal length / keyframe range / scene scale convention summary;
- confirmation of no site integration/scientific-layer changes.

## STOP / route

Route to Product only if achieving the approved look requires a materially different narrative/composition, new paid/third-party dependency, or a change that would compromise later continuous AOI approach.

Human gate for paid/licensed assets, credentials/admin, destructive action or commercial commitment.

Routine modelling, shader/light tuning, texture optimization, camera path refinement, Blender performance fixes and conformant look-dev iteration are implementer-owned.

## Branch policy

Continue on `feat/web-hero-001-predata-scene`; no main work or force push. Terminal state `REVIEW_READY`. `WEB-HERO-001C` begins from this phase's accepted scene state.