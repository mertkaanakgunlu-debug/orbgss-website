# WEB-005A R3 — Preview gate 3: four-corner acquisition story

**Task:** WEB-005A / MER-107 (bounded continuation; no new task, no new authority)
**State:** `PREVIEW_GATE_3_SUBMITTED` — low-cost preview evidence only. **Not** `REVIEW_READY`.
**Branch:** `feat/web-005a-hero-visual-fidelity`
**Answers:** Product's human visual review of preview gate 2 (`b6cd5fb`) — `REVISION_REQUIRED`.

**Governing authority, newest first:**

1. **Product chat override of 2026-09-18, after the human visual review of gate 2.** The viewer read "beams
   go toward the middle, then the AOI appears". The true AOI geometry and the true analytical / drape authority
   are preserved internally, but the *visible* acquisition may and must use a larger presentation reticle
   centred on the true AOI: four lines to its four corners, a clearly visible fan between them, a clear
   left-to-right sweep while the camera is fixed, the reticle legible during beam lock, then continuous
   tightening onto the true AOI. Thin line language, cyan / teal palette and zoom-after-retirement are kept.
2. `docs/web-005-polish-authority@b9579efbfa0c13342ac24a40e825909ac2845957:tasks/WEB-005A_R3_PREVIEW_GATE_2_PRODUCT_DECISION.md`
   — the platform may not cross the caption (§2); masked analytical ground shows Terrain, not dark patches
   (§3); no colour bar, legend, card or layer label in the hero (§4); timing not to be lengthened (§5).
3. `c7c6cb1…` (decision on gate 1), over `946cd8b…`, `db4605a…`, `473b48a…`.

> **One conflict, stated so it is not silent.** `b9579ef` §1 — written *before* the visual review, state
> `AWAITING_PUBLISHED_PREVIEW_REVIEW` — says the four lines must keep ending on the true corners and must not
> be spread for readability. The chat override (1) was given *after* that review and says the opposite for the
> visible lines. This preview follows the override. The authority branch still carries the older sentence;
> Product should publish the override there so the record and the render agree.

**What this is not.** Nothing shipped changes. `index.html`, `styles.css`, `script.js`, `assets/**`, the
production scene `hero_production_kizildere` and its shipped WebM / MP4 / poster are untouched; the site
validator is unchanged at PASS, 0 warnings. **No production render was made.** No deploy, no DNS, no merge.
Gates 1 and 2 are retained as before-evidence at `cd2018e` and `b6cd5fb`.

---

## 1. Deliverables

**1. Corrected animatic** — `hero/renders/preview_r3gate3/animatic/hero_r3_preview_gate3_0001-0384.mp4`
(local only, ignored, never site media; sent with this submission). 960 × 540, Cycles 32 samples, every frame
at 24 fps, 384 frames, 16.0 s: 11.5 s motion + 2.75 s analytical sequence + 1.79 s priority hold — the same
envelope as gate 2, not lengthened. H.264 / MP4, 4 398 426 bytes, SHA-256
`472836f2d19603c4e85ebe744c19371b08350d20f0ddbdf54da9adae52b1efb6`; 6.9 s/frame, 43.9 min wall clock. The
container opens as 960 × 540 with 384 frames. Record: `preview_frames.json` → `animatic`.

**2. 1440 × 900 real-page composites** — `hero/evidence/web005a_r3_preview3/`

| Required state | Frame | File |
| --- | --- | --- |
| beam start | 114 | `page_1440_f114_beam_start.webp` |
| full four-corner lock | 134 | `page_1440_f134_four_corner_lock.webp` |
| mid-scan fan sweep | 152 | `page_1440_f152_mid_scan.webp` |
| first post-scan zoom frame | 187 | `page_1440_f187_first_zoom.webp` (the literal first frame with camera motion) |
| final priority hold | 384 | `page_1440_f384_final_priority.webp` |
| *(extra)* reticle legible before any line | 104 | `page_1440_f104_reticle_first.webp` |
| *(extra)* platform exit, clear of the caption | 204 | `page_1440_f204_platform_exit.webp` |
| *(extra)* final hold under the unchanged shade | 384 | `page_1440_f384_current_shade.webp` |

Sheets: `three_gates_sheet.webp` (gates 1 / 2 / 3, same crop and scale, lock and mid-scan),
`draw_on_detail_sheet.webp` (frames 96 → 134 at 3×), `sweep_detail_sheet.webp` (west / middle / east),
`sequence_contact_sheet.webp` (29 stills), `page_1440_contact_sheet.webp`. Stills are 1280 × 720
(`preview_gate`, 9 s/frame); checksums in `preview_frames.json`.

