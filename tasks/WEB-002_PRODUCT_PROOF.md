# WEB-002 — Evidence-to-Intelligence Product Proof & Geothermal Pilot Experience

**Linear:** MER-90  
**Authority:** CURRENT — OrbGSS Website vNext Product & Execution Authority v1.4 + this R2 resume alignment.  
**Canonical repository:** `mertkaanakgunlu-debug/orbgss-website`  
**Reference/upstream only:** `baran-orbgss/website`  
**Accepted baseline:** `main@677bfa7672ac18c2c808ddaaf235ff12863de443` (accepted WEB-001).  
**Branch:** `feat/web-002-product-proof`  
**Product state:** `IN_PROGRESS — EXECUTION_CONTINUATION_READY`

## R2 — Science dependency resolved / resume authority

The WEB-002 Science dependency is resolved by the accepted public-safe package:

- `docs/WEB-002_SCIENCE_ASSET_PACKAGE.md`
- resolved request: `docs/WEB-002_SCIENCE_ASSET_REQUEST.md`
- Science package publication commit: `9ccd199470a74d44116b9634e032a2fe8864a80f`
- Science resolution HEAD before Product resume publication: `45e2e5b46a07a28cc4ec399173f57f3b82c19cbc`
- immutable Science release authority: `mertkaanakgunlu-debug/geothermal-prospectivity@215ef89d794cf6cbf98e94f8fc17184c859ebcd8`
- accepted Kızıldere v2 scoring identity: `8716e89324ff5566859f470f207d5a1f0ab651c19d9c7e9dba3087960a63cf3c`

WEB-002 already received deliberate CTO start approval before the domain STOP. This R2 publication does **not** create a new plan or require a second CTO start gate. Implementation continuation is authorized on the same branch and should proceed through normal E&D/implementer ownership to `REVIEW_READY`.

The website implementer may materialize website proof masters only through the accepted GEO-039 Workbench cartographic export path described by the Science package. Real generated SHA-256 values must be taken from each `export_manifest.json`; hashes not present in canonical evidence must never be invented.

Structure and Geology remain an explicit `DATA_GAP / optional support / score-invariant` state unless a separate public-safe authority later exists. No fault/lithology asset is required for WEB-002 completion under this contract.

## R1 — accepted Science alignment

The first WEB-002 implementation attempt correctly stopped because the website repository had no public-safe product-proof asset package. Product re-entry resolved one important semantic ambiguity: the accepted MVP score already exists and its meaning is not open for invention.

Canonical Science pointers:

- `geothermal-prospectivity/docs/decisions/ADR-0033-remote-sensing-first-mvp-scoring-boundary.md`
- `geothermal-prospectivity/tasks/GEO-037-mvp-relative-priority-scoring.md` / Linear MER-32 — DONE
- `geothermal-prospectivity/tasks/GEO-039-cartographic-export-final-mvp-acceptance.md` / Linear MER-40 — DONE
- GEO-042 / Linear MER-50 — MVP 1.0.0 release DONE

The active MVP profile is `mvp_remote_sensing_priority_v1`, user-facing as **Remote-Sensing Relative Priority — Experimental Baseline**. It is a deterministic 0–100 within-AOI screening/ranking surface. It is not Full Prospectivity, probability, reserve estimate, discovery likelihood, drilling-success estimate or a calibrated cross-AOI score.

The mandatory numeric core is the accepted remote-sensing evidence in ADR-0033: THM-01 thermal plus ALT-01/ALT-02 alteration proxies under the frozen `remote_sensing_equal_family_v1` hypothesis. Missing mandatory evidence fails closed; website work must not alter that rule.

NASADEM elevation/slope/hillshade are context/display layers only in the accepted MVP and carry no universal geothermal-favourability direction. Structural/geological evidence is optional support, is score-invariant, and is not a prerequisite for the accepted remote-sensing baseline.

## Outcome

Turn the accepted WEB-001 gallery shell into a credible product demonstration while preserving:

> **Gallery is the presentation grammar. Evidence-to-intelligence is the story.**

A first-time visitor should understand the released product truthfully: observation → terrain context → EO evidence → optional/support context and explicit data gaps → remote-sensing relative priority → geothermal first-application proof.

