# OrbGSS Website — CURRENT

**Canonical version:** `v1.0.0-rc3-web-005a-hero-visual-revision` — WEB-005A R3 `REVISION_REQUIRED`; second preview gate submitted (release candidate unchanged)
**Date:** 2026-09-18
**Stage:** WEB-005A / MER-107 is in **`REVISION_REQUIRED`** after Product/CTO human visual review of `37152222` (`docs/web-005-polish-authority@473b48a00bfe85d3dbe1cfe7219105c2b5ec7574:tasks/WEB-005A_R3_REVIEW_37152222.md`): the camera moved before the scan completed (A-HERO-15), the platform sat under the hero copy on the real 1440 × 900 page, and the analytical reveal was a planar page overlay rather than DEM relief (A-HERO-18/19). The review requires a low-cost **preview gate** before any further long production render. The first preview (`tasks/WEB-005A_R3_PREVIEW_GATE.md`, `cd2018e`, evidence `hero/evidence/web005a_r3_preview/`) was reviewed `PREVIEW_GATE_REVISION_REQUIRED / CONTINUATION_AUTHORIZED` (`docs/web-005-polish-authority@c7c6cb10e305c9de63d805c414b332440fd87ddb:tasks/WEB-005A_R3_PREVIEW_GATE_PRODUCT_DECISION.md`): the four primary lines must end on the true governed 36 km corners, the presentation reticle must be separate from true ground geometry, the platform exit must stay inside the 22 % fly-by bound, the final payoff must be protected from the left readability shade, and the shipping envelope is about 12 s of motion plus a 2.4–3.2 s analytical sequence. Product then added six clarifications (settle → aim → draw-on sequencing, lines that propagate, thinner line language, a cyan / teal scan palette, no hero colour bar or information card, brisker timing). The corrected **second preview is now submitted**: `tasks/WEB-005A_R3_PREVIEW_GATE_2.md` (same scene `hero_r3_preview_gate`, evidence `hero/evidence/web005a_r3_preview2/`). It changes no site file, no shipped media and not the production scene; WEB-005A returns to `REVIEW_READY` only after the gate is passed, the conforming production output is rendered and the integrated homepage is re-submitted. *The remainder of this paragraph describes the reviewed R3 checkpoint, which is what the branch still ships:* WEB-005A (hero visual revision, Product R2 visual lock as re-reviewed) was published `REVIEW_READY` at **R3** on `feat/web-005a-hero-visual-fidelity`. The R2 package (`a6897828d6e35595ea5a9a39a1e812b0fcbbfb35`) was technically green and did **not** pass the human visual gate; like the `ffa2f2944ca5992afb9e9891b42745a9bd1105ad` checkpoint before it, it is retained as before-evidence and is not accepted. R3 re-choreographs the same hero: a satellite that comes round the limb and settles for the whole acquisition beat, sensing lines that release while it is still in frame, one continuous dive onto the accepted 36 km analysis AOI with its own lock event, 30 m ground structure under the hold, and a page-layer evidence sequence (terrain → THM-01 → ALT-01 → priority) registered inside the analysis frame. Evidence: `tasks/WEB-005A_HERO_FIDELITY_EVIDENCE.md`. **Not merged to `main`. Nothing deployed. No DNS touched. WEB-005B and WEB-006 have not begun.**
**Site architecture:** static HTML + CSS + vanilla JavaScript
**Public domain target:** `https://orbgss.com`
**Canonical repository:** https://github.com/mertkaanakgunlu-debug/orbgss-website
**Accepted WEB-002 implementation HEAD:** `a10cc141e3a7830c5e3c67a22e950ab16c0fe92b`
**Accepted WEB-003 implementation HEAD:** `3670d43bece4ffba657a3d9645cbea20c7e698bf`
**Accepted WEB-004 implementation HEAD:** `56cb53039b85a852110c737505bc2ae2282acb08`
**Accepted GEO-WEB-002 implementation HEAD:** `ea693c29762279131fbed005e832c5ff2dca587b`
**Accepted WEB-005 terminal acceptance:** `main@00af0f232a8d7d77f5ca61d758461ff7316ba151` (`tasks/WEB-005_TERMINAL_PRODUCT_ACCEPTANCE.md`)
**WEB-005A rejected checkpoint (before-evidence):** `ffa2f2944ca5992afb9e9891b42745a9bd1105ad`
**WEB-005A R2 package (superseded, did not pass the human visual gate):** `a6897828d6e35595ea5a9a39a1e812b0fcbbfb35` (implementation `b285c90cf685f6ca9da61c41302ae496d7e8169b`)
**WEB-005A R3 implementation HEAD (reviewed, `REVISION_REQUIRED`):** `37152222c33fdc09265ba022ce45828c8d002723`
**WEB-005A R3 preview gate 1:** `tasks/WEB-005A_R3_PREVIEW_GATE.md` at `cd2018e` — reviewed, `PREVIEW_GATE_REVISION_REQUIRED` (before-evidence)
**WEB-005A R3 preview gate 2:** `tasks/WEB-005A_R3_PREVIEW_GATE_2.md` — `PREVIEW_GATE_2_SUBMITTED`, awaiting Product/CTO; no production render made
**Reference/upstream only:** https://github.com/baran-orbgss/website
**Science authority:** `mertkaanakgunlu-debug/geothermal-prospectivity@215ef89d794cf6cbf98e94f8fc17184c859ebcd8` (tag `v1.0.0`)
**Registrar / DNS:** Squarespace
**Hosting target:** Vercel
**Company:** VirgaSoft
**Product:** OrbGSS — Orbital Geo-Spatial Solutions
**Product authority:** OrbGSS Website vNext Product & Execution Authority v1.8 (`docs/WEB_VNEXT_AUTHORITY.md`); `docs/WEB_005_POLISH_VISUAL_DIRECTION_AUTHORITY.md` (R2 visual lock) where newer.
**Accepted WEB-HERO-001D evidence HEAD:** `e95fdcac7cac82e597d40dab4cdc96ce1a6b319e` (terminal Product acceptance published at `573f4f1`)
**WEB-005 execution baseline:** `main@d2421a772f2e4cfa38c85dd5ee71a419c5160838`
**Tracking:** MER-90 (WEB-002 accepted); MER-91 (WEB-003 accepted); MER-92 (WEB-004 accepted); MER-102 / GEO-WEB-002 (Science-accepted); MER-101 / WEB-HERO-001D (terminally accepted); MER-93 / WEB-005 (terminally accepted); **MER-107 / WEB-005A (REVISION_REQUIRED after R3 review; second preview gate submitted)**; MER-96 / GEO-WEB-001 resolved

