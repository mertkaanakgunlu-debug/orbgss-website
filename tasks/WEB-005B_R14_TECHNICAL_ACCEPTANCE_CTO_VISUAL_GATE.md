# WEB-005B R14 — Technical Revision Acceptance / CTO Visual Gate

**Linear:** MER-109  
**State:** TECHNICALLY_ACCEPTED / WAITING_CTO_VISUAL_REVIEW  
**Implementation under review:** local feat/web-005b-homepage-visual-fidelity@0938f2ab122b11d496441d0b04cd7c94550a9854  
**Base:** 4e6c7c106399140565c77da0febe59ffc14f3ab3

## Decision

The bounded R13 revision is accepted technically based on the reported evidence.

Accepted:
- homepage taxonomy restored to Geothermal / Mining / Marine;
- no production navigation invented for unfinished Mining/Marine cards;
- shared route copy was not silently repurposed;
- hero lane write-surface defect was repaired;
- secondary domain-card caption overlap was repaired;
- full validation returned GREEN;
- R11 accepted deviations remain preserved.

This does not constitute final visual acceptance.

## Remaining gate

CTO must visually inspect the actual implementation at HEAD 0938f2ab... using:
- current full desktop capture;
- current full mobile capture;
- current Domains desktop/mobile captures;
- actual scroll/playback recording through Hero → Place → Evidence → Result → inspection aid → Domains.

If visual review is accepted, MER-109 may terminally close after normal publication of the reviewed exact implementation head.

If visual review finds only bounded spacing/continuity/polish defects, revise within MER-109 without reopening design.

## Cross-route taxonomy observation

The homepage taxonomy is now Product-canonical:
- Geothermal
- Mining
- Marine

The existing /solutions/ route still uses legacy/application-ledger vocabulary such as Mineral Exploration and Environmental & Land Intelligence.

That is not a WEB-005B implementation defect because R13 explicitly kept non-homepage routes out of scope. It is a separate public-IA consistency issue and must be reconciled before WEB-006 public launch.

## Restrictions

No merge, deployment, DNS cutover or WEB-006 execution is authorized by this acceptance alone.

**Current state:** WAITING_CTO_VISUAL_REVIEW.
