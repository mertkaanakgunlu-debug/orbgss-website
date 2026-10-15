# Handoff

Reconciled by MER-213 on 2026-09-29, MER-218 on 2026-10-03 and MER-239 on 2026-10-15. `STATUS.md` is the current-state record and `CLAUDE.md` the rules; this file only orients a new session.

## Where things stand

- Git `main` is `2517369e0f0c4239d72603a3188227554053a6ea` and production serves it (published 2026-10-15, MER-219). It is the launched WEB-005C code `79cc2cb` plus MER-216 (hero delivery ladder and runtime hardening) and MER-237 (only the public site is deployed, via `.vercelignore`).
- Vercel deploys `main` to production automatically: a push to `main` is a production deployment. Publishing and rollback follow `tasks/MER-219_PREFLIGHT.md`. Agents cannot read the Vercel team (the connector's OAuth grant has no team access).
- Milestone 6 is planned and approved: `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md` (Home / Solutions / About / Partner with us, show-first content rules, static `/tr/`). MER-240 builds the English pages, MER-241 the Turkish ones; MER-242 asks Science for two Geothermal-page figures.
- The live site is static HTML, CSS and vanilla JS, six routes, bilingual EN/TR in `script.js`, provenance and checksums in `assets/imagery/sources.json`, enforced by `scripts/validate_site.py`.
- Hero: rendered sequence plus page-composited, lossless drape states. Blender 4.5 LTS is local production tooling, not a runtime dependency, and its large source textures are git-ignored.

## What is deliberately not done

- `CONTACT_RELEASE_GATE` (`contact@orbgss.com` ownership and deliverability) is carried open, now as MER-238 D4, a ship gate for MER-240.
- MER-238 D3 (privacy / KVKK, a legal call) and D5 (coastal Marine scene) are open.
- The repository holds no record of the WEB-006 DNS execution itself; its observable result is recorded in `tasks/MER-219_PREFLIGHT.md` §2.1.
- The GitHub repository is public; whether it should be private is a CTO decision (`STATUS.md` open decision 5).
- WEB-007 / MER-143, WEB-008 / MER-144, MER-145 and MER-146 are canceled and consolidated into MER-216, which is published.

## Next session

Wait for an explicit `MER-###'e başla`. Follow the task execution rule in `CLAUDE.md`, branch from the exact baseline the issue names, and stop at `REVIEW_READY`. Historical handoff notes (ORBWEB-001 → WEB-001) are in `STATUS.md` History and `tasks/`.
