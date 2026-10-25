# Violet brand adoption on the existing site: evidence

**Status:** `REVIEW_READY`, preview only. Not merged, not deployed, no DNS or domain action.
**Branch:** `claude/project-thread-osxzu4`, branched from the Heat Trace head `claude/project-thread-r4bx3f@a213731` (the light theme, the Agate adoption and the Atlas integration are below it). The pull request is against the Heat Trace branch.
**Tested commit:** `e57634f` (the commit before this file). Every automated check below ran on that commit in a detached worktree, one suite at a time; the branch HEAD is the tested commit plus records commits that touch only this file, `evidence/violet/` and the changelog and status text (none is deployed).
**Authority:** `docs/WEB_VIOLET_BRAND_AUTHORITY.md`.
**Decision:** the CTO, 2026-10-25, on the package `OrbGSS_Brand_Tasarim_Final.zip` (SHA-256 `b8869634badba9a62479bce86db7ab5ab0ad3b0648993dbc78006bca0740c675`): use the "Violet vurgu" theme; where folders conflict, `Final_v4` holds the final documents. `Final_v4/` is the one applied; `Final_v2/`, `Final_v3/` and the older folders are not used.

## 1. What changed

| Area | Change |
| --- | --- |
| Palette | In `styles.css` `:root`: `--magma` `#CD1B74` → `--violet` `#854AA6`, `--magma-light` `#F94997` → `--violet-light` `#AB7CC7`, `--amber-light` `#FFAA2E` → `#FFA323` (the package gives one Amber). The two `--wash` alphas follow the accent. Every other token (Ink, Muted, Mist, Mist soft, Night, Night lift, Pumice, white, Ink soft, Amber ink, rules) is unchanged. |
| Marks | New horizontal logo (header and footer of all 13 pages, same markup and size), favicon SVG, `favicon.ico`, touch icon and 192 / 512 icons from `Final_v4/`; hash-named under `assets/brand/`, recorded in `brand.json` (identity "Violet"); the Heat Trace files are deleted. `scripts/build_brand_assets.py --source <Final_v4/> --check` matches. |
| Locator map | `scripts/build_locator_map.py` applies the package's map rule: no brand colour on a map; the area of interest is a white dashed line over a 14 % white fill inside a Night halo at 70 %. New checksum-named SVG `kizildere-locator-19b40fa0.svg`, same Natural Earth source, byte-identical geometry; `web_m6.locator_map` in `sources.json` updated. |
| Target frame | The Act 4 target frame on the homepage priority result is white (it was Magma light). |
| Caption tone | Unchanged: Mist and Ink did not move, `CAPTION_TONE_CROSSOVER` stays 0.1967 (the validator derives it). |
| Validator | `BRAND_TOKENS`, the contrast pairs (violet replaces magma), `--magma` and `--magma-light` retired, `brand_checks` (identity "Violet", the six brand colours and the two UI forms of Violet in the record, logo paints Plum / Amber / Magma, favicon paints Night / Mist / Violet / Magma / Amber, map: white dashed callout, Night halo at 70 %, no brand colour), target frame white, skip-link ring and paper-ground link Violet. |
| Tests | `negative_tests_brand.py` has 52 cases (it had 43; new: pink returns as logo orbit, accent or token, Violet and Violet light drift, dark accent record, brand colour on the map, callout turns Violet or Magma, halo opacity); every other suite follows the new tokens, files and messages. |
| Records | `docs/WEB_VIOLET_BRAND_AUTHORITY.md` (new, with a Turkish summary); the Heat Trace, Agate, Atlas and light-theme documents marked superseded or recoloured; `CLAUDE.md`, `IMAGERY_RIGHTS.md`, `STATUS.md`, `CHANGELOG.md`; this file; `evidence/violet/` (measurement results, one new script). |
| Not changed | Page set, navigation, URLs, redirects, homepage structure and four acts, all imagery, every scientific raster, the hero video and its encodes, copy (EN and TR), fonts, type scale, dictionary keys, the page map, `vercel.json`, `sitemap.xml`, `robots.txt`, og images. |

`git diff --shortstat a213731..e57634f`: 51 files changed, 775 insertions(+), 273 deletions(-).

## 2. Automated verification (tested commit `e57634f`, container, detached worktree)

