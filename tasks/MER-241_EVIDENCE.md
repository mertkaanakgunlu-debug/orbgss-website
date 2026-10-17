# MER-241 — static Turkish pages (evidence)

**Issue:** MER-241 (Milestone 6 — Bilgi Mimarisi ve Gösterim Odaklı Sayfalar), Linear "Web sitesi: Türkçe statik sayfalar (/tr/)".
**Authority:** `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md` (MER-238, CTO-approved 2026-10-15; D2 Turkish slugs), the rules in `CLAUDE.md` § "Milestone 6 target".
**Branch:** `claude/mer-241-turkish-static-pages-sihwiy`, from `main@81d1f911d9b99abc25ba692012870b874eb2880d` (= production's site files; `a2045344` plus the MER-240 records commit).
**State:** `REVIEW_READY`. Nothing is merged, deployed or published, and `main`, DNS, Vercel settings and credentials are untouched. The final HEAD SHA is in the Linear report and the thread reply (a commit cannot name itself).

## 1. Scope and what was deliberately not done

In scope: the five static Turkish pages, the language switch as real links, the per-page language metadata, the sitemap, a bilingual 404, the validator rules and their negative suite, and the `.vercelignore` / lane records.

Not done, on the CTO's instruction: no redesign of any page, no dark / light theme toggle (the CTO will plan the pages one by one later), no new copy, no new claim. The Turkish text on every page is the Turkish value the `I18N` dictionary already held in production; this task added **no dictionary key and changed no Turkish string**. No company, legal or Esri-partnership statement was added.

## 2. What changed

| Area | Change |
| --- | --- |
| Generator | New `scripts/build_tr_pages.py` (standard library only, local tooling, nothing runs on Vercel). It parses the five English pages and the `I18N` dictionary in `script.js`, replaces every `data-i18n` / `data-i18n-html` / `data-i18n-alt` / `-aria-label` / `-content` / `-href` string by its Turkish value, and writes `tr/index.html`, `tr/cozumler/index.html`, `tr/cozumler/jeotermal/index.html`, `tr/hakkimizda/index.html` and `tr/is-birligi/index.html`. It also writes `sitemap.xml` and fills the Turkish lines of `404.html`. A byte-preserving edit engine (HTML tokenizer, offsets, no re-serialisation) keeps everything outside the replaced strings identical to the English page. It stops on a missing Turkish key, an internal link with no Turkish twin, markup inside a translated element, or an asset URL it cannot make root-absolute. Output is deterministic (no clock): a second run is byte-identical; `--check` exits 1 when anything on disk differs. |
| Turkish pages | `<html lang="tr">`, Turkish title / description / og tags, `canonical` and `og:url` of the Turkish URL, `og:locale tr_TR` with `en_US` as alternate, every internal link and the footer links pointing at the Turkish twin, anchor ids unchanged (every alias, `#mineral`, `#pilot-*`, …, works under `/tr/`), and root-absolute asset URLs so the homepage's relative `assets/…` paths do not break one directory down. A generated-file comment follows the doctype. |
| Language switch | EN and TR are two real `<a>` links with `hreflang`, `lang` and `aria-current="true"` on the current one, on every page (English, Turkish, 404). They navigate without JavaScript. There is no redirect by browser language. |
| `script.js` | The runtime language swap is gone (`applyLanguage`, the attribute map, the button handlers, the stored-language read). The page language is `document.documentElement.lang`. **Storage decision:** the site now neither reads nor writes `localStorage`; a leftover legacy `orbgss.lang` entry is removed once (`removeItem`). Consequence for MER-238 D3 (privacy): after this change the site stores nothing in the visitor's browser (`docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md` D3 facts updated). The dictionary itself is still inside `script.js`, because the generator and the validator read it there; at runtime only `nav.open` / `nav.close` use it. Moving the dictionary out of the shipped file is a possible later slimming and was not done (it would touch the hero-protected `script.js` beyond this scope). |
| Search / sharing | Each page lists three `rel="alternate"` links (`en`, `tr`, `x-default` → English) on both languages, reciprocal. `sitemap.xml` has 10 URLs, each with `xhtml:link` alternates for en, tr and x-default (namespace declared); the lastmod date is a constant. |
| 404 | One page serves every unknown path on Vercel, so `404.html` answers in both languages: the English headline, one Turkish line (`Bu sayfa ilgi alanının dışında.`) and two ways back (`/` and `/tr/`). Its navigation chrome stays English (limitation, §6). No Turkish redirects exist or were needed: the old routes never had `/tr/` versions. |
| Styles | `.lang-btn` as a link (inline-block, centred) with an accent colour for `aria-current="true"` (replaces the `aria-pressed` rule), and `.not-found-links`. No visual change otherwise. |
| `.vercelignore` | `!tr` added to the allowlist (deploy set: 13 root entries, 119 files). |
| Validator | `scripts/validate_site.py` gains the MER-241 block: stray files under `tr/`; the committed tree equals the generator's output byte for byte; per-page lang, canonical, og:url, og:locale, hreflang set equality and reciprocity; the two switch links; every visible string and translated attribute equals the dictionary's value in the page's effective language (a small, explicit allowlist covers brand names, numbers and coordinates), for English, Turkish and 404; English / Turkish parity of skeleton, assets, ids, hero ladder and data slots (the science is identical); internal links map to Turkish pages and every fragment resolves; the Turkish mandatory scientific warnings are present; sitemap alternates; `script.js` has no language swap, no stored preference, no browser-language redirect, and the 404 carries both languages. 844 strings were checked on the final run. |
| Negative suite | New `scripts/negative_tests_mer241.py`, 44 deliberate regressions (missing twin, stray `/tr/` file, hand-edited generated page, dictionary change not regenerated, wrong or missing hreflang / canonical / og:locale, English text left on a Turkish page, switch not a link, lost warning, changed asset or id, English link left on a Turkish page, sitemap alternate missing, `script.js` stores a preference or redirects, 404 loses a language, `.vercelignore` loses `!tr`, …). Two sitemap cases in `negative_tests_mer240.py` follow the new sitemap format (still 46/46). |
| Production tools | `evidence/mer219/smoke_production.py` and `browser_checks_production.py` understand `/tr/` (routes, the real switch links, the bilingual 404). **They were edited but not executed** in this container (the browser tool is a Windows CDP harness and the smoke tool needs production); the reviewer should run `smoke_production.py` on the Preview before any publication. |
| Records | `CLAUDE.md` (generated-file rule, change discipline), `STATUS.md`, `README.md`, `docs/HANDOFF.md`, `CHANGELOG.md`, `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md` (D3 fact) and the text fields of `hero/config/lane.json`. |

Diff against the baseline: the English pages change only by the language-switch markup, the hreflang and `og:locale` lines, and one `data-i18n-alt` on the no-JS hero image (its alt text was English-only; the key `alt.heroPriority` already existed). Hero media, ladder, camera, poster, drape, analytical derivatives, copy and layout are untouched; `index.html` keeps `data-hero-tiers`, which the validator compares with the Turkish homepage.

## 3. Verification (container, 2026-10-17)

| Check | Result |
| --- | --- |
| `python3 scripts/build_tr_pages.py --check` | OK, byte-identical |
| `python3 scripts/validate_site.py` | **PASS, 0 warnings** (5 routes + 404, 277 i18n keys, 844 strings checked on the Turkish pages and 404, 13 deploy-set root entries / 119 files) |
| `negative_tests_web005.py` / `_web005b.py` / `_web005c.py` / `_mer216.py` / `_mer237.py` / `_mer240.py` | 72/72, 55/55, 18/18, 19/19, 29/29, 46/46 caught; restored tree identical |
| `negative_tests_mer241.py` | **44/44 caught**; restored tree validates identically (CRLF-safe) |
| `python3 hero/scripts/validate_hero.py` | 412 checks, 13 failed: exactly the git-ignored source-texture checks (eight `materialized local path exists`, five SHA-256 on disk), the accepted fresh-clone result; the lane-boundary checks pass. Identical with and without this change. (The accepted 420/0 is the hero workstation's.) |

## 4. Browser acceptance (Chromium via Playwright, `evidence/mer241/tools/`)

`vercel_like_server.py` serves the repository as the Vercel project does (reads `vercel.json` and `.vercelignore`: clean URLs, trailing slash 308, the four 301s, internal paths 404, a real 404 status with `404.html` for every unknown path, range requests for the hero video). `check_mer241.py` ran in full: **240 page loads, 0 failures** (report: `evidence/mer241/browser_report.json`).

| Check | Result |
| --- | --- |
| Sweep: 10 pages (5 English, 5 Turkish) × widths 375, 390, 414, 768, 1024, 1280, 1440, 1920, 2560, 3840 CSS px × DPR 1 and 2 (3 up to 768 px) | 0 horizontal overflow, 0 broken images, 0 console errors, 0 failed requests; correct `<html lang>`; header height identical in EN and TR at every width (76 px ≤ 768, 88 px above), so no label wraps |
| No JavaScript, all five pairs | Each page is complete in its own language; the TR link reaches the Turkish twin (right title, h1, `hreflang` triple) and the EN link returns |
| Stored preference | `orbgss.lang = tr` on an English page, `en` on a Turkish page: the page language does not change, and the entry is removed |
| Mobile menu | English "Open navigation" / "Close navigation"; Turkish "Menüyü aç" / "Menüyü kapat"; the language switch stays visible in the open menu |
| Hero on `/tr/` | Same WebM request as `/` (root-absolute `/assets/hero/orbgss-hero-1920-ca741624.webm`, nothing under `/tr/assets/`), state `playing`, same tier and codec, every request 200 or 206. The check emulates a 4g connection because the container reports `downlink` 1.45, which makes `script.js` choose the held still ("slow-network") on both languages alike. |
| 404 | `/no-such-page/`, `/tr/yok/`, `/tr/cozumler/yok/`, `/STATUS.md`, `/tr/index.html.bak` all answer 404 with the English headline, the Turkish line and both ways back |
| Screenshots | WebP, desktop 1440 px and phone 390 px (DPR 2) of every page in both languages, plus the 404 (`evidence/mer241/*.webp`, 22 files, 5 MB). The Turkish uppercase labels render correctly (`İ`, `ı`). |

## 5. Decisions recorded in this task

| Question | Decision | Why |
| --- | --- | --- |
| What happens to the stored language preference? | Retired; the switch is a link and nothing is read or written | A stored preference that redirects or swaps text would make two URLs show one language, and would hurt search and sharing. Side effect: the site stores nothing in the browser (helps D3). |
| Redirect by browser language? | No | Same reason; the visitor picks the language by link. |
| Turkish redirects for the retired routes? | None | The old routes never existed under `/tr/` (M6 authority §6). |
| 404 | One bilingual page, not a copy under `/tr/` | Vercel serves one `404.html` for every path. |
| Where does the dictionary live? | Stays in `script.js` | The generator and the validator read it there; moving it is out of scope. |
| `lastmod` in the sitemap | A constant in the generator (`2026-10-17`) | Reproducible output; bump it when content changes. |

## 6. Remaining risks and the next gates

1. **Turkish copy is unread by a person in this task.** It is the production dictionary's existing Turkish, checked mechanically (every string equals the dictionary, nothing missing), not proofread. The CTO's reading of the Turkish pages is an acceptance item.
2. **Production tooling edits are unexecuted** (`evidence/mer219/*`, §2). Run the smoke tool against the Preview first.
3. **404 chrome is English** (navigation, footer, title): one file serves both languages. Only the headline's Turkish line and the Turkish way back are Turkish.
4. **`script.js` still ships the whole dictionary** though only two keys are read at runtime. No functional effect; a later slimming could remove it.
5. **Preview not exercised:** the local server mimics Vercel from `vercel.json`, but the real Preview (trailing slash, cleanUrls, the new `!tr` allowlist entry, hreflang as served) is untested. Vercel builds a protected Preview for this branch; the reviewer verifies `/tr/` there before any publication.
6. **Publication is a separate CTO gate.** A push to `main` is a production deployment and needs the CTO's explicit words naming it (`CLAUDE.md` § Deployment safety); then `evidence/mer219/smoke_production.py --expect-sha <sha>` and the browser checks.
7. Not run: physical Safari / Firefox / phone, a screen-reader pass, a search-console hreflang check (only possible after publication).

## 7. For the independent reviewer

1. Run `python3 scripts/build_tr_pages.py --check`, `validate_site.py`, the seven negative suites and `validate_hero.py` (13 texture failures only) on the final head.
2. Open the Preview: five Turkish routes, the EN | TR links both ways, `/tr/` no-JS, a 404 under `/tr/`, the hero video on `/tr/`, `#pilot-*` and `#mineral` aliases under `/tr/cozumler/…`, and the page source of two Turkish pages (lang, canonical, hreflang, og:locale).
3. Confirm no hero file, media, analytical derivative or English copy changed (diff of the hero lane, `assets/`, `hero/`).
4. Run `smoke_production.py` against the Preview host, then decide whether the unexecuted `browser_checks_production.py` edit needs a Windows run.
