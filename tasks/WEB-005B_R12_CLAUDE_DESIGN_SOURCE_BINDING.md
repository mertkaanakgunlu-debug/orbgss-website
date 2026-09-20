# WEB-005B R12 — Claude Design Source Binding

**Linear:** MER-109  
**State:** CTO_START_GRANTED / READY_FOR_CLAUDE_DESKTOP_START  
**Execution model:** manual Claude Code Desktop session  
**Design source:** https://claude.ai/design/p/c46c985e-4acd-49e0-9354-704f276beca7?file=OrbGSS+Homepage+-+Final+Direction.html

## 1. Bound design artifact

The Claude Design project above is the accepted visual implementation reference for WEB-005B.

Primary design file:
- `OrbGSS Homepage - Final Direction.html`

Design-system/reference files expected from the selection import:
- `_ds/orbgss-design-system-096b090f-3293-4b14-aafd-1a64575755ab/tokens/colors.css`
- `_ds/orbgss-design-system-096b090f-3293-4b14-aafd-1a64575755ab/tokens/effects.css`
- `_ds/orbgss-design-system-096b090f-3293-4b14-aafd-1a64575755ab/tokens/fonts.css`
- `_ds/orbgss-design-system-096b090f-3293-4b14-aafd-1a64575755ab/tokens/spacing.css`
- `_ds/orbgss-design-system-096b090f-3293-4b14-aafd-1a64575755ab/tokens/typography.css`
- `orbgss-base.css`

Representative design assets may include the Design export's hero poster, context/domain imagery and proof rasters. Those are useful for visual matching but do not automatically become production authority.

## 2. Import semantics

Claude Code should use the `claude_design` MCP to read/import the accepted design project when available.

The imported design is authoritative for:
- composition;
- section hierarchy;
- spacing/rhythm;
- typography intent;
- container widths/gutters;
- card proportions;
- evidence selector visual treatment;
- result composition;
- domain hierarchy;
- company/contact layout;
- responsive intent.

The imported design is **not** a wholesale production-source replacement.

Do not simply copy the full exported HTML/CSS tree over the repository if doing so would bypass the existing production architecture, tests, i18n, accessibility, scientific asset governance or accepted hero.

## 3. Production-authority precedence

When the Design export conflicts with production/canonical authority, precedence is:

1. accepted WEB-005A hero authority;
2. MER-108 + Product scientific/display authority;
3. R10/R11 Product implementation boundaries;
4. current accepted repository behavior/contracts;
5. Claude Design export as visual/layout authority.

Therefore:
- do not replace the accepted hero with the Design project's still/poster or any stale hero representation;
- do not resurrect the old `hero-handoff` UI;
- do not replace governed analytical assets merely because similarly named files are included in the Design export;
- do not replace EN/TR infrastructure with static prototype copy;
- do not migrate to a new framework or standalone generated site.

## 4. Design-token consumption

Claude may:
- adopt/refactor matching colour, spacing, typography and effect values from the imported design system;
- map them into the existing production CSS token system;
- reuse clean CSS declarations/components where they conform to the production architecture.

Prefer integration over duplication.

Do not ship the Design-system export directory as a parallel unused style system when equivalent values can be mapped into the production site.

## 5. Asset handling

For each imported Design asset, decide explicitly whether it is:
- visual reference only;
- already the same accepted production asset;
- a safe temporary/provisional homepage asset;
- outside current WEB-005B authority.

The current WEB-005B implementation should continue using accepted production media unless the Design asset is demonstrably the same source/derivative already authorized.

High-fidelity media replacement remains planned under WEB-007..010 after WEB-006.

## 6. Continuity deviations from prototype

The Design artifact is visually accepted, but R10 intentionally corrects prototype-level continuity defects during implementation:
- hero owns the initial viewport;
- no Act 02 leak at scroll position 0;
- continuous governing background through Acts 02/03/04;
- softer section handoffs;
- no scroll-jacking/snap.

These corrections are required even if the imported prototype renders differently.

## 7. Start command interpretation

The Design-generated prompt:

`Implement: OrbGSS Homepage - Final Direction.html`

means:

**integrate the accepted design into the existing OrbGSS production homepage under R10/R11/R12 constraints.**

It does not mean:
- replace the repository with the exported prototype;
- replace the hero;
- ship all imported assets blindly;
- bypass validators;
- redesign non-homepage routes.

## 8. Review state

Implementation returns:
`REVIEW_READY / WAITING_CTO_VISUAL_REVIEW`

No merge, deploy, DNS or WEB-006 start is implied.