## Authority

`docs/WEB_VNEXT_AUTHORITY.md` is the repository-local summary of the product-owned *OrbGSS Website vNext Product & Execution Authority*. Where it disagrees with newer canonical Drive Product authority, the current Drive authority wins. WEB-002 is terminally accepted under `tasks/WEB-002_PRODUCT_PROOF.md`. WEB-003 is terminally accepted under `tasks/WEB-003_PUBLIC_SITE_DEPTH.md` at implementation HEAD `3670d43bece4ffba657a3d9645cbea20c7e698bf` after one bounded Product review revision. WEB-004 is terminally Product-accepted under MER-92 at implementation HEAD `56cb53039b85a852110c737505bc2ae2282acb08`; canonical acceptance publication is `716104d677fea5021787b581470a436ed708f3a3` and acceptance record is `docs/WEB-004_PRODUCT_ACCEPTANCE.md`.

`docs/WEB_PUBLIC_VISUAL_NARRATIVE_AUTHORITY.md` locks the final four-act homepage story for WEB-005 and supersedes the repeated full-width proof-scene rhythm where they conflict; it does not supersede accepted Science semantics, WEB-002 provenance constraints, WEB-004 performance/accessibility decisions or the accepted route architecture. GEO-WEB-002 / MER-102 is the Science & Geospatial publication dependency it named. It is terminally accepted under `docs/GEO-WEB-002_SCIENCE_ACCEPTANCE.md` at implementation HEAD `ea693c29762279131fbed005e832c5ff2dca587b`. Product may bind the package into WEB-005 while preserving its exact labels, warnings, provenance and maximum-safe-render constraints.

