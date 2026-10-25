# MER-279 — Agate brand adoption on the existing site: evidence

**Status:** `REVIEW_READY`, preview only. Not merged, not deployed, no DNS or domain action.
**Branch:** `claude/project-thread-wbral7`, branched from the Atlas integration `claude/project-thread-07ccos@4bbbe0ee83905a0aafaa0c973154cb43f04feb93`.
**Tested commit:** `2ccc20a7b02edef2cce5e50306fac67f86a3647f`. Every check below ran on that commit in a detached worktree, one suite at a time. The branch HEAD is the tested commit plus one commit that adds only this file; `git diff 2ccc20a..HEAD` shows nothing else.
**Authority:** `docs/WEB_AGATE_BRAND_AUTHORITY.md`. **Screenshots:** the project Library, folder `agate-brand/` (indexed in §6).

## 1. What changed

| Area | Change |
| --- | --- |
| Palette | The Atlas cyan-on-navy tokens are replaced by the approved Agate palette in `styles.css` `:root`: Graphite `#202629`, Mineral Gray `#69716F`, Agate Teal `#18777A`, Mineral Gold `#C49A5A`, their dark-ground equivalents `#E3E5E4`, `#B7C0BD`, `#58AEB2`, `#D8B173`, and derived Ground `#171A1B`, Ground lift `#252A2B`, Limestone `#F6F5F2`, Graphite soft `#565D5A`, Gold ink `#735525`. Teal is the interactive accent; gold is a restrained non-fill highlight; no copper, no navy surface. Grounds keep their structural class names. |
| Marks | New horizontal logo in the header and footer of all 13 pages (six English, six Turkish, the 404); the footer logo's alt text is "OrbGSS" because the supplied logo carries no tagline (it was "OrbGSS — Orbital Geo-Spatial Solutions"); favicon SVG and `favicon.ico`; 180 px touch icon; 192 / 512 px manifest icons; `theme-color` and manifest colours `#171A1B`. Hash-named files in `assets/brand/` (and `/favicon.ico`), recorded in `assets/brand/brand.json`, rebuilt by `scripts/build_brand_assets.py`. `assets/logo.svg` and `assets/mark.svg` deleted. |
| Locator map | `scripts/build_locator_map.py` recoloured to the brand map rule; new checksum-named SVG, old one removed; record in `sources.json` → `web_m6.locator_map`. |
| Caption tone | `script.js` `CAPTION_TONE_CROSSOVER` 0.185 → 0.1885 for Mist / Graphite captions. |
| Validator | Palette pins, 14 contrast pairs, no other colour, no Atlas token, no gold fill, and `agate_brand_checks` (recorded files and hashes, SVG paints, page heads, header and footer markup, 120 px logo minimum, manifest, `.vercelignore`, locator map). |
| Tests | `scripts/negative_tests_agate_brand.py` (32 cases, new); the Atlas page-group and earlier suites follow the new tokens and files. |
| Records | `docs/WEB_AGATE_BRAND_AUTHORITY.md` (new), Atlas authority marked superseded on colour, `CLAUDE.md`, `STATUS.md`, `CHANGELOG.md`, `IMAGERY_RIGHTS.md`, this file, `evidence/mer279/` (tooling and raw results). |
| Not changed | Page set, navigation, URLs, redirects, homepage structure and four acts, all imagery, every scientific raster, the hero video and its encodes, copy (EN and TR), fonts, type scale, dictionary keys, `vercel.json`, `sitemap.xml`, `robots.txt`, og images. |

`git diff --shortstat 4bbbe0e..2ccc20a` (the tested commit): 59 files changed, 5162 insertions(+), 380 deletions(-).

## 2. Automated verification (tested commit, container, detached worktree)

| Check | Result |
| --- | --- |
| `scripts/validate_site.py` | PASS, 0 warnings |
| `scripts/build_tr_pages.py --check` | byte-identical |
| `scripts/negative_tests_agate_brand.py` | 32/32 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_atlas_foundation.py` | 43/43 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_atlas_geothermal.py` | 43/43 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_atlas_solutions_about.py` | 37/37 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_atlas_partner_sources.py` | 34/34 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_web005.py` | 72/72 caught (restored tree: site PASS; the hero check fails exactly as on the baseline, the 13 source-texture checks) |
| `scripts/negative_tests_web005b.py` | 55/55 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_web005c.py` | 18/18 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_mer216.py` | 19/19 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_mer237.py` | 29/29 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_mer240.py` | 46/46 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_mer241.py` | 51/51 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_mer255.py` | 49/49 caught (restored tree: site PASS, identical to baseline) |
| `scripts/build_brand_assets.py --source <final/> --check` | brand assets match a fresh build (7 files); package SHA-256 `56f749ec…b185f3` |
| `scripts/build_fonts.py --check` | `fonts.json` matches a fresh build (fonts untouched) |
| `py -3.14 hero/scripts/validate_hero.py` | 412 checks, 13 failed: exactly the 13 git-ignored source-texture checks of a fresh clone (5 SHA-256 on-disk, 8 materialized-path); the Atlas base gives the same 13 and nothing else fails, including "public-site changes since the baseline stay inside the integration write surface" |

## 3. Browser measurements (Chromium via Playwright, served from each checkout; `evidence/mer279/measure.py`)

**Layout, 13 routes × 6 widths (320, 360, 390, 768, 1024, 1440) = 78 cells.** Routes: `/`, `/solutions/`, `/solutions/geothermal/`, `/about/`, `/partner/`, `/sources/`, their six `/tr/` pages and `404.html`.
* Horizontal overflow: none in any cell.
* Console errors and page errors: none. Failed (≥ 400) responses: none.
* Icon links (`/favicon.ico`, the SVG favicon, the touch icon, the manifest) resolve with 200 on every page's head.
* `theme-color` is `#171A1B` on every page.
* Header logo 141 × 24 px at ≤ 560 px and 176 × 30 px above; footer logo 205–225 px wide. Natural width 634 px. Brand minimum 120 px: held in every cell.

