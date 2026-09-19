# WEB-005A — Final production hero and homepage integration

**Task:** WEB-005A / MER-107 (final production continuation; no new task, no re-plan)
**State:** `REVIEW_READY` — final production evidence for Product review. Not merged, not deployed, no DNS.
**Branch:** `feat/web-005a-hero-visual-fidelity`

**Governing authority (`docs/web-005-polish-authority`):** `946cd8b…` (fixed camera / globe drape),
`db4605a…` (analytical asset handoff), `c7c6cb1…` (decision on preview gate 1), `b9579ef…` (decision on
preview gate 2), and the chat-level final visual direction of 2026-09-19: move Preview Gate 3 to production
quality, preserve its storytelling, strong right-side analytical payoff, clean left copy-safe area, prepared 4K
assets, no colour bar / legend / card / layer title in the hero. The branch was fetched at the start of this
pass; `b9579ef` is still its head. (`b9579ef` §1 predates the visual review that put the visible lines on a
presentation reticle; this pass follows the later chat direction, as gate 3 did.)

---

## 1. What was produced

### 1.1 Motion video and poster — `assets/hero/` (lossy, no analytical pixel)

| File | Codec | Size | Ceiling | SHA-256 |
| --- | --- | --- | --- | --- |
| `assets/hero/orbgss-hero.webm` | VP9, 991 kbps, 1920 × 1080, 276 frames / 11.5 s | 2.83 MiB | 3.0 MiB | `5907372ab5aea646dda9a33f5f6c473e817717aa1226a54df164c407b6ac6ddd` |
| `assets/hero/orbgss-hero.mp4` | H.264, 2800 kbps, 1920 × 1080, 276 frames / 11.5 s | 4.05 MiB | 4.5 MiB | `9180cbd1011147d74095793cd0cfe91a79744b77ad63ae8e51b636854b931ad5` |
| `assets/hero/hero-poster-1600.webp` | WebP (lossy) q82, 1600 × 900, frame 276 | 117.9 KiB | 180 KiB | `389f2338f5a31faa3b87c1669544e29b4418ac0fe4c6306074288882ee96066f` |
| `assets/hero/hero-poster-900.webp` | WebP (lossy) q88, 900 × 506, frame 276 | 68.2 KiB | 180 KiB | `11818a638533b715bd62987b1cedd26c7b2bce5104144181cdd718d80b9b6964` |

Scene `hero_production_kizildere`, profile `production`: Cycles, 2304 × 1296, 128 adaptive samples (threshold
0.01), OptiX denoise, half-frame motion-blur shutter, delivered at 1920 × 1080 (1.44× supersampled), frames
**1–276** (11.5 s at 24 fps). Render: pass 1, all 276 frames, 5.25 h; pass 2, frames 24–216 re-rendered after the black-line defect (§2.1), 4.96 h; pass 3, frames 217–224 and 238–243, 0.21 h — 10.4 h in all on the workstation GPU, Blender 4.5.10 LTS (`hero/renders/production/render_record_pass1/2/3.json`, ignored directory). The delivered frames are 1–23, 225–237 and 244–276 from pass 1 (proved untouched by the defect), the rest from passes 2 and 3. Record: `hero/evidence/production_media.json`.

### 1.2 Analytical drape states — `assets/hero/drape/` (lossless, page-composited)

| State | File | Rendered frame | Size | SHA-256 |
| --- | --- | --- | --- | --- |
| terrain | `assets/hero/drape/hero-drape-terrain-1920.png` | 292 | 866.1 KiB | `f5469c1e906e432977640cbde4c56d7f7713f3a83fa47a4cc524d3782c514fb9` |
| thm01 | `assets/hero/drape/hero-drape-thm01-1920.png` | 306 | 946.8 KiB | `510442f9332359d8143ea99405b48d906d6e21d564952201e1201554a27ba2e8` |
| alt01 | `assets/hero/drape/hero-drape-alt01-1920.png` | 324 | 931.4 KiB | `92154136ffbeed51133e525da3056f624660adad71f0fcc1ec4d69be64ac209c` |
| priority | `assets/hero/drape/hero-drape-priority-1920.png` | 384 | 952.1 KiB | `a71336c2f7db01ff5163f3e8ec6f8688ef76f6203c9c4f7e3a51ec85c3bfc510` |

Profile `production_drape`: the delivered 1920 × 1080 (no resample against the video), 384 fixed samples, **no
denoiser** (a denoiser is a colour filter), `Standard` view, transparent film, 8-bit RGBA PNG. Two passes that
never share a pixel's colour: the data surface through the Standard view; outline, halo, brackets and the
block's glass sides through the scene's own view so they keep the look they have in the video. A third pass
holds the block's **contact shadow** alone (ground as shadow catcher, block invisible to the camera) and goes
*under* each state: the motion render ends before the block exists, so its held frame has no shadow for it, and
without one the block sat on the page like a sticker (found by comparing the first page composite with the
accepted gate-3 hold). No data pixel is touched by either effects pass. Records:
`hero/evidence/production_drape_states.json`, `assets/imagery/sources.json → web_005.hero_drape_states`.

