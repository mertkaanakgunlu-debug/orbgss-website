# OrbGSS Website — Post-WEB-006 Media Fidelity Roadmap

**State:** PLANNED / NOT STARTED  
**Linear milestone:** 5 — Media Fidelity & Runtime Hardening  
**Architecture:** semantic HTML + CSS + progressive-enhancement vanilla JavaScript

## Purpose

After WEB-006, raise the production site's media quality and runtime smoothness without reopening the accepted design or migrating frameworks.

The work separates four concerns so design, scientific display semantics and runtime performance do not get mixed together.

## Sequence

```
WEB-006 / MER-95
      |
      +---------------------+
      |                     |
WEB-007 / MER-143      WEB-008 / MER-144
Analytical masters     Hero adaptive delivery
      |                     |
      +----------+----------+
                 |
          WEB-009 / MER-145
          Media integration
                 |
          WEB-010 / MER-146
          4K/HiDPI acceptance
```

WEB-007 and WEB-008 may run in parallel after deliberate CTO start. WEB-009 waits for both. WEB-010 is terminal.

## Governing decisions

1. **No framework migration.** React/Vue/etc. do not improve pixel fidelity and are not part of this program.
2. **Public website != technical report.** Public display derivatives may be polished for clarity and perceived quality, within accepted Science bounds.
3. **Scientific masters remain authoritative.** Web derivatives never feed science/report/validation workflows.
4. **Terrain presentation:** governed elevation palette + neutral hillshade. No slope overlay without a separate Science decision.
5. **Analytical interpolation:** only MER-108-authorized display interpolation/resampling; no generative enhancement, sharpening or invented detail.
6. **Hero:** highest perceptual quality that plays smoothly; adaptive encodes, not one maximal file for everyone.
7. **Performance:** first preserve meaning, then focal quality, then smoothness; solve weight through responsive delivery before reducing fidelity.
8. **Modularity:** later copy, domain text, imagery or a verified metric can be swapped/inserted as bounded frontend changes without redesign.

## Existing authority consumed

- WEB Media Fidelity Architecture
- WEB Public Presentation Fidelity Policy
- WEB-005B R9 Visual Fidelity & Runtime Performance Plan
- MER-108 Website/Public-Facing Display Derivative Authority
- final CTO-accepted homepage design once published

## Human gate

All four issues are planning/publication only. None is started by this roadmap. New execution requires CTO start after WEB-006 as specified by each issue.

## Completion

The program closes when WEB-010 reaches `MEDIA_FIDELITY_ACCEPTED` with real-browser evidence, including a 4K/high-DPR class when available.
