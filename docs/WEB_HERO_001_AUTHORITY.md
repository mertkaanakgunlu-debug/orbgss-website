# WEB-HERO-001 — Pre-data cinematic hero authority

**State:** `CTO_START_APPROVED / READY_FOR_CLAUDE_DESKTOP_START`  
**Product owner:** Product & Software  
**Canonical Drive authority:** [CURRENT — OrbGSS Hero Visual & Production Authority v1.0](https://docs.google.com/document/d/1dFseWdo8CzasXUlj37adGiDeHzNzyYKeSIFnqYu4qjc/edit)  
**Website CURRENT authority:** [v1.6](https://docs.google.com/document/d/1pogJgQ1XtNSW12z4sGqedn_r_tqcIDEQczM6G707vTY/edit)  
**Linear parent:** `MER-97`  
**Repository:** `mertkaanakgunlu-debug/orbgss-website`  
**Branch:** `feat/web-hero-001-predata-scene`  
**Baseline:** `main@677bfa7672ac18c2c808ddaaf235ff12863de443`

## Decision

WEB-HERO-001 is a parallel-safe, pre-data production lane. It may proceed while WEB-002/003/004 continue because it is isolated under `hero/` and does **not** integrate the live homepage, publish scientific outputs, change deployment, or change DNS.

The previous rule that all hero production waits for WEB-004 is superseded only for this isolated pre-data lane. `WEB-005` remains the final real-data/media/site integration and release gate.

## Locked visual invariants

1. **Earth is true 3D geometry.** It is a sphere with coherent curvature, perspective, atmosphere, lighting and camera relationship; it is not a flat matte/background.
2. **AOI is surface-conforming.** AOI corners are anchored on the sphere; sampled borders follow the spherical surface with only a minimal anti-z-fighting offset. A flat screen-space quadrilateral pasted onto Earth is a failure.
3. **Scan geometry is registered in 3D.** Satellite acquisition beams and corner locks target the actual AOI footprint/corners and stay registered as the camera moves.
4. **Scale continuity is continuous, not editorial.** Global acquisition and regional approach are one scene/camera path. Frame-2/3/4-equivalent shots preserve the same AOI identity, center, orientation and geometry with no jump-cut scale mismatch.
5. **Acquisition palette:** deep navy/black space, restrained electric cyan / ice-blue / teal for atmosphere, scan, AOI and acquisition cues. Avoid purple/pink neon overload and HUD clutter.
6. **Future analytical palette:** cool cyan/teal → green → yellow → orange → warm red may be used later only to present approved real outputs. WEB-HERO-001 must not fabricate scientific values to demonstrate that palette.
7. **Premium but credible.** The sequence should be cinematic and engaging to non-technical audiences without becoming game-like, stock-space spectacle, or a fake sensor simulation.
8. **Website copy is never baked into the render.** Headline/CTA remain HTML in the later integration task.

## Scientific boundary

WEB-HERO-001 is deliberately pre-data.

Allowed: Earth/space materials; satellite; orbit path; configurable design AOI; scan beams; corner locks; surface-following scan sweep; neutral design-only placeholder surface needed to validate transitions.

Forbidden: fabricated DEM, thermal, alteration, fault, geology, structural, geothermal or score/prospectivity maps; fake fault traces; pseudo-scientific heatmaps; any change to Science semantics or any public presentation that could be mistaken for measured output.

The scene must expose a clean configuration/data-injection interface so later accepted AOI geometry and rendered scientific layers can replace the design fixture without rebuilding the scene system.

## Production architecture

All new production work belongs under `hero/` except explicitly allowed documentation/ignore changes.

Preferred shape (implementation may refine names without changing boundaries):

```text
hero/
  README.md
  config/
  scripts/
  assets/
    manifest.json
    source/
  blender/
  renders/        # local/ignored unless a task publishes bounded evidence
  evidence/
```

Blender Python + committed configuration are the reproducible source of scene truth. Manual Blender edits are allowed for bounded artistic work only if the resulting state remains reproducible or is captured in a bounded source `.blend` with a documented generation/edit path.

Preview iteration may use Eevee or low-sample Cycles. Master visual quality targets Cycles with GPU acceleration where available. FFmpeg is permitted as local production tooling; none of these introduce a website runtime dependency.

External assets require provenance/license/checksum records in `hero/assets/manifest.json`. Paid assets, unclear-rights assets, credentials, API keys or commercial commitments require a CTO human gate.

## Phase graph

`WEB-HERO-001A / MER-98` → `WEB-HERO-001B / MER-99` → `WEB-HERO-001C / MER-100` → `WEB-HERO-001D / MER-101`

- **001A:** production scaffold + render benchmark.
- **001B:** Earth, space, satellite + orbit cinematography.
- **001C:** spherical AOI acquisition + scan system.
- **001D:** continuous pre-data animatic + quality gate.

## Common branch and write-surface policy

- No feature work on `main`.
- Continue all four phases on `feat/web-hero-001-predata-scene` unless Product publishes a revision.
- Do not modify `index.html`, `styles.css`, `script.js`, public proof imagery, Vercel/deployment configuration, DNS or production-domain state in WEB-HERO-001.
- Normal bounded implementation commits are implementer-owned; no artificial micro-commit budget.
- Avoid committing render sequences or large generated binaries merely as progress evidence. Prefer reproducible source, checksums/pointers and a bounded set of review artifacts.
- No force push, destructive history rewrite, data deletion or irreversible external action.

## Common evidence

Every phase closes at `REVIEW_READY` with exact branch/HEAD, changed paths, tool versions, commands, render settings relevant to the phase, evidence pointers/hashes, acceptance results, and known limitations.

## Routing

Product re-entry is required only for a new visual/product behavior, architecture/dependency change, scope/acceptance change, or material conflict with this authority. Science re-entry is required only if a later step needs scientific interpretation or data semantics. Paid/licensed assets, credentials/admin access, destructive actions or commercial commitments are human gates.

Routine Blender/Python issues, shader tuning, camera/keyframe work, geometry implementation, render setup, GPU/CPU fallback, local dependency/tool setup, file-path problems, preview iteration, evidence generation and small conformant refactors are implementer-owned.