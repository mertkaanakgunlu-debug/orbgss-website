# WEB-HERO-001A — Blender production scaffold & render benchmark

**Linear:** `MER-98` (parent `MER-97`)  
**Authority:** `docs/WEB_HERO_001_AUTHORITY.md` + Drive CURRENT Hero Visual & Production Authority v1.0  
**Repository:** `mertkaanakgunlu-debug/orbgss-website`  
**Baseline:** `main@677bfa7672ac18c2c808ddaaf235ff12863de443`  
**Branch:** `feat/web-hero-001-predata-scene`  
**State:** `READY_FOR_CLAUDE_DESKTOP_START`

## Outcome

Create a reproducible local Blender production environment inside `hero/` that can build, validate and render the later hero scene at high quality without contaminating the website runtime architecture. Establish the source/config conventions, provenance discipline and a measured preview/master render benchmark on the available machine.

This is an enabling production outcome, not a requirement to finish the Earth/satellite art direction in this phase.

## Required scope

Establish a maintainable `hero/` workspace that includes, at minimum, the functional equivalents of:

- configuration for scene/render/shot parameters;
- Blender-Python scene bootstrap/build entrypoint;
- preview render entrypoint;
- bounded still/evidence render entrypoint;
- automated scene-contract validation entrypoint;
- asset provenance/license/checksum manifest;
- local generated-output directories and ignore policy;
- documented commands for a fresh operator/Claude session to reproduce the workspace.

The implementation may choose exact filenames/layout within the authority envelope; avoid unnecessary framework or package machinery.

## Production requirements

- Use Blender's Python API as the primary automation interface.
- Detect/document the installed Blender version and available render devices.
- Support a fast iteration profile and a high-quality profile. Fast iteration may use Eevee or low-sample Cycles; the high-quality target must use Cycles when available.
- Prefer NVIDIA GPU rendering when Blender exposes the compatible device; CPU fallback is allowed and must fail gracefully rather than hard-coding one machine path.
- Render settings must be configuration-driven rather than scattered magic constants.
- Default working aspect ratio is cinematic 16:9. Exact final website resolution/bitrate is intentionally deferred to WEB-004/WEB-005 performance authority.
- Do not add Blender/FFmpeg/Python tooling as a browser/runtime dependency of the website.

## Asset discipline

Create `hero/assets/manifest.json` (or an equivalently structured manifest) with fields sufficient to record:

- asset identifier and role;
- local materialized path when applicable;
- source URL/publisher;
- license/public-domain basis;
- checksum once materialized;
- notes/attribution obligations.

No paid or unclear-rights asset may be introduced. Large source assets should be reproducibly fetched/materialized or otherwise pointer-managed rather than committed blindly. Do not commit render sequences.

## Validation contract

Add an automated validation path that can fail clearly on broken production assumptions, including at least:

- expected directory/config presence;
- parseable configuration;
- no accidental scientific-layer asset declared in this pre-data phase;
- render profile consistency;
- asset manifest structural validity;
- generated-output directories not accidentally treated as source authority.

Do not over-engineer this into a general build system.

## Benchmark evidence

Create a minimal neutral test scene sufficient to benchmark the pipeline (camera + simple geometry + lighting is enough). Run representative preview and high-quality still renders and record:

- Blender version;
- render engine/device actually used;
- resolution/samples/denoise settings;
- wall-clock render time;
- output dimensions and file size;
- whether GPU acceleration was active;
- any machine-specific limitation.

The benchmark is for production planning, not a permanent quality target.

## Out of scope

- final Earth/space look;
- final satellite model;
- AOI/scan geometry;
- real or fake scientific layers;
- homepage HTML/CSS/JS changes;
- WebM/MP4 production encoding;
- Vercel/deployment/DNS;
- paid tooling/assets.

## Acceptance

Phase A is complete only when:

1. A fresh checkout of the branch has a clear documented path to materialize/build the Blender scene workspace.
2. Scene/config/render scripts run without relying on undocumented manual clicks.
3. A fast preview profile and a high-quality Cycles-capable profile exist.
4. Render device detection/fallback is truthful and recorded.
5. Asset rights/provenance structure exists and rejects/flags incomplete material where appropriate.
6. Generated outputs are kept out of source authority by ignore/pointer policy.
7. The validator passes on the committed scaffold.
8. At least one preview and one high-quality still benchmark are produced and recorded.
9. No public-site integration or scientific content is introduced.

## Verification / evidence

Report at `REVIEW_READY`:

- exact branch and final HEAD;
- changed paths;
- Blender version and Python version exposed by Blender;
- render device inventory and selected device;
- exact commands used for build/validate/preview/high-quality benchmark;
- validator result;
- benchmark table/results;
- evidence still pointer/hash;
- `hero/assets/manifest.json` summary;
- confirmation that `index.html`, `styles.css`, `script.js`, proof imagery, deployment and DNS were untouched.

## STOP / route

Stop for Product only if this requires a new website/runtime framework/dependency decision, a materially different repository architecture, or a change to the approved production boundary.

Human gate if paid/licensed assets, credentials/admin access, destructive action or commercial commitment becomes necessary.

Do **not** stop for normal Blender installation/path discovery, render-device configuration, local Python issues, shader/test-scene details, benchmark tuning, ignore-file updates, small conformant refactors or other routine production setup.

## Branch / publication policy

Continue on `feat/web-hero-001-predata-scene`. Normal bounded implementation commits are allowed. No feature work on `main`; no force push/history rewrite. Terminal phase state is `REVIEW_READY`. `WEB-HERO-001B` depends on this phase's accepted scaffold and benchmark evidence.