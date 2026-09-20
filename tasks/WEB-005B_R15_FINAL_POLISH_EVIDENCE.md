# WEB-005B R15 — final polish pass evidence

**Linear:** MER-109
**State:** `REVIEW_READY / WAITING_CTO_VISUAL_REVIEW`
**Branch:** `feat/web-005b-homepage-visual-fidelity`
**Starting HEAD (verified before any edit):** `5f118947` (R14)
**Science authority applied:**
`geothermal-prospectivity@e8aa5d65f56556be928499c50936eb63db88a6ad:tasks/MER-151_GEO-WEB-004_HOMEPAGE_EVIDENCE_PRESENTATION_PARITY_AUTHORITY.md`
(`TERMINAL_ACCEPTED — PUBLIC_WEBSITE_PRESENTATION_ONLY`, consumer WEB-005B / MER-109)
**Immutable hero upstream:** `feat/web-005a-hero-visual-fidelity@1135e7a7e0b0f6db6348dee139d505550d8ca8b9`
**Evidence artifacts:** `evidence/web005b_r15/`

This is a bounded polish pass on the accepted direction. The concept, the hero, the section order
and the visual language are not reopened. Hero markup is byte-identical to R14 and to the accepted
WEB-005A implementation.

---

## 1. What R15 changes, in one line each

| # | Change | Where |
|---|--------|-------|
| A | MER-151 presentation transfer applied to the analytical layers: ALT-01 gets the bounded display window it has needed since R14, THM-01 gets a bounded window plus one fixed gamma | `scripts/build_web005b_presentation.py`, `assets/proof/web005b/*` |
| B | Numbered prep labels removed: `02 · The place`, `03 · The evidence`, `04 · The result`, and the weak `Solutions` kicker | `index.html`, `script.js` |
| C | Act 03 re-measured: the stage is sized to its content and the reading column is anchored top and foot, so the section no longer has empty ground on the right and under the column | `styles.css`, `index.html` |
| D | Act 04 polished: the headline sets its own measure, the definition strip's rules moved into real gutters, the section gives up height so headline + map + legend read together on a laptop | `styles.css` |
| E | Solutions reframed: the pilot framing is gone from the card copy, the section leads on its headline, all three cards share one copy height | `index.html`, `script.js`, `styles.css` |
| F | Tonal hierarchy across the whole page: one family, three grounds, every section still starting and ending on the page ground | `styles.css` |

---

## 2. A — the Science-approved presentation transfer (MER-151)

### 2.1 Why ALT-01 was the whole point

Measured over the governed valid cells of `alt-alt01.tif`
(`ac7f2dade5274d9fd81b7fdbc8bcf7ae828bb958de5c74b9847e6332675fbf14`), on the canonical normalized
coordinate:

| quantile | 0.02 | 0.25 | 0.50 | 0.75 | 0.98 | 0.999 | 1.00 |
|---|---|---|---|---|---|---|---|
| n | 0.0209 | 0.0300 | 0.0350 | 0.0403 | 0.0523 | 0.0828 | 1.0000 |

99.9 % of the layer lived in the bottom 8.3 % of its own range, because a handful of outliers set
`vmax`. The unwindowed render therefore spent essentially the whole palette on cells that are not
there, and the map published as one flat violet field. That is what R14 recorded as blocked: the
only fix was a transfer, `geo_web_002.assets[alt01].legibility_note` forbade one, and every lever
was listed hero-only.

MER-151 resolves exactly that, for exactly this surface. ALT-01 now carries
`q_low = 0.02 / q_high = 0.98` (span 0.96, floor 0.94), resolved once over all valid cells of the
governed source — never from a crop, a tile or a viewport. 4.0 % of cells clip, 2 % at each end.

### 2.2 Per layer, and why

