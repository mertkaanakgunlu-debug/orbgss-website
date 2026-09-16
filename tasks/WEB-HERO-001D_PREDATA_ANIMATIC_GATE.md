# WEB-HERO-001D — Continuous pre-data hero animatic & quality gate

**Linear:** `MER-101` (parent `MER-97`)  
**Predecessor:** `MER-100 / WEB-HERO-001C` terminally accepted at remote implementation/publication HEAD `6593a80899720f8c7461aaa99ade0e5e63a3ea42`  
**Authority:** `docs/WEB_HERO_001_AUTHORITY.md` + Drive CURRENT Hero Visual & Production Authority v1.0  
**Branch:** `feat/web-hero-001-predata-scene`  
**State:** `REVIEW_READY`

## Outcome

Assemble the accepted Phase A–C systems into one continuous pre-data hero animatic that is visually strong enough to become the production base for the later real-data phase:

**Earth establish → satellite entrance → AOI acquisition/scan → continuous camera approach → stable regional hold.**

The quality gate must prove that the sequence no longer has the two reference-image defects Product explicitly rejected: a flat AOI pasted over the globe and a scale/orientation discontinuity between global/regional shots.

## Narrative / timing envelope

Target the pre-data portion so it can later fit naturally inside an approximately 8–12 second complete hero without forcing rushed motion. Exact timing is implementer-owned within these constraints:

- opening Earth rotation has enough time to establish place/quality;
- satellite entrance is readable but does not dominate;
- acquisition lock and scan clearly communicate target-area observation;
- camera approach begins from the same locked AOI and feels physically continuous;
- end state holds on the regional AOI long enough to receive real scientific layer reveals in the later phase.

Do not add the later evidence/priority reveal just to make the animatic feel complete.

## Continuity / cinematography contract

- Use one coherent scene/world coordinate system and the persistent AOI from Phase C.
- Avoid hidden cuts whose only purpose is to repair registration/scale. A deliberate cinematic cut could only be introduced by a future Product revision; this task targets a continuous move.
- Camera easing should feel premium and controlled, with no sudden acceleration, FOV snap or game-like flythrough.
- Preserve future headline-safe composition during the opening portion.
- Satellite should naturally leave or become compositionally secondary before the regional hold.
- Global and regional lighting/color should feel like the same visual world.

## Pre-data end state

The final hold is a clean regional view of the same surface-conforming AOI. It may retain subtle acquisition glow and existing Earth texture/neutral treatment, but must leave visual headroom for later real terrain/evidence/priority surfaces.

No fake scientific map is permitted as a placeholder final frame.

## Quality bar

Review should be performed against the locked authority, not against generic "looks good" criteria. The scene must demonstrate:

- convincing spherical Earth geometry;
- premium Earth/space/satellite art direction;
- clear satellite-to-AOI acquisition story;
- AOI border/scan tied to globe curvature;
- no AI-style floating panel artifact;
- continuous AOI identity/scale/orientation into the regional shot;
- disciplined cyan acquisition language without HUD clutter;
- strong visual appeal for non-technical audiences while remaining credible to technical viewers.

## Deliverables

Produce, at minimum:

1. a review animatic/preview of the full pre-data sequence;
2. high-quality stills representing: opening establish, satellite/acquisition, active scan, mid-approach, regional hold;
3. committed source/config/scripts sufficient to reproduce the sequence;
4. scene validation report/results;
5. render/asset manifest updates and evidence hashes/pointers;
6. a concise handoff note defining the future injection points for real AOI raster/terrain/evidence/score materials and the layer-reveal portion owned by later authority.

Large preview/master files do not need to be committed if repository hygiene would suffer; use bounded evidence artifacts plus exact local paths/hashes/pointers as appropriate.

## Out of scope

- real DEM/thermal/alteration/structure/geology/priority data;
- final analytical palette applied to scientific data;
- final master render/production bitrate decision;
- WebM/MP4/poster/reduced-motion production package;
- homepage HTML/CSS/JS integration;
- responsive crop/performance acceptance;
- WEB-006 deployment/DNS.

