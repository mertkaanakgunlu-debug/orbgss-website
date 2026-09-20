# WEB-005B R11 — accepted final design implementation evidence

**Linear:** MER-109
**State:** `REVIEW_READY / WAITING_CTO_VISUAL_REVIEW`
**Branch:** `feat/web-005b-homepage-visual-fidelity`
**Starting HEAD (verified before any edit):** `176e345166bcc084219aa5972c3209c872889626`
**Product authority:** `docs/web-005-polish-authority@1334e757:tasks/WEB-005B_R11_CLAUDE_DESKTOP_IMPLEMENTATION_HANDOFF.md`
**Continuity authority:** `docs/web-005-polish-authority@4051c28f:tasks/WEB-005B_R10_FINAL_DESIGN_CONTINUITY_IMPLEMENTATION.md`
**Design input:** `OrbGSS Homepage - Final Direction.html` + `Final Direction - States and Mobile.html`,
from the Claude Design handoff bundle the CTO shared into the session
(`Cinematic inspection module revision`, project `c46c985e-4acd-49e0-9354-704f276beca7`,
synced from this repository on 2026-09-20T02:25:53Z)
**Immutable hero upstream:** `feat/web-005a-hero-visual-fidelity@1135e7a7e0b0f6db6348dee139d505550d8ca8b9`
**Evidence artifacts:** `evidence/web005b_r11/`
**R13 bounded revision authority:** `docs/web-005-polish-authority@ba8d99b8:tasks/WEB-005B_R13_IMPLEMENTATION_REVIEW_DOMAIN_REVISION.md`
**R11 implementation HEAD (reviewed):** `4e6c7c106399140565c77da0febe59ffc14f3ab3`

## 0. R13 revision — the accepted domain taxonomy

Product reviewed the R11 implementation, accepted it for final visual review, and issued one
mandatory correction: the homepage domain taxonomy is **Geothermal / Mining / Marine**, and the
implementation's substitution of *Mineral Exploration* and *Environmental & Land Intelligence* is
not accepted. An existing route anchor is not authority to rename a published domain.

That correction is implemented. The three cards now read:

| Card | Label | Status | Anchor | Navigates |
| --- | --- | --- | --- | --- |
| lead | Geothermal | Active · First application | `#geothermal` | no |
| secondary | Mining | In development | `#mining` | no |
| secondary | Marine | In development | `#marine` | no |

No card navigates. The accepted design gives the domain cards no link, and Mining and Marine have
no production-ready destination route, so each states its status instead of offering one — the
option R13 section 2 allows. Nothing was disabled, because there was no control to disable.

The homepage domain module now carries its own `domain.*` strings. The `app.*` keys it used before
are **published by `/solutions/` as well**, and this revision is homepage-only, so repurposing them
would have silently retitled that route. `/solutions/` is therefore unchanged and still publishes
*Geothermal Exploration / Mineral Exploration / Environmental & Land Intelligence* under
`#geothermal` / `#mineral` / `#environment` — which every route's nav links point at, and which all
still resolve. **That divergence between the homepage taxonomy and the `/solutions/` taxonomy is now
visible to a visitor and is worth a follow-up task; it is outside this revision's envelope.**

Two things outside the taxonomy were also corrected, both defects rather than design changes:

- **`hero/config/lane.json`** — the eleven R11 domain derivatives were not on the integration write
  surface. The lane check only sees a public-site path once it is *tracked*, so the R11 gate run
  passed while they were untracked and `validate_hero.py` began failing on the first run after the
  commit. They are now declared, and the hero validator is back to 420 / 0.
- **secondary domain-card copy padding** — measured at 1440 px, the copy box on each half-width card
  ran 77-144 px into its own caption, in both languages. The caption is the same width on every card
  but a secondary card is half of one, so those cards now clear the caption vertically, exactly as
  the stacked card below 821 px already did. Verified overlap-free at 1440 / 1024 / 900 / 390 px in
  EN and TR.

Everything below is the R11 record, amended where R13 changed it.

## 1. Start verification

| Check | Result |
| --- | --- |
| Repository identity | `origin` = `github.com/mertkaanakgunlu-debug/orbgss-website` |
| Branch | `feat/web-005b-homepage-visual-fidelity`, tracking `origin/…` |
| Local HEAD before edits | `176e345166bcc084219aa5972c3209c872889626` — exactly the expected head |
| Working tree | clean except an untracked `AGENTS.md` (pre-existing, left untouched) |
| Stashes | none |
| Destructive work needed | none; no reset, no force, no discarded work |

