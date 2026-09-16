# WEB-005 — Cinematic Hero, Four-Act Homepage, Release Candidate: review evidence

**Linear:** `MER-93`
**Task authority:** `feat/web-005-cinematic-hero@c62e26304efaac40aaf0cc4975efae976381d7be:tasks/WEB-005_CINEMATIC_HERO.md`
**Branch:** `feat/web-005-cinematic-hero`
**Execution baseline:** `main@d2421a772f2e4cfa38c85dd5ee71a419c5160838`
**State:** `REVIEW_READY`

**Implementation HEAD:** `0e3b878280a5c4b4198c223153178f89137bd01c`  
**Final HEAD:** the evidence-publication commit that adds this document on top of it.

The changed-path inventory (§1) and the production media table (§6) are generated from git and from `hero/evidence/production_media.json` rather than transcribed, so they cannot drift from what was actually built.

---

## 0. Preconditions verified before any implementation

Every precondition named in the start instruction was checked against the repository before a
single file was touched.

| Precondition | Expected | Found | |
| --- | --- | --- | --- |
| Repository | `mertkaanakgunlu-debug/orbgss-website` | `origin` = `https://github.com/mertkaanakgunlu-debug/orbgss-website.git` | ✅ |
| Implementation branch | `feat/web-005-cinematic-hero` | present on `origin`, HEAD `c62e26304efaac40aaf0cc4975efae976381d7be` | ✅ |
| Execution baseline | `main@d2421a772f2e4cfa38c85dd5ee71a419c5160838` | `origin/main` resolves to exactly that commit | ✅ |
| Baseline is an ancestor of the branch | — | yes; the branch is the baseline plus one authority-publication commit touching only `tasks/WEB-005_CINEMATIC_HERO.md` | ✅ |
| WEB-HERO-001D evidence HEAD | `e95fdcac7cac82e597d40dab4cdc96ce1a6b319e` | commit present; `validate_hero.py` reproduces the accepted **151 checks, 0 failed** | ✅ |
| GEO-WEB-002 package on the baseline | package doc, science acceptance, task acceptance, machine-readable record | all four present; `sources.json` carries `geo_web_002` with 6 assets / 19 derivative files | ✅ |

### One authority defect found and worked around, not silently accepted

The task authority cites terminal Product acceptance at
`e95fdcac7cac82e597d40dab4cdc96ce1a6b319e:tasks/WEB-HERO-001D_TERMINAL_PRODUCT_ACCEPTANCE.md`.
**That path does not exist at that commit.** The acceptance record was published one commit later,
at `573f4f1` on the same branch, in a commit that changes only that one file (verified with
`git show --stat`). The accepted *implementation* content at `e95fdca` is therefore unaffected.

This is an evidence/publication pointer defect, which the task keeps inside implementation, so it
was not escalated. It is resolved **as a provenance correction only** and published in
`docs/WEB-HERO-001D_ACCEPTANCE_POINTER_CORRECTION.md`, with both pointers recorded machine-readably
in `hero/config/lane.json`. Nothing about what was accepted changes: both documents agree on the
accepted implementation HEAD and the accepted evidence HEAD, and only one citation path is wrong, by
one documentation-only commit.

Provenance in this task is retained to `e95fdcac7cac82e597d40dab4cdc96ce1a6b319e` exactly as
instructed; the acceptance *decision* is cited at
`573f4f10cbe397e8f3bdf6611deea5cd2660dcae` where it actually lives. The published task authority was
deliberately **not** edited — correcting a citation inside a Product-owned document is a Product
action, not an implementation one.

---

## 1. HEAD and changed paths

**Final implementation HEAD:** `0e3b878280a5c4b4198c223153178f89137bd01c`

**Branch:** `feat/web-005-cinematic-hero`  
**Baseline:** `d2421a772f2e4cfa38c85dd5ee71a419c5160838`

**Diff against baseline:** 70 files changed, 14561 insertions(+), 446 deletions(-)

**Commits (3):**

- `0e3b878 feat(web-005): four-act homepage, production hero media, release candidate`
- `48aa760 feat(web-005): carry forward the accepted hero lane and add the production scene`
- `c62e263 docs(web-005): publish cinematic hero integration authority`

**Changed-path inventory:**

*Public site*

- `index.html` (modified)
- `pilot/index.html` (modified)
- `script.js` (modified)
- `styles.css` (modified)

*Provenance & manifests*

- `assets/imagery/sources.json` (modified)

*Hero production lane*

