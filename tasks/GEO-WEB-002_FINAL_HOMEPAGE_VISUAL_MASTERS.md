# GEO-WEB-002 / MER-102 — Final homepage public-safe visual master package

- **State:** REVIEW_READY — implemented 2026-09-16; CTO start approved 2026-09-16
- **Owner domain:** Science & Geospatial
- **Consumer:** WEB-005 / MER-93
- **Authority branch:** `feat/geo-web-002-final-visual-masters`
- **Authority baseline:** `8a4fe9ba5cb19d09390cb8816c2324e012331728`
- **Linear:** MER-102
- **Implementation HEAD:** `3165a92` on `feat/geo-web-002-final-visual-masters`
- **Package:** `docs/GEO-WEB-002_FINAL_VISUAL_MASTER_PACKAGE.md` (`READY_FOR_PRODUCT_BINDING`)

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

## Execution evidence (2026-09-16, REVIEW_READY)

### 1. Branch and commits

- Branch `feat/geo-web-002-final-visual-masters`, from authority baseline `8a4fe9b`.
- `3165a92` — `feat(geo-web-002): publish final homepage visual master package (MER-102)`.
- This evidence commit records the implementation HEAD and reconciles `STATUS.md`.
- No force-push, no history rewrite, no work on `main`.

### 2. Changed paths

```
A  assets/imagery/kizildere-aoi-context-2025.jpg
A  assets/imagery/kizildere-aoi-context-2025-{2400,1800,1200,900}.webp
A  assets/proof/final/{terrain,thm01,alt01,alt02,priority}-1249.webp
A  assets/proof/final/{terrain,thm01,alt01,alt02,priority}-800.webp
A  assets/proof/final/{terrain,thm01,alt01,alt02,priority}-legend.png
A  docs/GEO-WEB-002_FINAL_VISUAL_MASTER_PACKAGE.md
A  scripts/build_final_visual_masters.py
M  assets/imagery/sources.json          (new geo_web_002 block; version 0.8)
M  IMAGERY_RIGHTS.md                     (v0.8: new source, class-B resolution ceiling)
M  scripts/build_imagery.py              (also builds the package's context scene)
M  scripts/validate_site.py              (enforces the new publication record)
M  tasks/GEO-WEB-002_FINAL_HOMEPAGE_VISUAL_MASTERS.md
M  STATUS.md
```

Nothing in `mertkaanakgunlu-debug/geothermal-prospectivity` was modified. It was read only: five accepted
export directories and their `export_manifest.json` files, plus the vendored batlow LUT used to measure
ramp occupancy for the legibility finding below.

### 3. Asset inventory

Full per-asset record with every SHA-256 is in `docs/GEO-WEB-002_FINAL_VISUAL_MASTER_PACKAGE.md` §4 and in
`assets/imagery/sources.json` → `geo_web_002.assets`. Summary:

| Asset | Role | Master | Shipped | Bytes (largest) |
| --- | --- | --- | --- | --- |
| `act2-context` | context | 2400 × 1500 JPEG in-repo | 2400 / 1800 / 1200 / 900 WebP | 867 942 |
| `terrain` | context | 2338 × 1654 PNG export, panel 1249 | 1249 + 800 WebP, 732 × 122 legend PNG | 41 698 |
| `thm01` | evidence | 2338 × 1654 PNG export, panel 1249 | 1249 + 800 WebP, 732 × 122 legend PNG | 251 574 |
| `alt01` | evidence | 2338 × 1654 PNG export, panel 1249 | 1249 + 800 WebP, 732 × 122 legend PNG | 393 032 |
| `alt02` | evidence | 2338 × 1654 PNG export, panel 1249 | 1249 + 800 WebP, 732 × 122 legend PNG | 381 046 |
| `priority` | derived score | 2338 × 1654 PNG export, panel 1249 | 1249 + 800 WebP, 732 × 122 legend PNG | 702 856 |

19 shipped files, 4 613 070 bytes in total across the whole responsive ladder.

### 4. Act-2 Landsat provenance

