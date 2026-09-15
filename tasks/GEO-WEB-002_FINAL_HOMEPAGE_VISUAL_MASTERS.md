# GEO-WEB-002 / MER-102 — Final homepage public-safe visual master package

- **State:** IN PROGRESS — CTO start approved 2026-09-16
- **Owner domain:** Science & Geospatial
- **Consumer:** WEB-005 / MER-93
- **Authority branch:** `feat/geo-web-002-final-visual-masters`
- **Authority baseline:** `8a4fe9ba5cb19d09390cb8816c2324e012331728`
- **Linear:** MER-102

## Outcome

Publish the rights-safe, provenance-traceable visual masters required by the locked four-act final homepage so WEB-005 can render the Kızıldere story without inventing science, redistributing raw provider data, using paid/closed MTA material, or visibly stretching the current 800/1400 px proof derivatives beyond their useful presentation size.

This task is an export/publication task. It does not authorize a new scientific method, scoring change, validation claim, product behavior change, or homepage implementation.

## Governing authority — exact pointers

Product presentation authority:

- `mertkaanakgunlu-debug/orbgss-website@8a4fe9ba5cb19d09390cb8816c2324e012331728:docs/WEB_PUBLIC_VISUAL_NARRATIVE_AUTHORITY.md`
- `mertkaanakgunlu-debug/orbgss-website@8a4fe9ba5cb19d09390cb8816c2324e012331728:docs/WEB-002_SCIENCE_ASSET_PACKAGE.md`
- `mertkaanakgunlu-debug/orbgss-website@8a4fe9ba5cb19d09390cb8816c2324e012331728:IMAGERY_RIGHTS.md`
- `mertkaanakgunlu-debug/orbgss-website@8a4fe9ba5cb19d09390cb8816c2324e012331728:assets/imagery/sources.json`

Accepted Science / export authority:

- `mertkaanakgunlu-debug/geothermal-prospectivity@215ef89d794cf6cbf98e94f8fc17184c859ebcd8:docs/decisions/ADR-0033-remote-sensing-first-mvp-scoring-boundary.md`
- `mertkaanakgunlu-debug/geothermal-prospectivity@215ef89d794cf6cbf98e94f8fc17184c859ebcd8:tasks/GEO-037-mvp-relative-priority-scoring.md`
- `mertkaanakgunlu-debug/geothermal-prospectivity@215ef89d794cf6cbf98e94f8fc17184c859ebcd8:tasks/GEO-039-cartographic-export-final-mvp-acceptance.md`
- release/tag: `215ef89d794cf6cbf98e94f8fc17184c859ebcd8` / `v1.0.0`

Accepted scoring identity remains:

- project: `kizildere_mvp_v2`
- profile: `mvp_remote_sensing_priority_v1`
- weighting identity: `remote_sensing_equal_family_v1`
- accepted run identity: `8716e89324ff5566859f470f207d5a1f0ab651c19d9c7e9dba3087960a63cf3c`
- mandatory score inputs: `thm-thm01`, `alt-alt01`, `alt-alt02`
- public score label: **Remote-Sensing Relative Priority — Experimental Baseline**

## Required package

### 1. Act 2 — real Kızıldere AOI Earth-observation context

Produce one high-quality natural-colour Kızıldere context master tied unambiguously to the accepted AOI.

Preferred rights-safe route is the already governed Class-A production pattern:

- USGS Landsat Collection 2 Level-2 surface reflectance;
- natural-colour OLI/OLI-2 bands 4/3/2 only;
- anonymous Microsoft Planetary Computer STAC access is allowed for source read;
- OrbGSS may crop/stretch/gamma/saturation/encode for presentation using the existing imagery pipeline grammar;
- record exact Landsat product id(s), acquisition date, sensor, source, rendered bounds, processing parameters, dimensions, output SHA-256 and USGS acknowledgement basis.

Selection criteria are visual/contextual only: the image must clearly cover the Kızıldere AOI, be reasonably cloud-free for presentation, and must not be described as analytical evidence or as the acquisition date of THM/ALT evidence unless that is independently true from accepted provenance.

No ungoverned web basemap, Google/Mapbox imagery, NASA-rendered image, raw provider raster copy, or paid/closed data may be substituted.

### 2. Compact evidence masters

Materialize presentation-safe masters/derivatives for the accepted Kızıldere AOI:

1. `top-dem` — **Elevation — NASADEM context**
2. `thm-thm01` — **THM-01 Thermal Anomaly**
3. accepted alteration evidence — prefer the clearest truthful public representation among `alt-alt01` and `alt-alt02`; publishing both masters is allowed and preferred when it does not create unnecessary duplication.

Use the accepted GEO-039 Workbench cartographic export path and governed styles. Preserve the exact scientific rendering semantics. Website derivatives may crop and resize for presentation only; no recolouring, re-projection, re-classification, value change, CSS colour transform, or invented date/interpretation.

### 3. Priority/result master

Materialize a presentation-safe master for:

- `score-mvp-remote-sensing-priority`
- accepted run/profile identity above
- public label **Remote-Sensing Relative Priority — Experimental Baseline**

This is an AOI-relative 0–100 experimental screening/ranking output. It is not probability, Full Prospectivity, reserve/resource estimation, discovery likelihood, drilling-success likelihood, or a calibrated cross-AOI score.

The final master must be suitable for the WEB-005 result/climax role without browser upscaling as the default desktop strategy. If the accepted renderer/source cannot support a larger presentation honestly, publish the exact maximum safe rendered size so WEB-005 can use a contained composition rather than stretching it.

## Resolution / derivative policy

Do not invent resolution by blindly enlarging the existing 800/1400 px website derivatives.

For each required visual:

1. resolve the accepted source/master or create a fresh accepted GEO-039 export from the same persisted accepted Kızıldere assets;
2. record master pixel dimensions and checksum before website derivation;
3. create only downscaled or presentation-crop derivatives from that master unless the accepted cartographic renderer itself can truthfully render a larger presentation master without changing scientific semantics;
4. if a visual cannot meet the intended large-display role, state its maximum safe CSS/render width explicitly.

Preferred delivery targets, when supported by the accepted source/render path without semantic change:

- Act-2 EO context: >= 2000 px wide master;
- evidence-card masters: >= 1200 px on the card's long axis;
- priority/result master: >= 2000 px on the intended large-display axis.

These are presentation targets, not permission to upscale scientific content or alter resampling semantics.

## Required publication record per asset

Publish a canonical package document under `docs/` and update `assets/imagery/sources.json` / `IMAGERY_RIGHTS.md` as applicable. Every asset entry must include:

- public role / homepage act;
- public label;
- exact source/export id and manifest pointer;
- source layer / project / accepted run identity where applicable;
- source/master dimensions and format;
- website derivative dimensions and format;
- SHA-256 for master and every shipped derivative;
- rights/public-safe basis and attribution requirement;
- crop/resample/encoding operation;
- maximum safe rendered size when relevant;
- mandatory warning semantics;
- clear statement whether the asset is context, evidence, or derived score.

## Scientific invariants — no change

- Mandatory numeric core remains THM-01 + ALT-01 + ALT-02 only.
- Missing mandatory evidence remains fail-closed; no weight renormalization.
- Terrain remains context/display only and is not a scored predictor.
- Structure/Geology remain `optional support / DATA_GAP / score-invariant` unless a separate accepted authority changes that state.
- Known fields/wells/manifestations remain reference/context only, never predictors.
- No MTA paid/closed/restricted data.
- No CRS/grid/units/NoData/mask/resampling/QA/feature-eligibility/scoring change.
- No new validation, uncertainty, probability, reserve/resource, discovery or drilling-success claim.
- No raw provider raster is committed to the website repository as a product-proof asset.

## Writable surface

Primary writable repository: `mertkaanakgunlu-debug/orbgss-website` on `feat/geo-web-002-final-visual-masters`.

Expected changed paths are limited to the outcome, normally:

- `tasks/GEO-WEB-002_FINAL_HOMEPAGE_VISUAL_MASTERS.md`
- `docs/GEO-WEB-002_FINAL_VISUAL_MASTER_PACKAGE.md`
- `assets/imagery/sources.json`
- `IMAGERY_RIGHTS.md`
- new Kızıldere context imagery under `assets/imagery/`
- new high-resolution public derivatives/masters under `assets/proof/` or a clearly named adjacent public asset directory
- existing imagery/provenance helper script(s) only when a small conformant change is necessary to reproduce the new Kızıldere natural-colour context or deterministic derivatives
- validator fixtures/expectations only as needed to verify the newly published assets/checksums

The `geothermal-prospectivity` repository and installed/persisted `kizildere_mvp_v2` project are read/export sources for this task. Do not change their scientific configuration, scoring output, registry semantics or release/tag.

## Verification and evidence

At minimum provide:

1. exact branch and final commit(s);
2. changed-path list;
3. asset inventory with master + derivative dimensions, bytes and SHA-256;
4. exact Landsat product/acquisition provenance for the Act-2 context image;
5. exact GEO-039 export id + `export_manifest.json` pointer for each cartographic master;
6. visual confirmation that each map is the intended Kızıldere AOI/layer and is not visibly soft at its declared safe rendered size;
7. deterministic checksum validation for every committed derivative;
8. existing site validator / relevant asset tests GREEN;
9. `git diff --check` GREEN;
10. no Science/Product semantic changes outside this task.

A screenshot alone is not provenance. The manifest/checksum/source pointers are mandatory.

## STOP / route

Stop and route to Science authority if completion requires:

- new scoring, weights, thresholds, feature eligibility, scientific interpretation or validation semantics;
- changing CRS/grid/units/NoData/mask/resampling semantics;
- using a new analytical provider/data family to stand in for accepted evidence.

Stop and route to Product if completion requires:

- changing the locked four-act homepage meaning or visual acceptance contract;
- relabelling the score/evidence meaning;
- introducing a new site architecture/dependency merely to display the assets.

Human gate is required for:

- credentials/admin access;
- paid/licensed/closed data or commercial asset purchase;
- destructive migration/deletion/history rewrite;
- any legal/commercial commitment.

Routine export failures, stale local paths, missing derivative scripts, checksum mismatches, image-encoding defects, validator failures, small conformant helper changes, and ordinary Git/branch hygiene are implementation-owned and must be self-fixed without reopening Product/Science semantics.

## Network / data permissions

- Public USGS Landsat read through the established anonymous Planetary Computer STAC route: **ALLOWED** for the Act-2 context master.
- Existing accepted local/persisted Kızıldere evidence and GEO-039 export path: **ALLOWED**.
- Paid/closed/restricted MTA data: **DENIED**.
- Arbitrary new basemap/provider integration: **DENIED**.
- External upload/sharing beyond normal repository publication: **DENIED** unless separately authorized.

## Commit / publication policy

- No feature work on `main`.
- Work only on `feat/geo-web-002-final-visual-masters` unless a branch conflict requires a normal non-destructive compatibility repair.
- Ordinary implementation commit structure is implementer-owned; do not create artificial micro-commit STOPs.
- No force-push or destructive history rewrite.
- Publish the completed branch non-force after verification.
- MER-102 reaches terminal Science state only after the canonical package pointer, checksums, rights basis, warnings and safe-render-size evidence are published and verified.
- Product may bind the accepted package into WEB-005 only after terminal Science acceptance.
