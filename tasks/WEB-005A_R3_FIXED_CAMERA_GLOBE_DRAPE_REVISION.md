# WEB-005A R3 — Fixed-Camera Acquisition & Globe-Draped Analytical Reveal

**State:** EXECUTION_AUTHORIZED / REVISION_REQUIRED  
**Parent:** WEB-005A / MER-107  
**Implementation branch:** `feat/web-005a-hero-visual-fidelity`  
**Current published R2 checkpoint:** `a6897828d6e35595ea5a9a39a1e812b0fcbbfb35`  
**Purpose:** supersede ambiguous camera/handoff interpretation from earlier WEB-005A authority without discarding conformant Earth, orbit, satellite, provenance, media-budget, fallback, validator or evidence work.

## 1. Outcome

Deliver one coherent hero sequence in which the viewer is a stationary observer until acquisition completes; the satellite alone moves into a readable orbital acquisition composition; four beams lock the real AOI corners; the AOI scans; only then does the camera smoothly approach the same AOI; real OrbGSS analytical outputs appear sequentially as globe-surface overlays inside the AOI; the final hold shows only the Score layer draped on the Earth inside the AOI.

This R3 authority supersedes any prior interpretation that permits early camera motion, a detached result-card payoff, or analytical layers presented as free-floating flat panels.

## 2. Locked sequence

### Phase A — fixed observer

Until the scan is complete, the camera is fixed in world/screen-space intent. No camera pan, orbit, dolly, zoom, target recentering or lens animation may create apparent observer motion.

The viewer should read as a stationary observer watching the Earth while the satellite moves.

### Phase B — satellite orbital entry

The satellite must emerge from behind the left-rear/left-limb of the Earth, become progressively visible, and move along an orbital-looking path toward the foreground acquisition position.

At the acquisition hold it settles slightly left of frame centre / left-centre, while Earth remains the dominant object. It must remain readable as a volumetric generic EO platform and must not clip during the primary acquisition beat.

### Phase C — four-corner acquisition

The satellite emits exactly four primary visible cyan sensing lines, each terminating at one of the four governed AOI-corner positions. Additional subtle support glow/trail may exist but cannot replace or obscure the four-corner read.

The four corner targets must come from the same governed AOI geometry used by the application/data package; no hand-placed decorative corner substitution.

### Phase D — AOI lock and scan

A neon AOI frame forms around the true AOI footprint using the accepted cyan language. The frame must visually acquire/lock: corner marks resolve, core line brightens, controlled glow appears, then a scan pass traverses the AOI.

The camera remains fixed throughout lock and scan.

### Phase E — smooth camera approach

Only after scan completion does the camera move.

The camera performs a smooth continuous zoom/dolly toward the same AOI. The satellite naturally exits the composition during this approach. There must be no unrelated cut or generic map jump.

The AOI must resolve to the **right-middle visual zone** of the hero frame so the left-side copy/readability area does not overlap the analytical target.

### Phase F — globe-draped analytical reveal

After the approach, show the real application outputs sequentially inside the true AOI footprint:

1. DEM
2. Thermal / THM-01
3. Alteration / ALT-01
4. Score / `mvp_remote_sensing_priority_v1`

Each analytical layer must be geospatially registered to the AOI and perspective-aligned/draped onto the visible Earth/globe surface. A detached flat UI card, floating 2D raster panel, billboard, or unrelated rectangular screenshot is not a conforming analytical reveal.

Transitions may crossfade or blend between layers, but the viewer must clearly understand that the same physical AOI is being analysed layer by layer.

### Phase G — final score-only hold

At the end, DEM, Thermal and Alteration are no longer visible. Only the governed Score layer remains inside the AOI on the globe surface, with the AOI/frame treatment settled around it. This score-on-globe state is the hero final hold/payoff.

A small detached result card may exist only as secondary supporting UI if later Product authority allows it; it cannot be the hero payoff and cannot obscure the AOI.

## 3. AOI geometry and data extent

The rendered AOI must correspond to the real data footprint. Visual convenience does not authorize moving the target.

If the current 36 km analytical extent is too small to produce a legible globe-draped reveal, implementation may either:

- adjust camera framing/target-box presentation while preserving the exact real AOI footprint; or
- request/materialize a **larger real analysis/data extent** through the existing application workflow and render that larger truthful footprint.

