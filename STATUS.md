# OrbGSS Website — CURRENT

**Canonical version:** `v0.7.1-web-002-review-revision` — WEB-002 accepted
**Date:** 2026-09-15
**Stage:** WEB-002 product proof accepted after bounded Product review revision; WEB-003 is next planned task and is not started
**Site architecture:** static HTML + CSS + vanilla JavaScript
**Public domain target:** `https://orbgss.com`
**Canonical repository:** https://github.com/mertkaanakgunlu-debug/orbgss-website
**Accepted WEB-002 implementation HEAD:** `a10cc141e3a7830c5e3c67a22e950ab16c0fe92b`
**Reference/upstream only:** https://github.com/baran-orbgss/website
**Science authority:** `mertkaanakgunlu-debug/geothermal-prospectivity@215ef89d794cf6cbf98e94f8fc17184c859ebcd8` (tag `v1.0.0`)
**Registrar / DNS:** Squarespace
**Hosting target:** Vercel
**Company:** VirgaSoft
**Product:** OrbGSS — Orbital Geo-Spatial Solutions
**Product authority:** OrbGSS Website vNext Product & Execution Authority v1.5 (`docs/WEB_VNEXT_AUTHORITY.md`)
**Tracking:** Linear MER-90 (WEB-002 accepted/complete); MER-96 / GEO-WEB-001 resolved

## Authority

`docs/WEB_VNEXT_AUTHORITY.md` is the repository-local summary of the product-owned *OrbGSS Website vNext Product & Execution Authority v1.5*. Where it disagrees with `docs/DESIGN_AUTHORITY.md` or `docs/PRODUCT_AND_CONTENT_AUTHORITY.md`, it wins for vNext work. WEB-002 is terminally accepted under `tasks/WEB-002_PRODUCT_PROOF.md`; the next planned contract is WEB-003 and must not be started without deliberate CTO approval.

## Current state (WEB-002 accepted)

The homepage tells the evidence-to-intelligence story on one real area of interest. The rhythm is
unchanged — dark technical beam → large full-width visual panel — but every story panel now shows
the **same Kızıldere pilot AOI** (36 × 36 km, EPSG:32635, 30 m grid), so the reader watches one
place accumulate evidence instead of touring six unrelated places.

1. navigation (right-aligned: Platform → Solutions⌄ → Pilot → Company → Contact → EN | TR)
2. hero: static Crater Lake poster, unchanged (`data-hero-slot="static-poster"`; WEB-005 owns it)
3. `01 Observe` → Kızıldere AOI — accepted MVP project context (`top-dem`, greyscale)
4. `02 Terrain` → Elevation — NASADEM context (`top-dem`, batlow terrain)
5. `03 Evidence` → keyboard-accessible layer switch across THM-01 / ALT-01 / ALT-02
6. `04 Structure` → **explicit data gap**, no image published
7. `05 Priority` → Remote-Sensing Relative Priority — Experimental Baseline, with its 0–100 legend
8. `06 Geothermal` → Kızıldere first-application composite (`top-dem` + score)
9. Pilot ledger, Company/Trust, Contact beam, footer — unchanged

Every visible string exists in EN and TR (`I18N` in `script.js`): 112 keys per language.

## Product-proof provenance

Every scientific visual is an OrbGSS cartographic export materialized through the accepted GEO-039
Workbench export path from the persisted `kizildere_mvp_v2` project, then cropped and resized for
the web. `assets/imagery/sources.json` (`web_002.proof_assets`) records, per asset: the export id,
the `export_manifest.json` pointer, the master PNG SHA-256 from that manifest, the crop box, and a
SHA-256 for every derivative shipped in this repository. `scripts/validate_site.py` recomputes
those derivative checksums on every run, so provenance is self-enforcing.

`05 Priority` and `06 Geothermal` use the accepted `mvp_remote_sensing_priority_v1` output from run
`8716e89324ff5566859f470f207d5a1f0ab651c19d9c7e9dba3087960a63cf3c` under
`remote_sensing_equal_family_v1`, published with its exact accepted semantics: a deterministic
0–100 within-AOI screening surface, never probability, Full Prospectivity, reserve, discovery or
drilling-success. Each panel carries its mandatory package warning as visible EN/TR copy.

`04 Structure` and geology stay an explicit `DATA_GAP / optional support / score-invariant` state:
no public-safe fault or lithology master is authorized, the page says so, and the copy records that
the absence does not change the baseline. Nothing is fabricated to fill it.

