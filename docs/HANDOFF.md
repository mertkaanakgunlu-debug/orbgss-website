# Handoff

Reconciled by MER-213 on 2026-09-29; current state re-reconciled by MER-218 on 2026-10-03. `STATUS.md` is the current-state record and `CLAUDE.md` the rules; this file only orients a new session.

## Where things stand

- The launched code baseline is `feat/web-005c-public-domain-taxonomy-parity@79cc2cb82a4542461cbbfc1d0c349cf02b861084` (WEB-005 → 005A hero → 005B homepage R15 → 005C Geothermal / Mining / Marine taxonomy). Git `main` is `f4f1d4d6cb6ff4acd4ad02129bb9ec13a50ade85`, the MER-213 documentation commit on top of it (code-identical); per the latest Linear record, Vercel production is a Git deployment of that `main`.
- MER-216 (media fidelity and runtime hardening) is accepted and Done at `claude/mer-216-s1r628@adf08186d3ee4a438bda73886272d05c970e670a`, 3 ahead / 0 behind `main`, and not yet published or deployed. MER-218 is its docs-only publication closure (`REVIEW_READY`); publishing is a separate CTO-approved, non-force fast-forward recorded in `tasks/MER-218_EVIDENCE.md`.
- The site is static HTML, CSS and vanilla JS, six routes, bilingual EN/TR in `script.js`, provenance and checksums in `assets/imagery/sources.json`, enforced by `scripts/validate_site.py`.
- Hero: rendered sequence plus page-composited, lossless drape states. Blender 4.5 LTS is local production tooling, not a runtime dependency, and its large source textures are git-ignored.

## What is deliberately not done

- `main` has not been updated for MER-216; nothing here deploys, changes DNS, credentials or Vercel configuration.
- `CONTACT_RELEASE_GATE` (`contact@orbgss.com` ownership and deliverability) is carried open.
- The repository holds no record of the WEB-006 deploy/DNS execution; the cutover contract is on `docs/web-005-polish-authority@e64d9fd`.
- The Claude Project instructions describe a different navigation (Home / Solutions / About / Partner with us) than the repository and the live site; unresolved, CTO decision.
- WEB-007 / MER-143, WEB-008 / MER-144, MER-145 and MER-146 are canceled and consolidated into MER-216; they are not separate tasks.

## Next session

Wait for an explicit `MER-###'e başla`. Follow the task execution rule in `CLAUDE.md`, branch from the exact baseline the issue names, and stop at `REVIEW_READY`. Historical handoff notes (ORBWEB-001 → WEB-001) are in `STATUS.md` History and `tasks/`.
