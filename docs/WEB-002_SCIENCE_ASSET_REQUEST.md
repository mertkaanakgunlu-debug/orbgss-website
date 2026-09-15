# WEB-002 — Science & Geospatial public-safe proof-asset request

**Requester:** OrbGSS Product / Website vNext  
**Blocked task:** `tasks/WEB-002_PRODUCT_PROOF.md` / Linear MER-90  
**Website branch:** `feat/web-002-product-proof`  
**State:** `RESOLVED — READY_FOR_PRODUCT_RESUME`  
**Resolution package:** `docs/WEB-002_SCIENCE_ASSET_PACKAGE.md`

## Why this request exists

WEB-002 correctly stopped before implementation because the website repository contains no accepted public-safe product-proof assets or canonical pointers for the real evidence layers. This is an asset/publication dependency, not a request to invent or revise scientific method.

Current accepted Science authority already defines the relevant product semantics:

- `geothermal-prospectivity/docs/decisions/ADR-0033-remote-sensing-first-mvp-scoring-boundary.md`
- `geothermal-prospectivity/tasks/GEO-037-mvp-relative-priority-scoring.md` / Linear MER-32 — DONE
- `geothermal-prospectivity/tasks/GEO-039-cartographic-export-final-mvp-acceptance.md` / Linear MER-40 — DONE
- GEO-042 / Linear MER-50 — MVP 1.0.0 release DONE

The accepted MVP profile is `mvp_remote_sensing_priority_v1`, user-facing as **Remote-Sensing Relative Priority — Experimental Baseline**. It is an AOI-relative 0–100 experimental screening/ranking surface, not probability and not Full Prospectivity. The mandatory numeric core is THM-01 plus ALT-01/ALT-02 under ADR-0033. Terrain is context/display only. Structural/geological evidence is optional support and must not change the base score.

## Product presentation revision fixed by this request

WEB-002 must tell the released product truthfully:

1. `observe` — real AOI/source-observation context;
2. `terrain` — real accepted remote-sensing terrain context;
3. `evidence` — real accepted thermal and/or alteration evidence;
4. `structure` — **explicit structural/geology context data-gap state when authoritative public-safe context is unavailable**; do not fabricate faults/lithology and do not make this slot a prerequisite for the base score;
5. `priority` — real `mvp_remote_sensing_priority_v1` output labelled **Remote-Sensing Relative Priority — Experimental Baseline**;
6. `geothermal` — first-application proof based on the accepted geothermal MVP evidence/output, with no field-validation, discovery, reserve, drilling-success or Full-Prospectivity claim.

The website must not call the MVP score a full prospectivity score or imply that missing structural/geology context invalidates the accepted remote-sensing baseline.

## Required Science deliverable

Provide a small **public-safe website proof asset package** from already accepted MVP evidence. Reuse existing accepted outputs/export paths where possible; no new scientific method, scoring change, provider semantics or validation claim is requested.

For each applicable deliverable provide the exact accepted source pointer, checksum/artifact identity where available, public-facing label, provenance/licensing basis and any mandatory warning text:

- source-observation/AOI visual;
- terrain/DEM or hillshade visual from the accepted remote-sensing context source;
- THM-01 visual or accepted thermal family contribution/output;
- ALT-01/ALT-02 visual or accepted alteration family contribution/output;
- `mvp_remote_sensing_priority_v1` cartographic image/output;
- one geothermal first-application proof visual, preferably from the accepted Kızıldere v2 / accepted real Workbench evidence when publication-safe;
- confirmation of the structural/geology `data gap / optional support` wording for the website.

Web-friendly PNG/WebP/JPEG derivatives are sufficient if they preserve the accepted visual semantics. If only accepted GeoTIFF/cartographic-export artifacts exist, provide exact pointers and the governed style/export authority needed to create a web derivative without changing interpretation.

## Public-safe constraints

- Do not include paid/closed/restricted MTA data or any asset without confirmed reuse rights.
- Do not use known fields/wells/manifestations as predictors or imply they contributed to the base score.
- Do not expose local secrets, credentials or private filesystem details in public metadata.
- Sentinel alteration outputs remain broad spectral alteration proxies, not mineral/kaolinite identification or proof of hydrothermal alteration.
- The score remains experimental AOI-relative screening, not probability, reserve estimate, discovery likelihood, drilling-success estimate or cross-AOI calibrated score.
- No new validation claim is requested.

## Acceptance of this request

The dependency is resolved when Science & Geospatial provides either:

1. exact existing public-safe artifact pointers for the required proof assets; or
2. a published package generated strictly through already accepted MVP output/export paths, with provenance and rights recorded.

If any requested asset cannot be made public-safe, state that explicitly. Product will retain an honest data-gap state rather than substitute fabricated evidence.

## Resolution — GEO-WEB-001 / MER-96

Resolved by `docs/WEB-002_SCIENCE_ASSET_PACKAGE.md` on this branch. The response uses only the accepted ADR-0033 / GEO-037 / GEO-039 / GEO-042 boundary and the already-accepted GEO-039 Workbench cartographic export path.

The package authorizes bounded derived website-export recipes for `observe`, `terrain`, THM-01, ALT-01, ALT-02, `mvp_remote_sensing_priority_v1`, and the Kızıldere first-application proof state; it explicitly returns Structure and Geology as `DATA_GAP` / optional support. No MTA data, new provider, new score, or validation claim is introduced.

**Terminal state:** `READY_FOR_PRODUCT_RESUME`