## Current state (WEB-005A R3 as reviewed — `REVISION_REQUIRED`; this is what the branch still ships)

WEB-005A revises only the hero's rendered media, the hero production configuration that generates it,
the page-layer handoff, and one footer attribution sentence. The four-act homepage and every accepted
scientific asset, label and warning are unchanged and re-verified.

- **Satellite.** The R2 procedural generic EO platform, on a **time-remapped derived orbit**
  (`orbit_intent.rate_profile`): hidden for the first two seconds, round the lower-left limb near
  frame 55, then held at (0.25, 0.40) of the frame — lower-left of the target, 13 % of the frame
  width — from frame 136 to 192, because the camera is locked off for the same frames. It is left
  behind by the dive and never becomes a foreground fly-by.
- **Acquisition.** Four thin cyan lines connect (110–124), the 420 km frame locks with a 2.6× pulse
  while its corner locks draw in (128–144), a sweep band crosses it (144–178), and the lines release
  with an acquisition-complete pulse at 178–192 **while the satellite is still in frame**.
- **Dive and hold.** One eased, motion-blurred dive (192–262) on the same registered target. The
  regional frame vanishes as its edges leave; the **accepted 36 × 36 km analysis AOI** draws in as
  its own frame with a lock pulse and settles. The hold (262–276) is genuinely still: 166 km across
  the frame, the AOI 23 % of the frame width.
- **Earth.** Same model, lighting and atmosphere; Blue Marble colour everywhere, multiplied under the
  hold by a 30 m **Sentinel-2-derived detail ratio** (structure only) with the cloud veil cleared over
  that window. Structure is sampled at 0.35× at the hold (`hero/evidence/texel_coverage.json`);
  attribution *Contains modified Copernicus Sentinel data (2025)* is in the footer.
- **Handoff.** The page maps the accepted derivatives **inside the analysis frame** with a CSS
  homography on the audited corners and reveals Elevation → THM-01 → ALT-01 → priority, each
  byte-exact under its exact label and accepted warning, ending on the priority result with its own
  legend. The stack never exceeds 1249 device pixels. No faults layer is shown: structure/geology
  remains the stated data gap and nothing is fabricated for it.
- **Gates.** Site validator PASS 0 warnings; hero validator 292/292; negative tests 27/27; shot audit 18/18.

## Current state (WEB-005, ACCEPTED)

The homepage is now the locked four-act story from `docs/WEB_PUBLIC_VISUAL_NARRATIVE_AUTHORITY.md`:
**Act 1 cinematic acquisition hero → Act 2 real Kızıldere EO context → Act 3 compact evidence trio →
Act 4 priority/result climax**, followed by the subordinate pilot ledger, company/trust and contact
sections. The WEB-001/002 six-scene `beam → full-width raster` gallery is gone, and
`scripts/validate_site.py` now fails the build if it returns.

- **Act 1** is the accepted WEB-HERO-001D sequence, re-rendered against the real accepted Kızıldere
  pilot centre and packaged as production WebM / MP4 / poster. It is a **render**, and its caption
  says so in both languages: `Rendered orbital sequence — not sensor imagery`.
- **The real-data/result handoff is a page element, not a video frame.** A governed class-B raster
  inside a lossy encode would have its colours and values changed by chroma subsampling and
  quantisation, which the accepted package forbids — so the accepted priority derivative is shipped
  as its own checksummed file and composited over the hero instead. The hero scene's
  `aoi_injection_interface.layer_slots` records that decision as `render_surface: html_overlay`, and
  `hero/scripts/validate_hero.py` enforces it.
- **Safe display density is measured, not asserted.** Across a 360–3840 CSS px viewport sweep of the
  built page, the widest render of each scientific visual is: Act-2 context 1199 CSS px (2398 device
  px at 2×, ceiling 2400), each evidence card 624 (1248, ceiling 1249), the Act-4 priority map 623
  (1246, ceiling 1249), the in-frame legend 248 against a 732 px native crop. Nothing is upscaled at
  any width or density. Each figure is recorded in `geo_web_002.assets[].web_005_placement.rendered`
  and re-checked by the validator.
