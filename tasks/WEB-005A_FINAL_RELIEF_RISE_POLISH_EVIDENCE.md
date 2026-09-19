# WEB-005A — Final relief-rise polish and startup-poster continuity

**Task:** WEB-005A / MER-107 (bounded final polish; no new task, no re-choreography)
**State:** `REVIEW_READY` — polish evidence for Product review. Not merged, not deployed, no DNS.
**Branch:** `feat/web-005a-hero-visual-fidelity`
**Base:** `e7098de8f05dfb3842620bbb578227d5c0bc2699` (accepted final visual base, published)

**Authority (`docs/web-005-polish-authority`, fetched at the start of this pass):**
`1437fbb…:tasks/WEB-005A_FINAL_PRODUCT_VISUAL_REVIEW_E7098DE.md` (startup-poster continuity) and
`0e876754e121b355426f71bd76f17d9aa81e9947:tasks/WEB-005A_FINAL_RELIEF_RISE_POLISH.md` (relief rise).

**Not touched:** the 276-frame motion render, both encodes, the held-frame posters and the four drape states are
byte for byte what was accepted at `e7098de` (checksums re-verified before and after). No camera, choreography,
asset, DEM exaggeration, palette or final-hold change.

---

## 1. Relief rise

The page used to jump from the flat held frame to the fully raised Terrain state. It now shows the DEM relief
**rising out of the ground**, with the outline, the glass sides and the contact shadow rising with it.

- **What was rendered.** Only the held-camera rise interval of the accepted production scene: its own frames
  **278, 280, 282, 284, 286, 288, 290**, strictly inside the scene's relief-rise keys (276 → 292, eased by the
  scene). `render_drape_states.py --rise-only`: same camera, governed DEM, mapping, 3× exaggeration and
  `production_drape` profile as a drape state (1920 × 1080, 384 fixed samples, no denoiser, `Standard` view). The
  effects pass and the contact-shadow pass are rendered **per frame**, which is what makes the outline rise with
  the same geometry (it rides the same `drape` shape key, from the same DEM samples, on the same keys).
- **Duration.** 16 frames at 24 fps = **0.667 s** (authorized 0.45–0.70 s). Terrain then dwells exactly as long
  as before (300 ms) and THM-01 → ALT-01 → Priority keep their 750 ms / 450 ms cadence. Measured on the real
  page: payoff on at 11.07 s, Terrain standing alone at 11.75 s, THM-01 12.03 s, ALT-01 12.85 s, Priority
  13.53 s, Priority alone 14.15 s. The whole reveal is about 0.2 s longer than it was.
- **How the page plays it.** Keyframes are *nothing (held frame) → the seven states → Terrain*. On a
  `requestAnimationFrame` clock the two neighbouring keyframes are shown at opacities (1 − p) and p inside an
  isolated group with `mix-blend-mode: plus-lighter`, which is an exact linear interpolation of two partly
  transparent images (a plain cross-fade dips in the middle). Every displayed frame is therefore a blend of two
  *rendered geometry states* two scene frames apart — not a scale or an opacity trick on one image. Where
  `plus-lighter` is unsupported the nearest state is shown whole (a flipbook). If the states are not decoded when
  the hold arrives, the previous accepted cross-fade runs instead.
- **Lossless, and proved.** Shipped as lossless WebP (VP8L). At write time each file's alpha and every visible
  pixel's RGB are read back and must equal the composited PNG exactly, or the render fails. The same pixels as PNG
  would be 6.08 MB; as lossless WebP they are **1,580,834 bytes (1.51 MiB)**.
- **Who pays for it.** Desktop layout, motion path only: `data-src`, fetched while the video plays (11 s of
  head-room). Verified on the real page: reduced-motion and slow-network visitors keep all seven deferred, as do
  phones.

| Scene frame | File | Bytes | SHA-256 |
| --- | --- | --- | --- |
| 278 | `assets/hero/drape/hero-rise-f278-1920.webp` | 216,146 | `dcd37bd9eee6bd2c886f89bd623302124c3bf3549f139f18819795cb938c656d` |
| 280 | `assets/hero/drape/hero-rise-f280-1920.webp` | 217,518 | `9898cef91f493a6091d80e69807fc1f71360223c74c5a7bb791db241ad648bac` |
| 282 | `assets/hero/drape/hero-rise-f282-1920.webp` | 223,158 | `6682675ccc834912e3cbc3f02663deb6f2bebf8d2c3d8113cf1a95dce8366fc4` |
| 284 | `assets/hero/drape/hero-rise-f284-1920.webp` | 229,950 | `f03e932ad630e717918efefd2bc656457b5120a5312a47f2197ad298171c35c3` |
| 286 | `assets/hero/drape/hero-rise-f286-1920.webp` | 234,600 | `da561e66898920738cb0eb94806e68971266fdd6ca6363c5c402934f1fdade13` |
| 288 | `assets/hero/drape/hero-rise-f288-1920.webp` | 227,644 | `723b978ecf12426d911921feddf451f22f0c81c688ee507d59b2c2d41d247125` |
| 290 | `assets/hero/drape/hero-rise-f290-1920.webp` | 231,818 | `83d8a8d6d510a099e9e0a3fd044c8b2e0daed93479081381caaf6e499724acf6` |

**Incremental payload: 1,580,834 bytes (1.51 MiB) in 7 files**, plus the startup poster below.
Records: `hero/evidence/production_relief_rise.json`, `assets/imagery/sources.json → web_005.hero_relief_rise`.

## 2. Startup-poster continuity

The poster used to be the held frame, so a visitor saw *held target → Earth establish → acquisition* for the
first ~0.3 s. The startup poster and the held base are now two stills with two jobs.