- `hero/README.md` (added)
- `hero/assets/manifest.json` (added)
- `hero/assets/source/.gitignore` (added)
- `hero/blender/.gitkeep` (added)
- `hero/config/lane.json` (added)
- `hero/config/render_profiles.json` (added)
- `hero/config/scene.json` (added)
- `hero/evidence/animatic_predata_animatic.json` (added)
- `hero/evidence/aoi_geometry_audit_design_primary.json` (added)
- `hero/evidence/aoi_geometry_audit_design_secondary.json` (added)
- `hero/evidence/aoi_geometry_audit_predata_animatic.json` (added)
- `hero/evidence/aoi_geometry_audit_predata_animatic_secondary.json` (added)
- `hero/evidence/benchmark.json` (added)
- `hero/evidence/benchmark_neutral_evidence_still.png` (added)
- `hero/evidence/environment.json` (added)
- `hero/evidence/hero_aoi_acquisition_beam_lock_f170.png` (added)
- `hero/evidence/hero_aoi_acquisition_continuity_sheet.png` (added)
- `hero/evidence/hero_aoi_acquisition_global_acquisition_f150.png` (added)
- `hero/evidence/hero_aoi_acquisition_regional_approach_f240.png` (added)
- `hero/evidence/hero_aoi_acquisition_scan_sweep_f205.png` (added)
- `hero/evidence/hero_aoi_fixture_comparison_f130.png` (added)
- `hero/evidence/hero_earth_orbit_establish_f1.png` (added)
- `hero/evidence/hero_earth_orbit_pre_acquisition_f120.png` (added)
- `hero/evidence/hero_earth_orbit_satellite_entrance_f60.png` (added)
- `hero/evidence/hero_predata_animatic_acquisition_lock_f140.png` (added)
- `hero/evidence/hero_predata_animatic_continuity_sheet.png` (added)
- `hero/evidence/hero_predata_animatic_establish_f24.png` (added)
- `hero/evidence/hero_predata_animatic_mid_approach_f200.png` (added)
- `hero/evidence/hero_predata_animatic_regional_hold_f236.png` (added)
- `hero/evidence/hero_predata_animatic_satellite_entrance_f78.png` (added)
- `hero/evidence/hero_predata_animatic_scan_sweep_f170.png` (added)
- `hero/evidence/phase_ab_reproducibility.json` (added)
- `hero/evidence/phase_abc_reproducibility.json` (added)
- `hero/evidence/production_media.json` (added)
- `hero/evidence/shot_audit_predata_animatic.json` (added)
- `hero/evidence/shot_plan_predata_animatic.json` (added)
- `hero/renders/.gitignore` (added)
- `hero/scripts/aoi_system.py` (added)
- `hero/scripts/audit_aoi.py` (added)
- `hero/scripts/audit_shot.py` (added)
- `hero/scripts/build_scene.py` (added)
- `hero/scripts/compare_renders.py` (added)
- `hero/scripts/contact_sheet.py` (added)
- `hero/scripts/encode_production_media.py` (added)
- `hero/scripts/hero_common.py` (added)
- `hero/scripts/probe_env.py` (added)
- `hero/scripts/render_animatic.py` (added)
- `hero/scripts/render_core.py` (added)
- `hero/scripts/render_preview.py` (added)
- `hero/scripts/render_still.py` (added)
- `hero/scripts/run_benchmark.py` (added)
- `hero/scripts/shot_plan.py` (added)
- `hero/scripts/validate_hero.py` (added)

*Validators*

- `scripts/negative_tests_web005.py` (added)
- `scripts/validate_site.py` (modified)

*Shipped hero media*

- `assets/hero/hero-poster-1600.webp` (added)
- `assets/hero/hero-poster-900.webp` (added)
- `assets/hero/orbgss-hero.mp4` (added)
- `assets/hero/orbgss-hero.webm` (added)

*Docs, status & task records*

- `CHANGELOG.md` (modified)
- `CLAUDE.md` (modified)
- `IMAGERY_RIGHTS.md` (modified)
- `STATUS.md` (modified)
- `docs/WEB-HERO-001D_ACCEPTANCE_POINTER_CORRECTION.md` (added)
- `tasks/WEB-005_CINEMATIC_HERO.md` (added)

---

## 2. What was consumed, and how provenance is retained

### WEB-HERO-001D production source

The whole `hero/` workspace was brought forward with
`git checkout e95fdcac7cac82e597d40dab4cdc96ce1a6b319e -- hero/` — 52 files, byte-identical to the
accepted evidence HEAD, no cherry-picking and no merge of unrelated branch history.

The four accepted scenes (`benchmark_neutral`, `hero_earth_orbit`, `hero_aoi_acquisition`,
`hero_predata_animatic`) are **unmodified**. The production scene inherits the accepted animatic
through `extends`, so the accepted Earth/satellite/camera system, AOI system, world convention and
beat map still have exactly one definition:

| | Accepted `hero_predata_animatic` | Production `hero_production_kizildere` |
| --- | --- | --- |
| Frames | 1–240 @ 24 fps (10.0 s) | 1–276 @ 24 fps (11.5 s) |
| Beats | establish / entrance / acquisition / scan / approach / release / hold | identical through 240; `regional_hold` extended to 276 |
| AOI fixture | `design_primary` — placeholder, "names no site" | `kizildere_regional` — real accepted pilot centre |
| Camera | 8 derived keyframes | the same 8, re-derived for the new centre, plus one tail state |
| Scientific layers | none | none baked into any frame |

**Frames 241–276 introduce no new motion.** They continue the accepted final easing (radius 7.55 →
7.47 BU, i.e. 1179 → 1099 km altitude) until the move comes to rest, so the shot ends on a still
frame that doubles as the poster instead of being cut off mid-settle. `validate_hero.py`'s
continuity contract — one scene, one AOI system, ordered beats, monotonic approach, hold long
enough to receive data, 6–12 s envelope — is applied to the production scene and passes.

### The AOI geometry change, stated plainly

The accepted design fixture was a deliberate placeholder at a round (38.0 N, 29.0 E) with a 420 km
span, documented as carrying no measurement meaning. WEB-005 replaces it with the real accepted
Kızıldere pilot centre **37.9794 N, 28.7907 E**, taken from
`geo_web_002.context_scenes[kizildere-aoi-context-2025]`. This is exactly what
`aoi_injection_interface` was built for: *"WEB-005 replaces the design fixtures below with accepted
AOI geometry … without touching scene or builder code."* It is a config change.

The span stays 420 km, and **that is a regional acquisition frame, not the analysis AOI.** The
accepted analysis AOI is 36 × 36 km. The hero holds on a region; the science covers a smaller box
inside it. The fixture declares `is_analysis_aoi: false`, `validate_hero.py` fails the build if a
production fixture omits that disclaimer, and public copy states the 36 × 36 km extent separately
in Act 4's metadata line. No copy anywhere calls the 420 km frame an AOI.

The camera was **re-derived**, not retyped: `shot_plan.py --derive` recomputed the `aoi_relative`
keyframes against the new centre. The 8 km centre shift moves a camera 1179 km up by almost
nothing — frame 240 went from `[1.6514, -6.6262, 3.2200]` to `[1.6274, -6.6334, 3.2176]`, about
25 m in world space. Measured framing at every keyframe: AOI in frame throughout, centre lock
exactly `x = 0.500, y = 0.500` from frame 136 on, headline-safe region clear of the planet through
frame 96.

### GEO-WEB-002 assets

Five of the six accepted assets are bound to the homepage; `alt02` is deliberately not placed, as
the accepted package names ALT-01 the preferred single alteration card. Every binding is recorded in
`geo_web_002.assets[].web_005_placement` with act, slot, routes, the warning it must carry, and the
measured render size. Nothing was re-exported, re-encoded, re-coloured or re-cropped: the shipped
files are the accepted derivatives, and the validator recomputes all 19 checksums on every run.

---

## 3. The decision that shaped the hero: why no science is inside the video

The task allows the post-hold handoff to reveal accepted result media and deliberately does not
prescribe how. It also requires that class-B assets receive no "CSS/video/post-processing that
changes their governed colours/contrast/opacity in a way that alters interpretation."

Those two pull against each other, because **baking a governed raster into a video frame is exactly
such a change.** VP9 and H.264 ship 4:2:0 chroma at a lossy bitrate; the priority surface is read
by colour, against a governed `batlow` ramp whose values carry the meaning. Encoding it would
quantise and subsample precisely the channel the science lives in — and no bitrate makes that
untrue, only less visible.

So the hero renders the acquisition and the **page** composites the result:

- the video is the accepted cinematic system over the real pilot region and contains **no**
  scientific layer in any frame;
- the handoff is an ordinary `<img>` carrying `assets/proof/final/priority-800.webp`, the exact
  accepted derivative, byte-identical and checksummed like every other raster on the site;
- the two are visibly different kinds of thing, which is also what the task asks for: *"the viewer
  can distinguish acquisition imagery from analytical evidence/results."*

This is recorded as a contract rather than a habit. The hero scene's
`aoi_injection_interface.layer_slots[result_priority]` declares
`render_surface: "html_overlay"` with its reason, and `validate_hero.py` fails if a populated layer
slot ever claims a different surface.

