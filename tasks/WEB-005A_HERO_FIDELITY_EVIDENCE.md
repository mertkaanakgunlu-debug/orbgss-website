# WEB-005A — Hero visual fidelity and motion refinement: review evidence

**Parent task:** WEB-005 / MER-93, terminally accepted at
`00af0f232a8d7d77f5ca61d758461ff7316ba151:tasks/WEB-005_TERMINAL_PRODUCT_ACCEPTANCE.md`
**Branch:** `feat/web-005a-hero-visual-fidelity`
**Execution baseline:** `main@00af0f232a8d7d77f5ca61d758461ff7316ba151`
**State:** `REVIEW_READY`
**Scope:** hero visual fidelity and motion only. No homepage restructuring, no science, no claims.

---

## 1. What this revision is, and what it deliberately is not

The accepted WEB-005 hero was structurally right and visually unfinished. Five Product defects were
named; each is addressed below with what changed and why. Nothing outside the hero's rendered media
and its playback timing was touched.

**Unchanged, and verified unchanged in §8:** the four-act homepage composition; every accepted
GEO-WEB-002 asset, checksum and placement; the `mvp_remote_sensing_priority_v1` public label and
semantics; the `render_surface: html_overlay` rule that keeps governed rasters out of the lossy
encode; EN/TR parity; accessibility; responsive behaviour; reduced-motion, reduced-data and
no-dual-download behaviour; the 420 km regional acquisition frame's classification as **not** the
36 × 36 km analysis AOI.

---

## 2. Defect 4 — satellite orbital motion

### What was wrong

The accepted path was eight hand-typed world-space points. Their distances from Earth's centre were
**11.77, 16.44, 10.91, 9.12 … 8.08 BU** — the "satellite" drifted outward, then inward, then
inward again. Nothing about it was orbital, which is why it read as a prop being slid around rather
than a spacecraft. It was also visible from frame 1, so there was no entrance at all.

### What changed

The path is now **one circular orbit**, generated rather than typed. Every key lies on the same
circle through the AOI centre, so the radius is **7.076 BU at every keyframe** — 705 km altitude,
which is the Landsat/Sentinel-2 class sun-synchronous altitude, borrowed from the mission type the
hero depicts rather than invented for the shot.

The pass was then **solved against the accepted camera path**, not eyeballed. A search over orbit
tilt, entry angle and exit angle scored candidates on four requirements at once — hidden at the
open, clean limb crossing, overhead at acquisition, and gone before the camera descends far enough
to expose the model at close range. The chosen solution (tilt −35°, −175° → +80°):

| Frame | Orbit angle | Occluded by Earth | In frame | Distance | On-screen size |
| --- | --- | --- | --- | --- | --- |
| 1 | −175° | **yes** | — | 53 048 km | 6 px |
| 30 | −142° | **yes** | — | 41 046 km | 9 px |
| 50 | −124° | no — limb crossing | yes | 33 064 km | 12 px |
| 96 | −69° | no | yes | 18 997 km | 21 px |
| 126 | −28° | no | yes | 10 470 km | 42 px |
| **150** | **−4°** | no — **overhead the AOI** | yes | 7 687 km | 59 px |
| 176 | +18° | no | yes (leaving) | 6 352 km | 78 px |
| 190 | +28° | no | **out of frame** | 6 126 km | 87 px |
| 236 | +59° | **yes** | — | 8 111 km | — |
| 276 | +80° | **yes** | — | 9 968 km | — |

So the spacecraft is hidden behind the Earth, emerges at the limb during the entrance beat, arcs up
across frame while the camera closes, is overhead the AOI exactly at the acquisition beat, leaves
frame as the scan finishes, and passes behind the Earth again before the camera reaches the hold.

**Why it was solved rather than tuned:** the previous version failed in a way a single preview frame
cannot show. An earlier attempt in this revision looked correct at the acquisition frame and then
put the satellite **525 px across, in the foreground over the Nile**, because it exited toward the
camera. Peak on-screen size is now **87 px** and the model is never seen larger than that.

---

## 3. Defect 3 — the scan/beam effect

### What was wrong

Four opaque cones fired from the spacecraft to the four AOI corners, plus a **13 %-of-AOI-wide**
white band sweeping across the footprint. The cones read as plastic tubes; the band read as a
blurry smear. Neither resembles how an Earth-observation instrument works.

