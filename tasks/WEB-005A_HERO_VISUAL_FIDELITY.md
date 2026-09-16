# WEB-005A — Hero Visual Fidelity, Orbital Choreography & Launch-Quality Motion

**State:** EXECUTION_AUTHORIZED / IN PROGRESS  
**Parent:** WEB-005 / MER-93 — terminally accepted  
**Canonical baseline:** `main@00af0f232a8d7d77f5ca61d758461ff7316ba151`  
**Implementation branch:** `feat/web-005a-hero-visual-fidelity`  
**Product visual authority:** `docs/WEB_005_POLISH_VISUAL_DIRECTION_AUTHORITY.md` on `docs/web-005-polish-authority`  
**Launch dependency:** must be terminally accepted before WEB-006.

## 1. Outcome

Raise the accepted WEB-005 homepage hero from structurally correct to launch-quality cinematic fidelity without changing the four-act homepage architecture or any accepted scientific/public semantics.

This is one bounded outcome: a visibly premium orbital-acquisition sequence whose satellite, camera path, sensing visualization, target frame, render fidelity and final handoff all read as intentional and finished.

The task incorporates the current bounded hero refinement already underway on `feat/web-005a-hero-visual-fidelity`; do not restart completed conformant work merely because this authority was published after execution began.

## 2. Required product behavior

The final sequence must preserve the accepted story while improving its visual execution:

Earth establish → generic EO satellite emerges around the Earth limb → readable orbital arc → acquisition attitude → restrained cyan sensing visualization → crisp target-frame activation → continuous regional approach → stable hold → intentional governed result/evidence handoff.

### Satellite

Use a rights-safe generic Earth-observation 3D satellite, or an in-repository model with equivalent visual quality. It must have enough real geometry/material response to avoid a flat-cutout silhouette: volumetric body, readable solar panels with thickness, material separation and restrained EO-platform detail.

It must not be represented as a specific operational spacecraft or specific sensor unless separate authority exists.

### Motion / camera

The satellite path must read as an orbital pass, not a foreground fly-by or arbitrary spline. It should emerge from the Earth-limb context, remain visually subordinate to the Earth, pass through an intentional acquisition composition and leave the viewer with a coherent sense of orbital motion.

Ordinary implementation strategy and exact keyframe solving are implementer-owned. The path may be numerically derived against the camera/framing rather than eyeballed.

### Sensing FX

Use the accepted cyan acquisition language from the Product visual authority. The effect must be thin, controlled and coherent with the satellite-target relationship. A soft cone/boresight, narrow scan band or restrained beam lines are conformant.

Rejected: thick fuzzy white slabs, noisy particles, game-like lasers, opaque geometry that obscures the Earth, or claims that the visualization is actual instrument physics.

### Target frame

The target outline/corner locks must be crisp and premium: thin border, controlled glow, clean registration language. Preserve accepted target registration/world geometry; do not silently move the accepted Kızıldere centre or redefine the analysis AOI.

### Ending / handoff

The final state must feel deliberately resolved, not like playback simply stopped. Registration/lock timing, camera settle and page-layer handoff should converge into a clear climax.

Governed scientific rasters/results remain page-layer/HTML handoff where lossy video would alter scientific colour meaning.

## 3. Media and fidelity contract

Preserve the accepted delivery behavior:

- WebM target/ceiling remains `<= 3.0 MiB` unless Product explicitly revises it after measured evidence;
- MP4 fallback remains `<= 4.5 MiB`;
- poster remains `<= 180 KiB`;
- no dual-video download;
- mobile/reduced-motion/reduced-data intentional static/fallback behavior remains intact.

Supersampling, denoising, render-sample changes, encoder preset tuning and other conformant quality work are implementer-owned.

If launch-quality fidelity is demonstrably impossible inside an existing ceiling, do not silently relax the ceiling. Publish exact before/after quality and byte evidence and return `WAITING_DOMAIN_DECISION` for that trade-off only.

### Earth-source-resolution clarification — Product R1

A demonstrated shortage of source texels in the cinematic Earth albedo/basemap is **not** a Product STOP by itself. WEB-005A explicitly authorizes replacing or augmenting the current cinematic Earth texture with a materially higher-resolution rights-safe Earth texture when needed to remove visible upscaling/softness in approved shots.

This is a presentation/source-fidelity change, not a scientific-data change, provided all of the following remain true:

- the asset is used only as cinematic Earth/context texture and is not presented as an OrbGSS analytical raster or a sensor-specific observation;
- the exact source URL/record, provider, usage-rights basis and materialized checksum are recorded in the existing asset manifest/provenance system;
- no NASA logo/insignia/identifier is introduced and no wording implies NASA endorsement;
- any third-party-copyrighted material or unclear-rights derivative is rejected;
- geography/orientation remain truthful enough for the cinematic context and the accepted Kızıldere/AOI registration is not redefined by the texture;
- the existing media byte ceilings remain unchanged unless separate measured Product approval is requested.