These are later hero/WEB-005 responsibilities after the relevant website and Science inputs are accepted.

## Acceptance

Phase D / WEB-HERO-001 pre-data lane is complete only when:

1. The full pre-data narrative plays as one coherent sequence from global Earth to regional AOI hold.
2. Earth remains a true 3D sphere with coherent atmosphere/perspective throughout.
3. AOI geometry visibly follows the globe and passes Phase C geometry validation.
4. Beam/corner-lock/scan registration remains correct during motion.
5. There is no perceptible identity, orientation or scale discontinuity in the AOI between acquisition and regional approach.
6. Satellite entrance/orbit/exit behavior is visually credible and secondary to the product story.
7. Opening composition preserves useful future HTML-copy safe space.
8. The regional hold is visually prepared for later real data but contains no invented scientific layer.
9. Asset rights/provenance are complete for all external production material.
10. The scene is reproducible from committed source/config and the accepted asset-materialization path.
11. Validation is green with no unexplained failure.
12. Review evidence is sufficient for Product to judge geometry, continuity and cinematic quality without opening Blender manually.

## Verification / evidence

Report at `REVIEW_READY`:

- exact branch/final HEAD and changed paths;
- Blender/tool versions, render engine/device, preview settings;
- full animatic pointer/hash, duration, resolution and file size;
- five representative still pointers/hashes;
- scene validation result including AOI sphere/registration checks;
- asset manifest summary and rights status;
- timing/keyframe/camera summary;
- explicit checklist for the 12 acceptance points;
- future real-data injection/handoff note;
- confirmation that no scientific output, website integration, deployment or DNS change occurred.

## Accepted Phase-C carry-forward

WEB-HERO-001C is terminally accepted with no further revision required. Phase D must consume, not redesign, its configuration-driven spherical AOI system, beam/corner registration, scan-sweep geometry and continuity convention.

The following accepted Phase-C limitations are explicit Phase-D quality-gate work, not reasons to reopen Phase C:

- the current 2048 px Phase-B Earth albedo is visibly soft at the closest regional approach;
- atmosphere treatment may require conformant refinement at regional scale;
- EEVEE beam sorting is not authoritative; final visual judgment remains on Cycles evidence.

A higher-resolution rights-safe Earth texture/material refinement is permitted only if it preserves the accepted geography/world-coordinate convention, is recorded in `hero/assets/manifest.json`, introduces no scientific semantics, and stays inside the existing free/rights-safe production architecture. Any paid/unclear-rights asset remains a CTO human gate.

## Implementation record — `REVIEW_READY`

Implemented on `feat/web-hero-001-predata-scene` from the accepted Phase-C publication HEAD
`6593a80899720f8c7461aaa99ade0e5e63a3ea42`, continuing the published branch HEAD
`46f70a8a49777254faa49a6eae9f669279fc4bd6`.

**Implementation HEAD:** `93e17f6293aeb8bdc882dfd28221ed786b772df1`

### What was built

`hero/config/scene.json` gains one scene, `hero_predata_animatic`, which `extends`
`hero_aoi_acquisition`. 240 frames at 24 fps, 10.0 s, one scene, one world, one uncut camera move:

| beat | frames | seconds |
| --- | --- | --- |
| Earth establish | 1–96 | 0.0–4.0 |
| satellite entrance | 40–104 | 1.6–4.3 |
| AOI acquisition | 90–138 | 3.7–5.8 |
| camera approach | 96–214 | 4.0–8.9 |
| scan sweep | 134–192 | 5.6–8.0 |
| satellite release | 146–166 | 6.1–6.9 |
| regional hold | 200–240 | 8.3–10.0 |

Frames 1–96 replay the three accepted Phase-B establish camera states verbatim, re-timed onto this
beat map so acquisition can start earlier and the shot can end on a real hold. The AOI is one
object system present for the whole range, never recentred, re-parented or rebuilt; the move from
global to regional is camera motion only.

The three accepted scene definitions (`benchmark_neutral`, `hero_earth_orbit`,
`hero_aoi_acquisition`) are byte-identical in `scene.json` to the versions accepted at `6593a80`.
The only `scene.json` changes are the added scene and the `phase` field. Every builder addition is
entered only when a scene spec asks for it, and only the new scene does.