| Role | File | Frame | Bytes | SHA-256 |
| --- | --- | --- | --- | --- |
| startup poster (`hero-poster-opening`), **new** | `assets/hero/hero-opening-1600.webp` | 1 | 117,528 | `dc22358e31880407a68429b134cdfead1637f24b66ef960e970b1d43dc960c98` |
| held base (`hero-poster`), unchanged | `assets/hero/hero-poster-1600.webp` | 276 | 120,764 | `389f2338f5a31faa3b87c1669544e29b4418ac0fe4c6306074288882ee96066f` |
| held base, narrow (`hero-poster-narrow`), unchanged | `assets/hero/hero-poster-900.webp` | 276 | 69,796 | `11818a638533b715bd62987b1cedd26c7b2bce5104144181cdd718d80b9b6964` |

- The startup poster is derived from the accepted frame 1 (`encode_production_media.py --opening-poster-only`,
  WebP q88, 114.8 KiB of the 180 KiB ceiling). No encode was re-run.
- `<picture>`: where the motion never plays — `(prefers-reduced-motion: reduce), (max-width: 780px)` — the source
  swaps in the held frame, which is what those visitors end on; everyone else gets the opening frame. The two
  `preload` links carry exactly those two complementary media queries, so each visitor preloads one still.
- **Held base** (`img[data-hero-held]`, `data-src`): every static state — Save-Data, slow network, autoplay
  blocked, stalled or failed playback — lays it over the startup poster *before* the payoff appears, and shows no
  payoff if it cannot load. The Priority state is never composited on the opening Earth. A visitor whose motion
  plays never fetches it (their video ends on that frame). `<noscript>` carries a held base under the payoff.
- Cost, stated plainly: a desktop visitor on Save-Data / slow network now fetches two stills (opening 115 KiB +
  held 118 KiB) where they fetched one. Reduced-motion and phone visitors still fetch one.

## 3. Evidence — `hero/evidence/web005a_final/`

- **`web005a_relief_rise_playback_1440x900.mp4`** (delivered with this report; kept out of git, 5.4 MB,
  SHA-256 `1fb5c60d63301b5599d4e013af10633b1af281bffd1c1064d47c2bd95184e18f`) — the REAL page played in real time
  in headless Chrome at 1440 × 900, recorded over the DevTools protocol (398 screencast frames, resampled to a
  constant 30 fps; nothing composited or simulated).
- `playback_1440_full_sequence_sheet.webp` — 16 frames of that capture: opening, acquisition, approach, hold,
  three frames of the rise, Terrain, THM-01, ALT-01, Priority, hold.
- `playback_1440_opening_first_0p8s.webp` — the first 0.8 s: dark page → opening Earth → video. No held frame.
- `playback_1440_relief_rise_detail_15fps.webp` — the footprint every 1/15 s from 11.00 s to 12.00 s.
- `rise_native_1920_held_rise_states_terrain.webp` — native-resolution crops: held frame, each delivered rise
  state over it, the Terrain state.
- `real_1440_static_slow_network_held_base_then_payoff.webp` — REAL page, desktop static path (forced 2G): the
  held base and the Priority state arrive together; the payoff never sits on the opening Earth.

## 4. Validators

| Gate | Result |
| --- | --- |
| `py -3.14 scripts/validate_site.py` | PASS, 0 warnings |
| `py -3.14 hero/scripts/validate_hero.py` | 420 checks, 0 failed |
| production audit (`shot_audit_production.json`, unchanged) | 59/59 |
| `py -3.14 scripts/negative_tests_web005.py` | 71/71 deliberate regressions caught (24 new); tree restored byte-identical |
| accepted media untouched | `orbgss-hero.webm` `5907372a…`, `orbgss-hero.mp4` `9180cbd1…`, held posters and the four drape states: checksums identical before and after |

New rules, each with a negative test that breaks it on purpose. *Site:* startup poster = the recorded opening
frame inside a `<picture>`; held frame swapped in exactly where the motion never plays; complementary preloads;
deferred held base and `<noscript>` held base; static states must go through `showHeldBase`; 6–12 rise states,
strictly between the held frame and the Terrain state frame, 0.45–0.70 s, each a recorded lossless VP8L RGBA WebP
at 1920 × 1080 under per-state and total ceilings, ending on the recorded Terrain state; rise markup first, in
order, `data-src` only; isolated drape group; `plus-lighter` with no CSS transition; rise states promoted in
exactly one place (the motion path). *Hero:* rise frames strictly inside the scene's own rise interval, which
starts on the held frame and lasts 0.45–0.70 s; the startup poster is the first motion frame.

## 5. For Product's attention

1. **Lossless WebP is a quarter of the PNG's bytes.** The four accepted drape states are PNG (3.61 MiB); the same
   writer would make them about 1 MiB with identical pixels. Not done here — they are accepted assets and this
   pass was told to leave the sequence unchanged — but it is a one-command, provable saving if wanted.
2. **Seven states, interpolated.** The authorization allows 6–12. Seven at two-frame spacing plus exact
   interpolation reads as continuous in the capture; all fifteen intermediate frames would cost about 3.4 MiB.
3. **Nothing is pushed.** Local commits only; say so in chat and the branch goes to `origin` as a fast-forward.

## 6. Reproduce

```powershell
$env:BLENDER = "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"
& $env:BLENDER -b -P hero/scripts/render_drape_states.py -- --scene hero_production_kizildere --profile production_drape --rise-only --out hero/renders/production/rise
py -3.14 hero/scripts/package_drape_states.py --rise
& $env:BLENDER -b -P hero/scripts/encode_production_media.py -- --scene hero_production_kizildere --width 1920 --height 1080 --opening-poster-only
```