| layer | display window | gamma | reason |
|---|---|---|---|
| terrain | disabled | disabled | this rendering is also the source of the accepted WEB-005A hero Terrain drape state, and it already reads across its full range; changing its transfer would break hero → page continuity for no gain |
| thm01 | `q_abs = 0.998`, resolved `M = 0.7036`, centre pinned at 0, 0.21 % clipped | 0.85 on \|s\| | 0.998 is the smallest clean quantile that clears the mandatory `M >= 0.70` floor (0.98 → 0.5517, 0.99 → 0.6078, 0.995 → 0.6528 all fail it) |
| alt01 | `q_low 0.02 / q_high 0.98`, span 0.96, 4.0 % clipped | disabled | see 2.1; no gamma stacked on top of the window |
| priority | **prohibited, and not used** | disabled | priority stays bound to the fixed scientific 0-100 domain and keeps exactly the colours the hero payoff ends on |

Terrain and priority are byte-identical to their R14 files (`terrain-1200.webp` 822 168 B,
`priority-1200.webp` 1 948 516 B, same SHA-256), which is the cleanest possible proof that the
pipeline outside the new transfer step did not move.

### 2.3 What was NOT used

`web_005b.analytical.not_used` records, and `scripts/validate_site.py` enforces, that none of these
is in the pipeline: AI/generative enhancement or super-resolution, scalar-space interpolation,
Gaussian smoothing or denoising, sharpening/unsharp, CLAHE or any local/adaptive tone mapping,
per-crop autoscaling, mask dilation/erosion/fill, hotspot emphasis, and any CSS filter or blend on
the page.

### 2.4 The 4K/HiDPI permission: implemented, bounded, deliberately not published

MER-151 section 2 authorizes one final RGBA Lanczos3 resize up to 4.00× per axis / 4800 px. It is
implemented in `lanczos_rgba()` — premultiplied alpha, channels clamped to legal range, and the
enlarged alpha masked by a nearest-neighbour enlargement of the governed valid mask so filtered
alpha can never create valid support the governed mask does not have — and it is bounded and
validated. **The published ladder does not use it, on delivery grounds rather than scientific
ones.** A 1800 px (1.50×) rung was built and weighed:

| layer | 1800 px lossless | passes the MER-108 §8 delivery gates? |
|---|---|---|
| terrain | 1.38 MB | yes |
| thm01 | 3.34 MB | no — rejected at every rung |
| alt01 | 5.96 MB | no — rejected at every rung |
| priority | 5.65 MB | no — rejected at every rung |

Three of the four cannot be re-encoded down, because a block transform moves saturated palette
colours off the governed ramp and pulls analytical chroma across the NoData boundary. Publishing
that rung would mean shipping 3–6 MB per panel to precisely the visitors on 2× displays.
Meanwhile every analytical surface on the homepage is capped at 600 CSS px, which the **native**
1200 px grid already serves at a true 2× device pixel ratio. There is no density to gain and a lot
of weight to lose, so the enlargement stays unused and the layout stays inside native density.

This is a delivery decision and needs no Science re-entry to revisit: MER-151 section 7 lets
Product & Software swap conformant derivatives in without reopening the authority.

### 2.5 Provenance recorded

`assets/imagery/sources.json → web_005b.analytical` carries, per layer: MER-113 export id, source
filename + SHA-256, the MER-108 and MER-151 authority pointers, the canonical normalization
identity and resolved parameters, the display-window parameters with their resolved limits and
clipped fraction (or `disabled`), the gamma with its formula and bounds (or `disabled`), the
palette topology id plus the exact ordered stops and the LUT SHA-256, the resize method and scale
per derivative, the mask/coverage mode, the hillshade parameters, renderer and encoder versions,
and the deterministic output SHA-256 of every file. The validator recomputes the LUT from the
recorded stops and re-checks every checksum against the file on disk.

**Truthfulness:** these are presentation derivatives of a 1200 × 1200 / 30 m / EPSG:32635 raster.
Nothing on the page, in the manifest or in the scripts claims finer ground resolution or additional
scientific evidence, and `resolution_claim` says so in the manifest itself.

---

## 3. B — prototype labels removed

Removed from the page and from both dictionaries: `act.context.kicker` (`02 · The place`),
`act.evidence.kicker` (`03 · The evidence`), `act.priority.kicker` (`04 · The result`) and
`solutions.kicker` (`Solutions`). Each section now leads on its headline and supporting paragraph.

