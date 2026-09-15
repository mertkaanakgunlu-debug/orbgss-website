# OrbGSS Website — CURRENT

**Canonical version:** `v0.8.2-web-003-product-acceptance` — WEB-003 accepted/complete
**Date:** 2026-09-15
**Stage:** WEB-003 public-site depth accepted after one bounded Product review revision; canonical `main` contains the accepted six-route public site. WEB-004 is the next task and remains not started pending deliberate CTO approval.
**Site architecture:** static HTML + CSS + vanilla JavaScript
**Public domain target:** `https://orbgss.com`
**Canonical repository:** https://github.com/mertkaanakgunlu-debug/orbgss-website
**Accepted WEB-002 implementation HEAD:** `a10cc141e3a7830c5e3c67a22e950ab16c0fe92b`
**Accepted WEB-003 implementation HEAD:** `3670d43bece4ffba657a3d9645cbea20c7e698bf`
**Reference/upstream only:** https://github.com/baran-orbgss/website
**Science authority:** `mertkaanakgunlu-debug/geothermal-prospectivity@215ef89d794cf6cbf98e94f8fc17184c859ebcd8` (tag `v1.0.0`)
**Registrar / DNS:** Squarespace
**Hosting target:** Vercel
**Company:** VirgaSoft
**Product:** OrbGSS — Orbital Geo-Spatial Solutions
**Product authority:** OrbGSS Website vNext Product & Execution Authority v1.8 (`docs/WEB_VNEXT_AUTHORITY.md`)
**Tracking:** Linear MER-90 (WEB-002 accepted/complete); MER-91 (WEB-003 accepted/complete); MER-92 (WEB-004 next, not started); MER-96 / GEO-WEB-001 resolved

## Authority

`docs/WEB_VNEXT_AUTHORITY.md` is the repository-local summary of the product-owned *OrbGSS Website vNext Product & Execution Authority* (v1.8). Where it disagrees with `docs/DESIGN_AUTHORITY.md` or `docs/PRODUCT_AND_CONTENT_AUTHORITY.md`, it wins for vNext work. WEB-002 is terminally accepted under `tasks/WEB-002_PRODUCT_PROOF.md`. WEB-003 is terminally accepted under `tasks/WEB-003_PUBLIC_SITE_DEPTH.md` at implementation HEAD `3670d43bece4ffba657a3d9645cbea20c7e698bf` after one bounded Product review revision. No new Product/Science semantics were introduced by the revision. WEB-004 is the next task and requires deliberate CTO start approval after Product publication.

## Current state (WEB-003 accepted)

Five public routes extend the homepage into a complete small public site, each as a real static directory (`<route>/index.html`, canonical trailing-slash URL):

- `/platform/` — the accepted workflow (AOI → source/context → evidence → explicit data gaps → integrated priority → investigation decision support) as an editorial numbered list.
- `/solutions/` — the application portfolio (Geothermal active first application; Mineral and Environmental & Land Intelligence as expansion directions), reusing the homepage's own copy and status labels.
- `/pilot/` — the Kızıldere first-application proof in depth, reusing the accepted WEB-002 proof imagery and the structure/geology data-gap panel with the same checksums and mandatory EN/TR warnings.
- `/company/` — company/about destination: OrbGSS identity, VirgaSoft parent attribution, operating principles and restrained expansion framing.
- `/contact/` — three mailto conversation starters (pilot, partnership, technical) plus the direct address; no form, backend, analytics or PII capture.

The homepage and every deeper route share one persistent header/footer navigation. `vercel.json` serves trailing-slash canonical URLs; `sitemap.xml` lists all six canonical routes. Language choice persists across routes through the shared `localStorage` key. The validator checks route metadata, internal/cross-page links, sitemap coverage, EN/TR parity, accessibility-label localization, pilot social-preview truthfulness and the unchanged WEB-002 scientific provenance/checksum/warning invariants.

The MER-91 bounded Product review revision closed three findings before acceptance: every human-readable `aria-label` on canonical routes is now bound to `data-i18n-aria-label`; `/pilot/` uses the accepted Kızıldere `assets/proof/geothermal-1400.webp` derivative for Open Graph instead of the unrelated Crater Lake hero; repository authority/status pointers were reconciled. Validator result remained PASS with 0 warnings and the implementation reported 185 site-wide i18n keys.

## Current state (WEB-002 accepted)

The homepage tells the evidence-to-intelligence story on one real area of interest. The rhythm is unchanged — dark technical beam → large full-width visual panel — and every scientific story panel shows the same Kızıldere pilot AOI (36 × 36 km, EPSG:32635, 30 m grid).

