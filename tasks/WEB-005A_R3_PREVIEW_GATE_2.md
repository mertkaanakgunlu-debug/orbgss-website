# WEB-005A R3 — Preview gate 2: corrected second low-cost motion preview

**Task:** WEB-005A / MER-107 (bounded continuation; no new task, no new authority)
**State:** `PREVIEW_GATE_2_SUBMITTED` — low-cost preview evidence only. **Not** `REVIEW_READY`.
**Branch:** `feat/web-005a-hero-visual-fidelity`
**Answers:** the Product decision on the first preview (`cd2018e`) plus the Product clarifications of 2026-09-18.

**Governing authority (`docs/web-005-polish-authority`):**

- `c7c6cb10e305c9de63d805c414b332440fd87ddb:tasks/WEB-005A_R3_PREVIEW_GATE_PRODUCT_DECISION.md` — continuation base
- over `946cd8b…` (fixed camera / globe drape), `db4605a…` (analytical asset handoff), `473b48a…` (R3 review)
- Product clarifications of 2026-09-18, six items: acquisition sequencing, beam draw-on, thinner line
  language, cyan / teal scan colour, no hero colour bar / no information card, timing

**What this is.** The corrected second low-cost preview that `c7c6cb1` §9 requires before any production
render. Same preview lane, same scene id (`hero_r3_preview_gate`), same low-cost profiles. The first
preview is retained as before-evidence in git at `cd2018e` and under `hero/evidence/web005a_r3_preview/`.
**No production render was made.**

**What this is not.** Nothing shipped changes. `index.html`, `styles.css`, `script.js`, `assets/**`, the
production scene `hero_production_kizildere` and its shipped WebM / MP4 / poster are untouched; the site
validator is unchanged at PASS, 0 warnings. No deploy, no DNS, no merge.

---

## 1. Deliverables

**1. Corrected animatic** — `hero/renders/preview_r3gate2/animatic/hero_r3_preview_gate2_0001-0384.mp4`
(local only, ignored, never site media; sent with this submission). 960 × 540, Cycles 32 samples, **every
frame at 24 fps** — the first gate rendered every second frame, which is too coarse to judge a 12-frame
draw-on. 384 frames, 16.0 s: 11.5 s motion + 2.75 s analytical sequence + 1.75 s priority hold.
H.264 / MP4, 4 401 045 bytes, SHA-256 `68809b5ed7b47feb67617167755867a370150debcdec6df07e1d130c926ac958`;
7.1 s/frame, 45.7 min wall clock on the workstation GPU (a production frame is 2304 × 1296 at 128 samples).
Decodes end to end with no dropped or failed frames. Its record is in `preview_frames.json` → `animatic`.
The animatic carries the whole reveal in one scene through the AgX view for motion review only; the
delivery concept for the analytical states is §3.10, not this file.

**2. 1440 × 900 real-page composites** — `hero/evidence/web005a_r3_preview2/`

| Required state | Frame | File |
| --- | --- | --- |
| beam start | 112 | `page_1440_f112_beam_start.webp` |
| full beam lock | 138 | `page_1440_f138_beam_lock.webp` |
| mid-scan | 156 | `page_1440_f156_mid_scan.webp` |
| first post-scan zoom frame | 187 | `page_1440_f187_first_zoom.webp` (the literal first frame with camera motion) |
| final priority hold | 384 | `page_1440_f384_final_priority.webp` |
| *(extra)* platform exit | 198 | `page_1440_f198_platform_exit.webp` |
| *(extra)* platform exit at the caption | 204 | `page_1440_f204_exit_caption.webp` (open item §5.2) |
| *(extra)* final hold under the unchanged shade | 384 | `page_1440_f384_current_shade.webp` (before-evidence for §3.8) |

