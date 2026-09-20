# WEB-005C / MER-149 — Public Domain Taxonomy Parity — Implementation Evidence

**State:** `REVIEW_READY` / `WAITING_PRODUCT_REVIEW` — **R2**, the bounded Product revision
**Branch:** `feat/web-005c-public-domain-taxonomy-parity`
**Exact accepted baseline:** `feat/web-005b-homepage-visual-fidelity@0af5b1ad0a5645f8ff3f39f818625944a096635d`
**R1 implementation (reviewed):** `289c8aef0c8237d1c4a123c1d2129c6142bd85ff`
**Authority:**
`docs/web-005-polish-authority@de173cab730fc64bcda26354d153de184b4e87fb:tasks/WEB-005C_R2_PRODUCT_REVIEW_CARD_ROUTING_AGENT_INVARIANT.md`,
over
`docs/web-005-polish-authority@0bd8522777b077e0adb643679b7dde37248596fd:tasks/WEB-005C_R1_START_AUTHORITY_EXACT_BASELINE.md`
and the parent
`docs/web-005-polish-authority@ce5f19878d287fdcd46aadeb5ef562924509aa21:tasks/WEB-005C_PUBLIC_DOMAIN_TAXONOMY_PARITY.md`
**Evidence:** `evidence/web005c/`

---

## R2 — the two Product corrections

Product accepted the R1 taxonomy implementation and required two bounded corrections. Both are
implemented. Section 0-8 below describe R1 and are unchanged except where R2 supersedes them; the
R2 detail is section 9.

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
2. ~~**Homepage domain cards still do not navigate.**~~ **Resolved in R2** — all three cards are
   native links to their own `/solutions/` rows. See section 9.
3. **"mineral exploration" survives as an activity phrase**, lowercase, in the Mining copy on the
   homepage and on `/solutions/`. That is the accepted description of what the domain does, not a
   top-level label, and the homepage sentence is untouched accepted copy.
4. ~~**`CLAUDE.md` still records the superseded nav order**~~ **Resolved in R2** — Product
   instructed the correction directly. See section 9.

## 8. Boundaries honoured

No homepage redesign. No change to WEB-005B layout, hero, analytical imagery or motion — the hero
markup and every Act 2/3/4 asset are byte-identical to the baseline. No solution-page redesign beyond
the taxonomy rename. No new capability, claim, metric or customer. No scientific semantics touched.
Not merged, not deployed, no DNS, no WEB-006 work.

---

## 9. R2 — Product revision (card routing + agent invariant)

**Authority:** `docs/web-005-polish-authority@de173cab:tasks/WEB-005C_R2_PRODUCT_REVIEW_CARD_ROUTING_AGENT_INVARIANT.md`
**Applied over:** `289c8aef0c8237d1c4a123c1d2129c6142bd85ff` (the reviewed R1 implementation)

### 9.1 Correction A — the homepage Solutions cards navigate

Each accepted card is now a native link to its own `/solutions/` row:

```html
<li class="domain-card is-lead" id="geothermal" …>
  <img … />
  <span class="domain-shade" aria-hidden="true"></span>
  <a class="domain-link" href="/solutions/#geothermal" aria-labelledby="domain-geothermal-title">
  <div class="domain-copy">
    <h3 id="domain-geothermal-title" data-i18n="domain.geothermal.title">Geothermal</h3>
```

The anchor wraps the copy block and **stays static on purpose**: that is what lets its `::after`
resolve against `.domain-card` rather than `.domain-copy`, so one transparent overlay makes the
whole card the click target while `.domain-copy` keeps its accepted `position`/`z-index` untouched.

| Requirement | How it is met |
|---|---|
| preserve the accepted visual design exactly | §9.3 — 0 box and 0 computed-style differences across the whole page at four viewports; 0 geometry differences across 23 widths |
| semantically valid | one `<a href>` per card wrapping real content; no `role`, no `tabindex`, no click handler |
| works with JavaScript disabled | §9.2 — proved with `Emulation.setScriptExecutionDisabled` |
| keyboard accessible | §9.2 — three tab stops in visual order, Enter activates |
| visible focus state consistent with the design | `2px solid var(--accent)` = `rgb(67, 191, 240)`, the page's own focus token; inset `-2px` because `.domain-card` clips its overflow, matching the evidence tabs (`-2px`) and submenu (`-3px`) |
| no CTA / arrow / copy / hover theatrics | nothing added but the anchor; the only hover behaviour is the image fade the card already had |
| no imagery, spacing, status or hierarchy change | §9.3 |

