# Handoff

Reconciled by MER-213 on 2026-09-29. `STATUS.md` is the current-state record and `CLAUDE.md` the rules; this file only orients a new session.

## Where things stand

- The accepted, launched baseline is `feat/web-005c-public-domain-taxonomy-parity@79cc2cb82a4542461cbbfc1d0c349cf02b861084` (WEB-005 → 005A hero → 005B homepage R15 → 005C Geothermal / Mining / Marine taxonomy). Per the MER-213 record, Vercel production serves that SHA.
- `main@00af0f232a8d7d77f5ca61d758461ff7316ba151` is an ancestor of the baseline (baseline ahead 25 / behind 0). Publishing it to `main` is a separate CTO-approved, non-force fast-forward.
- The site is static HTML, CSS and vanilla JS, six routes, bilingual EN/TR in `script.js`, provenance and checksums in `assets/imagery/sources.json`, enforced by `scripts/validate_site.py`.
- Hero: rendered sequence plus page-composited, lossless drape states. Blender 4.5 LTS is local production tooling, not a runtime dependency, and its large source textures are git-ignored.

## What is deliberately not done

- `main` has not been updated; nothing here deploys, changes DNS, credentials or Vercel configuration.
- `CONTACT_RELEASE_GATE` (`contact@orbgss.com` ownership and deliverability) is carried open.
- The repository holds no record of the WEB-006 deploy/DNS execution; the cutover contract is on `docs/web-005-polish-authority@e64d9fd`.
- The Claude Project instructions describe a different navigation (Home / Solutions / About / Partner with us) than the repository and the live site; unresolved, CTO decision.
- WEB-007 / MER-143 and WEB-008 / MER-144 are blocked until the MER-213 review is accepted.

## Next session

Wait for an explicit `MER-###'e başla`. Follow the task execution rule in `CLAUDE.md`, branch from the exact baseline the issue names, and stop at `REVIEW_READY`. Historical handoff notes (ORBWEB-001 → WEB-001) are in `STATUS.md` History and `tasks/`.
