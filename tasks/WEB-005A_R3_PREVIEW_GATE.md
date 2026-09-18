# WEB-005A R3 — Preview gate: fixed-camera acquisition, scan fan, persistent lock, DEM-relief reveal

**Task:** WEB-005A / MER-107 (continuation; no new task, no new authority)
**State:** `PREVIEW_GATE_SUBMITTED` — low-cost preview evidence only. **Not** `REVIEW_READY`.
**Branch:** `feat/web-005a-hero-visual-fidelity`
**Reviewed checkpoint this answers:** `37152222c33fdc09265ba022ce45828c8d002723` (evidence `3087d2515338d9f18089b0f27983dc95c3878ebf`)

**Governing authority (`docs/web-005-polish-authority`):**

- `946cd8b5795c86cbeef52f650ee432b8fcd8fd2e:tasks/WEB-005A_R3_FIXED_CAMERA_GLOBE_DRAPE_REVISION.md`
- `db4605abcb35be9ab0337deb6b15c80aab79b12b:tasks/WEB-005A_R3_ANALYTICAL_ASSET_HANDOFF.md`
- `473b48a00bfe85d3dbe1cfe7219105c2b5ec7574:tasks/WEB-005A_R3_REVIEW_37152222.md` — §6 mandatory preview gate
- Product clarification of 2026-09-18 (scan choreography: fan + left-to-right sweep + graceful retire; adaptive
  screen-space lock frame with a continuous morph instead of a regional→analysis swap)

**What this is.** The preview gate the R3 review requires *before* another long production render. One
new scene, `hero_r3_preview_gate`, is built by the lane's own configuration-driven builder and rendered
through a new low-cost profile (`preview_gate`: Cycles 1280 × 720, 48 samples, denoised, measured 17 s/frame —
the production profile is 2304 × 1296 at 128 samples). **No production render was made.**

**What this is not.** Nothing shipped changes. `index.html`, `styles.css`, `script.js`, `assets/**`, the
production scene `hero_production_kizildere` and its shipped WebM / MP4 / poster are untouched; the site
validator is unchanged at PASS, 0 warnings. No deploy, no DNS, no merge.

---

## 1. The twelve required states

Stills: `hero/evidence/web005a_r3_preview/` (1280 × 720 renders; page composites 1440 × 900; checksums in
`preview_frames.json`).
Contact sheets: `sequence_contact_sheet.webp`, `page_1440_contact_sheet.webp`.

| # | Required state | Frame | Evidence |
| --- | --- | --- | --- |
| 1 | fixed-camera establish | 1, 24 | `01_fixed_establish_f024.webp`, `00_fixed_establish_f001.webp` (identical framing, by construction); page: `page_1440_f024.webp` |
| 2 | readable integrated-page satellite | 60 → 104 → 140 | `02_entry_f060`, `03_settle_f104`; page: `page_1440_f104.webp`, `page_1440_f140.webp` |
| 3 | four-corner beam lock | 140 | `04_beam_lock_f140.webp`; page: `page_1440_f140.webp` |
| 4 | semi-transparent scan fan | 152 | `05_scan_fan_f152.webp` |
| 5 | left-to-right sweep | 160 → 172 → 186 | `06_sweep_west_f160`, `07_sweep_mid_f172`, `08_sweep_east_f186`; page: `page_1440_f172.webp` |
| 6 | beam / fan fade-out | 202 → 208 | `09_retire_f202`, `10_retired_f208` (camera still fixed, nothing left but the lock frame); page: `page_1440_f202.webp` |
| 7 | first post-scan zoom frame | 214 | `11_first_approach_f214`; page: `page_1440_f214.webp`; lock tightening `12_approach_morph_f246`, `13_approach_morph_f270` |
| 8 | DEM relief | 316 | `14_relief_terrain_f316.webp` |
| 9 | THM-01 | 350 | `15_thm01_f350.webp` |
| 10 | ALT-01 | 378 | `16_alt01_f378.webp` |
| 11 | Score | 400 | `17_priority_f400.webp` |
| 12 | score-only final hold | 420 | `18_final_hold_f420.webp`; page: `page_1440_f420.webp` |

Motion review (local only, ignored, never site media): `hero/renders/preview_r3gate/animatic/` — the
same scene at 960 × 540 on every second frame, played back in real time (17.5 s).

