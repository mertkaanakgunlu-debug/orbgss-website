# v6 brand adoption — evidence

**Spec:** `docs/WEB_V6_BRAND_AUTHORITY.md`. **Branch:** `claude/project-thread-v7zedp`, built on the missing-visuals head `claude/project-thread-sqytba@4223f58` (the whole unpublished chain: Atlas, Agate, light theme, Heat Trace, Violet, missing visuals, MER-242).
**Decision:** the team reviewed the candidate identities and the CTO chose `Final_v6` (2026-10-30) and asked for the site to be published; polish follows on the published site.
**Package:** `OrbGSS_Logo_Tasarim_Last.zip`, SHA-256 `9f1d0383314d980c1e542d7006b2ff8b1af3715cfe73d4ed58ceff6b111981b5`, folder `Final_v6/` (token file, README, SVG and PNG marks were the sources; the `.dc.html` design-tool pages were not used).

## 1. What changed

Palette tokens and their names, `rgba()` triples (Night, Mist, Mist soft, Muted, the two washes, the dropdown shadow), the logo and icon files, `favicon.ico`, the locator map and its record, the caption crossover, the validator pins, the brand and the other negative suites, `build_brand_assets.py`, `build_locator_map.py`, documents. No page copy, markup structure, script behaviour, image, scientific raster, hero asset or font changed.

## 2. Automated verification (container, copy of the working tree, one suite at a time)

| Check | Result |
| --- | --- |
| `scripts/validate_site.py` | PASS, 0 warnings |
| `scripts/build_brand_assets.py --source Final_v6/ --check` | files match a fresh build |
| `scripts/build_tr_pages.py --check` | byte-identical |
| `negative_tests_brand.py` | 60/60 caught |
| `_atlas_foundation.py` / `_atlas_geothermal.py` / `_atlas_solutions_about.py` / `_atlas_partner_sources.py` | 46/46, 46/46, 40/40, 34/34 |
| `_light_theme.py` / `_missing_visuals.py` | 27/27, 43/43 |
| `_web005.py` / `_web005b.py` / `_web005c.py` | 72/72, 55/55, 18/18 |
| `_mer216.py` / `_mer237.py` / `_mer240.py` / `_mer241.py` / `_mer255.py` | 19/19, 34/34, 46/46, 51/51, 49/49 |
| Total | 640 of 640 deliberate regressions caught; each restored tree validates identically to its baseline |
| `hero/scripts/validate_hero.py` | not changed by this work; a fresh clone fails exactly the 13 git-ignored source-texture checks (see §7) |
| Locator map source | Natural Earth v5.1.2 re-downloaded; SHA-256 `3e458fc0…7fdeb` equals the recorded source hash |

## 3. Browser measurements (headless Chromium, `evidence/v6/measurements/`)

| Measurement | Result |
| --- | --- |
| Text contrast (`evidence/heat_trace/measure_contrast.py`) | 13 routes (EN and TR) × 1440 and 390 px: 1,374 text nodes on solid grounds, 0 below their floor (4.5:1, 3:1 large) |
| Focus rings (`measure_states.py`) | 14 keyboard stops on the homepage, minimum ring contrast 5.25:1 (Ocean on white); dark-scope ring is Ocean light |
| Accent in use (`measure_accent_colours.py`) | Ocean 1,960 and Ocean light 488 computed colour uses at 1440 px; 0 elements still compute Violet, Violet light, the Violet-era Amber, Heat Trace Magma or the logo Magma |
| Overflow, console, requests (`measure_overflow.py`) | 13 routes × 6 widths (320 to 1440): 0 horizontal overflow, 0 console errors, 0 failed requests; header logo 120.4 × 28 px at ≤ 560 px, 137.6 × 32 px above |

## 4. Screenshots

1440 and 390 px, English and Turkish, of the homepage by act, Solutions, Geothermal, About, Partner, Sources, the Turkish homepage, Geothermal and Partner pages, the 404 page, the open mobile menu and 3× logo close-ups: project Library, `v6-brand/screens/`.

## 5. Independent review

Opus reviewer who did not implement, on `d435f7e1fdf5100a8dd9056c94cf4bab578fafd7`: **PASS WITH NON-BLOCKING NOTES, 0 blocking.** Report and screenshots: project Library, `v6-brand/review/`. Notes to carry into the polish round: the keyboard focus ring on the homepage Solutions cards is 2.40:1 against Pumice (draw it outside the card in Ocean); the second headline line over the photograph on the Geothermal page is about 2.1:1 (pre-existing); the Light theme and Atlas documents still quote Violet values; two comments cite a map-halo token that the v6 token file does not have; the validator does not catch gold as body text on a light ground or Ocean as a fill (the rendered site does neither).

## 6. Publication

Published on 2026-10-30 on the CTO's instruction ("v6 ya karar verildi. uygulayalım ve web sitesini yayınlayalım"): guards passed (`origin/main` was `81d1f911`, the head a descendant of it, the remote branch equal to the reviewed commit), then one non-force fast-forward `81d1f911` → `d435f7e1`. This published the whole unpublished chain (Atlas, Agate, light theme, Heat Trace, Violet, missing visuals, MER-242, v6; 53 commits).

| Check | Result |
| --- | --- |
| `evidence/mer219/smoke_production.py --expect-sha d435f7e1…` | 74 of 75; the one miss is the harness reading the redirect header case-sensitively (`curl -I http://orbgss.com/` answers `308` with `location: https://orbgss.com/`); served `index.html`, `script.js`, `styles.css` and `tr/index.html` are byte-identical to the commit |
| `evidence/mer219/browser_checks_production.py` | 20 of 20 |
| `/sources/`, `/tr/kaynaklar/`, `favicon.ico` | 200 |
| `/platform/`, `/pilot/`, `/company/`, `/contact/` | 301 to `/`, `/solutions/geothermal/`, `/about/`, `/partner/` |

Rollback target: the previous production deployment (`orbgss-website-o3rzsv0pl`, `main` at `81d1f911`), Instant Rollback in the Vercel dashboard (CTO action). The Vercel connector needs team re-authorization before it can list deployments.

## 7. Not run, and limits

No physical Safari, Firefox, phone or 4K panel; no Lighthouse. `validate_hero.py` shows the 13 expected source-texture failures of a fresh clone (the hero was not touched). The hero video's baked pale-cyan reticle and orbit trail remain.