Kept, because they are meaningful labels rather than numbering: `Inspection aid`, `Why it holds up`,
`Company`, `How we work`, `Contact`.

One more piece of specialist vocabulary went with them: the ALT-01 alt text said "clay and hydroxyl
spectral alteration proxy". Alt text is read aloud, so it is visible copy. It now describes what a
reader sees — and with the display window applied it is also simply more accurate, because the
layer really does run the length of its ramp now.

The mandatory scientific warnings were **not** shortened, reworded or moved. They are the honesty
anchors, the validator pins their required terms per placement in both languages, and R15 does not
economise on them.

---

## 4. C — Act 03 re-measured

The panel cap is unchanged at 600 CSS px. What changed is the stage: it used to run the full 1280
shell, so a 600 px map sat beside a 634 px column holding 330 px of text. The stage is now measured
to its content (`max-width: 1040px`, a 600 px map and a 394 px column), the column is stretched to
the map's height, and the subordinate structure/geology footnote — which used to run full width
underneath — moved to the foot of that column with the single frame spec under it. Same copy, same
subordinate weight, same `#structure` anchor.

---

## 5. D — Act 04 fit and the definition strip

* The headline's `max-width: 13ch` broke *"Where to look first."* after "look". The cap is gone and
  the sentence sets its own measure.
* `--result-map` tightened from `max(320px, min(600px, 100svh - 392px))` to
  `max(340px, min(600px, 100svh - 356px))`, and the section's own padding came down, so more of the
  map survives on a short window.
* The definition strip's rules used to be a border on the cell itself, running hard against the
  text on both sides, and the warning cell added a second gold rule of its own on top of that. The
  gutter is real space now and the rule sits in the middle of it, inset from the type top and
  bottom. The warning keeps its caution colour on its term, where nothing collides with it. The
  responsive ladder is 4 columns → 2 × 2 (≤1180 px) → one column (≤700 px), and each step moves
  which cells carry a rule instead of inheriting one that would land mid-row.

---

## 6. E — Solutions

The pilot framing is out of the card copy: Geothermal now reads "the application the workflow above
was built and published against" rather than naming a running pilot. The section leads on its
headline. The status labels stay, because `CLAUDE.md` requires the first active application and the
expansion directions to be labelled as such — that is a claim-discipline rule, not framing.

All three cards already shared one padding box after R14; they now also share one copy-block height,
so the title sits the same distance off the card's foot whether the sentence runs two lines or
three and whether the card is the full-width lead or one of the pair beneath it.

The per-card location / coordinate / kind captions stay removed, and the section footnote stays the
sole carrier of "these are public-domain Landsat scenes of other places, not OrbGSS results" — the
validator enforces its wording in both languages. The dead `.domain-card .scene-label` rule and the
mobile bottom padding that existed only to clear that caption are gone.

No card navigates: Mining and Marine still have no production-ready destination route, and no route
was invented for them.

---

## 7. F — the tonal system

The page stays one continuous ground. What changes is how high off it a section sits:

* `--orb-bg` `#030B12` — the page ground. Every section still starts and ends on it.
* `--orb-lift` `#061420` — the slightly raised ground a reading section rests on (Evidence,
  the inspection aid, the method grid).
* `--orb-deep` `#020810` — the ground the page settles onto as it closes (Result, Company, Contact,
  footer).
* `--orb-atmos` `rgba(28,74,104,.30)` — the one soft atmospheric tint on the page, a wide radial
  behind the Result.

The rule that makes this read as depth instead of blocks: the lift or the settle happens in the
**middle** of a section and returns to `--orb-bg` at both edges, so no boundary is ever a colour
step. The boundary hairlines fade out before the page gutter rather than cutting the full width.

Both new tokens are pinned in `scripts/validate_site.py` alongside the rest of the Product palette,
so a quiet edit to the page's depth fails the build.

---

## 8. Gates