## 2. Choreography (24 fps, one scene, one camera, no cut)

| Frames | Beat | Camera |
| --- | --- | --- |
| 1 – 208 | **fixed observer** | locked off: one identical state from frame 1, CONSTANT interpolation, AOI track constraint off, lens shift constant |
| 45 – 104 | platform comes round the **left limb** (hidden at the open), travels an orbital arc toward the foreground, settles left-of-centre at (0.555, 0.38) | fixed |
| 106 – 120 | four cyan sensing lines connect to the four corner anchors | fixed |
| 112 – 150 | lock frame resolves: border in, corner locks draw from the corners outward, 2.5× lock pulse, halo | fixed |
| 138 – 150 | scan fan rises between the lines | fixed |
| 148 – 194 | light curtain + ground band sweep **west → east = screen left → right** | fixed |
| 194 – 208 | fan, ground wash (194–206/208) then lines (198–208) retire; acquisition-complete pulse | fixed |
| 208 – 276 | one eased approach; the **same** lock frame tightens 544 km → 36 km | moves from 209 |
| 276 – 420 | hold, 160 km across, 36° incidence, footprint right-middle | still |
| 284 – 308 | footprint rises into DEM relief; lock frame drapes onto its rim | still |
| 284 – 398 | Terrain → THM-01 → ALT-01 → priority cross-fade on the one surface | still |
| 398 – 420 | **priority layer alone** | still |

## 3. How each review blocker is answered

**A-HERO-15 (fixed camera).** The opening camera state *is* the acquisition state: shot intent
`{"frame": 1, "mode": "hold_of", "of_frame": 208}`. The builder refuses to build if any camera channel
changes value before `fixed_through_frame`, then makes those segments CONSTANT. Measured over all 208
frames: translation 0.0 m, rotation 0.0°, focal length 0.0 mm, lens shift 0.0; first frame with any
motion is 209. What still moves before 209 is the satellite and the turning Earth — the limb
silhouette is static in every fixed frame, which is how to tell planetary rotation from a camera move.

**Integrated-page readability (A-HERO-12/13).** Measured in the built page at 1440 × 900: the widest
hero-copy line ends at 0.473 of the hero width. The pass was re-solved against the fixed camera so the
platform settles at x = 0.555; its projected silhouette never comes left of **0.490** during the
acquisition beat, is unclipped throughout, spans 12.4–12.7 % of the frame width, and drifts 2.6 % of
a frame width over 102 frames. Array yaw was re-set for this camera so the sun-tracking arrays present
about half their face instead of their edge. **No CSS, copy or gradient was changed** —
`page_1440_f140.webp` / `page_1440_f172.webp` are the real header, copy, shade and caption over the
preview frame.

**A-HERO-16 (four corners) and the scan fan.** Exactly four core lines (`aoi_beam_{nw,ne,se,sw}`),
each a constraint-derived tube from the platform to its corner anchor: worst tip error 0.7 m, root
error 0.0 m across the beat. Between them: a veil on the four pyramid faces (alpha 0 at the platform →
0.032 at the ground) and a light curtain — 48 translucent slices from the platform to a north–south
ground line, lit only near the sweep position (peak alpha 0.34, trailing 0.012). Curtain and ground band
read the *same* keyed value (measured difference 0.0), so they cross together by construction. Every
apex vertex is hooked to the platform; every ground vertex rides the Earth. The validator caps the veil
and curtain alphas so the fan cannot drift into a slab.

**Retire before zoom.** Line, fan and ground-wash presence are all 0.0 at frame 208, and on no frame in
which the camera moves is any of them above 0.0.

**Persistent lock frame (no swap).** One object on the accepted `kizildere_analysis` fixture. Each
ribbon is built at the true 36 km footprint and carries shape keys: `presented` (span), `sag_comp`
(chord sagitta, so it stays on the globe while it travels), `weight` (line weight) and `drape`. Span
and weight ramps are derived from the **evaluated** camera (`derive_presentation.py`) from a
screen-space intent. Measured: on-screen width 7.1 % → 24.3 % with a largest step of 0.38 % of a frame
width per frame; border 1.47–2.15 px and halo 8.7–12.7 px (at 1920, most foreshortened edge) across the
whole shot; lowest ribbon vertex 142 m above the sphere; settled frame 0.31 m from the true corners.

