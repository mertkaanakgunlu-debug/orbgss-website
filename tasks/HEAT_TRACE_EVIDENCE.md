# Heat Trace brand adoption on the existing site: evidence

**Status:** `REVIEW_READY`, preview only. Not merged, not deployed, no DNS or domain action.
**Branch:** `claude/project-thread-r4bx3f`, branched from the light-theme head `claude/project-thread-75kouq@7be2907` (the Agate adoption and the Atlas integration are below it). The pull request is against the light-theme branch.
**Tested commit:** `f33164a` (the commit before this file). Every check below ran on that commit in a detached worktree, one suite at a time; the branch HEAD is the tested commit plus records commits that touch only `CHANGELOG.md`, `STATUS.md`, this file and `evidence/heat_trace/` (none is deployed); `git diff --stat f33164a..HEAD` shows nothing else.
**Authority:** `docs/WEB_HEAT_TRACE_BRAND_AUTHORITY.md`. **Screenshots:** the project Library, folder `heat-trace/screenshots/` (indexed in §5).
**Decision:** the CTO, 2026-10-25, on the package `OrbGSS Logo Tasarım4.zip` (SHA-256 `cc5f769be1007a4929618237203218b94319454325188b8ea409fd53ee625635`): "bu son tasarım kararı uygula". The package holds `Final_v2/` and `Final_v3/`; `Final_v3/` is the revision of `Final_v2/` ("the 5c symbol and wordmark in the 6a Heat Trace palette, with the Magma and Amber orbits swapped, a single orb at the focal point and the app icon on Night") and is the one applied. This reading is the thread's assumption and was reported to the CTO.

## 1. What changed

| Area | Change |
| --- | --- |
| Palette | The Agate tokens in `styles.css` `:root` are replaced by the Heat Trace set: Ink `#2D1B30`, Muted `#756D76`, Magma `#CD1B74`, Amber `#FFA323`, Mist `#F5EFF7`, Mist soft `#C3BAC5`, Magma light `#F94997`, Amber light `#FFAA2E`, Night `#160A19`, Night lift `#241E25`, Pumice `#F7F5F8`, white, Ink soft `#5D525F`, Amber ink `#A15C13`, and four rule alphas. Every `var(--old)` and every hand-written `rgba(…)` triple (about 70 hero, band and caption shades) moved with them. Role variables (`--fg`, `--link`, `--limit`, `--hair`, `--surface`, `--matte`, `--wash`) are unchanged in name and meaning. |
| Marks | New horizontal logo in the header and footer of all 13 pages (138 × 32 px header, 120 × 28 px at ≤ 560 px; the markup is `width="619" height="144"`); favicon SVG and `favicon.ico`; 180 px touch icon; 192 / 512 px manifest icons. Hash-named files under `assets/brand/`, recorded in `brand.json`; the Agate files are deleted. `scripts/build_brand_assets.py` rebuilds them from `Final_v3/` (`--check` matches). |
| Locator map | `scripts/build_locator_map.py` applies the brand map rule (Night-family neutrals, dashed Magma area-of-interest callout with a Night halo, no Amber or Glow); new checksum-named SVG `kizildere-locator-006fcf1f.svg`, old one removed; `web_m6.locator_map` in `sources.json` updated (path, bytes, SHA-256, generator colours). |
| Target frame | The Act 4 target frame on the homepage priority result is Magma light (it was gold). |
| Caption tone | `script.js` `CAPTION_TONE_CROSSOVER` 0.1885 → 0.1967 for Mist / Ink captions. |
| Validator | `BRAND_TOKENS` (14 hexes and 4 alphas), 19 contrast pairs, no other colour, every Agate, Atlas and older token retired, no amber fill, `brand_checks` (identity "Heat Trace", palette record, files and hashes, SVG paints per ground, logo viewBox and carried colours, page heads, header and footer markup, 120 px minimum, manifest, locator map callout dashed Magma and no Amber or Glow) and a derived check that `CAPTION_TONE_CROSSOVER` equals the value computed from the Mist and Ink tokens. |
| Tests | `scripts/negative_tests_agate_brand.py` is renamed `negative_tests_brand.py` and has 43 cases (it had 38); every earlier suite follows the new tokens, files and messages. |
| Records | `docs/WEB_HEAT_TRACE_BRAND_AUTHORITY.md` (new, with a Turkish summary for the CTO); the Agate, Atlas and light-theme documents marked superseded or recoloured; `CLAUDE.md`, `IMAGERY_RIGHTS.md`, `STATUS.md`, `CHANGELOG.md`; this file; `evidence/heat_trace/` (browser measurement scripts and results). |
| Not changed | Page set, navigation, URLs, redirects, homepage structure and four acts, all imagery, every scientific raster, the hero video and its encodes, copy (EN and TR), fonts, type scale, dictionary keys, the light-theme page map, `vercel.json`, `sitemap.xml`, `robots.txt`, og images. |

