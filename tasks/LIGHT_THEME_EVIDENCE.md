# Light theme and plain-spoken pages — evidence

**Status:** `REVIEW_READY`, preview only. Not merged, not deployed, no DNS or domain action.
**Branch:** `claude/project-thread-75kouq`, branched from the Agate branch `claude/project-thread-wbral7@8f2d8ad48f7b246a6835e7f64575af1fe399cb69` (MER-279, pull request #1). Pull request #2 targets that branch, not `main`.
**Tested commit:** `cc850fbdf00f20384513abab9244cad26d6aa890`. Every check below ran on that commit (the suites in a detached worktree of it, one at a time). The branch HEAD is the tested commit plus one commit that adds only this file and `STATUS.md`; `git diff cc850fb..HEAD` shows nothing else, and neither file is deployed (`.vercelignore`).
**Preview:** `orbgss-website-git-claude-project-thread-75kouq-virga-soft.vercel.app` (deployment of the tested commit `orbgss-website-4rjc96z7t-virga-soft.vercel.app`, READY; protected, reached from cloud sessions through the proxy bypass).
**Authority:** `docs/WEB_LIGHT_THEME_AUTHORITY.md`. **Screenshots:** the project Library, folder `light-theme/` (indexed in §5).
**CTO request:** 2026-10-25, two messages (the pages are too dark and need contrast; the homepage needs the same contrast; the public site must not explain how the app works behind the scenes).

## 1. What changed

| Area | Change |
| --- | --- |
| Theme | Header and footer are white (`--white` `#FFFFFF`); pages sit on Limestone; Ground and Ground lift stay for photographs and the priority result. Components read role variables (`--fg`, `--fg-2`, `--link`, `--limit`, `--limit-line`, `--hair`, `--hair-soft`, `--surface`, `--matte`, `--wash`) that the light scope (`.ground-paper`, `.site-header`, `.site-footer`) and the dark scope (`.ground-orbit`, `.ground-lift`, `.domain-card`, `.domain-band`) each define. |
| Homepage | Hero video and the Kızıldere band stay dark; the Act 3 evidence trio, the inspection aid and the Solutions section are light; the Act 4 priority result and the Partner line stay dark. |
| Logo | The horizontal logo for light grounds replaces the dark-ground logo in the header and footer on all 13 pages; `scripts/build_brand_assets.py` role `logo-light`, `assets/brand/orbgss-logo-light.de682b8e.svg`; the dark-ground logo is no longer shipped. `theme-color` and the manifest colours are `#FFFFFF`. |
| Removed navigation | The in-page section bars: the Geothermal chapter bar, the Sources index, the Solutions pilot bar. |
| Removed warnings | The warning under every plate of the Geothermal layer atlas, the warning under the priority result and under the Kızıldere band, the legacy `story.*.note` warnings, the Geothermal ledger of what the result does and does not establish (English and Turkish). |
| Removed explanation | Every sentence on how a layer is used, what it is not, how the score is built (homepage Acts 3 and 4, the inspection note, the structure-gap footnote, the Geothermal glance and gap copy); "limits" in titles, descriptions and the About position statement. |
| Kept | The score's public label, the claim discipline in copy, the illustrative-imagery footnote on Solutions, the hero's "Rendered orbital sequence — not sensor imagery" line, every caption's place, coordinates and layer line, the data-gap and "accepted, not shown yet" placeholders, the footer attribution. |
| Validator | `scripts/validate_site.py`: the `--white` token and its contrast pairs, header and footer on white, both role scopes, the grounds per page, the `logo-light` role, white theme colour and manifest, no in-page bar class, no `.beam-note` / `.plate-note` / `.warning-label`, no retired explanation or warning key in the dictionary or on any page (`RETIRED_EXPLANATION_KEYS`), `public_warnings` in the manifest. |
| Tests | `scripts/negative_tests_light_theme.py` (14 cases, new); ten earlier suites follow the new grounds, strings and logo file. |
| Records | `docs/WEB_LIGHT_THEME_AUTHORITY.md` (new); `docs/WEB_AGATE_BRAND_AUTHORITY.md`, `docs/WEB_ATLAS_DESIGN_AUTHORITY.md`, `docs/WEB_ATLAS_GEOTHERMAL_AUTHORITY.md`, `docs/WEB_INTERIOR_REDESIGN_AUTHORITY.md`, `CLAUDE.md` amended; `assets/imagery/sources.json` → `public_warnings` (status `retired`, CTO 2026-10-25; the seventeen `visible_warning` records stay as the wording of record); `STATUS.md`; this file. |
| Not changed | Page set, navigation, URLs, redirects, hreflang, sitemap, the four-act order, the Solutions cards' links, the contact route, all imagery, every governed raster and its derivatives, windows and checksums, the hero video and its encodes, fonts and type. |

## 2. Automated verification (tested commit, container, detached worktree)

| Check | Result |
| --- | --- |
| `scripts/validate_site.py` | PASS, 0 warnings |
| `scripts/build_tr_pages.py --check` | byte-identical |
| `scripts/build_brand_assets.py --source <unpacked final/> --check` | brand assets match a fresh build (7 files) |
| `scripts/negative_tests_agate_brand.py` | 38/38 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_atlas_foundation.py` | 46/46 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_atlas_geothermal.py` | 43/43 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_atlas_solutions_about.py` | 39/39 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_atlas_partner_sources.py` | 34/34 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_mer216.py` | 19/19 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_mer237.py` | 29/29 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_mer240.py` | 46/46 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_mer241.py` | 51/51 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_mer255.py` | 49/49 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_web005.py` | 72/72 caught (restored tree: site PASS; the hero check fails exactly as on the baseline, the 13 source-texture checks) |
| `scripts/negative_tests_web005b.py` | 55/55 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_web005c.py` | 18/18 caught (restored tree: site PASS, identical to baseline) |
| `scripts/negative_tests_light_theme.py` | 14/14 caught (restored tree: site PASS, identical to baseline) |
| `hero/scripts/validate_hero.py` | 412 checks, 13 failed: exactly the git-ignored source-texture checks of a fresh clone (five scene texture hashes, the detail multiplier hash and the eight `hero/assets/source/` paths); the Agate base has the same 13 |

Earlier, while the suites were being brought up to date, every case that referred to a removed class, string or file was retargeted at what replaced it, never loosened; a suite counts a case as caught only when the validator fails on the in-memory mutation.

## 3. Measured in the browser (headless Chromium, local build of the same files; reduced motion, so the hero is its static poster)

**No horizontal overflow.** 13 routes (six English, six Turkish, the 404) at 320, 390, 768, 1024 and 1440 px: `scrollWidth` equals the viewport everywhere, and no element extends past the right edge unless an ancestor with `overflow:hidden` that itself ends inside the viewport clips it (that exempts only the inspection aid's deliberately cropped, zoomed base image, unchanged since the Agate branch). The Preview screenshots at 390 and 1440 px also report `scrollWidth` equal to the width on all 16 pages.

**Contrast.** Every text node was read against the colour it renders on (ancestor backgrounds composited), skipping text that sits on a photograph or video (judged by the per-panel caption-tone rule and its halo, unchanged). Twelve content routes (six English, six Turkish) at 1440 and 390 px: 1,742 text nodes judged off a photograph, all at or above 4.5:1 except two kinds of node the script cannot judge or should not:

* the language separator `|` (`aria-hidden`, decorative) at 1.48:1;
* the closing line ("Partner With Us →", "Discuss a pilot →" and the Turkish equivalents) which stands on a CSS gradient of Ground `#171A1B`; the script treats any `background-image` as unknown and reports the Limestone below it. Against its real ground the line is Mist `#E3E5E4` on Ground `#171A1B`, 13.83:1.

Figures per route are in the table below (text nodes read / of which over imagery, so not judged here / judged and under 4.5:1 for a reason other than the two above).

| Route | 1440 px | 390 px |
| --- | --- | --- |
| `/` and `/tr/` | 79 / 28 / 0 | 72 / 25 / 0 |
| `/solutions/` and `/tr/cozumler/` | 58 / 15 / 0 | 51 / 15 / 0 |
| `/solutions/geothermal/` and `/tr/cozumler/jeotermal/` | 134 / 27 / 0 | 127 / 21 / 0 |
| `/about/` and `/tr/hakkimizda/` | 66 / 3 / 0 | 59 / 3 / 0 |
| `/partner/` and `/tr/is-birligi/` | 39 / 3 / 0 | 32 / 3 / 0 |
| `/sources/` and `/tr/kaynaklar/` | 152 / 0 / 0 | 145 / 0 / 0 |

(English and Turkish counts are identical because the Turkish pages are generated from the English markup.)

**Header and footer.** White (`rgb(255,255,255)`) on every route; the logo is `orbgss-logo-light.de682b8e.svg` at 120 px or wider.

## 4. What was looked at

The Preview screenshots were looked at after capture: the homepage and the Geothermal page in full at 1440 px; Solutions, About, Partner and Sources at 1440 px; the homepage, Geothermal, About and the Turkish homepage at 390 px. The Turkish Geothermal page and the remaining mobile pages were captured but read only through the measurements above. At 1440 px the homepage reads hero (dark) → Kızıldere band (dark) → three-layer trio (light) → priority result (dark) → inspection aid (light) → Solutions (light) → Partner line (dark) → white footer; the Geothermal page reads dark photographic opening → light pilot record and layer atlas (no warning under any plate) → dark priority result with the empty relief slot → light "what is missing" → dark closing line → white footer. The hero seam recorded in the Agate document is gone: the white header meets the dark hero as a boundary.

## 5. Screenshot index (project Library, folder `light-theme/`)

Full-page, Preview of the tested commit, reduced motion: `home`, `solutions`, `solutions_geothermal`, `about`, `partner`, `sources`, `tr`, `tr_cozumler_jeotermal`, each as `<name>-w1440.png` and `<name>-w390.png` (16 files).

## 6. Remaining risks and open items

* **Open for the CTO** (`docs/WEB_LIGHT_THEME_AUTHORITY.md` §6): one neutral line near the results (none added); the pilot record still lists the 30 m grid, EPSG:32635 and the score's name; "what is missing" and the two pending plates say publicly what is not yet shown; two About lines about how OrbGSS publishes; a read of the rewritten Turkish copy.
* The Geothermal "does not establish" ledger was removed together with the warnings because it is the same grammar; it is a documented, reversible decision (the wording of record stays in `sources.json`).
* Contrast of text over photographs is judged by the per-panel caption-tone rule, not audited numerically here, as on earlier branches.
* The hero video's baked navy-black render content is unchanged (a re-render is a separate decision).
* Nothing is published. Merging this pull request into the Agate branch and then publishing is a separate CTO authorization (every push to `main` is a production deployment).
