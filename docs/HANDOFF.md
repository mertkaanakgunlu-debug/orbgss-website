# Handoff

Reconciled by MER-213 on 2026-09-29, MER-218 on 2026-10-03, MER-239 on 2026-10-15, MER-240 on 2026-10-16 and after the MER-240 publication on 2026-10-17. `STATUS.md` is the current-state record and `CLAUDE.md` the rules; this file only orients a new session.

## Coordination (from 2026-10-16)

- Website coordination moves to the CTO's Claude Project. It works from the same canonical sources: this repository, the Linear project "OrbGSS — Website" (milestone 6) and the authorities `CLAUDE.md` names. Its starting note is the Linear project document "Claude Projects handoff — 2026-10-16".
- Claude Code sessions execute one Linear issue each (`MER-###'e başla`) on a bounded branch, report on that issue, and stop at `REVIEW_READY`. They are not coordinators.
- In-review work lives on task branches. The default branch shows only what is published.

## Where things stand

- Production serves the MER-240 English Milestone 6 pages, `main@a2045344f4cc70fe189160ffd7254fe61020cad9`, published 2026-10-16 (Done in Linear). `main` also carries a docs-only records commit on top of it. Publication record: `tasks/MER-240_EVIDENCE.md` §8.
- Vercel deploys `main` to production automatically: a push to `main` is a production deployment. Publishing and rollback follow `tasks/MER-219_PREFLIGHT.md`. Agents can read a deployment by hostname (`get_deployment`) but not list the team, and branch Previews are protected.
- Milestone 6 authority: `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md`. MER-241 (static `/tr/` pages) is next. MER-242 (Science) supplies the Geothermal page's two figures and the layer-table thumbnails.
- Hero: rendered sequence plus page-composited, lossless drape states. Blender 4.5 LTS is local production tooling, not a runtime dependency, and its large source textures are git-ignored.

## What is deliberately not done

- MER-238 D3 (privacy / KVKK, a legal call) and D5 (coastal Marine scene) are open. D4 is closed: `contact@orbgss.com` receives external mail, though the CTO's test landed in spam.
- The repository holds no record of the WEB-006 DNS execution itself; its observable result is recorded in `tasks/MER-219_PREFLIGHT.md` §2.1.
- The GitHub repository is public; whether it should be private is a CTO decision (`STATUS.md` open decision 5).

## Next session

Wait for an explicit `MER-###'e başla`. Follow the task execution rule in `CLAUDE.md`, branch from the exact baseline the issue names, and stop at `REVIEW_READY`. A publication needs its own explicit CTO authorization each time. Historical handoff notes (ORBWEB-001 → WEB-001) are in `STATUS.md` History and `tasks/`.