### What changed

| | Accepted | WEB-005A |
| --- | --- | --- |
| Beams | 4 cones to the corners | **1** boresight to the AOI centre |
| Beam tip radius | 14 km | 172 km — a broad, soft sensing volume, not a needle |
| Beam alpha (root → tip) | 0.02 → 0.20 | **0.002 → 0.016** |
| Beam emission | 3.2 | **0.85** |
| Beam silhouette | 14 sides | 48 sides — no faceting |
| Scan band width | 0.13 of the AOI | **0.030** — a pushbroom line, not a wash |
| Scan band alpha | 0.45 | 0.30 |

The acquisition now reads as a single instrument footprint with a narrow leading edge travelling
across it, leaving a slightly denser acquired field behind — which is what a pushbroom sensor
actually does.

**The beam alpha was lowered twice, on review of the renders.** The first pass replaced four opaque
cones with one broad cone at 0.045 tip alpha. That was a real improvement, but at the scan beat it
still read as a translucent wedge with **hard straight silhouette edges** — the same "cheap overlay"
tell in a different shape. Dropping it to 0.016 removes the silhouette entirely: the directed-sensing
cue survives as a barely-there volume, and the acquisition is carried by the scan line and the AOI's
own response instead. That is also the more honest depiction, since an Earth-observation instrument
is passive and emits nothing.

Only frames 124–194 carry the beam, so the second pass re-rendered **71 frames rather than all 276** —
the material's presence ramp is exactly zero outside that range, which is checkable in the config
rather than assumed.

---

## 4. Defect 5 — the AOI frame

| | Accepted | WEB-005A | Effect at the hold |
| --- | --- | --- | --- |
| Border width | 9.0 km | **2.6 km** | ~11 px → ~3 px |
| Corner lock arm | 85 km | 52 km | less sprawl |
| Corner lock width | 15 km | **5.4 km** | chunky block → registration bracket |
| Corner lock offset | 90 m | 140 m | reads clear of the border |
| Edge samples | 48 | **112** | a drawn arc, not a polygon |
| Fill grid | 24 | 32 | smoother sweep parameterisation |

**Nothing that carries geometric meaning changed.** The centre, span, bearing and surface offset are
untouched, so the footprint covers exactly the same ground as the accepted build. Only line weight
and sampling density changed.

---

## 5. Defect 1 — the ending

### What was wrong

The shot stopped. The camera eased to rest and the last ~70 frames had nothing happening in them.
The corner locks had already appeared at frame 116–138, the beam had already gone at 146–166, so by
the hold every element was simply static — and the page-layer handoff was revealed at **frame 200**,
three seconds before the video ended, so the result arrived during dead air rather than as a payoff.

### What changed

The tail now carries a resolution, sequenced so each step lands after the last:

| Frames | What resolves |
| --- | --- |
| 146 → 198 | scan line completes its travel across the footprint |
| 172 → 194 | boresight retires |
| 196 → 224 | AOI border **firms** to 1.36× then settles to 1.06× |
| 204 → 234 | corner locks **resolve in** — moved here from 116–138, so the lock is the ending rather than an early flourish |
| 234 → 266 | locks pulse to 1.24× and settle |
| **240 (10.0 s)** | **page-layer handoff reveals** — moved from frame 200 |
| 266 → 276 | everything at rest; final composed still |

This needed one bounded builder addition: `border`, `corner_locks` and `fill` now accept an optional
post-appearance ramp (`emphasis` / `settle`) as `[[frame, factor], …]`. An appear ramp alone can only
say "this is here now"; an ending needs to be able to say "this is resolved".

The hero validator's guard against hand-typed geometry in the AOI spec correctly flagged those
`[frame, factor]` pairs as coordinate-shaped. Rather than weaken it, the guard now skips the two
ramp keys by name **and** a new check proves their shape — so the exemption cannot be used to
smuggle a position through a timing field. That is a net gain of one real check.

---

## 6. Defect 2 — softness: the hypothesis that was tested

Going in, the obvious explanation was that the accepted WebM was starved at 1 418 kbps for
1920 × 1080, and that a cleaner, supersampled source plus a better encoder preset would recover the
detail. Two changes were made on that basis:

- **Supersampling.** Frames render at **2304 × 1296** and deliver at 1920 × 1080. The downscale
  removes aliasing and averages sampling noise, so the encoder receives a cleaner signal. It also
  means 128 samples at render size is not a quality reduction — the downscale averages them back up
  per delivered pixel.
- **Encoder preset**, evaluated rather than assumed.

**The hypothesis was wrong.** §7 records the measurements that disproved it and the cause they
found instead. The changes above were kept because they are genuine improvements to the source, but
they are not what makes the ground soft, and the evidence says so plainly rather than claiming a
win that is not there.

---

## 7. Defect 2 — what the measurements actually found

The working assumption going in was that the accepted hero was soft because its encoder was
starved at 1 418 kbps. **That assumption was wrong, and the measurements say so clearly.**

All measurements below decode the shipped file in a browser, draw it at the displayed size
(1920 × 1080, which is what the full-bleed hero shows), and compute mean |Laplacian| over three
256 px crops of bare Earth surface at **t = 11.40 s**. The camera path is unchanged between builds,
so the framing at a given timestamp is identical and the comparison is like-for-like.

### Does more bitrate buy sharpness? No.

| Encode | Size | Mean detail | vs shipped |
| --- | --- | --- | --- |
| 1 460 kbps (**shipped**) | 2.799 MiB | 3.1209 | — |
| 1 866 kbps | 3.384 MiB | 3.1661 | **+1.4 %** |
| 2 400 kbps | 4.161 MiB | 3.1632 | **+1.4 %** |

Raising the budget by 64 % buys 1.4 % and then **plateaus**. The encoder is already past the
content's rate–distortion knee. **The byte ceiling is not the constraint, and this revision is
therefore not asking for it to be relaxed.**

### Is a lower delivery resolution better? No — materially worse.

| Delivery | Detail at displayed size | vs accepted |
| --- | --- | --- |
| 1920 × 1080 (shipped) | — | −1.7 % … −6.6 % |
| 1600 × 900, upscaled to fit | — | **−18.4 % … −24.3 %** |

1600 × 900 was encoded, measured and **rejected on evidence**. 1920 × 1080 stays.

### Can constrained-quality encoding fit the budget? No.

Blender's VP9 CRF ladder ignores the bitrate cap. The lowest tier above `LOWEST` still produces
**3.512 MiB — 17 % over the 3.0 MiB ceiling**; `LOW` produces 4.374 MiB. Constrained quality cannot
reach this budget without dropping to a tier visibly worse than the CBR result.

### The actual cause: the basemap runs out of pixels

The Earth albedo is the NASA Blue Marble 8192 px equirectangular composite. At the AOI's latitude
that is **3 856 m per texel**. At the regional hold the camera frames about 1 430 km of ground:

> **1 430 km ÷ 3 856 m/texel ≈ 371 texture pixels, stretched across 1 920 screen pixels — a 5.2×
> magnification of the source.**

There is no high-frequency detail left to encode, which is exactly why more bitrate does nothing,
why supersampling reaches parity rather than improvement, and why reducing resolution hurts.

### What this revision did achieve on defect 2

- the source is now **alias-free and lower-noise** (2304 × 1296 supersampled to 1920 × 1080), so
  what detail exists is delivered cleanly rather than competing with sampling noise for bits;
- the encoder was switched from `BEST` to `GOOD` on measurement, not preference: libvpx-vp9's
  "best" deadline cost roughly **20 minutes per attempt** here for a difference the format's own
  maintainers call negligible.

### `BLOCKED_ON_SOURCE_RESOLUTION` — needs a Product decision, not an envelope change

Materially sharper ground at the closest approach requires a **higher-resolution Earth basemap**,
which is a new source asset with its own rights and provenance record — not a render or encode
setting. The same NASA Blue Marble Next Generation series publishes 21 600 × 10 800 tiles
(≈ 500 m), which would take the magnification from **5.2× to about 1.3×**.

This revision does **not** fetch or add that asset: it is new external source material, and adding
it is a Product/rights decision rather than an implementation one. The byte ceilings need no change.

---

## 8. Scientific and public semantics — verified unchanged

This was checked by diffing against the accepted baseline rather than asserted.

