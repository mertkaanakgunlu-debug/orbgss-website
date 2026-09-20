# GEO-WEB-004 — Homepage Evidence Presentation Parity Decision Request

**Requester:** OrbGSS Product & Software  
**Owner domain:** Science & Geospatial  
**Consumer:** WEB-005B / MER-109  
**Status:** WAITING_SCIENCE_DECISION  
**Related accepted Science authority:** MER-108 / GEO-WEB-003

## Observed fact

The accepted WEB-005B homepage implementation is visually ready except for the analytical imagery used in the Evidence/Result narrative.

The current homepage Evidence surfaces use conformant governed derivatives, but the visual presentation is materially less polished than the already CTO-approved hero analytical sequence.

MER-108 currently provides two relevant authorities:

1. General website/public display derivative authority at:
   `geothermal-prospectivity@11c32e8d2d072aa709262e513c8888e6a745bb76:tasks/MER-108_PUBLIC_WEB_DISPLAY_DERIVATIVE_AUTHORITY.md`

   This already allows website-only display derivatives, including mask-aware bilinear display interpolation, area/box downsampling, neutral hillshade/context compositing and responsive web delivery, while preserving governed normalization/palette/masks.

2. Terminal hero-only amendment at:
   `geothermal-prospectivity@30779547ced0cbf047cb51fb6c2c6ed178547d56:tasks/MER-108_TERMINAL_WEBSITE_HERO_DISPLAY_AMENDMENT.md`

   This additionally allows, for the narrower `website_hero_public_presentation` surface, bounded display-window compression, bounded monotonic gamma transfer and final RGBA Lanczos3 upsampling.

The CTO has now explicitly requested that the homepage Evidence/Result presentation use the same polished visual family as the accepted hero while remaining non-technical marketing presentation media.

## Blocking question

May the already-accepted MER-108 hero presentation transfer be reused for the following **public homepage narrative surfaces**:

- Act 03 Evidence shared-frame states:
  - Terrain
  - Thermal
  - Alteration
- Act 04 Priority/Result visual
- the post-Result Context ↔ analytical inspection aid

with the same governed sources/palette orientation and deterministic provenance?

## Requested narrow decision

Product requests Science to choose one of the following, or publish an equivalent exact bounded rule:

### Option A — extend hero presentation eligibility

Classify the named homepage narrative surfaces as eligible consumers of the existing `website_hero_public_presentation` display pipeline for these presentation stages only:

- bounded display-window compression under MER-108 terminal §6;
- bounded monotonic gamma transfer under §7;
- single final RGBA Lanczos3 resize including upsampling under §8.

Product does **not** request Gaussian smoothing or unsharp sharpening for these homepage surfaces.

### Option B — publish a narrower homepage-presentation profile

Keep the hero surface distinct, but publish an exact bounded homepage profile authorizing the minimum equivalent transforms needed to reproduce the selected hero visual family on the shared-frame Evidence/Result assets.

## Invariants that must remain frozen

Any accepted extension must preserve:

- governed MER-113 scalar sources and checksums;
- accepted scientific normalization identity;
- selected MER-108 palette topology/orientation;
- THM scientific center at 0;
- Priority fixed 0–100 AOI-relative score meaning, not probability;
- CRS/grid/footprint/units;
- valid-data mask and NoData semantics;
- no hole filling/inpainting/extrapolation;
- no local/adaptive contrast;
- no AI/generative super-resolution;
- no scientific scalar Lanczos/bicubic/spline;
- no Gaussian smoothing;
- no sharpening/unsharp;
- no selective hotspot emphasis;
- no use of website derivatives as scientific/report/model inputs.

The scientific master remains unchanged and authoritative.

## Product presentation target

The final website should use high-resolution presentation derivatives regenerated from governed scalar masters, not enlarged low-resolution PNGs.

Target delivery may include large/high-DPR assets (up to 4K-class presentation dimensions where source/rendering bounds permit), but this request is not authority to invent spatial detail.

The visible homepage should use simple user-facing labels such as Terrain / Thermal / Alteration; scientific codes and detailed grid/CRS metadata may remain in provenance rather than repeated in visible marketing copy.

## Required Science output

Please publish:

1. exact surface eligibility / profile name;
2. allowed transform stages and numeric bounds;
3. whether the existing hero LUT/palette stop checksums may be reused directly;
4. whether one fixed parameter set per layer may be reused across hero + homepage evidence/result;
5. provenance fields required for the homepage derivative family;
6. explicit confirmation that no new scientific method/normalization decision is being introduced.

## Pointers

- MER-108 terminal hero amendment:
  `30779547ced0cbf047cb51fb6c2c6ed178547d56:tasks/MER-108_TERMINAL_WEBSITE_HERO_DISPLAY_AMENDMENT.md`
- MER-108 general website display authority:
  `11c32e8d2d072aa709262e513c8888e6a745bb76:tasks/MER-108_PUBLIC_WEB_DISPLAY_DERIVATIVE_AUTHORITY.md`
- WEB-005B current local implementation under visual review:
  `feat/web-005b-homepage-visual-fidelity@5f118946217199952ad0affea3d5e897212ea482`
- Product fidelity policy:
  `docs/web-005-polish-authority@e691ea8ea0fa3d7dd6a20aa5ffd670e17f97635c:docs/WEB_PUBLIC_PRESENTATION_FIDELITY_POLICY.md`
- Product runtime/fidelity plan:
  `docs/web-005-polish-authority@ff1cbc66b93e22e91ded99818e626310c465a990:tasks/WEB-005B_R9_VISUAL_FIDELITY_RUNTIME_PERFORMANCE_PLAN.md`

## Continuation rule

Until Science publishes the decision, do not apply the hero-only display-window/gamma/RGBA-upsample transforms to homepage Evidence/Result assets.

All other accepted WEB-005B polish at local HEAD `5f118946...` may remain intact.

Once Science publishes the decision, Product may authorize one bounded asset-generation/swap revision without reopening homepage layout/design.
