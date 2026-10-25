"""Negative tests of the light theme and the removed explanations (CTO, 2026-10-25).

    python scripts/negative_tests_light_theme.py

The site became a light theme (white header and footer, Limestone pages, granite grounds in parts of the content) and
stopped explaining how the work is done: the in-page section bars, the per-layer and per-result warnings and the
explanations of how layers are used and the priority is scored are gone, in English and Turkish. Each case brings one
of them back, or breaks one light-theme property, in memory and checks that scripts/validate_site.py names it. Run it
from a detached worktree of the committed HEAD, one suite at a time (scripts/atlas_negative.py).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from atlas_negative import Suite, regex, swap  # noqa: E402

suite = Suite("Light theme and removed explanations negative tests (2026-10-25)")
CSS, JS, SOURCES = "styles.css", "script.js", "assets/imagery/sources.json"
HOME, TR_HOME, ABOUT, PARTNER, SOURCES_PAGE = "index.html", "tr/index.html", "about/index.html", "partner/index.html", "sources/index.html"

# ---- the removed explanations stay removed -----------------------------------------------------------------
suite.case("an explanation of how a layer is used returns to the dictionary", JS,
           regex(r"(\n  en: \{\n)", r"\1    'act.evidence.copy': 'Each layer is read like this.',\n"),
           "copy that explained how the work is done")
suite.case("a per-layer warning key returns to the English dictionary", JS,
           regex(r"(\n  en: \{\n)", r"\1    'act.priority.note': 'x',\n"),
           "the retired warning key 'act.priority.note' is back in the 'en' dictionary")
suite.case("a per-layer warning is rendered on the homepage again", HOME,
           swap("</main>", '<p data-i18n="act.priority.note">x</p></main>'),
           "the retired warning key 'act.priority.note' is rendered on index.html")
suite.case("the record of the decision is changed to active", SOURCES,
           swap('"status": "retired",\n    "decided": "CTO, 2026-10-25"', '"status": "active",\n    "decided": "CTO, 2026-10-25"'),
           "sources.json must carry public_warnings")
suite.case("a section bar returns on Partner", PARTNER,
           swap("</main>", '<nav class="index-bar" aria-label="x"></nav></main>'),
           "an in-page section bar")

# ---- the homepage keeps three dark acts and three light sections --------------------------------------------
suite.case("the evidence trio goes back to a dark ground", HOME,
           swap('<section id="evidence" class="sec sec-evidence ground-paper"', '<section id="evidence" class="sec sec-evidence"'),
           "#evidence must be a light section")
suite.case("the inspection aid goes back to a dark ground on the Turkish homepage", TR_HOME,
           swap('<section id="inspect" class="sec sec-inspect ground-paper"', '<section id="inspect" class="sec sec-inspect"'),
           "tr/index.html: #inspect must be a light section")
suite.case("the Solutions section goes back to a dark ground", HOME,
           swap('<section id="solutions" class="sec sec-domains ground-paper"', '<section id="solutions" class="sec sec-domains"'),
           "#solutions must be a light section")
suite.case("the priority result is washed out to paper", HOME,
           swap('<section id="priority" class="sec sec-result"', '<section id="priority" class="sec sec-result ground-paper"'),
           "#priority is a photographic or result act and stays dark")

# ---- the two scopes the components read their colours from --------------------------------------------------
suite.case("the light scope loses its white surface", CSS,
           swap("--surface:var(--white);--matte:var(--limestone)", "--surface:var(--limestone);--matte:var(--limestone)"),
           "the light scope (.ground-paper, header, footer) must carry --surface:var(--white)")
suite.case("the light scope loses its paper hairline", CSS,
           swap("--hair:var(--rule-paper);--hair-soft:var(--rule-paper-soft);--surface:var(--white)", "--hair:var(--rule);--hair-soft:var(--rule-soft);--surface:var(--white)"),
           "the light scope (.ground-paper, header, footer) must carry --hair:var(--rule-paper)")
suite.case("the dark scope loses its lifted surface", CSS,
           swap("--surface:var(--ground-lift);--matte:var(--ground)", "--surface:var(--white);--matte:var(--ground)"),
           "the dark scope (.ground-orbit, .ground-lift, the domain bands) must carry --surface:var(--ground-lift)")
suite.case("the dark scope loses its light text", CSS,
           swap(".ground-orbit,.ground-lift,.domain-card,.domain-band{--fg:var(--mist);", ".ground-orbit,.ground-lift,.domain-card,.domain-band{--fg:var(--graphite);"),
           "the dark scope (.ground-orbit, .ground-lift, the domain bands) must carry --fg:var(--mist)")
suite.case("the ink for limits drifts toward the gold fill", CSS, swap("--gold-ink:#735525;", "--gold-ink:#C49A5A;"), "palette token --gold-ink")

if __name__ == "__main__":
    raise SystemExit(suite.run())