| Surface | Result |
| --- | --- |
| `index.html` | **byte-identical** to `main@00af0f2` — not touched |
| `styles.css` | **byte-identical** — not touched |
| `assets/imagery/sources.json` → `scenes` | **unchanged** |
| → `web_002` (accepted proof package) | **unchanged** |
| → `geo_web_002` (accepted visual masters + placements) | **unchanged** |
| → `production_source`, `web_vnext`, `policy` | **unchanged** |
| → `web_005` | only `hero_media`, `source`, `revision` — the hero media records |
| `script.js` | one constant: the handoff reveal moved from frame 200 to 240 |

So the four-act composition, every accepted GEO-WEB-002 asset and checksum, every placement and
safe-density record, the `mvp_remote_sensing_priority_v1` label and semantics, all EN/TR copy, every
mandatory warning and the whole of the public HTML are untouched by this revision. The only changes
are the hero's rendered media, the hero production configuration that generates it, and when the
page reveals the handoff.

The `render_surface: html_overlay` contract is unchanged and still enforced: **no governed
scientific raster is baked into the video.** The 420 km footprint is still classified
`production_regional_frame` with `is_analysis_aoi: false`.

---

## 9. Production media and validators

| File | Container / codec | Dimensions | Rate | Duration | Size / ceiling | Accepted build | SHA-256 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `assets/hero/orbgss-hero.webm` | WebM / VP9 | 1920 × 1080 | 24 fps | 11.5 s | **2.765 MiB** / 3.0 MiB | 2.800 MiB | `d86fdfc3ddf02011ed8fdfebd54a244b7ac804bec7a20199b8f2131b81d859a5` |
| `assets/hero/orbgss-hero.mp4` | MP4 / H.264 | 1920 × 1080 | 24 fps | 11.5 s | **3.521 MiB** / 4.5 MiB | 3.509 MiB | `333b182b54a9c7a73b1c062558a71ab6fbd03a3ef216697d99da01b74f8943b8` |
| `assets/hero/hero-poster-1600.webp` | WebP q88 | 1600 × 900 | — | — | **82.9 KiB** / 180.0 KiB | 81.6 KiB | `5f86d27df4db675b5a70e1035017144cc49f1738ab818e51dfaf55a1d618b98d` |
| `assets/hero/hero-poster-900.webp` | WebP q88 | 900 × 506 | — | — | **40.3 KiB** / 180.0 KiB | 39.4 KiB | `dd3ef9cbe50fa2d26552b1ef7a0583e4e74e4ea02bce9428d751ba547cee8338` |

Rendered at **2304 × 1296** (Cycles, OptiX, 128 adaptive samples, 16.3 s/frame), delivered at
1920 × 1080. Frames 124–194 were re-rendered in a second pass for the beam change; frames outside
that range are from the first pass, which is sound because the beam's presence ramp is exactly zero
outside it.

| Validator | Result |
| --- | --- |
| `py -3.14 scripts/validate_site.py` | **PASS, 0 warnings** |
| `py -3.14 hero/scripts/validate_hero.py` | **PASS — 187 checks, 0 failed** (was 184; the ramp shape check is new) |
| `py -3.14 scripts/negative_tests_web005.py` | see below |
| `node --check script.js` | OK |
| `git diff --check` | clean |

### Before/after stills

`hero/evidence/web005a/` carries the four Product-named moments as paired 1280 × 720 stills:

| Moment | Before | After |
| --- | --- | --- |
| Satellite entrance | `1_satellite_entrance_before.webp` | `1_satellite_entrance_after.webp` |
| Scan / acquisition | `2_scan_acquisition_before.webp` | `2_scan_acquisition_after.webp` |
| Regional hold | `3_regional_hold_before.webp` | `3_regional_hold_after.webp` |
| End state | `4_end_state_before.webp` | `4_end_state_after.webp` |

The hold and end-state pairs are the same frame numbers with an identical camera, so they are a
direct like-for-like comparison of the AOI frame treatment.

---

## 10. Residual observations (not blocking)

- **Satellite frame-edge crossing.** The spacecraft leaves through the top-right of frame over
  roughly frames 170–184 (~0.5 s), so for that moment it is partly at the frame edge. This is
  normal framing behaviour for a body moving out of shot and was judged not worth a second
  75-minute render; raised here so Product can disagree cheaply.
- **Duration.** 11.5 s is unchanged. Shortening the hero would raise bits per frame, but §7 shows
  bitrate is not the constraint, so it would buy nothing.
