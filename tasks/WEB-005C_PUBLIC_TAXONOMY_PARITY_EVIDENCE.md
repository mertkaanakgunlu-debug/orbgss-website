# WEB-005C / MER-149 — Public Domain Taxonomy Parity — Implementation Evidence

**State:** `REVIEW_READY` / `WAITING_PRODUCT_REVIEW`
**Branch:** `feat/web-005c-public-domain-taxonomy-parity`
**Exact accepted baseline:** `feat/web-005b-homepage-visual-fidelity@0af5b1ad0a5645f8ff3f39f818625944a096635d`
**Authority:**
`docs/web-005-polish-authority@0bd8522777b077e0adb643679b7dde37248596fd:tasks/WEB-005C_R1_START_AUTHORITY_EXACT_BASELINE.md`
and the parent
`docs/web-005-polish-authority@ce5f19878d287fdcd46aadeb5ef562924509aa21:tasks/WEB-005C_PUBLIC_DOMAIN_TAXONOMY_PARITY.md`
**Evidence:** `evidence/web005c/`

---

## 0. What this task fixed

WEB-005B R13 made the homepage taxonomy **Geothermal / Mining / Marine** but left `/solutions/` and
every navigation dropdown publishing the older application-ledger vocabulary — *Geothermal
Exploration*, *Mineral Exploration*, *Environmental & Land Intelligence* — under the anchors
`#geothermal` / `#mineral` / `#environment`. R13 recorded that divergence as visitor-visible and
asked for a follow-up. This is that follow-up.

The public site now publishes one taxonomy everywhere. Nothing else moved: no homepage redesign,
no hero change, no analytical imagery, no motion, no scientific semantics, no new claim.

## 1. Taxonomy, as published now

| Anchor | EN | TR | Status shown on `/solutions/` | Status shown on the homepage |
|---|---|---|---|---|
| `#geothermal` | Geothermal | Jeotermal | Active · First application | Active · First application |
| `#mining` | Mining | Madencilik | Expansion direction | In development |
| `#marine` | Marine | Denizel | Expansion direction | In development |

The two status vocabularies are both truthful and both pre-existing accepted copy — the homepage
cards say *In development*, the `/solutions/` ledger says *Expansion direction*. This task renamed
domains; it did not rewrite maturity wording. If Product wants those aligned too, that is a
one-line follow-up, not a WEB-005C decision.

## 2. Route / anchor compatibility

The superseded anchors are **not** removed. Each renamed `/solutions/` row carries its old anchor as
an alias:

```html
<li class="ledger-row" id="mining">
  <span class="anchor-alias" id="mineral" aria-hidden="true"></span>
```

`.anchor-alias` is `position:absolute` at the row origin with zero size, so it is not a grid item and
contributes nothing to layout, and it carries the same `scroll-margin-top` as the row. Measured at
1440 × 900:

| Deep link | Lands at | Canonical link | Lands at | Identical | Row shown |
|---|---|---|---|---|---|
| `/solutions/#mineral` | scrollY 866 px | `/solutions/#mining` | scrollY 866 px | yes | Mining |
| `/solutions/#environment` | scrollY 1013 px | `/solutions/#marine` | scrollY 1013 px | yes | Marine |

`evidence/web005c/legacy_anchor_compatibility.txt`,
`legacy_anchor_mineral_1440.webp`, `legacy_anchor_environment_1440.webp`.

Proof the alias costs nothing: with the alias spans present and with them removed from the live DOM,
every `.ledger-row` box — row top, row height, `h3` top, status top, copy-group top, index top — is
pixel-identical on all three rows. No redirect, no JavaScript, no server rule: an old link works with
scripting disabled.

Nothing else in the repository referenced `#mineral` or `#environment`; `sitemap.xml` and `404.html`
carry no fragments, so no other surface needed a compatibility shim.

## 3. Changed paths

| Path | Change |
|---|---|
| `index.html` | Solutions submenu only (3 links). The four acts, the domain module, the hero and every other section are untouched. |
| `platform/index.html`, `pilot/index.html`, `contact/index.html` | Solutions submenu only. |
| `company/index.html` | Solutions submenu + the "Where OrbGSS is headed" expansion sentence. |
| `solutions/index.html` | Submenu; rows 02/03 renamed with legacy anchor aliases; row 01 heading; intro; `description` and `og:description`. |
| `script.js` | EN/TR dictionary: taxonomy keys renamed and revalued (section 4). |
| `styles.css` | `position:relative` on `.ledger-row` + the new `.anchor-alias` rule. Two lines; no token, colour, spacing or type change. |
| `scripts/validate_site.py` | New WEB-005C taxonomy parity checks (section 5); the stale R13 comment corrected. |
| `scripts/negative_tests_web005c.py` | **New.** 13 deliberate regressions proving those checks bite. |
| `hero/config/lane.json` | Integration bookkeeping only: branch, lane, phase, owning task and authority now name WEB-005C. No hero file, asset or write-surface entry changed. |
| `tasks/WEB-005C_PUBLIC_TAXONOMY_PARITY_EVIDENCE.md`, `evidence/web005c/` | **New.** This document and its evidence. |