**Contrast, every visible text element on a solid ground (`measure.py --only contrast`), 13 routes at 1440 and 390 px.** 1,937 elements checked against 4.5:1 (3:1 for large text), computed colour alpha-blended over the nearest solid background. Text over photographs or background images (332 elements: hero, captions on imagery, card labels) is not audited by this method; it is governed by the caption-tone rule and was checked by eye on the sheets. The only element under its floor is the decorative `|` between EN and TR (`aria-hidden`, 1.63:1 at the line colour), at 1440 on all 13 routes; it was the same kind of element in the Atlas build. Every other element is at or above its floor; the palette pairs themselves are 4.59:1 to 14.05:1 (`docs/WEB_AGATE_BRAND_AUTHORITY.md` §1).

**Interaction states** (`states.py`, `measure.py --only states`, Tab walk of 58–59 stops on each of 7 routes; raw `evidence/mer279/measurements/states.json`):

| State | Measured |
| --- | --- |
| Navigation and footer link, rest → hover | Mineral Light `#B7C0BD` (9.41:1) → Mist `#E3E5E4` (13.83:1) |
| Current navigation item | Mist (13.83:1) with a 1 px Teal Light underline |
| Language switch, active / inactive | Teal Light (6.76:1) / Mineral Light → Mist on hover |
| Body link (mailto on Partner), rest → hover | Mist → Teal Light (6.76:1) |
| Focus ring (`:focus-visible`) | 2 px Teal Light at 4 px offset, 6.76:1 on the ground, on the brand link, navigation, trigger, language switch, footer links, controls and the skip link; card links (`.domain-link`) draw it on their `::after`. Every one of the Tab stops had an outline of at least 2 px and at least 3:1. The first sweep flagged the skip link at 2.37:1 because it measured the ring against the link's own Limestone chip; the ring is drawn 4 px outside the chip on the page ground, where it measures 6.76:1 (`states.json`, "skip link"). |
| Ghost button (`.button`) hover | measured: fill Mist `#E3E5E4`, label Graphite `#202629` (12.11:1); never gold, never teal |

**Mobile navigation (390 × 844, touch, `/`, `/solutions/`, `/tr/`):** the toggle is visible, the list is hidden at rest, `aria-expanded` is true after a click, the menu opens on the Ground background, closes with Escape (`aria-expanded` false) and with the toggle; rows are 44–46 px high. See `agate-brand/comparison/01b-home-menu-open-m390.jpg`.

**Reduced motion** (`prefers-reduced-motion: reduce`, `/`, `/solutions/`, `/solutions/geothermal/`): no running animations, the hero video has no source attached and is paused, and the number of elements with a transition is 50 / 24 / 26, identical to the Atlas base (`measurements/measure_atlas_motion.json`): the rebrand adds no motion.

**First-load weight** (all requests, decoded body bytes; production = `main` as served, 5 routes, no `/sources/` there):

| Route @ width | Production | Atlas | Agate |
| --- | --- | --- | --- |
| `/` @1440 | 1846.8 KiB, 10 req | 1971.0 KiB, 13 req | 1976.9 KiB, 13 req |
| `/` @390 | 539.5 KiB, 8 req | 663.6 KiB, 11 req | 669.5 KiB, 11 req |
| `/solutions/` @1440 | 961.8 KiB, 7 req | 1364.4 KiB, 10 req | 1370.3 KiB, 10 req |
| `/solutions/geothermal/` @1440 | 186.6 KiB, 6 req | 847.2 KiB, 13 req | 853.2 KiB, 13 req |
| `/about/` @1440 | 160.6 KiB, 5 req | 471.7 KiB, 9 req | 477.6 KiB, 9 req |
| `/partner/` @1440 | 157.5 KiB, 5 req | 404.9 KiB, 9 req | 410.8 KiB, 9 req |

