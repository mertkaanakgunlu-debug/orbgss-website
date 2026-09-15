# OrbGSS Public Visual Narrative & Palette Authority

**State:** CANONICAL PRODUCT DECISION — 2026-09-15  
**Owner:** Product & Software  
**Repository:** `mertkaanakgunlu-debug/orbgss-website`  
**Authority role:** downstream presentation authority for the website/hero workstream. This file does **not** reopen or change the active `WEB-HERO-001A` implementation scope.

## 1. Current WEB-002 map status

The current WEB-002 maps are **real OrbGSS application outputs**. They are not illustrative or fabricated maps.

Their current scientific/technical palettes are valid for analytical proof, but they are **not** the final public-facing visual palette.

Later public presentation may re-render/re-export the same accepted outputs with a more visually compelling palette only if the underlying scientific meaning remains unchanged. Styling changes must not alter or imply changes to accepted Science invariants, score interpretation, ranking meaning, CRS/grid/units, masks/NoData, resampling semantics, feature eligibility, validation semantics or uncertainty.

Palette work is a presentation transformation, not a scientific-method change.

## 2. Locked public visual story

For the key public homepage sequence, the preferred visual order is:

1. **Hero** — cinematic Earth → satellite → AOI acquisition/scan.
2. **Real AOI satellite image** — one high-quality real Earth-observation image of the selected/scanned area, consistent with the premium EO imagery language already preferred by the team.
3. **Evidence panel** — one section with **three side-by-side evidence cards** rather than separate full-width posters for every technical layer. Intended families:
   - elevation / topography;
   - alteration;
   - faults / structural evidence.
4. **Score / prospectivity result** — one large, visually dominant result map below the evidence panel.

This replaces the earlier concept of spreading many evidence families across a long sequence of separate technical posters/cards.

## 3. Presentation intent

- The hero captures attention and communicates observation/acquisition.
- The real AOI image grounds the story in a real place.
- The three-card evidence panel explains the analytical basis without overwhelming non-technical visitors.
- The large score/result map is the analytical visual climax.
- The public site should remain legible to landowners, prospective customers, geothermal teams, research teams, commercial stakeholders and technical reviewers — not only GIS/geoscience engineers.
- Avoid a crowded technical-document aesthetic, card walls or a long multi-poster evidence stack.

## 4. Hero invariants already locked

The following existing hero decisions remain authoritative:

- Earth is a true 3D sphere with coherent perspective and atmosphere.
- The AOI is surface-conforming / geodetically anchored to the globe; it must never read as a flat screen-space rectangle pasted over Earth.
- Scan beams and corner locks register to the real 3D AOI footprint.
- The scan should visibly frame/lock the AOI and read as a genuine satellite acquisition/scan event.
- Global → acquisition → regional camera motion preserves the same AOI identity, orientation and scale continuously; no AI-style scale jump is acceptable.
- Acquisition visual language is restrained cyan / ice-blue / teal with premium cinematic lighting, not neon/HUD overload.
- Realism is preserved while visual appeal may be elevated for a broad public audience.

## 5. Task boundaries

- `WEB-HERO-001A..001D` remain the pre-data Blender scene-system lane.
- No invented DEM, thermal, alteration, fault, geology or score layer is permitted in the pre-data lane.
- The current active `WEB-HERO-001A` scope is unchanged by this publication.
- `WEB-HERO-001B/C/D` continue to consume the locked Earth/satellite/AOI/continuity invariants.
- Real scientific layer injection, public palette refinement and final public-layout/media integration remain downstream work owned by `WEB-005` or a later explicit Product revision.
- `WEB-005` must treat **Hero → Real AOI satellite image → 3-card Evidence panel → Large Score/Prospectivity result** as the preferred public presentation direction unless a newer Product authority explicitly supersedes it.

## 6. Science/public-safe constraint on the evidence trio

The three-card layout is a Product presentation decision, not permission to fabricate data. If one intended family lacks approved/public-safe evidence, the site must use the canonical optional-support/data-gap semantics rather than inventing a layer.

The public-facing palette may be more engaging than the technical/scientific palette, but it must remain truthful and must never imply stronger evidence, probability, reserve, discovery likelihood or drilling-success semantics than the accepted product/science authority supports.
