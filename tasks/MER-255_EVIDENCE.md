# MER-255 — premium multi-page visual redesign of the interior routes (evidence)

**Issue:** MER-255.
**Authority:** `docs/WEB_INTERIOR_REDESIGN_AUTHORITY.md` (written by this task under the design authority the CTO delegated in the task brief, 2026-10-19). It wins over `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md` only where the two disagree about how the five interior routes are presented (§2 of the authority). Scientific, legal and claim rules are unchanged.
**Branch:** `claude/premium-interior-redesign-65zdlt`, from the MER-241 head `f071751b` (`claude/mer-241-turkish-static-pages-sihwiy`), because the Turkish generator and the VirgaSoft removal are part of what the redesign builds on. `main` (production) is `81d1f911` and was not touched.
**State:** `REVIEW_READY`. The independent review has not run yet (the coordinator starts it). Nothing was merged, deployed or published, and no DNS, credential or Vercel setting was changed. The branch HEAD is the one named in the Linear report.

## 1. What was run, and what it returned

Everything below was run on the final tree of this branch. A check that was not run is listed in §6, never counted as passed.

| Check | Result |
| --- | --- |
| `python3 scripts/validate_site.py` | `RESULT: PASS`, 0 warnings, 14 deployed root entries, 130 deployed files, 6 of 6 Turkish routes byte-identical to the generator |
| `python3 scripts/build_tr_pages.py --check` | OK, byte-identical |
| `python3 scripts/build_interior_crops.py --check` | OK (the crop files and their record in `sources.json` match a fresh build from the Kızıldere master) |
| `node --check script.js` | OK |
| `scripts/negative_tests_mer255.py` | 46 / 46 caught; restored tree validates identically |
| `scripts/negative_tests_mer240.py` | 46 / 46 caught; restored tree validates identically (its table cases were rewritten for the ruled lists, see the authority §2) |
| `scripts/negative_tests_mer241.py` | 51 / 51 caught; restored tree validates identically |
| `scripts/negative_tests_web005.py` | 72 / 72 caught |
| `scripts/negative_tests_web005b.py` | 55 / 55 caught; restored tree validates identically |
| `scripts/negative_tests_web005c.py` | 18 / 18 caught; restored tree validates identically |
| `scripts/negative_tests_mer216.py` | 19 / 19 caught; restored tree validates identically |
| `scripts/negative_tests_mer237.py` | 29 / 29 caught; restored tree validates identically |
| `python3 hero/scripts/validate_hero.py` | 412 checks, 13 failed: exactly the 13 known failures of a fresh clone (5 recorded source-texture hashes and 8 missing git-ignored files under `hero/assets/source/`). No other failure. |
| `evidence/mer255/qa_browser.py` (Playwright + Chromium) | 110 of 110 combinations pass (5 routes × EN and TR × 11 viewports), see §2. Result file `evidence/mer255/qa_browser_result.json` is the output of the last run; a re-run on the final tree returned the identical file. |
| `scripts/measure_interior_renders.py` | Browser-measured drawn size of every interior crop and scene at 19 viewports × DPR 1 and 2, recorded in `assets/imagery/sources.json`; see §3. |

No validator rule was loosened to pass. The validator gained the MER-255 contract (grammar kept off the homepage, every crop recorded and never drawn above its own pixels, thumbnails, no governed raster on the Geothermal page, no data collection, the sources page and the unchanged MIT text, a 12-word list-line budget replacing the retired table cell budget). The old table rules were replaced only where `docs/WEB_INTERIOR_REDESIGN_AUTHORITY.md` §2 revises the decision, and the replacements are exercised by the cases in `negative_tests_mer255.py` and the rewritten table cases of `negative_tests_mer240.py`.

## 2. Real-browser QA

`evidence/mer255/qa_browser.py` loads every interior route in English and Turkish at 360×740, 390×844 and 414×896 (DPR 2), 600, 768, 834, 1024, 1280, 1440, 1920 and 2560 CSS px wide, scrolls the whole page and reports:

* horizontal overflow: 0 px in all 110 combinations;
* console and page errors, and failed or 4xx requests: none;
* broken images after the scroll-through: none;
* cumulative layout shift: 0 in all 110 combinations;
* heading structure, missing `alt` attributes, in-page and internal links, and text contrast on opaque backgrounds: no failure. Text drawn over a photograph cannot be computed this way and was judged on the screenshots.

## 3. Image density

