"""Negative tests of the missing-visuals work (the photographs of other places, 2026-10-25).

    python scripts/negative_tests_missing_visuals.py

One case per check of the `web_m6.context_scenes` block of scripts/validate_site.py, and per rule of the work: the
About, Partner and Marine photographs are recorded public-domain Landsat scenes of places that are NOT the pilot area,
never drawn above their own pixels, captioned with ground they show, framed as "another place, not an OrbGSS result",
and the Geothermal page carries no empty frame for a figure Science has not delivered. Each case breaks exactly one
thing in memory and checks that the validator names it, with the harness in scripts/atlas_negative.py. Run it from the
committed HEAD, one suite at a time, never in parallel with another suite.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from atlas_negative import Suite, regex, swap  # noqa: E402

suite = Suite("Negative tests - the photographs of other places and the Geothermal page without empty frames")
MANIFEST, SCRIPT, STYLES = "assets/imagery/sources.json", "script.js", "styles.css"
ABOUT, PARTNER, SOLUTIONS, GEOTHERMAL, SOURCES = ("about/index.html", "partner/index.html", "solutions/index.html",
                                                  "solutions/geothermal/index.html", "sources/index.html")
RIGHTS = "IMAGERY_RIGHTS.md"
DOT = re.S


def as_json(edit):
    def mutate(text):
        data = json.loads(text)
        edit(data)
        return json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    return mutate


def scene(data, sid):
    return next(s for s in data["web_m6"]["context_scenes"] if s["id"] == sid)


# ---- the record: provenance, rights, checksums ------------------------------------------------------------------
suite.case("a derivative loses its checksum", MANIFEST,
           as_json(lambda d: scene(d, "death-valley-2024")["derivatives"][0].update(sha256="0" * 64)),
           "does not match its recorded SHA-256 / size")
suite.case("a master is swapped without its record", MANIFEST,
           as_json(lambda d: scene(d, "aluto-rift-2026")["master"].update(sha256="0" * 64)),
           "master does not match its recorded SHA-256")
suite.case("a scene records a render with a no-data wedge", MANIFEST,
           as_json(lambda d: scene(d, "menderes-delta-2025")["production"]["render"].update(coverage=0.9)),
           "at least 99 % valid coverage")
suite.case("a derivative is wider than its master", MANIFEST,
           as_json(lambda d: scene(d, "aluto-rift-2026")["derivatives"][0].update(width_px=2000)),
           "(upscaled)")
suite.case("a scene stops recording that nothing is upscaled", MANIFEST,
           as_json(lambda d: scene(d, "death-valley-2024").update(operations_not_used=["tone or colour change", "generative or AI step"])),
           "must record that no upscaling is used")
suite.case("a scene stops recording the public-domain basis", MANIFEST,
           as_json(lambda d: scene(d, "menderes-delta-2025").update(rights_basis="Licensed.")),
           "must record the public-domain basis and the USGS credit line")
suite.case("a scene names a product that is not Collection 2 Level-2 Tier 1", MANIFEST,
           as_json(lambda d: scene(d, "death-valley-2024")["production"].update(product_ids=["LC08_L1TP_040035_20241003_01_RT"])),
           "must name a Landsat Collection 2 Level-2 Tier 1 product")
suite.case("a scene's acquisition date disagrees with its product", MANIFEST,
           as_json(lambda d: scene(d, "aluto-rift-2026").update(acquired="2020-01-01")),
           "says it was acquired")
suite.case("a scene is recorded for the wrong page", MANIFEST,
           as_json(lambda d: scene(d, "aluto-rift-2026").update(page="about")),
           "is recorded for 'about', expected 'partner'")
suite.case("a scene loses its measured placement", MANIFEST,
           as_json(lambda d: scene(d, "death-valley-2024").pop("rendered")),
           "is missing rendered")
suite.case("a scene's measured upscale exceeds the bound", MANIFEST,
           as_json(lambda d: scene(d, "menderes-delta-2025")["rendered"].update(max_upscale_factor=1.45)),
           "the bound is")
suite.case("a scene's recorded width exceeds its pixels", MANIFEST,
           as_json(lambda d: scene(d, "aluto-rift-2026")["rendered"].update(max_css_width=1200)),
           "above its 1000 px widest candidate")
suite.case("IMAGERY_RIGHTS.md stops recording a scene", RIGHTS,
           lambda t: t.replace("death-valley-2024", "death-v"), "does not record the interior crop 'death-valley-2024'")

# ---- the scene is never the pilot ---------------------------------------------------------------------------------
suite.case("a scene's ground reaches the pilot area", MANIFEST,
           as_json(lambda d: scene(d, "menderes-delta-2025")["production"]["render"].update(bounds_wgs84=[27.0, 37.0, 29.5, 38.5])),
           "reaches the Kızıldere pilot area")
suite.case("a scene is captioned as the pilot area", SCRIPT,
           swap("'scene.aluto.place': 'Aluto volcano, Ethiopia',", "'scene.aluto.place': 'Kızıldere pilot area, Türkiye',"),
           "names the pilot area")
suite.case("a scene's description names the pilot area", SCRIPT,
           swap("'alt.deathvalley': 'Natural-colour Landsat 9 view of Death Valley:", "'alt.deathvalley': 'Natural-colour Landsat 9 view of the Kızıldere pilot area:"),
           "names the pilot area")
suite.case("a pilot-area photograph replaces the About figure", ABOUT,
           swap('src="/assets/imagery/death-valley-2024-149bc2b0-1600.webp"', 'src="/assets/imagery/kizildere-stage-161b5b57-1600.webp"'),
           "recorded for 'about' alone")

# ---- captions name ground the image shows ---------------------------------------------------------------------------
suite.case("a caption names a point outside its scene", SCRIPT,
           swap("'scene.deathvalley.coords': '36.3000° N, 116.7500° W',", "'scene.deathvalley.coords': '37.9794° N, 28.7907° E',"),
           "outside the ground the scene shows")
suite.case("the Turkish caption coordinate drifts from the English one", SCRIPT,
           swap("'scene.aluto.coords': '7.7800° K, 38.8000° D',", "'scene.aluto.coords': '7.7800° K, 38.8100° D',"),
           "names different coordinates in en and tr")
suite.case("a figure is captioned with another scene's keys", ABOUT,
           swap('data-i18n="scene.deathvalley.place"', 'data-i18n="scene.aluto.place"'),
           "is captioned with")
suite.case("a figure is described by another scene's description", PARTNER,
           swap('data-i18n-alt="alt.aluto"', 'data-i18n-alt="alt.deathvalley"'),
           "the image is described by")

# ---- framing: another place, not an OrbGSS result --------------------------------------------------------------------
suite.case("About loses the illustrative framing", ABOUT,
           swap('data-i18n="scene.illustrative"', 'data-i18n="scene.illustrativeX"'),
           "does not carry the illustrative framing scene.illustrative")
suite.case("Partner loses the illustrative framing", PARTNER,
           regex(r'<p class="act-footnote scene-note">.*?</p>', "", DOT),
           "does not carry the illustrative framing scene.illustrative")
suite.case("the framing stops saying it is another place", SCRIPT,
           swap("'scene.illustrative': 'A public-domain Landsat scene of another place, not an OrbGSS result.',", "'scene.illustrative': 'Shown for illustration.',"),
           "must say, in both languages, that the scene is of another place")
suite.case("the Marine panel is shown on a second page", PARTNER,
           swap("</main>", '<img src="/assets/imagery/menderes-delta-2025-34e35c2d-900.webp" alt="" width="900" height="562">\n  </main>'),
           "recorded for 'solutions' alone")

# ---- the figure may not grow past its pixels --------------------------------------------------------------------------
suite.case("the Partner figure is allowed to grow past its scene", STYLES,
           swap(".split-figure{position:relative;width:100%;max-width:500px;", ".split-figure{position:relative;width:100%;max-width:640px;"),
           "is capped at 640 CSS px")
suite.case("the About figure is allowed to grow past its scene", STYLES,
           swap(".wide-figure{position:relative;width:100%;max-width:728px;", ".wide-figure{position:relative;width:100%;max-width:900px;"),
           "is capped at 900 CSS px")

# ---- the Sources page lists the scenes -----------------------------------------------------------------------------------
suite.case("the Sources page drops a scene credit", SOURCES,
           regex(r'\s*<li class="credit-row">\s*<img class="thumb" src="/assets/imagery/death-valley-2024[^"]*".*?</li>', "", DOT),
           "thumbnailed image credits, expected at least 9")

# ---- Geothermal shows no empty frame ---------------------------------------------------------------------------------------
suite.case("an empty pending frame returns to Geothermal", GEOTHERMAL,
           swap('<section class="ground ground-paper" id="missing"', '<div class="plate-pending"></div>\n    <section class="ground ground-paper" id="missing"'),
           "a frame still to be supplied is on the page")
suite.case("the iron frame returns to the atlas", GEOTHERMAL,
           swap('<section class="ground ground-paper" id="missing"', '<figure class="plate geo-plate" id="iron"></figure>\n    <section class="ground ground-paper" id="missing"'),
           "#iron is back on the page")
suite.case("the relief section returns", GEOTHERMAL,
           swap('<section class="ground ground-paper" id="missing"', '<section class="ground ground-orbit geo-relief" id="relief"></section>\n    <section class="ground ground-paper" id="missing"'),
           "#relief is back on the page")
suite.case("the missing index stops listing the iron layer", GEOTHERMAL,
           regex(r'\s*<div class="geo-missing-row"><span data-i18n="geothermalPage\.layer\.iron">.*?</div>', "", DOT),
           "must list the iron layer and the relief figure as two unlinked rows")

raise SystemExit(suite.run())
