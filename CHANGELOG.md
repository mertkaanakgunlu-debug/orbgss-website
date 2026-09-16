# Changelog

## v0.9.0-web-hero-001d-predata-animatic — 2026-09-16 (WEB-HERO-001D, branch `feat/web-hero-001-predata-scene`)

Assembles the accepted Phase A–C systems into one continuous pre-data hero animatic and closes the three quality-gate items Phase C left open. Phase C is consumed, not redesigned: `benchmark_neutral`, `hero_earth_orbit` and `hero_aoi_acquisition` are byte-identical in `scene.json` to their accepted definitions, and every builder addition is entered only when a scene spec asks for it.

- new scene `hero_predata_animatic` `extends` `hero_aoi_acquisition`: 240 frames at 24 fps (10.0 s) running Earth establish → satellite entrance → AOI acquisition and scan → continuous camera approach → stable regional AOI hold, as one scene, one world and one uncut camera move. Frames 1–96 replay the three accepted Phase-B establish camera states verbatim, re-timed onto a beat map that starts acquisition earlier so the shot can end on a real 1.7 s hold;
- **the camera path is derived from the AOI, not typed by eye.** `hero/scripts/shot_plan.py` converts a high-level `shot_intent` — be 13° off the footprint at a geocentric radius of 7.55 BU on a 44 mm lens — into world keyframes, resolving the AOI centre through `aoi_system` and rotating it by the Earth's own animated rotation at that frame. The validator re-derives the committed keyframes and fails if they have drifted from their intent, so the shot plan cannot become a story told about numbers someone later nudged;
- **camera aim is locked by constraint, the way Phase-C beams are.** Authored keyframes can only be correct *at* a keyframe: the footprint travels an arc on a rotating planet while an interpolated camera aims along a chord, so it drifts in between. A Track To constraint on the AOI centre empty, with keyframed influence, removes that residual. Influence is 0 through the establish so the planet can sit off-axis for the headline, and 1 from frame 136. Measured AOI centre error after handover is **0.0** frame widths;
- **atmosphere rebuilt from the right physical parameter.** Every previous shell drove brightness from Fresnel, a property of the shell *surface* rather than of the air a ray crosses, which is why it kept producing a hard-edged hoop; shaping it into a band only moved the edge, and a Mix Shader made it paint a solid teal band across the sky once the camera was low enough to see it edge-on. The new `limb_airmass` profile computes each view ray's perigee in the shader (camera position recovered from Incoming × View Distance), then `exp(-max(0, h-R)/H) · min(sec i, √(2πR/H))` — exponential decay above the limb, real air mass across the disc, combined with Add Shader because air adds light rather than occluding. The shell has no visible edge at any distance, and the planet is hazy at its horizon and clean at nadir;
- **closest-approach sharpness**: Earth albedo moved to the 8192×4096 member of the same already-cleared NASA Visible Earth record (57735) — same scene, clouds, projection and geography at four times the linear resolution, so the accepted world-coordinate convention and the AOI's longitude offset carry over unchanged. Texture magnification at the regional hold drops from about **14× to 3.9×** at evidence resolution. Sampling set to Cubic;
- **regional hold tuned against measured framing, not appearance**: 1 179 km altitude, 1 963 km slant range, 44 mm, AOI filling 26.1 % of frame width at 59.9° incidence with the limb crossing the top edge. The approach was tuned against incidence and metres-per-render-pixel because pushing closer trades surface sharpness and Earth curvature against footprint size, and that trade is easier to settle with numbers than with renders;
- **headline-safe space is measured, not asserted**: the reserved region (x 0.05–0.38, y 0.16–0.78) was widened until the planet first intruded and then stepped back to the last width that stays completely clear through frame 96. `shot_plan.py` ray-casts a 28×28 grid of it per keyframe; worst occupancy through the establish is **0.0**;
- `hero/scripts/audit_shot.py` measures the *evaluated* camera every frame and turns the cinematography contract into eight numbers: AOI centre lock 0.0, worst apparent-size reversal −0.000276, worst orientation step 0.215°/frame, camera jerk ratio 0.137, lens rate 0.206 mm/frame, cut ratio 2.48, zero frames with the AOI out of shot, headline occupancy 0.0. All pass;
- `hero/scripts/render_animatic.py` renders the whole range from a single scene build (an 8K albedo costs seconds to decode per build) and reports engine, device, duration, size and SHA-256. Video goes through Blender's own bundled FFmpeg, so the lane still depends on nothing but Blender. It is explicitly a *review* artifact: container, bitrate, poster frame and reduced-motion packaging remain WEB-005 decisions;
- Phase-C geometry validation re-run on the new scene and still green: worst radial deviation **0.726 m**, worst beam tip error **2.249 m**, beam root error **0.0 m**, footprint edge spread **0.019 km**; the secondary fixture passes unchanged;
- `validate_hero.py` grew 117 → 151 checks with the Phase-D continuity contract (one AOI system, ordered and in-range beats, a hold long enough to receive a reveal, an approach that overlaps the establish, a monotonically closing camera, keyframes matching their derivation, a clear headline region, an atmosphere shell that clears its own falloff). Verified against eight deliberate regressions, all caught;
- **reproducibility proven with a same-session A/A control.** A single repeat render underestimates the Cycles+OptiX noise floor: `hero_earth_orbit` frame 120 first measured 3.0 / 0.012 % from one repeat pair, which made the accepted-versus-current result look like a regression at 9.0 / 0.087 %. Rendering that frame three times per tree and cross-comparing every pairing showed the real floor is 9.0 / 0.086 % — including the accepted tree disagreeing with *itself* by exactly the amount it disagrees with the Phase-D tree. The accepted Phase-C tree was extracted whole from `6593a80` and rendered in the same session, so each comparison differs in one thing only. Recorded in `hero/evidence/phase_abc_reproducibility.json`; the accepted Phase-C record is left in place beside it;
- six Cycles evidence stills, a 16-frame Cycles continuity sheet, both geometry audits, the shot audit, the shot-plan framing report and the animatic pointer/hash committed under `hero/evidence/`; the 4.8 MB animatic itself stays out of Git by lane policy and is cited by path and SHA-256;
- one latent bug fixed in passing: `hero_common.resolve_scene_spec` referenced an undefined `hc` in its own module, so a missing scene raised `NameError` instead of the intended `KeyError`;
- no fabricated scientific layer, no real-data visualization, no homepage integration, no production media packaging, no deployment and no DNS change.