WEB-002 does not redesign the information architecture and does not create the cinematic Earth/satellite hero.

## Required homepage proof sequence

Preserve the accepted WEB-001 structure and progressively replace the current `temporary-gallery` slots only with public-safe assets:

1. `observe` — materialize the accepted `kizildere_mvp_v2` AOI/project-context export from `top-dem` + Project AOI through GEO-039. Public label: **Kızıldere AOI — accepted MVP project context**. This is source/AOI context only, not validation evidence.
2. `terrain` — materialize `top-dem` with the registry-approved DEM style through GEO-039. Public label: **Elevation — NASADEM context**. Terrain is context/display only, not a scored predictor and carries no universal geothermal-favourability direction.
3. `evidence` — materialize the accepted evidence layers through GEO-039:
   - `thm-thm01` → **THM-01 Thermal Anomaly**;
   - `alt-alt01` → **ALT-01 Alteration Proxy — clay/hydroxyl**;
   - `alt-alt02` → **ALT-02 Alteration Proxy — ferric/iron**.
   Sentinel alteration is a broad spectral proxy, never mineral/kaolinite identification or proof of hydrothermal alteration.
4. `structure` — deliberately render **Structural context — optional support / data gap** and, where editorially useful, the parallel **Geology context — optional support / data gap** state. Do not publish the existing Macrostrat/GEM acceptance layers as WEB-002 public masters under this authority. Missing structure/geology does not change the accepted base score.
5. `priority` — materialize `score-mvp-remote-sensing-priority` from accepted run `8716e89324ff5566859f470f207d5a1f0ab651c19d9c7e9dba3087960a63cf3c` through GEO-039. Public label: **Remote-Sensing Relative Priority — Experimental Baseline**.
6. `geothermal` — materialize a Kızıldere first-application map through GEO-039 using `top-dem` + `score-mvp-remote-sensing-priority`, optionally with accepted thermal/alteration contribution layers when editorially useful. Public label: **Kızıldere — first geothermal application of the experimental remote-sensing baseline**. This is first-application proof, not field-validation/discovery/reserve/drilling-success proof.

For every materialized export, follow the exact provenance, rights/public-safe basis, checksum authority and mandatory warning text in `docs/WEB-002_SCIENCE_ASSET_PACKAGE.md`.

## Public-safe asset execution rule

The website implementer may produce presentation derivatives from accepted persisted evidence only through the accepted GEO-039 export mechanism. Do not copy raw provider rasters into the website repository.

For each website master and optimized derivative:

- retain provider/source attribution and mandatory scientific warnings;
- record the original export manifest pointer and generated master SHA-256 from `export_manifest.json`;
- record the optimized derivative's own checksum in `assets/imagery/sources.json` or the accepted provenance manifest;
- crop/resize/compress only for presentation without changing rendered scientific meaning;
- do not invent scene dates, hashes, validation semantics or source rights not present in canonical evidence.

Paid/closed/restricted MTA data must not be published.

## Scientific boundary

Website work may present accepted scientific outputs but may not redefine them. Do not change or invent:

- CRS, grid, units, NoData/mask behavior;
- resampling or categorical/QA semantics;
- constants or feature eligibility;
- validation meaning;
- uncertainty semantics;
- score interpretation;
- geothermal methodology;
- weights, thresholds or scoring transforms.

Known fields, wells, manifestations and other validation/reference evidence must never be implied to be predictors in the accepted remote-sensing baseline.

## Scope

- Materialize the approved public-safe proof exports and replace temporary gallery visuals with them.
- Preserve the dark technical beam → full-width visual rhythm and WEB-001 navigation/order.
- Add concise editorial metadata/captions; do not turn the page into a GIS dashboard.
- Make the observation → context → evidence → priority relationship understandable at a glance.
- Present geothermal as the first active application; keep Mineral Exploration and Environmental & Land Intelligence subordinate as expansion directions.
- Update `assets/imagery/sources.json` or the accepted provenance manifest for every public visual.
- Preserve EN/TR parity for visible copy and alt text.
- Optimize web derivatives without changing scientific interpretation.
- Update the validator only where required to enforce the accepted proof contract.