`git diff --shortstat 7be2907..f33164a`: 52 files changed, 1,073 insertions(+), 483 deletions(-) (excluding this file and the records commit).

## 2. Automated verification (tested commit, container, detached worktree)

| Check | Result |
| --- | --- |
| `scripts/validate_site.py` | PASS, 0 warnings |
| `scripts/build_tr_pages.py --check` | byte-identical |
| `scripts/build_brand_assets.py --source <Final_v3/> --check` | matches a fresh build (7 files) |
| `scripts/build_fonts.py --check` | not run (needs the network and `fontTools`; fonts and `assets/fonts/` are untouched by this work) |
| `scripts/negative_tests_brand.py` | 43/43 caught (restored tree: site PASS, identical to baseline) |
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
| `hero/scripts/validate_hero.py` | 412 checks, 13 failed: exactly the git-ignored source-texture checks of a fresh clone (5 texture hashes, 8 asset paths under `hero/assets/source/`), unchanged from the baseline |

Total: 577 deliberate regressions across 14 suites, all caught. A case counts only when the validator fails with the expected text on an `ERROR` line the unmutated baseline did not print.

## 3. Browser verification (headless Chromium, local static server, 1440 and 390 px)

| Measurement | Result |
| --- | --- |
| Text contrast, solid grounds | 1,354 text nodes on 13 routes (English and Turkish) at two widths; 0 below 4.5:1 (3:1 for large text). Text over photographs, the hero, figures and caption labels is judged by the caption-tone rule and is not in this audit. `evidence/heat_trace/measure_contrast.py`, `measurements/contrast_audit.json`. |
| Focus ring | 14 keyboard stops on the homepage, every one a visible 2 px solid ring: Magma `#CD1B74` on light grounds (5.24:1 on white), Magma light `#F94997` on dark grounds (5.89:1 on Night). `measurements/states.json`. |
| Hover | Navigation link Ink soft → Ink; the ghost button fills Mist with an Ink label, 14.17:1. |
| Overflow, console, network | 13 routes at 320, 360, 390, 768, 1024 and 1440 px: no horizontal overflow, no console error, no failed request. The header logo box is 120.4 × 28 px at ≤ 560 px and 137.6 × 32 px above; the header is 76 px high up to 980 px and 88 px on the desktop nav, with the navigation fitting at 1024 px. `evidence/heat_trace/measure_overflow.py`, `measurements/overflow.json`. |
| Hero seam | Hero left edge `(26,14,28)`, `(25,13,27)`, `(23,11,25)` against Night `(22,10,25)`; the header is white, so the join is a clear boundary. The video's own navy-black space is render content and is not recoloured. |
| Mobile menu | Opens with the button, keeps the white header, rows legible, language switch visible (`menu_m.png`). |

Not re-measured here: the reduced-motion path and the per-route 1,937-node text audit of the Agate evidence. This change touches colour and the logo's size only (the new lock-up is taller and narrower than the Agate one: 32 / 28 px high against 30 / 24 px, and 138 / 120 px wide against 176 / 141 px, because its proportions are 619 × 144 instead of 634 × 108; both widths are at or over the brand's 120 px minimum); the reduced-motion code is untouched.

## 4. Open points and residuals

1. Fonts: the brand token file names Mona Sans and Martian Mono; the site keeps its self-hosted Plex subsets (decision for the CTO).
2. Hero: the video's baked navy-black space stays (a re-render on a Night space background is a separate task).
3. `og:image` is still the hero poster, which has no logo.
4. `build_fonts.py --check` was not run (§2).
5. The package's Review pages (`*.dc.html`) need a network to render and were not used; the PNG previews and the READMEs were.
6. Nothing is merged, deployed or published.

## 5. Screenshots (project Library, `heat-trace/screenshots/`)

`home_d.png` (homepage, 1440 px, full page), `home_d_top.png` (first viewport), `geo_d.png` (Geothermal with the locator map), `sol_d.png` (Solutions), `about_d.png`, `partner_d.png`, `tr_home_d.png`, and at 390 px `home_m.png`, `geo_m.png`, `sol_m.png`, `tr_home_m.png`, `menu_m.png` (mobile menu open).
