# MER-240 — Milestone 6 English pages (evidence)

**Issue:** MER-240 (Milestone 6 — Bilgi Mimarisi ve Gösterim Odaklı Sayfalar).
**Authority:** `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md` (MER-238, CTO-approved 2026-10-15), with the rules codified in `CLAUDE.md` § "Milestone 6 target".
**Branch:** `mertkaanakgunlu/mer-240-web-sitesi-yeni-sayfalarin-uygulanmasi-en`, from `main@464a73543a440f7d51a1600599998e97b53e982f` (= `origin/main`, verified by fetch on 2026-10-16).
**State:** `REVIEW_READY`. Nothing is merged, published or deployed. `main`, Vercel, DNS and credentials are untouched.

## 1. Decisions taken in this task (CTO, 2026-10-16)

| Question | Answer | Effect |
| --- | --- | --- |
| Download Natural Earth for the locator map (V1)? | Yes | `ne_50m_admin_0_countries.geojson` v5.1.2 and its `LICENSE.md` were downloaded to the session scratchpad and read as data. The download is not committed. |
| Layer-table thumbnails (V5)? | Not for now | MER-151 authorizes its presentation derivatives for the homepage surfaces only, so G2 ships without thumbnails. The layer names link to the homepage sections that show them, and the request was added to MER-242 (Request 3). |
| Marine scene (D5)? | Keep the Ili Delta | V4 is deferred. The hub's Marine band uses the existing Ili Delta scene with the illustrative footnote. |

## 2. What changed

**Pages** (`docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md` §2, §4):

| Route | Sections |
| --- | --- |
| `/solutions/` (rebuilt) | S0 header · S1 comparison table · S2–S4 full-size bands `#geothermal`, `#mining` (alias `#mineral`), `#marine` (alias `#environment`), each with name, status and caption, plus the Geothermal link · S5 illustrative footnote |
| `/solutions/geothermal/` (new) | G0 header with the locator map · G1 `#glance` facts (alias `#pilot-observe`) · G2 `#layers` layer table, each warning verbatim (aliases `#pilot-terrain`, `#pilot-evidence`, `#pilot-priority`, `#pilot-geothermal`) · G5 `#outputs` · G6 `#gap` empty frame (alias `#pilot-structure`) · G7 "Discuss a pilot →". G3 and G4 are absent until MER-242 (D1); the iron row reads "Accepted, not shown yet". |
| `/about/` (new) | A0 header (`company.title`, `company.copy`, Built by VirgaSoft) · A1 `#principles` (six principles, "See it" links, `proof.foot`) · A2 `#sources` (six sources, including Natural Earth) · A3 Partner link |
| `/partner/` (new) | P0 header · P1 conversation table with three `mailto:` links, each with its translated subject · P2 the address |
| `404.html` | The new navigation, one line and a link home. It now uses `styles.css` and `script.js`, so EN/TR works there too. |

**Retired:** `platform/`, `pilot/`, `company/` and `contact/` are deleted. `vercel.json` answers each with a **301** (`statusCode: 301`; `permanent: true` would answer 308) to `/`, `/solutions/geothermal/`, `/about/` and `/partner/`. `.vercelignore` drops the four entries and adds `!about` and `!partner`. `sitemap.xml` lists the five canonical routes, dated 2026-10-16.

**Navigation:** Home → Solutions (Geothermal `/solutions/geothermal/`, Mining `/solutions/#mining`, Marine `/solutions/#marine`) → About → Partner with us → EN | TR, on every page including the 404 page. The footer lists the same pages. `aria-current="page"` marks the current page; on the Geothermal page it marks the Solutions trigger and the Geothermal item.

**Homepage** (§4.1):
- The hero, Acts 2–4 and the inspection aid are byte-identical apart from four link targets and two link labels. The hero and Act 4 "Partner With Us" calls point to `/partner/` (the homepage carries no `mailto:`). Act 3 reads "See every layer →" and points to `/solutions/geothermal/#layers`. Act 4 reads "See the Kızıldere pilot →" and points to `/solutions/geothermal/`.
- The cards show image, name and status only. Geothermal links to `/solutions/geothermal/`. Mining and Marine read "Expansion direction" (R8) through the shared `app.*.status` keys.
- Method (`#proof`) and Company (`#company`) are removed, and `#contact` is one centred "Partner With Us →" line.
- Footer: the last attribution sentence is "Every source is listed on the About page.", which links to `/about/#sources`.

