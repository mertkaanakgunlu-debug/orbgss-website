# WEB-002 — Evidence-to-Intelligence Product Proof & Geothermal Pilot Experience

**Linear:** MER-90  
**Authority:** CURRENT — OrbGSS Website vNext Product & Execution Authority v1.3 + this R1 alignment.  
**Canonical repository:** `mertkaanakgunlu-debug/orbgss-website`  
**Reference/upstream only:** `baran-orbgss/website`  
**Accepted baseline:** `main@677bfa7672ac18c2c808ddaaf235ff12863de443` (accepted WEB-001).  
**Branch:** `feat/web-002-product-proof`  
**Product state:** `WAITING_DOMAIN_DECISION — Science & Geospatial public-safe asset/pointer required`

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

The canonical cross-domain blocker/request is `docs/WEB-002_SCIENCE_ASSET_REQUEST.md`. No implementation should resume until that request is resolved with exact public-safe artifact pointers/package.

## Outcome

Turn the accepted WEB-001 gallery shell into a credible product demonstration while preserving:

> **Gallery is the presentation grammar. Evidence-to-intelligence is the story.**

A first-time visitor should understand the released product truthfully: observation → terrain context → EO evidence → optional/support context and explicit data gaps → remote-sensing relative priority → geothermal first-application proof.

WEB-002 does not redesign the information architecture and does not create the cinematic Earth/satellite hero.

## Required homepage proof sequence

Preserve the accepted WEB-001 structure and progressively replace the current `temporary-gallery` slots only with public-safe assets:

1. `observe` — real AOI/source-observation context that establishes where analysis begins.
2. `terrain` — real accepted remote-sensing terrain/DEM-derived context. Do not imply elevation/slope is a score predictor or universal favourability direction.
3. `evidence` — real accepted thermal and/or alteration evidence. Public labels must match canonical Science semantics; Sentinel alteration is a broad spectral proxy, never mineral/kaolinite identification or proof of hydrothermal alteration.
4. `structure` — when authoritative public-safe structural/geological context is unavailable, this section must deliberately render an **explicit data-gap / optional-support state** rather than fake faults/lithology. Structural/geological absence does not invalidate or numerically change `mvp_remote_sensing_priority_v1`.
5. `priority` — real accepted `mvp_remote_sensing_priority_v1` output, publicly labelled **Remote-Sensing Relative Priority — Experimental Baseline** or a shorter equivalent that preserves the same meaning. Do not call it Full Prospectivity.
6. `geothermal` — first-application proof tied to accepted geothermal MVP evidence/output. Prefer accepted Kızıldere v2 / real Workbench evidence if Science confirms the exact asset is publication-safe.

The exact scientific layer names shown publicly must match the actual accepted assets supplied by Science & Geospatial.

## Public-safe asset dependency

The website implementer does not own regeneration or reinterpretation of scientific outputs.

Before implementation resumes, `docs/WEB-002_SCIENCE_ASSET_REQUEST.md` must be resolved with exact pointers to an accepted public-safe package or existing artifacts for the applicable proof states, including provenance/licensing and mandatory warning text.

Paid/closed/restricted MTA data must not be published. If a requested optional/support asset cannot be made public-safe, keep an honest data-gap state.

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

## Scope after asset dependency resolves

- Replace temporary gallery visuals with the accepted public-safe proof package.
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
3. `structure` truthfully communicates optional/support context and any current data gap; no fabricated fault/geology evidence appears.
4. `priority` uses the accepted `mvp_remote_sensing_priority_v1` semantics and never implies Full Prospectivity/probability.
5. Every scientific/product visual has traceable provenance, rights/public-safe basis and exact label.
6. Geothermal is clearly the active first application; expansion directions remain subordinate.
7. No unsupported validation, accuracy, ROI, customer, partner, AI, discovery or drilling claim appears.
8. EN/TR parity exists for new visible copy and alt text.
9. New imagery is responsive/optimized without changing interpretation.
10. Keyboard/focus/navigation behavior from WEB-001 remains intact.
11. Provenance records are complete and repository validation passes with zero unexplained warnings.
12. WEB-005 hero work, WEB-003, deployment and DNS remain untouched.

## Verification / evidence

Provide at minimum:

- exact branch and final implementation HEAD;
- changed-path list;
- `py -3.14 scripts/validate_site.py` result;
- desktop/tablet/narrow-mobile visual evidence;
- exact mapping `observe / terrain / evidence / structure / priority / geothermal` → asset or deliberate data-gap state + public label + source pointer;
- provenance/public-safe basis for every new visual;
- confirmation that `mvp_remote_sensing_priority_v1` disclaimer semantics are preserved;
- confirmation that no hero/deploy/DNS work started.

## STOP / route conditions

Stop rather than invent if:

- `docs/WEB-002_SCIENCE_ASSET_REQUEST.md` remains unresolved for load-bearing proof assets;
- scientific meaning conflicts with accepted Science authority;
- rights/public-safe status is unclear;
- implementation would publish paid/closed/restricted data;
- a new scientific/product/UX/dependency decision outside this contract is required;
- destructive Git history changes would be required.

Routine HTML/CSS/JS bugs, image optimization, responsive/accessibility fixes, validator changes and conformant visual polish are implementer-owned.

## Branch/publication policy

- No feature work on `main`.
- Continue on `feat/web-002-product-proof` after the Science asset dependency is resolved.
- Normal bounded implementation commits are allowed.
- Do not begin WEB-003.
- Terminal implementation state after successful resume: `REVIEW_READY`.
