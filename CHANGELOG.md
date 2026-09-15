# Changelog

## v0.8.1-web-003-review-revision — 2026-09-15 (WEB-003 Product review revision, MER-91, branch `feat/web-003-public-site-depth`)

Bounded conformant fixes from Product review. No redesign, no scope or semantics change.

- **EN/TR accessibility-text parity closed.** `/contact/`'s `aria-label="Contact options"` and `/pilot/`'s `aria-label="Next steps"` were the only two `aria-label` values on any canonical public route not bound to `data-i18n-aria-label` — both now carry it (`contactPage.optionsLabel`, `pilotPage.nextStepsLabel`), so they switch with the page like every other accessible name. `scripts/validate_site.py` now fails the build if any canonical route ever reintroduces an aria-label with no `data-i18n-aria-label` on the same element; verified the check has teeth by reverting each fix locally, confirming the new error, then restoring it.
- **`/pilot/` social preview is now truthful.** Its Open Graph image no longer borrows the homepage's Crater Lake hero photo; it now points at the already-approved, already-checksummed Kızıldere `assets/proof/geothermal-1400.webp` derivative (unmodified — no re-colour, re-crop or re-encode), with `og:image:type` / `:width` / `:height` added for correctness. The validator now rejects the Crater Lake image specifically on `/pilot/` and requires its `og:image` to be a self-hosted `assets/proof/` or `assets/imagery/` asset.
- **Authority/status pointers reconciled.** `docs/WEB_VNEXT_AUTHORITY.md` and `STATUS.md` now read Product & Execution Authority v1.7 and record WEB-003's actual state (implemented, `REVIEW_READY`, MER-91 bounded review revision) instead of the stale "not started" language left over from before CTO approval. No Product/Science semantics changed anywhere in this revision.

## v0.8.0-web-003-public-site-depth — 2026-09-15 (WEB-003, branch `feat/web-003-public-site-depth`)

- published five new public routes as real static directories — `/platform/`, `/solutions/`, `/pilot/`, `/company/`, `/contact/` (each `<route>/index.html`, root-relative assets) — completing the public information architecture beyond the homepage;
- `vercel.json` now serves trailing-slash canonical URLs (`trailingSlash: true`) to match the published route model; `sitemap.xml` lists all six canonical routes;
- the homepage and every new route share one persistent header/footer navigation that now routes to these five destinations instead of same-page anchors; the homepage's own WEB-002 section ids, content and hero CTA are untouched, so the accepted evidence-to-intelligence narrative and its provenance/checksums are unchanged;
- `/platform/` explains the accepted workflow (AOI → source/context → evidence → explicit data gaps → integrated priority → investigation decision support) as an editorial numbered list, not a feature grid;
- `/solutions/` presents the three-application portfolio (Geothermal active first application; Mineral and Environmental & Land Intelligence as expansion directions) as an extended ledger, reusing the homepage's own application copy and status labels;
- `/pilot/` reuses the accepted WEB-002 proof imagery and the structure/geology data-gap panel verbatim for Kızıldere — same assets, same checksums, same "no CSS transform on scientific rasters" guard, same mandatory EN/TR warnings — around new explanatory prose, so the first-application story can be read in depth without restating or drifting from the accepted semantics;
- `/company/` and `/contact/` give OrbGSS an actual about/contact destination (operating principles, restrained expansion framing, three mailto conversation starters); no form, backend, analytics or PII capture;
- every route carries truthful route-specific `<title>`, meta description, canonical URL and Open Graph metadata; `aria-current="page"` marks the active nav item; language selection persists coherently across routes via the existing shared `localStorage` key;
- `script.js` gained new EN/TR key pairs for the five routes (plus `mail.pilot` / `mail.technical`), reusing existing homepage keys everywhere the meaning is identical (nav labels, trust list, company copy, mandatory warnings, image captions, coordinates) rather than forking duplicate strings;
- `styles.css` gained a small set of new page-level components (`.page-hero`, `.workflow-list`, `.contact-options`, `.editorial-note`, `.ledger-copy-group`) built from the existing palette and type scale; no new visual system, no card grid;
- validator extended site-wide: every route now gets metadata checks, internal-link and cross-page fragment resolution, sitemap coverage, and an EN/TR parity check across every `data-i18n*` key referenced anywhere on the site; the WEB-002 provenance/checksum/warning checks above it are untouched and stay scoped to `index.html`; PASS with 0 warnings;
- no deploy, DNS, analytics, form backend, or WEB-004/WEB-005/WEB-006 work introduced.