The accessible name is the **card title alone** (`aria-labelledby` → the card's own `<h3>`), not the
whole card read aloud. It needs no translation of its own, so EN/TR parity is automatic.

### 9.2 Behaviour proofs — `evidence/web005c/r2_behaviour_proofs.txt`

**No JavaScript.** `Emulation.setScriptExecutionDisabled(true)`; each card clicked **on its
photograph**, above the copy block, to prove the whole card is the target:

| Card | Clicked at | Result | Lands on |
|---|---|---|---|
| Geothermal | y 263 (card top 200, copy starts 326) | `/` → `/solutions/#geothermal` | row *Geothermal*, scrollY 614 |
| Mining | y 246 (card top 200, copy starts 292) | `/` → `/solutions/#mining` | row *Mining*, scrollY 866 |
| Marine | y 246 (card top 200, copy starts 292) | `/` → `/solutions/#marine` | row *Marine*, scrollY 1013 |

**Keyboard.** Three tab stops, in visual order, each a real `<a>` with `tabIndex=0`:
`/solutions/#geothermal` → `/solutions/#mining` → `/solutions/#marine`, accessible names
`'Geothermal'`, `'Mining'`, `'Marine'`. Enter on the focused Mining card navigates to
`/solutions/#mining`.

**Focus** (`r2_focus_state.txt`, `card_focus_{geothermal,mining,marine}_1440.webp`): with
`:focus-visible` armed by a real Tab keypress, all three report
`outline: rgb(67, 191, 240) solid 2px`, `outline-offset: -2px`.

**EN / TR.** Both languages, all three cards: `href` canonical, accessible name and status localised
— `Geothermal/Jeotermal`, `Mining/Madencilik`, `Marine/Denizel`;
`In development` / `Geliştirme aşamasında`.

**Legacy anchors, both languages** — still identical landings:

| | EN | TR |
|---|---|---|
| `#mineral` vs `#mining` | 866 = 866 → *Mining* | 837 = 837 → *Madencilik* |
| `#environment` vs `#marine` | 1013 = 1013 → *Marine* | 983 = 983 → *Denizel* |

### 9.3 No unrelated visible homepage change

**Whole-page layout parity** — `r2_homepage_layout_parity.txt`. A full-page *pixel* diff is not a
valid instrument here: two captures of the **same** tree differ by ~1 % of pixels at up to 8/255,
because lazy image decode order shifts gradient dithering. So parity is proved deterministically
instead, by snapshotting every element's layout box plus the computed styles that carry the design
(font, colour, background, border, padding, margin, opacity, transform, display, position, z-index,
text-decoration, letter-spacing, line-height, text-transform, object-fit/position,
grid-template-columns, gap):

| Viewport | Elements compared | Document height | Boxes differing | Computed styles differing |
|---|---|---|---|---|
| 1440 × 900 | 322 | 8621 px → 8621 px | **0** | **0** |
| 1440 × 900 TR | 322 | 8569 px → 8569 px | **0** | **0** |
| 1024 × 800 | 322 | 7813 px → 7813 px | **0** | **0** |
| 390 × 844 | 322 | 9455 px → 9455 px | **0** | **0** |

The only new nodes on the page are the three card links themselves.

**Geometry sweep** — `r2_geometry_sweep.txt`. Card, `<img>`, `.domain-shade`, `.domain-copy`, `<h3>`
and `.domain-status` boxes at **23 widths from 320 to 2560 px**: identical at every width. The link
is an in-flow block, so it keeps contributing the copy block's height to the card exactly as the
copy block did alone — the cards cannot collapse at any width.

**Copy** — `r2_copy_preservation_vs_289c8ae.txt`: **0 visible-copy differences** against the R1
commit. R2 changed no string in either language.

**Pixels, disclosed precisely** — `r2_visual_delta.txt`. The Solutions-section capture *is*
deterministic (0 differing px between two runs of the same tree), so it is the instrument used. It
reports one delta: a **≤ 7/255 single-channel dither shift** in the `.domain-shade` gradient over the
cards, with **zero pixels at or above 16/255** anywhere. Cause identified by isolation — with the
`<a>` present but the `::after` overlay rule removed, the same comparison is **0 differing pixels at
every viewport**. The overlay is a positioned descendant, so Chrome rasterises the card's gradient
into a different backing store and its ordered dither lands one step differently.

This is not a design change: no geometry, type, colour token, spacing, imagery, status or hierarchy
value moves, as §9.3 proves twice over. The zero-pixel alternative is to drop the overlay and let
only the copy block navigate — not taken, because R2 §2 asks for the **card** to be the navigation
surface, and a sub-perceptual dither in a dark gradient is not worth trading that for. Flagged here
so Product decides rather than discovers.

### 9.4 Correction B — `CLAUDE.md` taxonomy invariant

Three bullets carried the superseded taxonomy. Only those changed:

- the navigation invariant now reads *Solutions (dropdown: Geothermal, Mining, Marine)*, preceded by
  a new bullet stating the taxonomy outright, that the superseded labels must not return to visible
  copy, and that `#mineral` / `#environment` survive as compatibility aliases that must keep
  resolving;
- a new bullet records that the three homepage cards are native links to their `/solutions/` rows,
  navigate without JavaScript, and carry no CTA, arrow or added copy;
- under *Content / claim discipline*: "Mineral and environmental/land intelligence may be presented
  as solution directions" → "Mining and marine…", and "Geothermal Exploration is the first active
  application; Mineral Exploration and Environmental & Land Intelligence are expansion directions" →
  "Geothermal is the first active application; Mining and Marine are expansion directions".

No other CLAUDE.md instruction was touched.

### 9.5 R2 changed paths

| Path | Change |
|---|---|
| `index.html` | Three `<a class="domain-link">` wrappers + an `id` on each card `<h3>`; the authoring note above the module corrected (it still explained why the cards did *not* navigate). No copy, image, status or class change. |
| `styles.css` | `.domain-link`, its `::after` stretch overlay and the focus rule. Nothing existing modified. |
| `CLAUDE.md` | §9.4. |
| `scripts/validate_site.py` | Card-link contract checks (§9.6). |
| `scripts/negative_tests_web005c.py` | 13 → **18** cases. |
| `tasks/WEB-005C_PUBLIC_TAXONOMY_PARITY_EVIDENCE.md`, `evidence/web005c/r2_*`, `card_focus_*`, `solutions_cards_*` | This section and its evidence. |

`script.js` is untouched, so the R1 `.domain-card > img` selector still matches — the image
graceful-failure handler is unaffected.

### 9.6 What R2 adds to the validator

`validate_site.py` now fails if, for any of the three domains: the card is not a native
`<a class="domain-link" href aria-labelledby>`; its `href` is not its own `/solutions/` anchor; the
`aria-labelledby` does not point at that card's own `<h3>` id; or `styles.css` declares no
`.domain-link:focus-visible` rule that actually draws an outline. `negative_tests_web005c.py` breaks
each of those five ways — **18/18 caught**, restored tree identical.

### 9.7 R2 gates

| Gate | Result |
|---|---|
| `scripts/validate_site.py` | **PASS** — 6 routes, 268 i18n keys, 0 warnings |
| `hero/scripts/validate_hero.py` | **PASS** — 420 checks, 0 failed |
| `scripts/negative_tests_web005.py` | **72/72**, restored tree identical (site + hero) |
| `scripts/negative_tests_web005b.py` | **55/55**, restored tree identical |
| `scripts/negative_tests_web005c.py` | **18/18**, restored tree identical |
| `scripts/check_copy_preservation.py` vs R1 | **0 visible-copy differences** |

Full output: `evidence/web005c/r2_validators.txt`.

### 9.8 Boundaries honoured in R2

No homepage or Solutions redesign. No copy change in either language. No scientific semantics. No
hero or media change — `script.js`, `hero/`, every asset and every manifest entry are untouched by
R2. Legacy `#mineral` / `#environment` aliases preserved and re-proved. *In development* vs
*Expansion direction* left alone; lowercase "mineral exploration" activity wording left alone. Not
merged, nothing deployed, no Vercel, no DNS, no WEB-006 work.
