# WEB-005A — Hero Visual Fidelity, Orbital Choreography & Launch-Quality Motion

**State:** REVISION_REQUIRED / IN PROGRESS  
**Parent:** WEB-005 / MER-93 — terminally accepted  
**Canonical baseline:** `main@00af0f232a8d7d77f5ca61d758461ff7316ba151`  
**Implementation branch:** `feat/web-005a-hero-visual-fidelity`  
**Rejected review checkpoint:** `ffa2f2944ca5992afb9e9891b42745a9bd1105ad` — technically green, visually not accepted  
**Product visual authority:** `docs/WEB_005_POLISH_VISUAL_DIRECTION_AUTHORITY.md` on `docs/web-005-polish-authority`  
**Launch dependency:** must be terminally accepted before WEB-006.

## 1. Outcome

Raise the accepted WEB-005 homepage hero to launch-quality cinematic fidelity without changing the four-act homepage architecture or accepted scientific/public semantics.

The current `ffa2f294...` checkpoint is preserved as useful technical/before evidence, but Product visual review rejected it because the Earth treatment is stronger than the rest of the hero: the satellite is too hard to read, the acquisition relationship is too weak, the target frame lacks a clear activation moment, and the final result handoff does not deliver the intended cinematic climax.

This revision is one bounded outcome. Do not restart conformant geometry, fallback, media-budget, validator or provenance work. Continue the same branch and revise only what is needed to meet this contract.

The CTO will provide two visual reference images with the execution prompt. They are **composition/style references only**, not source assets. Do not copy or ship them.

## 2. Required product behavior — R2 visual lock

The final sequence must read clearly, at normal desktop viewing size, as:

Earth establish → generic EO satellite emerges around the Earth limb → readable orbital arc → lower-left/left-lower acquisition composition → visible cyan sensing lines to the target → luminous target-frame lock → continuous approach to the same target → resolved governed analytical reveal.

### 2.1 Earth

Preserve the accepted strong Earth model, lighting, atmosphere and overall global look. Replace/augment the cinematic Earth texture with a materially higher-resolution rights-safe source if needed to remove visible regional softness.

### 2.2 Satellite

Use a rights-safe generic Earth-observation 3D satellite, or an in-repository model of equivalent quality. It must have enough real geometry/material response to avoid a flat-cutout or bright-speck read:

- volumetric body;
- solar panels with visible thickness / panel segmentation;
- physically coherent material separation/highlights;
- restrained antenna/sensor-housing detail;
- believable attitude relative to the target;
- no claim or visual identity of a specific operational spacecraft/sensor.

During the acquisition beat, the satellite must be unmistakably readable as a 3D EO platform without becoming the dominant object over Earth.

### 2.3 Orbital choreography

The visible pass must approximate the accepted visual-reference reading:

- satellite emerges from behind/around the Earth limb;
- the orbital arc is visibly understandable in screen space;
- acquisition composition places the satellite toward the lower-left / left-lower area relative to the Earth while Earth remains right-dominant;
- the satellite does not clip the frame during the intentional acquisition beat;
- optional orbital trail remains subtle and secondary;
- the satellite exit may leave frame later, but not before the viewer has clearly understood satellite → target relationship.

Numerical orbit solving remains implementation-owned. Physical plausibility and visual readability are both required.

### 2.4 Sensing FX

The prior nearly invisible cone is not acceptable. Acquisition FX must be restrained **and clearly readable**.

Preferred direction:

- two or more thin cyan sensing lines, or an equivalently readable restrained multi-line/boresight treatment;
- beam core `#7FEFFF`;
- outer glow `#3CCBFF`;
- lines remain visibly connected to satellite and target/footprint;
- lines may taper/soften near target but cannot disappear at normal desktop viewing;
- a low-opacity cone may support the lines but must not become the primary read.

Rejected:

- thick/fuzzy white slabs;
- opaque cones obscuring Earth;
- nearly invisible acquisition FX;
- noisy particles;
- game-like lasers;
- wording or metadata claiming literal sensor physics.

### 2.5 Target frame / lock event

The target outline/corner locks must be crisp and premium and must have a visible acquisition event:

- thin crisp cyan core;
- controlled emissive halo/glow;
- corner locks/registration marks visually resolve into place;
- brief intensification/pulse at acquisition is conformant;
- target remains registered to the accepted world/AOI geometry;
- no thick blurred/smeared outline;
- no silent move of Kızıldere centre or analysis AOI.

### 2.6 Camera approach

The camera continues toward the same target continuously. Preserve AOI identity/orientation/registration. The transition must not feel like generic map zoom or an unrelated cut; it should feel like the orbital acquisition naturally resolving into the regional target.

### 2.7 Final analytical handoff

The final state must feel deliberately resolved and visually substantial.

A small detached floating result card alone is not sufficient. Preferred behavior:

- target frame/corner locks intensify and settle;
- the regional target fills a meaningful portion of the composition;
- governed analytical content appears **inside, clipped to, or immediately coupled to the target region** as a page-layer/HTML overlay;
- the result is large enough to read as the product payoff;
- HTML headline/CTA remains separate from rendered media;
- governed raster pixels are not baked into lossy video where colour semantics would be altered;
- any visible analytical label/warning remains exact and truthful.

The final handoff may tease the accepted priority/result surface while Act 4 remains the full analytical climax later on the page.

## 3. Media / source-fidelity contract

Preserve:

