# WEB-005A — Hero visual fidelity: review evidence

**Task:** WEB-005A / MER-107 — `tasks/WEB-005A_HERO_VISUAL_FIDELITY.md`
(canonical: `docs/web-005-polish-authority@f58f4361ef5cb13371464e530bdf9a19ac5c575a`)
**Visual direction:** `docs/WEB_005_POLISH_VISUAL_DIRECTION_AUTHORITY.md`
(canonical: `docs/web-005-polish-authority@5622e6765763e69f374796c33986bf680db86e6a`)
**Parent:** WEB-005 / MER-93, terminally accepted at `main@00af0f232a8d7d77f5ca61d758461ff7316ba151`
**Branch:** `feat/web-005a-hero-visual-fidelity`
**Rejected review checkpoint (retained as before-evidence):** `ffa2f2944ca5992afb9e9891b42745a9bd1105ad`
**State:** `REVIEW_READY` (R2)
**Final HEAD:** see §1 — recorded at publication.

This document has two parts. **Part A** is the R2 revision Product asked for after rejecting the
`ffa2f294…` checkpoint. **Part B** is the original checkpoint's evidence, kept verbatim below the
line because it is the "before" of every comparison here and because the technical work it
records (orbit solve method, bitrate investigation, AOI thinning, resolved tail) was accepted as
useful and is carried forward rather than restarted.

---

# Part A — R2 visual revision

## 1. Identity

| | |
| --- | --- |
| Branch | `feat/web-005a-hero-visual-fidelity` |
| Final implementation HEAD | `<!-- HEAD -->` |
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

# Part B — Rejected checkpoint `ffa2f294…` (retained before-evidence)

*Recorded on 2026-09-16 before Product review. Technically green, visually not accepted. Kept as
the "before" of Part A; nothing below is current implementation state.*

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