- **Act 4 is deliberately contained.** The accepted score raster is 1200 × 1200 cells at 30 m drawn
  at 1249 px and *cannot* reach the ≥ 2000 px Act-4 presentation target from accepted science. The
  composition carries the weight instead of the raster being stretched, and the export's own legend
  sits inside the map frame — there is no detached homepage colour bar.
- **Structure/geology stays an explicit, subordinate data gap.** Not fabricated, not promoted to an
  act, and stated as score-invariant.

Remaining gates are unchanged and are **not** WEB-005's to close: `CONTACT_RELEASE_GATE`,
`HOSTED_PREVIEW_NOT_RUN`, and the WEB-006 production DNS cutover human gate.

## Current state (GEO-WEB-002, ACCEPTED / COMPLETE)

`tasks/GEO-WEB-002_FINAL_HOMEPAGE_VISUAL_MASTERS.md` is implemented and terminally accepted. The canonical package is
`docs/GEO-WEB-002_FINAL_VISUAL_MASTER_PACKAGE.md` (`READY_FOR_PRODUCT_BINDING`), mirrored
machine-readably in `assets/imagery/sources.json` → `geo_web_002`. Nothing is placed on a public route:
this publishes the visual masters the locked four-act homepage in
`docs/WEB_PUBLIC_VISUAL_NARRATIVE_AUTHORITY.md` needs, for WEB-005 to bind under its own authority.

- **Act 2 — real AOI context.** One natural-colour Landsat 8 OLI composite of the Kızıldere AOI in its
  regional setting: `LC08_L2SP_179034_20250505_02_T1`, acquired 2025-05-05, 0.90 % cloud, rendered by the
  existing `scripts/build_imagery.py` grammar at native 30 m into a 2400 × 1500 px (72 × 45 km) EPSG:32635
  frame with 100 % valid coverage, plus 2400 / 1800 / 1200 / 900 WebP candidates.
- **Acts 3 and 4 — cartographic masters.** `terrain`, `thm01`, `alt01`, `alt02` and `priority` resolve to
  their accepted GEO-039 exports of persisted `kizildere_mvp_v2`. Each ships the rendered map panel as a
  crop with **no resampling at all** (1249 px), an 800 px card derivative, and a native-resolution lossless
  crop of the master's own governed legend — so a necessary legend can sit inside the map frame instead of becoming a
  detached homepage colour bar.
- **Resolution ceiling.** The accepted grid is 1200 × 1200 cells at 30 m and the accepted renderer draws it
  at 1249 px, so **1249 device pixels** is the maximum honest rendered width for any cartographic asset.
  Act 2 meets its ≥ 2000 px target natively and the evidence cards meet ≥ 1200 px. The Act-4 priority master
  **cannot** reach ≥ 2000 px from accepted science: the package publishes the exact ceiling instead of
  upscaling, and WEB-005 must give Act 4 a contained composition (1249 CSS px at 1×, approximately 624 CSS px at 2×).
- **Findings WEB-005 must not "fix".** ALT-01/ALT-02 render as dark fields with bright anomalies — their
  registry-approved style normalizes linearly over the full value range, so ~87 % of valid cells sit in
  the lowest fifth of the ramp. No re-stretch, re-normalize or CSS colour/contrast adjustment. NoData (0.0–5.5 % per panel)
  stays visible. ALT-01 is the preferred single alteration card under the accepted package.
- **Enforcement.** `scripts/build_final_visual_masters.py` rebuilds every derivative deterministically and
  refuses an altered master, a wrong-layer export, a wrong 1200 × 1200 source grid or any presentation upscale beyond the accepted renderer-native panel. `scripts/validate_site.py` recomputes all
  19 derivative checksums plus the class-A master and enforces the publication record,
  including each asset's declared no-upscale ceiling. REVIEW_READY evidence records validator PASS, 0 warnings; `git diff --check` green; negative tests and byte-for-byte rebuild PASS.