- WebM `<= 3.0 MiB`;
- MP4 `<= 4.5 MiB`;
- poster `<= 180 KiB`;
- no dual-video download;
- mobile/reduced-motion/reduced-data intentional static/fallback behavior.

The earlier bitrate investigation is accepted evidence: regional softness is source-resolution dominated, not primarily encoder-limited. Do not reopen bitrate experiments unless a new measured reason appears.

### Earth source-resolution authority

WEB-005A may replace/augment the cinematic Earth albedo/basemap with a materially higher-resolution rights-safe source when needed. Record exact source/record, provider, usage-rights basis, dimensions and SHA-256. Reject unclear-rights third-party derivatives. Do not introduce endorsement language or provider branding. Preserve geographic orientation and accepted target registration.

A previous `BLOCKED_ON_SOURCE_RESOLUTION` disposition is superseded. Rights-safe higher-resolution Earth-texture materialization is implementation-owned.

## 4. Explicitly out of scope

- full Act 2/3/4 redesign beyond bounded hero-handoff integration;
- analytical raster recolouring/new palette semantics without Science authority;
- new scientific claims or sensing-physics claims;
- framework/runtime migration;
- production deploy/Vercel production alias/DNS/domain work;
- WEB-006 execution;
- destructive Git/history operations.

## 5. Acceptance tests

### A-HERO-01 — geometry continuity
Existing Earth/world/AOI registration invariants remain green. Visual treatment must not move governed target registration.

### A-HERO-02 — orbital-path audit
Evidence demonstrates a coherent orbital solution and no foreground blow-up/fly-by regression. Camera-relative framing and on-screen satellite size remain intentional through the visible acquisition pass.

### A-HERO-03 — generic-satellite provenance
Any external satellite asset has public-commercial-safe provenance/rights recorded; model/metadata does not claim a specific spacecraft/sensor identity.

### A-HERO-04 — sensing-FX negative gate
Tests/evidence can reject thick/opaque slabs, governed raster baked into hero video, actual-sensor-physics claims, and acquisition FX so faint that the satellite-target link is not legible at review size.

### A-HERO-05 — target-frame quality gate
Acquisition/regional evidence shows a thin crisp frame with controlled glow and a visible lock/activation event; registration remains numerically valid.

### A-HERO-06 — resolved ending
Playback evidence proves a deliberate final resolve and governed page-layer handoff rather than accidental stalled playback.

### A-HERO-07 — production media integrity
Record dimensions, codec/container, frame rate, duration, exact bytes and SHA-256 for WebM/MP4/posters; validators enforce ceilings/manifest consistency.

### A-HERO-08 — fallback/network behavior
Verify desktop motion plus reduced-motion, Save-Data/slow-network and representative mobile fallback. No case downloads both hero video encodes.

### A-HERO-09 — regression suite
Site + hero validators remain green; new invariant checks include deliberate negative cases where practical.

### A-HERO-10 — human visual gate
Provide before/after stills at satellite entrance, acquisition/scan, regional hold and final handoff plus a short full-sequence capture. Public preview URL is not required.

### A-HERO-11 — source-resolution/upscaling gate
Record Earth source dimensions and reproducible effective source-texel coverage at the softest approved hold. Demonstrate material reduction of previous upscaling or equivalent objective improvement together with rights/provenance checks.

### A-HERO-12 — satellite readability gate
At the primary acquisition frame, visual evidence must show the satellite body and solar-panel silhouette clearly enough to be recognized as a 3D EO platform at normal 1440-class viewing. A tiny bright speck or unreadable silhouette fails.

### A-HERO-13 — reference-composition gate
Human evidence must show the intended reference-A hierarchy: Earth dominant right, satellite lower-left/left-lower during acquisition, readable satellite-target linkage, and luminous target frame. Exact pixel mimicry is not required; composition/energy/readability are.

### A-HERO-14 — analytical-handoff gate
Final-state evidence must show governed analytical content in/directly coupled to the acquired target region and visually substantial enough to read as the payoff. A small detached result card as the sole payoff fails.

## 6. Required evidence at REVIEW_READY

- exact branch/final HEAD;
- changed-path inventory;
- rejected checkpoint `ffa2f294...` retained as before evidence;
- exact satellite model/asset provenance;
- exact replacement Earth texture source/provenance/dimensions/checksum if used;
- motion/orbit/framing audit;
- four before/after still pairs;
- full hero screen/video capture;
- target registration evidence;
- Earth source-resolution/upscaling evidence;
- production media metrics/hashes;
- A-HERO-01..A-HERO-14 result matrix;
- site/hero/negative-test results;
- fallback matrix;
- explicit scientific/public semantic non-change statement;
- explicit `NOT RUN` for any genuinely unavailable check.

## 7. STOP conditions

Return `WAITING_DOMAIN_DECISION` only if completion requires:

- changing four-act hierarchy/product behavior outside this authority;
- changing scientific/data semantics;
- claiming specific sensor/platform or literal sensing physics;
- using paid/unclear-rights satellite or Earth assets;
- relaxing media ceilings;
- production deploy/domain/DNS;
- credentials/payment/legal/commercial action;
- destructive/irreversible action.

Render iteration, encoder tuning, Blender/tool issues, rights-safe Earth-texture materialization, 3D satellite modelling/integration, CSS/JS hero-handoff fixes, validator repair, bounded scene refactors and evidence defects remain implementation-owned.

**Terminal implementation state:** `REVIEW_READY`.