## v0.7.1-web-002-review-revision — 2026-09-15 (WEB-002 Product review revision, branch `feat/web-002-product-proof`)

Bounded conformant fixes from Product review at `854c37f`. No redesign, no scope or semantics change.

- **Scientific rasters are no longer visually transformed.** Removed `saturate(.9) contrast(1.03)` from the story panels and evidence panes and the `opacity:.92` from the score colour ramp, and added an explicit `[data-visual-status="product-proof"] img, .scale-strip>img{filter:none;opacity:1}` guard so a future gallery-grade edit cannot reach proof imagery. The hero keeps its gallery grade.
- **One frame for one ground.** Deleted the six per-slot `object-position` crops left over from WEB-001, when each slot held a different Landsat scene. Every story panel renders the same Kızıldere AOI, so all now use the default centred framing.
- **THM-01 warning semantics restored** in EN, TR and the static HTML: THM-01 is thermal evidence, not geothermal probability, reserve or resource, discovery or drilling-success evidence.
- **Warning coverage is now enforced.** Each proof asset carries a `visible_warning` record naming the i18n key and the exact wording required in each language; the validator checks the term appears in the EN dictionary, the TR dictionary and the static HTML, so a warning cannot silently disappear — including for readers with JavaScript disabled.
- **Caption contrast re-checked** against the new framing; `priority` moved to the dark tone (5.1:1 desktop / 6.4:1 mobile, against 3.7 / 2.9 for white) and the dark halo was tightened so it no longer blooms over mid-tone ground.
- **Stale copy reconciled:** the no-JS footer attribution in `index.html` now matches the dictionary (Landsat hero + WEB-002 cartographic exports); `STATUS.md` moves to Product authority v1.5 and drops the obsolete temporary-gallery / `Natural-color composite` story-panel rules; `IMAGERY_RIGHTS.md` and the `sources.json` policy now state the two asset classes and their different handling rules explicitly.

## v0.7.0-web-002-product-proof — 2026-09-15 (WEB-002, branch `feat/web-002-product-proof`)

- replaced the temporary gallery story panels with real OrbGSS product proof: every panel 01–06 now shows the same Kızıldere pilot AOI (36 × 36 km, EPSG:32635, 30 m) so the reader watches one place gain evidence rather than six unrelated places;
- materialized seven website masters through the accepted GEO-039 Workbench cartographic export path from the persisted `kizildere_mvp_v2` project — `observe`, `terrain`, THM-01, ALT-01, ALT-02, `priority` and the Kızıldere first-application composite — using only the layer selections authorized by `docs/WEB-002_SCIENCE_ASSET_PACKAGE.md`;
- `05 Priority` and `06 Geothermal` carry the accepted `mvp_remote_sensing_priority_v1` output from run `8716e893…`, published as **Remote-Sensing Relative Priority — Experimental Baseline** with its 0–100 legend cropped from the same export;
- `03 Evidence` gained a restrained, keyboard-accessible layer switch (THM-01 / ALT-01 / ALT-02) — the page's single interactive moment; each layer's caption travels with its pane so the label can never drift from the raster;
- `04 Structure` is a deliberate data-gap state with no image: no public-safe fault or lithology master is authorized, and the copy says so and records that the gap is score-invariant;
- every proof panel carries its mandatory scientific warning as visible copy in EN and TR;
- `assets/imagery/sources.json` gained `web_002` with, per asset, the export id, `export_manifest.json` pointer, master SHA-256 from that manifest, crop box and a SHA-256 for each shipped derivative; the three Landsat scenes no longer placed on the homepage are marked `retired-from-homepage` with rights intact;
- validator now verifies proof-asset provenance by recomputing every derivative checksum, requires a `data_gaps` record behind any data-gap slot, and rejects overstated score wording outside a mandatory warning; PASS with 0 warnings;
- no raw provider raster, no MTA data, no change to CRS/grid/units/NoData/scoring semantics; WEB-005 hero, WEB-003, deployment and DNS untouched.

