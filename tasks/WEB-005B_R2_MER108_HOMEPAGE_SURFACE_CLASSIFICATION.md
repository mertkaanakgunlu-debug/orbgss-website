# WEB-005B R2 — MER-108 Surface Classification for Homepage Acts 3–4

**State:** ACCEPTED PRODUCT CLARIFICATION  
**Parent authority:** `tasks/WEB-005B_R1_HOMEPAGE_DESIGN_IMPLEMENTATION_BOUNDARY.md`  
**Science authority consumed:** `geothermal-prospectivity@30779547ced0cbf047cb51fb6c2c6ed178547d56:tasks/MER-108_TERMINAL_WEBSITE_HERO_DISPLAY_AMENDMENT.yaml`

## Decision

For WEB-005B only, homepage Acts 3 and 4 are classified as the public website marketing presentation surface covered by MER-108's allowed surface `website_marketing_hero`.

Therefore:

- Act 3 Terrain, THM-01 and ALT-01 homepage display derivatives MUST use conformant MER-108 derivatives built from the governed MER-113 rasters and the frozen CTO-approved palette topology/stops.
- Act 4 Priority homepage display derivative MUST use the conformant MER-108 Priority derivative and the same frozen CTO-approved palette topology/stops.
- This establishes hero → evidence → result palette continuity across the homepage.
- NoData/masked support remains alpha 0 exactly as governed.
- All derivatives remain presentation-only marketing media and MUST NOT be reused as scientific rasters, analytical workbench outputs, report cartography, quantitative exports, validation/QA evidence, model inputs or customer-report maps.

## Act 2 exclusion

Act 2 remains natural-colour real EO context and is NOT an MER-108 analytical derivative surface.

## Scientific boundary

This clarification does not expand MER-108 or change Science semantics. It only selects one already-authorized MER-108 surface classification (`website_marketing_hero`) for WEB-005B homepage Acts 3–4.

The MER-108 pipeline, scalar values, normalization, masks, topology, exact LUT/stops, checksums and provenance requirements remain authoritative.

## Implementation consequence

Do not keep GEO-WEB-002 byte-exact display exports for Acts 3–4 merely to avoid derivative work. Build/checksum conformant MER-108 website-marketing derivatives from the governed MER-113 sources and use them consistently for Acts 3–4.

No Product or Science re-entry is required unless implementation would exceed MER-108 bounds or alter governed semantics.