Restrained optional interactions such as before/after reveals or simple layer-state comparison are allowed when they improve comprehension and remain accessible/mobile-safe. No scroll-jacking, fake GIS controls, HUD chrome, icon walls or SaaS card grids.

## Copy and claim rules

Allowed framing includes traceable provenance, explicit data gaps, evidence-backed spatial prioritization, decision support, experimental remote-sensing baseline and the need for field investigation.

Not allowed without separate authority:

- accuracy percentages or ROI;
- customer/partner endorsements;
- production-readiness claims for expansion verticals;
- AI/model-performance claims;
- field-validation/discovery/reserve/drilling-success claims;
- claims that OrbGSS replaces field exploration;
- calling the MVP score probability, Full Prospectivity or a cross-AOI calibrated metric.

## Out of scope

- new scientific method or analysis pipeline;
- recomputing/changing canonical score semantics;
- paid/closed data acquisition;
- cinematic Earth/satellite hero or WebM/MP4 integration (WEB-005);
- WEB-003 site-depth work;
- Vercel production cutover / Squarespace DNS (WEB-006);
- new frontend framework/backend, analytics, auth, billing or CRM.

## Acceptance

WEB-002 is complete only if:

1. WEB-001 gallery identity and narrative order remain intact.
2. Real public-safe proof assets communicate a coherent remote-sensing evidence-to-priority workflow.
3. `observe`, `terrain`, THM-01, ALT-01, ALT-02, `priority` and geothermal proof are materialized through the accepted GEO-039 export path or an exact canonical reason is recorded if a package recipe cannot execute.
4. `structure`/`geology` truthfully communicate optional-support/data-gap status; no fabricated or unapproved fault/geology evidence appears.
5. `priority` uses the accepted `mvp_remote_sensing_priority_v1` semantics and never implies Full Prospectivity/probability.
6. Every scientific/product visual has traceable provenance, public-safe basis, exact label, master export-manifest pointer and truthful checksum metadata.
7. Geothermal is clearly the active first application; expansion directions remain subordinate.
8. No unsupported validation, accuracy, ROI, customer, partner, AI, discovery or drilling claim appears.
9. EN/TR parity exists for new visible copy and alt text.
10. New imagery is responsive/optimized without changing interpretation.
11. Keyboard/focus/navigation behavior from WEB-001 remains intact.
12. Provenance records are complete and repository validation passes with zero unexplained warnings.
13. WEB-005 hero work, WEB-003, deployment and DNS remain untouched.

## Verification / evidence

Provide at minimum:

- exact branch and final implementation HEAD;
- changed-path list;
- `py -3.14 scripts/validate_site.py` result;
- desktop/tablet/narrow-mobile visual evidence;
- exact mapping `observe / terrain / evidence / structure / priority / geothermal` → asset or deliberate data-gap state + public label + source pointer;
- for each materialized scientific visual: GEO-039 export id/path, `export_manifest.json` pointer, generated master SHA-256 and website derivative SHA-256;
- confirmation that all mandatory package warning/disclaimer semantics are preserved;
- confirmation that no raw provider raster, MTA data, hero/deploy/DNS work was introduced.

## STOP / route conditions

Stop rather than invent if:

- an approved export recipe cannot be materialized from the accepted persisted evidence and resolving it would require a new scientific/data-rights/product decision;
- scientific meaning conflicts with accepted Science authority;
- rights/public-safe status is unclear beyond the published package;
- implementation would publish paid/closed/restricted data;
- a new scientific/product/UX/dependency decision outside this contract is required;
- destructive Git history changes would be required.

Routine export execution, web-derivative generation, HTML/CSS/JS bugs, image optimization, responsive/accessibility fixes, provenance-manifest updates, validator changes and conformant visual polish are implementer-owned and must not trigger Product re-entry.

## Branch/publication policy

- No feature work on `main`.
- Continue on `feat/web-002-product-proof` from the current authority HEAD after this R2 publication.
- Normal bounded implementation commits are allowed; no artificial micro-step commit budget.
- Do not begin WEB-003.
- Terminal implementation state: `REVIEW_READY`.