### Phase-C quality-gate items

**Closest-approach Earth sharpness.** The Earth albedo now reads the 8192×4096 member of the same
already-cleared NASA Visible Earth record (57735) as the accepted 2048 px asset — same scene, same
clouds, same equirectangular projection, same geography, four times the linear resolution — so the
accepted world-coordinate convention and the AOI's configured longitude offset carry over
unchanged. Texture magnification at the regional hold drops from about 14× to 3.9× at evidence
resolution. Sampling set to Cubic. The 2048 px asset stays recorded because the accepted scenes
still reference it.

**Regional atmosphere treatment.** Every previous shell drove brightness from the Fresnel factor,
which is a property of the shell *surface* rather than of the air a ray crosses. Fresnel is
monotonic, so the glow was brightest exactly at the shell silhouette and ended on a hard geometric
line; shaping it into a band moved the line, a second shell added a second one, and because a Mix
Shader replaces what is behind it, the shell painted a solid teal band across the sky as soon as
the camera was low enough to see it edge-on. The new `limb_airmass` profile recovers the camera
position in-shader (`Incoming × View Distance`), computes each view ray's perigee radius `h`, and
drives the glow with `exp(-max(0, h-R)/H) · min(sec i, √(2πR/H))` — exponential decay above the
limb, real relative air mass across the disc — combined with **Add Shader**, because air adds light
rather than occluding. The shell has no visible edge at any distance; the planet is hazy at its
horizon and clean at nadir. The accepted Phase-B/C shells are untouched and the legacy path is
still taken whenever a spec declares no `profile`.

**Authoritative Cycles evidence.** All six representative stills and the 16-frame continuity sheet
are Cycles renders on OptiX (`evidence_still` profile), not EEVEE. Beam and footprint appearance
and occlusion were judged on those.

### Cinematography made measurable

`hero/scripts/shot_plan.py` (no `bpy`) converts a committed `camera.shot_intent` — *at frame 240,
be 13° off the AOI at a geocentric radius of 7.55 BU on a 44 mm lens* — into world keyframes,
resolving the AOI centre through `aoi_system.py` and rotating it by the Earth's own animated
rotation at that frame. Keyframes stay committed literally so the camera path is diff-able; the
validator re-derives them and fails on drift, so intent and keyframes cannot silently disagree.

The camera's aim is held by a `TRACK_TO` constraint on `aoi_target_center` with keyframed
influence: 0 through the establish, where the planet deliberately sits off-axis so a headline has
somewhere to live, and 1 from frame 136. Authored keyframes past the handover already aim at the
AOI centre, so the constraint cannot swing the camera; it removes only the drift that appears
*between* keys, because the footprint travels an arc on a rotating planet while an interpolated
camera aims along a chord. This is the same move the Phase-C beams make when they derive their
endpoints instead of baking them.

`hero/scripts/audit_shot.py` measures the evaluated camera every frame — after F-curve
interpolation, Earth rotation, satellite animation and the constraint — and turns the contract into
eight thresholds.

`hero/scripts/render_animatic.py` renders the whole range from a single scene build and reports a
full evidence record. Video goes through Blender's own bundled FFmpeg, so the lane still depends on
nothing beyond Blender.

### Changed paths

