# MER-278 evidence: Partner and Sources in the Atlas design

**Status:** preview, pending CTO acceptance (parent MER-274; foundation MER-275). Nothing here is published.
**Baseline:** `claude/project-thread-csvxkc@a477368` (MER-275 foundation).
**Scope:** `/partner/` and `/sources/` and their Turkish twins, in the `atlas:partner-sources` region of `styles.css`, `script.js` and `scripts/validate_site.py`, plus `scripts/negative_tests_atlas_partner_sources.py`. The 404 is the shared shell (`atlas:shell`) and was not touched here; it renders on the Atlas tokens as the foundation left it.

## What changed

**Partner** (design `Partner.dc.html` with change 2 applied)
* Opens on Orbit: kicker, the two-tone headline (Sans 300 at the page-title size; the second half in Steel, by tone and never by weight), the lede, the address set large as the one text link, and the Kızıldere valley photograph with its three-line bottom-right caption.
* The conversations stay on Orbit: three rows (Pilot, Partnership, Technical), each with its **new audience line** (A7), the existing description and a "Write" link. The mailto links and their three subjects are unchanged in both languages. The old "Direct" section is gone; the address moved into the opening, where the design puts it.
* The photograph is a bare frame (no border), as the plates are.

**Sources** (design `Sources.dc.html` with change 5 applied)
* Opens on Orbit (headline, one-paragraph introduction, the numbered index of the four parts). The body is a paper colophon: Source data (six records in a three-column register), Image credits (rows with a 160 px thumbnail), References, Licences and notices. Every MER-255 record, credit line, image credit, reference DOI and the Crameri MIT notice are unchanged; the Crameri line still carries no year.
* **A8, the font licence:** the Licences part gains a terms entry (`#terms-fonts`) and a licence block (`#licence-fonts`) with IBM's five notices (Copyright 2018 for Plex Sans, 2017 for Plex Mono, the Reserved Font Name line, the licence sentence, the trademark line) in English in both languages, and a link to the full SIL Open Font License text. Each line also stands in `assets/fonts/OFL.txt`, and the validator compares them.
* Two lines of MER-255 copy were reworded to fit the new layout: "The notice below must accompany the colour scales" became "The notice on this page must accompany the colour scales" (the notice now sits beside the terms on desktop), and the Licences lede became "Terms for each source, and the full licence texts."

## Decisions, and what was left out

* **Headline emphasis uses two `data-i18n` spans (`t1`, `t2`)**, not `data-i18n-html`: the shared validator checks do not support inner markup and a change there would collide with the sibling threads. Turkish puts the verb last, so on the Partner page the toned half is the first span in Turkish (`html[lang="tr"] .is-split h1 .t1`); the validator pins that rule.
* **No priority thumbnail on the Sources "Evidence and priority maps" row.** The design marks one (annotation A1). The only recorded file is `priority-600.webp`, 758 KB, for a 100 px thumbnail, and it would widen the MER-151 homepage-only scope to a second page. It needs a small dedicated derivative from Science (MER-242) and the CTO's A1 acceptance. The row stays text-only, as in MER-255.
* **No internal link to `/assets/fonts/OFL.txt`:** the site's link rules allow internal links to page routes only. The notices are printed on the page and the full text is linked from `openfontlicense.org`. Both new external URLs (`https://openfontlicense.org/open-font-license-official-text/`, `https://www.ibm.com/plex/`) could not be opened from the cloud environment (network policy); they are from memory and **need one click each before publication**.
* **Turkish strings are new or reworded and pending the CTO's language review:** the three audience lines ("Olası müşteriler için", "Sektör ortakları için", "Teknik paydaşlar için"; "işbirlikçi" was avoided on purpose, it has a negative meaning in Turkish), the font licence entry (title, note, terms line, link label), the reworded licence terms line and lede, and the split Partner and Sources headlines. The Partner headline keeps the MER-241 sentence word for word: "Sırada nereye bakacağımızı konuşalım."
* The straight apostrophe of "Let's talk" became the typographic one (U+2019), as in the design.

## Verification

* `python scripts/validate_site.py`: PASS, with the region's own checks (grounds, headline spans, mailto routes and subjects, audience lines, the one address, no form, photograph caption, the font licence and its link and its notices against `OFL.txt`, Crameri line without a year and both DOIs, no mention of Esri, the region's CSS) and the type-ready rules switched on for the region (nothing under 10 px, one tracking and two sizes for capitals, palette only).
* `python scripts/negative_tests_atlas_partner_sources.py`: see the report in the thread (run alone, in a detached worktree of the committed HEAD).
* `python hero/scripts/validate_hero.py` after committing: 412 checks, 13 failed, the accepted fresh-clone result.
* Measured in Chromium (Playwright) at 1440 and 390 px, English and Turkish, on all four pages: no horizontal overflow; the headline in OrbGSS Sans 300 at 92 px (44 px on the phone); the smallest rendered text is 10.07 px (the caption token) on Partner and 11 px on Sources; the three-line caption sits inside the photograph frame at both widths (it wraps to four lines on the phone and still fits); fonts loaded: Sans 300, Sans 400, Mono 400.

## Handed back to the foundation, if wanted

* `body.interior .page-section::before` (the hairline) and the numbered `.chapter` head are overridden for the paper sections in this region; the shell could offer a ground-aware hairline and a numeral variant instead.
* The hero heading size is overridden here for the two heroes; when all page threads land, the shell's own `.page-hero h1` can move to `--t-page` and the overrides can go.