NASA Visible Earth / Blue Marble high-resolution imagery is an authorized candidate source **only after the exact selected asset record is verified against NASA media-use guidance and its own record for third-party restrictions**. The implementer may download/materialize such an asset as ordinary task-local production work and must record provenance/checksum. No additional Product approval is required merely because the texture has higher source resolution.

Therefore a prior `BLOCKED_ON_SOURCE_RESOLUTION` disposition based solely on needing a rights-safe higher-resolution cinematic Earth texture is superseded by this clarification. If no conforming rights-safe source can be verified, or the chosen asset would add a new scientific/public claim, then route back.

## 4. Explicitly out of scope

- homepage Act 2/3/4 redesign beyond bounded hero-handoff integration;
- analytical raster recolouring or new palette semantics;
- new scientific claims or sensing-physics claims;
- framework/runtime migration;
- production deploy, Vercel production alias, DNS/domain work;
- WEB-006 execution;
- destructive Git/history operations.

## 5. Acceptance tests

The implementation must encode and execute the following checks. Test file decomposition is implementer-owned.

### A-HERO-01 — accepted geometry continuity

Existing accepted Earth/world/AOI registration invariants remain green. A changed visual treatment must not move the governed target registration.

### A-HERO-02 — orbital-path audit

Machine-readable or generated evidence demonstrates that the satellite path used for the production scene is coherent with the intended orbital solution and does not produce the previously rejected foreground blow-up/fly-by behavior. Camera-relative framing and on-screen satellite size must remain intentional through the visible pass.

### A-HERO-03 — generic-satellite provenance

Any external satellite asset has recorded rights/provenance and is safe for public commercial presentation. The model/metadata must not claim a specific spacecraft/sensor identity.

### A-HERO-04 — sensing-FX negative gate

Validation/evidence must make it possible to reject at least these regressions: thick/opaque acquisition slabs, governed scientific raster baked into the hero render, or a public configuration that labels the visualization as actual sensor physics.

### A-HERO-05 — target-frame quality gate

Production evidence at the acquisition/regional frames shows a thin, crisp target frame/corner-lock treatment without the previous thick blurred/smeared appearance. Registration remains numerically valid.

### A-HERO-06 — resolved ending

Playback evidence proves the sequence reaches an intentional final state and the governed page-layer handoff occurs at the intended hold/resolve point rather than appearing as an accidental stalled frame.

### A-HERO-07 — production media integrity

For WebM, MP4 and poster record dimensions, codec/container, frame rate where applicable, duration, exact bytes and SHA-256; validators enforce accepted ceilings and manifest consistency.

### A-HERO-08 — fallback/network behavior

Verify desktop motion-allowed playback plus reduced-motion, Save-Data/slow-network and representative mobile fallback. No case may require both hero video encodes to download.

### A-HERO-09 — regression suite

Site + hero validators remain green after conformant updates. New invariant checks must include deliberate negative cases where practical so the new gate is proved capable of failing.

### A-HERO-10 — human visual gate

Provide Product/CTO with before/after stills at:

1. satellite entrance;
2. acquisition/scan moment;
3. regional hold;
4. final handoff/end state;

and a short full-sequence screen/video capture. A public preview URL is not required.

### A-HERO-11 — source-resolution / upscaling gate

For the production Earth texture used by the approved regional/acquisition shots, evidence must record source dimensions and a reproducible estimate of effective source texel coverage at the softest approved hold. If the previous material-upscaling defect is addressed through a higher-resolution source, demonstrate the before/after effective texel ratio or equivalent objective evidence and show that the new asset passes the provenance/rights checks above.

## 6. Required evidence

At `REVIEW_READY` provide:

- exact branch and final HEAD;
- changed-path inventory;
- exact source/provenance for the satellite model/asset;
- exact source/provenance/dimensions/checksum for any replacement Earth texture;
- motion/orbit/framing audit;
- four before/after still pairs;
- complete hero playback video/screen capture pointer;
- target geometry/registration evidence;
- source-resolution/upscaling evidence for the Earth texture;
- production media metrics/hashes;
- site/hero/negative-test results;
- fallback matrix;
- explicit confirmation that scientific/public semantics are unchanged;
- explicit `NOT RUN` for any genuinely unavailable check.

## 7. STOP conditions

Return `WAITING_DOMAIN_DECISION` only if completion requires:

- changing accepted Product behavior or four-act hierarchy;
- changing scientific/data semantics;
- claiming a specific sensor/platform or actual sensing physics;
- using a paid/unclear-rights satellite or Earth asset;
- relaxing media ceilings as a Product trade-off;
- production deploy/domain/DNS work;
- credentials/payment/legal/commercial action;
- destructive/irreversible action.

Render iteration, encoder tuning, Blender/tool issues, rights-safe higher-resolution cinematic Earth-texture materialization, CSS/JS bugs, validator repair, bounded scene refactors and evidence defects remain implementation-owned.

**Terminal implementation state:** `REVIEW_READY`.