## 2. Choreography (24 fps, one scene, one camera, no cut)

| Frames | Beat | Camera |
| --- | --- | --- |
| 1 – 186 | **fixed observer** | locked off |
| 24 – 84 | satellite comes round the **lower-left limb**, rises and **settles** at (0.56, 0.38); measured settled at 85 | fixed |
| 86 – 102 | **aiming beat**: 56.8° slew onto the target | fixed |
| 98 – 114 | **the target resolves first**: reticle frame + halo at 0.7 of their locked brightness (98–110), corner brackets drawn (100–114) | fixed |
| 108 – 126 | four thin lines **draw on** from the instrument aperture to the reticle's **four corners**, staggered 2 frames, 12 frames each | fixed |
| 132 | **lock**: the reticle brightens 2.75× once all four lines have landed | fixed |
| 126 – 168 | translucent fan **between the four lines** (126–136); light curtain + ground band sweep **west → east = left → right** (136–168, 1.33 s) | fixed |
| 168 – 178 | fan and wash retire (168–176), lines release (170–178) | fixed |
| 178 – 210 | platform resumes its pass and leaves through the **right edge**, above the caption | fixed to 186 |
| 186 – 266 | one eased approach; the reticle **tightens continuously onto the true 36 km corners** | moves from 187 |
| 266 – 384 | hold: relief rises (276–292); Terrain → THM-01 → ALT-01 → priority (276–342); **priority alone** (342–384) | still |

## 3. How each required change is answered

Numbers are from `preview_gate_audit.json` (384 evaluated frames) unless a pixel measurement is named.

**3.1 Four lines visibly land on four corners.** `beams.anchor` is `presented` again, this time by Product
instruction, and the validator now *requires* it. Each line ends on its own reticle corner (worst 0.69 m) and
starts on the instrument aperture rim. The reticle is 7.1–7.2 % of the frame wide while acquiring — 15.1× the
true footprint — so the four endpoints are about 135 px apart at 1920 instead of 9. What keeps this honest:
the reticle corners are the true governed corners scaled along the footprint's **own diagonals** about the
**true centre** (angular deviation 0.0003°, one scale factor on all four; centre offset never above 2.5 m);
the true corners are still built as `aoi_true_<corner>` and audited; and **no anchor moves while a line is
attached** — the validator refuses a morph window that opens before the release frame (measured drift while
attached: 0.48 m over a 394 km anchor-to-corner distance, consistent with single-precision noise in the
evaluated world matrices as the Earth turns; both ends are Earth-fixed empties and the morph value is 1.0
throughout).

**3.2 The fan is clearly visible between the beams.** The fan's top is now exactly the aperture square the
lines leave from and its foot is the reticle they land on, so it *is* the volume between the four lines
(validator-enforced). Veil alpha 0.06 from mid-way down; curtain peak alpha 0.24 with a faint trail behind the
blade so direction is unambiguous; both in `scan_cyan`, both dimmer than the lines. See
`sweep_detail_sheet.webp`.

**3.3 Clear left-to-right sweep while the camera is fixed.** The curtain's foot travels **6.4 % of the frame
width**, west slice to east slice, monotonically left to right on screen (gate 2: 0.5 % on the ground). Sweep
136–168, entirely inside the fixed phase; curtain and ground band read one keyed value.

**3.4 The target is legible during beam lock — it no longer "appears afterwards".** The order is now
settle → aim → **reticle resolves** → lines → lock → sweep. When the first line leaves the aperture (frame
109) the reticle frame is already at 0.67 of its locked brightness and its brackets are 71 % drawn; it is
complete before the last line lands (126). The lock itself is an event *on an already visible target*: a
2.75× brightening at 132. Validator: the reticle must start at least 8 frames before the first line and its
brackets must finish before the last line lands. `page_1440_f104_reticle_first.webp` shows the target with no
line yet.

**3.5 Thin line language and cyan / teal kept.** Same stated weights as gate 2 (outline 1.5 px, halo 7 px,
brackets 2.4 px at 1920; core radius 1.5–1.9 km, 3× sheath). Measured on the most foreshortened edge across
the shot: outline 1.0–1.4 px, halo 4.7–6.8 px, brackets 1.6–2.2 px. Line-core pixels on the four separated
lines at the lock frame: median RGB (146, 194, 200), hue 188°, saturation **0.28** (gate 1: 0.10, gate 2: 0.27).

