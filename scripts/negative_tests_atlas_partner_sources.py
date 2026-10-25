"""Negative tests of the Atlas redesign: Partner and Sources (MER-278).

    python scripts/negative_tests_atlas_partner_sources.py

Each case breaks exactly one thing the Partner and Sources region of scripts/validate_site.py promises, in
memory, and checks that the validator names it: the grounds (Partner opens and stays on Orbit; Sources opens on
Orbit with a paper colophon), the two-tone headlines, the mailto routes, their audience lines and subjects, the
one address and no form, the photograph's caption, the font licence next to the unchanged Crameri MIT notice and
DOIs (A8), no Esri mention, and the region's own CSS (type scale, palette, the bare photograph frame). Run it
from a detached worktree of the committed HEAD, one suite at a time (scripts/atlas_negative.py).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from atlas_negative import Suite, regex, swap  # noqa: E402,F401

suite = Suite("Atlas negative tests - Partner and Sources (MER-278)")
PARTNER, PARTNER_TR = "partner/index.html", "tr/is-birligi/index.html"
SOURCES, SOURCES_TR = "sources/index.html", "tr/kaynaklar/index.html"
CSS, JS = "styles.css", "script.js"

# ---- Partner: grounds, headline, routes, address, photograph --------------------------------------------
suite.case("the Partner opening leaves paper", PARTNER, swap("page-hero is-split ground-paper", "page-hero is-split"),
           "the Partner opening must be a page-hero is-split on paper")
suite.case("the conversations leave Orbit", PARTNER, swap("route-section ground-orbit", "route-section"),
           "(#routes) must sit on Orbit")
suite.case("a Lift band appears on Partner", PARTNER, swap("route-section ground-orbit", "route-section ground-orbit ground-lift"),
           "no Lift band")
suite.case("the headline loses its tone span", PARTNER, swap('<span class="t2" data-i18n="partnerPage.title.b">', '<span data-i18n="partnerPage.title.b">'),
           "the Partner headline must be the two tone spans")
suite.case("a Pilot subject changes", PARTNER, swap("?subject=OrbGSS%20Pilot%20Inquiry", "?subject=OrbGSS%20Pilot"),
           "the three conversation routes must be the mailto links with their pinned subjects")
suite.case("a Turkish subject changes", PARTNER_TR, swap("OrbGSS%20Pilot%20Talebi", "OrbGSS%20Pilot%20Talep"),
           "tr/is-birligi/index.html: the three conversation routes must be the mailto links")
suite.case("a route loses its audience line", PARTNER,
           swap('<span class="route-for" data-i18n="partnerPage.pilot.for">For prospective customers</span>\n              ', ""),
           "the pilot route has no audience line")
suite.case("an audience line is emptied in the dictionary", JS, swap("'partnerPage.technical.for': 'For technical collaborators'", "'partnerPage.technical.for': ''"),
           "no audience line partnerPage.technical.for")
suite.case("the address changes", PARTNER, swap('<a href="mailto:contact@orbgss.com"><span>contact@orbgss.com</span>', '<a href="mailto:hello@orbgss.com"><span>contact@orbgss.com</span>'),
           "the opening must carry the one address link")
suite.case("a form appears", PARTNER, swap("</main>", "<form></form></main>"), "<form> on the Partner page")
suite.case("the photograph loses its kind line", PARTNER,
           swap('<span class="scene-kind" data-i18n="scene.kind.naturalColor">Natural-color composite</span>', ""),
           "the photograph keeps its three-line bottom-right caption")
suite.case("the photograph gains a border", CSS,
           swap(".split-figure{position:relative;width:100%;max-width:500px;margin:0;", ".split-figure{border:1px solid var(--rule);position:relative;width:100%;max-width:500px;margin:0;"),
           ".split-figure carries a border")
suite.case("the Turkish flip rule is removed", CSS, swap('html[lang="tr"] .is-split h1 .t1{color:var(--fg-2)}', ""),
           "must tone its first half")
suite.case("the second half stops being Steel", CSS, swap(".is-split h1 .t2,.is-register h1 .t2{color:var(--fg-2)}", ".is-split h1 .t2,.is-register h1 .t2{color:var(--fg)}"),
           "second half of the two-tone headline must be Steel")
suite.case("Esri is mentioned on Partner", PARTNER, swap('<p class="kicker" data-i18n="nav.partner">Partner with us</p>', '<p class="kicker" data-i18n="nav.partner">Partner with us</p><p>Esri partner</p>'),
           "mentions Esri")
suite.case("Esri is mentioned in a Sources string", JS, swap("'sourcesPage.scm.by': 'Fabio Crameri',", "'sourcesPage.scm.by': 'Fabio Crameri, Esri partner',"),
           "mentions Esri")

# ---- Sources: grounds, headline, the font licence (A8), the Crameri notice -----------------------------
suite.case("the Sources opening leaves Orbit", SOURCES, swap("page-hero is-register ground-orbit", "page-hero is-register"),
           "the Sources opening must be a page-hero is-register on Orbit")
suite.case("a Sources part leaves the paper", SOURCES, swap('chapter ground-paper" id="images"', 'chapter ground-orbit" id="images"'),
           "the paper colophon")
suite.case("the Turkish Sources body leaves the paper", SOURCES_TR, swap('chapter ground-paper" id="data"', 'chapter" id="data"'),
           "tr/kaynaklar/index.html: the four parts of Sources")
suite.case("the Sources headline loses its tone span", SOURCES, swap('<span class="t2" data-i18n="sourcesPage.title.b">', '<span data-i18n="sourcesPage.title.b">'),
           "the Sources headline must be the two tone spans")
suite.case("the font licence block is gone", SOURCES, swap('id="licence-fonts"', 'id="licence-font"'),
           "#licence-fonts must hold IBM's five notices")
suite.case("a font notice is dropped from the page", SOURCES,
           swap('<p data-i18n="sourcesPage.fonts.trademark">IBM Plex(R) is a trademark of IBM Corp, registered in many jurisdictions worldwide.</p>\n', ""),
           "#licence-fonts must hold IBM's five notices")
suite.case("a font notice changes in the dictionary", JS, swap("'IBM Plex Sans: Copyright 2018 IBM Corp. All rights reserved.'", "'IBM Plex Sans: Copyright 2019 IBM Corp. All rights reserved.'"),
           "changed IBM's notice")
suite.case("the full licence text link loses its safe target", SOURCES,
           swap('href="https://openfontlicense.org/open-font-license-official-text/" target="_blank" rel="noopener"', 'href="https://openfontlicense.org/open-font-license-official-text/"'),
           "must link the full SIL Open Font License text")
suite.case("the typefaces lose their terms entry", SOURCES, swap('<li id="terms-fonts">', '<li id="terms-font">'),
           "the typefaces need a terms entry")
suite.case("the shipped licence file loses IBM's Mono notice", "assets/fonts/OFL.txt", swap("Copyright 2017 IBM Corp. All rights reserved.", "Copyright IBM Corp."),
           "no longer carries the notice shown on /sources/")
suite.case("a Crameri copyright year is invented", JS, swap("'sourcesPage.mit.copyright': 'Copyright (c) Fabio Crameri',", "'sourcesPage.mit.copyright': 'Copyright (c) 2023 Fabio Crameri',"),
           "without a year")
suite.case("the Crameri MIT block is gone", SOURCES, swap('id="licence-scm"', 'id="licence-colour"'),
           "(#licence-scm) is gone")
suite.case("a Crameri DOI is dropped", SOURCES, swap('href="https://doi.org/10.5281/zenodo.8035877"', 'href="https://doi.org/10.5281/zenodo.0"'),
           "the Crameri DOI https://doi.org/10.5281/zenodo.8035877 is gone")

# ---- the region's own CSS ---------------------------------------------------------------------------------
suite.case("text under 10px in the region", CSS,
           swap(".route-for{flex:1 1 200px;font-family:var(--mono);font-variant-ligatures:none;font-size:var(--t-label);",
                ".route-for{flex:1 1 200px;font-family:var(--mono);font-variant-ligatures:none;font-size:9px;"),
           "sets 9px text; nothing is set under 10px")
suite.case("capitals get a second tracking in the region", CSS,
           swap("line-height:1.6;letter-spacing:var(--track);text-transform:uppercase;color:var(--link)}\n.route-copy", "line-height:1.6;letter-spacing:.24em;text-transform:uppercase;color:var(--link)}\n.route-copy"),
           ".route-for sets capitals with tracking .24em")
suite.case("capitals get a third size in the region", CSS,
           swap(".route-go{flex:none;font-family:var(--mono);font-variant-ligatures:none;font-size:var(--t-label);", ".route-go{flex:none;font-family:var(--mono);font-variant-ligatures:none;font-size:13px;"),
           ".route-go sets capitals at 13px")
suite.case("a stray colour in the region", CSS, swap(".route-list a:hover{background:var(--wash)}", ".route-list a:hover{background:#112233}"),
           "is not in the Agate palette")
suite.case("a medium weight in the region", CSS, swap(".route-title{flex:1 1 240px;font-size:var(--t-section);font-weight:300;", ".route-title{flex:1 1 240px;font-size:var(--t-section);font-weight:500;"),
           "font-weight 500")

if __name__ == "__main__":
    raise SystemExit(suite.run())