No asset, no manifest entry, no raster, no video, no hero file.

## 4. EN / TR changes

Keys renamed so one vocabulary is published: `nav.mineral` → `nav.mining`, `nav.environment` →
`nav.marine`, `app.mineral.*` → `app.mining.*`, `app.environment.*` → `app.marine.*`,
`solutionsPage.mineral.*` → `solutionsPage.mining.*`, `solutionsPage.environment.*` →
`solutionsPage.marine.*`. Revalued in both languages: `nav.geothermal`, `app.geothermal.title`,
`solutionsPage.intro`, `solutionsPage.meta.description`, `solutionsPage.meta.ogDescription`,
`companyPage.expansion`.

Wording discipline:

- The Mining row keeps its existing body, with only the subject noun changed: *"Mining follows the
  same underlying pattern … applied to the evidence families relevant to mineral targeting."* The
  activity is still described as mineral targeting, matching the accepted homepage Mining card
  (*"…extended to mineral exploration targets."*). The **domain name** changed; the capability
  description did not.
- The Marine row is the one genuine subject change, and it is not new: it adopts the accepted
  homepage Marine claim (*"Coastal and marine ground read as spatial evidence on the same
  footing."*) at the same unchanged *Expansion direction* status. No capability, customer, metric or
  timeline was invented.
- Mandatory scientific warnings were not touched. The strings containing *"not mineral
  identification"* / *"mineral tanımlaması değildir"* are byte-identical to the baseline — the
  taxonomy check matches the capitalised domain labels case-sensitively precisely so it can never
  drag a scientific warning with it.

EN/TR parity is machine-enforced: the validator already fails when any referenced key is missing from
either dictionary (268 keys site-wide), and WEB-005C additionally pins the three domain names in both
languages.

Copy preservation against the baseline (`evidence/web005c/copy_preservation_vs_0af5b1a.txt`): 68
differences, all taxonomy. The homepage's entire visible-copy delta is the three submenu labels —
`Geothermal Exploration → Geothermal`, `Mineral Exploration → Mining`, `Environmental & Land
Intelligence → Marine`. No other homepage string changed.

## 5. What is now enforced

`scripts/validate_site.py` gained `PUBLIC_TAXONOMY`, `LEGACY_DOMAIN_ANCHORS` and
`RETIRED_DOMAIN_LABELS`, and four checks:

1. every route's Solutions submenu publishes exactly `/solutions/#geothermal` → `/solutions/#mining`
   → `/solutions/#marine`, in that order, with the matching `nav.*` key and EN label;
2. those keys resolve to the canonical name in **both** languages;
3. `/solutions/` carries a row for each domain **and** keeps `#mineral` / `#environment` resolvable;
4. no route's HTML and neither dictionary carries a superseded domain label, EN or TR.

`scripts/negative_tests_web005c.py` breaks each of these 13 ways and confirms the validator fails
every time, then proves the restored tree validates identically to the baseline.

## 6. Gates

| Gate | Result |
|---|---|
| `scripts/validate_site.py` | **PASS** — 6 routes, 268 i18n keys, 0 warnings |
| `hero/scripts/validate_hero.py` | **PASS** — 420 checks, 0 failed |
| `scripts/negative_tests_web005.py` | **72/72** caught; restored tree identical |
| `scripts/negative_tests_web005b.py` | **55/55** caught; restored tree identical |
| `scripts/negative_tests_web005c.py` | **13/13** caught; restored tree identical |
| Browser, 1440 × 900 | 0 console errors; EN/TR switch clean on `/solutions/` incl. the translated meta description |

Full output: `evidence/web005c/validators.txt`.

## 7. Known remaining public naming notes

1. **Status vocabulary differs by surface** — homepage *In development* vs `/solutions/*Expansion
   direction*. Both truthful, both pre-existing accepted copy, deliberately left alone (section 1).
2. **Homepage domain cards still do not navigate.** R13 gave them no link because Mining and Marine
   had no destination. `/solutions/#mining` and `/solutions/#marine` are now real, named rows, so
   linking them has become possible — but adding links is a homepage design change and is out of
   scope here. Flagged for Product, not taken.
3. **"mineral exploration" survives as an activity phrase**, lowercase, in the Mining copy on the
   homepage and on `/solutions/`. That is the accepted description of what the domain does, not a
   top-level label, and the homepage sentence is untouched accepted copy.
4. **`CLAUDE.md` still records the superseded nav order** ("Solutions (dropdown: Geothermal
   Exploration, Mineral Exploration, Environmental & Land Intelligence)") as a design invariant. It
   is now contradicted by accepted Product taxonomy. Left unedited so Product amends its own
   invariant rather than having it rewritten inside an implementation commit.

## 8. Boundaries honoured

No homepage redesign. No change to WEB-005B layout, hero, analytical imagery or motion — the hero
markup and every Act 2/3/4 asset are byte-identical to the baseline. No solution-page redesign beyond
the taxonomy rename. No new capability, claim, metric or customer. No scientific semantics touched.
Not merged, not deployed, no DNS, no WEB-006 work.