## v0.8.0-web-hero-001c-aoi-acquisition — 2026-09-16 (WEB-HERO-001C, branch `feat/web-hero-001-predata-scene`)

- accepted the WEB-HERO-001B Earth/satellite/camera scene at `e35bb16`; implemented WEB-HERO-001C on the same branch;
- built the `hero_aoi_acquisition` scene: it `extends` `hero_earth_orbit` instead of copying it, reuses the 001B camera keyframes verbatim for frames 1–120, and continues that same move to frame 240 through acquisition and regional approach — one scene, one camera path, one AOI identity, no cut;
- `hero/scripts/aoi_system.py` owns every AOI coordinate conversion and sampling decision and imports no `bpy`, so `validate_hero.py` checks the same numbers the renderer uses without launching Blender;
- AOI corners come from the spherical destination formula applied to the configured centre/span/bearing; edges and interior are sampled by slerp between unit vectors and scaled by one radius, so sphere conformance is true by construction rather than by tuning — measured worst radial deviation is 0.68 m on a 6 371 km radius, which is single-precision transform error;
- border and corner-lock ribbons are widened by rotating each sample *within its own tangent plane*, so both rails stay on the sphere instead of a flat strip being stretched over it;
- beam registration is structural, not keyframed: each beam is a unit-length tapered tube with Copy Location on the satellite and Stretch To on its corner empty, so an endpoint is derived from the AOI every frame rather than being a constant that happens to match on one; measured tip-to-corner error stays at 2.2 m on beams up to 11 000 km;
- the scan sweep is a band in the interior mesh's own AOI-local UV space, so it travels across the footprint without any possibility of detaching from the surface;
- generated meshes are face-oriented by comparing each face normal against the direction it should face; a wrongly wound blended face renders as *nothing*, which cost a debugging pass when the footprint fill was present, correct and invisible;
- the beams appearing to stop short of the AOI in EEVEE was blend-sorting against the atmosphere shell, not a geometry error — Cycles, the actual quality target, resolves them correctly; preview iteration on this scene should not be trusted for beam/footprint occlusion;
- atmosphere shell gained an optional `silhouette_fade_start`, off unless a scene asks for it: 001B never flew close enough for the shell's hard outer edge to show, and at approach distance it became a straight-edged wedge across frame; `hero_earth_orbit` does not set it and rebuilds unchanged;
- `validate_hero.py` grew 81 → 117 checks covering the AOI contract (points on the configured sphere, offset small enough to be a z-fighting guard rather than an altitude, four uniquely named corners, edges measuring the configured span, chord-to-arc sagitta ≤ 50 m, beams targeting the AOI system, no literal coordinate in an `aoi_system` spec, two fixtures resolving to genuinely different footprints); verified against nine deliberate regressions, all caught;
- `hero/scripts/audit_aoi.py` measures the *built* scene in world space per frame; both fixtures pass all five checks;
- discovered and documented that the Cycles+OptiX GPU path is not bit-reproducible here, so Phase A/B reproducibility is proven by pixel measurement against the renderer's own noise floor (`hero/scripts/compare_renders.py`, `hero/evidence/phase_ab_reproducibility.json`) rather than by checksum;
- four Cycles evidence stills, a continuity contact sheet and a fixture A/B comparison committed under `hero/evidence/`, plus both geometry audits;
- no new external asset (the whole AOI system is procedural), no scientific layer, no homepage integration, no deployment or DNS change.