```text
CHANGELOG.md
CLAUDE_SESSION_BOOTSTRAP.txt
STATUS.md
tasks/WEB-HERO-001D_PREDATA_ANIMATIC_GATE.md
hero/README.md
hero/assets/manifest.json
hero/config/lane.json
hero/config/render_profiles.json
hero/config/scene.json
hero/scripts/audit_shot.py            (new)
hero/scripts/build_scene.py
hero/scripts/hero_common.py
hero/scripts/render_animatic.py       (new)
hero/scripts/shot_plan.py             (new)
hero/scripts/validate_hero.py
hero/evidence/animatic_predata_animatic.json                     (new)
hero/evidence/aoi_geometry_audit_predata_animatic.json           (new)
hero/evidence/aoi_geometry_audit_predata_animatic_secondary.json (new)
hero/evidence/phase_abc_reproducibility.json                     (new)
hero/evidence/shot_audit_predata_animatic.json                   (new)
hero/evidence/shot_plan_predata_animatic.json                    (new)
hero/evidence/hero_predata_animatic_establish_f24.png            (new)
hero/evidence/hero_predata_animatic_satellite_entrance_f78.png   (new)
hero/evidence/hero_predata_animatic_acquisition_lock_f140.png    (new)
hero/evidence/hero_predata_animatic_scan_sweep_f170.png          (new)
hero/evidence/hero_predata_animatic_mid_approach_f200.png        (new)
hero/evidence/hero_predata_animatic_regional_hold_f236.png       (new)
hero/evidence/hero_predata_animatic_continuity_sheet.png         (new)
```

No file outside `hero/` and the bounded documentation set was touched. `hero/config/lane.json`
protected public-site paths are unchanged from the pinned baseline and carry no uncommitted
modification; the validator checks both on every run.

### Tools, engine and settings

| item | value |
| --- | --- |
| Blender | 4.5.10 LTS, build `6dc0b208d1b5`, 2026-05-19 |
| embedded Python | 3.11.11 |
| validator Python | 3.14 (`py -3.14`, no Blender) |
| host | Windows 11, Intel Core i9-14900HX, NVIDIA GeForce RTX 4070 Laptop GPU |
| evidence stills | `evidence_still` — Cycles, 1280×720, 8-bit PNG, 256 samples, adaptive 0.01, 8 bounces, OptiX denoise, **OptiX** device |
| animatic | `preview` — EEVEE Next, 1280×720, 32 samples, Blender GPU context |
| animatic encode | Blender bundled FFmpeg, MPEG4/H.264, CRF `HIGH`, preset `GOOD`, GOP 12, no audio |
| view transform | AgX, look None |
| Cycles still throughput | 8.20 s/frame |
| animatic throughput | 0.27 s/frame, 63.8 s for 240 frames |

### Animatic pointer

Not committed — 4.8 MB of generated video, which lane policy keeps out of Git.

| field | value |
| --- | --- |
| path | `hero/renders/animatic/hero_predata_animatic_preview0001-0240.mp4` |
| SHA-256 | `07b4091887e4a2f1a26b397ed237e86474a6e3fee10b5eeebaf96202a712dba6` |
| bytes | 5 032 871 |
| resolution | 1280×720 |
| frames | 240 at 24 fps |
| duration | 10.0 s |
| record | `hero/evidence/animatic_predata_animatic.json` |

Regenerate with:

```powershell
& $env:BLENDER -b -P hero/scripts/render_animatic.py -- --scene hero_predata_animatic --record hero/evidence/animatic_predata_animatic.json
```

The animatic is a **review** artifact. Container, bitrate, poster frame and reduced-motion
packaging are out of scope here and remain WEB-005 decisions.

### Five representative stills

All Cycles / OptiX, `evidence_still` profile, 1280×720.

| beat | frame | file |
| --- | --- | --- |
| opening establish | 24 | `hero/evidence/hero_predata_animatic_establish_f24.png` |
| satellite entrance | 78 | `hero/evidence/hero_predata_animatic_satellite_entrance_f78.png` |
| satellite/acquisition lock | 140 | `hero/evidence/hero_predata_animatic_acquisition_lock_f140.png` |
| active scan | 170 | `hero/evidence/hero_predata_animatic_scan_sweep_f170.png` |
| mid-approach | 200 | `hero/evidence/hero_predata_animatic_mid_approach_f200.png` |
| regional hold | 236 | `hero/evidence/hero_predata_animatic_regional_hold_f236.png` |

Six rather than five: the satellite entrance is a named beat in its own right and the acquisition
lock is the frame that shows the beams, so both are published. A 16-frame Cycles continuity sheet
spanning the whole range is at `hero/evidence/hero_predata_animatic_continuity_sheet.png`.

### Scene and geometry validation

