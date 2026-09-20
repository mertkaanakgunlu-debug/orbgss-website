# WEB-005B R11 — Claude Code Desktop Implementation Handoff

**Linear:** MER-109  
**State:** CTO_START_GRANTED / READY_FOR_CLAUDE_DESKTOP_START  
**Supersedes execution-routing wording in:** R10 only  
**Design decision:** FINAL CLAUDE DESIGN ACCEPTED FOR IMPLEMENTATION  
**Repository:** `mertkaanakgunlu-debug/orbgss-website`  
**Implementation branch:** `feat/web-005b-homepage-visual-fidelity`  
**Verified remote branch head before start:** `176e345166bcc084219aa5972c3209c872889626`  
**Accepted immutable hero upstream:** `1135e7a7e0b0f6db6348dee139d505550d8ca8b9`  
**Architecture:** semantic HTML + CSS + progressive-enhancement vanilla JavaScript

## 1. Execution model

This task is started manually by the CTO in **Claude Code Desktop**.

Do not route through E&D or Control Plane for this implementation run.

The CTO will share the accepted Claude Design artifact directly into the Claude Code session. That shared design is the visual target for layout, composition, hierarchy and responsive intent.

Canonical Product authority remains the Git task chain; the design artifact does not override scientific, content, hero, architecture or release boundaries.

## 2. Start verification

Before editing:

1. verify repository identity;
2. verify working tree state;
3. verify local/remote state of `feat/web-005b-homepage-visual-fidelity`;
4. verify the branch can be based on exact remote `176e345166bcc084219aa5972c3209c872889626` without destructive reset;
5. read R10 and this R11;
6. inspect the shared Claude Design artifact;
7. inspect existing homepage implementation/tests/assets before deciding code structure.

If the working tree contains unknown user changes, or branch identity cannot be reconciled safely, STOP and report exact facts. Do not discard work.

## 3. Implementation objective

Translate the accepted final Claude Design homepage into the existing production stack with high visual fidelity.

This is not another concept exploration.

Implement:
- accepted post-hero composition;
- Act 02 / The Place;
- Act 03 / The Evidence shared-frame layer selector;
- Act 04 / The Result;
- Domains hierarchy;
- proof/differentiator treatment;
- Company;
- Contact/footer;
- responsive desktop/mobile behavior;
- continuity polish required by R10.

Preserve the existing approved hero exactly.

## 4. Three-pass execution envelope

### Pass A — structural design integration

Rebuild the homepage post-hero structure to match the accepted design:
- semantic markup;
- layout/grid/container system;
- typography hierarchy;
- spacing;
- image framing;
- cards/metadata/caveats;
- layer-selector interaction;
- domain hierarchy;
- company/contact composition.

Prioritize structural fidelity before micro-polish.

Do not optimize media quality beyond the current accepted WEB-005B assets in this pass; WEB-007..010 remain post-WEB-006 work.

### Pass B — continuity and interaction polish

After structural fidelity is in place, fix the known continuity defects:
- hero owns initial viewport; no Act 02 leakage at scroll position 0;
- Acts 02/03/04 share one governing page background;
- remove visually abrupt full-width near-black/navy changes;
- soften Hero→Place, Place→Evidence and Evidence→Result handoffs;
- preserve generous centered gutters on large monitors;
- use only restrained opacity/translate reveals where useful;
- preserve reduced-motion behavior;
- no scroll-jacking or mandatory scroll snap.

Layer switching:
- one fixed/shared evidence frame;
- Terrain / THM-01 / ALT-01 selectable;
- selected state visible beyond colour alone;
- crossfade only;
- keyboard/touch accessible;
- no three-card gallery.

Do not invent a compare slider unless it exists in the final shared accepted design. If present there, implement only at the location and role shown by the accepted design.

### Pass C — review/evidence hardening

Run existing validators and add/update only tests needed by the new final layout.