## v0.7.1-web-hero-001b-visual-revision — 2026-09-16 (WEB-HERO-001B visual-acceptance revision, branch `feat/web-hero-001-predata-scene`)

Narrow visual-polish revision on the reviewed WEB-HERO-001B scene; no composition, geography, camera-path, or scope change.

- satellite no longer casts a shadow onto Earth (`visible_shadow = False` on every satellite part) — at review size the cast shadow read as a stray planning-marker/overlay mark on the surface rather than a deliberate detail, so it is suppressed;
- satellite hull and solar panels gain a shared, reusable Fresnel-gated rim-light (`_apply_rim_light`) so the satellite keeps a crisp, legible silhouette against both deep space and sunlit Earth; panel grid cells enlarged (`cell_scale` 7→4) and thickened for clearer "solar panel" read at hero scale;
- atmosphere rim narrowed and thinned (`falloff_min` 0.25→0.45, `fresnel_ior` 1.15→1.08, `strength` 2.4→1.5) and, more importantly, now scales with the same sun-direction term the Earth material's terminator uses, so the glow is bright on the day limb and fades to a faint hint on the night limb instead of a uniform, physically-detached outline;
- starfield rebuilt as two Voronoi layers (bright/sparse + dim/dense) with per-star brightness pulled from Voronoi's own colour output, plus a very-low-contrast large-scale noise brightness drift ("restrained star/nebula depth" from the original locked composition) — replaces the single uniform-threshold layer that read as an obviously repeating procedural grid;
- three representative Cycles evidence stills re-rendered and replaced in `hero/evidence/` at the same frames (1/60/120); Phase A validator (81 checks) and benchmark re-verified green, since the touched builder functions are shared with the `benchmark_neutral` scene.

## v0.7.0-web-hero-001b-earth-satellite — 2026-09-15 (WEB-HERO-001B, branch `feat/web-hero-001-predata-scene`)