A larger extent must retain exact provenance, source/output identifiers, CRS/grid/units/NoData/mask/resampling/scoring semantics and must not invent or extrapolate unavailable values. If producing the larger extent requires a new scientific method or changes scoring semantics, route to Science instead of improvising.

## 4. Hero composition and text-safe zone

The hero remains a full-bleed visual panel. The left side must carry a controlled dark gradient/readability treatment for the existing hero copy.

During the post-scan approach and analytical reveal, the AOI/score payoff must remain in the right-middle zone and clear of the left copy block.

This same full-bleed-visual + left readability-gradient direction is also the Product target for lower homepage gallery/visual panels and should be consumed by WEB-005B; WEB-005A must not implement unrelated lower-panel redesign.

## 5. Real analytical assets

The R3 reveal must use real, governed OrbGSS outputs. Do not create illustrative/fake DEM, Thermal, Alteration or Score textures for production.

If current output derivatives are not suitable for globe draping, derive presentation-safe texture assets from the governed outputs without changing value semantics. Preserve checksums/provenance and exact mapping/legend authority.

Scientific value-to-colour remapping remains Science-gated. Presentation geometry, alpha, masking and perspective projection are Product/implementation concerns only when they preserve governed pixel/value meaning.

## 6. Reference-image policy

CTO-provided/generated reference images accompanying the execution prompt are **visual choreography/composition references only**. They establish:

- fixed-camera early phase;
- left-rear satellite emergence and left-centre settle;
- four-corner beam geometry;
- right-middle AOI placement;
- neon lock/scan language;
- curved/globe-surface analytical drape;
- score-only final hold;
- left-side text-safe darkening.

They are not production assets, not scientific data, not exact geography, and must not be copied into the site.

## 7. New R3 acceptance gates

### A-HERO-15 — fixed-camera pre-scan gate

Camera transform/lens/target evidence proves no intentional camera motion from Earth establish through completion of AOI scan. Visual before/after frames must show observer framing continuity while satellite motion changes.

### A-HERO-16 — four-corner acquisition gate

Production/preview evidence shows exactly four primary satellite→AOI lines terminating at the four governed AOI corners. Corner coordinates/scene anchors must be derived from authoritative AOI geometry and be validator/audit visible.

### A-HERO-17 — right-middle AOI composition gate

After camera approach, AOI bounding region occupies the right-middle visual zone and does not overlap the left hero copy-safe region at 1440-class review width. Responsive fallback may differ, but desktop hero must satisfy this composition.

### A-HERO-18 — real globe-drape sequence gate

Evidence proves the production reveal uses real governed DEM → Thermal → Alteration → Score outputs, geospatially registered and projected/draped onto the globe/AOI surface. Detached-card-only or flat billboard presentation fails.

### A-HERO-19 — score-only final hold gate

Final hero state shows only the governed Score layer inside the AOI on the globe surface; DEM/Thermal/Alteration transition layers are no longer visible. Final state remains readable and stable long enough to function as the hero hold.

## 8. Preview-before-render requirement

Before any new long production render, produce low-cost preview/still evidence for Product/CTO showing all of the following in one coherent sequence:

1. fixed-camera Earth establish;
2. satellite emerging from the left-rear/limb and settling left-centre;
3. four beams reaching all four AOI corners;
4. neon AOI lock + scan while camera remains fixed;
5. first post-scan camera-approach frame with AOI moving into right-middle composition;
6. DEM draped on globe;
7. Thermal draped on globe;
8. Alteration draped on globe;
9. Score draped on globe;
10. score-only final hold.

Do not spend the full production-render budget until these preview gates are visually coherent.

## 9. Preserve existing WEB-005A contracts

Unless superseded above, all prior WEB-005A constraints remain binding, including:

- accepted Earth quality/provenance work;
- rights-safe generic EO satellite identity;
- scientific/public semantic non-change;
- WebM/MP4/poster ceilings;
- reduced-motion/reduced-data/mobile fallbacks;
- no dual-video download;
- EN/TR/accessibility/route invariants;
- no production deploy/DNS/WEB-006;
- full evidence and validator truthfulness.

**Terminal state remains:** `REVIEW_READY`, followed by Product/CTO human visual acceptance.