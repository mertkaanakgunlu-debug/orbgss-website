# WEB-005A — Hero visual fidelity: review evidence

**Task:** WEB-005A / MER-107 — `tasks/WEB-005A_HERO_VISUAL_FIDELITY.md`
(canonical: `docs/web-005-polish-authority@f58f4361ef5cb13371464e530bdf9a19ac5c575a`)
**Visual direction:** `docs/WEB_005_POLISH_VISUAL_DIRECTION_AUTHORITY.md`
(canonical: `docs/web-005-polish-authority@5622e6765763e69f374796c33986bf680db86e6a`)
**Parent:** WEB-005 / MER-93, terminally accepted at `main@00af0f232a8d7d77f5ca61d758461ff7316ba151`
**Branch:** `feat/web-005a-hero-visual-fidelity`
**Rejected review checkpoint (retained as before-evidence):** `ffa2f2944ca5992afb9e9891b42745a9bd1105ad`
**Superseded R2 package (retained as before-evidence; did not pass the human visual gate):** `a6897828d6e35595ea5a9a39a1e812b0fcbbfb35`
**State:** `REVIEW_READY` (R3)
**Final implementation HEAD:** `37152222c33fdc09265ba022ce45828c8d002723` (this evidence publication follows it as a documentation-only commit)

This document has three parts. **Part A** is the R3 revision: the current implementation state and
the only part under review. **Part B** is the R2 package, which was technically green, was pushed at
`a6897828…`, and did not pass the human visual gate; it is kept verbatim because it is the "before" of
every R3 comparison and because its satellite model, sensing-line envelope, lock event, Earth albedo
stack and validators are carried forward rather than restarted. **Part C** is the first checkpoint's
evidence, kept for the same reason.

---

# Part A — R3 visual revision

## 1. Identity

| | |
| --- | --- |
| Branch | `feat/web-005a-hero-visual-fidelity` |
| Final implementation HEAD | `37152222c33fdc09265ba022ce45828c8d002723` |
| Baseline | `main@00af0f232a8d7d77f5ca61d758461ff7316ba151` |
| Superseded R2 package (did not pass the human visual gate) | `a6897828d6e35595ea5a9a39a1e812b0fcbbfb35` (implementation `b285c90cf685f6ca9da61c41302ae496d7e8169b`) — Part B |
| Rejected first checkpoint | `ffa2f2944ca5992afb9e9891b42745a9bd1105ad` — Part C |
| Product visual references | two CTO-supplied images, composition/energy only; not copied, not shipped, not in the repository |

## 2. What changed, against the required visual outcome

| Narrative beat | R2 (superseded) | R3 |
| --- | --- | --- |
| 1 · Earth rotates in space | accepted establish | unchanged accepted establish (frames 1–96), same model, lighting, atmosphere and AgX look |
| 2 · satellite enters from behind the Earth | emerged at frame 31 as a 1.7 % speck and crawled the limb for four seconds | hidden for the first two seconds, comes round the lower-left limb at frame 50–58 on a fast arc (2.4 °/frame), 4 % of the frame width by frame 80, 8 % by 112 |
| 3 · settles into position | constant 0.7 °/frame: drifted through the acquisition composition and out of the bottom-left at frame 166 | time-remapped derived orbit: the rate eases to 0.03 °/frame over frames 60–110 and the camera is locked off for the beat, so the platform **holds at (0.25, 0.40) ± 0.01 of the frame from frame 136 to 192** at 13 % of the frame width |
| 4 · scan / acquisition | lines connected, but stayed drawn from off-screen for two seconds after the satellite had left | lines connect 110–124, frame locks 128–144 (pulse 2.6×, corner locks draw in), a brighter sweep band crosses the frame 144–178, the lines **release at 178–192 with an acquisition-complete pulse while the satellite is still in frame**; the acquisition frame is 6.3 % of the frame width (was 3.9 %) |
| 5 · regional zoom / hold | slow drift to an oblique 1260 km view; ground soft | one decisive dive (192–262) on the same registered target, eased in and out, motion-blurred; the 420 km frame vanishes as its edges leave, and the **accepted 36 × 36 km analysis AOI draws in as its own frame** (236–254, lock pulse 2.4×, sweep) and settles; genuinely still hold 262–276, 166 km across the frame, 27° off nadir |
| 5b · Earth under the hold | 500 m Blue Marble window | Blue Marble colour everywhere, multiplied under the hold by a **30 m Sentinel-2 detail ratio** (structure only, no colour or season change); cloud veil cleared over the window |
| 6 · evidence layers over the AOI | — (one detached result panel) | page layer registered **inside the analysis frame** by a CSS homography on the audited corners: Elevation (NASADEM context) → THM-01 → ALT-01, each byte-exact with its exact label and accepted warning in the caption column |
| 7 · priority result as payoff | 320–440 px panel beside a 36 px marker | the accepted priority surface fills the analysis frame (23 % of the frame width — 334 CSS px at 1440, 596 at 2560) with its own legend, ledger of the four layers, exact label, mandatory warning, meta line and CTA |

**Faults / structure.** The requested narrative names a faults layer. No public-safe fault or lithology
master is authorized (`docs/PRODUCT_AND_CONTENT_AUTHORITY.md`, CLAUDE.md design invariants: structure/geology
is a deliberate, score-invariant data gap that must not be filled). The hero therefore shows the accepted
evidence set — terrain context, THM-01, ALT-01 — and the accepted priority result, and nothing is
fabricated in the place of a fault layer. This is the one deliberate deviation from the requested beat list.

Unchanged and re-verified: the four-act homepage; every GEO-WEB-002 asset, checksum and Act 2–4
placement; the `mvp_remote_sensing_priority_v1` label and semantics; `render_surface: html_overlay` (no
governed raster in any lossy encode); EN/TR parity; reduced-motion, reduced-data, small-screen and
no-dual-download behaviour; the media ceilings; the accepted Kızıldere centre; the 420 km regional frame's
classification as **not** the analysis AOI.

## 3. Satellite asset provenance (A-HERO-03)

Unchanged from R2: procedural and OrbGSS-original (`hero/scripts/satellite_model.py`), no external model,
no operational spacecraft or sensor identity; the validator scans the spec for spacecraft/sensor names.
R3 changes only its hero scale (`wingspan_bu` 1.0 → 1.15, because it now holds farther from the camera,
out at the limb) and its pass. Light linking still gives it self-shadowing without a planet shadow.