Sheets: `page_1440_contact_sheet.webp`, `sequence_contact_sheet.webp` (27 stills),
`draw_on_detail_sheet.webp` (frames 104 → 138 at 3×: the propagation a single still cannot show),
`first_vs_second_gate_sheet.webp` (same crop, same scale, lock and mid-scan).
Stills are 1280 × 720 (`preview_gate`: 48 samples, denoised, 9 s/frame); checksums in `preview_frames.json`.

## 2. Choreography (24 fps, one scene, one camera, no cut)

| Frames | Beat | Camera |
| --- | --- | --- |
| 1 – 186 | **fixed observer** | locked off: one identical state, CONSTANT interpolation, track off, shift constant |
| 24 – 84 | satellite comes round the **left limb** and **settles** at (0.56, 0.38); measured settled at **85** | fixed |
| 86 – 102 | **aiming beat**: the platform slews 56.7° to face the target; nothing else happens | fixed |
| 106 – 124 | four lines **draw on** from the instrument aperture to the four **true** 36 km corners, staggered 2 frames (nw, ne, se, sw), 12 frames each, ease-out | fixed |
| 118 – 140 | **AOI lock**: true outline resolves on the footprint (118–126), reticle brackets draw from their corners (122–136), lock pulse (140) | fixed |
| 132 – 172 | fan rises (132–142); light curtain + ground band sweep **west → east = left → right** (140–172, 1.33 s) | fixed |
| 172 – 186 | fan and wash retire (172–184), lines release (176–186) | fixed |
| 186 – 266 | platform resumes its own pass and leaves lower-right (gone by 207); one eased approach; the **reticle** tightens continuously onto the true outline | moves from 187 |
| 266 – 384 | hold: 160 km across, 36° incidence, footprint right-middle | still |
| 276 – 342 | relief rises (276–292); Terrain → THM-01 → ALT-01 → priority cross-fade, 2.75 s | still |
| 342 – 384 | **priority alone** | still |

## 3. How each required correction is answered

Numbers are from `preview_gate_audit.json` — 384 evaluated frames, after F-curves, constraints, hooks and
shape keys — unless a pixel measurement is named.

**3.1 Acquisition sequencing (clarification 1).** The order is now a contract, proved twice. From
configuration (validator): the orbit rate is evaluated *per frame* and must be at station-keeping from
before the slew begins until the last line has released; the slew must be complete before the first line.
From the evaluated scene (audit): settled **85** ≤ slew starts **86**; slew complete **102** < first
visible line **107**; lines whole **124** ≤ lock **136** ≤ sweep **140**; retired **186**; first camera
motion **187**. The aiming beat is a real slew — boresight error falls 56.7° and is 0.0° when the first
line leaves. While any line is attached the platform's on-screen travel never exceeds 0.04 % of a frame
width per frame and the aim influence is 1.0. In the first gate the lines began at 106 while the slew ran
92 → 116; that overlap is what read as beams appearing during transitional motion.

**3.2 Draw-on (clarification 2).** The lines are fully present from their first frame and a mask along
each tube's own length does the revealing, so what is seen is propagation, never a fade; geometry — and
therefore the endpoint — stays owned by the constraints. One linear keyed value drives all four, each line
reads its own start offset, and the ease-out (fast off the platform, soft onto the corner) is applied per
line, so all four take **12 frames** and differ only in when they start. A short brighter head rides the
front. Measured: 16 % drawn on the first visible frame, largest single step 0.16, monotonic.
See `draw_on_detail_sheet.webp`.

**3.3 True governed corner endpoints (`c7c6cb1` §2).** `beams.anchor` is `true` and the validator refuses
anything else. The anchors *are* the true corners (0.0 m apart); worst line-tip error against the
`aoi_true_<corner>` empties is **0.74 m** across the beat. Nothing on the ground is drawn at presentation
size any more: scan fill, fan foot and anchors are all the governed 36 km footprint. The lines now leave the
**instrument aperture** (four rim points laid out along the footprint's own east and north, so no two lines
cross) instead of the middle of the bus.