The brand change adds 5.9 KiB per page over the Atlas base (the logo SVG is 4.9 KB against 1.1 KB, plus the favicon request), with the same number of requests. The difference between production and Atlas is the Atlas redesign (fonts, imagery on the new pages), not this task. Incidentally, in the Atlas base `/about/` at 390 px loads 2.4 MB of WebP (184 KB at 1440); that is unchanged here and outside this task, noted for the Atlas review.

## 4. The CTO brief, point by point

| Brief | Evidence |
| --- | --- |
| Replace logo, symbol, favicon, touch icon, social-brand assets with the approved Agate versions (not variant-b) | §1; `assets/brand/brand.json`; `agate-brand/comparison/00-logo-closeups.jpg`, `00b-favicon-and-icons.png`. The social image (`og:image`) is the hero poster, which carries no logo; a branded card is an option (§7). |
| Translate the palette into tokens; Graphite neutrals, Teal interactive, Gold restrained; no copper, no navy surfaces, no AI-dashboard look | `docs/WEB_AGATE_BRAND_AUTHORITY.md` §1; validator rejects any other colour, any Atlas token, any gold fill. |
| Preserve structure, four-act homepage, imagery, exports, captions, navigation, URLs, scientific statements | The HTML diff is limited to the head (icon links, theme colour), the header and footer brand markup and the locator-map file name; no body copy, image or URL changes. 78-cell layout matrix; `01-` to `03-` homepage sheets. |
| Do not use `illustrative-map.jpg`; do not recolour scientific rasters | Validator fails if it is placed or shipped; no existing raster changed (the only new rasters are the brand icons, and the only changed image file is the locator SVG). |
| No new theme switch; static stack; no new dependencies | None added: no new script, library, font request or package file; fonts unchanged. |
| Contrast, hover, focus, reduced motion, responsive, mobile nav | §3. |
| Validate with the canonical validators and negative suites | §2. |
| Before and after screenshots of the real homepage and key pages against production **and** the Atlas preview | §6. |
| Reviewable PR with exact HEAD and evidence; no merge, deploy or domain change | This branch and its pull request (base: the Atlas integration branch). |

## 5. Constraints held

No push to `main`, no merge, no Vercel production deployment, no DNS or domain change, no force-push or history rewrite. The Atlas CTO-open items are untouched: A1 (MER-151 derivatives full-size on the Geothermal page), the CTO's reading of the new Turkish copy, the font and colour-map licence links and the empty MER-242 slots. The Natural Earth file used to rebuild the locator map is the same pinned v5.1.2 `ne_50m_admin_0_countries.geojson` the page already credits (SHA-256 `3e458fc0…` equals the recorded one; fetched through the pinned jsDelivr mirror, not committed).

## 6. Screenshot index (project Library, `agate-brand/`)

Each sheet has three columns: **Production** (the live site as of 2026-10-25; its HTML for the five production routes was compared byte for byte with the checkout the screenshots came from), **Atlas preview** (the base of this branch) and **Agate** (this branch).

| File | Shows |
| --- | --- |
| `comparison/00-logo-closeups.jpg`, `00b-favicon-and-icons.png` | Header and footer logo at 3×; favicon at 16–128 px, in dark and light tabs against the old mark; the three `.ico` frames; touch and manifest icons |
| `comparison/01-home-hero-d1440.jpg`, `…-m390.jpg` | Homepage hero 0.9 s after load and settled |
| `comparison/01b-home-menu-open-m390.jpg` | Mobile menu open |
| `comparison/02-home-acts-*.jpg` | Header, Act 2 band, Act 3 evidence trio, Act 4 priority result |
| `comparison/03-home-lower-*.jpg` | Inspection aid, Solutions cards, footer |
| `comparison/04-` to `08-` | Solutions, Geothermal (with the recoloured locator map), About, Partner, Sources: full length, 1440 and 390 px |
| `comparison/09-tr-and-404-d1440.jpg` | Turkish homepage and About, and the 404 (Agate only) |
| `native-hero/*.png` | The settled hero at native size for the three builds |
| `states/` | Focus and hover crops, Solutions card focus ring and hover, `states.json` |
| `measurements/` | The raw JSON behind §3 |

## 7. Residuals and decisions that stay with the CTO

1. **Hero seam.** The hero video's baked space is a navy-black (`rgb(3,12,22)`); the header and page ground are Graphite `#171A1B`. On the homepage the left of the hero reads slightly bluer than the header. It is render content, not a UI colour, so it is not touched (no filter, no blend, no re-encode). Re-rendering on a Graphite space background is a separate task (new master frames, encode ladder, shot audit). The sheets `01-home-hero-*` show the seam.
2. **Social card.** `og:image` is still the hero poster. A Graphite card with the logo is an option.
3. **Decorative separator** at 1.63:1 (§3), unchanged in kind.
4. **Icons as supplied.** The 192 / 512 px icons have transparent rounded corners; no maskable variant was supplied.
5. **Open Atlas items** stay open (§5).
