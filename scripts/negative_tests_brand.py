"""Negative tests of the Heat Trace brand adoption (CTO decision of 2026-10-25; the Agate suite of MER-279 became this one).

    python scripts/negative_tests_brand.py

Each case breaks exactly one property of the approved identity in memory and checks that
scripts/validate_site.py names it: the recorded brand files and their hashes, what a logo or icon may paint, the
palette record, the head of every page (favicon, touch icon, theme colour), the header and footer logo, the
minimum logo width, the manifest, the map rule (Night-family neutrals, one dashed Magma callout, no Amber or Glow) and the
caption crossover derived from the caption colours. Only text
files are mutated. Run it from a detached worktree of the committed HEAD, one suite at a time
(scripts/atlas_negative.py).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from atlas_negative import Suite, regex, swap  # noqa: E402

suite = Suite("Heat Trace brand negative tests")
CSS, RECORD = "styles.css", "assets/brand/brand.json"
LOGO = "assets/brand/orbgss-logo-light.27e93f98.svg"
FAVICON = "assets/brand/orbgss-favicon.73a16b96.svg"
MAP = "assets/maps/kizildere-locator-006fcf1f.svg"
HOME, ABOUT, PARTNER, TR_HOME, TR_ABOUT = "index.html", "about/index.html", "partner/index.html", "tr/index.html", "tr/hakkimizda/index.html"

# ---- the recorded files --------------------------------------------------------------------------
suite.case("the logo drawing is edited after it was recorded", LOGO, swap('<title>OrbGSS</title>', '<title>OrbGSS logo</title>'), "does not match its recorded SHA-256")
suite.case("the logo carries a metadata element again", LOGO, swap("<title>OrbGSS</title>", "<title>OrbGSS</title><metadata>x</metadata>"), "carries metadata")
suite.case("the logo carries a script", LOGO, swap("<title>OrbGSS</title>", "<title>OrbGSS</title><script>1</script>"), "carries metadata, script")
suite.case("the logo paints the old cyan", LOGO, lambda t: t.replace("#CD1B74", "#43BFF0"), "not Heat Trace brand colours for that ground")
suite.case("the logo loses its amber orb", LOGO, lambda t: t.replace("#FFA323", "#371641"), "must carry the light-background brand colours")
suite.case("the logo is the dark-ground drawing", LOGO, lambda t: t.replace("#371641", "#F5EFF7").replace("#CD1B74", "#E43386"), "not Heat Trace brand colours for that ground")
suite.case("the logo's viewBox changes", LOGO, swap('viewBox="0 0 619.41 144"', 'viewBox="0 0 634 108"'), "the logo's viewBox is not the approved")
suite.case("the favicon tile leaves Night", FAVICON, swap('fill="#160A19"', 'fill="#030B12"'), "not Heat Trace brand colours for that ground")
suite.case("a logo file loses its hash name", RECORD, swap('"file": "orbgss-logo-light.27e93f98.svg"', '"file": "orbgss-logo-light.svg"'), "does not exist")
suite.case("a recorded role is renamed", RECORD, swap('"icon-192": {', '"icon-193": {'), "must record exactly")
suite.case("the record goes back to the dark-ground logo role", RECORD, swap('"logo-light": {', '"logo-dark": {'), "must record exactly")
suite.case("the record names another identity", RECORD, swap('"identity": "Heat Trace"', '"identity": "Agate"'), "must record the Heat Trace identity")
suite.case("the recorded palette drifts", RECORD, swap('"magma": "#E43386"', '"magma": "#E43387"'), "must record the approved palette exactly")
suite.case("a brand colour drifts in the stylesheet", CSS, swap("--amber-light:#FFAA2E;", "--amber-light:#FFAA2F;"), "palette token --amber-light")
suite.case("Magma drifts in the stylesheet", CSS, swap("--magma:#CD1B74;", "--magma:#CE1B74;"), "palette token --magma")
suite.case("an old Agate token comes back", CSS, swap("--ink:#2D1B30;", "--ink:#2D1B30;\n  --graphite:#202629;"), "retired colour token --graphite")

# ---- the head of every page ----------------------------------------------------------------------
suite.case("a page loses the touch icon", ABOUT, regex(r'  <link rel="apple-touch-icon"[^\n]*\n', ""), "the head must carry")
suite.case("a page loses the root favicon link", PARTNER, regex(r'  <link rel="icon" href="/favicon\.ico"[^\n]*\n', ""), "the head must carry")
suite.case("a page points its favicon at the old mark", ABOUT, regex(r'<link rel="icon" href="/assets/brand/orbgss-favicon[^"]*"', '<link rel="icon" href="/assets/mark.svg"'), "the head must carry")
suite.case("a page keeps the old navy theme colour", PARTNER, swap('<meta name="theme-color" content="#FFFFFF" />', '<meta name="theme-color" content="#030B12" />'), "theme-color must be the white header")
suite.case("the Turkish homepage goes back to a dark theme colour", TR_HOME, swap('<meta name="theme-color" content="#FFFFFF" />', '<meta name="theme-color" content="#160A19" />'), "tr/index.html: theme-color must be")
suite.case("favicon.ico is no longer deployed", ".vercelignore", swap("!favicon.ico\n", ""), "favicon.ico")

# ---- the logo in the header and the footer ----------------------------------------------------------
suite.case("the text wordmark returns to the homepage header", HOME,
           regex(r'<img class="brand-logo"[^>]*/>', '<span class="brand-wordmark">Orb<span>GSS</span></span>'), "the header brand link must hold exactly")
suite.case("the header logo gets alt text", ABOUT, swap('<img class="brand-logo" src="/assets/brand/orbgss-logo-light.27e93f98.svg" alt=""', '<img class="brand-logo" src="/assets/brand/orbgss-logo-light.27e93f98.svg" alt="OrbGSS"'), "the header brand link must hold exactly")
suite.case("the footer shows the old logo", PARTNER, swap('<img src="/assets/brand/orbgss-logo-light.27e93f98.svg" alt="OrbGSS" width="619" height="144" />', '<img src="/assets/logo.svg" alt="OrbGSS" width="420" height="120" />'), "the footer brand must hold exactly")
suite.case("the Turkish About footer drops the logo alt", TR_ABOUT, swap('alt="OrbGSS" width="619" height="144" />', 'alt="" width="619" height="144" />'), "tr/hakkimizda/index.html: the footer brand must hold exactly")
suite.case("the header logo shrinks under the brand minimum", CSS, swap(".brand-logo{height:28px}", ".brand-logo{height:18px}"), "under the brand's 120px minimum width")
suite.case("the illustrative map is placed on a page", ABOUT, swap("</main>", '<img src="/assets/brand/illustrative-map.jpg" alt="" /></main>'), "places the illustrative map")

# ---- the manifest --------------------------------------------------------------------------------
suite.case("the manifest keeps the old navy theme colour", "site.webmanifest", swap('"theme_color": "#FFFFFF"', '"theme_color": "#030B12"'), "site.webmanifest theme_color must be")
suite.case("the manifest background goes back to Night", "site.webmanifest", swap('"background_color": "#FFFFFF"', '"background_color": "#160A19"'), "site.webmanifest background_color must be")
suite.case("the manifest loses the 512 px icon", "site.webmanifest", regex(r'    \{\n      "src": "/assets/brand/orbgss-icon-512[^}]*\},\n', ""), "site.webmanifest icons must be exactly")

# ---- the white header and footer (the light theme) ------------------------------------------------------------
suite.case("the header goes back to the Night ground", CSS, swap("border-bottom:1px solid var(--hair);background:var(--white);position:relative;z-index:40}", "border-bottom:1px solid var(--hair);background:var(--night);position:relative;z-index:40}"), ".site-header must sit on white")
suite.case("the footer goes back to the Night ground", CSS, swap("gap:60px;background:var(--white);border-top:1px solid var(--hair)}", "gap:60px;background:var(--night);border-top:1px solid var(--hair)}"), ".site-footer must sit on white")
suite.case("white drifts in the stylesheet", CSS, swap("--white:#FFFFFF;", "--white:#FEFEFE;"), "palette token --white")
suite.case("a stray white literal appears", PARTNER, swap('<a class="skip-link"', '<a style="color:#FAFAFA" class="skip-link"'), "colour #FAFAFA is not in the Heat Trace palette")

# ---- colour rules in the stylesheet ------------------------------------------------------------------
suite.case("the hero shade goes back to navy", CSS, swap("linear-gradient(90deg,rgba(22,10,25,.97) 0%", "linear-gradient(90deg,rgba(3,11,18,.97) 0%"), "is not in the Heat Trace palette")
suite.case("a button is filled with amber", CSS, swap(".button:hover{background:var(--mist);", ".button:hover{background:var(--amber);"), "fills with amber")
suite.case("a cyan accent returns in an inline style", PARTNER, swap('<a class="skip-link"', '<a style="color:#73E7FF" class="skip-link"'), "colour #73E7FF is not in the Heat Trace palette")

# ---- the map rule: Night-family neutrals, one dashed Magma callout, no Amber or Glow -------------------------
suite.case("the map callout turns amber", MAP, lambda t: t.replace('stroke="#E43386"', 'stroke="#FFAA2E"').replace('fill="#E43386"', 'fill="#FFAA2E"'), "must carry the Magma area-of-interest callout")
suite.case("the map callout loses its dash", MAP, swap(' stroke-dasharray="6 3"', ''), "callout must be dashed")
suite.case("the map goes back to the old navy sea", MAP, swap('fill="#110C12"/>', 'fill="#030b12"/>'), "a map uses Night-family neutrals and the Magma callout only")

# ---- the caption tone follows the caption colours -------------------------------------------------------------
suite.case("the caption crossover is left at the Agate value", "script.js", swap("const CAPTION_TONE_CROSSOVER = 0.1967;", "const CAPTION_TONE_CROSSOVER = 0.1885;"), "CAPTION_TONE_CROSSOVER must be")
suite.case("the caption crossover goes missing", "script.js", swap("const CAPTION_TONE_CROSSOVER = 0.1967;", "const CAPTION_TONE_CROSSOVER_X = 0.1967;"), "CAPTION_TONE_CROSSOVER must be")

if __name__ == "__main__":
    raise SystemExit(suite.run())