**3.4 Reticle separated from true geometry (`c7c6cb1` §2, §9.2, §9.5).** Two different things, drawn
differently. The **true outline** (border + halo) sits on the governed corners on *every* frame of the shot
(worst 0.71 m) and only its line weight is screen-derived; while acquiring it is 0.5 % of the frame wide —
the small bright target the four lines converge on. The **reticle** is the four corner brackets only:
7.1 % of the frame while acquiring (≥ 14× the outline, so it cannot be read as the footprint), tightening
continuously during the approach (largest step 0.78 % of a frame width per frame, never widening) and
landing on the true corners (0.42 m). `20_reticle_tightening_f252.webp` shows both at once.

**3.5 Thinner line language (clarification 3).** Stated intent at 1920: outline 2.2 → **1.5 px**, halo
13 → **7 px**, brackets 4.0 → **2.4 px**, shorter bracket arms; line core radius 2.4–4.2 km → **1.5–1.9 km**
and glow sheath 4.5× → **3×**. Measured on the most foreshortened edge across the whole shot: outline
1.08–1.40 px (first gate 1.47–2.15), halo 5.1–6.8 px (8.7–12.7), brackets 1.6–2.2 px. No ribbon comes
within 185 m of the sphere.

**3.6 Scan colour (clarification 4).** Two new palette entries, used by this scene only — `scan_cyan`
#35D6E8 and `scan_teal` #1FB8B4 — replace the pale R2 FX colours on every acquisition effect, and emission
is cut to about a third: under AgX plus the frame's bloom a strong pale emitter walks to white, which is
what the first gate did. Measured on the line-core pixels of the rendered stills: first gate median
RGB (218, 237, 240), saturation **0.10**; second gate (151, 199, 206), hue 188°, saturation **0.27**. The
curtain is dimmer than the lines it supports (validator-enforced) and peaks at alpha 0.30. One thing worth
knowing: a faint veil has to stay *brighter* than sunlit desert, because an alpha mix replaces a fraction of
what is behind it — a darker teal printed a grey wedge across North Africa until that was corrected.
Over open sea the fan reads cyan; over the Sahara it necessarily reads paler.

**3.7 Broad fan, true foot (`c7c6cb1` §2).** The fan's upper edge is a 380 × 44 km rectangle on the
aperture, long along the sweep axis; its foot is the governed footprint. The curtain crosses from its west
face to its east face, so the sweep travels about 5 % of the frame width aloft while it travels 0.5 % on the
ground. Curtain and ground band still read one keyed value (difference 0.0).

**3.8 No hero colour bar, no information card (clarification 5); analysis-safe shade (`c7c6cb1` §7).** The
scene renders no legend, colour bar or card (validator-enforced), and the page composites carry none: the
harness removes the page-layer stage with its legend and the handoff card. The only text over the hero is
the existing bare bottom-right caption, unchanged. The final composite uses a **proposed** state-shifted
shade (exact CSS in `hero/renders/preview_r3gate2/composite.html`, reproduced in §6): identical to the
shipped shade behind the copy column (x ≤ 0.48) and in the caption band (y ≤ 0.12), feathered to nothing
over 0.50–0.61 before the footprint begins at 0.577. Measured on the 1440 × 900 composites against an
unshaded capture: the shipped shade leaves the footprint's left 60 px at **70 %** luminance and the whole
footprint at 83 %; the proposed shade leaves them at **99.4 %** and **99.9 %** (largest difference 5 / 255).

**3.9 Bounded satellite exit (`c7c6cb1` §6).** Zooming about the AOI cannot meet the bound, with any
lens / dolly split: the platform's silhouette would need about 3.5× magnification before it cleared the
frame, which is 44 % of the frame width. So the exit is the platform's own motion: at the release frame it
resumes its pass (0.015 → 2.3° of arc per frame over 18 frames) and leaves lower-right, while the approach
starts almost purely optically (1.23× by frame 210). Measured on the *whole* projected silhouette, on every
frame in which any of it is in frame: widest **18.8 %** at frame 206 (bound 22 %; first gate about 29 % and
growing), out of frame from **207**, never re-enters. Acquisition position and readability are unchanged
(x ≥ 0.498 against the 0.475 copy edge, 12.7 % wide, unclipped).

