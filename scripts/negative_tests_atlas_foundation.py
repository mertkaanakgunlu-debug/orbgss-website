"""Negative tests of the Atlas redesign's shared foundation (MER-275).

    python scripts/negative_tests_atlas_foundation.py

The foundation is the palette (since MER-279 the Agate brand colours and their rules, and no other UI colour), the type system (OrbGSS
Sans 300 / 400 and OrbGSS Mono 400, the scale, no other weight), the self-hosted fonts and their licence, the
marked regions that keep the page threads apart, and the shared components. Each case breaks exactly one of
them in memory and checks that scripts/validate_site.py names it. Run it from a detached worktree of the
committed HEAD, one suite at a time (scripts/atlas_negative.py).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from atlas_negative import Suite, regex, swap  # noqa: E402

suite = Suite("Atlas negative tests - foundation (MER-275)")
CSS, JS, FONTS = "styles.css", "script.js", "assets/fonts/fonts.json"

# ---- the palette ---------------------------------------------------------------------------------
suite.case("a palette token drifts", CSS, swap("--teal-light:#58AEB2;", "--teal-light:#43BFF0;"), "palette token --teal-light")
suite.case("a line token drifts", CSS, swap("--rule:rgba(183,192,189,.22);", "--rule:rgba(183,192,189,.5);"), "palette token --rule")
suite.case("a retired WEB-005B token comes back", CSS, swap("body{margin:0;background:var(--ground)", "body{margin:0;background:var(--orb-bg)"), "retired colour token --orb-bg")
suite.case("a retired beam token is defined again", CSS, swap("--ground:#171A1B;", "--ground:#171A1B;\n  --orb-beam-core:#7FEFFF;"), "retired colour token --orb-beam-core")
suite.case("a stray hex colour in a rule", CSS, swap(".site-footer{min-height:180px;", ".site-footer{color:#ffffff;min-height:180px;"), "is not in the Agate palette")
suite.case("a stray rgba colour in a rule", CSS, swap(".beam-note{margin:0;", ".beam-note{color:rgba(10,10,10,.5);margin:0;"), "is not in the Agate palette")
suite.case("a CSS named colour", CSS, swap(".kicker,.mono-label{margin:0 0 18px;", ".kicker,.mono-label{border-color:red;margin:0 0 18px;"), "border-color: red")
suite.case("an inline style colour on the homepage", "index.html", swap('<a class="skip-link"', '<a style="color:#ffffff" class="skip-link"'), "index.html: colour #ffffff")
suite.case("a <style> block colour on the About page", "about/index.html", swap("</head>", "<style>a{color:#ABCDEF}</style></head>"), "about/index.html: colour #ABCDEF")
suite.case("gold used as a fill", CSS, swap(".plate-gap{border:1px dashed var(--gold-light);", ".plate-gap{background:var(--gold-light);border:1px dashed var(--gold-light);"), "never a fill")
suite.case("a retired Atlas token comes back (--signal)", CSS, swap(".skip-link{position:fixed;", ".skip-link{border-color:var(--signal);position:fixed;"), "retired colour token --signal")
suite.case("a retired Atlas token comes back (--paper)", CSS, swap(".lede{margin:0;font-size:var(--t-lede);line-height:1.62;color:var(--fg);", ".lede{margin:0;font-size:var(--t-lede);line-height:1.62;color:var(--paper);"), "retired colour token --paper")
suite.case("a retired Atlas token is defined again (--orbit)", CSS, swap("--ground:#171A1B;", "--ground:#171A1B;\n  --orbit:#030B12;"), "retired colour token --orbit")
suite.case("the old Orbit navy returns as a rule colour", CSS, swap(".beam-note{margin:0;", ".beam-note{color:rgba(3,11,18,.5);margin:0;"), "is not in the Agate palette")

# ---- the type system -----------------------------------------------------------------------------
suite.case("a medium weight appears", CSS, swap(".t-figure{margin:0;font-size:var(--t-figure);font-weight:400;", ".t-figure{margin:0;font-size:var(--t-figure);font-weight:500;"), "font-weight 500")
suite.case("a third family appears", CSS, swap(".t-figure{margin:0;", ".t-figure{font-family:\"Space Grotesk\";margin:0;"), "only var(--sans)")
suite.case("a font shorthand appears", CSS, swap(".lede{margin:0;", ".lede{font:400 19px/1.5 serif;margin:0;"), "font shorthand")
suite.case("font synthesis is switched back on", CSS, swap("font-synthesis-weight:none;", ""), "font-synthesis-weight:none")
suite.case("capitals get a second tracking", CSS, swap(".kicker,.mono-label{margin:0 0 18px;font-family:var(--mono);font-variant-ligatures:none;font-size:var(--t-label);font-weight:400;line-height:1.6;letter-spacing:var(--track);", ".kicker,.mono-label{margin:0 0 18px;font-family:var(--mono);font-variant-ligatures:none;font-size:var(--t-label);font-weight:400;line-height:1.6;letter-spacing:.24em;"), "caps use one tracking")
suite.case("capitals get a third size", CSS, swap(".domain-status{margin:2px 0 0;font-family:var(--mono);font-variant-ligatures:none;font-size:var(--t-label);", ".domain-status{margin:2px 0 0;font-family:var(--mono);font-variant-ligatures:none;font-size:13px;"), "caps come in the label and caption sizes")
suite.case("text under 10px on the homepage", CSS, swap(".act-meta{margin:0;font-size:var(--t-caption);", ".act-meta{margin:0;font-size:9px;"), "nothing is set under 10px")

# ---- the self-hosted fonts -----------------------------------------------------------------------
suite.case("a font file no longer matches its record", FONTS, regex(r'("sans-300": \{.*?"sha256": ")[0-9a-f]{64}', r"\g<1>" + "0" * 64, 16), "recorded SHA-256")
suite.case("a family takes IBM's reserved name", FONTS, swap('"family": "OrbGSS Mono"', '"family": "IBM Plex Mono"'), "reserved name")
suite.case("the licence loses its text", "assets/fonts/OFL.txt", swap("SIL OPEN FONT LICENSE Version 1.1", "a licence"), "SIL OPEN FONT LICENSE Version 1.1")
suite.case("the licence loses IBM's notice", "assets/fonts/OFL.txt", lambda t: t.replace("Copyright 2018 IBM Corp.", "Copyright"), "Copyright 2018 IBM Corp.")
suite.case("a face stops swapping", CSS, swap("font-display:swap;", "", ), "font-display: swap")
suite.case("a face loads another file", CSS, regex(r'url\("assets/fonts/orbgss-sans-300\.[0-9a-f]{8}\.woff2"\)', 'url("assets/fonts/other.woff2")'), "exactly the recorded font files")
suite.case("a face loses the recorded unicode-range", CSS, swap("unicode-range:U+0020-007E", "unicode-range:U+0021-007E"), "unicode-range")
suite.case("a fallback loses its metric match", CSS, swap("size-adjust:99.09%;", ""), "lost its size-adjust")
suite.case("a page stops preloading the fonts", "about/index.html", regex(r'  <link rel="preload" href="/assets/fonts/orbgss-sans-300[^\n]*\n', ""), "must preload the Sans 300 and Sans 400")
suite.case("the Turkish twin stops preloading the fonts", "tr/index.html", regex(r'  <link rel="preload" href="/assets/fonts/orbgss-sans-400[^\n]*\n', ""), "must preload the Sans 300 and Sans 400")

# ---- the regions ---------------------------------------------------------------------------------
suite.case("a CSS region end marker is removed", CSS, swap("/* === /atlas:home === */", ""), "must contain exactly the regions")
suite.case("a rule sits outside every region", CSS, lambda t: t.rstrip("\n") + "\n.stray{display:none}\n", "rules outside the atlas regions")
suite.case("a dictionary region is removed", JS, swap("// === /atlas:geothermal ===", "", ), "must carry the dictionary regions")
suite.case("a page-group key sits in the shared dictionary", JS, swap("    'a11y.skip': 'Skip to content',", "    'a11y.skip': 'Skip to content',\n    'geothermalPage.stray': 'x',"), "belongs in the atlas:geothermal region")
suite.case("a foreign key sits in a group's dictionary region", JS, regex(r"(// === atlas:partner-sources ===[^\n]*\n)", r"\g<1>    'nav.stray': 'x',\n"), "is not one of its prefixes")
suite.case("a validator region marker is removed", "scripts/validate_site.py", swap("# === /atlas:geothermal ===", "#"), "must carry the region atlas:geothermal")

# ---- the shared components -----------------------------------------------------------------------
suite.case("the mandatory warning loses its gold rule", CSS, swap("border-left:2px solid var(--limit-line)", "border-left:2px solid var(--mineral-light)"), "2px gold left rule")
suite.case("a plate gets a radius", CSS, swap(".plate{margin:0;width:100%;max-width:600px}", ".plate{margin:0;width:100%;max-width:600px;border-radius:4px}"), "gives a plate chrome")
suite.case("the paper ground keeps the dark-ground teal for links", CSS, swap("--link:var(--teal);--limit", "--link:var(--teal-light);--limit"), "paper ground must carry")
suite.case("the header leaves the Graphite ground", CSS, swap("border-bottom:1px solid var(--rule-soft);background:var(--ground);position:relative;z-index:40}", "border-bottom:1px solid var(--rule-soft);background:var(--ground-lift);position:relative;z-index:40}"), "must sit on the Graphite ground")
suite.case("the target frame turns teal", CSS, swap("height:22px;border:0 solid var(--gold-light)", "height:22px;border:0 solid var(--teal-light)"), "target frame must be Mineral Gold")
suite.case("the plate component is deleted", CSS, swap(".plate-frame{position:relative;", ".platex-frame{position:relative;"), "lost the shared component .plate-frame")

if __name__ == "__main__":
    raise SystemExit(suite.run())