- **No semantic change.** Mandatory core remains THM-01 + ALT-01 + ALT-02; fail-closed behaviour,
  terrain-as-context, the structure/geology `DATA_GAP`, CRS/grid/unit/NoData/mask/resampling semantics and
  every public label and mandatory warning are carried from `docs/WEB-002_SCIENCE_ASSET_PACKAGE.md`.
  No structure or geology asset is published; nothing is fabricated to fill that gap.

## Current state (WEB-004 accepted / complete)

WEB-004 hardened the accepted six-route site without redesigning it. Full measurements, tooling
versions and negative tests are in `docs/WEB-004_HARDENING_EVIDENCE.md`; terminal Product acceptance is in `docs/WEB-004_PRODUCT_ACCEPTANCE.md`.

- **Performance.** Homepage Lighthouse Performance 77 → **94**; LCP 6.5 s → 3.2 s; CLS 0; TBT 0 ms. Total page transfer **1369.6 KiB → 645.1 KiB (−53%)**. All six routes clear Accessibility / Best Practices / SEO ≥ 95, and Performance ≥ 90 on the homepage and every deep route.
- **Hero delivery.** Three recorded WebP derivatives (900 / 1400 / 1800) plus `srcset`/`sizes` and a matching preload; a 375 px phone fetches ~148 KiB instead of 553 KiB. Resize-and-encode only, checksummed in `assets/imagery/sources.json`, validator-enforced. The hero visual itself is untouched and still belongs to WEB-005.
- **Inactive evidence layers deferred** behind `data-src`/`data-srcset` and promoted as the section approaches the viewport — 340 KiB off the initial load, switching still instant, provenance still enforced.
- **Caption contrast is measured per viewport.** `object-fit: cover` re-crops each proof raster as the viewport changes shape, so the WEB-002 hand-chosen tones fell to 2.84 / 3.53 / 4.21:1 at some widths. The accepted rule is applied continuously between the same two accepted tones; every caption clears 4.5:1 at 375 / 768 / 1024 / 1440 (worst case 4.58:1). No raster is modified, and the caption remains bare monospace text with no card, box or band.
- **Accessibility.** Viewport-change reset for the mobile menu and Solutions disclosure; WCAG 2.5.8 touch targets (footer nav, direct email, brand, desktop EN/TR); `/contact/` heading order corrected (route Accessibility 98 → 100); real web-manifest icon. Zero horizontal overflow and zero undersized targets across all six routes at all four widths.
- **Gates.** `HOSTED_PREVIEW_NOT_RUN — permission unavailable` was accepted under WEB-004 on MER-92. `CONTACT_RELEASE_GATE` **remains open** for pre-WEB-006 launch verification: every mailto correctly targets `contact@orbgss.com` in both languages, but mailbox ownership still requires Workspace/account evidence.
- **Product decisions accepted (MER-92).** Homepage LCP 3.2 s under the recorded local synthetic mobile profile is an accepted bounded WEB-004 deviation; accepted scientific proof derivatives must not be re-encoded solely to chase 2.5 s. The score-legend `image-aspect-ratio` finding is an accepted intentional deviation; the scientific legend must not be re-proportioned solely to clear the heuristic. No Product/Science semantics changed.

### WEB-005 hero media budget (ACCEPTED, MER-92)

The binding WEB-005 media envelope accepted by Product is:

| Asset | Ceiling |
| --- | --- |
| Desktop autoplay WebM | ≤ 3.0 MiB |
| MP4 fallback | ≤ 4.5 MiB |
| Poster still | ≤ 180 KiB |
| Mobile / reduced-data | intentional static/poster fallback, no dual-video download |

The engineering conditions WEB-004 measured under remain: one encode per client; the poster stays the preloaded LCP element with
`imagesrcset`/`imagesizes` matching the `<img>`; `prefers-reduced-motion: reduce` gets the static
poster; the bottom-right caption region must keep ≥ 4.5:1; and hero media must be recorded and checksummed like the accepted derivatives.

