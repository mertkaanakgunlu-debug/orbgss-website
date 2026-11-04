# Interior cleanup — authority (CTO decisions of 2026-11-04)

Status: implemented on a review branch, previewed, **not published**. Publishing is a separate CTO gate (`main` is production).
Source: the Claude Design prototype, revisions 1 to 3 (the zip `OrbGSS prototype testingv3`, its `REVISION-1.md`, `REVISION-2.md`
and `copy-new.md`), reviewed by the CTO, plus three decision cards answered on 2026-11-04.

Why: the interior pages read as unfinished and defensive: design-stage numerals, repeated notes, the same fact stated twice, a
"what is missing" section, captions on every image. The CTO asked for a cleaner, calmer, less repetitive site with motion and a
little more weight in the type. Nothing about the science, the claims or the homepage's four acts changed.

## Decisions (D1–D7, R1–R5)

| Id | Decision | Where it lives now |
|---|---|---|
| D1 | No design-stage numbering on any page (section kickers, plate numbers, Sources chapter numerals). About keeps its six principle numerals. | `script.js` dictionary, the six pages |
| D2 | One result figure on the Geothermal page: the priority over shaded relief (MER-242). The plain priority map is not drawn there. | `solutions/geothermal/` |
| D3 | No "What is missing" section and no structure-and-geology gap statement anywhere. Five-plate atlas. `#gap` and `#pilot-structure` stay as invisible anchors (they must sit in a positioned container: `.geo-head`). | Geothermal page, validator |
| D4 / R1 | No text on the five atlas plates: the plate name and "role · source" sit under the image. The opening stage, the locator and the result figure (public score label, 0–100 legend, 10 km bar) keep their captions. Scenes of other places keep their own place and coordinates. | `web_m6.interior_crops[kizildere-aoi].caption_on_image = false` |
| D5 | Every "Illustrative … another place" note is removed (About, Partner, Solutions, homepage cards). The hero's "Rendered orbital sequence — not sensor imagery" line stays. | `RETIRED_CLEANUP_KEYS` in the validator |
| D6 | Homepage: the second "See the pilot / Partner with us" pair under the Act 4 map is removed. The hero pair stays. | `index.html` |
| D7 | "Partner with us" text links are dropped from page closings; the header pill carries it. | all pages |
| R2 | Homepage evidence tabs lose the 01 / 02 / 03 numerals. | `index.html` |
| R3 | `/solutions/` has one link to the pilot (the filled button in the Geothermal band); it ends on the Mining and Marine pair. | `solutions/index.html` |
| R4 | The header pill reads "Partner" at **387 px** and below ("İş Birliği" in Turkish, `nav.partnerShort`), "Partner with us" from 388 px, the navigation pill from 981 px. Logo never under 120 px. The prototype's 374 px threshold was measured with 11 px labels; at the 12 px label size "Partner with us" touched the logo at 375 px, so the threshold moved to 387 px (10.8 px gap at 388 px). Below 340 px the short label gives up 4 px of padding and some tracking so the Turkish pill keeps 14 px beside the logo at 320 px. Measured: pill 44 px tall, one line, no horizontal scroll at 320 to 980 px in both languages. | header, `styles.css`, validator |
| R5 | About principle 03 ("Explicit data gaps") is unchanged by decision. | `about/` |

Three decisions made on cards, same day: the Turkish short label is **"İş Birliği"**; the priority map is drawn at full size on the
homepage **and** on `/solutions/` as **one named R2 exception** (that asset, those two pages, 600 CSS px at most); labels are **12 px**
in the header, footer and interior pages (the homepage's four acts keep 11 px, so the hero boxes stay identical to production).

## Rules this reverses (older authorities lose on exactly these points)

- CLAUDE.md, "Each image carries its location and coordinates": no longer true of the five atlas plates (D4). It still holds for the
  opening stage, the locator, the homepage acts and the scenes of other places.
- CLAUDE.md and the M6 / Atlas Geothermal authorities, "structure/geology is published once, in What is missing": the gap is **no longer
  published anywhere**. It is still a gap and the score is still score-invariant; the site simply does not talk about it. Do not fill it
  with a picture or a statement.
- MER-255 / M6 R6: the illustrative-imagery footnote and `scene.illustrative` / `domains.illustrative` are retired (D5). Provenance
  stays in `sources.json`, `IMAGERY_RIGHTS.md` and `/sources/`.
- R2 (one full-size appearance): the priority map is drawn full size on the homepage and `/solutions/`. Nowhere else; the Geothermal
  page borrows only its legend ramp. Recorded in `web_005b.placement.priority.solutions_placement`, measured by
  `scripts/measure_geothermal_renders.py`.
- R4 (the lead visual opens the section): the Geothermal band on `/solutions/` sets its copy beside its map (map second in the DOM, so
  on a phone the copy comes first, as reviewed).
- Atlas design, "two weights": there is a third face, **OrbGSS Sans 500** (IBM Plex Sans Medium subset, self-hosted, rebuilt by
  `scripts/build_fonts.py`). It is used for the interior headlines and the About numerals only, inside the `atlas:interior` region.
- Atlas design, type floor: labels are 12 px in header, footer and interior pages (11 px stays on the homepage acts).

## What was added

- `styles.css`: the last region `atlas:interior` (the prototype layer: entrance motion, interaction, type, composition). It is a known
  debt to fold its rules into the page regions later; it exists so the reviewed look is preserved exactly.
- Entrance motion: `html.page-motion` is set before first paint by a tiny inline head script on the five interior pages; the hidden
  starting state is static CSS; `script.js` (`interiorEntrance`) plays it once per element with an IntersectionObserver. Reduced motion,
  printing, a hidden tab and no JavaScript all show everything. The RISE and LINES selector lists exist in CSS and JS: change both.
- The TR switch, `nav.partnerShort` and the Sources contents label (`sourcesPage.toc`) have Turkish strings; the new Turkish wording is
  pending the CTO's language review like the other new Turkish blocks.

## Open

- The `atlas:interior` region should be folded into the page regions (debt, no visual effect).
- Retired copy and rules are enforced by `RETIRED_CLEANUP_KEYS` and the negative suites; a reinstatement needs the CTO.