**A-HERO-17.** Settled footprint x 0.577–0.820, y 0.359–0.694 (24.3 % of the width): right-middle, clear
of the copy column.

**A-HERO-18 (real relief, one registration).** Geometry is a 600 × 600 grid displaced **only** from the
governed `top-dem.tif` (read as float32 by Blender; min/max/mean and corner cells verified identical to
rasterio), 3× presentation exaggeration (authorized band 2–4×), lift 0.13–5.04 km, referenced to the
DEM minimum so the graben floor meets the globe. Relief corners sit 0.22 m from the true corners. The
four prepared display textures are material only, share **one** UV, and are consumed byte-for-byte —
no ramp, curve or hue node touches them. Sides of the block are a cyan glass that fades to nothing at
the globe; NoData is a neutral dark surface, not a hole.

**A-HERO-19.** Final frame weights: priority 1.0, all others 0.0; priority-only hold 23 frames in this
preview timing. No detached card is part of the payoff.

## 4. Analytical asset ingest (handoff §"record the exact file checksums actually ingested")

`hero/scripts/materialize_analytical_assets.py` — copy + SHA-256 only, no processing. Record:
`hero/evidence/web005a_r3_preview/analytical_asset_ingest.json`. Export `20260917T161155Z-5e7a0e53`,
project `kizildere_mvp_v2`, config hash `c6eac560…b777c`.

| Materialized file | Use | SHA-256 |
| --- | --- | --- |
| `kizildere_top_dem.tif` | relief geometry (only) | `590f74322c6ad942e0d36b79446934da7a0938c7d87c06ab8c9bd27da73fb694` — equals the export manifest's own DEM checksum |
| `terrain_webhero_display_4k.png` | display texture | `5fdf81f525020a7c96bf09c01bb784d2a4b2bda8f959c9a7c8837c697a5c7694` |
| `thm01_webhero_display_4k.png` | display texture | `3a497c3342a52f20ee5a9d41c2c924068466431849aa425327e415619035a2df` |
| `alt01_webhero_display_4k.png` | display texture | `16ba3668a8fbeeeccec972458d2b0a6e4a3ed0489fc9f39be672638ae253ea56` |
| `priority_webhero_display_4k.png` | display texture | `bfcdec473a40558de559e59733c599b54c9cf59bad5e301e43d62417f4e89f50` |

All five are materialized under the ignored `hero/assets/source/`; none is committed. The prepared
`webhero_display_final_manifest.json` carries no checksums, so there was nothing to differ from; the
values above are what was ingested.

## 5. Decisions this preview asks Product / CTO to make

These are the places where I chose, and where a different answer changes the production render. None is
hidden in the pictures.

1. **Where the four lines end while the camera is fixed.** At the fixed camera the true 36 km footprint
   is about 8 px wide at 1920; four lines onto it read as one, and neither the fan nor a sweep across it
   is visible. So the lines lock the corners of the **presented** lock frame (544 km, 6.6 % of the
   frame), whose corners are the true footprint's corners scaled **15.1×** along the footprint's own
   diagonals (measured angular deviation 0.0005°), same centre, same 1.10° bearing, same construction.
   The lines retire before the frame begins to tighten, so no anchor ever moves while a line is
   attached, and the true corners are built as separate `aoi_true_*` anchors and audited. The true AOI
   geometry is unchanged. If Product reads "authoritative AOI corners" as *the 36 km corners, at the
   fixed camera*, the fan and sweep requirements cannot be met at this framing and the choice is a
   closer fixed camera (limb and orbital entry are lost) — `beams.anchor` is one configuration value.
2. **Delivery surface for the draped layers.** Repository invariants and the hero validator still forbid
   any governed scientific raster inside a lossy encode (`render_surface: html_overlay`). The prepared
   display PNGs are presentation-only, but THM-01 / ALT-01 / priority are still read by colour. The hold
   is genuinely still, so I recommend: video ends on the settled frame; the relief stages are delivered
   as **losslessly encoded rendered stills composited by the page** over the held frame, with the exact
   labels and mandatory EN/TR warnings as page text. The alternative — baking the reveal into the WebM —
   needs an explicit Product waiver of that invariant. The validator now fails if the *production* scene
   picks up the relief while this gate is open.
