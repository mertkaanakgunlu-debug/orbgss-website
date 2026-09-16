# WEB-005B — Homepage Visual Fidelity & Public Palette System

**State:** READY_FOR_CTO_APPROVAL — NOT STARTED  
**Parent:** WEB-005 / MER-93 — terminally accepted  
**Canonical baseline:** `main@00af0f232a8d7d77f5ca61d758461ff7316ba151`  
**Implementation branch:** `feat/web-005b-homepage-visual-fidelity`  
**Product visual authority:** `docs/WEB_005_POLISH_VISUAL_DIRECTION_AUTHORITY.md` on `docs/web-005-polish-authority`  
**Dependency:** start after WEB-005A R2 is stable enough that hero-handoff contracts will not churn; terminal acceptance requires no unresolved Science palette dependency.

## 1. Outcome

Raise Acts 2–4 to the same launch-quality visual bar as the refined hero and establish a reusable public presentation palette system for website/application outputs without changing scientific meaning.

Current-site review confirms that the structure is correct but the visual presentation is too technical/report-like compared with the accepted reference direction. WEB-005B owns the non-hero visual correction:

1. Act 2 real Kızıldere EO context quality;
2. Act 3 compact evidence-trio visual coherence and energy;
3. Act 4 priority/result visual dominance;
4. reusable Product-owned brand/UI/acquisition palette tokens;
5. Science-approved analytical palette bindings where governed value-to-colour mappings are changed.

The CTO-provided analytical reference image is a **visual/style reference only**: vivid analytical surface, strong relief/contour depth, luminous cyan target frame and clear visual hierarchy. It is not a source asset and must not be copied into production.

## 2. Act 2 — real Kızıldere context

The current real Kızıldere image is provenance-valid but visually reads like a processed/technical raster. Replace or re-present it, within accepted public-safe provenance, so it clearly communicates “the real place before analysis.”

Required qualities:

- natural-colour / photographic EO appearance;
- trustworthy terrain, settlement/agricultural and land/water relationships;
- neutral/restrained processing;
- visibly closer to a real Earth-observation image than to THM/ALT/thematic output;
- enough local contrast to read relief and spatial context;
- no ungoverned basemap/provider substitution;
- no aggressive browser upscaling;
- context-only meaning stays explicit and separate from analytical evidence semantics.

If the current master cannot produce the desired natural read without semantic/provenance ambiguity, use another accepted/public-safe derivative tied to the same Kızıldere context role and record full provenance.

## 3. Act 3 — compact evidence trio

Preserve exactly:

1. Terrain/NASADEM;
2. THM-01 Thermal Anomaly;
3. ALT-01 Alteration Proxy.

The current three-card implementation is technically correct but visually too flat and report-like. Improve the composition so the three images read as one coherent analytical stage:

- more image-led card proportions;
- stronger surrounding contrast / framing;
- consistent metadata/legend treatment;
- reduced low-value text clutter;
- greater visual energy and hierarchy;
- responsive scaling without unsafe upscaling;
- vividness through presentation shell until Science palette authority permits raster recolouring.

Structure/Geology remains optional support / DATA_GAP / score-invariant and must not reappear as a major homepage act.

Governed raster pixels must not be recoloured or semantically transformed without accepted Science authority.

## 4. Act 4 — priority/result climax

Preserve exact public label and meaning:

**Remote-Sensing Relative Priority — Experimental Baseline**

It remains an AOI-relative 0–100 screening/ranking result, not probability, Full Prospectivity, reserve/resource, discovery likelihood or drilling-success likelihood.

The current result presentation is too small/contained relative to its role. Final Act 4 must become the strongest analytical visual on the page through:

- substantially more visual area than any single evidence card;
- clean negative space and framing;
- integrated truthful legend;
- strong title/metadata hierarchy;
- controlled cyan framing/glow in surrounding UI where useful;
- Science-approved vivid analytical palette once GEO-WEB-003 permits it.

Do not use detached decorative colour bars. Governed result pixels remain authoritative; any new value-to-colour mapping requires Science acceptance.

## 5. Product-owned palette system

### Brand/UI

- `--orb-bg`: `#030B12`
- `--orb-surface`: `#08131D`
- `--orb-panel`: `#0D1B27`
- `--orb-divider`: `#183245`
- `--orb-text-primary`: `#EAF2F8`
- `--orb-text-secondary`: `#9EB1C1`
- `--orb-meta`: `#6F8597`
- `--orb-cyan`: `#73E7FF`
- `--orb-cyan-glow`: `#8AF1FF`

### Acquisition / non-scientific framing FX

- beam core: `#7FEFFF`
- beam glow: `#3CCBFF`
- target frame: `#98F5FF`

These may be used in surrounding UI, target framing and non-scientific acquisition visualization without Science approval.

