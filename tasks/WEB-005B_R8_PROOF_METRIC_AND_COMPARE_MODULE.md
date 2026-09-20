# WEB-005B R8 — Proof Metric Deferral and Post-Result Compare Module

**State:** DESIGN_REFINEMENT_ACTIVE / HYBRID_AB  
**Parent:** MER-109 / WEB-005B  
**Consumes:** R7 hybrid A+B refinement direction

## 1. Quantitative proof metrics

No quantitative OrbGSS performance, accuracy, success-rate, ROI, customer-count, deployment-count or scale metric is currently authorized for homepage publication.

Do not invent a realistic-looking percentage or number, even for the implementation baseline.

The final homepage concept should therefore:
- keep the current differentiator/proof section qualitative;
- reserve structural flexibility for one future verified metric/proof module;
- avoid making the layout depend on any specific number;
- allow a future metric card/strip to be inserted without redesigning surrounding sections.

A design-only placeholder is allowed only if clearly marked as non-shipping, e.g. `VERIFIED METRIC SLOT` or `XX% — PROTOTYPE ONLY`; a fabricated plausible value is not allowed.

The absence of a metric does not block homepage design acceptance.

## 2. Future metric insertion requirement

The selected design must make later content changes low-risk:
- copy should be replaceable without restructuring the page;
- differentiator modules should be reusable;
- one optional metric/proof component may be inserted or removed;
- spacing/tokens should preserve the same visual language when this happens.

Production remains static HTML/CSS/vanilla JS, so later insertion is expected to be a bounded frontend change rather than a redesign.

## 3. Compare slider placement

Do not place a compare slider inside the main Act 03 evidence selector.

Act 03 remains the clean single-stage layer-switching interaction.

If the final concept uses a compare slider, place it **after Act 04 Result and before Domains** as a compact proof bridge.

Preferred compare:
- left/base: natural-colour AOI context;
- right/analysis: final Priority result;
- exact same geographic footprint/alignment;
- clear labels such as `Context` and `Priority`;
- concise supporting copy;
- contained centered width with generous side margins;
- not full-screen, not dashboard-like.

Purpose:
show the transformation from observed ground to decision-support output without adding control density to the evidence stage.

The slider is optional if it weakens hierarchy or mobile usability. If included, it must:
- work accessibly by pointer, touch and keyboard;
- have a static/no-JS fallback showing both states;
- preserve scientific image truthfulness and legends/caveats where required;
- remain subordinate to the main Act 04 payoff.

## 4. Mobile

On narrow screens, the compare module may:
- use a simple draggable divider if touch behavior is robust; or
- fall back to stacked Context / Priority images when that is clearer.

Do not force a small-screen slider merely for parity.

**Current state:** `WAITING_REFINED_CONCEPT`.