**Dictionary** (`script.js`):
- 148 keys were removed in both languages: those of the retired pages and sections, and the retired `domain.*.copy` / `domain.*.status`. The five `story.*.note` warnings are kept, because `sources.json` binds them to the WEB-002 proof assets.
- 133 keys were added in both languages.
- Seven values changed, in both languages: `act.evidence.deeper`, `act.priority.deeper`, `footer.attribution` (last sentence dropped), and `solutionsPage.meta.description` / `.meta.ogDescription` / `.title` / `.intro`. No other existing value changed.
- Accepted wording was reused where the authority says *existing*, including every mandatory warning verbatim. I wrote the TR drafts for the new strings and proofread them in the captures; a native-speaker read is still welcome before MER-241 generates `/tr/`.

**Visuals:**
- **V1, the locator map:** `assets/maps/kizildere-locator-23c85f44.svg` (22,523 B). It is generated by `scripts/build_locator_map.py` (stdlib only) from Natural Earth 1:50m Admin 0 v5.1.2, which is public domain (source SHA-256 `3e458fc0…`). It has no text, and neighbouring countries are drawn without borders between them. The file name carries its own checksum. It is recorded in `sources.json` → `web_m6.locator_map` and in `IMAGERY_RIGHTS.md`.
  - Deviation: the authority named the 1:10m layer. 1:50m is used, because at the 1,100 CSS px the figure is drawn at, the 1:10m detail is not visible.
- **Hub bands:** Chuquicamata and the Ili Delta gained 2400 / 2880 px WebP derivatives.
  - They are built by `scripts/build_domain_derivatives.py`, which now keeps every existing derivative byte for byte.
  - Each band is capped at 1440 CSS px, so a 2× display is served the 2880 px master width and nothing is upscaled. The measured maximum drawn width is 1440 CSS px at 19 widths × DPR 1 and 2 (`evidence/mer240/measure_bands.json`).
  - Recorded per scene in `sources.json` → `web_m6_placement`.
- **Social previews:** every route's `og:image` is the hero poster. Deviation from V6, which suggested the Kızıldere priority for the Geothermal page: that file is a MER-151 derivative, authorized for the homepage only.

**Styles** (`styles.css`): new components `.data-table` (tables are show-first elements, not cards; on phones each row becomes a stacked group), `.domain-band`, `.locator-figure`, `.gap-split` / `.gap-frame`, `.mail-address`, `.page-closing` and `.page-note`. The rules only the retired routes and sections used are removed: story-beam, ledger, workflow, editorial figure, contact options, Method grid, Company/trust and the scale strip. The WEB-002 "no filter on product proof" guard is kept.

## 3. Content rules, enforced (`scripts/validate_site.py`)

These checks are new in MER-240:

- **Page set:** the routes, the `404.html` page, the navigation order and labels (EN/TR), the current-page marker, the footer navigation and the footer's sources link.
- **Retired routes:** the redirects (exactly four, each a 301 to a canonical route), the retired directories gone and not deployed, the sitemap listing exactly the canonical routes with dates, and the Geothermal alias anchors.
- **Homepage:** the trim (no `#proof` / `#company`, no `mailto:`, `#contact` one link, both deep links, cards with name and status only).
- **R8:** pinned status labels, and no "In development" / "Geliştirme aşamasında" on any page or in the dictionary.
- **R4:** every section on the reworked pages opens with a marked lead visual (table, image, figure, the gap frame or the address block). Outside sections, `<main>` holds only the closing link and the footnote.
- **R5:** headline 8, intro 30, section body 40, cell 12 words, at most 7 rows, and the page budget (250; Geothermal 350), in EN and in TR (+15 %). R6 fixed texts are exempt.
- **R3:** no software or development terms, and no layer codes, in either language.
- **R1:** a sentence of 6 or more words is stated on one route only.
- **R2:** a visual is shown at full size on one route only. The homepage domain cards are the accepted exception (authority §4.2).
- **V1:** the locator map's record, checksum, byte size and hash name, its one placement and its three-line caption.
- **Partner:** the three translated `mailto:` links, and no `mailto:` on any other route.
- **Hub scenes:** a placed `web_m6_placement`, its pixel bound, and the framing footnote rendered wherever the photographs appear.

