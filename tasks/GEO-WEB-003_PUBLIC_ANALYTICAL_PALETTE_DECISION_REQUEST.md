# GEO-WEB-003 — Public Analytical Palette Authority Decision Request

**State:** WAITING_SCIENCE_DECISION  
**Requester:** Product & Software  
**Owner domain:** Science & Geospatial  
**Consumers:** WEB-005B and future OrbGSS application/public output renderers  
**Baseline:** `main@00af0f232a8d7d77f5ca61d758461ff7316ba151`

## 1. Decision requested

Product requests a Science-owned public/application palette authority for four analytical visual families:

1. Terrain/elevation;
2. THM-01 thermal anomaly;
3. ALT-01 alteration proxy;
4. `mvp_remote_sensing_priority_v1` priority/result.

The goal is a reusable public-facing palette system that is visually vivid, legible and consistent across website and application surfaces without changing scientific meaning.

## 2. Product target direction

These are desired visual directions, not pre-authorized scientific mappings:

- Terrain/elevation: muted relief / earth-safe sequential treatment;
- THM-01: perceptually ordered dark-purple → magenta/red → warm-yellow progression;
- ALT-01: visually distinct teal → green → yellow progression;
- Priority/result: controlled perceptually ordered palette preserving AOI-relative ranking semantics and avoiding probability-like red/green good/bad signalling.

## 3. Science must decide and publish

For each family, publish:

- whether recolouring is scientifically/presentationally acceptable;
- exact value domain and normalization basis;
- exact value-to-colour mapping or approved named palette + parameters;
- whether mapping is continuous or classified;
- if classified, exact class breaks and semantics;
- NoData/mask treatment;
- whether opacity/blending is allowed and under what constraints;
- legend requirements;
- whether the same mapping is valid across AOIs or must remain AOI-relative;
- whether any existing accepted palette must remain canonical instead;
- export/render constraints for website/application use;
- machine-readable specification location and acceptance evidence.

## 4. Invariants

Do not change:

- feature eligibility;
- scoring method, weights or thresholds;
- CRS/grid/units/NoData/mask semantics;
- resampling policy;
- THM/ALT scientific interpretation;
- validation/uncertainty meaning;
- priority meaning.

Priority remains **Remote-Sensing Relative Priority — Experimental Baseline**, an AOI-relative 0–100 screening/ranking result, not probability, Full Prospectivity, reserve/resource, discovery likelihood or drilling-success likelihood.

## 5. Acceptance

Science acceptance is complete only when Product can consume an exact canonical pointer and a machine-readable palette specification without inferring or inventing scientific semantics.

If the existing governed palette must remain unchanged for one or more families, publish that as the accepted decision and explain what non-pixel presentation treatments Product may safely use instead.

## 6. STOP / human gate

No paid/licensed/closed data is required. If palette validation requires new field/closed/paid evidence or a change to scientific method, stop and route separately rather than expanding this request.