## Current state (WEB-003 accepted)

Five public routes extend the homepage into a complete small public site, each as a real static directory (`<route>/index.html`, canonical trailing-slash URL):

- `/platform/` — the accepted workflow (AOI → source/context → evidence → explicit data gaps → integrated priority → investigation decision support) as an editorial numbered list.
- `/solutions/` — the application portfolio (Geothermal active first application; Mineral and Environmental & Land Intelligence as expansion directions), reusing the homepage's own copy and status labels.
- `/pilot/` — the Kızıldere first-application proof in depth, reusing the accepted WEB-002 proof imagery and the structure/geology data-gap panel with the same checksums and mandatory EN/TR warnings.
- `/company/` — company/about destination: OrbGSS identity, VirgaSoft parent attribution, operating principles and restrained expansion framing.
- `/contact/` — three mailto conversation starters (pilot, partnership, technical) plus the direct address; no form, backend, analytics or PII capture.

The homepage and every deeper route share one persistent header/footer navigation. `vercel.json` serves trailing-slash canonical URLs; `sitemap.xml` lists all six canonical routes. Language choice persists across routes through the shared `localStorage` key. The validator checks route metadata, internal/cross-page links, sitemap coverage, EN/TR parity, accessibility-label localization, pilot social-preview truthfulness and the unchanged WEB-002 scientific provenance/checksum/warning invariants.

The MER-91 bounded Product review revision closed three findings before acceptance: every human-readable `aria-label` on canonical routes is bound to `data-i18n-aria-label`; `/pilot/` uses the accepted Kızıldere `assets/proof/geothermal-1400.webp` derivative for Open Graph instead of the unrelated Crater Lake hero; repository authority/status pointers were reconciled. Validator result remained PASS with 0 warnings and the implementation reported 185 site-wide i18n keys.

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
- The locked four-act authority in `docs/WEB_PUBLIC_VISUAL_NARRATIVE_AUTHORITY.md` supersedes earlier homepage-layout assumptions where they conflict; WEB-005 owns that integration.

## Product positioning

OrbGSS is a geospatial-intelligence platform. Geothermal Exploration is the active first application/pilot. Mineral Exploration and Environmental & Land Intelligence are expansion directions and remain labelled as such.

## Production blockers

1. `CONTACT_RELEASE_GATE` (open, MER-92) — confirm `contact@orbgss.com` ownership and deliverability before public launch. Route/mailto correctness is verified; mailbox ownership requires Workspace/account evidence. Mandatory pre-WEB-006 gate.
2. WEB-005 is terminally accepted. WEB-005A / MER-107 is `REVISION_REQUIRED` after the R3 review; its second low-cost preview gate (`tasks/WEB-005A_R3_PREVIEW_GATE_2.md`) awaits Product/CTO, and the production render, page integration and return to `REVIEW_READY` follow only after that gate is passed. It is not merged and not deployed. WEB-005B (Acts 2–4 polish) follows under the same visual-direction authority and has not begun.
3. `HOSTED_PREVIEW_NOT_RUN` was accepted under WEB-004. A hosted Vercel preview still needs to be produced under already-authorized credentials before launch; WEB-004 recorded a reproducible local preview instead.
4. WEB-006 only: connect `orbgss.com` / `www.orbgss.com` through Squarespace DNS while preserving Google Workspace MX/SPF/DKIM/DMARC and unrelated records.

## Next canonical task

GEO-WEB-002 / MER-102 is **ACCEPTED / COMPLETE** at implementation HEAD `ea693c29762279131fbed005e832c5ff2dca587b`; terminal acceptance is `docs/GEO-WEB-002_SCIENCE_ACCEPTANCE.md`. Product may bind the accepted package into WEB-005 without reopening Science so long as the package constraints are preserved.

WEB-004 is **PRODUCT_ACCEPTED / COMPLETE** under MER-92 at implementation HEAD `56cb53039b85a852110c737505bc2ae2282acb08` with acceptance publication `716104d677fea5021787b581470a436ed708f3a3`.

