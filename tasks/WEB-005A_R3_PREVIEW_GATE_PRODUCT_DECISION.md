# WEB-005A R3 Preview Gate — Product Decision

**State:** PREVIEW_GATE_REVISION_REQUIRED / CONTINUATION_AUTHORIZED  
**Parent:** WEB-005A / MER-107  
**Reviewed preview:** `feat/web-005a-hero-visual-fidelity@cd2018e011c4f547c74495cd06ca5c7a833d14f6`  
**Preview evidence:** `tasks/WEB-005A_R3_PREVIEW_GATE.md`  
**Parent authorities:**  
- `946cd8b5795c86cbeef52f650ee432b8fcd8fd2e:tasks/WEB-005A_R3_FIXED_CAMERA_GLOBE_DRAPE_REVISION.md`
- `db4605abcb35be9ab0337deb6b15c80aab79b12b:tasks/WEB-005A_R3_ANALYTICAL_ASSET_HANDOFF.md`
- `473b48a00bfe85d3dbe1cfe7219105c2b5ec7574:tasks/WEB-005A_R3_REVIEW_37152222.md`

This decision resolves the Product questions raised by the low-cost preview. It does not authorize a long production render yet. The preview architecture is substantially closer to the required result and should be preserved, but two semantic defects and the final motion gate must be corrected before promotion.

## 1. Accepted preview findings to preserve

The following preview decisions are accepted and should not be reopened without a concrete regression:

- fixed observer through scan: camera motion begins only after acquisition FX retire;
- integrated-page acquisition composition places the satellite clear of the 1440-class copy column without changing copy/CSS;
- four-line + translucent fan + left-to-right sweep is the accepted scan language;
- fan/beam retirement before post-scan camera motion;
- one visually persistent adaptive lock presentation rather than an abrupt regional-frame -> analysis-frame swap;
- DEM-derived relief from governed `top-dem.tif`, 3x presentation exaggeration, one common mapping/UV for Terrain, THM-01, ALT-01 and Priority;
- layer order Terrain -> THM-01 -> ALT-01 -> Priority and Priority-only final hold;
- lossless page-layer delivery remains preferred over baking governed thematic pixels into lossy hero video.

The current preview remains low-cost evidence only; none of these statements promote its scene to production by themselves.

## 2. Decision 1 — four primary beams MUST terminate at the true governed AOI corners

The preview's current beam target is not accepted for production.

The four primary beams currently terminate at the corners of a 544 km presented lock frame, approximately 15.1x the true 36 km AOI. That is a presentation reticle, not the governed AOI footprint. Canonical A-HERO-16 and the explicit Product boundary require the four primary lines to terminate at the true authoritative AOI corner positions.

Required correction:

- `beams.anchor` must resolve to the four true governed 36 km AOI corners under the same deterministic globe projection used by the relief/layers;
- no decorative enlargement or scaled-diagonal substitute may be used as a primary beam endpoint;
- the true beam endpoints remain fixed while beams are attached.

The visibility problem must be solved without falsifying the target.

Accepted visual mechanism:

- keep a larger **presentation/acquisition reticle** centered on the true AOI if needed for screen readability;
- treat that reticle explicitly as screen-space presentation, not as the AOI footprint;
- the reticle may tighten continuously during the post-scan approach and converge onto the true AOI frame;
- the true AOI itself remains the authoritative ground intersection throughout.

For the scan effect, the semi-transparent fan/light curtain may remain visually broad in space while its ground intersection is governed by the true AOI. A moving volumetric curtain can remain legible even when the global-view AOI is only a few pixels wide; no 544 km fake ground footprint is required.

This preserves the user's desired premium scan language and the scientific/geometric truth simultaneously.

## 3. Decision 2 — use lossless page-composited drape states; do NOT waive the lossy-video invariant

Approved delivery architecture:

1. hero video carries Earth -> satellite -> four-corner lock -> scan -> retire -> post-scan approach;
2. the video settles on one deterministic held camera/geometry state;
3. Terrain, THM-01, ALT-01 and Priority are delivered as losslessly encoded rendered drape states aligned to that exact held geometry;
4. the page cross-fades the lossless states in order;
5. the final state holds Priority only;
6. exact labels, warnings and legend remain HTML/page content where required.

No Product waiver is granted to bake governed THM/ALT/Priority pixels into a lossy WebM/MP4.

The rendered states must still read as relief/globe-surface analysis, not flat cards. They may be transparent/lossless overlays or full held-frame lossless composites, provided registration is exact and there is no visual jump.

## 4. Decision 3 — the website-hero palette is already resolved by MER-108; do not use batlow for the hero Priority layer

There is no remaining Science palette decision here.

