# WEB-005B R16 — R15 Technical Acceptance / Final Visual Review Gate

**Linear:** MER-109  
**State:** TECHNICALLY_ACCEPTED / WAITING_FINAL_CTO_VISUAL_REVIEW  
**Implementation under review:** local feat/web-005b-homepage-visual-fidelity@0af5b1a  
**Science authority consumed:** geothermal-prospectivity@e8aa5d65f56556be928499c50936eb63db88a6ad:tasks/MER-151_GEO-WEB-004_HOMEPAGE_EVIDENCE_PRESENTATION_PARITY_AUTHORITY.md

## 1. Technical disposition

R15 is technically accepted based on the reported evidence.

Accepted changes:
- MER-151 presentation pipeline applied to homepage Evidence/Result;
- ALT-01 bounded display window q_low=0.02 / q_high=0.98;
- THM-01 bounded symmetric display window q_abs=0.998 with resolved M=0.7036 and gamma=0.85;
- Terrain and Priority left without extra transfer and preserved against the prior accepted bytes;
- numbered/prototype-like section labels removed;
- weak Solutions kicker removed;
- Evidence stage rebalanced;
- Result viewport fit improved;
- Result definition strip gutters/dividers corrected;
- three-ground tonal hierarchy introduced while preserving seamless section boundaries;
- no hero change;
- validators GREEN.

## 2. Product decision on 4K/HiDPI publication

The Science authority permits 4K-class presentation derivatives, but WEB-005B is not required to ship the largest permitted asset merely because it is allowed.

Product accepts the current decision not to publish the 1800/3840 analytical delivery rungs in this revision because:
- focal analytical surfaces cap near 600 CSS px;
- the 1200 px governed presentation assets provide exact 2x density at that display size;
- the tested 1800 px lossless assets materially increase payload;
- the current visual-review goal is fidelity and continuity, not maximum theoretical pixel count.

This is not a rejection of high-DPI support.

WEB-007 / MER-143 remains responsible for broader responsive high-DPI/4K delivery, codec/variant optimization and source selection without redesign. If the CTO visual review finds the current 1200 px presentation visibly soft on the target laptop/display, that becomes evidence to pull a larger conformant rung forward before WEB-006.

## 3. Final visual gate

No further Product/Science semantic work is required before visual review.

Review must inspect the actual R15 implementation for:
- Place -> Evidence -> Result -> Solutions tonal continuity;
- whether the lower-page darkness is sufficiently relieved without losing brand cohesion;
- Evidence Terrain/Thermal/Alteration visual quality;
- Result headline + full map fit on laptop-height viewport;
- corrected 4-item Result strip spacing/dividers;
- Solutions hierarchy and card consistency;
- removal of numbered/prototype labels;
- mobile continuity.

Required current evidence:
- full desktop homepage;
- laptop-height Result view;
- Evidence Terrain/Thermal/Alteration states;
- Solutions desktop;
- full mobile homepage;
- real scroll/playback capture from hero through lower-page sections.

## 4. Continuation

If visual review is accepted:
- publish the exact reviewed implementation head normally;
- terminally accept MER-109;
- continue to WEB-005C / MER-149;
- then WEB-006.

If only bounded visual polish remains, revise inside MER-109 without reopening design or Science.

No merge, deploy or DNS change is authorized by this document.

**Current state:** WAITING_FINAL_CTO_VISUAL_REVIEW.
