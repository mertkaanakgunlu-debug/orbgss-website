# WEB-005B R13 — Implementation Review Disposition & Bounded Domain Revision

**Linear:** MER-109  
**State:** REVISION_REQUIRED / BOUNDED_PRODUCT_CORRECTION  
**Implementation under review:** local feat/web-005b-homepage-visual-fidelity@4e6c7c106399140565c77da0febe59ffc14f3ab3  
**Base:** 176e345166bcc084219aa5972c3209c872889626

## 1. Review disposition

The R11 implementation is technically acceptable enough to proceed to a bounded revision rather than reopening design.

Reported implementation evidence is GREEN:
- site validator PASS;
- hero 420/0;
- WEB-005 negative suite 72/72;
- WEB-005B negative suite 42/42;
- git diff --check clean;
- immutable hero preserved;
- continuity defects addressed;
- responsive evidence and real-browser scroll evidence produced.

Do not reopen the homepage concept or rewrite the implementation.

## 2. Mandatory correction — domain taxonomy

The implementation's visible homepage domain taxonomy must follow the accepted Product authority:

- **Geothermal** — active / first application
- **Mining** — in development
- **Marine** — in development

The implementation's substitution of **Mineral Exploration** and **Environmental & Land Intelligence** is not accepted.

Reason:
- R7/R10 explicitly bind Mining and Marine as the accepted homepage domain taxonomy;
- existing route anchors or current /solutions/ taxonomy do not override the accepted homepage Product decision;
- a missing/unfinished route is a routing/availability concern, not authority to silently rename the domain.

Implementation options:
- visible labels remain Mining / Marine;
- if a matching destination route is not yet production-ready, the card may remain non-navigating / disabled / in development;
- do not invent a new homepage domain solely to satisfy an existing anchor;
- do not redesign the cards.

This is the only mandatory Product correction identified from the implementation report.

## 3. Accepted implementation deviations

### Mobile Act 02

Accepted.

Moving copy below the image at narrow widths to preserve legibility is conformant responsive implementation judgement. Desktop retains the integrated image/copy composition; mobile need not force text over bright imagery.

### AOI overlay under protection shade

Accepted.

The AOI geometry may remain partially subdued beneath the desktop protection shade when that is required for copy legibility. Do not change the crop merely to expose every corner unless visual review later shows the AOI is misleading or unreadable.

The overlay is presentation framing, not a scientific analytical layer.

### Co-registered inspection aid

Accepted, subject to the already-published placement/content authority.

The inspection module may remain between Result and Domains. Its browser interaction must use the recorded co-registration rather than approximate alignment.

### Production assets vs prototype assets

Accepted.

Using governed/accepted WEB-005B assets instead of blindly copying the Claude Design prototype's proof/final files is correct.

### Domain-photo captions

Accepted.

Truthful captions/provenance on illustrative domain imagery are preferred to implying those images are outputs from the active Kızıldere pilot.

## 4. Environment note

Installing Pillow/websocket-client in the local Python environment is not a Product blocker so long as:
- no unrelated repository dependency change was committed;
- validation remains reproducible in the documented development environment;
- the implementation does not silently require an undeclared runtime dependency for the public site.

## 5. Revision envelope

Modify only what is required to restore the canonical domain taxonomy and any directly coupled homepage selector/link/accessibility/test/manifest text.

Do not:
- redesign the homepage;
- alter hero;
- alter analytical rendering;
- redo media derivatives;
- change continuity behavior;
- change Company/Contact;
- start WEB-006;
- merge/deploy/DNS.

A single bounded local revision commit is authorized.

## 6. Evidence after revision

Re-run only the affected/full required validators as appropriate and provide:
- exact revised local HEAD;
- changed paths;
- test results;
- updated Domains desktop/mobile captures;
- confirmation that the rest of R11 evidence remains representative or updated evidence if the revision affected it.

Then return:
REVIEW_READY / WAITING_CTO_VISUAL_REVIEW.

The CTO visual gate remains required before MER-109 terminal acceptance.
