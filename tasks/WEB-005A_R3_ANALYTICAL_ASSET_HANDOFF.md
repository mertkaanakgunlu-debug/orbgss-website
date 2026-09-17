# WEB-005A R3 — Governed Analytical Asset & DEM-Relief Handoff

**State:** READY_FOR_CONTINUATION under existing WEB-005A / MER-107 execution authority  
**Parent authority:** `tasks/WEB-005A_R3_FIXED_CAMERA_GLOBE_DRAPE_REVISION.md`  
**Owning gate:** **A-HERO-18 — real globe-drape sequence gate**  
**Preview checkpoint:** R3 preview-before-render steps 6–10 (DEM → THM-01 → ALT-01 → Score → score-only final hold)

## Decision

The real-data globe-draped reveal, including terrain relief, is part of **WEB-005A R3 / MER-107**, not a later WEB-005B palette task and not a new standalone hero phase.

When WEB-005A resumes, implementation must consume the already prepared Kızıldere assets below rather than rediscovering raster locations, palette intent, or the reveal contract.

## Prepared source package

Governed source export package on the CTO workstation:

`C:\Projects\geothermal-prospectivity\outputs\kizildere_mvp_v2\exports\20260917T161155Z-5e7a0e53`

Expected governed raster inputs:

- `top-dem.tif`
- `thm-thm01.tif`
- `alt-alt01.tif`
- `score-mvp-remote-sensing-priority.tif`

These source rasters remain the analytical/scientific masters for the WEB-HERO handoff. Do not overwrite or destructively smooth them.

## Accepted hero display asset set

Prepared website/Blender display assets on the CTO workstation:

`C:\Projects\geothermal-prospectivity\outputs\webhero_display_final`

Expected 4K presentation textures:

- `terrain_webhero_display_4k.png`
- `thm01_webhero_display_4k.png`
- `alt01_webhero_display_4k.png`
- `priority_webhero_display_4k.png`
- `webhero_display_final_contactsheet.png`
- `webhero_display_final_manifest.json`

These PNGs are presentation-only derivatives for the cinematic hero. They are not scientific rasters and must not be used as elevation/displacement authority.

## Geometry / displacement contract

Terrain geometry must be derived from the governed **`top-dem.tif`**, not from the colored terrain PNG/TIFF.

Required architecture:

1. Preserve the accepted Earth sphere/world coordinates and AOI registration from WEB-HERO-001C/001D.
2. At the post-scan regional approach, use a sufficiently subdivided AOI-local surface patch or equivalent conforming geometry capable of visible relief.
3. Register that patch to the same authoritative AOI transform used by all thematic overlays.
4. Normalize the DEM only for geometry mapping; do not modify the stored source values.
5. A bounded cinematic vertical exaggeration is permitted for legibility. Start with approximately **2–4× visual exaggeration** and tune within the low-cost preview gate; it is a presentation parameter, not a scientific claim.
6. The colored `terrain_webhero_display_4k.png` is material/albedo only. Do not derive displacement from its RGB values or embedded hillshade.
7. THM-01, ALT-01 and Score are material/thematic overlays only; they must not deform terrain geometry.

## Layer-registration invariant

DEM geometry, Terrain color, THM-01, ALT-01 and Score must use one common AOI mapping/UV/geospatial transform so there is no visible layer jump between reveal stages.

The R3 layer sequence remains:

1. Terrain / DEM
2. THM-01
3. ALT-01
4. `mvp_remote_sensing_priority_v1`
5. Score-only final hold

A detached flat raster card or billboard remains non-conforming.

## Display-asset boundary

The final smoothed 4K PNGs may use display-only resampling/softening for website/Blender presentation. This treatment does not authorize alteration of the governed source rasters, scientific normalization semantics, feature meaning, scoring, masks, CRS/grid, or validation semantics.

For implementation provenance, record the exact file checksums actually ingested into the website/hero workspace. If any expected file is missing or differs from the prepared manifest, stop only the asset-ingest step and resolve the concrete file/provenance mismatch; do not redesign the visual language.

## Required low-cost proof before production render

A-HERO-18 must be proven before any long/full production render. The preview evidence must show, on the same AOI and same camera approach:

- DEM-derived relief visibly conforming to the globe/AOI surface;
- Terrain display texture correctly aligned to that relief;
- THM-01, ALT-01 and Score each occupying exactly the same registered footprint;
- no layer-to-layer geographic drift;
- no rectangular floating-panel read;
- final Score-only hold;
- relief magnitude visually credible at hero scale and free of obvious mesh tearing, UV seams or edge lift.

Once this preview is green, the same accepted mapping must be carried into the production render rather than re-authored.

## Implementation autonomy

Claude may choose the Blender implementation mechanism (displacement modifier, shader displacement/bump plus local patch geometry, geometry nodes, or an equivalent conforming technique) provided the invariants above hold. Product does not require a specific modifier stack.

Routine mesh density, subdivision level, texture filtering, render sampling, cache organization and reversible asset-copy wiring are implementation details inside this authority.

## STOP conditions

Return to Product only if a conforming implementation would require changing the true AOI footprint, public layer meaning, accepted reveal sequence, or material architecture; or if the prepared governed inputs are insufficient and a larger/new scientific data extent is genuinely required.

Do not re-enter Product merely for routine Blender setup, texture import, subdivision, UV mapping, interpolation, render-performance tuning, or local file-copy mechanics.