3. **Display palettes differ from the accepted public palettes.** The prepared priority display texture
   is a purple–orange–yellow ramp; the accepted GEO-WEB-002 derivative and its in-frame legend are
   `batlow`. Value-to-colour is Science-gated, so nothing was recoloured — but the page legend that
   accompanies the final hold must match whichever ramp ships. Rendering also passes the textures through
   the scene's AgX view transform and scene light (thematic layers are 62 % emissive to stay legible), so
   on-screen colour is close to, not identical to, the delivered PNG.
4. **Known bounded registration residual.** The accepted fixture places corners by spherical
   construction on a 6371 km sphere; the governed EPSG:32635 grid corners inverse-projected on WGS84 sit
   49.8–55.6 m from them (< 2 cells, 0.15 % of the span, 0.7 px at the hold). Frame, relief and all
   layers share the fixture mapping, so there is no layer-to-layer drift; the residual is common-mode.
   Left as is rather than editing accepted AOI geometry.
5. **Platform exit.** R3 parked the platform at x = 0.25, so the dive left it behind at under 17 % of the
   frame width. Parked at x = 0.555 to clear the copy, it has further to travel: it leaves lower-left
   during the approach, passes under the copy shade (x < 0.47) from about frame 220, and its centre
   crosses the bottom edge at frame 232, by which point its silhouette is roughly 0.29 frame widths
   (planned from the wingspan; the last ~0.5 s, motion-blurred). It is never in frame at the hold. If
   that reads as a fly-by in the animatic, the lever is the first 24 frames of the approach (more zoom,
   less dolly), not the acquisition composition.
6. **Shade over the payoff.** The unchanged hero shade still carries roughly a third of its strength at
   x = 0.58, so the left edge of the settled footprint is slightly dimmed on the page
   (`page_1440_f420.webp`). Not touched here; it belongs with the delivery-surface work in item 2.
7. **Duration.** This preview runs 17.5 s because it carries the whole reveal in one review animatic.
   Under recommendation 2 the shipped video would end near frame 288 (12 s, against 11.5 s today).

## 6. Gates

| Gate | Result |
| --- | --- |
| `py -3.14 scripts/validate_site.py` | PASS, 0 warnings (site untouched) |
| `py -3.14 hero/scripts/validate_hero.py` | 343 checks, 0 failed (34 new preview-gate checks) |
| `hero/scripts/audit_preview_gate.py` (420 evaluated frames) | 36 passed, 0 failed — `hero/evidence/web005a_r3_preview/preview_gate_audit.json` |
| Accepted scenes / production scene | unchanged; still build and validate |
| Production render spent | none |

## 7. Reproduce

```powershell
$env:BLENDER = "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"
py -3.14 hero/scripts/materialize_analytical_assets.py
py -3.14 hero/scripts/shot_plan.py  --scene hero_r3_preview_gate --derive
py -3.14 hero/scripts/orbit_plan.py --scene hero_r3_preview_gate --derive
& $env:BLENDER -b -P hero/scripts/derive_presentation.py -- --scene hero_r3_preview_gate
& $env:BLENDER -b -P hero/scripts/audit_preview_gate.py  -- --scene hero_r3_preview_gate --out hero/evidence/web005a_r3_preview/preview_gate_audit.json
& $env:BLENDER -b -P hero/scripts/render_animatic.py -- --scene hero_r3_preview_gate --profile preview_gate --frames 1,24,60,84,104,140,152,160,172,186,202,208,214,246,270,316,350,378,400,420 --out $PWD/hero/renders/preview_r3gate/stills
```

Page composites: a local harness under the ignored `hero/renders/` fetches the real `index.html`,
swaps only the hero media for one still and removes the video, the R3 page-layer stage and the handoff
card; captured with headless Chrome at 1440 × 900. No site file is edited to make them.

## 8. Next, only after this gate is passed

Promote the accepted configuration into `hero_production_kizildere`, re-run `audit_shot.py`, rebind
`data-hero-anchor`, implement the delivery surface Product chooses in §5.2, render production, and
return WEB-005A to `REVIEW_READY`. Nothing in that list has been started.