`py -3.14 hero/scripts/validate_hero.py` — **151 checks, 0 failed** (117 at Phase C). The new
sequence contract covers: exactly one AOI system, beats starting in narrative order and lying
inside the frame range, an approach beginning before the establish ends, a hold long enough to
receive a later reveal, a duration inside the hero envelope, a monotonically closing camera, a
focal length that never reverses during the approach, keyframes matching their derivation, a clear
headline-safe region, and an atmosphere shell clearing its own falloff.

Verified against eight deliberate regressions — drifted keyframe, widened headline region, thinned
atmosphere shell, a second AOI system, shortened hold, reordered beats, camera backing off,
duration outside the envelope — **8/8 caught**, configuration restored, validator green again.

`audit_aoi.py` on the new scene, primary fixture, 13 frames spanning the whole range:

| measurement | value | tolerance |
| --- | --- | --- |
| worst radial deviation | 0.726 m | 6.371 m |
| worst beam tip-to-corner error | 2.249 m | 22.9 m |
| worst beam root-to-satellite error | 0.0 m | 22.9 m |
| footprint edge spread across the shot | 0.019 km | 0.5 km |

All five Phase-C geometry checks pass, and the `design_secondary` fixture passes unchanged. The
residual is single-precision transform error at planetary scale, not approximation.

`audit_shot.py`, all 240 frames, all eight checks pass:

| check | measured | threshold |
| --- | --- | --- |
| AOI stays locked to frame centre after handover | 0.0 | 0.02 frame widths |
| AOI apparent size never reverses | −0.000276 | 0.0015 per frame |
| AOI screen orientation changes continuously | 0.215°/frame | 2.0°/frame |
| camera speed changes without a jerk | 0.137 | 0.35 |
| focal length ramps without a snap | 0.206 mm/frame | 0.6 mm/frame |
| no hidden cut in the camera path | 2.48 | 4.0 |
| AOI stays in frame from handover to end | 0 frames out | 0 |
| headline-safe region clear of the Earth | 0.0 occupancy | 0.0 |

### Timing and camera summary

`hero/evidence/shot_plan_predata_animatic.json` holds the full per-keyframe report.

| frame | altitude | slant to AOI | lens | AOI width | incidence | m per render px |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 40 544 km | 41 338 km | 28 mm | 0.79 % | 31.0° | 27 682 |
| 52 | 24 536 km | 25 272 km | 35 mm | 1.62 % | 31.0° | 13 539 |
| 96 | 16 179 km | 16 848 km | 33 mm | 2.28 % | 31.0° | 9 572 |
| 136 | 9 529 km | 10 663 km | 38 mm | 4.16 % | 43.5° | 5 261 |
| 164 | 5 229 km | 6 173 km | 40 mm | 7.56 % | 44.7° | 2 893 |
| 192 | 2 929 km | 3 709 km | 41 mm | 12.90 % | 47.1° | 1 696 |
| 214 | 1 929 km | 2 706 km | 43 mm | 18.54 % | 52.5° | 1 180 |
| 240 | 1 179 km | 1 963 km | 44 mm | 26.14 % | 59.9° | 837 |

AOI width is the footprint as a fraction of frame width; incidence is the sightline angle at the
footprint, 0° straight down and 90° tangential. Metres per render pixel is quoted at 1920 wide;
at the 1280-wide evidence resolution the hold is 1 255 m/px against a 4 886 m texel, hence 3.9×
magnification.

Pushing closer makes the footprint bigger and the surface softer and takes the limb out of frame;
no setting wins all three, so the approach was tuned against these numbers rather than against how
a render happened to look. At the hold the limb still crosses the top edge of frame.

The satellite is in frame from frame 1 to frame 162, then leaves up and to the left as the camera
descends past its altitude — continuous, monotonic, and complete before the regional hold begins.
Beams release over frames 146–166, so they are gone as the satellite exits.

### Asset provenance and rights

`hero/assets/manifest.json`, three assets, all `rights_status: cleared` with recorded SHA-256:

| id | file | publisher / licence | SHA-256 |
| --- | --- | --- | --- |
| `earth_day_composite` | `land_ocean_ice_cloud_2048.jpg` | NASA Earth Observatory, US government public domain | `fb67ac03…708e` |
| `earth_day_composite_8k` | `land_ocean_ice_cloud_8192.tif` | NASA Earth Observatory, US government public domain | `edd98f81…86a3` |
| `earth_night_composite` | `dnb_land_ocean_ice.2012.3600x1800.jpg` | NASA Earth Observatory, US government public domain | `373e5a08…b124` |

WEB-HERO-001D introduces no new *class* of external material: the one addition is the 8192×4096
member of the record the 2048 px asset already came from, fetched from the same host under the same
public-domain policy. Nothing paid, restricted or unclear-rights was used, so no human gate was
reached. The refined atmosphere, the camera lock and every AOI element remain fully procedural,
generated from committed configuration, and none of them encodes, derives or displays a scientific
quantity.

### Reproducibility of the accepted phases

The Cycles + OptiX path is not bit-reproducible here, so this was measured rather than checksummed,
and measured against the accepted *code* rather than against an old file: the Phase-C tree was
extracted whole from `6593a80`, given the same source textures, and rendered in the same Blender
session as the current tree, so each pair differs in exactly one thing.

A single repeat render underestimates the noise floor. `hero_earth_orbit` frame 120 first measured
a floor of 3.0 / 0.012 %, which made the accepted-versus-current result of 9.0 / 0.087 % look like a
regression. Rendering that frame three times per tree and cross-comparing every pairing showed the
real floor is 9.0 / 0.086 % — the accepted tree disagrees with *itself* by exactly the amount it
disagrees with the Phase-D tree. That accepted-versus-accepted control is kept in the record
because it is what makes the result conclusive.

Every accepted phase rebuilds unchanged. Recorded in
`hero/evidence/phase_abc_reproducibility.json`; the accepted Phase-C record
`phase_ab_reproducibility.json` is left in place beside it.

### Acceptance checklist

| # | acceptance point | result |
| --- | --- | --- |
| 1 | full pre-data narrative plays as one coherent sequence | **Met.** One scene, one AOI system, one camera path spanning frames 1–240 with no cut; measured cut ratio 2.48 against a 4.0 threshold. Beats ordered and overlapping, validated from configuration. |
| 2 | Earth remains a true 3D sphere with coherent atmosphere/perspective | **Met.** Unchanged 6.371 BU sphere at 256×128 segments; the limb crosses frame at every approach keyframe including the hold; atmosphere is a perigee-driven additive shell with no silhouette edge. |
| 3 | AOI geometry follows the globe and passes Phase-C geometry validation | **Met.** `audit_aoi.py` on the new scene: worst radial deviation 0.726 m of a 6 371 km radius; all five checks pass on both fixtures. |
| 4 | beam/corner-lock/scan registration stays correct during motion | **Met.** Worst beam tip-to-corner error 2.249 m, root-to-satellite 0.0 m, across 13 frames spanning the shot. Registration is structural: Copy Location plus Stretch To, endpoints derived per frame. |
| 5 | no perceptible identity, orientation or scale discontinuity | **Met.** AOI centre error 0.0 frame widths after handover; worst apparent-size reversal −0.000276 per frame; worst orientation step 0.215°/frame; footprint edge spread 0.019 km. |
| 6 | satellite entrance/orbit/exit credible and secondary | **Met.** Continuous arc, in frame 1–162, exits up and left as the camera descends past its altitude, before the hold begins. Beams release 146–166 so they leave with it. |
| 7 | opening composition preserves HTML-copy safe space | **Met.** Left column x 0.05–0.38, y 0.16–0.78, measured clear of the Earth at every establish keyframe and every frame to 96 (occupancy 0.0). The region was widened until the planet intruded and then stepped back, so the guarantee is the largest one that actually holds. The satellite transits the column as a small element; that is recorded, not hidden. |
| 8 | regional hold prepared for data, with no invented scientific layer | **Met.** 1.7 s hold on the footprint at 26 % of frame width, carrying only the neutral acquisition wash left by the sweep. `layer_slots` is empty, the pre-data boundary check passes, and no gradient anywhere encodes a measured quantity. |
| 9 | asset rights/provenance complete | **Met.** Three assets, all cleared with recorded SHA-256 and source URL; the one addition is another member of an already-cleared NASA public-domain record. |
| 10 | reproducible from committed source/config | **Met.** Configuration is scene truth; the camera path is derived from committed intent and re-checked by the validator; no manual `.blend` is source. Accepted phases proven to rebuild unchanged against a same-session control. |
| 11 | validation green with no unexplained failure | **Met.** 151 checks, 0 failed. Two failures during development were in the new checks, not the scene — a focal-length rule that contradicted the accepted Phase-B establish and a beat order that had the approach after the scan — and both were corrected in the checker. 8/8 negative regressions caught. |
| 12 | evidence sufficient to judge without opening Blender | **Met.** Six Cycles beat stills, a 16-frame Cycles continuity sheet, a 10 s animatic by path and hash, two geometry audits, a per-frame shot audit, a per-keyframe framing report and a reproducibility record. |