WEB-005 / MER-93 is **terminally accepted** (`tasks/WEB-005_TERMINAL_PRODUCT_ACCEPTANCE.md`). WEB-005A / MER-107 is **REVISION_REQUIRED** on `feat/web-005a-hero-visual-fidelity` under `tasks/WEB-005A_HERO_VISUAL_FIDELITY.md`; the reviewed R3 evidence package is `tasks/WEB-005A_HERO_FIDELITY_EVIDENCE.md`. The next canonical step is Product/CTO review of the second preview gate, `tasks/WEB-005A_R3_PREVIEW_GATE_2.md`. Only after it passes: production render, page integration, `REVIEW_READY`, then Product terminal exact-head acceptance and publication to `main`; WEB-005B follows.

WEB-006 / MER-95 production DNS cutover remains deferred behind its explicit CTO human gate and **may not begin from this publication alone**.

## History

- ORBWEB-001 (2026-09-09): production imagery from USGS Landsat Collection 2 Level-2, provenance pinned.
- ORBWEB-001.1 (2026-09-09): on-image labels, right-aligned navigation with Solutions dropdown, EN/TR.
- ORBWEB-002A (2026-09-10): GitHub publication to `baran-orbgss/website`.
- WEB-001 (2026-09-15): vNext foundation accepted at `677bfa7672ac18c2c808ddaaf235ff12863de443`.
- WEB-002 (2026-09-15): public-safe GEO-039 proof exports, Kızıldere evidence/prospectivity presentation and provenance/checksum enforcement accepted after one bounded Product review revision; implementation HEAD `a10cc141e3a7830c5e3c67a22e950ab16c0fe92b`.
- WEB-003 (2026-09-15): `/platform/`, `/solutions/`, `/pilot/`, `/company/`, `/contact/`; cross-route EN/TR, metadata, sitemap/link validation and reuse of accepted Kızıldere proof. Initial implementation `5d99eb811dfbb3396ebade17ff6ab863b5463a35`.
- WEB-003 bounded Product review revision (2026-09-15): accessibility-label localization guard, truthful Kızıldere pilot social preview and authority/status reconciliation; final implementation HEAD `3670d43bece4ffba657a3d9645cbea20c7e698bf`; Product accepted and fast-forwarded canonical main non-destructively.
- WEB-004 (2026-09-16): responsive/accessibility/performance hardening accepted under MER-92; implementation HEAD `56cb53039b85a852110c737505bc2ae2282acb08`; acceptance publication `716104d677fea5021787b581470a436ed708f3a3`. `HOSTED_PREVIEW_NOT_RUN` accepted; `CONTACT_RELEASE_GATE` remains open for launch verification.
- WEB-005 (2026-09-16): four-act homepage, production cinematic hero and truthful fallbacks; terminally accepted at `main@00af0f232a8d7d77f5ca61d758461ff7316ba151`.
- WEB-005A (2026-09-16): hero visual fidelity. Checkpoint `ffa2f2944ca5992afb9e9891b42745a9bd1105ad` (circular orbit, thinned frame, single boresight, resolved tail, bitrate investigation) was technically green but visually rejected; R2 delivered the Product visual lock — derived orbital pass, volumetric generic EO satellite, readable sensing lines, lock event, recomposed approach, NASA BMNG 500 m regional albedo, coupled page-layer analytical handoff — `REVIEW_READY`.
- GEO-WEB-002 (2026-09-16): final homepage visual master package for the locked four-act composition — Kızıldere Act-2 natural-colour Landsat context master at native 30 m (2400 × 1500 px), and renderer-native `terrain` / `thm01` / `alt01` / `alt02` / `priority` cartographic panels, card derivatives and in-frame legend crops from the accepted GEO-039 exports; per-asset provenance, checksums, rights, warnings and maximum safe rendered size published. Act-4 ≥2000 px target is not honestly achievable under accepted science and the task-authorized 1249-device-pixel contained-composition fallback is accepted. Implementation HEAD `ea693c29762279131fbed005e832c5ff2dca587b`; terminal Science acceptance `docs/GEO-WEB-002_SCIENCE_ACCEPTANCE.md`.