## 2. What was built

The accepted design was translated into the existing static HTML + CSS + vanilla-JS stack. The
approved WEB-005A hero is byte-identical in markup and unchanged in behaviour; only the box it is
drawn in changed, which R10 section 2 and R11 section 9 explicitly authorize.

### Pass A — structural design integration

- **Act 02 · The place** — one contained photograph capped at 1600 CSS px, with the copy inside
  the protected zone of the image on desktop (R10 section 8) and the caption, AOI specification and
  analysis square on the image itself.
- **Act 03 · The evidence** — the rejected three-equal-card gallery is replaced by **one shared
  geographic frame**: three radio-driven layers cross-fading in a single 600 px square, a three-tab
  selector, and a reading column that names the layer, describes it and carries its mandatory
  warning. The frame never moves, which is the point the three cards could not make.
- **Act 04 · The result** — centred: large headline, the priority surface alone as the dominant
  object, a concise lead, and a four-part definition structure ending on what the score is **not**.
- **Inspection aid** — present in the accepted final design at exactly one place and role: its own
  quiet section between the result and the domains, wiping the photograph against one derived
  layer. Implemented only there; nothing was invented or relocated.
- **Domains** — Geothermal leads at full width, the two expansion directions sit beneath it, every
  card states its own truthful status.
- **Why it holds up** — six method commitments on a hairline grid. No icons, no figures.
- **Company / Contact / footer** — the accepted calm, low-density treatment; contact becomes one
  centred ending with one action.
- Responsive desktop / tablet / mobile layouts throughout, same narrative order at every width.

### Pass B — continuity and interaction polish

1. **Hero owns the first viewport.** `height:calc(100svh - var(--header-h))` replaces the old
   `clamp(680px,82vh,980px)`, whose 980 px cap let Act 02 sit visibly below the hero on any window
   taller than ~1068 px. `svh` is deliberate: `dvh` would expose Act 02 when mobile browser chrome
   retracts. Measured at 19 widths × DPR 1 and 2 — Act 02 begins at exactly the viewport height in
   every one of the 38 cases, never above it. No scroll-jacking, no scroll snap.
2. **One governing page ground.** `--orb-bg` carries the whole post-hero story, the footer
   included (scoped by `body.home` so the shared footer on deep routes is untouched). The
   alternating `#02070b` / `#040d15` / `#061018` / `#050d13` section grounds are gone. Section
   distinction is spacing, type scale, imagery, one soft hairline per boundary and inner stages.
3. **Hero → Place.** Act 02 begins below the fold and is revealed by scrolling. The hero's own
   bottom shade already lands on near-black, so there is no colour seam into the page ground, and
   the first post-hero section deliberately carries no top rule.
4. **Place → Evidence.** The photograph's bottom edge dissolves into the page ground through its
   own gradient rather than ending on a line, and Act 03 opens on generous space.
5. **Evidence → Result.** Same ground. The result is dominant by headline scale, centring and the
   silence around it, not by a background change.
6. **Evidence interaction.** One fixed frame; Terrain / THM-01 / ALT-01 selectable. State is three
   radio inputs, so it works with **no JavaScript**, with arrow keys inside the group, and with
   touch (66 px tab targets). Selection is carried by a 2 px underline rule, the label colour
   **and** a "Shown" marker — never colour alone. Plates share one grid cell and cross-fade; the
   reading column stacks in one cell too, so switching never shifts the layout.
7. **Result.** Composition preserved in full; it did not shrink back into a report card.
8. **Domains.** Accepted hierarchy preserved.
9. **Company / Contact.** Not redesigned beyond the accepted centring and the shared ground.

All non-essential motion is opacity/translate only and is disabled under `prefers-reduced-motion`.

### Pass C — tests and evidence

See sections 4-6.

## 3. Deviations from the shared design

Each of these is a deliberate departure; nothing else in the design was changed.

