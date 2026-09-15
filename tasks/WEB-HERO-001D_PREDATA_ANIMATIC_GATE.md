# WEB-HERO-001D — Continuous pre-data hero animatic & quality gate

**Linear:** `MER-101` (parent `MER-97`)  
**Predecessor:** `MER-100 / WEB-HERO-001C` terminally accepted at remote implementation/publication HEAD `6593a80899720f8c7461aaa99ade0e5e63a3ea42`  
**Authority:** `docs/WEB_HERO_001_AUTHORITY.md` + Drive CURRENT Hero Visual & Production Authority v1.0  
**Branch:** `feat/web-hero-001-predata-scene`  
**State:** `READY_FOR_CTO_APPROVAL`

## Outcome

Assemble the accepted Phase A–C systems into one continuous pre-data hero animatic that is visually strong enough to become the production base for the later real-data phase:

**Earth establish → satellite entrance → AOI acquisition/scan → continuous camera approach → stable regional hold.**

The quality gate must prove that the sequence no longer has the two reference-image defects Product explicitly rejected: a flat AOI pasted over the globe and a scale/orientation discontinuity between global/regional shots.

## Narrative / timing envelope

Target the pre-data portion so it can later fit naturally inside an approximately 8–12 second complete hero without forcing rushed motion. Exact timing is implementer-owned within these constraints:

- opening Earth rotation has enough time to establish place/quality;
- satellite entrance is readable but does not dominate;
- acquisition lock and scan clearly communicate target-area observation;
- camera approach begins from the same locked AOI and feels physically continuous;
- end state holds on the regional AOI long enough to receive real scientific layer reveals in the later phase.

Do not add the later evidence/priority reveal just to make the animatic feel complete.

## Continuity / cinematography contract

- Use one coherent scene/world coordinate system and the persistent AOI from Phase C.
- Avoid hidden cuts whose only purpose is to repair registration/scale. A deliberate cinematic cut could only be introduced by a future Product revision; this task targets a continuous move.
- Camera easing should feel premium and controlled, with no sudden acceleration, FOV snap or game-like flythrough.
- Preserve future headline-safe composition during the opening portion.
- Satellite should naturally leave or become compositionally secondary before the regional hold.
- Global and regional lighting/color should feel like the same visual world.

## Pre-data end state

The final hold is a clean regional view of the same surface-conforming AOI. It may retain subtle acquisition glow and existing Earth texture/neutral treatment, but must leave visual headroom for later real terrain/evidence/priority surfaces.

No fake scientific map is permitted as a placeholder final frame.

## Quality bar

Review should be performed against the locked authority, not against generic "looks good" criteria. The scene must demonstrate:

- convincing spherical Earth geometry;
- premium Earth/space/satellite art direction;
- clear satellite-to-AOI acquisition story;
- AOI border/scan tied to globe curvature;
- no AI-style floating panel artifact;
- continuous AOI identity/scale/orientation into the regional shot;
- disciplined cyan acquisition language without HUD clutter;
- strong visual appeal for non-technical audiences while remaining credible to technical viewers.

## Deliverables

Produce, at minimum:

1. a review animatic/preview of the full pre-data sequence;
2. high-quality stills representing: opening establish, satellite/acquisition, active scan, mid-approach, regional hold;
3. committed source/config/scripts sufficient to reproduce the sequence;
4. scene validation report/results;
5. render/asset manifest updates and evidence hashes/pointers;
6. a concise handoff note defining the future injection points for real AOI raster/terrain/evidence/score materials and the layer-reveal portion owned by later authority.

Large preview/master files do not need to be committed if repository hygiene would suffer; use bounded evidence artifacts plus exact local paths/hashes/pointers as appropriate.

## Out of scope

- real DEM/thermal/alteration/structure/geology/priority data;
- final analytical palette applied to scientific data;
- final master render/production bitrate decision;
- WebM/MP4/poster/reduced-motion production package;
- homepage HTML/CSS/JS integration;
- responsive crop/performance acceptance;
- WEB-006 deployment/DNS.

These are later hero/WEB-005 responsibilities after the relevant website and Science inputs are accepted.

## Acceptance

Phase D / WEB-HERO-001 pre-data lane is complete only when:

1. The full pre-data narrative plays as one coherent sequence from global Earth to regional AOI hold.
2. Earth remains a true 3D sphere with coherent atmosphere/perspective throughout.
3. AOI geometry visibly follows the globe and passes Phase C geometry validation.
4. Beam/corner-lock/scan registration remains correct during motion.
5. There is no perceptible identity, orientation or scale discontinuity in the AOI between acquisition and regional approach.
6. Satellite entrance/orbit/exit behavior is visually credible and secondary to the product story.
7. Opening composition preserves useful future HTML-copy safe space.
8. The regional hold is visually prepared for later real data but contains no invented scientific layer.
9. Asset rights/provenance are complete for all external production material.
10. The scene is reproducible from committed source/config and the accepted asset-materialization path.
11. Validation is green with no unexplained failure.
12. Review evidence is sufficient for Product to judge geometry, continuity and cinematic quality without opening Blender manually.

## Verification / evidence

Report at `REVIEW_READY`:

- exact branch/final HEAD and changed paths;
- Blender/tool versions, render engine/device, preview settings;
- full animatic pointer/hash, duration, resolution and file size;
- five representative still pointers/hashes;
- scene validation result including AOI sphere/registration checks;
- asset manifest summary and rights status;
- timing/keyframe/camera summary;
- explicit checklist for the 12 acceptance points;
- future real-data injection/handoff note;
- confirmation that no scientific output, website integration, deployment or DNS change occurred.

## Accepted Phase-C carry-forward

WEB-HERO-001C is terminally accepted with no further revision required. Phase D must consume, not redesign, its configuration-driven spherical AOI system, beam/corner registration, scan-sweep geometry and continuity convention.

The following accepted Phase-C limitations are explicit Phase-D quality-gate work, not reasons to reopen Phase C:

- the current 2048 px Phase-B Earth albedo is visibly soft at the closest regional approach;
- atmosphere treatment may require conformant refinement at regional scale;
- EEVEE beam sorting is not authoritative; final visual judgment remains on Cycles evidence.

A higher-resolution rights-safe Earth texture/material refinement is permitted only if it preserves the accepted geography/world-coordinate convention, is recorded in `hero/assets/manifest.json`, introduces no scientific semantics, and stays inside the existing free/rights-safe production architecture. Any paid/unclear-rights asset remains a CTO human gate.

## STOP / route

Route to Product only if the approved continuous narrative, composition or visual invariants require a material change; if a new production dependency/architecture is required; or if quality cannot be achieved within the rights-safe/free tooling envelope without a Product trade-off.

Route to Science if any real analytical output or semantic interpretation is requested before a later accepted data-layer authority.

Human gate for paid/licensed assets/services, credentials/admin access, destructive/irreversible actions or commercial commitments.

Do not stop for normal keyframe/camera revisions, shader tuning, render performance, local tooling issues, geometry fixes, evidence generation or conformant polish.

## Branch / publication policy

Continue on `feat/web-hero-001-predata-scene`. Normal bounded implementation/revision commits are Claude-owned through `REVIEW_READY`; no feature work on `main`, no force push/history rewrite. Completion of this task does **not** authorize live hero integration. The accepted output becomes an input to the later real-data hero phase and `WEB-005` integration/release gate.

Publication/readiness does not auto-start Claude execution. CTO deliberate start remains required.