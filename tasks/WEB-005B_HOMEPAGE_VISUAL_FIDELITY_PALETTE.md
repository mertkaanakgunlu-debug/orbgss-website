# WEB-005B — Homepage Visual Fidelity & Public Palette System

**State:** READY_FOR_CTO_APPROVAL — NOT STARTED  
**Parent:** WEB-005 / MER-93 — terminally accepted  
**Canonical baseline:** `main@00af0f232a8d7d77f5ca61d758461ff7316ba151`  
**Implementation branch:** `feat/web-005b-homepage-visual-fidelity`  
**Product visual authority:** `docs/WEB_005_POLISH_VISUAL_DIRECTION_AUTHORITY.md` on `docs/web-005-polish-authority`  
**Dependency:** may start after WEB-005A is stable enough that homepage hero integration contracts will not churn; terminal acceptance requires no unresolved Science palette dependency.

## 1. Outcome

Raise the non-hero homepage acts to the same launch-quality visual bar as the refined hero and establish a reusable public presentation palette system for website/application outputs without changing scientific meaning.

The outcome covers:

1. Act 2 real Kızıldere EO context quality;
2. Act 3 compact evidence-trio presentation;
3. Act 4 priority/result climax presentation;
4. reusable Product-owned brand/UI and acquisition-FX palette tokens;
5. Science-approved analytical palette bindings where governed value-to-colour mappings are changed.

## 2. Act 2 — real Kızıldere context

The current real Kızıldere image is provenance-valid but visually reads too much like a technical raster. Replace or re-present it, within accepted public-safe provenance, so the section clearly communicates “the real place before analysis.”

Required qualities:

- natural Earth-observation / geographic appearance;
- trustworthy terrain, settlement/agricultural and land/water relationships;
- no synthetic-looking thematic palette;
- no ungoverned basemap/provider substitution;
- no aggressive browser upscaling;
- context-only meaning remains explicit and separate from THM/ALT acquisition dates or evidence semantics.

A different rights-safe/public-safe derivative may be selected if it is canonically tied to the same Kızıldere context role and provenance is complete.

## 3. Act 3 — compact evidence trio

Preserve exactly:

1. Terrain/NASADEM;
2. THM-01 Thermal Anomaly;
3. ALT-01 Alteration Proxy.

Improve presentation through layout, framing, typography, in-frame legend treatment, surrounding contrast, spacing and controlled emphasis. The three cards should read as one coherent analytical stage rather than three disconnected technical exports.

Structure/Geology remains optional support / DATA_GAP / score-invariant and must not reappear as a major homepage act.

Governed raster pixels must not be recoloured or semantically transformed without Science authority.

## 4. Act 4 — priority/result climax

Preserve the exact public label and meaning:

**Remote-Sensing Relative Priority — Experimental Baseline**

It remains an AOI-relative 0–100 screening/ranking result, not probability, Full Prospectivity, reserve/resource, discovery likelihood or drilling-success likelihood.

Presentation should become the strongest analytical visual on the page through scale, framing, typography and a compact integrated legend. Do not use detached decorative colour bars.

The governed result pixels remain authoritative. Any new value-to-colour mapping requires Science acceptance.

## 5. Product-owned palette system

Implement reusable tokens for the accepted Product palette:

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

### Acquisition / hero FX

- beam core: `#7FEFFF`
- beam glow: `#3CCBFF`
- target frame: `#98F5FF`

These may be used in surrounding UI and non-scientific acquisition visualization without Science approval.

## 6. Analytical palette direction and Science boundary

Desired application/public families are:

- Terrain/elevation: muted relief / earth-safe sequential treatment;
- Thermal anomaly: perceptually ordered dark-purple → magenta/red → warm-yellow;
- Alteration proxy: distinct teal → green → yellow;
- Priority/result: controlled perceptually ordered palette that preserves ranking semantics and avoids probability-like good/bad coding.

This task does **not** authorize changing governed value-to-colour mappings by itself. If the implementation wants to recolour THM-01, ALT-01, terrain or priority raster pixels, it must consume the separate Science acceptance for the public analytical palette authority. Until then, improve vividness through presentation shell, not scientific pixel remapping.

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

Act 2 uses a provenance-safe real EO context image and is explicitly identifiable as context-only, not analytical evidence. Visual review must show a more natural/geographic presentation than the current technical-raster-like state.

### B-VIS-02 — Act 2 provenance/rights

Source, derivative, dimensions, rights/public-safe basis and SHA-256 are recorded and validator-checkable.

### B-VIS-03 — evidence-trio cardinality

Homepage contains exactly the three accepted evidence cards and no standalone Structure/Geology major act.

### B-VIS-04 — governed-pixel protection

A validator or checksum/provenance assertion proves that governed scientific assets are not silently recoloured/reclassified/value-transformed unless a cited Science palette authority explicitly permits it.

### B-VIS-05 — palette-token contract

Brand/UI/acquisition palette tokens are defined once and used consistently. A regression test must detect drift of locked Product tokens where practical.

### B-VIS-06 — priority semantics

The exact public label and AOI-relative non-probability warning remain present in EN/TR. Tests must fail on prohibited probability/prospectivity reinterpretation.

### B-VIS-07 — safe-density sweep

At representative and wide viewports, major scientific visuals remain within accepted safe rendered device-pixel ceilings. Evidence records source/master, selected derivative and actual rendered size.

### B-VIS-08 — legend discipline

No detached decorative homepage scientific colour bar/scale strip. Necessary legends are integrated inside or directly coupled to the relevant visual.

### B-VIS-09 — responsive/accessibility regression

375 / 768 / 1024 / 1440 screenshots plus DOM/validator evidence confirm no overflow, clipped copy, inaccessible controls or localization regressions.

### B-VIS-10 — human visual gate

Provide before/after screenshots for Acts 2, 3 and 4 at desktop and representative responsive widths. Product/CTO visual acceptance may use screenshots; a public preview URL is not required.

## 9. Required evidence

At `REVIEW_READY` provide:

- exact final HEAD and changed-path inventory;
- Act 2 source/provenance package and before/after evidence;
- Act 3 and Act 4 before/after screenshots;
- final Product palette token record;
- any consumed Science palette authority pointer;
- governed-pixel checksum/provenance evidence;
- safe-density measurements;
- EN/TR/accessibility/route validator results;
- negative-test results for new invariants where practical;
- explicit semantic non-change statement;
- explicit `NOT RUN` for any genuinely unavailable check.

## 10. Out of scope

- hero Blender/motion redesign except bounded integration with the accepted WEB-005A output;
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