1. navigation: Platform → Solutions⌄ → Pilot → Company → Contact → EN | TR
2. hero: static Crater Lake poster (`data-hero-slot="static-poster"`; final integration remains downstream)
3. `01 Observe` → Kızıldere AOI — accepted MVP project context
4. `02 Terrain` → Elevation — NASADEM context
5. `03 Evidence` → keyboard-accessible THM-01 / ALT-01 / ALT-02 switch
6. `04 Structure` → explicit public data gap
7. `05 Priority` → Remote-Sensing Relative Priority — Experimental Baseline, 0–100 within-AOI ranking
8. `06 Geothermal` → Kızıldere first-application composite
9. Pilot ledger, Company/Trust, Contact, footer

## Product-proof provenance

Every scientific visual is an OrbGSS cartographic export materialized through the accepted GEO-039 Workbench export path from persisted `kizildere_mvp_v2`, then cropped/resized for the web. `assets/imagery/sources.json` (`web_002.proof_assets`) records export identity, export manifest pointer, master SHA-256, derivative crop/size and derivative SHA-256. `scripts/validate_site.py` recomputes shipped derivative checksums.

`05 Priority` and `06 Geothermal` use accepted `mvp_remote_sensing_priority_v1` output from run `8716e89324ff5566859f470f207d5a1f0ab651c19d9c7e9dba3087960a63cf3c` under `remote_sensing_equal_family_v1`: deterministic 0–100 within-AOI screening/ranking, never probability, Full Prospectivity, reserve, discovery or drilling-success. Mandatory warning semantics remain visible in EN/TR.

`04 Structure` / geology remain `DATA_GAP / optional support / score-invariant`: no public-safe fault or lithology master is authorized and nothing is fabricated to fill the gap.

## Locked design decisions

- Full-width high-resolution EO/product imagery remains the core visual system.
- Scientific proof imagery stays clean; no fake GIS controls, HUD chrome or decorative overlays that imply functionality.
- Product-proof rasters and score ramp must preserve accepted scientific rendering; no color/contrast/opacity reinterpretation.
- Same-AOI proof panels maintain one-ground framing.
- Mandatory scientific warnings remain visible and validator-enforced.
- Secondary monospace is reserved for coordinates, evidence labels, metadata/status and technical descriptors.
- Navigation order remains Platform → Solutions → Pilot → Company → Contact → EN | TR.
- EN default / TR second language; no flags/framework.
- No unsupported customer, partner, revenue, ROI, accuracy, AI-performance or production-deployment claims.
- Later R7 public visual/palette authority may simplify/recompose the final homepage story only under its downstream integration authority; WEB-004 hardening must not silently redesign the accepted WEB-003 site.

## Product positioning

OrbGSS is a geospatial-intelligence platform. Geothermal Exploration is the active first application/pilot. Mineral Exploration and Environmental & Land Intelligence are expansion directions and remain labelled as such.

## Production blockers

1. Confirm `contact@orbgss.com` ownership before public launch, or retain an explicit release gate.
2. WEB-004 and WEB-005 remain incomplete.
3. Hosted preview/performance/accessibility acceptance is owned by WEB-004.
4. WEB-006 only: connect `orbgss.com` / `www.orbgss.com` through Squarespace DNS while preserving Google Workspace MX/SPF/DKIM/DMARC and unrelated records.

## Next canonical task

WEB-003 is **ACCEPTED / COMPLETE** at implementation HEAD `3670d43bece4ffba657a3d9645cbea20c7e698bf`. The next task is WEB-004 — responsive, accessibility, performance and hosted preview acceptance. Product may publish its exact task authority, but implementation must not start until deliberate CTO approval. WEB-005 final cinematic hero integration and WEB-006 production DNS cutover remain deferred.

## History

- ORBWEB-001 (2026-09-09): production imagery from USGS Landsat Collection 2 Level-2, provenance pinned.
- ORBWEB-001.1 (2026-09-09): on-image labels, right-aligned navigation with Solutions dropdown, EN/TR.
- ORBWEB-002A (2026-09-10): GitHub publication to `baran-orbgss/website`.
- WEB-001 (2026-09-15): vNext foundation accepted at `677bfa7672ac18c2c808ddaaf235ff12863de443`.
- WEB-002 (2026-09-15): public-safe GEO-039 proof exports, Kızıldere evidence/prospectivity presentation and provenance/checksum enforcement accepted after one bounded Product review revision; implementation HEAD `a10cc141e3a7830c5e3c67a22e950ab16c0fe92b`.
- WEB-003 (2026-09-15): `/platform/`, `/solutions/`, `/pilot/`, `/company/`, `/contact/`; cross-route EN/TR, metadata, sitemap/link validation and reuse of accepted Kızıldere proof. Initial implementation `5d99eb811dfbb3396ebade17ff6ab863b5463a35`.
- WEB-003 bounded Product review revision (2026-09-15): accessibility-label localization guard, truthful Kızıldere pilot social preview and authority/status reconciliation; final implementation HEAD `3670d43bece4ffba657a3d9645cbea20c7e698bf`; Product accepted and fast-forwarded canonical main non-destructively.
