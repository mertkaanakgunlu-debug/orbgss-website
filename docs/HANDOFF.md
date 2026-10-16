# Handoff

Reconciled by MER-213 on 2026-09-29, MER-218 on 2026-10-03, MER-239 on 2026-10-15 and MER-240 on 2026-10-16. `STATUS.md` is the current-state record and `CLAUDE.md` the rules; this file only orients a new session.

## Coordination (from 2026-10-16)

- Website coordination moves to the CTO's Claude Project. It works from the same canonical sources: this repository, the Linear project "OrbGSS — Website" (milestone 6) and the authorities `CLAUDE.md` names. Its starting note is the Linear project document "Claude Projects handoff — 2026-10-16".
- Claude Code sessions execute one Linear issue each (`MER-###'e başla`) on a bounded branch, report on that issue, and stop at `REVIEW_READY`. They are not coordinators.
- In-review work lives on task branches. The default branch shows only what is published.

## Where things stand

- Git `main` is `464a73543a440f7d51a1600599998e97b53e982f` and production serves it (published 2026-10-15, MER-219). It is the launched WEB-005C code `79cc2cb` plus MER-216 (hero delivery ladder and runtime hardening), MER-237 (only the public site is deployed, via `.vercelignore`) and the MER-239 documentation.
- MER-240 (the English Milestone 6 pages) is `REVIEW_READY` on `mertkaanakgunlu/mer-240-web-sitesi-yeni-sayfalarin-uygulanmasi-en`, not published. Its head SHA and verification are in the latest comment on the Linear issue; evidence is in `tasks/MER-240_EVIDENCE.md`.
- Vercel deploys `main` to production automatically: a push to `main` is a production deployment. Publishing and rollback follow `tasks/MER-219_PREFLIGHT.md`. Agents cannot read the Vercel team (the connector's OAuth grant has no team access), and branch Previews are SSO-protected.
- Milestone 6 authority: `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md`. MER-241 builds the static `/tr/` pages after MER-240 is published. MER-242 (Science) supplies the Geothermal page's two figures and the layer-table thumbnails.
- Hero: rendered sequence plus page-composited, lossless drape states. Blender 4.5 LTS is local production tooling, not a runtime dependency, and its large source textures are git-ignored.

## What is deliberately not done

- `CONTACT_RELEASE_GATE` (`contact@orbgss.com` ownership and deliverability) is open as MER-238 D4, the ship gate for MER-240.
- MER-238 D3 (privacy / KVKK, a legal call) and D5 (coastal Marine scene) are open.
- MER-237, MER-238, MER-239 and MER-219 are accepted (and published where they ship code) but still "In Review" in Linear; closing them is the CTO's action.
- The repository holds no record of the WEB-006 DNS execution itself; its observable result is recorded in `tasks/MER-219_PREFLIGHT.md` §2.1.
- The GitHub repository is public; whether it should be private is a CTO decision (`STATUS.md` open decision 5).

## Next session

Wait for an explicit `MER-###'e başla`. Follow the task execution rule in `CLAUDE.md`, branch from the exact baseline the issue names, and stop at `REVIEW_READY`. A publication needs its own explicit CTO authorization each time. Historical handoff notes (ORBWEB-001 → WEB-001) are in `STATUS.md` History and `tasks/`.