**3.10 Lossless drape states and colour fidelity (`c7c6cb1` §3–4).** `hero/scripts/render_drape_states.py`
renders each analytical state on its own from the same build and held camera: relief only, transparent film,
RGBA PNG, **Standard** view transform, crisp frame lines as holdouts. THM-01, ALT-01 and priority are now
fully emissive, so scene light no longer re-authors thematic colour; only Terrain, which is context, takes
light. The final-hold composite is that lossless priority state laid over the held frame by the page, with
the same fit rule as the hero media. Indicative colour check (`pixel_measurements.json`): **99.96–100 %** of
the overlay's interior pixels fall inside the delivered texture's own colour set (modelled with the
material's compositing rule, ±8 / 255); the same pixels in the AgX scene render: 66 %. This is a membership
test, not a per-pixel ΔE — see §5.3.

**3.11 Timing (clarification 6, `c7c6cb1` §8).** Motion section **11.5 s** (frames 1–276), analytical
sequence **2.75 s**, sweep **1.33 s** (first gate 1.92 s), priority hold 1.79 s in this animatic. The
validator ties the layer ramps to the declared window so they cannot drift apart.

**Preserved from the accepted first-gate findings (`c7c6cb1` §1), re-measured:** fixed observer (0.0 m,
0.0°, 0.0 mm, 0.0 shift over 186 frames); retirement before motion; one persistent adaptive presentation;
relief from the governed `top-dem.tif` only, 3×, one UV (corners 0.46 m from true); Terrain → THM-01 →
ALT-01 → priority; priority-only final hold (43 frames); governed-grid residual 49.8–55.6 m, accepted.

## 4. Gates

| Gate | Result |
| --- | --- |
| `py -3.14 scripts/validate_site.py` | PASS, 0 warnings (site untouched) |
| `py -3.14 hero/scripts/validate_hero.py` | 359 checks, 0 failed (16 new gate-2 checks) |
| `hero/scripts/audit_preview_gate.py` (384 evaluated frames) | 52 passed, 0 failed — `preview_gate_audit.json` |
| Negative tests (each mutation must fail the validator) | 11 / 11 caught — `negative_tests.json` |
| Accepted scenes / production scene | unchanged; still build and validate |
| Production render spent | none |

One negative test earned its keep: "platform resumes its pass while lines are attached" was first caught
only by an unrelated keyframe-drift check, because the station-keeping rule looked at rate-profile *keys*
and a ramp that starts early has no key inside the window. The rule now evaluates the rate per frame.

## 5. What I would want Product / CTO to look at, and what is still open

1. **Four lines at true scale are a slender bundle.** At the fixed camera the governed footprint is 9 px of a
   1920 frame. Four lines from a 44 km aperture to four corners 36 km apart are, truthfully, near-parallel:
   they read as four at the platform and converge to the target. That is the geometry `c7c6cb1` §2 asks for,
   and the reticle and the fan carry the readability. If the animatic reads as "one beam", the honest lever
   is the emitter spread on the platform (`beams.emitter.half_side_km`), never the ground end. The fan is
   deliberately quiet now (`first_vs_second_gate_sheet.webp` shows how far it moved); if it reads as too
   quiet in motion, the levers are `scan_fan.top.half_length_km` and the curtain's `band_alpha`, both still
   well inside the validator's caps.
2. **The exit crosses the lower right.** The platform leaves along its own orbit, so it passes below the
   target and out through the bottom-right corner in about 0.9 s. At frame 204 it is a heavily
   motion-blurred dark streak that touches the right end of the bottom-right caption
   (`page_1440_f204_exit_caption.webp`); the caption stays legible because the streak is dark, but the
   ≥ 4.5 : 1 caption rule has not been measured on those frames. It is physically the natural read ("the pass
   continues") and it is what bounds the exit; whether it is visually subordinate to the AOI transition is a
   motion judgement for the animatic. If the caption contact matters, the lever is the orbit heading (so the
   platform leaves through the right edge above the caption band); not tried, because it re-solves the
   accepted acquisition position.
3. **Colour check is indicative.** The membership test shows the Standard-view lossless path stays on the
   delivered palette and the AgX path does not. Before production acceptance it should become a per-pixel
   comparison through the UV, and `c7c6cb1` §4 still requires the exact ordered stops / LUT checksum frozen in
   the derivative build manifest — not done here. **Finding:** the prepared ALT-01 and priority textures
   carry a feathered alpha mask (≈ 9 % transparent, ≈ 16 % partial). The relief material blends those texels
   toward the declared NoData neutral, which is why parts of the priority surface read dark. Whether masked
   ground should show the neutral or the Terrain layer beneath is a presentation decision I have not taken.
4. **Unlit thematic layers flatten the relief cue.** With scene light removed from THM-01 / ALT-01 / priority
   (as §4 of the decision requires) the DEM reads through silhouette, walls and perspective, not through
   shading. Terrain, the first state, still carries the lit relief.
5. **No hero legend supersedes part of `c7c6cb1`.** Clarification 5 makes §4's "regenerate the hero legend"
   moot for the hero, and §3.6's "labels, warnings and legend remain page content" now means below-the-fold
   content. The repository invariant that every *proof panel* carries its mandatory warning is unaffected
   (Act 4 carries it), but the hero now shows the priority surface with no label. If Product wants one, the
   conforming place is the existing bare caption's third line at the final state — not implemented, site
   files untouched.
6. **The relief rise has no delivery surface yet.** In the animatic the block rises geometrically (276–292).
   Under lossless page delivery that is either a dissolve into the raised Terrain state or a short lossless
   sequence; it sits inside the 2.75 s budget either way.
7. **The proposed shade is a proposal.** It is injected by the harness only. Caption-band contrast is
   unchanged by construction, but the ≥ 4.5 : 1 measurement at 375 / 768 / 1024 / 1440 belongs with the
   integration, as does the 900-px breakpoint shade, which this does not touch.

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
& $env:BLENDER -b -P hero/scripts/audit_preview_gate.py  -- --scene hero_r3_preview_gate --out hero/evidence/web005a_r3_preview2/preview_gate_audit.json
& $env:BLENDER -b -P hero/scripts/render_animatic.py -- --scene hero_r3_preview_gate --profile preview_gate --frames 24,56,84,96,104,110,112,116,120,124,138,146,156,166,180,186,187,198,206,236,252,266,292,310,328,346,384 --out $PWD/hero/renders/preview_r3gate2/stills
& $env:BLENDER -b -P hero/scripts/render_drape_states.py -- --scene hero_r3_preview_gate --profile preview_gate --out hero/renders/preview_r3gate2/drape
& $env:BLENDER -b -P hero/scripts/render_animatic.py -- --scene hero_r3_preview_gate --profile preview_gate_animatic --frame-step 1 --out $PWD/hero/renders/preview_r3gate2/animatic/hero_r3_preview_gate2_
```

Page composites: the local harness under the ignored `hero/renders/` fetches the real `index.html`, swaps
only the hero media, removes the video, the page-layer stage and the handoff card, optionally lays a drape
state over the still with the hero media's own fit rule, and is captured by headless Chrome at 1440 × 900.
Pixel measurements are a scratch tool run with PIL / numpy against those files; their output is
`pixel_measurements.json`.

## 8. Next, only after this gate is passed

Unchanged from the first gate: promote the accepted configuration into `hero_production_kizildere`, re-run
`audit_shot.py`, rebind `data-hero-anchor`, implement the lossless drape-state delivery and the
analysis-state shade in the page, freeze the hero LUT checksum, render production, and return WEB-005A to
`REVIEW_READY`. **None of that has been started.**
