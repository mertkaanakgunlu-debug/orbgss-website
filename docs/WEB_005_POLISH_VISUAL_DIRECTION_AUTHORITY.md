# WEB-005 Polish Visual Direction Authority

**State:** ACCEPTED PRODUCT DIRECTION — publication only  
**Repository:** `mertkaanakgunlu-debug/orbgss-website`  
**Baseline:** `main@00af0f232a8d7d77f5ca61d758461ff7316ba151`  
**Consumers:** WEB-005A, WEB-005B  
**Launch gate:** WEB-006 remains blocked until Product terminal review of these polish outcomes.

## 1. Accepted visual direction

The accepted WEB-005 structure and public/scientific semantics remain valid. The remaining work is a pre-launch visual-quality pass.

### Hero cinematography

The hero should read as one premium orbital-acquisition story:

1. Earth establish;
2. a generic Earth-observation satellite emerges from behind/around the Earth limb on a readable orbital arc;
3. satellite motion resolves into an intentional acquisition attitude;
4. restrained cyan sensing beams/cone connect the satellite and target region;
5. the target frame and corner-lock language activate with a thin crisp cyan glow;
6. the camera continues into the regional hold;
7. the governed analytical/result handoff resolves as an intentional climax rather than a stalled final frame.

The reviewed reference direction is accepted: satellite composition biased to the lower/left side of the frame relative to the Earth, a visible orbital-arc feeling, thin coherent cyan sensing lines, and a luminous but controlled target frame.

The satellite should use a rights-safe generic EO 3D model, or an in-repository model of equivalent visual quality, with real depth, solar-panel thickness, body/material separation, restrained antenna/sensor-housing detail and physically coherent light response. It must not claim or visually identify a specific operational spacecraft or sensor.

### Hero effects

Hero effects are visualization language, not sensor-physics claims. Public copy/evidence must not describe the beams, cone or footprint as an actual instrument model unless separately authorized.

Accepted acquisition-FX direction:

- thin cyan beam core: `#7FEFFF`;
- restrained outer glow: `#3CCBFF`;
- target/AOI frame: `#98F5FF`;
- optional halo/trail treatment must remain subtle and subordinate to the Earth imagery.

The target outline must be crisp, narrow and technically premium. Thick blurred borders, fuzzy white smears, noisy particles and game-like laser effects are rejected.

### Result/evidence handoff

Governed analytical rasters must not be baked into lossy hero video when that would alter their value-to-colour meaning. The accepted WEB-005 HTML/page-layer handoff remains valid. The transition into that layer may be cinematic, but the analytical pixels and semantics remain governed.

## 2. Homepage public visual direction

The final homepage remains exactly four major visual acts:

1. cinematic acquisition hero;
2. real Kızıldere EO context;
3. compact Terrain + THM-01 + ALT-01 evidence trio;
4. large `mvp_remote_sensing_priority_v1` result climax.

### Act 2 — real place

Act 2 must read immediately as a real Earth-observation view of the Kızıldere/Büyük Menderes setting before analysis. The current accepted source/provenance constraints remain binding, but presentation should feel photographic and geographic rather than like another technical evidence raster.

Preferred qualities:

- natural-looking land/water/terrain relationships;
- clean spatial context;
- restrained processing;
- enough local contrast to read terrain and settlement/agricultural structure;
- no synthetic-looking palette, fake basemap or ungoverned provider substitution.

### Acts 3 and 4 — analytical presentation

Evidence and result visuals should be more vivid, legible and attention-holding through composition, framing, typography, legend design, local contrast around the raster, and surrounding UI treatment.

Product may improve the presentation shell without changing governed pixel values. Any change to a scientific value-to-colour mapping, class thresholds, raster colours or semantic interpretation requires explicit Science authority.

## 3. Product-owned palette lock

### Brand / UI

- Background: `#030B12`
- Surface: `#08131D`
- Panel: `#0D1B27`
- Fine lines/dividers: `#183245`
- Primary text: `#EAF2F8`
- Secondary text: `#9EB1C1`
- Muted metadata: `#6F8597`
- Accent cyan: `#73E7FF`
- Glow cyan: `#8AF1FF`

### Acquisition / hero FX

- Beam core: `#7FEFFF`
- Beam outer glow: `#3CCBFF`
- Target frame: `#98F5FF`
- Supporting glow/trail must remain restrained, low-opacity and non-dominant.

### Analytical palette direction — PRODUCT TARGET, SCIENCE-GATED

The following are desired public/application families, not authorization to recolour governed scientific outputs:

- Terrain/elevation: muted relief / earth-safe sequential treatment; subdued compared with evidence anomalies.
- Thermal anomaly: perceptually ordered dark-purple → magenta/red → warm-yellow progression; vivid but not probability-coded.
- Alteration proxy: distinct teal → green → yellow progression, clearly separable from thermal.
- Priority/result: the most controlled and scientific-looking ordered palette; preserve AOI-relative ranking semantics and avoid probability-like red/green good/bad messaging.

Exact value-to-colour mappings, class breaks and any replacement of the currently accepted governed raster palette require Science acceptance before implementation.

## 4. Human visual review evidence

A public preview URL is optional, not required. Product visual review may be completed from:

- 1440 desktop screenshots;
- 768 tablet screenshots where layout changes materially;
- 375 mobile screenshots;
- short screen/video capture showing the complete hero motion and handoff;
- before/after hero stills at entrance, acquisition, regional hold and final handoff.

Screenshots/video are evidence for visual judgment; numeric claims such as media size, safe density, validation results and provenance must still come from reproducible measurements/files.

## 5. Invariants

- No production deploy, DNS/domain cutover or WEB-006 work under this authority.
- No new scientific method, score meaning, thresholds, eligibility, CRS/grid/unit/NoData/mask/resampling semantics.
- No specific-sensor identity or fabricated sensing-physics claim.
- Existing four-act architecture, EN/TR parity, accessibility and fallbacks remain binding.
- Routine render/encode iteration, CSS/layout fixes, test repair and evidence publication are implementation-owned.
