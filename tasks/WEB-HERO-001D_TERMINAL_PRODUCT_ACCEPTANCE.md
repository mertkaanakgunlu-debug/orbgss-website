# WEB-HERO-001D — Terminal Product Acceptance

**Linear:** `MER-101`  
**Branch:** `feat/web-hero-001-predata-scene`  
**Accepted implementation HEAD:** `93e17f6293aeb8bdc882dfd28221ed786b772df1`  
**Accepted REVIEW_READY/evidence HEAD:** `e95fdcac7cac82e597d40dab4cdc96ce1a6b319e`  
**Predecessor:** `MER-100 / WEB-HERO-001C` terminally accepted at `6593a80899720f8c7461aaa99ade0e5e63a3ea42`  
**State:** `TERMINAL_PRODUCT_ACCEPTANCE`

## Decision

WEB-HERO-001D is accepted as the terminal phase of the WEB-HERO-001 pre-data production lane. No further Phase-D revision is required under the accepted task authority.

This acceptance is for the pre-data cinematic system only: Earth establish → satellite entrance → AOI acquisition/scan → continuous camera approach → stable regional AOI hold. It does not authorize real scientific layers, final analytical palette, production media packaging, homepage integration, responsive/performance release work, deployment or DNS changes.

## Acceptance basis

Product verified the canonical branch/evidence package at `e95fdcac7cac82e597d40dab4cdc96ce1a6b319e`:

- branch progression is fast-forward from the published Phase-D start authority and contains the accepted Phase-C HEAD in history;
- the new `hero_predata_animatic` consumes the accepted Phase-C spherical AOI/beam/scan system rather than redesigning it;
- accepted Phase-C scene definitions remain unchanged while Phase-D additions are opt-in to the new scene;
- `validate_hero.py`: 151 checks, 0 failed; 8/8 deliberate negative regressions caught;
- Phase-C geometry remains green in the Phase-D scene: worst radial deviation 0.726 m, beam-tip error 2.249 m, beam-root error 0.0 m, footprint-edge spread 0.019 km; secondary fixture unchanged;
- per-frame camera/continuity audit passes all eight thresholds, including AOI centre lock 0.0 frame widths, no out-of-shot frames and headline-safe occupancy 0.0;
- evidence includes six Cycles/OptiX beat stills, a 16-frame Cycles continuity sheet, animatic record/pointer/hash, two AOI geometry audits, shot audit, shot-plan/framing report and Phase A–C reproducibility evidence;
- 8K Earth albedo provenance is the same NASA Earth Observatory record as the accepted 2K asset and is recorded as cleared/public-domain in `hero/assets/manifest.json`;
- no fabricated or real scientific layer, live-site integration, production WebM/MP4/poster packaging, deployment, DNS, paid/unclear-rights asset, force-push or history rewrite was introduced.

## Accepted limitations / downstream contract

The review animatic remains a review artifact, not the production website media package. The stable regional hold and `aoi_injection_interface.layer_slots` are the accepted downstream injection points for later real-data authority. Analytical palette semantics remain undefined here and must come from the later accepted Science/Product authority.

The accepted Phase-D scene is now an input to the later real-data hero phase and `WEB-005` integration/release gate. Publication of this acceptance does **not** auto-start either lane; CTO deliberate start remains required for a new plan/task.

## Canonical-state note

This document is the Product terminal-acceptance authority published after the implementation task reached `REVIEW_READY`. Where the earlier `REVIEW_READY` wording in `tasks/WEB-HERO-001D_PREDATA_ANIMATIC_GATE.md` or `STATUS.md` describes the pre-acceptance review state, this later acceptance record is authoritative for completion state.