| gate | result |
|---|---|
| `py -3.14 scripts/validate_site.py` | **PASS**, 0 warnings, 29 homepage images, 268 i18n keys |
| `py -3.14 hero/scripts/validate_hero.py` | **420 checks, 0 failed** |
| `py -3.14 scripts/negative_tests_web005.py` | **72/72 caught**, restored tree identical to baseline |
| `py -3.14 scripts/negative_tests_web005b.py` | **55/55 caught** (12 of them new MER-151 bounds), restored tree identical |
| `py -3.14 scripts/check_copy_preservation.py 5f11894` | 28 differences, **all of them declared** in §3 and §6 — three kicker keys, `solutions.kicker`, `alt.alt01`, `solutions.copy`, `domain.geothermal.copy`, in both languages |
| hero markup | **byte-identical** to R14 and to the accepted WEB-005A implementation (10 148 B, `<section class="hero">…</section>`) |

Evidence artifacts: `evidence/web005b_r15/` — full pages at 1440 / 1920 / 1024 / 768 / 390 and in
Turkish, first viewports, every section at 1440, the three Evidence states, the Act 04 laptop fit at
1366×768 / 1440×800 / 1512×860, narrow-width Result / Evidence / Solutions, reduced motion, the
before/after transfer sheet, plus `layout_measurements.txt`, `delivery_ladder.txt`,
`negative_tests_web005*.txt`, `copy_preservation_vs_r14.txt` and `validators.txt`.

### 8.1 Layout measurements (`evidence/web005b_r15/layout_measurements.txt`)

**Safe density** — 13 widths × DPR 1, 2 and 3, drawn width measured with `getBoundingClientRect`,
never inferred from `sizes`:

| surface | widest CSS px ever drawn | at DPR 2 | published native |
|---|---|---|---|
| Act 02 context photograph | 1600.00 | 3200 | 3200 |
| Act 03 evidence panel | 598.00 | 1196 | 1200 |
| Act 04 result map | 598.00 | 1196 | 1200 |
| inspection aid | 598.00 | 1196 | 1200 |

No governed raster is ever laid out above its native density. `document.scrollWidth == innerWidth`
at every one of the 39 combinations, so there is no horizontal overflow anywhere.

**Act 04 laptop fit** — headline top to legend bottom, against the viewport:

| viewport | headline → legend | map | fits? |
|---|---|---|---|
| 1280×720 | 627 px of 720 (87 %) | 362 | yes |
| 1366×768 | 683 px of 768 (89 %) | 410 | yes |
| 1440×800 | 719 px of 800 (90 %) | 442 | yes |
| 1440×900 | 819 px of 900 (91 %) | 542 | yes |
| 1512×860 | 782 px of 860 (91 %) | 502 | yes |
| 1600×950 | 872 px of 950 (92 %) | 592 | yes |
| 1920×1080 | 932 px of 1080 (86 %) | 598 | yes |

R14 measured 73–76 % of the section visible on these screens; R15 puts the headline, the lead, the
whole map and its legend inside one viewport at every laptop size tested.

**First viewport** — the header plus the hero own it exactly, and Act 02 leaks 0 px at
1280×720, 1440×900, 1920×1080, 1920×1440, 768×1024 and 390×844.

### 8.2 Delivery encoding (`evidence/web005b_r15/delivery_ladder.txt`)

Unchanged in method from R3, re-run against the new renders. Terrain still qualifies at q98
(−79.5 / −82.2 / −84.6 %, PSNR 46.6–47.7 dB, NoData untouched). THM-01, ALT-01 and Priority stay
lossless: at the most conservative rung on the ladder they measure PSNR 32.7 / 23.6 / 24.8 dB with
off-ramp distances of 40 / 112 / 90 levels and NoData chroma bleed of 80–106 levels, which is a
visible, interpretation-changing change rather than a delivery encode.

### 8.3 Payload

The shipped analytical payload on a 1× desktop is **2.16 MB** (terrain 50 KB delivery + thermal
552 KB + alteration 799 KB + priority 758 KB; the inspection aid re-uses the same files), against
1.54 MB at R14. The whole +0.62 MB is ALT-01 and THM-01 carrying real detail now that the display
window has stopped collapsing them — an unwindowed near-uniform field compresses to almost nothing
precisely because there is nothing in it. That is the honest cost of the legibility fix, and it is
the reason the 1800 px rung in §2.4 was measured rather than assumed.