### 1.3 The exact 4K analytical assets used

Prepared display set `C:\Projects\geothermal-prospectivity\outputs\webhero_display_final`, governed export
`kizildere_mvp_v2 / 20260917T161155Z-5e7a0e53`, ingested by copy + SHA-256 only
(`hero/evidence/web005a_r3_preview/analytical_asset_ingest.json`); the packager refuses a texture whose
checksum differs from ingest.

| Use | File (4096 × 4096 unless noted) | SHA-256 |
| --- | --- | --- |
| relief geometry only | `kizildere_top_dem.tif` (governed float32 DEM, 1200 × 1200) | `590f74322c6ad942e0d36b79446934da7a0938c7d87c06ab8c9bd27da73fb694` |
| Terrain state; underlay for masked support | `terrain_webhero_display_4k.png` | `5fdf81f525020a7c96bf09c01bb784d2a4b2bda8f959c9a7c8837c697a5c7694` |
| THM-01 state | `thm01_webhero_display_4k.png` | `3a497c3342a52f20ee5a9d41c2c924068466431849aa425327e415619035a2df` |
| ALT-01 state | `alt01_webhero_display_4k.png` | `16ba3668a8fbeeeccec972458d2b0a6e4a3ed0489fc9f39be672638ae253ea56` |
| Priority state (final hold) | `priority_webhero_display_4k.png` | `bfcdec473a40558de559e59733c599b54c9cf59bad5e301e43d62417f4e89f50` |

No low-resolution substitute and no simplified panel: the relief is one vertex per governed DEM cell
(1200 × 1200), the textures are consumed byte for byte, and nothing recolours them.

## 2. Narrative contract — preserved from preview gate 3, measured on the production scene

`hero/evidence/shot_audit_production.json` — 59/59 checks pass over 384 evaluated frames.

| # | Beat | Frames | Measured |
| --- | --- | --- | --- |
| 1 | Earth establish, fixed observer | 1–186 | camera translation, rotation, focal length, lens shift: 0.0 |
| 2 | Satellite entry and settle | 24–84 | settled 85; slew 86–102 (56.8°, ends on target) |
| 3 | Reticle legible over the target first | 98–114 | 0.67 of locked brightness, brackets 71 % drawn when the first line leaves (109) |
| 4 | Four lines land on four reticle corners | 108–126 | 12 frames each, staggered; tip error 0.7 m; anchors static while attached |
| 5 | Cyan fan between the lines | 126–136 | fan top = aperture square, foot = reticle |
| 6 | Left-to-right sweep, camera fixed | 136–168 | curtain foot crosses 6.4 % of the frame width, monotonic |
| 7 | Lines / fan retire | 168–178 | all 0.0 by 178 |
| 8 | Zoom only then | 187 → 266 | platform exits right edge, silhouette ≤ 19.3 % (bound 22 %), zero frames in the caption region |
| 9 | Settle on the analysis area | 266–276 | reticle lands 0.42 m from the true 36 km corners; **hold still by construction** |
| 10 | Terrain → THM-01 → ALT-01 → Priority | page, 2.7 s | four lossless states, 750 ms apart, 450 ms cross-fade |
| 11 | Priority hold on terrain/context | page | priority state alone; Terrain through masked support |

**One production defect found and fixed.** The single-render previews could not show it: during the
"still" hold the true footprint wandered **6.1 px** at 1920 (camera keys chasing a turning Earth move on a chord
while the ground moves on an arc). With page-composited states that is a registration jump. The hold is now
still by construction — Earth rotation and camera state frozen from the settle frame — and the audit proves
**0.0 px** between the frame the video ends on and any frame a state is rendered at.