## v0.6.0-web-001-vnext-foundation — 2026-09-15 (WEB-001, branch `feat/web-001-vnext-foundation`)

- published the repository-local vNext authority (`docs/WEB_VNEXT_AUTHORITY.md`) and the WEB-001 contract (`tasks/WEB-001_VNEXT_FOUNDATION.md`) before feature code;
- rebuilt the homepage as an evidence-to-intelligence story while keeping the beam → full-width panel gallery rhythm: Hero → 01 Observe → 02 Terrain → 03 Evidence → 04 Structure → 05 Priority → 06 Geothermal → Pilot ledger → Company/Trust → Contact → Footer;
- static poster hero (`Earth data. Evidence. Priority.` / `Know where to look next.` / `Explore the Platform`), built so WEB-005 replaces only the visual layer;
- navigation: Platform / Solutions (Geothermal Exploration, Mineral Exploration, Environmental & Land Intelligence) / Pilot / Company / Contact / EN | TR; all anchors real; disclosure and mobile behaviour unchanged;
- technical beams now carry index, title, statement and a monospace descriptor; scene labels moved to the monospace treatment; story panels add a `Natural-color composite` line;
- pilot ledger marks Geothermal `Active · First application`, Mineral and Environmental & Land `Expansion direction`; company block with restrained trust list; contact beam;
- temporary story visuals reuse the four provenance-safe Landsat composites (marked `data-visual-slot` / `temporary-gallery`; placement recorded in `sources.json`); no scientific outputs fabricated; WEB-002 owns replacements;
- full EN/TR parity for every new string;
- validator extended to the vNext anchors and visual-slot discipline; PASS with 0 warnings.

## v0.5.1-nav-labels-bilingual — 2026-09-09 (ORBWEB-001.1)

- replaced the metadata strips under every satellite image with a bottom-right on-image location + coordinates label (no background container, subtle text-shadow only); sensor/date remain in the manifest and rights documentation;
- rebuilt desktop navigation: right-aligned Home → Solutions (dropdown: Geothermal, Mining, Marine) → About → Partner With Us → EN | TR; Home cyan underline; Partner With Us as a plain item;
- Solutions dropdown as an accessible disclosure: hover, focus and click open; Escape, click-outside and focus-out close; ArrowUp/Down/Home/End move through items; tap-to-expand on mobile;
- added client-side EN/TR bilingual support (`I18N` dictionary in `script.js`): instant switch, scroll preserved, `<html lang>`, title, meta/og descriptions, alt texts and mail subjects update, choice persisted in `localStorage`, English default;
- footer navigation now Home / Solutions / About / Contact; footer is the `#about` anchor;
- design and product authority docs updated so the new decisions are canonical;
- imagery, provenance, pipeline and product claims unchanged; validator PASS with 0 warnings.

## v0.5-production-imagery — 2026-09-09

- populated all four production scenes as self-hosted OrbGSS natural-color composites built from USGS Landsat Collection 2 Level-2 surface reflectance (public domain);
- added `scripts/build_imagery.py` (reproducible crop/stretch/encode pipeline; `--record` writes render provenance into the manifest);
- pinned Landsat product identifiers, crop geometry, stretch parameters and rendered bounds per scene in `assets/imagery/sources.json`;
- removed the remote NASA Earth Observatory fallback dependency (`data-fallback`, preconnect) while keeping graceful image-failure behavior;
- updated footer attribution and `IMAGERY_RIGHTS.md` for the live asset provenance;
- removed `scripts/fetch-imagery.py` (superseded by the build pipeline);
- validator passes with zero warnings.

## v0.4-claude-handoff — 2026-09-09

- added canonical Claude Code bootstrap authority (`CLAUDE.md`);
- added current state pointer (`STATUS.md`);
- documented locked visual direction and product/content boundaries;
- documented Squarespace → Vercel deployment guardrails;
- added bounded continuation tasks;
- added site validator and handoff prompt;
- included visual-direction reference image;
- retained v0.3 page implementation and imagery provenance files.

## v0.3

- locked four visual scene roles and provenance manifest;
- local-first imagery paths with verified prototype fallback URLs;
- imagery rights/provenance documentation.