The three Landsat scenes no longer placed on the homepage (Yellowstone, Chuquicamata, Ili Delta)
are marked `retired-from-homepage` with files, provenance and rights intact.

## Locked design decisions

- Full-width, high-resolution Earth-observation imagery is the primary visual system.
- Except for the hero, imagery stays clean: no cards, floating UI, map controls, pins, grids, diagrams or overlay copy.
- Story copy lives on the dark technical beams: index, uppercase title, one or two sentences, monospace descriptor.
- Every image shows its real location and coordinates directly on the image, bottom-right, bare monospace text. The third line names what the layer is: the accepted public label on a product-proof panel (`Natural-color composite` applies only to Landsat gallery imagery, which the story panels no longer use). No metadata strip below any image.
- Product-proof rasters and the score colour ramp are published exactly as the accepted GEO-039 export rendered them: no saturation, contrast, brightness or opacity change. The gallery grade remains on the hero only.
- All story panels render the same Kızıldere AOI, so their framing is identical. Per-slot `object-position` crops belonged to WEB-001's four different scenes and must not return.
- Every proof asset's mandatory scientific warning is carried in visible page copy, in EN and TR and in the static HTML, and the validator enforces that wording.
- Secondary monospace treatment is reserved for coordinates, evidence labels, metadata, status tags and technical descriptors.
- Desktop navigation order is fixed: Platform → Solutions (Geothermal Exploration, Mineral Exploration, Environmental & Land Intelligence) → Pilot → Company → Contact → EN | TR, right-aligned. All destinations are real anchors.
- Bilingual (EN default, TR) through the client-side dictionary; no flags, no framework.
- No `How it works` section, icon wall, SaaS card grid, fake dashboard, HUD chrome, stock photography or globe in the logo mark.
- Dark, restrained, scientific/EO aesthetic; desktop stays wide and cinematic.

## Product positioning

OrbGSS is a geospatial-intelligence platform. Geothermal Exploration is the first active application (pilot). Mineral Exploration and Environmental & Land Intelligence are expansion directions and are labelled as such. No customer, partner, revenue, ROI, accuracy, AI-performance or production-deployment claims.

## Production blockers

1. Confirm `contact@orbgss.com` before public launch.
2. WEB-003, WEB-004 and WEB-005 remain incomplete.
3. Vercel preview/acceptance is owned by WEB-004.
4. WEB-006 only: connect `orbgss.com` / `www.orbgss.com` through Squarespace DNS, preserving Google Workspace MX/SPF/DKIM/DMARC.

## Next canonical task

WEB-002 is **ACCEPTED / COMPLETE** at implementation HEAD `a10cc141e3a7830c5e3c67a22e950ab16c0fe92b`. The next planned task is WEB-003 (public-site depth, credibility, conversion and bilingual content). Publication/preparation may occur under Product ownership, but implementation does not start without deliberate CTO approval. WEB-005 (cinematic hero) and WEB-006 (DNS cutover) remain deferred.

## History

- ORBWEB-001 (2026-09-09): production imagery from USGS Landsat Collection 2 Level-2, provenance pinned.
- ORBWEB-001.1 (2026-09-09): on-image labels, right-aligned navigation with Solutions dropdown, EN/TR.
- ORBWEB-002A (2026-09-10): GitHub publication to `baran-orbgss/website`.
- WEB-001 (2026-09-15): vNext authority published; homepage shell, story sections, pilot ledger, company/trust, contact; navigation and hero renewed; validator extended. Accepted at `677bfa7`.
- WEB-002 (2026-09-15): Science package MER-96 resolved; seven GEO-039 proof exports materialized and published with checksummed provenance; evidence layer switch; structure/geology data-gap state; validator now verifies proof provenance.
- WEB-002 review revision (2026-09-15): removed CSS colour/contrast/opacity transforms from the scientific rasters and the score ramp; unified AOI framing across all story panels; restored THM-01 warning semantics in EN/TR and in the static HTML; reconciled the no-JS footer attribution and the two asset-class policies; validator now enforces visible warning coverage.
- WEB-002 terminal Product acceptance (2026-09-15): accepted implementation HEAD `a10cc141e3a7830c5e3c67a22e950ab16c0fe92b`; no new Science/Product semantics introduced.