`LC08_L2SP_179034_20250505_02_T1` — Landsat 8 OLI, acquired **2025-05-05**, WRS-2 path 179 / row 034,
Collection 2 Level-2 Tier 1, scene cloud cover 0.90 %, read anonymously through the Planetary Computer STAC
mirror of the USGS archive. Rendered natural-colour (OLI 4/3/2) at native 30 m into EPSG:32635,
2400 × 1500 px = 72 × 45 km, bounds UTM `621268.9, 4182542.0, 693268.9, 4227542.0`, 100 % valid coverage;
percentile stretch `[1.0, 99.0]`, gamma 1.65, saturation 1.20, JPEG quality 82. Master SHA-256
`9d4f93298d11b31ec7317e72bfd0485fe7bf8a724188108abdc48c8a630197a4`.

The frame is centred on the accepted AOI centre 37.9794° N, 28.7907° E, so the 36 × 36 km AOI sits in the
middle of a regional view. Selection was visual/contextual only. Three single scenes in 2024–2026 fully
covered the frame with < 2 % cloud; this one was chosen for seasonal legibility. Two small cloud puffs
remain in the north-west mountains, outside the AOI. No acquisition date is attributed to any THM/ALT
evidence layer anywhere in the package.

### 5. GEO-039 export identity per cartographic master

All on `kizildere_mvp_v2`, renderer `geo039-cartographic-renderer-v1`, project config hash
`c6eac56027d3118280d2a454bdcacf5b01ddb0d733ab23dacbf348b6a50b777c`; manifest pointer
`geothermal-prospectivity/outputs/kizildere_mvp_v2/exports/<id>/export_manifest.json`.

| Asset | Export id | Master SHA-256 |
| --- | --- | --- |
| `terrain` | `20260915T104731Z-00fae5eb` | `8fc9403a022f28a6e5d56443ad16e5b2390a676fd2cd9cf2e50285eae2be6ca1` |
| `thm01` | `20260915T104733Z-cfba9119` | `fe789994c29a9a87a3e08a29af5663e7c922f07c6e3016027fb1f5d2ef505dac` |
| `alt01` | `20260915T104801Z-eb1bc414` | `80fd75303100728ca6fd935b56167f17f0fd68b0b719b9306e1fac9ed5b5adf8` |
| `alt02` | `20260915T104804Z-1f837163` | `b3d1824de39293af4b10a56beb04f4e7bb28988cf86cafb30024da66b528f950` |
| `priority` | `20260915T104736Z-55609249` | `4791435a1b1c1d19a18337997eaf51dfb468ed022349771e1007c6da026aa2ad` |

These are the accepted masters the WEB-002 recipes already materialized, resolved rather than re-exported:
an identical plan re-renders byte-identically under the GEO-039 determinism contract, so a fresh export
would have produced the same bytes under a new id and weakened, not strengthened, traceability. Each was
re-verified against the checksum in its own `export_manifest.json` before any derivative was written.

### 6. Resolution outcome against the task's presentation targets

The accepted grid is 1200 × 1200 cells at 30 m; the accepted renderer draws that panel at 1249 px with
nearest-neighbour compositing. **1249 device pixels is the maximum honest rendered width for class B.**

| Target | Delivered | Verdict |
| --- | --- | --- |
| Act-2 EO context ≥ 2000 px | 2400 px native | met |
| Evidence cards ≥ 1200 px long axis | 1249 px | met |
| Priority ≥ 2000 px large-display axis | 1249 px | **not met, not honestly achievable** |

Raising `CARTOGRAPHIC_MAP_DPI` in the Science repository would yield a larger file with no more information
and would break the byte-identical determinism the accepted GEO-039 contract relies on, so it was not done.
The task's stated fallback was taken instead: every asset publishes `max_safe_rendered_px` with its basis,
and the package tells WEB-005 that Act 4 must be a contained composition of at most 1249 device pixels on
its long axis (1249 CSS px at 1×, 624 CSS px at 2×).

