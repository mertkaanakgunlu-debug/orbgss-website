# WEB-002 — Science & Geospatial public-safe proof-asset package

**Domain response:** GEO-WEB-001 / Linear MER-96  
**Consumer:** `tasks/WEB-002_PRODUCT_PROOF.md` / Linear MER-90  
**State:** `READY_FOR_PRODUCT_RESUME`  
**Publication scope:** website proof visuals only; no scientific-method, scoring, provider, validation, or data-rights-policy change.

## 1. Governing accepted authority

This package is a publication/pointer response only. Scientific meaning remains governed by the already accepted Science authority:

- `mertkaanakgunlu-debug/geothermal-prospectivity@215ef89d794cf6cbf98e94f8fc17184c859ebcd8:docs/decisions/ADR-0033-remote-sensing-first-mvp-scoring-boundary.md`
- `mertkaanakgunlu-debug/geothermal-prospectivity@215ef89d794cf6cbf98e94f8fc17184c859ebcd8:tasks/GEO-037-mvp-relative-priority-scoring.md`
- `mertkaanakgunlu-debug/geothermal-prospectivity@215ef89d794cf6cbf98e94f8fc17184c859ebcd8:tasks/GEO-039-cartographic-export-final-mvp-acceptance.md`
- GEO-042 MVP 1.0.0 publication closeout: `mertkaanakgunlu-debug/geothermal-prospectivity:tasks/GEO-042_WP-3-mvp-1.0.0-release-closeout.md`, publication evidence dated 2026-09-05, release commit/tag target `215ef89d794cf6cbf98e94f8fc17184c859ebcd8`, tag `v1.0.0`.

Accepted Kızıldere v2 scoring identity from GEO-037:

- project: `kizildere_mvp_v2`
- profile: `mvp_remote_sensing_priority_v1`
- weighting identity: `remote_sensing_equal_family_v1`
- deterministic accepted run identity: `8716e89324ff5566859f470f207d5a1f0ab651c19d9c7e9dba3087960a63cf3c`
- mandatory score inputs: `thm-thm01`, `alt-alt01`, `alt-alt02`
- user-facing score semantics: **Remote-Sensing Relative Priority — Experimental Baseline**

GEO-039 accepted the normal Workbench cartographic export path for PNG/PDF/GeoTIFF with a machine-readable `export_manifest.json`, source provenance and generated-file SHA-256 checksums. Kızıldere Phase-1 evidence proved the export path on the persisted `kizildere_mvp_v2` project. The public website package below uses that already-accepted export mechanism with a deliberately narrower remote-sensing/terrain-only layer selection.

## 2. Public-safe boundary

`PUBLIC_SAFE` in this package means **OrbGSS-rendered website imagery generated through the accepted GEO-039 PNG/PDF export path from accepted persisted assets**. It does not authorize redistribution of raw provider bytes, does not restate or expand third-party source licences, and does not authorize any paid/closed/restricted data.

Required publication rules:

1. Materialize website visuals only through the accepted Workbench cartographic export path; do not copy raw provider rasters into the website repository.
2. Retain the export's provider/source attribution and scientific warning semantics in visible copy or adjacent provenance metadata.
3. When a website-optimized PNG/WebP/JPEG derivative is made, preserve the rendered scientific content, crop only for presentation, and record the original export manifest pointer plus the derivative checksum in `assets/imagery/sources.json` (or the repository's accepted provenance manifest).
4. Never include MTA paid/closed data.
5. Do not publish Structure/Geology support from the existing mixed-support Kızıldere proof exports under this package; the requested authority set does not establish a website-public reuse basis for those optional support assets.
6. Do not turn known geothermal fields/wells/manifestations into score inputs or imply that they validated the score.

## 3. Approved proof-state package

All recipes below use the accepted project `kizildere_mvp_v2`, the normal GEO-039 Workbench export flow, registry-approved styles, project AOI/CRS, and PNG as the website master. The accepted Kızıldere map evidence used `EPSG:32635`.

| Website state | Status | Exact accepted layer/export recipe | Public label | Provenance / temporal semantics | Rights/public-safe basis | Checksum authority | Mandatory warning |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `observe` | `APPROVED_EXPORT_RECIPE` | `kizildere_mvp_v2` → normal Workbench → show `top-dem` and Project AOI only → GEO-039 PNG export. Use the AOI outline and source line as the observation/start-context visual; do not substitute an ungoverned web basemap or raw satellite scene. | **Kızıldere AOI — accepted MVP project context** | AOI/project context from the accepted persisted Kızıldere v2 project; terrain source family is NASADEM. CRS `EPSG:32635`. No scene-date claim is required for this AOI-context state. | Derived OrbGSS cartographic export only; no raw provider redistribution. | Generated PNG SHA-256 must be copied from that export's `export_manifest.json`; website derivative gets its own checksum. | Scientific source/AOI context only; not validation evidence. |
| `terrain` | `APPROVED_EXPORT_RECIPE` | `kizildere_mvp_v2` → `top-dem` → registry-approved DEM style → GEO-039 PNG export. | **Elevation — NASADEM context** | NASADEM-derived elevation context accepted in MVP 1.0.0. Unit: metres. CRS/project AOI from accepted project. | Derived OrbGSS cartographic export only. | From generated `export_manifest.json`; do not invent a hash if the manifest is unavailable. | **Context/display only. Terrain is not a scored predictor and carries no universal geothermal-favourability direction.** |
| `thermal` / THM-01 | `APPROVED_EXPORT_RECIPE` | `kizildere_mvp_v2` → `thm-thm01` → governed THM-01 style → GEO-039 PNG export. | **THM-01 Thermal Anomaly** | Accepted Landsat-derived thermal evidence family. Use the persisted accepted THM-01 asset as-is. The governing GEO-037/GEO-039 closeouts do not duplicate individual acquisition dates; website copy must not invent them. | Derived OrbGSS cartographic export only; source attribution retained by export. | Source asset/checksum lineage and generated PNG SHA-256 are recorded by the accepted layer registry/export manifest; copy them verbatim when materialized. | Evidence layer only. Do not describe it as geothermal probability, reserve, discovery, or drilling-success evidence. |
| `alteration` / ALT-01 | `APPROVED_EXPORT_RECIPE` | `kizildere_mvp_v2` → `alt-alt01` → governed ALT-01 style → GEO-039 PNG export. | **ALT-01 Alteration Proxy — clay/hydroxyl** | Accepted Sentinel-2-derived broad spectral alteration proxy. Use the persisted accepted ALT-01 asset as-is; do not invent acquisition dates outside its accepted provenance. | Derived OrbGSS cartographic export only; source attribution retained by export. | Source lineage and generated PNG SHA-256 from `export_manifest.json`. | **Broad Sentinel-2 spectral alteration proxy; not mineral/kaolinite identification and not proof of hydrothermal alteration.** |
| `alteration` / ALT-02 | `APPROVED_EXPORT_RECIPE` | `kizildere_mvp_v2` → `alt-alt02` → governed ALT-02 style → GEO-039 PNG export. | **ALT-02 Alteration Proxy — ferric/iron** | Accepted Sentinel-2-derived broad spectral alteration proxy. Use the persisted accepted ALT-02 asset as-is; do not invent acquisition dates outside its accepted provenance. | Derived OrbGSS cartographic export only; source attribution retained by export. | Source lineage and generated PNG SHA-256 from `export_manifest.json`. | **Broad Sentinel-2 spectral alteration proxy; not mineral identification and not proof of hydrothermal alteration.** |
| `priority` | `APPROVED_EXPORT_RECIPE` | `kizildere_mvp_v2` → `score-mvp-remote-sensing-priority` generated by accepted `mvp_remote_sensing_priority_v1` run `8716e89324ff5566859f470f207d5a1f0ab651c19d9c7e9dba3087960a63cf3c` → governed score style → GEO-039 PNG export. | **Remote-Sensing Relative Priority — Experimental Baseline** | Derived only from accepted THM-01 + ALT-01/ALT-02 mandatory core under `remote_sensing_equal_family_v1`; AOI-relative 0–100 ranking/screening. | Derived OrbGSS cartographic export only. No MTA/Structure/Geology input is introduced. | GEO-037 run identity above; source/output lineage plus generated PNG SHA-256 from `export_manifest.json`. | **AOI-relative experimental screening only. Not probability, reserve/resource estimation, discovery likelihood, drilling-success likelihood, Full Prospectivity, or a calibrated cross-AOI score.** |
| `geothermal` | `APPROVED_EXPORT_RECIPE` | Use the same accepted `kizildere_mvp_v2` priority output, rendered as a Kızıldere first-application map through GEO-039. Allowed visible layers: `top-dem` + `score-mvp-remote-sensing-priority` (and, if editorially useful, `score-mvp-thermal` / `score-mvp-alteration`). Do **not** add optional Structure/Geology or MTA layers under this package. | **Kızıldere — first geothermal application of the experimental remote-sensing baseline** | Accepted Kızıldere v2 persisted project + accepted GEO-037 scoring output. Geographic/application context only; no validation/reference occurrence is promoted into the predictor set. | Derived OrbGSS cartographic export only; no restricted MTA or unapproved support data. | Same accepted scoring run identity; generated PNG SHA-256 from its export manifest. | **First-application proof, not field validation, discovery, reserve/resource, drilling-target, or drilling-success proof.** |
| `structure` | `DATA_GAP` | No website asset authorized by this package. | **Structural context — optional support / data gap** | Structure is optional engineering-secondary support and score-invariant under ADR-0033/GEO-037. | No public-site reuse basis is asserted here for existing support assets. | N/A | Missing structural context does not change `mvp_remote_sensing_priority_v1`. Do not fabricate faults. |
| `geology` | `DATA_GAP` | No website asset authorized by this package. | **Geology context — optional support / data gap** | Geology is optional engineering-secondary support and score-invariant under ADR-0033/GEO-037. | No public-site reuse basis is asserted here for existing support assets. | N/A | Missing geology context does not change `mvp_remote_sensing_priority_v1`. Do not fabricate lithology. |

## 4. Exact accepted export evidence and checksum semantics

GEO-039 acceptance proves the export mechanism and checksum contract. Relevant accepted evidence:

- Kızıldere Phase-1 export evidence in accepted PR #69 used project `kizildere_mvp_v2` and generated PNG/PDF/GeoTIFF through the normal Workbench.
- Accepted Kızıldere Phase-1 export ids include `20260904T151954Z-7a37d382` and R1 order proof `20260904T161928Z-e86ba6cb`.
- The final post-merge rehearsal export id was `20260904T173233Z-91237fe0` on the accepted generic runtime proof project; it is evidence for the export/checksum machinery, **not** a Kızıldere website visual.
- Canonical export package shape: `artifacts/validation/<project>/export/<export_id>/map.png`, `map.pdf`, selected raster GeoTIFFs, and `export_manifest.json`.
- The accepted manifest contract records generated filenames, byte sizes, SHA-256 checksums, selected layer/source identities, provenance, project CRS/grid/AOI identity, and warning state.

The exact per-file SHA-256 values of the above local proof exports are not duplicated in the accepted Git task text. Therefore this package intentionally does **not** fabricate them. When Product materializes the approved website masters, the authoritative checksum is the value in that export's `export_manifest.json`; the web-optimized derivative must receive and record its own checksum.

Important exclusion: the already-demonstrated Kızıldere Phase-1 compositions contained optional Macrostrat/GEM support layers. They remain valid GEO-039 engineering acceptance evidence, but are **not** the public WEB-002 asset masters authorized by this package. WEB-002 must render fresh presentation-only derivatives from the same accepted Kızıldere persisted evidence with only the approved remote-sensing/terrain layer selections above.

## 5. No-change scientific invariants

- Mandatory numeric core remains THM-01 + ALT-01 + ALT-02 only.
- Missing mandatory evidence still fails closed; no weight renormalization.
- Terrain remains context/display only.
- Structure and Geology remain optional support and score-invariant.
- Known fields/wells/manifestations remain reference/context only, never predictors.
- No MTA paid/closed/restricted data is included or authorized.
- No new validation claim is created by this package.
- No CRS/grid/units/NoData/mask/resampling/QA/feature-eligibility/scoring semantics are changed.

## 6. Product resume authority

The Science/Geospatial dependency requested by `docs/WEB-002_SCIENCE_ASSET_REQUEST.md` is resolved by this bounded package. Product may resume WEB-002 on `feat/web-002-product-proof` using only the approved export recipes and `DATA_GAP` states above.

**Terminal domain state:** `READY_FOR_PRODUCT_RESUME`
