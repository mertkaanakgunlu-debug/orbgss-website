# MER-255 — premium multi-page visual redesign of the interior routes (evidence)

**Issue:** MER-255.
**Authority:** `docs/WEB_INTERIOR_REDESIGN_AUTHORITY.md` (written by this task under the design authority the CTO delegated in the task brief, 2026-10-19). It wins over `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md` only where the two disagree about how the five interior routes are presented (§2 of the authority). Scientific, legal and claim rules are unchanged.
**Branch:** `claude/premium-interior-redesign-65zdlt`, from the MER-241 head `f071751b` (`claude/mer-241-turkish-static-pages-sihwiy`), because the Turkish generator and the VirgaSoft removal are part of what the redesign builds on. `main` (production) is `81d1f911` and was not touched.
**State:** `REVIEW_READY` again after a review revision (§0). Nothing was merged, deployed or published, and no DNS, credential or Vercel setting was changed. The branch HEAD is the one named in the Linear report.

## 0. Review history

* **First independent review, at `cffadf8a` (2026-10-19): FAIL**, three blocking defects. Everything else in that review passed (validator, all negative suites, byte-identity of the Preview, browser checks on EN and TR at four widths).
  * **B1.** The hero validator reported 14 failures, not the 13 this file claimed. `hero/config/lane.json` did not list the nine new crop files in `integration_write_surface`, and its `phase`, `lane` and `integration_task` fields still named MER-241. The "13 failed" figure had been taken from an earlier tree.
  * **B2.** The licence record on `/sources/` printed "Copyright (c) 2023, Fabio Crameri". This file said the line was "carried from the repository's earlier text". That was false: the repository held only "Fabio Crameri; MIT licence" and the DOI, and the line had no source. The PyPI `cmcrameri` 1.10 package (which bundles SCM v8.0) says "Copyright (c) 2020 Fabio Crameri" in its own licence file.
  * **B3.** The About terrain crop and the Partner valley crop were captioned with the pilot's declared coordinates (37.9794° N, 28.7907° E), which lie about 18 km and 4 km outside the ground those two crops show. The earlier IMAGERY_RIGHTS text ("a crop does not claim to be centred on them") did not make that acceptable on an image whose caption reads as a location.
  * Remark: Mining and Marine on `/solutions/` are structurally card-like, and the `CLAUDE.md` rule that Act 3 is the single permitted card-like composition had not been revised.
* **Second independent review, at `da2c0d7f`: FAIL on one text defect** (B1–B3 verified closed, no site regression). The sentence this revision had added to `CLAUDE.md` defined an "equal-weight grid cell" as a card and said the validator enforces "no grid", but Mining and Marine sit in a two-column grid and no such check exists. Corrected in a third commit (text only, layout unchanged): `CLAUDE.md`, `CHANGELOG.md`, authority §2 and §1 below now say exactly what the validator checks, and one comment in `scripts/validate_site.py` was reworded to match.
* **This revision (commit after `cffadf8a` on the same branch)** fixes all of them; what changed is in §1 and what was run in §2. A push invalidates the earlier review, so the independent re-review has to run again at the new HEAD (§7).

## 1. What changed in the revision