**Against implied causality.** A hero that shows a satellite acquiring a box and then reveals a
score risks implying the pass produced the score — the "direct satellite-to-score causality" the
task forbids. The handoff copy is built to break that read: the kicker is `04 · Result`, numbering
it as the fourth act rather than an immediate output, and the link says *"See how it was derived"*.
Acts 2–4 then show the actual chain.

---

## 4. The four acts

| Act | Section | Composition | Visual | Provenance |
| --- | --- | --- | --- | --- |
| 1 | `#hero` | full-bleed video + protected HTML copy column | production hero media | WEB-HERO-001D @ `e95fdca` |
| 2 | `#context` | tightly coupled split, contained | `kizildere-aoi-context-2025-*` | `geo_web_002.assets[act2-context]` |
| 3 | `#evidence` | the one compact three-card composition | `terrain`, `thm01`, `alt01` | `geo_web_002.assets[...]` |
| 4 | `#priority` | dark stage, contained figure, legend inside the frame | `priority` | `geo_web_002.assets[priority]` |

Four different compositions, deliberately — the superseded homepage repeated one beam/panel
template six times, which is what made correct cartography read as a gallery.

**Removed:** the six-scene `#platform`/Observe, Terrain, Evidence (tablist), Structure, Priority and
Geothermal full-width story sections, the detached score `scale-strip`, and the evidence layer
switch. `scripts/validate_site.py` now fails the build if `story-section`, `story-beam` or
`layer-switch` reappears on the homepage, if the act count or order changes, or if the evidence act
holds anything other than three cards.

**Structure/geology** is a short subordinate footnote under Act 3 (`#structure`), stating the gap
and that it is score-invariant. Not fabricated, not an act.

**Legend policy.** The only legend on the homepage is the priority export's own governed legend,
cropped losslessly from its master, placed *inside* the map frame at 248 CSS px against a 732 px
native crop, on the light plate it was rendered against — not inverted, not recoloured. There is no
detached homepage colour bar; the validator checks for one.

---

## 5. Safe display density — measured, not asserted

The accepted package's hard limit is **1249 device pixels** for class-B cartographic assets (a
1200 × 1200 cell grid at 30 m drawn at 1249 px) and 2400 for the class-A context master. The
question that matters is not what `sizes` says but what the browser actually renders, on a 2×
display, at the worst viewport.

Measured by `getBoundingClientRect()` on the built page across a **360 → 3840 CSS px** sweep
(17 widths):

| Visual | Widest CSS render | At viewport | Device px @2× | Ceiling | |
| --- | --- | --- | --- | --- | --- |
| Act 2 — Kızıldere context | 1199 px | 2560 | 2398 | 2400 | ✅ |
| Act 3 — each evidence card | 624 px | 2560 | 1248 | 1249 | ✅ |
| Act 4 — priority map | 623 px | 768 | 1246 | 1249 | ✅ |
| Act 4 — in-frame legend | 248 px | 700 | 496 | 732 | ✅ |

**A real violation was found and fixed by this measurement.** Uncapped, an evidence card reached
**767 CSS px on a 2560 px display — 1534 device pixels**, i.e. the browser upscaling scientific
content by 23% past the honest limit. The `sizes` attribute alone would never have revealed it.
`.evidence-card` now carries `max-width: 624px`, with the reason written next to it.

Act 4 is contained for the same reason and cannot be otherwise: the accepted score raster **cannot**
reach the ≥ 2000 px Act-4 presentation target from accepted science, and the package says so
explicitly. The composition carries the weight instead of the raster being stretched.

Each measured figure is stored in `geo_web_002.assets[].web_005_placement.rendered` alongside the
method used, and `scripts/validate_site.py` now recomputes `max_css_width × dpr ≤ device_px` for
every placed asset, so a later layout change that quietly widens a scientific visual fails the build.

**No horizontal overflow at any of the 17 widths**, and no element extending past the viewport.

### Caption contrast — a second regression found and fixed

WEB-004 established that every on-image caption must clear WCAG 1.4.3's 4.5:1, and measured a
worst case of 4.58:1. Re-measuring the same way on the new homepage found it had slipped, for two
independent reasons:

1. **The third caption line was dimmed to 86% opacity** for visual hierarchy. On a mid-luminance
   backdrop that cost up to 1.9:1 and put it as low as **2.97:1** — and on the hero that line is
   `Rendered orbital sequence — not sensor imagery`, which is the single most important sentence
   on the page to be able to read.
2. **On a mid-luminance backdrop neither accepted tone can pass.** At a backdrop luminance around
   0.19, pure white reaches only 4.37:1 and pure black 4.80:1, so the WEB-004 tone switch — which
   picks the better of two colours — has nothing good to pick. Act 2's natural-colour terrain sits
   exactly there. The tone switch was never broken; it had run out of room.

