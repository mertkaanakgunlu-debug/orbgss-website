# WEB-005 — Cinematic Hero Production, Homepage Integration & Release-Candidate Gate

**Linear:** `MER-93`  
**Status:** `READY_FOR_CTO_APPROVAL — NOT STARTED`  
**Canonical repository:** `mertkaanakgunlu-debug/orbgss-website`  
**Implementation branch:** `feat/web-005-cinematic-hero`  
**Execution baseline:** `main@d2421a772f2e4cfa38c85dd5ee71a419c5160838`  
**Publication semantics:** this file publishes exact Product authority only. It does **not** start implementation. A deliberate CTO start is required.

## 1. Outcome

Produce the final pre-launch OrbGSS homepage release candidate by consuming the accepted WEB-HERO-001D cinematic system and the accepted GEO-WEB-002 public-safe visual package, then integrating them into the existing WEB-004-hardened six-route site.

WEB-005 owns one coherent engineering outcome:

1. finish the accepted pre-data cinematic hero with the authorized real-data/result handoff;
2. encode and integrate production hero media and truthful fallbacks;
3. replace the intermediate six-scene homepage gallery with the locked four-act final homepage narrative;
4. preserve accepted science, routes, EN/TR parity, accessibility, provenance and performance behavior; and
5. leave one evidence-backed release candidate ready for Product terminal review and later WEB-006 launch.

WEB-005 is **not** a deployment/DNS task.

## 2. Exact upstream authority and accepted inputs

### Product presentation authority

- `main@8a4fe9ba5cb19d09390cb8816c2324e012331728:docs/WEB_PUBLIC_VISUAL_NARRATIVE_AUTHORITY.md`
- Current baseline includes that authority and all later accepted website publications through `main@d2421a772f2e4cfa38c85dd5ee71a419c5160838`.

The homepage hierarchy is locked to exactly four major visual acts:

**Hero → real AOI context → compact evidence trio → priority/result climax**.

### Accepted WEB-HERO-001D input / MER-101

- branch: `feat/web-hero-001-predata-scene`
- accepted implementation HEAD: `93e17f6293aeb8bdc882dfd28221ed786b772df1`
- accepted REVIEW_READY/evidence HEAD: `e95fdcac7cac82e597d40dab4cdc96ce1a6b319e`
- terminal Product acceptance: `e95fdcac7cac82e597d40dab4cdc96ce1a6b319e:tasks/WEB-HERO-001D_TERMINAL_PRODUCT_ACCEPTANCE.md`
- accepted downstream join: stable regional AOI hold + `aoi_injection_interface.layer_slots`

WEB-005 must consume this accepted production source rather than redesigning the Earth/satellite/AOI geometry, camera/world convention, acquisition scan, or stable regional hold. The review animatic is an input/evidence artifact, not production website media.

### Accepted GEO-WEB-002 input / MER-102

Canonical package is on the execution baseline:

- `docs/GEO-WEB-002_FINAL_VISUAL_MASTER_PACKAGE.md`
- `docs/GEO-WEB-002_SCIENCE_ACCEPTANCE.md`
- `tasks/GEO-WEB-002_FINAL_HOMEPAGE_VISUAL_MASTERS_ACCEPTANCE.md`
- machine-readable provenance/checksum record: `assets/imagery/sources.json -> geo_web_002`

Terminal Science acceptance is complete. WEB-005 may bind and present these assets; it may not reopen or reinterpret their scientific semantics.

Bound asset roles are:

- **Act 2:** accepted Kızıldere natural-colour EO context package (`kizildere-aoi-context-2025*`), including the 2400 × 1500 master and approved responsive derivatives;
- **Act 3 / Terrain:** accepted `terrain` final derivative;
- **Act 3 / Thermal:** accepted `thm01` final derivative;
- **Act 3 / Alteration:** accepted `alt01` final derivative as the default alteration card selected by the GEO-WEB-002 package;
- **Act 4:** accepted `mvp_remote_sensing_priority_v1` final priority derivative and its exact public semantics.

Class-B scientific derivatives have a maximum safe rendered long axis of **1249 device px** under the accepted package. WEB-005 must use contained/max-width composition rather than browser or video-frame upscaling that materially exceeds that limit.

### WEB-004 regression baseline

WEB-004 remains the accepted hardening baseline. Preserve:

- canonical routes `/`, `/platform/`, `/solutions/`, `/pilot/`, `/company/`, `/contact/`;
- static HTML/CSS/vanilla-JS architecture;
- accepted responsive/accessibility/navigation behavior;
- EN default / TR parity and persistence;
- provenance/checksum and public-claim discipline;
- `CONTACT_RELEASE_GATE` until WEB-006 verifies mailbox ownership/delivery;
- production hero media envelope:
  - autoplay WebM `<= 3.0 MiB`;
  - MP4 fallback `<= 4.5 MiB`;
  - poster `<= 180 KiB`;
  - mobile/reduced-data must have an intentional static/poster experience and must not download both video encodes.

No accepted scientific proof asset may be visually reinterpreted merely to improve page aesthetics or synthetic performance scores.

## 3. Product behavior and visual invariants

### Act 1 — Cinematic acquisition hero

The hero must remain one continuous visual story rooted in the accepted WEB-HERO-001D system:

Earth establish → satellite entrance → AOI acquisition/scan → continuous camera approach → stable regional AOI hold → approved real-data/result handoff.

The post-hold data handoff may reveal accepted evidence/result media through the accepted injection interface, but it must not imply fabricated sensor physics, direct satellite-to-score causality, mineral identification, geothermal probability, reserve/resource, discovery likelihood, or drilling-success likelihood.

Implementation strategy for the post-hold transition is deliberately not prescribed. It may use conformant 2D/3D compositing, contained planes, masks, transitions or camera treatment as long as:

- accepted world/AOI registration is not silently changed;
- accepted class-B pixels are not recoloured, reclassified, value-transformed, reprojected or misleadingly warped;
- any scientific visual remains within its truthful safe display density;
- the viewer can distinguish acquisition imagery from analytical evidence/results;
- the final result remains the accepted remote-sensing priority output, not a fabricated hero-only visualization.

HTML headline/copy must stay outside the rendered media and occupy a protected motion-safe region. A restrained dark contrast treatment is allowed; baked marketing copy in the video is not.

### Act 2 — Real Kızıldere AOI context

Immediately after the hero, show one strong accepted natural-colour EO view of the Kızıldere area. Copy and provenance must be visually coupled to the image. The act must identify it as geographic/EO context, not analytical evidence and not the acquisition date of THM/ALT evidence.

### Act 3 — Compact evidence trio

Use one deliberate three-evidence composition only:

1. Elevation — NASADEM context;
2. THM-01 Thermal Anomaly;
3. ALT-01 Alteration Proxy — clay/hydroxyl.

The three visuals must clearly belong to the same AOI/story stage. Their exact warnings, labels, source attribution and semantic roles come from the accepted GEO-WEB-002 package.

Structure/Geology remains `optional support / DATA_GAP / score-invariant` and must not be fabricated or promoted into a standalone major homepage act.

### Act 4 — Priority/result climax

Use the accepted priority output with the exact public label:

**Remote-Sensing Relative Priority — Experimental Baseline**

It is an AOI-relative 0–100 screening/ranking result, not probability and not Full Prospectivity. It must be presented as the analytical climax answering “where to look next” while respecting the accepted 1249-device-pixel safe limit.

A compact truthful legend may be integrated inside the visual frame if useful. Detached homepage colour bars/scale strips are prohibited.

### Supporting homepage content

Existing supporting geothermal, expansion-direction, trust/company and contact/partnership content may follow the four acts, but must remain visually subordinate and must not recreate the superseded six-scene full-width technical gallery rhythm.

Deep methodology/detail remains on accepted `/pilot/` and `/platform/` routes.

## 4. Scientific/data boundary

WEB-005 is presentation/integration authority only.

It must not change or invent:

- scoring method, weights, thresholds or feature eligibility;
- CRS, grid, units, NoData, masks or resampling semantics;
- THM/ALT scientific interpretation;
- validation, uncertainty or probability semantics;
- acquisition dates not present in accepted authority;
- structure/geology evidence;
- MTA paid/closed/restricted content;
- the meaning of `mvp_remote_sensing_priority_v1`.

Class-B assets must not receive CSS/video/post-processing that changes their governed colours/contrast/opacity in a way that alters interpretation. Presentation crops/downscales are allowed only within the exact accepted GEO-WEB-002 rules.

## 5. UX, accessibility and localization

WEB-005 may materially improve homepage composition but must not regress the accepted site behavior.

Required:

- responsive layouts at representative 375 / 768 / 1024 / 1440 CSS px;
- no horizontal overflow, clipped copy, inaccessible controls or unstable media sizing;
- keyboard-accessible navigation and controls remain intact;
- visible focus, skip-link/landmarks/headings and accepted ARIA behavior remain intact;
- EN/TR visible-copy and accessible-name parity remains complete;
- scientific warnings/labels remain available and readable in both languages;
- `prefers-reduced-motion` gets an intentional non-animated or minimal-motion hero state;
- reduced-data/mobile strategy must not force both hero video encodes to download;
- poster/fallback state must retain sufficient contrast for separate HTML hero copy.

The hero may autoplay only when browser/platform policy and the accepted muted/inline behavior allow it. Failure to autoplay must degrade cleanly to an intentional poster/static state without obscuring primary content.

## 6. Performance and media contract

The accepted WEB-004 site is the regression baseline. WEB-005 must not silently relax its budgets.

Mandatory hero ceilings:

- WebM `<= 3.0 MiB`;
- MP4 `<= 4.5 MiB`;
- poster `<= 180 KiB`.

Use production-oriented encoding, dimensions and delivery rather than shipping the Phase-D review animatic as-is. Record codec/container, pixel dimensions, frame rate, duration, bytes and SHA-256 for each production hero asset.

The page must avoid duplicate/unnecessary eager media requests and major layout shift. Responsive imagery must use deliberate source selection; class-B assets may not be stretched beyond accepted safe display density merely to fill desktop width.

WEB-004 accessibility / Best Practices / SEO floors and the accepted performance evidence remain regression references. If meeting the media contract still produces a material performance regression that cannot be fixed without changing accepted Product/Science behavior, return to Product rather than weakening the gate.

## 7. Allowed implementation envelope

Implementation may modify the existing website and accepted hero production source only as needed to achieve the outcome. Expected conformant change classes include:

- homepage HTML/CSS/vanilla JS composition;
- responsive media delivery and fallbacks;
- production hero scene/config/render/encoding support carried forward from the exact accepted WEB-HERO-001D source;
- rights-safe production hero assets derived from already accepted inputs;
- existing site validation/tests where required to encode the new four-act invariants;
- repository evidence/status/provenance records for WEB-005.

Do not mechanically merge unrelated history from the hero branch. Bring forward only the exact accepted hero production files/history needed for WEB-005 and retain exact provenance to `e95fdcac7cac82e597d40dab4cdc96ce1a6b319e`.

Ordinary implementation strategy, file decomposition, bounded refactors, encoding iteration and test repair are implementer-owned. No planner-authored micro-step sequence or artificial implementation commit limit is imposed.

## 8. Explicitly out of scope

- production deployment or promotion;
- Vercel production-domain attachment/change;
- Squarespace/DNS mutation;
- MX/SPF/DKIM/DMARC/Google Workspace administration;
- analytics, tracking, cookies/consent systems, CRM, auth, database, forms backend or PII collection;
- framework/package-manager/CMS migration;
- a new scientific method or visual reinterpretation of accepted scientific assets;
- paid/licensed/unclear-rights media or data;
- MTA closed/restricted data;
- new routes or public product claims outside accepted authority;
- redesign of deep routes unless a bounded homepage integration regression requires a conformant fix;
- WEB-006 launch work.

## 9. Acceptance

WEB-005 reaches `REVIEW_READY` only when all of the following are true:

1. Homepage has exactly four major visual acts in the required order: Hero → real AOI context → compact evidence trio → priority/result climax.
2. The old six-scene Observe/Terrain/Evidence/Structure/Priority/Geothermal full-width homepage gallery is gone.
3. The accepted WEB-HERO-001D cinematic geometry/continuity is consumed rather than rebuilt incompatibly, and the final production hero reaches a stable truthful real-data/result handoff.
4. Hero scientific/result reveals use only accepted GEO-WEB-002/public-safe assets or exact conformant derivatives and introduce no fabricated science.
5. Production WebM, MP4 and poster satisfy the media ceilings and have recorded dimensions/codec/duration/bytes/SHA-256.
6. Hero HTML copy remains separate, readable and protected across desktop/mobile/fallback states.
7. Mobile, reduced-motion and reduced-data/fallback behavior is intentional; no dual-video download is required.
8. Act 2 uses the accepted Kızıldere EO context and retains its context-only meaning and USGS attribution.
9. Act 3 is exactly the compact Terrain + THM-01 + ALT-01 evidence composition with truthful labels/warnings and no fabricated Structure/Geology scene.
10. Act 4 uses the accepted priority output and exact public label/meaning; its raster is not visibly upscaled beyond the accepted safe density.
11. No detached decorative homepage scientific legend/scale strip remains; any necessary legend belongs inside its visual.
12. Copy-to-visual ownership is clear and composition varies intentionally rather than repeating one template.
13. EN/TR content/accessibility parity remains green.
14. Canonical routes, navigation, keyboard behavior, responsive layout and accepted deep-route content remain green.
15. Existing provenance/checksum/public-claim validators remain green and validate the final shipped visual/media inventory.
16. WEB-004 performance/accessibility quality does not materially regress without an explicit Product decision.
17. No production deployment, domain/DNS mutation, analytics/backend or unrelated architecture change occurred.

## 10. Mandatory verification and evidence

At final implementation HEAD provide at minimum:

- exact branch and final implementation HEAD;
- changed-path inventory;
- exact WEB-HERO-001D source files carried forward and provenance pointer to `e95fdcac7cac82e597d40dab4cdc96ce1a6b319e`;
- hero scene/geometry/continuity validation relevant to the accepted Phase-D invariants;
- repository site validator result (`py -3.14 scripts/validate_site.py`, or the canonical interpreter invocation if the environment resolves the same validator differently);
- link/asset/provenance/checksum validation;
- desktop/tablet/mobile screenshots of all four homepage acts, including representative 375 / 768 / 1024 / 1440 px evidence;
- visual-quality inventory for every major homepage visual: source/master dimensions, selected derivative, actual rendered dimensions and safe-density decision;
- production WebM/MP4/poster codec/container, dimensions, frame rate, duration, bytes and SHA-256;
- hero autoplay/playback/fallback evidence and reduced-motion/mobile/reduced-data behavior;
- keyboard/focus/navigation/language-persistence regression evidence;
- EN/TR visible-copy and accessible-name parity result;
- performance regression evidence against the accepted WEB-004 baseline, including media request behavior and layout stability;
- confirmation that scientific labels/warnings/priority semantics match accepted authority exactly;
- explicit `NOT RUN` for any genuinely unavailable check rather than implied PASS.

A hosted preview may be produced only if already-authorized credentials/context are available without admin, payment, ownership or production-domain changes. Hosted preview absence does not justify production access requests; a reproducible local preview is sufficient for WEB-005 review.

## 11. Genuine STOP / domain-route conditions

Return `WAITING_DOMAIN_DECISION` only if completion requires one of the following:

- changing accepted homepage behavior/hierarchy, product claims or UX policy;
- changing framework/application architecture or adding a new runtime dependency policy;
- changing any Science/data semantics, accepted raster interpretation or priority meaning;
- using an asset outside accepted public-safe/rights authority;
- exceeding the accepted scientific image safe-density limits as a Product acceptance trade-off;
- loosening the hero media envelope or accepted accessibility/performance policy;
- production deployment/domain/DNS changes;
- credentials/admin/ownership transfer, payment/purchase or commercial/legal action;
- destructive/irreversible action or history rewrite;
- scope expansion into WEB-006.

Routine HTML/CSS/JS defects, browser quirks, render/encode iteration, responsive bugs, accessibility fixes, fixture/validator repair, local environment issues, bounded conformant refactors and evidence/publication defects remain inside implementation/E&D.

If accepted source authorities conflict, stop with the exact conflicting pointers; do not silently choose new Product or Science semantics.

## 12. Branch and publication policy

- No feature work on `main`.
- Implement only on `feat/web-005-cinematic-hero` from the published authority baseline.
- Normal bounded implementation/revision commits are allowed; no force-push, amend/rebase of published authority history, destructive reset or history rewrite.
- Do not merge to `main` during implementation.
- E&D/implementer owns routine revision through GREEN/`REVIEW_READY` under this contract.
- Product performs terminal exact-head acceptance and main publication after review.
- WEB-006 may not begin from this publication alone.
- Production DNS/cutover remains a separate CTO human gate under WEB-006 / MER-95.

**Terminal implementation state:** `REVIEW_READY`  
**Current planning state after this authority publication:** `READY_FOR_CTO_APPROVAL`.