Measured on this branch:

| Page | Budgeted words EN / TR | Budget | Longest headline | Longest cell |
| --- | --- | --- | --- | --- |
| `/solutions/` | 71 / 67 | 250 | 7 | 4 |
| `/solutions/geothermal/` | 241 / 226 | 350 | 7 | 9 |
| `/about/` | 225 / 219 | 250 | 4 | 12 |
| `/partner/` | 74 / 64 | 250 | 7 | 11 |
| `404.html` | 12 / 8 | 250 | 8 | — |

## 4. Verification (this branch, 2026-10-16)

| Check | Result |
| --- | --- |
| `py -3.14 scripts/validate_site.py` | PASS, 0 warnings (4 scenes, 5 routes + 404, 277 i18n keys, deploy set 12 root entries / 114 files) |
| `scripts/negative_tests_mer240.py` (new) | 46/46 caught (45, plus one added in the review revision, §7); restored tree identical |
| `negative_tests_web005.py` / `_web005b.py` / `_web005c.py` / `_mer216.py` / `_mer237.py` | 72/72, 55/55, 18/18, 19/19, 29/29; restored trees identical |
| `py -3.14 hero/scripts/validate_hero.py` | 420 / 0 (hero workstation). `hero/config/lane.json` names MER-240 and adds `404.html`, `sitemap.xml` and the four new derivatives to the integration write surface. |
| `node --check script.js` | OK |
| Acceptance sweep (`evidence/mer240/tools/sweep_mer240.py`) | 6 pages × 10 widths (375–3840 CSS px) × DPR 1 / 2 / 3 = 180 loads: 0 horizontal overflow, 0 broken images. Homepage CLS 0 at 1440 and 390 (`sweep_report.json`). |
| Visual QA (`evidence/mer240/tools/capture_mer240.py`) | 6 pages × desktop 1440 / phone 390 × EN / TR. No horizontal overflow, broken image or console error anywhere. `lang` switches, the current-page marker is right on every page, and a JavaScript-disabled pass renders each page's English `h1` with native links. Captures are in `evidence/mer240/*.webp`, findings in `capture_report.json`. Strings reported as "same in both languages" are names, numbers and the required English Copernicus attribution. |

## 5. Earlier suites, retargeted

The retired routes no longer exist, so these cases now mutate their successors. Every case keeps what it proves:

- **`negative_tests_web005b.py`:** the "WEB-005B asset leaks beyond the homepage" case now leaks onto `/solutions/geothermal/` instead of `/pilot/`.
- **`negative_tests_web005c.py`:**
  - the alias and anchor cases find the hub's bands instead of the ledger rows;
  - the nav-order and body-copy cases mutate `/about/` instead of `/platform/` and `/company/`;
  - the TR ogDescription case uses the new value;
  - the Geothermal card case uses the new link target.
- **`negative_tests_mer237.py`:**
  - the "dropped route" case now drops `!about`, and the "names nothing" case adds `!press`;
  - the relative-path case runs on `/solutions/geothermal/`;
  - the og:image and stray-tool cases run on `/about/` and `/partner/`.

## 6. Not verified, and gates

- **Scope 8 (retired assets):** no file qualified for removal. The issue allows removing an asset only where `sources.json` marks it retired and nothing references it. Crater Lake is marked retired, but its scene record and the validator's four-locked-scenes check still reference it. The WEB-002 proof derivatives under `assets/proof/` lost their last page with `/pilot/`, but they are a governed package record, not marked retired, and the validator re-checks their checksums. Both stay deployed and placed on no page; removing them is a separate decision.
- **Redirects, local check:** the local static server does not apply `vercel.json`, so the 301s were checked statically (exactly four, each a 301 to a canonical route, the sources gone and not deployed) and the fragments by the alias-id check (a static check that an id exists proved not to be enough: §7, B1).

