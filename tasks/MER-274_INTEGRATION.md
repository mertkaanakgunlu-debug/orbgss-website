# MER-274 integration: the Atlas redesign on one branch

**Status:** preview, pending an independent review and the CTO's acceptance. Nothing here is merged to `main`, published or deployed.
**Baseline:** `claude/project-thread-csvxkc@a477368` (MER-275 foundation, itself on MER-255 `fe8cc470`).
**Merged, in this order, with no textual conflicts** (each group owned its own marked regions):

| Group | Branch | HEAD merged |
|---|---|---|
| MER-276 Geothermal | `claude/project-thread-xix6pw` | `a3cc5da4` |
| MER-277 Solutions + About | `claude/project-thread-2pruwu` | `b6454e48` |
| MER-278 Partner + Sources | `claude/project-thread-x7yk8d` | `cd51c132` |

Shared files that more than one group touched (`assets/imagery/sources.json`, `script.js`, `styles.css`, `scripts/validate_site.py`, `scripts/negative_tests_mer240.py`, `scripts/negative_tests_mer255.py`) merged without a conflict marker; the validator and every negative suite below confirm nothing was lost semantically.

## The one thing this step changed

`scripts/measure_interior_renders.py --write` was re-run on the integrated tree. The Geothermal stage crop is now drawn at **1600 CSS px** at most (`kizildere-stage`, 1600 px candidate, upscale 1.00x), so the earlier worry (1621 px on the foundation, 1602 recorded) is resolved by the Geothermal group's 1600 px cap, not by a CSS change here. The record in `sources.json` followed the measurement: stage 1602 to 1600, and the AOI and valley crops moved by a few pixels (534 and 500 CSS px) because the Solutions and Geothermal layouts changed. Every value is below its own ceiling and no derivative is upscaled by more than 1.00x. `scripts/measure_geothermal_renders.py` agrees with the Geothermal group's records: terrain, THM-01 and ALT-01 at most 534 CSS px, priority 600 CSS px, worst upscale 1.000x.

## Verification, at the integrated tree

* `scripts/validate_site.py`: PASS, 6 routes, 6 of 6 static Turkish pages, generator tree byte-identical.
* `hero/scripts/validate_hero.py`: 412 checks, 13 failed. All 13 are the git-ignored local source textures under `hero/assets/source/` (the accepted fresh-clone result); nothing else fails.
* Negative suites, one at a time, in a detached worktree of the committed tree (every suite restored the tree to its baseline and exited 0): Atlas foundation 39/39, Geothermal 43/43, Solutions + About 37/37, Partner + Sources 34/34, MER-240 46/46, MER-255 49/49, MER-241 51/51, MER-237 29/29, WEB-005B 55/55, WEB-005C 18/18, WEB-005 72/72, MER-216 19/19 deliberate regressions caught. They were run once on the merge result and again after the measurement record was updated (the record lives in `sources.json`, which several suites mutate).
* Browser sweep (headless Chromium, Vercel-style clean URLs): twelve routes (six English, six Turkish) at 1440 x 900 @1x and 390 x 844 @2x, plus the two Geothermal routes at 1680 x 900 @1x. No horizontal overflow, no console or network error, OrbGSS Sans 300 / 400 and OrbGSS Mono loaded, h1 in OrbGSS Sans 300 on every page, no visible text under 10 px, `404.html` on the Atlas tokens at both widths. The homepage's lazily loaded hero posters carry `data-src` until scrolled into use; that is existing behaviour, not a regression (the homepage markup is identical to the foundation's).

## Open items that stay with the CTO or with Science (unchanged by integration)

1. **A1:** the four MER-151 layers are shown full size on Geothermal (MER-276) and as thumbnails of at most 160 CSS px on Solutions (one) and About (five) (MER-277). `CLAUDE.md` and `docs/WEB_ATLAS_DESIGN_AUTHORITY.md` still say MER-151 derivatives are homepage-only; change them to "homepage, Geothermal and the two index thumbnails" only after the CTO accepts A1. The Sources page shows none (a 100 px thumbnail would need a small derivative from Science, MER-242).
2. **A7:** the new or rewritten Turkish strings need the CTO's language read: 38 Geothermal strings (list in `docs/WEB_ATLAS_GEOTHERMAL_AUTHORITY.md` section 5), the `solutionsPage.*` and `aboutPage.*` keys, and on Partner and Sources the three audience lines, the font-licence entry, the licence-terms row, the licence section intro and the two split headlines.
3. **A2, A5, A6** (Geothermal) are marked preview-pending.
4. Geothermal's iron layer (Plate 06) and "priority over relief" remain pending slots until Science delivers (MER-242); structure and geology stays a data gap.
5. Two external links could not be opened from the cloud environment and need one human click before publication: `https://openfontlicense.org/open-font-license-official-text/` and `https://www.ibm.com/plex/`.
6. Foundation clean-up that the three page groups each worked around: the shell's `.page-section-head p` over `.kicker`, the numbered `.chapter` rule and `body.interior .page-section::before` on paper bands, and the per-page hero `h1` size are overridden separately in the Solutions/About and Partner/Sources regions. A later foundation pass can fold them in; none changes what the page shows.
