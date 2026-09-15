# OrbGSS Website — CURRENT

**Canonical version:** `v0.9.0-web-004-preview-hardening` — WEB-004 REVIEW_READY
**Date:** 2026-09-16
**Stage:** WEB-004 responsive/accessibility/performance hardening implemented on `feat/web-004-preview-hardening` from accepted `main@f4d77b4144ddff70c309986e6a45b163f62cdcd4`; REVIEW_READY at implementation HEAD `56cb530`, not merged. Awaiting Product review and terminal acceptance.
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
**Tracking:** Linear MER-90 (WEB-002 accepted/complete); MER-91 (WEB-003 accepted/complete); MER-92 (WEB-004 implemented, REVIEW_READY); MER-96 / GEO-WEB-001 resolved

## Authority

`docs/WEB_VNEXT_AUTHORITY.md` is the repository-local summary of the product-owned *OrbGSS Website vNext Product & Execution Authority* (v1.8). Where it disagrees with `docs/DESIGN_AUTHORITY.md` or `docs/PRODUCT_AND_CONTENT_AUTHORITY.md`, it wins for vNext work. WEB-002 is terminally accepted under `tasks/WEB-002_PRODUCT_PROOF.md`. WEB-003 is terminally accepted under `tasks/WEB-003_PUBLIC_SITE_DEPTH.md` at implementation HEAD `3670d43bece4ffba657a3d9645cbea20c7e698bf` after one bounded Product review revision. No new Product/Science semantics were introduced by the revision. WEB-004 is published under `tasks/WEB-004_PREVIEW_HARDENING.md` (authority publication `3a4d8e006add2725d45b02071bda654be5bd09f5`), received CTO start approval, and is implemented on `feat/web-004-preview-hardening` at `REVIEW_READY`. Product performs terminal acceptance/merge.

## Current state (WEB-004, REVIEW_READY)

WEB-004 hardened the accepted six-route site without redesigning it. Full measurements, tooling
versions and negative tests are in `docs/WEB-004_HARDENING_EVIDENCE.md`.

- **Performance.** Homepage Lighthouse Performance 77 → **94**; LCP 6.5 s → 3.2 s; CLS 0; TBT 0 ms. Total page transfer **1369.6 KiB → 645.1 KiB (−53%)**. All six routes clear Accessibility / Best Practices / SEO ≥ 95, and Performance ≥ 90 on the homepage and every deep route.
- **Hero delivery.** Three recorded WebP derivatives (900 / 1400 / 1800) plus `srcset`/`sizes` and a matching preload; a 375 px phone fetches ~148 KiB instead of 553 KiB. Resize-and-encode only, checksummed in `assets/imagery/sources.json`, validator-enforced. The hero visual itself is untouched and still belongs to WEB-005.
- **Inactive evidence layers deferred** behind `data-src`/`data-srcset` and promoted as the section approaches the viewport — 340 KiB off the initial load, switching still instant, provenance still enforced.
- **Caption contrast is now measured per viewport.** `object-fit: cover` re-crops each proof raster as the viewport changes shape, so the WEB-002 hand-chosen tones fell to 2.84 / 3.53 / 4.21:1 at some widths. The accepted rule is now applied continuously between the same two accepted tones; every caption clears 4.5:1 at 375 / 768 / 1024 / 1440 (worst case 4.58:1). No raster is modified, and the caption remains bare monospace text with no card, box or band.
- **Accessibility.** Viewport-change reset for the mobile menu and Solutions disclosure; WCAG 2.5.8 touch targets (footer nav, direct email, brand, desktop EN/TR); `/contact/` heading order corrected (route Accessibility 98 → 100); real web-manifest icon. Zero horizontal overflow and zero undersized targets across all six routes at all four widths.
- **Gates.** `HOSTED_PREVIEW_NOT_RUN - permission unavailable` (no Vercel CLI, project link or token present; no credentials requested, no account state touched), with a reproducible local preview. `CONTACT_RELEASE_GATE` retained: every mailto correctly targets `contact@orbgss.com` in both languages, but mailbox ownership cannot be proven without Workspace access.
- **Routed to Product, not silently relaxed.** Homepage LCP is 3.2 s against the 2.5 s target; the residual is `assets/proof/priority-800.webp` (249.7 KiB), an accepted checksummed proof derivative WEB-004 may not re-encode. Closing it needs either authority to re-export proof derivatives at web scale or explicit acceptance of 3.2 s under this synthetic profile. Separately, `image-aspect-ratio` still flags the deliberately squashed score legend (Best Practices 96, above its ≥ 95 floor), recorded as an accepted deviation.