To avoid a second resample the widest class-B derivative is the map-panel crop itself at 1249 px with no
resizing at all; the 800 px card derivative is a Lanczos downscale of the same crop.

### 7. Visual confirmation

Each of the five cartographic panels was inspected and is the intended Kızıldere AOI and the intended
layer, with the same framing, north arrow, scale bar and AOI outline. At 1:1 the priority panel resolves
individual 30 m cells with no softness. The Act-2 composite resolves fields, roads and settlements and the
Büyük Menderes graben scarp at native 30 m.

Two presentation findings are published in package §5 as facts WEB-005 must not "fix":

- **ALT-01 / ALT-02 read as dark fields with bright anomalies.** `alt_batlow_sequential` is the only
  registry-approved style for both layers and it normalizes linearly over the full value range; measured on
  the shipped panels, 87.4 % (ALT-01) and 87.5 % (ALT-02) of valid cells fall in the lowest fifth of the
  batlow ramp. That is accepted scientific rendering — no re-stretch, re-normalize or CSS adjustment.
  ALT-01 is recommended as the single alteration card and ALT-02 is published alongside it.
- **NoData is real and visible**: 0.0 % (`terrain`), 0.2 % (`thm01`), 4.0 % (`alt01`), 4.6 % (`alt02`),
  5.5 % (`priority`) of each panel is the neutral `#f3f2ee` ground.

### 8. Deterministic checksum validation

`scripts/build_final_visual_masters.py` re-verifies each class-B master against its own export manifest,
checks the export's rendered layer ids against the asset's declared layers, and refuses any derivative
wider than the master's map panel. Re-running the full build after the fact reproduced every shipped file
byte-for-byte (validation stayed green with no checksum drift). A deliberately tampered master was
rejected: `terrain: master checksum mismatch against its own export manifest … refusing to derive from an
altered master`.

`scripts/validate_site.py` now recomputes the SHA-256 and byte size of the class-A master and of all 19
shipped derivatives on every run, requires the full publication record per asset, requires
`derivation.no_upscale`, requires each asset to state whether it is context, evidence or a derived score,
and fails any derivative wider than the ceiling the asset itself declares.

Negative tests (mutate, run, restore — all six produced the expected failure and the tree was restored):

| Mutation | Result |
| --- | --- |
| edit a shipped derivative | `geo_web_002 derivative checksum mismatch for assets/proof/final/priority-800.webp` |
| drop `mandatory_warning` | `geo_web_002 asset 'priority' missing field: mandatory_warning` |
| lower an asset's declared ceiling below its shipped width | `… is 1249 px wide but 'priority' declares a 800 px ceiling` |
| drift the class-A master checksum | `geo_web_002 asset 'act2-context' master checksum mismatch …` |
| diverge the scene and asset derivative records | `… publish different derivative records` |
| drop a class-B master pointer | `geo_web_002 asset 'terrain' missing export.master_sha256` |

### 9. Test and hygiene status

- `python scripts/validate_site.py` — **PASS**, 0 warnings, 6 routes, 185 i18n keys, 6 package assets /
  19 files. Run before the change (PASS at baseline) and after.
- `git diff --check` — **GREEN**.
- No public route, homepage composition, copy, style or script behaviour outside the package was changed;
  the accepted WEB-002/WEB-003/WEB-004 site renders exactly as before.

### 10. Semantic boundary

No Science or Product semantics changed. Mandatory core remains THM-01 + ALT-01 + ALT-02; fail-closed
behaviour, terrain-as-context, the structure/geology `DATA_GAP`, reference-data exclusion, CRS/grid/unit/
NoData/mask/resampling semantics and every public label and mandatory warning are carried verbatim from
`docs/WEB-002_SCIENCE_ASSET_PACKAGE.md`. No new validation, uncertainty, probability, reserve/resource,
discovery or drilling-success claim exists anywhere in the package. No structure or geology asset is
published and nothing is fabricated to fill that gap. No STOP condition was reached.

### 11. Remaining gate

MER-102 reaches terminal Science state on acceptance of this branch. Product may bind the package into
WEB-005 only after that acceptance.