The brief's honest-render rule is enforced by the validator and recorded per crop (`assets/imagery/sources.json` → `web_m6.interior_crops`, with the analysis-grid overlap of each crop). Browser measurement across 19 viewports and DPR 1 and 2 gives a worst upscale of 1.00× for all four Kızıldere crops (none is drawn above its own pixels), 1.00× for the Yellowstone scene and 0.88× for the two small scenes. All four crops are Class A (natural-colour Landsat); no governed scientific raster (Class B) was added to any interior page.

## 4. Visual inspection

The screenshots were looked at, not only measured. Full-page and per-section captures were taken of all five routes in English and Turkish at 1440 and 390 px (and the Geothermal and About pages at 1920 and 834 px), at every iteration of the design. After the final tree was restored (§7), all 20 full-page captures (English and Turkish, 1440 and 390) were re-taken and compared pixel by pixel with the captures that had been inspected: 18 are identical. The two that differ are the English Sources page at 1440 (47 px shorter than the earlier capture) and the Turkish Geothermal page at 390 (only the letter-spacing of the mono scene-ID lines differs). Both differences match edits made after the earlier captures were taken (two shortened licence-term lines, and `letter-spacing:0` on those lines at phone width); the two pages were looked at again in their final state and read correctly.

Defects found by measurement and inspection and fixed along the way: scene IDs wrapping awkwardly on phones; the stage hero and one Yellowstone band drawing their crop above its own pixels between 600 and 1000 px; a crop that overlapped the analysis grid, which made its alt text and role wrong.

Delivered for review in the project files: `interior-redesign/before-after-<page>-<d1440|m390>.png` (the four redesigned pages, before and after) and `interior-redesign/after/` (montages of every page, EN and TR, 1440 and 390, plus the 1920 and 834 views of Geothermal).

## 5. Research

Direct access to the reference sites (Seequent, Planet, Mapbox, Esri, Carto and similar) was blocked from the build container (`getaddrinfo ENOTFOUND`), and web search returned link lists only, so no page of any of them was read or looked at. The design principles in the authority (§1) were derived from what is generally known of how such sites present Earth-observation work (one large real image leading each page, little text, a clear status vocabulary, sources kept separate from the story). They are not a measured comparison, and nothing was copied.

## 6. Not run, or not verifiable from here

* **The independent review.** Pending; the coordinator starts it.
* **The Vercel Preview of this HEAD** is listed in the Linear report once it is built. The checks above ran locally against a static server that mimics `cleanUrls` and `trailingSlash`; they were not re-run against the deployed Preview.
* **Link liveness.** The external links on `/sources/` (USGS, NASA, ESA, Zenodo, DOI resolvers, Natural Earth) were not fetched: the container has no route to them. They are the links the previous About table already carried, plus the DOIs the brief names. The validator checks their shape, not that they resolve.
* **The Scientific colour maps copyright line.** `/sources/` reproduces the unchanged MIT licence text and the line "Copyright (c) 2023, Fabio Crameri". The Zenodo release (https://doi.org/10.5281/zenodo.1243862) could not be opened, so that line is carried from the repository's earlier text and flagged in an HTML comment on the page. It needs a check against the licence file of the v8.0 release before publication (authority §8, item 4).
* **Safari and Firefox.** Only Chromium was run.
* **Screen readers.** Heading and landmark structure were checked by script, not with assistive technology.

## 7. Integrity note on the negative-test suites

The negative-test suites mutate real files in the working tree and restore them in a `finally` block. They must be run one after another. During the final verification the eight suites were started at the same time to save time, so they mutated and "restored" the same files concurrently, and several files were left holding another suite's mutation (a swapped navigation item, a removed `data-hero-tiers` attribute, an `og:image` pointing at a missing file, a renamed `playRise`, and similar). None of this was committed or pushed.

The tree was repaired before anything else was done: each swap was reversed by its own test definition with a check that the forward mutation reproduces the damaged text; the destructive ones (the hero markup in `index.html`, and `hero_relief_rise` in `sources.json`) were restored from `HEAD` plus this task's own change, and the few mutations written as lambdas or regular expressions were undone by hand from the validator's errors; and the validator, the Turkish generator check, all eight suites (run sequentially this time, so the figures in §1 are from the sequential run), the hero validator, the browser QA and the pixel comparison of §4 were then re-run on the repaired tree. The QA result file came back identical to the one recorded before the incident.

## 8. Open decisions for the CTO

Listed with their consequences in `docs/WEB_INTERIOR_REDESIGN_AUTHORITY.md` §8: the Geothermal layer imagery (MER-242), Mining and Marine as panels rather than bands, the shortened footer attribution on every page including the homepage, the Scientific colour maps copyright line, D3 (privacy / KVKK) and D5 (coastal Marine scene), and that MER-241 is contained in this branch and still unpublished. Any publication needs the CTO's explicit "main'e push et".