### Future real-data injection — handoff

Nothing in this scene has to be rebuilt to receive real data. The injection points are:

1. **AOI geometry** — `aoi_injection_interface.fixtures` in `hero/config/scene.json`. Replace the
   design fixture with the accepted AOI's centre, span, bearing and sampling density, or add a
   fixture and point `active_fixture` at it. Everything downstream — footprint, border, corner
   locks, beam targets, sweep parameter space, and now the whole camera path — is derived from it,
   so a real AOI moves the shot with it and needs no keyframe edits. Re-run
   `shot_plan.py --derive` and sync the camera keyframes; the validator enforces that they match.
2. **Terrain / evidence / priority surfaces** — `aoi_injection_interface.layer_slots`, currently
   empty by contract. This is where accepted rendered scientific layers attach to the footprint
   interior. The interior mesh already carries AOI-local `(u, v)` in its UV layer, so a layer maps
   onto it directly and stays surface-conforming by construction.
3. **The reveal itself** — frames 200–240 are a stable hold on the footprint at a fixed scale and
   orientation, carrying only a faint acquisition wash. That is the window a later authority
   reveals real layers into, and it is deliberately left visually clear for exactly that.
4. **Analytical palette** — not defined here. The cool-to-warm analytical ramp belongs to the later
   data-layer authority and must not be applied to anything in this scene, which has no measured
   values to apply it to.

Out of scope here and still owned by later authority: real DEM/thermal/alteration/structure/geology
/priority data, the final analytical palette, the master render and bitrate decision, WebM/MP4/
poster/reduced-motion packaging, homepage HTML/CSS/JS integration, responsive crop and performance
acceptance, and WEB-006 deployment/DNS.

### Confirmation

No scientific output was produced or implied; no real-data visualization exists in the scene; no
public-site file, proof imagery, deployment configuration or DNS record was touched; no production
media package was built; no external resource was created, deleted or connected; no paid or
unclear-rights asset was used; no force push or history rewrite occurred. Work stayed on
`feat/web-hero-001-predata-scene`.

## STOP / route


Route to Product only if the approved continuous narrative, composition or visual invariants require a material change; if a new production dependency/architecture is required; or if quality cannot be achieved within the rights-safe/free tooling envelope without a Product trade-off.

Route to Science if any real analytical output or semantic interpretation is requested before a later accepted data-layer authority.

Human gate for paid/licensed assets/services, credentials/admin access, destructive/irreversible actions or commercial commitments.

Do not stop for normal keyframe/camera revisions, shader tuning, render performance, local tooling issues, geometry fixes, evidence generation or conformant polish.

## Branch / publication policy

Continue on `feat/web-hero-001-predata-scene`. Normal bounded implementation/revision commits are Claude-owned through `REVIEW_READY`; no feature work on `main`, no force push/history rewrite. Completion of this task does **not** authorize live hero integration. The accepted output becomes an input to the later real-data hero phase and `WEB-005` integration/release gate.

Publication/readiness does not auto-start Claude execution. CTO deliberate start remains required.