**3.6 Zoom only after beam / fan retirement.** Camera translation, rotation, focal length and lens shift are
0.0 for frames 1–186; first motion at 187; lines, fan and wash are all 0.0 by 178. The lens shift is now
*held* until 214 (see 3.7).

**3.7 Platform exit clear of the caption (`b9579ef` §2).** Zooming cannot move the platform out (gate 2
analysis), so the exit is its own orbit — and one great circle fixes both entry and exit. The anchor point
fixes *where* it acquires; the heading only chooses the circle through it. Heading **100° → 86°**: the
acquisition position is identical by construction (x ≥ 0.498 against the 0.475 copy edge, 12.7 % wide,
unclipped, drift 1.8 %), the entry now comes round the lower-left limb and rises into position, and the exit
leaves through the **right edge at mid-height** instead of the bottom-right corner. It resumes at the release
frame (178, camera still fixed) at **1.3° of arc per frame** against gate 2's 2.3, so it glides rather than
streaks; the lens shift is held until it has gone, because re-framing the target early carries the platform
down toward the caption. Measured against a protected region built from the caption's real box on the
1440 × 900 page (frame x 0.698–0.944, y 0.070–0.134) plus 0.04 / 0.05 margins, with the silhouette grown by its
motion-blur travel: **zero frames inside**, closest approach 0.010 frame heights above the region (0.060 above
the text). Widest silhouette **19.3 %** (bound 22 %), out of frame from 210, never re-enters.

**3.8 Masked analytical ground shows Terrain (`b9579ef` §3).** The relief material now shows the Terrain
layer — lit as context, exactly as in the Terrain state — under each analytical layer's **own alpha, used as
delivered**: no fill, no dilation, no threshold, no extrapolation. A new coverage pass
(`render_drape_states.py --coverage`) renders the material's per-pixel analytical coverage so the mask can be
measured rather than assumed: rendered mean coverage 0.849 (priority) and 0.854 (ALT-01) against the delivered
textures' mean alpha 0.834 and 0.840. Screen space is perspective-weighted, so that 1.5-point difference is
indicative, not proof; it is an open item (§5.3). On pixels the pass reports as fully covered, **99.9–100 %**
fall inside the delivered texture's own colour set through the lossless Standard-view path (the same pixels in
the AgX scene render: 67 %).

**3.9 No colour bar, legend, card or label (`b9579ef` §4).** None is rendered (validator) and none is in the
composites. The only text over the hero is the existing bottom-right caption, unchanged. The final composite
uses the same **proposed** analysis-state shade as gate 2 (CSS in §6, harness-only): the shipped shade leaves
the footprint's left 60 px at 70 % luminance, the proposed one at 99.5 % (whole footprint 99.9 %).

**Preserved and re-measured:** fixed observer; draw-on (16 % on the first visible frame, 12 frames per line,
monotonic); retirement before motion; one persistent adaptive presentation (largest step 0.78 % of a frame
width per frame, only ever tightening, landing 0.42 m from the true corners); relief from the governed
`top-dem.tif` only, 3×, one UV (0.46 m); Terrain → THM-01 → ALT-01 → priority; priority-only hold 43 frames;
governed-grid residual 49.8–55.6 m (accepted); motion 11.5 s, reveal 2.75 s, sweep 1.33 s.

## 4. Gates

| Gate | Result |
| --- | --- |
| `py -3.14 scripts/validate_site.py` | PASS, 0 warnings (site untouched) |
| `py -3.14 hero/scripts/validate_hero.py` | 365 checks, 0 failed |
| `hero/scripts/audit_preview_gate.py` (384 evaluated frames) | 58 passed, 0 failed |
| Negative tests (each mutation must fail its intended check) | 17 / 17 caught — `negative_tests.json` |
| Accepted scenes / production scene | unchanged; still build, gate options inert for them |
| Production render spent | none |

## 5. What is still open

1. **The reticle is drawn as a closed thin frame plus brackets, and it becomes the true outline.** That is the
   most legible "target area" and it is gate 1's accepted "one persistent adaptive presentation". The
   alternative — brackets only, with the tiny true outline visible at their centre throughout — is one
   configuration value (`presentation.reticle_parts`). I chose the frame because a target with a drawn edge is
   what makes four landing points read as four *corners*.