Canonical Science authority:
`mertkaanakgunlu-debug/geothermal-prospectivity@30779547ced0cbf047cb51fb6c2c6ed178547d56:tasks/MER-108_TERMINAL_WEBSITE_HERO_DISPLAY_AMENDMENT.md`

For `website_hero_public_presentation`, the accepted Priority topology is:

**deep purple -> red/orange -> yellow, low -> high**

Therefore:

- the prepared purple/orange/yellow Priority direction is the correct hero direction;
- the older batlow public derivative is not the hero palette authority;
- the hero legend must be regenerated/matched to the terminal hero palette, not vice versa;
- exact ordered stops/LUT and LUT checksum must be frozen in the derivative build manifest before production acceptance.

The current preview textures are not automatically publication-conformant merely because their direction looks correct. If their exact build parameters/stops/checksums cannot be reconstructed inside MER-108's bounded pipeline, regenerate them deterministically from the governed MER-113 rasters. No Science re-entry is required for conforming regeneration.

### Colour fidelity at the draped surface

Do not allow scene lighting/AgX to materially shift thematic colours away from the approved hero LUT while presenting a matching legend.

For THM-01, ALT-01 and Priority, use a colour-faithful/unlit or otherwise verified render path so the final lossless page asset remains within a small, documented colour tolerance of the approved display derivative. Relief geometry may provide shape/perspective, but thematic value-to-colour meaning must not be re-authored by scene lighting.

## 5. Decision 4 — the ~50–56 m globe-projection residual is accepted as bounded presentation projection

The reported common-mode residual between WGS84/grid corners and the accepted 6371 km spherical hero fixture is acceptable for this cinematic surface because:

- the governed scalar grid/CRS/geotransform are unchanged;
- frame, relief and every layer use the same deterministic mapping;
- there is no layer-to-layer drift;
- the residual is under two 30 m cells and approximately 0.7 px at the hold.

Do not edit scientific source geometry to remove it.

However, all beam endpoints, relief, true AOI outline and thematic layers must use the same authoritative projection path. The accepted residual does not authorize the 544 km presentation-reticle endpoints rejected in §2.

## 6. Decision 5 — current planned satellite exit envelope is too large

The preview reports an estimated satellite silhouette of roughly 0.29 frame widths during the lower-left exit.

That is outside the established no-foreground-fly-by envelope used by WEB-005A (approximately 22% maximum frame width). It is not accepted for production even before subjective motion review.

Required correction:

- preserve the accepted acquisition position/readability;
- once scan is complete, shape the first approach segment so the satellite exits without exceeding the existing foreground/fly-by bound;
- prefer more optical zoom / less forward dolly early in the approach, or an equivalent conforming orbit/camera solve;
- the satellite may naturally leave frame after acquisition, but it must not become a large foreground object or steal attention from the AOI transition.

Target: <= 22% frame width through the intentional exit, with the transition visually subordinate to the AOI.

## 7. Decision 6 — final analytical payoff must be protected from the left readability shade

The current unchanged shade still reaches the left edge of the settled AOI/score surface.

For the final analytical reveal:

- preserve the dark treatment behind the left copy;
- taper/clip/state-shift the shade so it no longer materially darkens the governed thematic surface;
- avoid a hard boundary; use a controlled feather between copy-safe and analysis-safe zones;
- the score palette/legend must not be visually altered by a page gradient.

This is bounded page-compositing work inside WEB-005A and does not reopen homepage layout.

## 8. Decision 7 — timing envelope

The 17.5 s preview exists for review and is not the shipping duration.

Production target:

- rendered motion section: approximately 11.5–12.5 s;
- lossless analytical sequence after the settled hold: approximately 2.4–3.2 s total for Terrain -> THM-01 -> ALT-01 -> Priority;
- Priority then remains as the stable final hold.

Exact easing/dwell remains implementation-owned, but do not turn the four analytical states into a slow slideshow.

## 9. Required second low-cost motion preview before production render

Do not promote to the production scene yet.

Produce a corrected low-cost animatic using the same preview lane with:

1. true governed AOI beam endpoints;
2. presentation reticle clearly separated from true ground geometry;
3. translucent fan + left-to-right sweep;
4. retirement before camera motion;
5. continuous adaptive reticle tightening;
6. corrected satellite exit <= established fly-by bound;
7. fixed held camera/relief state;
8. lossless-render concept for Terrain -> THM -> ALT -> Priority;
9. Priority-only final hold with analysis-safe page shading.

Submit both:
- the motion animatic;
- 1440x900 real-page composites at beam lock, mid-scan, first approach, and final Priority hold.

Product/CTO will judge motion continuity, fan aesthetics, reticle tightening and satellite exit from that animatic. The still/numeric gates alone cannot terminally pass those motion qualities.

**Continuation:** existing MER-107 execution authority remains active. No new CTO start is required. No long production render until this corrected preview is visually accepted.