Production-only polish, none of it choreography: relief grid 600 → 1200 (one vertex per DEM cell), beam tube
24 sides, 96 curtain slices, line emission 2.8 → 3.0 (the lane's own legibility floor), orbit tail eased to the
station-keeping crawl instead of zero (an orbit does not stop).

### 2.1 Defect found on first viewing, fixed and re-rendered

The first final render (`92745527`) was declared review-ready and was **not**: on first viewing the owner saw a line
leave the platform before it had settled and a band sweep across the frame while it left. Confirmed in the frames: a
**black line from the platform to a reticle corner** at f72, f100–112 and f180, and a thick dark band during the exit
at f208–219. Cause: the scan fan went from 64 to 96 slices for production under an unchanged
`transparent_max_bounces` of 96. A view ray that crosses the whole slice stack plus a line tube exhausts the budget
and Cycles ends the path black — *whether or not the slices are visible*, so it showed exactly when no effect should
exist. The choreography was right; invisible geometry printed black.

- Proved by A/B on the same frames and seed (budget 96 vs 512): the line disappears, nothing else changes.
- Budget is now 512; `validate_hero.py` requires at least 2 × slices + 64; a negative test breaks it on purpose.
- Frames 24–216 re-rendered; frames 1–23 and 217–276 A/B-checked at low resolution, and the few that differed
  (217–220, 239, 242) re-rendered with margin (217–224, 238–243). The rest differ by exactly 0.
- Why it was missed: the audit measures keyed values, not pixels, and I checked six beats instead of the sequence.
  The re-render was checked every 4th frame **before** encoding (`sequence_check_*.webp`).
- `REVIEW_READY` was withdrawn in `STATUS.md` at `99b7e25` for the duration. Drape states and page integration were
  never affected.

## 3. Page integration (desktop)

- **Architecture, explicit.** The video carries the motion and ends on the held frame (also the poster). The
  analytical reveal is four full-frame lossless images in the hero media's own box with the same
  `object-fit` / `object-position` as the poster, so they register at every hero size with no placement maths.
  The R3 CSS-homography stage, its legend, the floating handoff card, ledger, labels and warnings are **removed
  from the hero**; Acts 3 and 4 keep the exact public labels, mandatory EN/TR warnings and legend.
- **Copy-safe left, payoff right.** One shade element whose gradient stops are registered custom properties,
  so the gradient itself transitions: identical to the shipped shade behind the copy (x ≤ 46 %) and in the
  caption band (y ≤ 12 %), clear over the footprint (x 57.6–82.1 %). No mid-fade lightening behind the copy.
- **Static states** (reduced motion, Save-Data, slow network, autoplay blocked, stalled playback) show the
  priority state at once and never fetch the three transitional states (`data-src`). A stalled playback falls
  back to the poster first, because the states register with the held frame only. No-JS shows the priority
  state through a `<noscript>` rule.
- **Below 981 px the drape stays off** and the hero ends on the held frame: the copy spans the frame there and
  a bright surface behind it would cost the copy its contrast. Narrow crops are re-biased (79 %) to keep the
  outline whole.
- Only the existing bottom-right rendered-sequence caption remains over the hero, unchanged.
- **Motion path verified with the delivered media**, not only the static states: the real page was played in real
  time in headless Chrome (autoplay, no reduced motion). Logged: WebM selected, the four states warmed during
  playback, video ended at 11.5 s, `data-hero-state="held"`, `data-hero-payoff="on"`, then Terrain → THM-01 →
  ALT-01 → Priority with each outgoing state dropped, ending on Priority alone.

Evidence, `hero/evidence/web005a_final/`:

- `contact_sheet_motion_beats_1440.webp` — eight production frames under the real 1440 × 900 page chrome: reticle before any line (104), first line (114), four-corner lock (134), mid-scan (152), first zoom frame (187), platform exit (210), approach (230), held frame the video ends on (276)
- `page_1440_f104_… / f114_… / f134_… / f152_… / f187_… / f210_… / f230_… / f276_….webp` — the same eight, full size (harness: real `index.html` + `styles.css`, hero media swapped for the production still)
- `defect_black_line_before_after.webp` — §2.1: the black line / dark band of the first render beside the re-render, frames 72, 108, 180, 210, 217
- `sequence_check_f072_f132 / f134_f162 / f164_f224_every_4th.webp` — dense check of the re-rendered frames, every 4th frame: settle → slew → reticle → draw-on → fan → sweep → retire → exit, no stray line anywhere
- `transparent_budget_ab_detection.json` — frames 1–23 and 217–276 rendered twice (budget 96 vs 512, same seed); all but 217–220, 239 and 242 differ by exactly 0
- `contact_sheet_analytical_reveal_1440.webp` — REAL page, the four states in order: Terrain → THM-01 → ALT-01 → Priority
- `real_1440_terrain / thm01 / alt01.webp` — REAL page, each transitional state (static state + `#hero-layer=` review hook)
- `real_1440_priority_final_hold.webp` — REAL page, final priority hold, 1440 × 900 — **the primary desktop review image**
- `real_1920_priority_final_hold.webp` — REAL page, final priority hold, 1920 × 1080
- `real_1440_priority_final_hold_tr.webp` — REAL page, Turkish: the three-line headline still clears the payoff
- `real_1440_motion_path_after_playback.webp` — REAL page after the WebM played in real time in headless Chrome: video ended at 11.5 s → `held` → Terrain → THM-01 → ALT-01 → Priority, settled on Priority alone
- `real_390_mobile_held_frame.webp` — REAL page at 390 px: held frame with the outline whole, no drape fetched
- `handoff_native_1920_held_terrain_thm01_alt01_priority.webp` — native-resolution crop of the footprint: held frame, then each delivered state over it
- `page_registration_measurements.json` — static path vs motion path on the real page: footprint differs by 0.24 / 255 (same lossless pixels), surround by 2.5 / 255 (WebM vs WebP of the same frame)
- `drape_pixel_measurements.json` — colour path and mask of the delivered states

## 4. Validators and audits

| Gate | Result |
| --- | --- |
| `py -3.14 scripts/validate_site.py` | PASS, 0 warnings |
| `py -3.14 hero/scripts/validate_hero.py` | 418 checks, 0 failed |
| production audit (`audit_preview_gate.py --scene hero_production_kizildere`) | 59/59 checks pass |
| `py -3.14 scripts/negative_tests_web005.py` | 47/47 deliberate regressions caught; tree restored byte-identical (`negative_tests.txt`) |
| drape colour path (`drape_pixel_measurements.json`) | 99.99–100 % of fully covered pixels inside the delivered texture's own colour set (THM-01 / ALT-01 / priority) |
| drape mask | rendered mean analytical coverage 0.850 (priority), 0.854 (ALT-01) vs delivered texture mean alpha 0.834, 0.840 — perspective-weighted, indicative |

The site validator's hero contract was rewritten for the accepted delivery: exact four states in order, each
a recorded lossless 8-bit RGBA PNG at 1920 × 1080 tied to its ingested 4K texture, transitional states
deferred, fit rule shared with the poster, anchor matching the production audit — and it **fails if a legend,
label, warning, ledger or card returns to the hero**. The hero validator now runs the preview-gate contract on
the production scene, requires the gate alias to be the production scene unchanged, and requires the lossy
motion render to end before any analytical pixel exists. Superseded two-frame R3 rules were retired, not
weakened.

## 5. For Product's attention

1. **Payload.** Four lossless states are 3.61 MiB in total, fetched only on the desktop layout and only
   once motion plays; a static desktop visitor fetches the priority state alone. Lossless is the rule, so the
   lever would be delivery size, not compression.
2. **Below 981 px there is no analytical payoff in the hero** (no card is allowed and the copy owns the frame).
3. **Terrain underlay is used as delivered**: masked lowland reads near-black and masked high ground reads
   cream beside priority's yellow. Dimming it would be a recolouring decision.
4. **Class-B 1249 px ceiling.** These are MER-108 hero display derivatives (4096 px), not GEO-WEB-002 class-B
   exports, so the ceiling was not applied. For the record: the footprint is 24.4 % of the hero width and would
   pass 1249 device px only on a hero wider than about 5130 device px.
5. **Outline height.** In the states the outline rides on the raised block, a few pixels above the ground-level
   outline of the held frame, which stays visible as the block's base edge inside its shadow. In the gate-3 single
   render the one outline rose with the block; on the page the ground one remains. It reads as a slab with a base.
6. **WebM bitrate.** The 3.0 MiB ceiling and the encoder's own bitrate search put VP9 at 991 kbps (2.83 MiB) for
   11.5 s of 1080p (H.264 fallback: 2800 kbps, 4.05 MiB). Fine on the dark, slow frames; the fastest approach
   frames are where it would show first.
7. **`b9579ef` §7 asks for a push.** Nothing has been pushed; I take push instructions from chat.
8. **Local capture note.** Headless captures against the local Python server occasionally dropped the poster
   request (the page then hides the failed image by design, WEB-004); such captures were retaken. It is a
   dev-server artefact, not a page state.

## 6. Reproduce

```powershell
$env:BLENDER = "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"
py -3.14 hero/scripts/materialize_analytical_assets.py
py -3.14 hero/scripts/shot_plan.py  --scene hero_production_kizildere --derive
py -3.14 hero/scripts/orbit_plan.py --scene hero_production_kizildere --derive
& $env:BLENDER -b -P hero/scripts/derive_presentation.py -- --scene hero_production_kizildere
& $env:BLENDER -b -P hero/scripts/audit_preview_gate.py  -- --scene hero_production_kizildere --out hero/evidence/shot_audit_production.json
& $env:BLENDER -b -P hero/scripts/render_animatic.py -- --scene hero_production_kizildere --profile production --frames (1..276 -join ',') --out $PWD/hero/renders/production/frame.png
& $env:BLENDER -b -P hero/scripts/encode_production_media.py -- --scene hero_production_kizildere --width 1920 --height 1080
& $env:BLENDER -b -P hero/scripts/render_drape_states.py -- --scene hero_production_kizildere --profile production_drape --coverage --frame-lines --ground-shadow --out hero/renders/production/drape
py -3.14 hero/scripts/package_drape_states.py
```