## 4. Earth source provenance and resolution (A-HERO-11)

All R2 NASA sources are unchanged (Part B §4). R3 adds one derived texture:

| Asset | Source | Dimensions | Bytes | SHA-256 |
| --- | --- | --- | --- | --- |
| `earth_s2_detail_multiplier` — `hero/assets/source/s2_kizildere_detail_30m.png` (16-bit greyscale ratio, lon 28.15–29.42 E, lat 36.94–38.84 N) | Copernicus Sentinel-2 L2A, tiles T35SPC + T35SPB, 2025-09-25 (S2C, baseline 05.11, cloudy pixels 0.001–0.002 %, no snow); bands B04, B02, SCL; six source files identified by name and SHA-256 in `hero/evidence/earth_detail_sharpen.json` | 3720 × 7051 | 48 460 935 | `c6c89c9837bc34524edaf28ed83c263f3353716817b4e5f780c43d7837ee463a` |

Method (`hero/scripts/materialize_earth_sharpen.py`): 10 m BOA reflectance → 30 m block mean → broadband
pan = 0.6 red + 0.4 blue → **ratio = pan / (pan blurred to 510 m)**, clipped 0.45–2.0, open water held to
0.85–1.18, cloud/shadow/snow/no-data (SCL) = 1.0 → inverse-mapped from an equirectangular grid through the
WGS84 UTM 35N forward projection (verified against the accepted centre to **0.05 m**) → 16-bit PNG. The
Earth material multiplies the Blue Marble albedo by it inside the window, so the 500 m mean is preserved,
**no colour is introduced** and no seam can form. Rights: Copernicus Sentinel data are free, full and
open; the required attribution *Contains modified Copernicus Sentinel data (2025)* is now in the site
footer (EN/TR). The source tiles are the science project's raw archive and are not copied into this
repository. The ratio has no units and no palette, is not a measured layer, carries no forbidden layer
class and is never delivered to the page.

**Effective source-texel coverage at the R3 hold** (`hero/evidence/texel_coverage.json`; 165.5 km across
the frame, 86.2 m per delivered pixel):

| Texture | m / texel | source texels across the frame | magnification at 1920 px |
| --- | --- | --- | --- |
| rejected checkpoint (8192 composite) — what this hold would have shown | 3856 | 43 | 44.7× upscaled |
| Blue Marble 500 m window (colour) | 366 | 453 | 4.24× |
| **Sentinel-2 detail multiplier (structure)** | **30** | **5518** | **0.35× — not upscaled** |

Colour stays Blue Marble at 500 m by design; every ridge, valley, field pattern and coastline the viewer
resolves at the hold comes from the 30 m multiplier.

## 5. Motion, orbit and framing audit (A-HERO-01, A-HERO-02, A-HERO-12, A-HERO-13)