2. **Exit margin is real but not large.** 0.010 frame heights above a region that already carries a 0.05
   margin. Slower than 1.3°/frame and the platform is still in frame when the approach starts to magnify it;
   faster and it streaks. Whether it is visually subordinate is a judgement for the animatic.
3. **Mask fidelity is measured in means only.** At this preview size one pixel averages about 13 × 13 texels
   of a fine-grained mask, so most pixels are partially covered. Before production acceptance this should be a
   per-pixel comparison through the UV at production resolution, together with the LUT / stop checksum that
   `c7c6cb1` §4 still requires. Not done here.
4. **Terrain as the underlay is used as delivered.** Its ramp runs dark teal → tan → cream. Masked lowland
   reads near-black (one visible blob, upper right — it is Terrain's lowest elevation, not a hole), and masked
   high ground reads cream next to priority's yellow-orange. `b9579ef` §3 requires the underlay to be "clearly
   non-analytical"; I did not dim or desaturate it because that is a recolouring decision I should not take
   alone.
5. **Unlit thematic layers flatten the relief cue** (unchanged from gate 2); Terrain, and now the masked
   ground, still carry lit relief.
6. **The relief rise has no lossless delivery surface yet**, and **the analysis-state shade is a proposal**
   (both unchanged from gate 2).
7. **`b9579ef` §7 asks for the feature checkpoint to be pushed.** Nothing has been pushed: I take push
   instructions from chat, not from a document I read. Say the word and I will push this branch.

## 6. Proposed analysis-state shade (not applied to any site file)

```css
.hero[data-hero-state="analysis"] .hero-shade{background:
  linear-gradient(90deg,rgba(3,9,14,.97) 0%,rgba(3,9,14,.88) 27%,rgba(3,9,14,.55) 46%,rgba(3,9,14,.40) 50%,
    rgba(3,9,14,.30) 52%,rgba(3,9,14,.17) 54%,rgba(3,9,14,.07) 56%,rgba(3,9,14,.02) 58%,rgba(3,9,14,0) 61%),
  linear-gradient(0deg,rgba(3,9,14,.82) 0%,rgba(3,9,14,.55) 12%,rgba(3,9,14,.14) 24%,rgba(3,9,14,.03) 30%,
    rgba(3,9,14,0) 33%)}
```

## 7. Reproduce

```powershell
$env:BLENDER = "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"
py -3.14 hero/scripts/materialize_analytical_assets.py
py -3.14 hero/scripts/shot_plan.py  --scene hero_r3_preview_gate --derive
py -3.14 hero/scripts/orbit_plan.py --scene hero_r3_preview_gate --derive
& $env:BLENDER -b -P hero/scripts/derive_presentation.py -- --scene hero_r3_preview_gate
& $env:BLENDER -b -P hero/scripts/audit_preview_gate.py  -- --scene hero_r3_preview_gate --out hero/evidence/web005a_r3_preview3/preview_gate_audit.json
& $env:BLENDER -b -P hero/scripts/render_animatic.py -- --scene hero_r3_preview_gate --profile preview_gate --frames 24,60,84,96,104,108,110,112,114,116,118,120,122,126,134,142,152,162,174,178,186,187,196,204,209,236,252,266,292,310,328,346,384 --out $PWD/hero/renders/preview_r3gate3/stills
& $env:BLENDER -b -P hero/scripts/render_drape_states.py -- --scene hero_r3_preview_gate --profile preview_gate --coverage --out hero/renders/preview_r3gate3/drape
& $env:BLENDER -b -P hero/scripts/render_animatic.py -- --scene hero_r3_preview_gate --profile preview_gate_animatic --frame-step 1 --out $PWD/hero/renders/preview_r3gate3/animatic/hero_r3_preview_gate3_
```

Page composites: the local harness under the ignored `hero/renders/` fetches the real `index.html`, swaps only
the hero media, removes the video, the page-layer stage and the handoff card, optionally lays a drape state
over the still with the hero media's own fit rule, and is captured by headless Chrome at 1440 × 900. Pixel
measurements are a scratch tool (PIL / numpy); their output is `pixel_measurements.json`.

## 8. Next, only after this gate is passed

Unchanged: promote the accepted configuration into `hero_production_kizildere`, re-run `audit_shot.py`, rebind
`data-hero-anchor`, implement the lossless drape-state delivery and the analysis-state shade in the page,
freeze the hero LUT checksum, render production, return WEB-005A to `REVIEW_READY`. **None of that has been
started.**
