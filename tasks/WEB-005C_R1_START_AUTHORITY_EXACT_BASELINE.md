# WEB-005C R1 — Start Authority / Exact Baseline

**Linear:** MER-149  
**State:** CTO_START_GRANTED / READY_FOR_CLAUDE_DESKTOP_START  
**Repository:** `mertkaanakgunlu-debug/orbgss-website`  
**Exact accepted baseline:** `feat/web-005b-homepage-visual-fidelity@0af5b1ad0a5645f8ff3f39f818625944a096635d`

## Outcome

Converge the public website domain taxonomy on the accepted Product naming:

- Geothermal
- Mining
- Marine

This is a public IA/copy consistency task only.

## Required scope

Review and minimally update public:
- primary navigation where domain names appear;
- Solutions landing labels/headings;
- public anchors/routes directly coupled to those names;
- EN/TR dictionaries and accessibility labels;
- validators/tests coupled to those route labels.

Preserve route compatibility where practical.

If old anchors such as `#mineral` or `#environment` are already linked internally or externally, prefer compatibility aliases/redirect behavior rather than silently breaking them.

## Product semantics

Visible top-level public taxonomy:
- Geothermal
- Mining
- Marine

Mining and Marine may remain clearly marked as in development where appropriate.

Do not reinterpret the underlying product capabilities merely to make the names match.

## Hard boundaries

Do not:
- redesign the homepage;
- alter accepted WEB-005B visual layout, hero, analytical imagery or motion;
- redesign solution pages beyond the minimum taxonomy consistency work;
- invent capabilities, customers, metrics or claims;
- alter scientific semantics;
- merge, deploy or change DNS;
- start WEB-006 deployment work.

## Implementation model

CTO will run this task manually in Claude Code Desktop.

Claude may make routine implementation choices for:
- route/anchor compatibility;
- localization key organization;
- accessibility labels;
- focused validators/tests;
- small conformant cleanup directly required by taxonomy parity.

## Acceptance

- homepage and Solutions surfaces use Geothermal / Mining / Marine consistently;
- EN/TR remain semantically aligned;
- no broken public nav or deep-link regressions;
- legacy anchors remain compatible where practical;
- no unrelated visual changes;
- full relevant site/hero validators remain GREEN.

Return:
`REVIEW_READY / WAITING_PRODUCT_REVIEW`

No deployment.