`hero/evidence/shot_audit_production.json` (`audit_shot.py`, evaluated scene, all 276 frames, projection
through Blender's own `world_to_camera_view`). **All 18 checks pass:**

| Check | Measured | Threshold |
| --- | --- | --- |
| AOI locked to the shifted anchor after handover | 0.00001 | ≤ 0.02 frame |
| AOI apparent size never reverses | 0.0009 | ≤ 0.0015 / frame |
| AOI orientation continuous | 0.02°/frame | ≤ 2° |
| camera jerk ratio | 0.158 | ≤ 0.35 |
| focal-length rate (now relative: a zoom's speed is Δf / f) | 3.3 % / frame | ≤ 5 % |
| cut ratio | 2.78 | ≤ 4.0 |
| AOI in frame from handover to end | 0 frames out | 0 |
| headline-safe region clear through the establish | 0.0 occupancy | 0.0 |
| satellite fully in frame and unoccluded through the beat (**110–192**, was 116–160) | none clipped | none |
| satellite lower-left of the target through the beat | none wrong-side | none |
| satellite never overlaps the target frame | none | none |
| satellite readable at the anchor frame (146) | **13.0 % of frame width** | ≥ 8 % |
| satellite never a foreground fly-by | 21.9 % max (as it leaves the left edge) | ≤ 25 % |
| **sensing lines release while the satellite is still in frame** | visible at frame 192 | required |
| **satellite has left before the analysis hold** | none visible from 262 | none |
| **analysis AOI spans the declared width through the hold** | 23.2–23.4 % | 19–26 % |
| **analysis frame settles for the hold** | width 0.0002 / frame, centre 0.00001 / frame | ≤ 0.0015, ≤ 0.002 |
| **analysis frame fully inside the frame through the hold** | 0 frames | 0 |

Pass, per frame (x, y as frame fractions, y from the bottom; width as a fraction of frame width):

| Frame | Satellite (x, y) | Width | Target (x, y) | 420 km frame | 36 km AOI |
| --- | --- | --- | --- | --- | --- |
| 48 | behind the planet | — | 0.64, 0.63 | 2.4 % | — |
| 56 | 0.42, 0.33 — coming round the lower-left limb | 2.8 % | 0.64, 0.63 | 2.7 % | — |
| 80 | 0.41, 0.44 — climbing the limb | 4.1 % | 0.66, 0.64 | 3.2 % | — |
| 112 | 0.36, 0.45 — lines connecting, camera completing its handover | 7.8 % | 0.62, 0.62 | 4.5 % | — |
| 136 | **0.25, 0.40** — in position | 12.6 % | 0.68, 0.64 | 6.2 % | — |
| 144 | **0.25, 0.40** — lock pulse | 13.0 % | 0.68, 0.65 | 6.3 % | — |
| 176 | **0.25, 0.41** — sweep | 13.1 % | 0.69, 0.65 | 6.4 % | — |
| 192 | **0.24, 0.41** — lines released | 14.3 % | 0.69, 0.65 | 6.6 % | — |
| 200 | 0.17, 0.38 — left behind by the dive | 17.2 % | 0.69, 0.65 | 7.6 % | — |
| 208 | out of frame (left edge) | — | 0.68, 0.64 | 10.1 % | 0.7 % |
| 232 | — | — | 0.65, 0.59 | 37.9 % | 2.5 % |
| 248 | — | — | 0.63, 0.56 | beyond the frame, vanished | 9.1 % |
| 264–276 | — | — | **0.63, 0.553** | — | **23.3 %** |

Orbit: one circle at 900 km, over 22.2 N 2.6 W at frame 146 heading 060; `rate_profile`
2.4 → 0.03 °/frame (eased over 60–110). The committed satellite keyframes derive from that intent
(`orbit_plan.py`, exact integral of the piecewise-linear rate), the camera's from its `shot_intent`, and the
validator re-derives both. The pass was solved, not tuned: the anchor is the solution of "be at (0.25, 0.40)
of the frame at frame 146", and the diagnosis that made it possible is recorded in the intent's note — the
on-screen drift of a platform this close is parallax from the camera's own dolly, so the camera is locked
off for the beat (radius 14.4 → 14.0 BU, 37 → 38 mm) and makes its whole approach afterwards.

Registration: the regional fixture is unchanged. The analysis frame is a new fixture
`kizildere_analysis` (`production_analysis_aoi`, `is_analysis_aoi: true`): the accepted centre, the accepted
36 km extent, turned 1.10° for UTM 35N grid convergence so it sits on the accepted EPSG:32635 grid square. The
validator enforces all of that, and `audit_aoi`'s sphere conformance applies to it through the same code path.

## 6. Sensing FX and lock events (A-HERO-04, A-HERO-05)

| Element | Value | Gate |
| --- | --- | --- |
| core lines / glow / cone | unchanged R2 envelope (4 lines to the corners, 2.2 → 3.6 km, #7FEFFF; sheath #3CCBFF; faint cone) | unchanged |
| regional frame | 2.6 km border, halo ribbon 15 km, corner-lock arms 64 km; **now gated by a transparent presence node**, so it is absent before it appears and its border, halo and fill can vanish (224–240) instead of turning into a dark ribbon; its corner locks are left to sweep outward past the frame edges (gone by 250), which reads as the acquisition frame opening onto the analysis AOI | halo + pulse required |
| lock pulse | emphasis 1.0 → **2.6** (frame 138) → 1.15; acquisition-complete pulse 1.9 at 188 as the lines release | peak ≥ 1.8 |
| sweep | band alpha 0.5, width 0.06, 144–178 | forward range |
| analysis frame | 0.34 km border, halo 1.6 km, locks 6.5 km; appears 236–248, **locks draw in 240–254, pulse 2.4× at 254**, sweep 248–264; its own material datablocks | appears after release; pulse ≥ 1.8; locks land before the hold; no sensing lines of its own |
| timing | lines 110–124 on, **178–192 off (inside the beat)**; regional vanish after release and before the hold | ordered, validator-enforced |
| motion blur | production profile, shutter 0.5 | — |
| claims | no sensing-physics vocabulary in the production configuration or hero copy | scanned |

`validate_hero.py`: **292 checks, 0 failed** (R2 contract + the R3 contract: time-remapped pass with a settled
section covering the beat, release inside the beat, exactly one analysis frame on the accepted 36 km extent
and centre, its lock event and ordering, the hold framing re-derived Blender-free from the committed camera,
the detail multiplier's manifest record, checksum, window, attribution and strength).

## 7. Final handoff (A-HERO-06, A-HERO-14)

The sequence ends on the accepted analysis AOI at audited screen geometry: centre (0.630, 0.553), corners
nw (0.532, 0.730) · ne (0.746, 0.717) · se (0.730, 0.371) · sw (0.512, 0.387), y from the bottom.
`index.html` carries those numbers as `data-hero-anchor`; `script.js` maps them through the poster/video
cover-fit (`object-position: center 46%`) and, from 260/24 s (or at once in every static state):

1. places the evidence stage on the four corners with a CSS `matrix3d` homography — a screen-space
   placement of the image elements; no raster is re-projected, recoloured, filtered or cropped;
2. reveals **Elevation — NASADEM context → THM-01 → ALT-01 → priority**, 0.95 s apart, each an accepted
   byte-exact `geo_web_002` derivative (800 / 1249 by `sizes`), while the caption column beside the frame shows
   a four-row ledger and the current layer's exact public label and accepted warning (`.beam-note`);
3. settles on the priority result with the export's own legend inside the frame, the exact label, the meta
   line (36 × 36 km · EPSG:32635 · 30 m), the mandatory warning and the CTA to Act 4.

Ceiling: the stage is at most `1249 / devicePixelRatio` CSS px; beyond that the raster stack shrinks about
its centre inside the frame instead of upscaling. Measured live, the payoff layer is 283 CSS px wide at a 1024 px viewport, 296 at 1280, 334 at 1440, 596 at 2560 (1192 device px at 2×) and 895 at 3840 (1×) — recorded per asset in `sources.json` → `web_005_placement.hero_stage`. The caption column sits right of the frame from about 1240 px and folds to a compact two-column strip under it below that; the headline column is constrained to stay left of the frame from first layout, so nothing reflows at the reveal. The hero crop moved from `center 52%` to `center 46%` (and `69% 46%` below 981 px) so the analysis frame stays whole on 3840-wide and phone-width heroes.
Below 981 px the stage is off and the accepted strip (priority thumbnail, kicker, exact label) is used.
`scripts/validate_site.py` fails if the anchor or any corner drifts from the audit by more than 0.006, if the
object-position changes, if the ceiling clamp is missing, if the four layers are not accepted derivatives in
the accepted evidence order ending on the priority payoff with its legend, or if any layer's exact label or
warning is missing.

## 8. Production media (A-HERO-07)

<!-- media-table-r3-start -->
Rendered at **2304 × 1296** (Cycles, OptiX, 128 adaptive samples, compositor bloom, motion blur shutter 0.5) and delivered at 1920 × 1080; encoded through Blender 4.5.10 LTS's bundled FFmpeg with the bitrate search recorded in `hero/evidence/production_media.json`. The poster is the last frame.

| File | Container / codec | Dimensions | Rate · frames · duration | Bitrate | Size / ceiling | SHA-256 |
| --- | --- | --- | --- | --- | --- | --- |
| `assets/hero/orbgss-hero.webm` | WebM / VP9 | 1920 × 1080 | 24 fps · 276 frames · 11.5 s | 1396 kbps | **2.797 MiB** / 3.0 MiB | `c094d323be7747de7ff3c6299a634c8ddd66d2de58317e9c8575449c871423ad` |
| `assets/hero/orbgss-hero.mp4` | MP4 / H.264 | 1920 × 1080 | 24 fps · 276 frames · 11.5 s | 2800 kbps | **3.880 MiB** / 4.5 MiB | `e02e25e2ccd7ef344e06cffff8b96ff30d632c0d0e202a3802fb7a9734a977d9` |
| `assets/hero/hero-poster-1600.webp` | WebP q88 | 1600 × 900 | — | — | **169.4 KiB** / 180 KiB | `4b80ba21ef9125bd8accbcf01d5085f7bf7d5ab93921ff3f8891315eb0123f83` |
| `assets/hero/hero-poster-900.webp` | WebP q88 | 900 × 506 | — | — | **67.7 KiB** / 180 KiB | `467a29f208c35fcbfb2771f7c553c2160be83103b347fa314ff47b6841c6d319` |

Bitrate search (WebM): 1900 kbps → 3.591 MiB; 1396 kbps → 2.797 MiB.
<!-- media-table-r3-end -->

## 9. Fallback matrix (A-HERO-08)

| Profile | Hero | Handoff | Video bytes |
| --- | --- | --- | --- |
| desktop ≥ 981 px, motion allowed | one encode attached at runtime (WebM if VP9 `probably`, else MP4), plays once, holds on the last frame | evidence sequence from 260/24 s; layer rasters are warmed when playback starts | one encode |
| `prefers-reduced-motion: reduce` | poster only, video never attached | priority result inside the frame at once, no transitions; a mid-visit switch cancels a running sequence and settles on the result | 0 |
| ≤ 780 px | poster only | strip layout, at once | 0 |
| 781–980 px | one encode | strip layout at the hold | one encode |
| Save-Data / slow network | poster only | at once | 0 |
| autoplay refused / encode error | poster | at once | ≤ one encode |
| JavaScript off | poster; `<video>` has no `src`/`<source>` | stage and figure stay `hidden` — the answer is Act 4 | 0 |

No state downloads both encodes (validator-enforced).

## 10. Human visual gate (A-HERO-10)

`hero/evidence/web005a_r3/` — 1280 × 720 WebP stills of the R3 production frames, each beside the R2 frame
it replaces (`*_r2.webp`, the superseded package's "after"):

| Moment | R2 (before) | R3 (after) |
| --- | --- | --- |
| Satellite entry | `1_entry_r2.webp` (f80) | `1_entry_r3.webp` (f84) |
| Acquisition / scan | `2_acquisition_r2.webp` (f146) | `2_acquisition_r3.webp` (f146) |
| Scan sweep, satellite holding | — | `2b_scan_hold_r3.webp` (f176) |
| Dive, frames handing over | `3_regional_hold_r2.webp` (f240) | `3_dive_r3.webp` (f236) |
| Hold / handoff frame | `4_final_handoff_r2.webp` (f276) | `4_hold_r3.webp` (f276) |

Full sequence: the shipped `assets/hero/orbgss-hero.webm` / `.mp4`; a 24-frame contact sheet
(`sequence_contact_sheet.png`, frames 1 → 276); and page captures (headless Edge against the local static server, reduced-motion
static state, each retried until a pixel probe confirmed the poster and the layer had painted): `page_1440_payoff.png` and
`page_2560_payoff.png` (final state), `page_1440_layer1_terrain.png`, `page_1440_layer2_thm01.png`,
`page_1440_layer3_alt01.png` (the evidence sequence, stepped deterministically with the `#hero-layer=<id>` review hook),
`page_768.png` and `page_375.png` (strip layout). The narrow captures are taken through a fixed-width iframe: headless Edge
enforces a minimum window width of about 500 px, which is why the R2 package's `page_375.png` shows a cropped 500 px layout
rather than a true phone layout. The live playback path was exercised in the browser pane (static reveal, layer states, relayout
on resize); a screen recording of live playback is **NOT RUN** — the shipped encodes are the sequence capture.

## 11. A-HERO-01 … A-HERO-14 matrix

| Gate | Result | Evidence |
| --- | --- | --- |
| A-HERO-01 geometry continuity | **PASS** | §5; `validate_hero.py` 292 checks, 0 failed |
| A-HERO-02 orbital-path audit | **PASS** | §5; derived, time-remapped circular orbit; 21.9 % peak as it exits, no fly-by |
| A-HERO-03 generic-satellite provenance | **PASS** | §3 |
| A-HERO-04 sensing-FX negative gate | **PASS** | §6; envelope + negative cases; no baked raster |
| A-HERO-05 target-frame quality | **PASS** | §6; two lock events, both pulsed and drawn in; registration §5 |
| A-HERO-06 resolved ending | **PASS** | §5, §7; still hold 262–276, sequence from 260/24 s, `held` state |
| A-HERO-07 production media integrity | **PASS** | §8 |
| A-HERO-08 fallback/network | **PASS** | §9 |
| A-HERO-09 regression suite | **PASS** | site validator PASS 0 warnings; hero validator 292/292; negative tests 27/27, tree restored byte-identical |
| A-HERO-10 human visual gate | **evidence supplied — awaiting Product** | §10 |
| A-HERO-11 source resolution | **PASS** | §4; structure at 0.35× at a hold 7.6× closer than R2's |
| A-HERO-12 satellite readability | **PASS** | §5; 13.0 % of frame width at frame 146 = 187 px at 1440 CSS px, held for 56 frames |
| A-HERO-13 reference composition | **evidence supplied — awaiting Product** | `2_acquisition_r3.webp`: Earth right-dominant, satellite lower-left on the limb, four lines to a luminous frame |
| A-HERO-14 analytical handoff | **PASS** | §7; governed content inside the acquired target, 23 % of the frame width |

`NOT RUN`: hosted preview (accepted `HOSTED_PREVIEW_NOT_RUN`); bit-reproducibility of the GPU render (not
reproducible on this machine, per `hero/README.md`; not a WEB-005A gate).

## 12. Scientific / public semantic non-change statement

No scientific method, score meaning, threshold, eligibility, CRS/grid/unit/NoData/mask/resampling semantics,
public label or warning changed, and no new evidence family appears. The hero now *shows* three more accepted
assets (terrain, THM-01, ALT-01) — the same byte-exact derivatives Act 3 shows, under the same exact labels and
warnings; their `web_005_placement` records gain a `hero_stage` note and nothing else. `sources.json` →
`scenes`, `web_002`, `production_source`, `web_vnext` and `policy` are untouched. The hero caption still says
*Rendered orbital sequence — not sensor imagery*. The analysis frame is the accepted AOI drawn as a frame;
nothing scientific is rendered into it and no governed pixel enters the video. The Sentinel-2 detail ratio is a
presentation texture of the render, not a layer. Structure/geology remains the stated data gap. One piece of
accepted footer copy changed, for truthfulness: the sentence describing the hero as a Landsat composite (true of
the pre-WEB-005 poster, not of the render) now names NASA Blue Marble and the Copernicus attribution.

## 13. Not done under this authority

No production deploy, no Vercel production alias, no DNS/domain change, no WEB-005B, no WEB-006.
`CONTACT_RELEASE_GATE` and `HOSTED_PREVIEW_NOT_RUN` remain as recorded by WEB-004/005.

---

# Part B — R2 package `a6897828…` (superseded; did not pass the human visual gate)

*Recorded on 2026-09-16. Technically green, visually not accepted. Kept as the "before" of Part A; nothing below is current implementation state.*

## 1. Identity

| | |
| --- | --- |
| Branch | `feat/web-005a-hero-visual-fidelity` |
| Final implementation HEAD | `b285c90cf685f6ca9da61c41302ae496d7e8169b` |
| Baseline | `main@00af0f232a8d7d77f5ca61d758461ff7316ba151` |
| Rejected checkpoint (before) | `ffa2f2944ca5992afb9e9891b42745a9bd1105ad` |
| Product visual references | two CTO-supplied images, composition/energy only; not copied, not shipped, not in the repository |
| Baseline review video (Product's rejected recording) | `2026-09-16 09-51-15.mp4`, 2560 × 1600, 60 fps, 2481 frames, 20 135 600 bytes, SHA-256 `98c72ed90c3d3b377f4da3210fa8cbbeb8a7835a1413df4addfeed0b44787840` (held outside the repository) |

## 2. What changed, against the R2 lock

| R2 requirement | Rejected checkpoint | R2 |
| --- | --- | --- |
| Earth model / lighting | 8192 px Blue Marble composite, 5.9× upscaled at the hold | same model, lighting, atmosphere and AgX look; albedo replaced by NASA BMNG 21600 × 10800 plus a lossless 500 m regional window under the target (0.56× — no upscaling) with the same cloud layer the old composite was built from |
| Satellite | bus + two flat panels + cone; 59 px at the acquisition frame; read as a speck | procedural volumetric generic EO platform (bevelled MLI bus, end frames, radiator, nadir instrument deck with two apertures, three-segment arrays with real thickness on yokes, dish with feed, star trackers, thruster); 10.2 % of frame width at the anchor frame, arrays spread across the line of sight |
| Orbital choreography | circular orbit, but emerging at the bottom edge and overhead the AOI at the lock | derived orbit (900 km, over 22 N 4 W at frame 146, heading 105, 0.7 °/frame): hidden at the open, emerges from behind the left limb at mid-height (frame 31), rides the limb against the atmosphere glow, sits lower-left of the target through the whole beat, exits bottom-left after 166 |
| Sensing FX | one cone at 0.016 alpha — invisible | four thin core lines (#7FEFFF) to the footprint corners inside fainter glow sheaths (#3CCBFF), one very faint support cone, compositor bloom; connected root-to-target by constraint at every frame |
| Target frame / lock | thin border, locks appeared late, no event | crisp #98F5FF border with a soft halo ribbon on the sphere; lock pulse (2.6×) at 134–158 while the lines connect; corner locks draw in from their corners; second settle at 232–262 that the page hands off from |
| Camera | AOI dead-centre; Earth filled the frame symmetrically | accepted establish untouched; lens shift places the target upper-right (x 0.72, y 0.69) with Earth right-dominant and the headline column clear; closer, longer hold (829 km, 48 mm: the frame spans 37 % of the width) |
| Final handoff | 110 px detached card at bottom right | registration marker at the audited position of the 36 km analysis AOI inside the rendered 420 km frame, leader lines, and the accepted priority derivative with its in-frame legend as a 320–440 CSS px panel coupled below the frame; exact label, mandatory warning, meta line and CTA in EN/TR |

Unchanged and re-verified: the four-act homepage; every GEO-WEB-002 asset, checksum and
placement; the `mvp_remote_sensing_priority_v1` label and semantics; `render_surface:
html_overlay` (no governed raster in any lossy encode); EN/TR parity; reduced-motion,
reduced-data, small-screen and no-dual-download behaviour; the 420 km regional frame's
classification as **not** the analysis AOI; the accepted Kızıldere centre (37.9794 N, 28.7907 E),
span, bearing and surface offset.

## 3. Satellite asset provenance (A-HERO-03)

The satellite is **procedural and OrbGSS-original**: `hero/scripts/satellite_model.py`, driven
entirely by the `eo_satellite` object spec in `hero/config/scene.json`. No external model was
downloaded, so there is no third-party licence to clear. Its vocabulary — boxy MLI bus, nadir
instrument deck, two three-segment arrays, small dish, star trackers, thruster — is generic to
civil EO platforms and specific to none; the validator scans the spec for operational
spacecraft/sensor names and the hero copy for sensing-physics vocabulary, and the negative tests
prove both checks fire. Scale is a hero-scale fiction, as the accepted lane's was (`wingspan_bu`
1.0 = 1000 km; the accepted placeholder's bus was 220 km).

Self-shadowing without a planet shadow: Cycles light linking gives the satellite its own sun with
only its own parts as blockers, and removes it from the primary sun's blocker set, so the body
reads volumetric and never prints a shadow on the Earth.

## 4. Earth source provenance and resolution (A-HERO-11)

Materialized under the task's Earth-source-resolution authority; all NASA public domain under the
NASA media usage guidelines (`https://www.nasa.gov/nasa-brand-center/images-and-media/`), NASA
acknowledged as source, no insignia, no endorsement implied, no third-party restriction on any
record. Recorded in `hero/assets/manifest.json`; the hero validator recomputes every SHA-256.

| Asset | Record | Dimensions | Bytes | SHA-256 |
| --- | --- | --- | --- | --- |
| BMNG July 2004 w/ topography & bathymetry, global | Visible Earth 73751 → `science.nasa.gov/earth/earth-observatory/blue-marble-next-generation/base-topography-bathymetry` | 21600 × 10800 | 27 201 049 | `d225f1f35a6448a4d1d8f6de6e48f3433e470085b70a35800e64f384f269a7b0` |
| BMNG July 2004 500 m tile C1 (lon 0–90 E, lat 0–90 N) | same record | 21600 × 21600 | 87 763 762 | `ee8490ab1eb35d620d8d1ad8e69b3234c0b050e4eddb80e7232a2d165e475aa0` |
| Regional detail crop of tile C1 (lon 12–46 E, lat 27–50 N; texels x 2880–11040, y 9600–15120; lossless PNG) | derived by `hero/scripts/materialize_earth_detail.py`; `hero/evidence/earth_detail_crop.json` | 8160 × 5520 | 56 247 989 | `0e819ee7fb6e0efcfe51c28f4b052ae9216c39f2386e3556686a0efd47059882` |
| Blue Marble clouds | Visible Earth 57747 | 8192 × 4096 | 35 870 468 | `d137775d8966ab8d443fd5126dc6e7ad72072bc1ed50555c5818d221735daf0f` |

**Effective source-texel coverage at the hold** (`hero/scripts/texel_coverage.py` →
`hero/evidence/texel_coverage.json`; frame width at the AOI 1261 km on the last keyframe, 657 m per
delivered pixel at 1920 px):

| Albedo under the target | m / texel (E–W at 38 N) | source texels across the frame | magnification at 1920 px |
| --- | --- | --- | --- |
| rejected checkpoint (8192 composite) | 3856 | 327 | **5.87× upscaled** |
| R2 global basemap (21600) | 1462 | 862 | 2.23× |
| R2 regional detail window (500 m crop) | 366 | 3449 | **0.56× — not upscaled** |

Linear texel-density gain under the target: **10.5×**. The detail window contains the accepted
target centre and is blended into the global basemap over a 2.5° feather; the validator checks
the material's window against the crop record and every texture against the manifest.

## 5. Motion, orbit and framing audit (A-HERO-01, A-HERO-02, A-HERO-12, A-HERO-13)

`hero/evidence/shot_audit_production.json` (`audit_shot.py`, evaluated scene, all 276 frames, projection
through Blender's own `world_to_camera_view` so lens shift is included). All 13 checks pass:

| Check | Measured | Threshold |
| --- | --- | --- |
| AOI locked to the shifted anchor after handover | 0.00001 | ≤ 0.02 frame |
| AOI apparent size never reverses | 0.0 | ≤ 0.0015 / frame |
| AOI orientation continuous | 0.23°/frame | ≤ 2° |
| camera jerk ratio | 0.156 | ≤ 0.35 |
| focal-length rate | 0.21 mm/frame | ≤ 0.6 |
| cut ratio | 2.83 | ≤ 4.0 |
| AOI in frame from handover to end | 0 frames out | 0 |
| headline-safe region clear through the establish | 0.0 occupancy | 0.0 |
| satellite fully in frame and unoccluded through the beat (116–160) | none clipped | none |
| satellite lower-left of the target through the beat | none wrong-side | none |
| satellite never overlaps the target frame | none | none |
| satellite readable at the anchor frame (146) | **10.2 % of frame width** | ≥ 8 % |
| satellite never a foreground fly-by | 19.1 % max | ≤ 22 % |

Pass, per frame (x, y as frame fractions, y from the bottom; width as a fraction of frame width):

| Frame | Satellite (x, y) | Width | Target (x, y) | Frame extent |
| --- | --- | --- | --- | --- |
| 32 | 0.49, 0.57 — emerging from behind the left limb | 1.7 % | 0.63, 0.60 | 1.8 % |
| 80 | 0.41, 0.63 — in space, riding the limb | 3.0 % | 0.66, 0.63 | 3.4 % |
| 120 | 0.30, 0.49 — lines connecting | 5.5 % | 0.61, 0.58 | 4.0 % |
| 144 | 0.28, 0.42 — lock pulse | 9.7 % | 0.68, 0.63 | 5.6 % |
| 160 | 0.18, 0.20 — end of beat | 15.9 % | 0.71, 0.66 | 8.4 % |
| 168 | out of frame bottom-left | — | 0.71, 0.67 | 10.2 % |
| 276 | behind the planet | — | **0.72, 0.687** | **37.3 %** |

Registration: the AOI system, its fixture and its centre are the accepted ones; the audit's
"AOI locked to anchor" is 0.00001 of the frame, and `audit_aoi.py`'s sub-metre sphere conformance
is unchanged because no AOI geometry changed. The camera's committed keyframes still derive from
their `shot_intent`, and the satellite's from its `orbit_intent`, both re-derived by the validator.

## 6. Sensing FX and lock event (A-HERO-04, A-HERO-05)

Configuration, enforced by `validate_hero.py` (`WEB-005A R2 visual-fidelity contract`, 35 checks)
and exercised by `scripts/negative_tests_web005.py`:

| Element | Value | Gate |
| --- | --- | --- |
| core lines | 4, to the corners; 2.2 → 3.6 km radius; alpha 0.92 → 0.50; emission 7.0; #7FEFFF | tip radius ≤ 8 km; alpha ≥ 0.6/0.35; emission ≥ 3 |
| glow sheath | 4.5× radius; alpha 0.14 → 0.05; #3CCBFF | root alpha ≤ 0.3 |
| support cone | tip 210 km; alpha 0 → 0.028 | tip alpha ≤ 0.06 |
| border | 2.6 km, #98F5FF, emission 5; halo ribbon 11 km, alpha 0.5 | halo ribbon required |
| lock pulse | emphasis 1.0 → **2.6** (frame 142) → 1.15; second settle 1.15 → 1.9 (246) → 1.25 | peak ≥ 1.8 |
| corner locks | draw in 132 → 150; pulse 1.5 at 156; 1.45 at 248 | draw keys required, inside the beat |
| timing | lines 116–132 on, 192–214 off; scan 150–204; locks after the lines connect | ordered |
| bloom | compositor BLOOM, threshold 1.8, strength 0.26, size 7 | — |
| claims | no sensing-physics vocabulary in the production configuration or the hero copy | scanned |

Negative tests (deliberate regressions, all caught): lines faded to 0.05 alpha; lines thickened
to a 90 km slab; a "radar swath" claim in the satellite note; a satellite keyframe typed off its
orbit; the lock pulse removed; the handoff anchor moved; the exact label removed; the warning
detached from its mandatory-warning class — plus the 12 WEB-005 cases. **20/20**, restored tree
byte-identical to baseline.

## 7. Final handoff (A-HERO-06, A-HERO-14)

The rendered sequence ends on the acquired 420 km regional frame at audited screen coordinates
(centre 0.72, 0.687; extent 0.373; bounds 0.518–0.891 × 0.507–0.821). `index.html` carries those
numbers as `data-hero-anchor`; `script.js` maps them through the poster/video cover-fit
(`object-position: center 52%`) at any hero size and, at the second lock settle (frame 236,
9.83 s) or immediately in every static state:

1. a registration marker appears at the true position of the 36 × 36 km analysis AOI inside the
   rendered frame (36/420 of its extent);
2. two leader lines draw from the marker to the result panel;
3. the panel rises: the accepted `priority-800` / `priority-1249` derivative (byte-exact,
   unfiltered, ≤ 440 CSS px = 880 device px at 2×, inside the 1249 px ceiling) with the export's
   own legend inside its frame, the kicker, the exact public label, a meta line stating the
   36 km AOI against the 420 km frame, the mandatory warning as a `.beam-note`, and the CTA.

Placement is deterministic: right-aligned above the caption, never over the marker, never over the
headline column; it stacks, then shrinks, and below 981 px it is the accepted full-width strip.
`scripts/validate_site.py` fails if the anchor drifts from the audit by more than 0.006, if the
CSS object-position or panel clamp changes, or if the label, warning, legend, meta or marker are
missing. Governed pixels are never in the video.

## 8. Production media (A-HERO-07)

<!-- media-table-start -->
Rendered at **2304 × 1296** (Cycles, OptiX, 128 adaptive samples, compositor bloom) and delivered at 1920 × 1080; encoded through Blender 4.5.10 LTS's bundled FFmpeg with the bitrate search recorded in `hero/evidence/production_media.json`. The poster is the last frame.

| File | Container / codec | Dimensions | Rate · frames · duration | Bitrate | Size / ceiling | SHA-256 |
| --- | --- | --- | --- | --- | --- | --- |
| `assets/hero/orbgss-hero.webm` | WebM / VP9 | 1920 × 1080 | 24 fps · 276 frames · 11.5 s | 1385 kbps | **2.819 MiB** / 3.0 MiB | `0ef4b223290015aea31349884c226f8116ef34b8c8655ac8abe73936ce613c81` |
| `assets/hero/orbgss-hero.mp4` | MP4 / H.264 | 1920 × 1080 | 24 fps · 276 frames · 11.5 s | 2800 kbps | **3.678 MiB** / 4.5 MiB | `5b7f6877c5b5bf5caadac1514962452e7c5edf4c5be1808035a8b3c4309ae416` |
| `assets/hero/hero-poster-1600.webp` | WebP q88 | 1600 × 900 | — | — | **98.7 KiB** / 180 KiB | `70105cd3ebe74823330dff33b99253bc3d4e1ec36ceb63a7a16c9ea0a514b161` |
| `assets/hero/hero-poster-900.webp` | WebP q88 | 900 × 506 | — | — | **43.8 KiB** / 180 KiB | `c3bdcd3bde5e18c21630a828c80a2a7c1527ce98ad132a61f160382311c5a1f2` |

Bitrate search (WebM): 1900 kbps → 3.621 MiB; 1385 kbps → 2.819 MiB.
<!-- media-table-end -->

## 9. Fallback matrix (A-HERO-08)

| Profile | Hero | Handoff | Video bytes |
| --- | --- | --- | --- |
| desktop ≥ 981 px, motion allowed | one encode attached at runtime (WebM if VP9 `probably`, else MP4), plays once, holds on the last frame | marker + leaders + panel at 236/24 s | one encode |
| `prefers-reduced-motion: reduce` | poster only, video never attached | shown immediately, no transitions | 0 |
| ≤ 780 px | poster only | strip layout, immediately | 0 |
| Save-Data / slow network | poster only | immediately | 0 |
| autoplay refused / encode error | poster | immediately | ≤ one encode |
| JavaScript off | poster; `<video>` has no `src`/`<source>` | figure is `hidden` — the answer is Act 4 | 0 |

No state downloads both encodes: the markup declares no `<source>` and no `src` (validator-enforced),
and `script.js` attaches exactly one.

## 10. Human visual gate (A-HERO-10)

`hero/evidence/web005a_r2/` — 1280 × 720 WebP pairs from the rejected checkpoint's frames (before)
and the R2 production frames (after):

| Moment | Before | After |
| --- | --- | --- |
| Entrance | `1_entrance_before.webp` (f68) | `1_entrance_after.webp` (f80) |
| Acquisition / lock | `2_acquisition_before.webp` (f150) | `2_acquisition_after.webp` (f146) |
| Regional hold | `3_regional_hold_before.webp` (f236) | `3_regional_hold_after.webp` (f240) |
| Final handoff | `4_final_handoff_before.webp` (f276) | `4_final_handoff_after.webp` (f276) |

Full sequence: the shipped `assets/hero/orbgss-hero.webm` / `.mp4` are the capture; a 24-frame contact
sheet (frames 1 → 276, 1960 × 1676) is at `hero/evidence/web005a_r2/sequence_contact_sheet.png`. Page
captures (headless Edge against the local static server) are in the same folder: `page_1440_handoff.png`
(1440 × 900, reduced-motion static state, so the last-frame poster, the analysis-AOI marker, the leaders
and the result panel are all revealed deterministically), `page_768.png` and `page_375.png` (strip
layout). The playback path was verified live in the browser pane: the sequence plays once, reaches
`held`, and the marker, leaders and panel are revealed at the same audited geometry (marker at
1003 × 195 CSS px, panel 614 × 354 CSS px at 1440 × 900).

## 11. A-HERO-01 … A-HERO-14 matrix

| Gate | Result | Evidence |
| --- | --- | --- |
| A-HERO-01 geometry continuity | **PASS** | §5 (0.00001 lock; AOI unchanged); `validate_hero.py` 242 checks, 0 failed |
| A-HERO-02 orbital-path audit | **PASS** | §5; derived orbit, 19.1 % peak width, no fly-by |
| A-HERO-03 generic-satellite provenance | **PASS** | §3; procedural, no identity, validator scan + negative test |
| A-HERO-04 sensing-FX negative gate | **PASS** | §6; envelope + 3 negative cases; no baked raster (`render_surface` check) |
| A-HERO-05 target-frame quality | **PASS** | §6; pulse 2.6×, draw-in, halo; registration §5 |
| A-HERO-06 resolved ending | **PASS** | §7; settle at 232–262, handoff at 236/24 s, `held` state |
| A-HERO-07 production media integrity | **PASS** | §8; validators recompute bytes/SHA-256 and ceilings |
| A-HERO-08 fallback/network | **PASS** | §9 |
| A-HERO-09 regression suite | **PASS** | site validator PASS 0 warnings; hero validator PASS; negative tests 20/20 |
| A-HERO-10 human visual gate | **PASS (evidence supplied)** | §10 |
| A-HERO-11 source resolution | **PASS** | §4; 5.87× → 0.56×, provenance and checksums recorded |
| A-HERO-12 satellite readability | **PASS** | §5; 10.2 % of frame width at frame 146 = 147 px at 1440 CSS px; `2_acquisition_after.webp` |
| A-HERO-13 reference composition | **PASS (evidence supplied)** | Earth right-dominant, satellite lower-left, lines to a luminous frame — `2_acquisition_after.webp`, `1_entrance_after.webp` |
| A-HERO-14 analytical handoff | **PASS** | §7; `page_1440_handoff.png` |

`NOT RUN`: hosted preview (accepted `HOSTED_PREVIEW_NOT_RUN`); bit-reproducibility of the GPU render
(not reproducible on this machine, per `hero/README.md`; not a WEB-005A gate).

## 12. Scientific / public semantic non-change statement

No scientific method, score meaning, threshold, eligibility, CRS/grid/unit/NoData/mask/resampling
semantics, label or warning changed. `assets/imagery/sources.json` → `scenes`, `web_002`,
`geo_web_002`, `production_source`, `web_vnext` and `policy` are untouched; `web_005` changed only in
its hero-media records and descriptive provenance fields. The hero caption still says *Rendered
orbital sequence — not sensor imagery* in EN and TR. The satellite depicts no operational spacecraft
or sensor, and the sensing lines are attention, not physics. The 420 km frame is still
`production_regional_frame`, `is_analysis_aoi: false`; the 36 km analysis AOI is shown only at its
true relative position and size, and its result only as the accepted, byte-exact derivative.

## 13. Not done under this authority

No production deploy, no Vercel production alias, no DNS/domain change, no WEB-005B, no WEB-006.
`CONTACT_RELEASE_GATE` and `HOSTED_PREVIEW_NOT_RUN` remain as recorded by WEB-004/005.

---

# Part C — Rejected checkpoint `ffa2f294…` (retained before-evidence)

*Recorded on 2026-09-16 before Product review. Technically green, visually not accepted. Kept as
the "before" of Part B; nothing below is current implementation state.*

## B.1 What this revision was

The accepted WEB-005 hero was structurally right and visually unfinished. Five Product defects were
named; each is addressed below with what changed and why. Nothing outside the hero's rendered media
and its playback timing was touched.

## B.2 Defect 4 — satellite orbital motion

The accepted path was eight hand-typed world-space points whose distances from Earth's centre were
11.77, 16.44, 10.91, 9.12 … 8.08 BU — nothing about it was orbital. The checkpoint replaced it with
one circular 705 km orbit generated rather than typed and solved against the accepted camera path
(tilt −35°, −175° → +80°): occluded at the open, limb crossing at ~50, overhead the AOI at 150, out
of frame by ~190, behind the Earth again by 236. Peak on-screen size 87 px. Product's R2 finding: the
satellite remained a speck and emerged at the bottom edge.

## B.3 Defect 3 — the scan/beam effect

Four opaque corner cones and a 13 %-wide scan band were replaced by a single boresight at
0.002 → 0.016 alpha and a 0.030-wide pushbroom line. Product's R2 finding: the cone was nearly
invisible and the satellite–target link illegible.

## B.4 Defect 5 — the AOI frame

Border 9.0 → 2.6 km, corner-lock arm 85 → 52 km, width 15 → 5.4 km, edge samples 48 → 112, fill grid
24 → 32; nothing that carries geometric meaning changed. Carried forward into R2 unchanged.

## B.5 Defect 1 — the ending

The tail was re-choreographed so the scan completes, the boresight retires, the border firms, the
corner locks resolve in and the page-layer handoff reveals at frame 240. R2 keeps the idea and
moves the lock event to the acquisition beat with a second settle for the handoff.

## B.6 Defect 2 — softness: measurements

Bitrate was not the constraint (+64 % bitrate bought +1.4 % measured detail; 1600 × 900 delivery was
−18 … −24 %; constrained-quality could not fit the budget). The cause was the 8192 px basemap:
3856 m per texel at the AOI, ~371 texels across a 1430 km frame, a 5.2× magnification. The
checkpoint left that as `BLOCKED_ON_SOURCE_RESOLUTION`; the R1 Product clarification and the R2
authority made the higher-resolution rights-safe source implementation-owned, and Part A §4 closes
it.

## B.7 Checkpoint media (superseded)

| File | Codec | Dimensions | Duration | Size | SHA-256 |
| --- | --- | --- | --- | --- | --- |
| `assets/hero/orbgss-hero.webm` | VP9 | 1920 × 1080 | 11.5 s | 2.765 MiB | `d86fdfc3ddf02011ed8fdfebd54a244b7ac804bec7a20199b8f2131b81d859a5` |
| `assets/hero/orbgss-hero.mp4` | H.264 | 1920 × 1080 | 11.5 s | 3.521 MiB | `333b182b54a9c7a73b1c062558a71ab6fbd03a3ef216697d99da01b74f8943b8` |
| `assets/hero/hero-poster-1600.webp` | WebP q88 | 1600 × 900 | — | 82.9 KiB | `5f86d27df4db675b5a70e1035017144cc49f1738ab818e51dfaf55a1d618b98d` |
| `assets/hero/hero-poster-900.webp` | WebP q88 | 900 × 506 | — | 40.3 KiB | `dd3ef9cbe50fa2d26552b1ef7a0583e4e74e4ea02bce9428d751ba547cee8338` |

Validators at the checkpoint: site PASS 0 warnings; hero PASS 187 checks; negative tests 12/12.
Before/after stills of the checkpoint itself remain in `hero/evidence/web005a/`.