| Check | Result |
| --- | --- |
| `scripts/validate_site.py` | PASS, 0 warnings |
| `scripts/build_tr_pages.py --check` | byte-identical |
| `scripts/build_brand_assets.py --source <Final_v4/> --check` | matches a fresh build (7 files) |
| `scripts/build_fonts.py --check` | not run (fonts and `assets/fonts/` are untouched by this work) |
| `scripts/negative_tests_brand.py` | 52/52 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_atlas_foundation.py` | 46/46 caught |
| `scripts/negative_tests_atlas_geothermal.py` | 43/43 caught |
| `scripts/negative_tests_atlas_solutions_about.py` | 40/40 caught |
| `scripts/negative_tests_atlas_partner_sources.py` | 34/34 caught |
| `scripts/negative_tests_light_theme.py` | 27/27 caught |
| `scripts/negative_tests_web005.py` | 72/72 caught (restored tree: site PASS; the hero check fails exactly as on the baseline, the 13 source-texture checks) |
| `scripts/negative_tests_web005b.py` | 55/55 caught |
| `scripts/negative_tests_web005c.py` | 18/18 caught |
| `scripts/negative_tests_mer216.py` | 19/19 caught |
| `scripts/negative_tests_mer237.py` | 34/34 caught |
| `scripts/negative_tests_mer240.py` | 46/46 caught |
| `scripts/negative_tests_mer241.py` | 51/51 caught |
| `scripts/negative_tests_mer255.py` | 49/49 caught |
| `hero/scripts/validate_hero.py` | 412 checks, 13 failed: the git-ignored source-texture checks of a fresh clone, unchanged from the baseline |

Total: 586 deliberate regressions across 14 suites, all caught. A case counts only when the validator fails with the expected text on an `ERROR` line the unmutated baseline did not print.

## 3. Browser verification (headless Chromium, local static server)

| Measurement | Result |
| --- | --- |
| Text contrast, solid grounds | 1,354 text nodes on 13 routes (English and Turkish) at 1440 and 390 px; 0 below 4.5:1 (3:1 for large text). Text over photographs, the hero, figures and caption labels is judged by the caption-tone rule and is not in this audit. `evidence/heat_trace/measure_contrast.py --out evidence/violet/measurements/contrast_audit.json`. |
| Focus ring | 14 keyboard stops on the homepage, every one a visible 2 px solid ring: Violet `#854AA6` on light grounds (5.95:1 on white), Violet light `#AB7CC7` on dark grounds (5.90:1 on Night). `measurements/states.json`. The states script classified the dark ring by the old Magma value; it now keys on Violet light. |
| Hover | Navigation link Ink soft → Ink; the ghost button fills Mist with an Ink label, 14.17:1. |
| Overflow, console, network | 13 routes at 320, 360, 390, 768, 1024 and 1440 px: no horizontal overflow, no console error, no failed request; header and logo boxes unchanged (logo 120.4 × 28 px at ≤ 560 px, 137.6 × 32 px above). `measurements/overflow.json`. |
| Accent in the rendered pages | Across the 13 routes at 1440 px the computed styles carry Violet and Violet light and none of Magma `#CD1B74`, Magma light `#F94997`, the Heat Trace amber `#FFAA2E` or the logo Magma `#E43386` (0 elements). `evidence/violet/measure_accent_colours.py`, `measurements/accent_colours.json`. |
| Look | Looked at in the browser: Act 4 with the white target corners on the priority result, and the Kızıldere locator map with the white dashed 36 km area. No screenshot set was produced; the independent review does the full browser pass. |

Not re-measured here: the reduced-motion path and the mobile menu (this change touches colour and the logo files only; the logo's drawing proportions and the markup are the same as in Heat Trace).

## 4. Open points and residuals

1. Fonts: the package names Mona Sans and Martian Mono and ships their TTFs; the site keeps its self-hosted Plex subsets (decision for the CTO).
2. Hero: the video's baked navy-black space and its pale-cyan reticle and orbit trail stay (a re-render is a separate task); the reticle does not match the brand's white AOI line.
3. `og:image` is still the hero poster, which has no logo.
4. The supplied SVGs carried a C2PA "provided by Claude" credential, stripped as before; any trademark question is the CEO/COO's.
5. `build_fonts.py --check` was not run (§2).
6. The package's Review pages (`*.dc.html`) need a network to render and were not used; the README, the token files and the PNG and SVG assets were.
7. Nothing is merged, deployed or published.