- **D4, the ship gate:** that `contact@orbgss.com` receives external mail is not evidenced. The CTO confirms it before publication.
- **Redirects live:** the four 301s are validated statically, and Vercel documents `statusCode: 301`. Their live behaviour, including whether a slash-less `/pilot` answers 308 → `/pilot/` before the 301, is first observable on the protected branch Preview or after publication. `evidence/mer219/smoke_production.py` now checks both forms and the new routes; run it after publication.
- **Not exercised:** physical browsers, phones and 4K panels, as in earlier tasks.
- **Accessibility of tables on phones:** they become stacked blocks (`display:block`), which may drop the table semantics in some engines. The column headers stay in the markup.
- **Waiting:** G3 / G4 and the G2 thumbnails (MER-242), the coastal Marine scene (D5), `/tr/` (MER-241), and D3 (privacy / KVKK, legal).
- **Publication** is a CTO-authorized non-force fast-forward of `main` to the reviewed head. Given the COUPLED topology, that push is the production deployment. Rollback target after publication: the current production deployment `orbgss-website-29bzudvea` (`464a7354`).

## 7. Review revision (independent review of `2bbb384a`: `REVISION_REQUIRED`, three blockers)

The review reported three defects, all inside MER-240's scope. Nothing else changed: no optional polish, no new page, no new asset.

- **B1: old `/pilot/#pilot-*` links landed at the top of the page.**
  - Cause: `.anchor-alias` is `position:absolute`, and `.page-section` was static, so the alias resolved against the page (`scrollY` stayed 0 for all six aliases at 1440 and 390 px).
  - Fix: `.page-section{position:relative}` (`styles.css`). The hub's `.domain-band` already was positioned.
  - Guard: `validate_site.py` now requires every `.anchor-alias` on every page to sit in a container that an unconditional `styles.css` rule positions (a rule inside an `@media` block does not count). `negative_tests_mer240.py` has one new case for it, so the suite is 46 cases. A static check cannot scroll, so the browser run below is the real evidence.
  - Real-browser run (Chromium 1440 and 390, `vercel.json` emulated, 301 chain followed): on `2bbb384a` all six aliases ended at `scrollY 0`. On the fix each one lands on its section: `#pilot-observe` on `#glance`, `#pilot-terrain`, `#pilot-evidence`, `#pilot-priority` and `#pilot-geothermal` on `#layers`, `#pilot-structure` on `#gap`. The page's own `#glance` / `#layers` / `#gap`, the hub's `#mineral` / `#environment` and `/#contact` still land as before.
  - Side effect check: full-page screenshots of `/about/`, `/partner/`, `/solutions/`, `/solutions/geothermal/` and `404.html`, at 1440 and 390 (DPR 2), before and after. Every pair is pixel-identical except `/about/`, whose only differences are the B2 label and, on the phone, a sub-pixel text snap (section offsets are equal to 1/64 px; `position:relative` makes Chromium snap the paint origin to whole device pixels).
  - A link now lands with the section's top edge about 100 px under the header, the same distance the hub's aliases already had; that spacing is the known double offset (`html{scroll-padding-top}` plus `scroll-margin-top`) and is left for a separate decision.
- **B2: the About sources row named the wrong mission.**
  - The row said "Landsat 8 (USGS)", but its uses (natural colour, thermal evidence, domain photographs) span more than Landsat 8: the Chuquicamata photograph is Landsat 9 OLI-2 (`IMAGERY_RIGHTS.md`, `sources.json`), and the thermal evidence records only "Landsat thermal" with no mission.
  - It now reads "Landsat (USGS)" in both languages (`about/index.html`, `script.js` `aboutPage.source.landsat`, EN and TR). This is a deliberate, documented deviation from the wording in `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md` §A2, which still says "Landsat 8 (USGS)": that section says each row's wording follows `IMAGERY_RIGHTS.md`, and a mission number is only honest per image. Specific missions stay where they are recorded: Landsat 8 on the Kızıldere pages, Landsat 9 in the manifest.
- **B3: `negative_tests_mer240.py` only ran on CRLF checkouts.**
  - The cases searched for hard-coded `\r\n`, so a clean Linux checkout stopped at the fifth case.
  - The runner now mutates the LF form of each file and writes the file's own line ending back; the five literals are LF.
  - Observed: 46/46 on this Linux (LF) checkout, and 46/46 on a copy of the tree with 172 text files converted to CRLF (the locator SVG, which is `-text`, left alone). The five earlier suites are untouched and pass as before (72/72, 55/55, 18/18, 19/19, 29/29).

Still not verified here, unchanged by this revision: a real Vercel Preview (the redirects were followed on an emulation of `vercel.json`, not on Vercel), the D4 mailbox gate, and physical devices.