* **B1.** `hero/config/lane.json`: the nine crop files (`kizildere-stage-161b5b57-{1600,2400,3200}`, `kizildere-aoi-1a7d0c36-{800,1200}`, `kizildere-terrain-984f936e-{1000,1459}`, `kizildere-valley-28b19cfd-{700,1000}`) are in the write surface, and `phase`, `lane` and `integration_task` name MER-255 (the pre-MER-255 text stays in each field, marked as such). The hero validator was run after the commit, because it diffs baseline to HEAD.
* **B2.** The "2023" line is **withdrawn**. `/sources/` now carries the standard MIT permission and warranty text, in the standard ASCII wording, under "Copyright (c) Fabio Crameri", with no year. `assets/imagery/sources.json` → `web_m6.licence_notices["scientific-colour-maps-v8.0"]` records the published line, the null year, what the repository and the PyPI package say (with the sdist SHA-256), and the open item. The validator fails if a year appears on the page without a recorded `year_verified_from`, and if the page line differs from the record. **No year is asserted anywhere.** Taking the exact notice from the Zenodo v8.0 release file (version DOI 10.5281/zenodo.8035877) is a source-usage-rights decision and stays with the CTO (authority §8, decision 4). The release file itself could not be opened from the build environment (zenodo.org, doi.org and github.com refuse the connection).
* **B3.** Each interior crop now has a recorded `label_point` (master pixel, latitude, longitude, basis). Stage and aoi contain the pilot centre and keep its coordinates. About's terrain crop is captioned "East of the Kızıldere pilot area, Türkiye — 38.0936° N, 29.2483° E" and Partner's valley crop "South-west of the Kızıldere pilot area, Türkiye — 37.8744° N, 28.5695° E", the centres of the two crops. `scripts/geo_frame.py` (UTM 35N, the master's 30 m grid; self-check against the recorded frame corners and the AOI centre) projects each printed pair back onto the master, and `scripts/validate_site.py` fails when it is outside the crop box, when it differs from the record, or when the figure's caption keys differ from the record's. Turkish uses K/D for N/E and is held to the same numbers.
* **Cards.** The hairline frame around the Mining and Marine panels is gone, and the validator rejects a border, radius, shadow, outline or backdrop declared on `.domain-panel`, `.panel-figure` or `.pair-grid`, and a link inside the pair. It does **not** check the two-column grid, the item count, the placeholder colour behind the photograph or the copy; an earlier version of this paragraph, of `CLAUDE.md` and of `CHANGELOG.md` said "no grid" and "grid-cell treatment", which overstated the check and was corrected after the re-review. `docs/WEB_INTERIOR_REDESIGN_AUTHORITY.md` §2 ("CLAUDE.md card rule — Clarified, not loosened") defines a card and says why captioned photographs are not one; `CLAUDE.md` carries the same sentence. Whether the CTO prefers full-width bands instead of two panels remains open (decision 2).
* **Small.** The Turkish credit lines on `/tr/kaynaklar/` are the providers' original English wording and say so ("Atıf cümlesi (özgün)"); straight quotes in the licence paragraphs; the About trust note no longer claims credits "where it appears"; `aboutPage.see.glance` and the TR Chuquicamata place line corrected.

## 2. What was run, and what it returned

Everything below was run on the committed HEAD of this revision or on a working tree identical to it; a check that was not run is listed in §6, never counted as passed. The eight negative-test suites (348 cases in all) were run **one after another** in a detached worktree of the committed HEAD `8ecd64f4` (§8); the figures are theirs, nothing was reported that was not run. Two commits follow it: the evidence file, and the text-only card-wording correction described in §0 (`CLAUDE.md`, `CHANGELOG.md`, authority §2, this file, and one comment line in `scripts/validate_site.py`; no behaviour, markup, CSS or asset changed). After the last commit the validator, the Turkish generator check, `negative_tests_mer255.py` (58 cases, in a detached worktree) and the hero validator were re-run at the final HEAD; the other seven suites were not re-run, because nothing they exercise changed.

| Check | Result |
| --- | --- |
| `python3 scripts/validate_site.py` | `RESULT: PASS`, 0 warnings, 14 deployed root entries, 130 deployed files, 6 of 6 Turkish routes byte-identical to the generator |
| `python3 scripts/build_tr_pages.py --check` | OK, byte-identical |
| `python3 scripts/build_interior_crops.py --check` | OK (crop files and their `sources.json` record match a fresh build from the Kızıldere master) |
| `python3 scripts/geo_frame.py` | self-check OK (AOI centre at master pixel 1140.96, 899.93) |
| `node --check script.js` | OK |
| `scripts/negative_tests_mer255.py` | 58 / 58 caught (46 before; 12 new); restored tree validates identically |
| `scripts/negative_tests_mer240.py` | 46 / 46 caught; restored tree validates identically |
| `scripts/negative_tests_mer241.py` | 51 / 51 caught; restored tree validates identically |
| `scripts/negative_tests_web005.py` | 72 / 72 caught; restored tree identical to baseline for the site validator and for the hero validator (the hero validator's 13 fresh-clone failures are the baseline) |
| `scripts/negative_tests_web005b.py` | 55 / 55 caught; restored tree validates identically |
| `scripts/negative_tests_web005c.py` | 18 / 18 caught; restored tree validates identically |
| `scripts/negative_tests_mer216.py` | 19 / 19 caught; restored tree validates identically |
| `scripts/negative_tests_mer237.py` | 29 / 29 caught; restored tree validates identically |
| `python3 hero/scripts/validate_hero.py` (after the commit) | 412 checks, **13 failed**: the 8 `materialized local path exists` checks and the 5 `…on disk matches its recorded SHA-256` checks for the git-ignored textures under `hero/assets/source/`, i.e. exactly the known fresh-clone failures. All six `lane boundary` checks pass, including "public-site changes since the baseline stay inside the integration write surface". |
| `evidence/mer255/qa_browser.py` (Playwright + Chromium) | 110 of 110 combinations pass (5 routes × EN and TR × 11 viewports from 360 to 2560 CSS px): horizontal overflow 0, CLS 0, no console or page error, no failed or 4xx request, no broken image, no missing `alt`, heading structure and in-page links fine. The result file is byte-identical to the one recorded before this revision. |
| `scripts/measure_interior_renders.py` | Not re-run: this revision changed no image, no crop box, no `srcset` and no CSS width cap (the only CSS change removed a 1 px border). The recorded measurement (19 viewports × DPR 1 and 2, worst 1.00×) stands; the validator's CSS-cap bound still passes. |

No validator rule was loosened to pass. The revision only added checks (caption coordinates, the licence line and its year guard, the not-a-card guard). Each new check is exercised by a case in `negative_tests_mer255.py`, which now has 58 cases (46 before).

## 3. Real-browser QA and visual inspection

`evidence/mer255/qa_browser.py` loads every interior route in English and Turkish at 360×740, 390×844 and 414×896 (DPR 2), 600, 768, 834, 1024, 1280, 1440, 1920 and 2560 CSS px wide, scrolls the whole page and reports the figures in §2. Text drawn over a photograph cannot be computed that way and was judged on screenshots.

For this revision the changed pages (Solutions, About, Partner, Sources; English, 1440 and 390 px) were re-captured and looked at: the Mining and Marine panels read as two captioned photographs without a frame; the About terrain and Partner valley captions show the new place line and coordinates and stay legible on the captures at 1440 and 390 px (the mono text carries its own shadow; contrast under a photograph was judged by eye, not computed); the Sources page shows the year-less licence line. No horizontal overflow at 390 px.

Image density is unchanged from the first submission: all four crops are Class A natural-colour Landsat, none is drawn above its own pixels (worst 1.00×), and no governed scientific raster (Class B) was added to any interior page.

## 4. Research

Direct access to the reference sites (Seequent, Planet, Mapbox, Esri, Carto and similar) was blocked from the build container (`getaddrinfo ENOTFOUND`), and web search returned link lists only, so no page of any of them was read or looked at. The design principles in the authority (§1) were derived from what is generally known of how such sites present Earth-observation work. They are not a measured comparison, and nothing was copied.

## 5. Known, not blocking

Noted by the review or by inspection and left as they are, because none changes a claim, a licence or a layout contract:

* extra empty space under the About "Too much ground, too little time" section and the Geothermal "gap" section at some desktop widths;
* the layer-diagram labels are small (about 8 px) on phones;
* the Sources thumbnails ship without `srcset` (they are at most 160 CSS px and each is a recorded image);
* caption legibility over pale terrain depends on the mono text's shadow, no measurement of contrast under a photograph was possible;
* a missing page under `/tr/` is answered by the single bilingual `404.html` (an English page with one Turkish line), not by a separate Turkish 404.

## 6. Not run, or not verifiable from here

* **The independent re-review of this revision.** A push invalidates the earlier review; the coordinator starts the new one.
* **The Scientific colour maps copyright notice.** Not verified against the release file; the page therefore states no year (§1, B2). Open for the CTO.
* **The Vercel Preview of this HEAD** is named in the Linear report; the checks above ran locally against a static server that mimics `cleanUrls` and `trailingSlash`. Whether the Preview serves the same bytes as the local tree is reported in the thread, not here.
* **Link liveness.** The external links on `/sources/` (USGS, NASA, ESA, Zenodo, DOI resolvers, Natural Earth) were not fetched: the container has no route to them. The validator checks their shape, not that they resolve.
* **Safari and Firefox.** Only Chromium was run.
* **Screen readers.** Heading and landmark structure were checked by script, not with assistive technology.
* **Reference sites** (§4).

## 7. Open decisions for the CTO

Listed with their consequences in `docs/WEB_INTERIOR_REDESIGN_AUTHORITY.md` §8: the Geothermal layer imagery (MER-242), Mining and Marine as panels rather than bands, the shortened footer attribution on every page including the homepage, the Scientific colour maps copyright notice (now year-less pending the release file), D3 (privacy / KVKK) and D5 (coastal Marine scene), and that MER-241 is contained in this branch and still unpublished. Any publication needs the CTO's explicit "main'e push et".

## 8. Integrity note on the negative-test suites

The suites mutate real files in the working tree and restore them in a `finally` block, so they must run one after another. During the first submission the eight suites were started at the same time, mutated and "restored" the same files concurrently, and left several files holding another suite's mutation (a swapped navigation item, a removed `data-hero-tiers` attribute, an `og:image` pointing at a missing file, a renamed `playRise`, and similar). Nothing was committed or pushed in that state; the tree was repaired and re-verified, and the incident is recorded here so the same shortcut is not taken again.

For this revision the suites were run **sequentially, one at a time**, in a detached `git worktree` of the committed HEAD, so a failing or interrupted case could not touch the working tree under review. The validator was run once after each suite as a restore check.