| # | Deviation | Why |
| --- | --- | --- |
| ~~D1~~ | **Withdrawn — overruled by R13.** R11 shipped canonical application names; Product ruled that the accepted homepage taxonomy is Geothermal / Mining / Marine and that route anchors do not override it. | Corrected in section 0. The homepage anchors are now `#geothermal` / `#mining` / `#marine`; `/solutions/` keeps its own vocabulary and every nav link still resolves. |
| D2 | **No per-layer legend chip on the evidence plates.** The design shows a white legend plate on each Act 3 raster and on the result. | Only the priority layer has a governed legend asset (`priority-legend-ramp.png`, the map's own 256-entry LUT). Adding legends for Terrain/THM-01/ALT-01 would mean either inventing them or importing the GEO-WEB-002 `assets/proof/final/*-legend.png` files, which are bound to `/pilot/`. The result keeps its coupled legend exactly as the design shows. |
| D3 | **Act 3 and 4 use the WEB-005B derivatives, not `assets/proof/final/*-1249.webp`.** The design prototype imported the GEO-WEB-002 masters. | R11 section 7: use the currently accepted WEB-005B presentation assets. The homepage binds `web_005b.analytical`; the `proof/final` package stays bound to `/pilot/`. |
| D4 | **Mobile Act 02 puts the copy below the photograph** instead of over it. The design's appendix shows "copy fills the frame" at 390 px. | Measured at 390 px the overlaid copy left the headline, statement and mandatory warning sitting on bright irrigated fields with no usable contrast, and the caption collided with the specification lines. The photograph is now a 4:5 window you scroll into, with its caption on it, and the copy reads on the page ground below. Desktop (≥1101 px) is the accepted integrated composition exactly as designed. **Worth a look in review.** |
| D5 | **The inspection aid is genuinely co-registered.** The prototype wiped the square 36 km rasters against the wide 96 × 54 km photograph and caveated it as "approximate common framing"; its note also said the two sides are "shown at approximate common framing… not a co-registered overlay". | It does not have to be approximate. The manifest records the analysis grid's exact bounds inside the context frame (`x 0.169063–0.544063`, `y 0.166667–0.833333` of the 3200 × 1800 master = exactly 1200 × 1200 at 30 m). The CSS scales and offsets the photograph by those recorded fractions, so both sides really are the same ground — visible in `inspect_*_1440.webp`, where the ridge lines continue across the divider. The caveat copy was corrected to match the fact. `validate_site.py` recomputes the four CSS numbers from the manifest. |
| D6 | **Act 02's AOI square is shown only where the whole 16:9 frame is on screen** (≥701 px), and its label sits above the square's top-right corner. The design placed a decorative AOI box at a fixed `right:16%; top:28%`. | The production square is the *recorded* geometry, not decoration, so it may only be drawn where the fractions it is built from are true of what is on screen. The design drops its box below 1100 px for the same practical reason. |
| D7 | **Domain photographs carry their own place/coordinates/kind caption** and an explicit "Illustrative" footnote; the design used a short `Landsat — illustrative` source line. | `CLAUDE.md` requires location and coordinates on every image, with the third line naming what the layer is. The footnote also states plainly that these are not OrbGSS outputs, not results, and not the pilot area. |

## 4. Copy

No canonical visible copy was removed. `scripts/check_copy_preservation.py` reports 273
differences against `1135e7a7e0b0`, of which the only removals are two attribute bindings:

- `act.evidence.listLabel → @aria-label` ("Evidence layers") — the shared-frame switch is labelled
  by the existing `evidence.switchLabel` ("Evidence layer") instead. The key remains in both
  dictionaries, now unreferenced.
- `alt.terrain → @alt` → `alt.terrain.home` — pre-existing at the starting head, not this pass.

Everything else is an addition. 62 new keys were added in **both** EN and TR (the site validator
fails on any key missing from either). New copy is confined to:

- structural labels for the new composition (tab names, "Shown", the shared-frame metadata lines);
- the four result definitions — the fourth is the existing mandatory warning `act.priority.note`,
  rendered as `<dd class="beam-note">` so it stays excluded from the claim scan;
- the inspection aid's own copy, including its caveat;
- the six method commitments, which restate disciplines this repository already enforces;
- the domain illustrative-photography footnote;
- the contact headline and its CTA.

**No accuracy, performance, customer, ROI, validation or quantitative-metric claim was introduced,
and there are no placeholder metrics in the shipping implementation.** The closing method line
says so explicitly: *"No accuracy, performance, deployment, customer or scale figures are published
for this baseline."*

## 5. Scientific / media boundary

Nothing in the WEB-007..010 program was performed. No super-resolution, no sharpening, blurring or
denoising, no slope overlay, no palette, normalization, mask or NoData change, no reprocessing.
Every Act 3/4 pixel is the same recorded, checksummed MER-108 derivative the starting head shipped.

The one asset change is class-A illustrative photography: the three domain scenes
(`yellowstone-2013`, `chuquicamata-2024`, `ili-delta-2020`) were retired from the homepage by
WEB-002 and are placed again by the accepted design, so they gained responsive WebP derivatives
built by the new `scripts/build_domain_derivatives.py` — a Lanczos downscale of the recorded master
and a WebP encode, no crop and no colour, tone or gamma change, recorded in each scene's
`derivatives` list with width, height, byte size and SHA-256 and recomputed by the validator.

### Safe display density (re-measured, 19 widths × DPR 1 and 2)

| Placement | Widest CSS width | At 2× | Native / widest candidate | |
| --- | --- | --- | --- | --- |
| Act 2 photograph | 1600.00 | 3200 | 3200 | ✅ |
| Terrain | 598.00 | 1196 | 1200 | ✅ |
| THM-01 | 598.00 | 1196 | 1200 | ✅ |
| ALT-01 | 598.00 | 1196 | 1200 | ✅ |
| Priority (result) | 598.02 | 1196 | 1200 | ✅ |
| Inspection aid — photograph | 1595.60 | 3191 | 3200 | ✅ |
| Inspection aid — derived layer | 598.00 | 1196 | 1200 | ✅ |
| Domain · geothermal | 1278.00 | 2556 | 2880 | ✅ |
| Domain · mineral | 727.81 | 1456 | 1800 | ✅ |
| Domain · environment | 727.81 | 1456 | 1800 | ✅ |

The two secondary domain cards stack to the full content width below 821 px and measured 728 CSS
px there, which asks for 1456 at 2× — 1400 was not enough, so they carry an 1800 px candidate. The
lead card asks for 2556 and carries the 2880 px master width. Raw data:
`evidence/web005b_r11/safe_density_sweep.json` and `safe_density_summary.json`.

## 6. Test results

| Suite | Result |
| --- | --- |
| `py -3.14 scripts/validate_site.py` | **PASS** — 4 scenes, 29 html images, 6 routes, 276 i18n keys, 0 warnings |
| `py -3.14 scripts/negative_tests_web005.py` | **72/72** deliberate regressions caught; restored tree identical to baseline |
| `py -3.14 scripts/negative_tests_web005b.py` | **42/42** deliberate regressions caught; restored tree identical to baseline |
| `py -3.14 scripts/check_copy_preservation.py` | 273 differences, 0 canonical visible-copy removals (section 4) |
| `git diff --check` | clean |

### Test updates (only what the new accepted structure required)

- `scripts/validate_site.py`
  - the Act-3 composition check now requires **exactly one** shared `.evidence-frame`, three
    `figure.evidence-plate` and three `label.evidence-tab`, replacing the count of three
    `li.evidence-card`. Three separate frames — the rejected gallery under new class names — now
    fail as loudly as a fourth layer does.
  - the native-density CSS caps now cover `.evidence-frame` and the new `.inspect-frame`.
  - **new:** the inspection aid's registration is recomputed from
    `web_005b.context.frame.aoi_in_frame` and compared against the four CSS numbers, and the
    recorded grid is checked to be square inside the context frame.
  - **new:** any locked scene whose derivatives appear on the homepage must carry a
    `web_005b_placement`, stay homepage-only, name one of its own derivatives, keep
    `css_width × dpr` at or under its widest candidate, and render its on-image label keys; the
    illustrative footnote must exist in both dictionaries.
- `scripts/negative_tests_web005.py` — three mutation anchors retargeted at the new markup, and a
  new case that rebuilds the rejected per-layer-frame gallery. 71 → 72 cases.
- `scripts/negative_tests_web005b.py` — two anchors retargeted, seven new cases covering the
  inspection aid's registration and density and the domain-card placement records. 35 → 42 cases.

## 7. Review artifacts — `evidence/web005b_r11/`

| File | What it proves |
| --- | --- |
| `homepage_desktop_1440_full.webp` | full desktop page, one continuous ground |
| `homepage_desktop_1920_full.webp` | wide monitor: content stays centred and inset |
| `homepage_desktop_1440_full_tr.webp` | the same layout in Turkish (the longer language) |
| `homepage_mobile_390_full.webp` | full mobile page, same narrative order |
| `top_desktop_1440.webp`, `top_desktop_1920.webp`, `top_mobile_390.webp` | scroll position 0: header + hero only, no Act 02 leakage |
| `first_viewport.txt` | the measured numbers behind those captures |
| `evidence_state_terrain_1440.webp`, `…_thermal_…`, `…_alteration_…` | all three evidence states, each with the shown-marker / plate / reading column asserted in the capture log |
| `inspect_thermal_25_1440.webp`, `inspect_alteration_50_1440.webp`, `inspect_priority_75_1440.webp` | the inspection aid on each pair at three wipe positions; the co-registration is visible where the terrain continues across the divider |
| `domains_desktop_1440.webp`, `domains_desktop_1440_secondary.webp`, `…_tr.webp` | the R13 taxonomy on desktop in both languages, with each card's label, status and link count asserted in the capture log |
| `mobile_390_place/evidence/result/inspect/domains.webp` | each section on a phone |
| `scroll_hero_to_domains_1024.webp` | **the continuity artifact**: a real Chrome screencast of Hero → Place → Evidence → Result → Inspection → Domains, resampled by the scroll offset Chrome reports per frame |
| `homepage_desktop_1440_full_reduced_motion.webp`, `top_desktop_1440_reduced_motion.webp`, `reduced_motion.txt` | reduced motion: no video source attached at all, no reveal class, transitions 0 s, `scroll-behavior:auto`, nothing left hidden |
| `safe_density_sweep.json`, `safe_density_summary.json` | the 38-case density and layout sweep, including the empty `first_viewport_leak` and `horizontal_overflow` lists |

Full-page captures are stitched from real scrolled viewport shots.
`Page.captureScreenshot` with `captureBeyondViewport` returned black bands for the lazily-decoded
Act 2 photograph, the result map and the domain cards, because the compositor never painted them;
that was a capture artifact, and stitching is what makes the evidence honest.

## 8. Acceptance checklist (R11 section 12)

| Requirement | State |
| --- | --- |
| shared final design recognizably reproduced | ✅ (deviations in section 3) |
| hero unchanged | ✅ hero markup byte-identical; only `.hero` height and the removed `@media` height overrides changed |
| no Act 02 initial-viewport leakage | ✅ 38/38 measured cases |
| no hard section-colour cuts | ✅ one governing ground for the whole post-hero story |
| layer selector works accessibly | ✅ radios, arrow keys, 66 px targets, non-colour selected state, works with JS off |
| Result visually dominant | ✅ |
| domain hierarchy matches | ✅ |
| desktop/mobile centred and low-density | ✅ |
| no horizontal overflow | ✅ 0 cases in the sweep |
| reduced motion works | ✅ |
| scientific/display invariants pass | ✅ |
| tests and `git diff --check` pass | ✅ |
| real-browser scroll evidence exists | ✅ |

## 9. Remaining visual polish worth CTO attention

1. ~~D1 — domain naming.~~ **Resolved by R13**: the taxonomy is Geothermal / Mining /
   Marine. What remains is that `/solutions/` still publishes the older application
   vocabulary, so the site now says "Mining" on the homepage and "Mineral Exploration"
   one click away. A follow-up task, not this revision.
2. **D4 — mobile Act 02.** The accepted appendix wants the copy over the frame at 390 px; it is
   below it here for legibility. Compare `mobile_390_place.webp` against the design's mobile view.
3. **Act 02 AOI square legibility.** The analysis square sits partly behind the copy column on
   desktop because the recorded geometry puts its left edge at 16.9 % of the frame. The corner
   marks are drawn under the protection shade, so they fade out behind the copy rather than ruling
   lines across it. If Product wants the whole square visible, the honest fix is a different Act 2
   crop, which changes the recorded mark fractions and is a Product/Science decision.
4. **Inspection aid left column.** It is vertically centred against a 600 px figure, as in the
   design, which leaves a tall void above the headline at 1440 px and wider.
5. **Vertical rhythm around Act 04.** The result is given a lot of room on both sides. Intentional,
   but it is the largest single stretch of empty ground on the page.
6. `act.evidence.listLabel` is now an unreferenced dictionary key in both languages. Left in place
   rather than deleting canonical copy.

## 10. Boundaries respected

- Homepage only; no other public route was redesigned.
- No framework migration; static HTML + CSS + vanilla JS throughout, no WebGL.
- No Blender re-render, no hero media, choreography, drape-timing or analytical-sequence change,
  and the obsolete `hero-handoff` result card did not return.
- WEB-006 not started. No merge to `main`, no deploy, no DNS change, no force-push.

**Terminal state:** `REVIEW_READY / WAITING_CTO_VISUAL_REVIEW`