### WEB-005 hero media budget (adopted from measurement)

Tightened from the Product defaults where the evidence supports it:

| Asset | Ceiling |
| --- | --- |
| Desktop autoplay WebM | ≤ 3.0 MiB (default was 4 MiB) |
| MP4 fallback | ≤ 4.5 MiB (default was 6 MiB) |
| Poster still | ≤ 180 KiB (default was 500 KiB) |
| Mobile / reduced-data | poster only, no video encode |

Hard constraints: one encode per client, ever; the poster stays the preloaded LCP element with
`imagesrcset`/`imagesizes` matching the `<img>`; `prefers-reduced-motion: reduce` gets the static
poster; the bottom-right caption region must keep ≥ 4.5:1 (today 6.84:1 against the image alone,
and the hero caption is deliberately outside the runtime tone system because `.hero-shade` sits
between raster and text); and any hero media must be recorded and checksummed like the derivatives
above.

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

1. `CONTACT_RELEASE_GATE` — confirm `contact@orbgss.com` ownership and deliverability before public launch. Route/mailto correctness is verified; mailbox ownership is not, and cannot be from this repository.
2. WEB-004 is REVIEW_READY and awaiting Product acceptance; WEB-005 remains incomplete.
3. `HOSTED_PREVIEW_NOT_RUN` — a hosted Vercel preview still needs to be produced under already-authorized credentials; WEB-004 recorded a reproducible local preview instead.
4. Product decision outstanding: accept homepage LCP 3.2 s under the synthetic mobile profile, or authorize re-export of the proof derivatives at web scale.
5. WEB-006 only: connect `orbgss.com` / `www.orbgss.com` through Squarespace DNS while preserving Google Workspace MX/SPF/DKIM/DMARC and unrelated records.

## Next canonical task

WEB-004 is implemented and **REVIEW_READY** on `feat/web-004-preview-hardening`. Product performs terminal review and acceptance; two decisions are routed with it (homepage LCP 3.2 s versus the 2.5 s target, and the score-legend `image-aspect-ratio` deviation). After acceptance: WEB-005 final cinematic hero integration, which now has an explicit measured media budget above. WEB-006 production DNS cutover remains deferred behind an explicit CTO human gate.

## History

- ORBWEB-001 (2026-09-09): production imagery from USGS Landsat Collection 2 Level-2, provenance pinned.
- ORBWEB-001.1 (2026-09-09): on-image labels, right-aligned navigation with Solutions dropdown, EN/TR.
- ORBWEB-002A (2026-09-10): GitHub publication to `baran-orbgss/website`.
- WEB-001 (2026-09-15): vNext foundation accepted at `677bfa7672ac18c2c808ddaaf235ff12863de443`.
- WEB-002 (2026-09-15): public-safe GEO-039 proof exports, Kızıldere evidence/prospectivity presentation and provenance/checksum enforcement accepted after one bounded Product review revision; implementation HEAD `a10cc141e3a7830c5e3c67a22e950ab16c0fe92b`.
- WEB-003 (2026-09-15): `/platform/`, `/solutions/`, `/pilot/`, `/company/`, `/contact/`; cross-route EN/TR, metadata, sitemap/link validation and reuse of accepted Kızıldere proof. Initial implementation `5d99eb811dfbb3396ebade17ff6ab863b5463a35`.
- WEB-003 bounded Product review revision (2026-09-15): accessibility-label localization guard, truthful Kızıldere pilot social preview and authority/status reconciliation; final implementation HEAD `3670d43bece4ffba657a3d9645cbea20c7e698bf`; Product accepted and fast-forwarded canonical main non-destructively.
- WEB-004 (2026-09-16): responsive/accessibility/performance hardening of the accepted six-route site — homepage Lighthouse Performance 77 → 94, page transfer −53%, measured per-viewport caption tone, viewport-change disclosure reset, WCAG 2.5.8 touch targets, `/contact/` heading order, validator extended to responsive and deferred imagery. `HOSTED_PREVIEW_NOT_RUN` and `CONTACT_RELEASE_GATE` recorded. Implemented on `feat/web-004-preview-hardening` from accepted `main@f4d77b4144ddff70c309986e6a45b163f62cdcd4`; implementation HEAD `56cb530`; REVIEW_READY, not merged.
