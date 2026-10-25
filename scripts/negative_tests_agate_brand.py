"""Negative tests of the Agate brand adoption (MER-279).

    python scripts/negative_tests_agate_brand.py

Each case breaks exactly one property of the approved identity in memory and checks that
scripts/validate_site.py names it: the recorded brand files and their hashes, what a logo or icon may paint, the
palette record, the head of every page (favicon, touch icon, theme colour), the header and footer logo, the
minimum logo width, the manifest, and the map rule (Graphite neutrals, one gold callout, no teal). Only text
files are mutated. Run it from a detached worktree of the committed HEAD, one suite at a time
(scripts/atlas_negative.py).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from atlas_negative import Suite, regex, swap  # noqa: E402

suite = Suite("Agate brand negative tests (MER-279)")
CSS, RECORD = "styles.css", "assets/brand/brand.json"
LOGO = "assets/brand/orbgss-logo-dark.9085b960.svg"
FAVICON = "assets/brand/orbgss-favicon.31dba293.svg"
MAP = "assets/maps/kizildere-locator-226827d0.svg"
HOME, ABOUT, PARTNER, TR_HOME, TR_ABOUT = "index.html", "about/index.html", "partner/index.html", "tr/index.html", "tr/hakkimizda/index.html"

# ---- the recorded files --------------------------------------------------------------------------
suite.case("the logo drawing is edited after it was recorded", LOGO, swap('<title>OrbGSS</title>', '<title>OrbGSS logo</title>'), "does not match its recorded SHA-256")
suite.case("the logo carries a metadata element again", LOGO, swap("<title>OrbGSS</title>", "<title>OrbGSS</title><metadata>x</metadata>"), "carries metadata")
suite.case("the logo carries a script", LOGO, swap("<title>OrbGSS</title>", "<title>OrbGSS</title><script>1</script>"), "carries metadata, script")
suite.case("the logo paints the old cyan", LOGO, swap("#58AEB2", "#43BFF0"), "not Agate dark-background brand colours")
suite.case("the logo loses its gold focal point", LOGO, lambda t: t.replace("#D8B173", "#B7C0BD"), "must carry all four dark-background brand colours")
suite.case("the logo is the light-ground drawing", LOGO, lambda t: t.replace("#E3E5E4", "#202629").replace("#58AEB2", "#18777A"), "not Agate dark-background brand colours")
suite.case("the favicon tile leaves Graphite", FAVICON, swap('fill="#202629"', 'fill="#030B12"'), "not Agate dark-background brand colours")
suite.case("a logo file loses its hash name", RECORD, swap('"file": "orbgss-logo-dark.9085b960.svg"', '"file": "orbgss-logo-dark.svg"'), "does not exist")
suite.case("a recorded role is renamed", RECORD, swap('"icon-192": {', '"icon-193": {'), "must record exactly")
suite.case("the record names another identity", RECORD, swap('"identity": "Agate"', '"identity": "Atlas"'), "must record the Agate identity")
suite.case("the recorded palette drifts", RECORD, swap('"agate_teal": "#58AEB2"', '"agate_teal": "#5BAEB2"'), "must record the approved palette exactly")
suite.case("a brand colour drifts in the stylesheet", CSS, swap("--gold-light:#D8B173;", "--gold-light:#D8B174;"), "palette token --gold-light")
suite.case("Mineral Gray drifts in the stylesheet", CSS, swap("--mineral:#69716F;", "--mineral:#6A7270;"), "palette token --mineral")

# ---- the head of every page ----------------------------------------------------------------------
suite.case("a page loses the touch icon", ABOUT, regex(r'  <link rel="apple-touch-icon"[^\n]*\n', ""), "the head must carry")
suite.case("a page loses the root favicon link", PARTNER, regex(r'  <link rel="icon" href="/favicon\.ico"[^\n]*\n', ""), "the head must carry")
suite.case("a page points its favicon at the old mark", ABOUT, regex(r'<link rel="icon" href="/assets/brand/orbgss-favicon[^"]*"', '<link rel="icon" href="/assets/mark.svg"'), "the head must carry")
suite.case("a page keeps the old navy theme colour", PARTNER, swap('<meta name="theme-color" content="#171A1B" />', '<meta name="theme-color" content="#030B12" />'), "theme-color must be the Graphite ground")
suite.case("the Turkish homepage keeps the old navy theme colour", TR_HOME, swap('<meta name="theme-color" content="#171A1B" />', '<meta name="theme-color" content="#030B12" />'), "tr/index.html: theme-color must be")
suite.case("favicon.ico is no longer deployed", ".vercelignore", swap("!favicon.ico\n", ""), "favicon.ico")

# ---- the logo in the header and the footer ----------------------------------------------------------
suite.case("the text wordmark returns to the homepage header", HOME,
           regex(r'<img class="brand-logo"[^>]*/>', '<span class="brand-wordmark">Orb<span>GSS</span></span>'), "the header brand link must hold exactly")
suite.case("the header logo gets alt text", ABOUT, swap('<img class="brand-logo" src="/assets/brand/orbgss-logo-dark.9085b960.svg" alt=""', '<img class="brand-logo" src="/assets/brand/orbgss-logo-dark.9085b960.svg" alt="OrbGSS"'), "the header brand link must hold exactly")
suite.case("the footer shows the old logo", PARTNER, swap('<img src="/assets/brand/orbgss-logo-dark.9085b960.svg" alt="OrbGSS" width="634" height="108" />', '<img src="/assets/logo.svg" alt="OrbGSS" width="420" height="120" />'), "the footer brand must hold exactly")
suite.case("the Turkish About footer drops the logo alt", TR_ABOUT, swap('alt="OrbGSS" width="634" height="108" />', 'alt="" width="634" height="108" />'), "tr/hakkimizda/index.html: the footer brand must hold exactly")
suite.case("the header logo shrinks under the brand minimum", CSS, swap(".brand-logo{height:24px}", ".brand-logo{height:18px}"), "under the brand's 120px minimum width")
suite.case("the illustrative map is placed on a page", ABOUT, swap("</main>", '<img src="/assets/brand/illustrative-map.jpg" alt="" /></main>'), "places the illustrative map")

# ---- the manifest --------------------------------------------------------------------------------
suite.case("the manifest keeps the old navy theme colour", "site.webmanifest", swap('"theme_color": "#171A1B"', '"theme_color": "#030B12"'), "site.webmanifest theme_color must be")
suite.case("the manifest loses the 512 px icon", "site.webmanifest", regex(r'    \{\n      "src": "/assets/brand/orbgss-icon-512[^}]*\},\n', ""), "site.webmanifest icons must be exactly")

# ---- colour rules in the stylesheet ------------------------------------------------------------------
suite.case("the hero shade goes back to navy", CSS, swap("linear-gradient(90deg,rgba(23,26,27,.97) 0%", "linear-gradient(90deg,rgba(3,11,18,.97) 0%"), "is not in the Agate palette")
suite.case("a button is filled with gold", CSS, swap(".button:hover{background:var(--mist);", ".button:hover{background:var(--gold);"), "fills with gold")
suite.case("a cyan accent returns in an inline style", PARTNER, swap('<a class="skip-link"', '<a style="color:#73E7FF" class="skip-link"'), "colour #73E7FF is not in the Agate palette")

# ---- the map rule: Graphite neutrals, one gold callout, no teal ---------------------------------------------
suite.case("the map callout turns teal", MAP, lambda t: t.replace("#D8B173", "#58AEB2"), "must carry the gold area-of-interest callout")
suite.case("the map goes back to the old navy sea", MAP, swap('fill="#121415"/>', 'fill="#030b12"/>'), "a map uses Graphite neutrals and the gold callout only")

if __name__ == "__main__":
    raise SystemExit(suite.run())