- accepted the WEB-HERO-001A production scaffold and benchmark at `81a0b89`; implemented WEB-HERO-001B on the same branch;
- built the `hero_earth_orbit` scene: true 3D Earth (256×128-segment sphere) with a real day/night material, a Fresnel atmosphere shell, a procedural Voronoi starfield, and a procedurally-modelled Earth-observation satellite (bus, twin solar panels, nadir dish, instrument boom) on a keyframed orbital-entrance path;
- Earth day/night material blends a NASA Blue Marble day/cloud composite against a NASA Black Marble night-lights composite via a `dot(normal, fixed sun direction)` terminator factor computed at shader-build time from the scene's authored sun light — independent of the texture's own longitude placement, so lighting stays stable regardless of how the map is rotated into place;
- longitude placement uses a Mapping-node U-axis *translation* (Repeat wrap), not a 2D UV rotation — an initial rotation-based approach silently folded the map near the seam and produced unpredictable geography; fixed and documented in `build_scene.py`;
- satellite is fully procedural (no external geometry asset); a `TRACK_TO` constraint keeps it nadir-pointing at Earth across the whole keyframed path, so no per-frame orientation math is needed as the path is extended in later phases;
- `scene.json` gained a shared `world_coordinate_convention` (1 BU = 1000 km, Earth centred at the origin, +Z = rotation axis, longitude 0°/latitude 0° on +X at frame 1) for WEB-HERO-001C/D to build on without a scene reset; per-scene `world_overrides` (starfield) so the Phase A benchmark scene renders unchanged; camera/object keyframe schemas; a `satellite` object type;
- two NASA public-domain Earth composites recorded in `hero/assets/manifest.json` with source URL, publisher, license and SHA-256 (`land_ocean_ice_cloud_2048.jpg`, `dnb_land_ocean_ice.2012.3600x1800.jpg`); no other external asset;
- three representative Cycles evidence stills committed under `hero/evidence/` (establish / satellite-entrance / pre-acquisition) plus a 7-frame low-cost EEVEE preview sequence (local, not committed) showing the full rotation/entrance arc;
- no AOI, scan geometry or scientific layer introduced; Phase A validator (81 checks) and benchmark path re-verified green; no public-site, imagery, deployment or DNS change.

## v0.6.1-web-hero-001a-scaffold — 2026-09-15 (WEB-HERO-001A, branch `feat/web-hero-001-predata-scene`)

- established the isolated Blender production workspace under `hero/`: configuration-driven scene and render truth, Blender-Python entrypoints, a rights manifest and a workspace validator;
- `hero/config/` holds the lane boundary and pinned baseline (`lane.json`), the palette, camera defaults, scene definitions and AOI data-injection interface (`scene.json`), and the render profiles, 16:9 aspect contract and GPU preference order (`render_profiles.json`);
- three render profiles: `preview` (EEVEE, fast iteration), `master` (Cycles 1920×1080, 256 samples, OptiX denoise, 16-bit, never committed) and `evidence_still` (same Cycles path at reviewable 8-bit size, committed as bounded evidence);
- truthful render-device selection: walks the configured preference order, requires a backend to actually have a device behind it, falls back to CPU gracefully and records what was used rather than what was requested;
- `render.engine`, `compute_device_type` and `cycles.denoiser` are dynamic Blender enums that report nothing through `bl_rna`, so they are probed by assignment; reading `enum_items` silently hid Cycles and every GPU backend;
- `hero/scripts/validate_hero.py` runs without Blender and fails on a missing scaffold, unparseable or inconsistent configuration, a broken aspect/profile contract, an invalid or unlicensed asset entry, a scientific layer declared while pre-data, generated output promoted to source authority, or drift in the protected public-site paths; 68 checks, verified against five deliberate negative cases;
- benchmarked on Blender 4.5.10 LTS with an NVIDIA GeForce RTX 4070 Laptop GPU: preview 1.68 s, master 4.72 s, evidence still 1.97 s (warm shader cache); evidence in `hero/evidence/`;
- no external asset introduced, no scientific layer, no public-site, imagery, deployment or DNS change; the site validator still passes at the WEB-001 baseline.

## v0.6.0-web-001-vnext-foundation — 2026-09-15 (WEB-001, branch `feat/web-001-vnext-foundation`)