## 6. Analytical palette direction and Science boundary

Desired public/application families remain:

- Terrain/elevation: muted relief / earth-safe sequential treatment;
- Thermal anomaly: perceptually ordered dark-purple → magenta/red → warm-yellow;
- Alteration proxy: distinct teal → green → yellow;
- Priority/result: controlled ordered palette with stronger contrast/energy than the current proof render, while preserving ranking semantics and avoiding probability-like red/green good/bad coding.

This task does **not** authorize governed pixel recolouring by itself. Consume GEO-WEB-003 / MER-108 before changing scientific value-to-colour mappings. Until then improve presentation shell only.

## 7. Responsive / accessibility invariants

Preserve:

- 375 / 768 / 1024 / 1440 CSS-px representative layouts;
- no horizontal overflow or unstable image sizing;
- accepted class-B safe-density limits;
- EN/TR visible-copy and accessible-name parity;
- keyboard/focus/landmark behavior;
- mandatory scientific warnings in static HTML where required;
- accepted routes and deep-route semantics.

## 8. Acceptance tests

### B-VIS-01 — Act 2 context semantics
Act 2 uses a provenance-safe real EO context image and is explicitly context-only, not analytical evidence. Human review must show a materially more natural/geographic read than the current technical-raster-like checkpoint.

### B-VIS-02 — Act 2 provenance/rights
Source, derivative, dimensions, rights/public-safe basis and SHA-256 are recorded and validator-checkable.

### B-VIS-03 — evidence-trio cardinality
Homepage contains exactly the three accepted evidence cards and no standalone Structure/Geology major act.

### B-VIS-04 — governed-pixel protection
Validator/checksum/provenance assertion proves scientific assets are not silently recoloured/reclassified/value-transformed unless cited Science authority explicitly permits it.

### B-VIS-05 — palette-token contract
Brand/UI/acquisition palette tokens are defined once and used consistently. Regression test detects locked-token drift where practical.

### B-VIS-06 — priority semantics
Exact public label and AOI-relative non-probability warning remain present in EN/TR; tests fail on prohibited probability/prospectivity reinterpretation.

### B-VIS-07 — safe-density sweep
Major scientific visuals remain inside accepted rendered device-pixel ceilings across representative/wide viewports. Evidence records source/master, selected derivative and actual rendered size.

### B-VIS-08 — legend discipline
No detached decorative homepage scientific colour bar/scale strip. Necessary legends are integrated in/directly coupled to the relevant visual.

### B-VIS-09 — responsive/accessibility regression
375 / 768 / 1024 / 1440 screenshots plus DOM/validator evidence confirm no overflow, clipped copy, inaccessible controls or localization regression.

### B-VIS-10 — human visual gate
Provide before/after screenshots for Acts 2, 3 and 4 at desktop and representative responsive widths. Public preview URL not required.

### B-VIS-11 — visual-hierarchy gate
At 1440-class desktop, Act 4 must clearly dominate any single evidence card, and Act 3 must read as one coherent analytical stage rather than three isolated report exports. Human review compares against the CTO-provided analytical reference for energy/hierarchy only, not pixel imitation.

### B-VIS-12 — natural-context separation gate
A first-time viewer must be able to distinguish Act 2 natural EO context from Act 3 analytical rasters without reading the captions. Human review evidence must demonstrate this separation.

## 9. Required evidence

At `REVIEW_READY` provide:

- exact final HEAD and changed-path inventory;
- Act 2 source/provenance package and before/after evidence;
- Act 3 and Act 4 before/after screenshots;
- final Product palette token record;
- consumed Science palette authority pointer where applicable;
- governed-pixel checksum/provenance evidence;
- safe-density measurements;
- EN/TR/accessibility/route validator results;
- B-VIS-01..B-VIS-12 matrix;
- negative-test results for new invariants where practical;
- explicit semantic non-change statement;
- explicit `NOT RUN` for any genuinely unavailable check.

## 10. Out of scope

- hero Blender/motion redesign except bounded integration with accepted WEB-005A output;
- new scientific method, thresholds, score meaning or evidence eligibility;
- unapproved scientific recolouring;
- paid/closed/restricted data;
- framework/CMS migration;
- production deploy/domain/DNS changes;
- WEB-006 execution.

## 11. STOP conditions

Return `WAITING_DOMAIN_DECISION` only for a true Product behavior/architecture/scope conflict, or `WAITING_SCIENCE_DECISION` if desired analytical recolouring has no accepted Science authority. Rights ambiguity, credentials/payment/legal/commercial and destructive actions remain human gates.

Ordinary CSS/layout defects, responsive fixes, image-delivery tuning, accessibility fixes, validator repair, screenshots and evidence publication remain implementation-owned.

**Terminal implementation state:** `REVIEW_READY`.