Capture:
- full desktop screenshot;
- full mobile screenshot;
- top-of-page desktop + mobile proof showing no Act 02 leakage;
- short real-browser scroll recording showing Hero→Place→Evidence→Result→Domains;
- representative layer-selector states;
- reduced-motion evidence.

Return exact local commit/head, changed paths, test results and artifact paths.

## 5. Visual authority

Use the shared final Claude Design for:
- proportions;
- composition;
- spatial rhythm;
- hierarchy;
- placement;
- responsive intent.

Do **not** blindly reproduce prototype artefacts that contradict canonical rules.

In particular:
- repository `main` is stale for the current hero and must not be used as hero authority;
- old `hero-handoff` result-card UI is obsolete;
- the accepted WEB-005A hero remains immutable;
- final page should feel continuous rather than like stacked gallery pages.

## 6. Content boundary

The shared design is **not final marketing-copy authority**.

Do not invent or materially expand:
- accuracy/performance claims;
- customer claims;
- ROI;
- validation claims;
- quantitative metrics;
- scientific promises.

Preserve existing canonical EN/TR meaning wherever possible.

If the design uses different placeholder wording mainly to demonstrate layout, prioritize the accepted visual structure and retain safe/current product wording. Record any unavoidable copy delta explicitly in evidence.

No fake metric placeholders in shipping implementation.

## 7. Scientific/media boundary

Consume MER-108 and Product public-presentation authority.

For this task:
- use current accepted WEB-005B presentation assets;
- do not perform the later WEB-007 high-fidelity media program;
- no AI super-resolution;
- no sharpening/blur/denoise of analytical data;
- no new slope overlay;
- no palette/normalization/mask semantic change;
- no scientific reprocessing.

Current lower-fidelity assets may be swapped later under WEB-007..010 without redesign.

## 8. Architecture boundary

Keep:
- static HTML;
- CSS;
- vanilla JavaScript.

No React/Vue/Next/Svelte migration.
No WebGL requirement.
No new build framework unless an existing repo tool already requires it.

Claude may use normal engineering judgment for code organization, responsive CSS, DOM structure, test fixtures and bounded refactors that do not change published semantics.

## 9. Hero hard boundary

Do not:
- rerender Blender;
- modify hero video;
- modify choreography;
- change drape timing;
- change hero analytical sequence;
- reintroduce obsolete hero result UI.

Integration may adjust only surrounding layout/container behavior required to make the approved hero own the first viewport and transition cleanly into Act 02.

## 10. Scope boundary

Homepage only.

Do not redesign:
- Geothermal route;
- Mining route;
- Marine route;
- About route;
- Partner/Contact routes;
- global information architecture beyond homepage navigation adjustments already required by the accepted design.

Do not start WEB-006.
Do not merge to `main`.
Do not deploy or change DNS.

## 11. Commit / publication behavior

Work on `feat/web-005b-homepage-visual-fidelity` from the verified exact branch head.

A local implementation commit is authorized.

Do not force-push.
Do not merge.
Do not deploy.

If normal remote publication is needed solely to surface review artifacts, report REVIEW_READY first and wait for CTO instruction unless the session was explicitly given separate push authority.

## 12. Acceptance

The implementation is ready for CTO review when:

- shared final design is recognizably reproduced;
- hero is unchanged;
- no Act 02 initial-viewport leakage;
- page continuity no longer has hard section-colour cuts;
- layer selector works accessibly;
- Result remains visually dominant;
- domain hierarchy matches accepted design;
- desktop/mobile stay centered and low-density;
- no horizontal overflow;
- reduced motion works;
- existing scientific/display invariants pass;
- relevant tests and `git diff --check` pass;
- real-browser scroll evidence exists.

**Terminal return:** `REVIEW_READY / WAITING_CTO_VISUAL_REVIEW`.

After CTO review, only bounded visual polish/revision remains inside MER-109. WEB-006 stays blocked until MER-109 is terminally accepted.