- published the repository-local vNext authority (`docs/WEB_VNEXT_AUTHORITY.md`) and the WEB-001 contract (`tasks/WEB-001_VNEXT_FOUNDATION.md`) before feature code;
- rebuilt the homepage as an evidence-to-intelligence story while keeping the beam → full-width panel gallery rhythm: Hero → 01 Observe → 02 Terrain → 03 Evidence → 04 Structure → 05 Priority → 06 Geothermal → Pilot ledger → Company/Trust → Contact → Footer;
- static poster hero (`Earth data. Evidence. Priority.` / `Know where to look next.` / `Explore the Platform`), built so WEB-005 replaces only the visual layer;
- navigation: Platform / Solutions (Geothermal Exploration, Mineral Exploration, Environmental & Land Intelligence) / Pilot / Company / Contact / EN | TR; all anchors real; disclosure and mobile behaviour unchanged;
- technical beams now carry index, title, statement and a monospace descriptor; scene labels moved to the monospace treatment; story panels add a `Natural-color composite` line;
- pilot ledger marks Geothermal `Active · First application`, Mineral and Environmental & Land `Expansion direction`; company block with restrained trust list; contact beam;
- temporary story visuals reuse the four provenance-safe Landsat composites (marked `data-visual-slot` / `temporary-gallery`; placement recorded in `sources.json`); no scientific outputs fabricated; WEB-002 owns replacements;
- full EN/TR parity for every new string;
- validator extended to the vNext anchors and visual-slot discipline; PASS with 0 warnings.

## v0.5.1-nav-labels-bilingual — 2026-09-09 (ORBWEB-001.1)

- replaced the metadata strips under every satellite image with a bottom-right on-image location + coordinates label (no background container, subtle text-shadow only); sensor/date remain in the manifest and rights documentation;
- rebuilt desktop navigation: right-aligned Home → Solutions (dropdown: Geothermal, Mining, Marine) → About → Partner With Us → EN | TR; Home cyan underline; Partner With Us as a plain item;
- Solutions dropdown as an accessible disclosure: hover, focus and click open; Escape, click-outside and focus-out close; ArrowUp/Down/Home/End move through items; tap-to-expand on mobile;
- added client-side EN/TR bilingual support (`I18N` dictionary in `script.js`): instant switch, scroll preserved, `<html lang>`, title, meta/og descriptions, alt texts and mail subjects update, choice persisted in `localStorage`, English default;
- footer navigation now Home / Solutions / About / Contact; footer is the `#about` anchor;
- design and product authority docs updated so the new decisions are canonical;
- imagery, provenance, pipeline and product claims unchanged; validator PASS with 0 warnings.

## v0.5-production-imagery — 2026-09-09

- populated all four production scenes as self-hosted OrbGSS natural-color composites built from USGS Landsat Collection 2 Level-2 surface reflectance (public domain);
- added `scripts/build_imagery.py` (reproducible crop/stretch/encode pipeline; `--record` writes render provenance into the manifest);
- pinned Landsat product identifiers, crop geometry, stretch parameters and rendered bounds per scene in `assets/imagery/sources.json`;
- removed the remote NASA Earth Observatory fallback dependency (`data-fallback`, preconnect) while keeping graceful image-failure behavior;
- updated footer attribution and `IMAGERY_RIGHTS.md` for the live asset provenance;
- removed `scripts/fetch-imagery.py` (superseded by the build pipeline);
- validator passes with zero warnings.

## v0.4-claude-handoff — 2026-09-09

- added canonical Claude Code bootstrap authority (`CLAUDE.md`);
- added current state pointer (`STATUS.md`);
- documented locked visual direction and product/content boundaries;
- documented Squarespace → Vercel deployment guardrails;
- added bounded continuation tasks;
- added site validator and handoff prompt;
- included visual-direction reference image;
- retained v0.3 page implementation and imagery provenance files.

## v0.3

- locked four visual scene roles and provenance manifest;
- local-first imagery paths with verified prototype fallback URLs;
- imagery rights/provenance documentation.
