# WEB-HERO-001C — Surface-conforming AOI acquisition & scan system

**Linear:** `MER-100` (parent `MER-97`)  
**Blocked by:** `MER-99 / WEB-HERO-001B`  
**Authority:** `docs/WEB_HERO_001_AUTHORITY.md` + Drive CURRENT Hero Visual & Production Authority v1.0  
**Branch:** `feat/web-hero-001-predata-scene`  
**State:** `REVIEW_READY`  
**Predecessor:** `WEB-HERO-001B` accepted at `e35bb168f9b08300fac23bfc4148c3bbfa2a9874`  
**Implementation HEAD:** `9a79a03e742d007b8abba2e4c6ec572e20df0155`

## Outcome

Implement the signature acquisition interaction so the target area looks physically attached to Earth and genuinely acquired by the satellite: configuration-driven spherical AOI geometry, surface-conforming border, restrained corner locks, 3D scan beams and a surface-following scan sweep that remains registered under the continuous camera move.

This phase exists specifically to eliminate the AI-generated look of a flat quadrilateral pasted over a globe.

## Geometry contract — hard requirement

The AOI must be generated from geographic-style coordinates/configuration and mapped onto the Earth sphere in world space.

Required behavior:
- AOI corner positions lie on the sphere at the configured Earth radius plus a very small visual offset only to prevent z-fighting;
- each boundary edge is sampled/interpolated densely enough to follow globe curvature rather than drawing a straight 3D chord or screen-space line;
- the interior footprint, if rendered, conforms to the same spherical surface;
- AOI geometry remains correct when Earth rotates, the camera changes position/focal length and the shot moves from global to regional scale;
- implementation exposes a clean data/config interface so a later real AOI can replace the design fixture without code surgery.

A flat plane hovering over Earth, a composited 2D rectangle, or a quadrilateral whose edges visibly detach from the globe is an acceptance failure.

## Acquisition system

Build a restrained acquisition language with:

- satellite-to-AOI beam geometry in actual scene/world coordinates;
- beams that visually resolve to the footprint/corner region rather than a random Earth center point;
- four subtle corner-lock nodes or equivalent acquisition markers attached to the footprint;
- a surface-following scan sweep/pulse across the AOI after lock;
- controlled cyan / ice-blue / teal emission and bloom;
- optional subtle volumetric scattering only where it improves readability without turning the scene into a laser spectacle.

The animation may stylize remote sensing for comprehension; do not imply literal sensor-beam physics or add public claims.

## Continuity contract

Use the Earth/satellite/camera scene established in Phase B. The AOI target used for global acquisition and regional approach is one persistent object/system with one identity.

The transition must prove:
- no AOI recentering jump;
- no rotation/orientation swap;
- no artificial scale reset;
- no cut to a separately generated map panel;
- beam endpoints/corner locks remain registered until the narrative intentionally releases them.

## Neutral interior only

Until the real-data hero phase, the AOI interior may show only a neutral, clearly non-scientific treatment needed to communicate scan progress (for example a transparent cyan glass/fill, procedural grid-free sweep, or subtle illumination of existing Earth texture).

Forbidden here:
- synthetic DEM/elevation colors;
- heatmap/prospectivity gradients;
- fake faults/structures;
- fake thermal/alteration patterns;
- scientific labels or legends.

## Automated validation

Extend the scene validator with deterministic checks where practical, including:

- AOI vertices/ring points lie within a defined tolerance of the configured spherical radius/offset;
- boundary sampling count/density is sufficient for the configured shot scale;
- all four configured corners resolve to scene objects/coordinates;
- beam target endpoints reference the AOI system rather than arbitrary constants;
- AOI configuration can be changed to a second test fixture without rebuilding code paths;
- no prohibited scientific-layer asset/config appears in the phase.

Do not attempt to mathematically validate subjective visual quality; provide rendered evidence for that.

## Out of scope

- real OrbGSS scientific layers;
- final analytical color palette applied to data;
- web video encoding;
- homepage integration;
- production performance budget acceptance.

## Acceptance

Phase C is complete only when:

1. AOI border and any fill visibly conform to Earth curvature at global, acquisition and regional-approach views.
2. Geometry validation confirms the AOI sits on the configured sphere within the chosen tolerance.
3. Satellite scan beams/corner locks target the actual AOI 3D system and remain registered during motion.
4. A scan sweep travels across the footprint without detaching from the surface.
5. Changing the design AOI configuration to a second fixture proves the system is configurable rather than hand-modelled for one shot.
6. The same AOI identity/orientation is preserved from acquisition through approach.
7. Review stills/video contain no fake scientific layer content.
8. Phase A/B build and render paths remain reproducible and green.

## Verification / evidence

Report at `REVIEW_READY`:

- exact branch/HEAD and changed paths;
- AOI configuration schema/example(s);
- validation command/results including sphere-distance/tolerance checks;
- representative global, acquisition and closer regional stills showing curvature;
- short preview showing beam lock + scan sweep + beginning of approach;
- evidence that a second AOI config works without code restructuring;
- render settings/tool versions and relevant evidence hashes/pointers;
- confirmation that no fake science or public-site integration was introduced.

## STOP / route

Route to Product if the locked surface-conforming AOI or continuity behavior cannot be achieved without changing the approved visual concept, or if a new runtime/dependency architecture is required.

Route to Science only if someone attempts to attach semantic meaning to the design AOI or asks for real analytical layers before later authority.

Human gate for paid assets/services, credentials/admin, destructive action or commercial commitment.

Routine geometry math, coordinate conversion implementation, sampling density tuning, shader/beam tuning, keyframe work, validator implementation and conformant visual iteration are implementer-owned.

## Branch policy

Continue on `feat/web-hero-001-predata-scene`; no main work or force push. Terminal state `REVIEW_READY`. `WEB-HERO-001D` begins from this phase's accepted acquisition system.