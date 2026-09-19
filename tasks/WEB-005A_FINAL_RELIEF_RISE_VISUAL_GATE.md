# WEB-005A — Final Relief-Rise Visual Gate

**State:** VISUAL_GATE_PASSED / PUBLICATION_PENDING  
**Parent:** WEB-005A / MER-107  
**Reviewed local checkpoint:** `feat/web-005a-hero-visual-fidelity@1135e7a7e0b0f6db6348dee139d505550d8ca8b9`  
**Current remote HEAD at review time:** `e7098de8f05dfb3842620bbb578227d5c0bc2699`  
**Evidence:** real 1440×900 playback `web005a_relief_rise_playback_1440x900.mp4`.

## Product/CTO visual decision

The bounded final-polish visual gate is passed.

Accepted:
- startup poster now establishes on Earth rather than flashing the held/final target;
- progressive DEM relief rise is visually restored before Terrain;
- relief rise is smooth enough at the reviewed 1440×900 playback and preserves the sense that terrain resolves physically out of the surface;
- AOI outline/shadow rise with the relief without a detached-frame pop;
- Terrain -> THM-01 -> ALT-01 -> Priority order and timing remain coherent;
- final Priority hold, left-copy safety, no hero colorbar/legend/card/label, and prior accepted scan/acquisition choreography remain intact;
- no full 276-frame rerender was required;
- lossless rise-state delivery and deterministic validation/reproduction approach are accepted.

No further visual revision is requested for WEB-005A from this review.

## Publication requirement

The reviewed implementation is still local. Publish `1135e7a7e0b0f6db6348dee139d505550d8ca8b9` to `origin/feat/web-005a-hero-visual-fidelity` by non-force fast-forward and verify exact remote HEAD.

After exact-head publication verification, WEB-005A is eligible for terminal Product acceptance without another human visual revision, provided the pushed tree is byte-identical to the reviewed local checkpoint and validators remain green.

## Scope lock

Do not opportunistically convert the four already-accepted drape PNGs to WebP in this closeout. That optimization is visually lossless in principle but is not required to close WEB-005A and would create another delivery/evidence delta after the final visual gate. Track payload optimization separately if desired.

No merge, deploy or DNS action is authorized by this record.