Fixed at the source rather than by nudging a colour:

- all three caption lines now carry the full tone colour; hierarchy comes from tracking, not alpha;
- the hero's existing shade, which protects the headline on the left, now also protects the caption
  at the bottom — the same mechanism, extended, on a class-C render where presentation treatment is
  allowed. The `max-width: 980px` override was carrying the old weak gradient and was fixed too;
- Act 2 gets an equivalent gradient, because it is a **class-A photograph**;
- **Acts 3 and 4 get no gradient at all.** Darkening a governed class-B raster changes what it
  shows. Their labels and caption therefore sit *outside* the frame, on the page background. That
  is the rule: a caption may sit on the image only where a protection gradient is permitted.
- panels whose caption sits over a gradient are marked `data-label-tone-locked` and the tone script
  skips them. It samples the raster and would miss the gradient on top — which is how you end up
  choosing dark text for a deliberately darkened corner. The accepted `/pilot/` proof panels, whose
  captions sit on untreated imagery, are still measured exactly as WEB-004 does it.

Measured on the built page against the **composited** backdrop (raster luminance with the gradient's
own parsed stops applied at the caption's exact position), for the dimmest line:

| Viewport | Hero | Act 2 context |
| --- | --- | --- |
| 375 | 11.26:1 | 9.65:1 |
| 414 | 7.49:1 | 9.40:1 |
| 768 | 16.25:1 | 8.35:1 |
| 1024 | 10.84:1 | 7.99:1 |
| 1280 | 14.67:1 | 10.15:1 |
| 1440 | 15.50:1 | 7.55:1 |
| 1920 | 17.15:1 | 8.71:1 |

**Worst case 7.49:1**, against a 4.5:1 requirement and WEB-004's 4.58:1 baseline. The change also
raises contrast on the existing `/pilot/` captions, since the opacity fix applies site-wide.


---

## 6. Production hero media

Rendered from scene `hero_production_kizildere` at profile `production` (1920 × 1080), delivered at 1920 × 1080. Encoded through Blender 4.5.10 LTS's own bundled FFmpeg — there is no system ffmpeg on this machine, and adding one would be a new dependency for a static site.

Source frames: 276 PNGs in `hero/renders/production/frame.png` (generated output, not tracked). Colour management on the encode path is forced to Standard/None because the stills already carry the render's view transform; applying it twice would shift every pixel.

| File | Role | Container / codec | Dimensions | Rate | Duration | Bytes / ceiling | SHA-256 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `assets/hero/orbgss-hero.webm` | hero-webm | WebM / VP9 | 1920 × 1080 | 24 fps | 11.5 s (276 frames) | **2.8 MiB** / 3.0 MiB | `fa0561103bedf3c743bc11fdeeb742c883917088b62fa3365ed2a3ad417de21a` |
| `assets/hero/orbgss-hero.mp4` | hero-mp4 | MP4 / H.264 | 1920 × 1080 | 24 fps | 11.5 s (276 frames) | **3.509 MiB** / 4.5 MiB | `40bb37ee18a343267d08ed05ea69c507341fa5b52ee585db74768ed183c134ab` |
| `assets/hero/hero-poster-1600.webp` | hero-poster | WebP / WebP (lossy) q88 | 1600 × 900 | — | — | **81.6 KiB** / 180.0 KiB | `8fc3779a326f80fa1463e09dfa31c3da61eda97a01807a211f24b0c5170b2e52` |
| `assets/hero/hero-poster-900.webp` | hero-poster-narrow | WebP / WebP (lossy) q88 | 900 × 506 | — | — | **39.4 KiB** / 180.0 KiB | `15b6abb86eede88e508a09cc912914a8a4219db1c7ea36c8c4f79100031d4849` |

**Every file is inside its ceiling.**

### The bitrate was found, not guessed

A byte budget is not a bitrate you can type — it depends on the content, and this content is a slow camera move over a mostly smooth sphere, which compresses far better than a rate table predicts. Each encode was measured and re-encoded against its own result, keeping the **largest** encode that still fits, because inside the ceiling the biggest file is the best-looking one. The full search:

- **hero-webm** (1418 kbps chosen): 1900 kbps = 3.537 MiB → 1418 kbps = 2.8 MiB
- **hero-mp4** (2800 kbps chosen): 2800 kbps = 3.509 MiB
- **hero-poster** (quality 88 chosen): q88 = 81.6 KiB
- **hero-poster-narrow** (quality 88 chosen): q88 = 39.4 KiB

The poster is the **last** rendered frame, not the first: the shot ends on the stable regional hold, so the still a visitor sees before playback is the composition playback settles into, and the crossfade cannot shift the framing.

Full machine-readable record, including every search step: `hero/evidence/production_media.json`.

---

## 7. Hero behaviour: autoplay, fallback, reduced motion, reduced data

The markup ships a poster `<img>` and an **empty** `<video>` — two candidate URLs in `data-`
attributes, no `<source>` children, no `src`, `preload="none"`. A `<source>` child starts fetching
during parse, and with two declared, a browser can fetch both; the media contract forbids exactly
that. `script.js` owns the decision instead:

| Condition | Behaviour | Video bytes |
| --- | --- | --- |
| `prefers-reduced-motion: reduce` | intentional still hero, handoff revealed immediately | **0** |
| viewport ≤ 780 px (phones) | intentional still hero, handoff revealed immediately | **0** |
| `navigator.connection.saveData` | intentional still hero | **0** |
| `effectiveType` ∈ {slow-2g, 2g, 3g} | intentional still hero | **0** |
| JavaScript disabled | poster is the hero; handoff stays hidden, Act 4 carries the result | **0** |
| autoplay refused by policy | caught, settles to the poster, handoff revealed | one encode |
| otherwise | exactly one encode, chosen by `canPlayType` | one encode |

`prefers-reduced-motion` is also honoured **mid-visit**: a change event pauses playback and settles
to the still hero. A 15 s belt-and-braces timer guarantees the result is revealed however playback
goes, so the analytical answer is never hidden behind a video that failed.

The video is `aria-hidden="true"`, `tabindex="-1"` and carries no controls — it is decoration over
which the real content sits. All hero copy is HTML in the motion-safe region the accepted shot was
measured against; nothing is baked into a frame.

### Measured, not asserted

Each row below was produced by loading the real page with the relevant condition stubbed before
`script.js` runs, then reading the hero's state, the video's attached `src` and its `<source>`
child count:

| Stubbed condition | `data-hero-state` | Reason recorded | Attached `src` | `<source>` children | Handoff |
| --- | --- | --- | --- | --- | --- |
| `prefers-reduced-motion: reduce` | `static` | `reduced-motion` | none | 0 | revealed |
| `saveData: true` | `static` | `save-data` | none | 0 | revealed |
| `effectiveType: 3g` | `static` | `slow-network` | none | 0 | revealed |
| viewport 375 px | `static` | `small-screen` | none | 0 | revealed |
| viewport 768 px | `static` | `small-screen` | none | 0 | revealed |
| 4g, desktop, motion allowed | `playing` → `held` | — | `orbgss-hero.webm` | 0 | revealed at the hold |

The playing case was followed frame by frame to the end:

```
t=0.52  playing   handoff hidden
t=2.34  playing   handoff hidden
t=4.16  playing   handoff hidden
t=5.98  playing   handoff hidden
t=7.80  playing   handoff hidden
t=9.62  playing   handoff REVEALED     <- accepted regional hold begins at frame 200 = 8.33 s
t=11.44 playing   handoff revealed
t=11.50 held      handoff revealed     <- settles on the final frame, which is the poster frame
```

Intrinsic size read back as 1920 × 1080, duration 11.5 s. **Zero `<source>` children in every
case**, so no browser can be made to fetch both encodes.

One incidental confirmation: the browser used for verification genuinely reports
`effectiveType: "3g"` at 1.55 Mbps, and the page correctly refused to fetch a 2.87 MiB video on it
without being told to. That was not a stub.


---

## 8. Accessibility, navigation and localization

| Check | Result |
| --- | --- |
| Focusable elements on the homepage | 23, in DOM order matching visual order |
| Elements with no visible focus ring | **0** |
| Landmarks | `banner`, `main`, 2 × `navigation`, `contentinfo` all present; skip-link target resolves |
| Heading order | `h1` → `h2` ×4 → `h3` ×3 → `h2` ×2; no level skipped |
| Hero video in tab order | no (`tabindex="-1"`) |
| Canonical routes | `/`, `/platform/`, `/solutions/`, `/pilot/`, `/company/`, `/contact/` — all HTTP 200, plus `/404.html` |
| Broken images across all routes | **0** |
| EN/TR visible-copy parity | complete — every measured string differs between languages |
| EN/TR accessible-name parity | complete — `aria-label`s, `alt` text and `<title>` all switch |
| `<html lang>` | switches `en` ↔ `tr` |
| `aria-pressed` on EN/TR | tracks selection |
| Language persistence | `localStorage['orbgss.lang']`, survives reload and route change |

Every mandatory scientific warning is present as **static HTML** in both languages, so a reader with
JavaScript disabled still sees it. The validator was extended to prove this per route rather than
only on the homepage: a warning must now be rendered on *every* route that displays its asset —
which matters now that the WEB-002 proof assets live on `/pilot/` and no longer on the homepage.

### Screenshot evidence

Captured from the running local preview at each required width. All four acts are covered at
desktop; the acts that change layout are covered at every width.

| Width | Act 1 hero | Act 2 context | Act 3 evidence | Act 4 priority |
| --- | --- | --- | --- | --- |
| 375 (mobile) | ✅ static poster, handoff strip, caption | ✅ stacked | ✅ single column | ✅ contained + in-frame legend |
| 768 (tablet) | ✅ static poster, handoff strip | ✅ stacked | ✅ two-column wrap | ✅ contained |
| 1024 | ✅ measured (no overflow, acts stacked) | ✅ | ✅ two-column | ✅ 624 px contained |
| 1440 (desktop) | ✅ video held on final frame, handoff card | ✅ coupled split | ✅ three cards | ✅ contained + legend inside frame |

Capture method: the Claude browser pane at an emulated viewport, served from
`py -3.14 -m http.server 8080`. Widths larger than the pane are scaled down for capture, so the
screenshots evidence *layout*; the numeric claims in §5, §8 and §10 come from direct measurement of
the live DOM rather than from the images.


---

## 9. Validators

| Validator | Result |
| --- | --- |
| `py -3.14 scripts/validate_site.py` | **PASS, 0 warnings** |
| `py -3.14 hero/scripts/validate_hero.py` | **PASS — 184 checks, 0 failed** |
| `py -3.14 scripts/negative_tests_web005.py` | **12/12 deliberate regressions caught**; tree restored byte-identically |
| `git diff --check` | clean |
| `node --check script.js` | OK |

### The new checks were proved to have teeth

A check nobody has seen fail is a check nobody has tested, so every WEB-005 invariant was
deliberately violated and the validator confirmed to fail on it. `scripts/negative_tests_web005.py`
mutates one real file per case, runs the relevant validator, and restores the file in a `finally`
block; the run ends by proving both validators produce output identical to the baseline.

| # | Deliberate regression | Caught by |
| --- | --- | --- |
| 1 | Act 2 loses its `data-act`, leaving three acts | site |
| 2 | A fourth evidence card is added | site |
| 3 | The superseded `story-section` component returns to the homepage | site |
| 4 | The hero video gains an eager `<source>` child | site |
| 5 | An act anchor is renamed, breaking `#priority` | site |
| 6 | The priority map is laid out at 900 CSS px — 1800 device px at 2×, past its 1249 ceiling | site |
| 7 | A placed package asset loses its `web_005_placement` record | site |
| 8 | An accepted derivative's recorded SHA-256 drifts from the file | site |
| 9 | A layer slot claims the governed raster is baked into the render | hero |
| 10 | The production fixture claims to be the analysis AOI | hero |
| 11 | An accepted design fixture is quietly reclassified as production geometry | hero |
| 12 | A scientific layer is smuggled into an accepted pre-data scene | hero |

**12/12 caught.**

### What was added to the validators

`scripts/validate_site.py`:
- exactly four acts, in order, with their anchors present;
- exactly three evidence cards;
- the superseded `story-section` / `story-beam` / `layer-switch` components fail the build;
- scientific imagery provenance now accepts either accepted package (`web_002.proof_assets` or
  `geo_web_002.assets`) and rejects anything in neither;
- mandatory warnings checked **per route that shows the asset**, in both languages and in static
  HTML, instead of on the homepage only;
- `web_005_placement` required for any placed package asset, including a checked
  `max_css_width × dpr ≤ max_safe_rendered_px.device_px`;
- hero media: every file recorded with container, codec, dimensions, frame rate, duration, bytes and
  SHA-256, all recomputed, all ceilings enforced; a `<source>` child or `src` on the hero video
  fails the build; no hero asset may appear in the markup without a record;
- a detached homepage scale strip fails the build.

`hero/scripts/validate_hero.py`:
- the pre-data guarantee narrowed rather than dropped: the four accepted scenes must still name no
  scientific layer, and both design fixtures must stay classified as design fixtures;
- a populated layer slot must carry a complete provenance and presentation contract, name an
  accepted GEO-WEB-002 asset, deliver a file that exists, and declare `render_surface`;
- a production fixture must disclaim being the analysis AOI and record where its geometry came from;
- lane isolation became lane *boundary*: in `integration` mode, public-site changes must stay inside
  the declared write surface, and only allowlisted hero files may name a public-site path.

Check counts: hero validator **151 → 184**; site validator additions listed above.

---

## 10. Performance regression against the WEB-004 baseline

Measured by loading the built page in a real browser with every asset cache-busted, and summing
`PerformanceResourceTiming.encodedBodySize` — actual bytes over the wire, not a reading of the
markup.

| | WEB-004 accepted baseline | WEB-005 | |
| --- | --- | --- | --- |
| Mobile (375 px) total transfer | 645.1 KiB | **646.0 KiB** | ≈ unchanged |
| Mobile video bytes | n/a | **0** | ✅ |
| Mobile poster fetches | 1 | **1** (900 w, 39.4 KiB) | ✅ |
| Desktop (1440 px) encodes fetched | n/a | **1** (WebM, 2 866.9 KiB) | ✅ never both |
| Desktop total excluding hero video | — | 1 015.2 KiB | — |
| Layout shift from hero media | 0 | poster and video share one box with explicit `width`/`height` | ✅ |

The mobile figure is the one that matters against the WEB-004 floors, because Lighthouse's mobile
profile is what those floors were measured on — and on that profile the hero costs **zero video
bytes** by design. Desktop pays 2.87 MiB for the hero, once, after `load`, inside the accepted
3.0 MiB envelope.

Both poster candidates resolve correctly: the `<link rel="preload" imagesrcset/imagesizes>` and the
`<img srcset/sizes>` agree, so exactly one poster is fetched at each width — the trap WEB-004 called
out explicitly.

**`LIGHTHOUSE_NOT_RUN — tooling unavailable.`** The WEB-004 floors (Performance ≥ 90, Accessibility
/ Best Practices / SEO ≥ 95) were measured with Lighthouse 13.4.1, which is not installed on this
machine and would be a new dependency. Rather than report an unverifiable score, the things that
actually moved are measured directly above and in §5 and §8. The two accepted WEB-004 deviations are
unchanged: `priority-800.webp` is still the LCP-adjacent heavy proof derivative and is still not
re-encoded, and the score legend is still not re-proportioned.

One honest limitation, carried from the accepted package rather than introduced here: **the smallest
class-B derivative is 800 px**, so a 375 px phone is served an 800 px file for a ~345 px slot.
Producing a smaller one requires the Science export path, which WEB-005 may not touch. It is raised
in §12.

---

## 11. Scope discipline

Not done, deliberately: no merge to `main`; no deployment; no Vercel project or domain change; no
DNS, MX, SPF, DKIM, DMARC or Workspace change; no analytics, tracking, cookies, CRM, auth, database,
forms backend or PII capture; no framework, package manager, CMS or runtime dependency; no new
route; no new or reinterpreted science; no new public claim; no force-push, amend, rebase or history
rewrite; no WEB-006 work.

Scientific semantics are unchanged. The published score is still
`mvp_remote_sensing_priority_v1`, public label **Remote-Sensing Relative Priority — Experimental
Baseline**, an AOI-relative 0–100 screening surface — never probability, Full Prospectivity,
reserve/resource, discovery or drilling-success likelihood, and never a cross-AOI calibrated score.

### `NOT RUN` items

- **`HOSTED_PREVIEW_NOT_RUN — permission unavailable.`** No Vercel CLI, project link or token is
  present on this machine, and obtaining one would require credentials/ownership action the task
  places out of scope. No credentials were requested and no account state was touched. A
  reproducible local preview is provided instead, which the task accepts as sufficient for review.
- **`LIGHTHOUSE_NOT_RUN — tooling unavailable.`** The WEB-004 performance floors were measured with
  Lighthouse 13.4.1, which is not installed here. Direct measurements of the things that moved are
  given in §10 instead of an unverifiable score.
- **`CONTACT_RELEASE_GATE` remains open** and is not WEB-005's to close: mailbox ownership and
  deliverability for `contact@orbgss.com` require Workspace access. Every mailto on both languages
  targets the correct address.

---

## 12. Recommendations for Product (not blocking)

1. Correct the terminal-acceptance pointer in `tasks/WEB-005_CINEMATIC_HERO.md` from `e95fdca` to
   `573f4f1` (§0).
2. The accepted GEO-WEB-002 package's smallest class-B derivative is 800 px, so a 375 px phone is
   served an 800 px file for a ~345 px slot. Fixing that properly means a smaller derivative from
   the Science export path, which WEB-005 may not create. Worth a Science-side request if mobile
   transfer becomes a launch concern.
3. Deep routes still apply `text-transform: uppercase` to metadata lines containing the exact
   scoring-profile identifier. WEB-005 removed that on the homepage so the identifier renders as
   authored; `/pilot/` and `/platform/` were left alone as out of scope.
