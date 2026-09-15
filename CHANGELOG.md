# Changelog

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
