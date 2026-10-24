"""Negative tests of the Atlas redesign: Geothermal (MER-276).

    python scripts/negative_tests_atlas_geothermal.py

One case per check of the atlas:geothermal region of scripts/validate_site.py, plus the generic hooks MER-276
added for A1 (a governed raster's second, recorded home). Each case breaks exactly one thing in memory and
checks that the validator names it, with the harness in scripts/atlas_negative.py. Run it from a detached
worktree of the committed HEAD, one suite at a time.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from atlas_negative import Suite, regex, swap  # noqa: E402

suite = Suite("Atlas negative tests - Geothermal (MER-276)")
PAGE, CSS, JS, SOURCES = "solutions/geothermal/index.html", "styles.css", "script.js", "assets/imagery/sources.json"
DOT = re.S

# ---- the page frame -----------------------------------------------------------------------------
suite.case("the body loses the class its CSS is scoped to", PAGE, swap('<body class="interior page-geothermal">', '<body class="interior">'), "page-geothermal")
suite.case("an old pilot alias disappears", PAGE, swap('id="pilot-structure"', 'id="pilot-structures"'), "#pilot-structure is missing")
suite.case("the result chapter leaves Orbit", PAGE, swap('<section class="ground ground-orbit" id="result"', '<section class="ground ground-paper" id="result"'), "section #result must sit on ground-orbit")
suite.case("the record chapter leaves paper", PAGE, swap('<section class="ground ground-paper" id="glance"', '<section class="ground ground-lift" id="glance"'), "section #glance must sit on ground-paper")
suite.case("the ledger leaves paper", PAGE, swap('<section class="ground ground-paper geo-ledger"', '<section class="ground ground-lift geo-ledger"'), "the ledger (Establishes / Does not establish) must be a paper band")
suite.case("the chapter index points elsewhere", PAGE, regex(r'(<nav class="lead-set geo-index-list".*?)href="#result"', r'\g<1>href="#results"', DOT), "the chapter index links")
suite.case("the missing index loses a link", PAGE, regex(r'(<div class="geo-missing-list lead-set".*?)href="#iron"', r'\g<1>href="#irons"', DOT), "the index of what is missing links")
suite.case("prototype wording comes back", PAGE, swap("<body class=\"interior page-geothermal\">", "<body class=\"interior page-geothermal\"><!-- prototype -->"), "prototype wording is back")

# ---- the atlas -----------------------------------------------------------------------------------
suite.case("a plate leaves the atlas order", PAGE, swap('<figure class="plate geo-plate" id="elevation">', '<figure class="plate geo-plate" id="elevations">'), "the atlas holds plates")
suite.case("a plate loses its warning key", PAGE, regex(r'(id="thermal">.*?class="plate-note beam-note" data-i18n=")[^"]+', r"\g<1>story.terrain.note", DOT), "plate #thermal must carry its mandatory warning")
suite.case("a plate image is declared at the wrong grid", PAGE, regex(r'(id="alteration">.*?)width="1200"', r'\g<1>width="1000"', DOT), "plate #alteration: the image is declared")
suite.case("a plate image gets an inline style", PAGE, regex(r'(id="thermal">.*?<img )', r'\g<1>style="filter:contrast(1.2)" ', DOT), "plate #thermal: an inline style on a plate image")
suite.case("a plate caption names the wrong things", PAGE, regex(r'(id="thermal">.*?)scene.aoi.coords', r'\g<1>scene.priority.coords', DOT), "plate #thermal: the bottom-right caption must read")
suite.case("a plate frame loses its caption tone", PAGE, swap('<div class="plate-frame" data-label-tone="light" data-visual-slot="thermal"', '<div class="plate-frame" data-visual-slot="thermal"'), "plate #thermal: the frame lost its data-label-tone")
suite.case("an analytical plate stops saying product-proof", PAGE, swap('data-visual-slot="alteration" data-visual-status="product-proof"', 'data-visual-slot="alteration" data-visual-status="photo"'), 'must say data-visual-status="product-proof"')
suite.case("a plate shows another layer's derivative", PAGE, regex(r'(id="alteration">.*?)alt01-900\.webp', r"\g<1>priority-900.webp", DOT), "which are not recorded MER-151 derivatives of alt01")
suite.case("a plate drops the 600/900/1200 ladder", PAGE, regex(r'(id="thermal">.*?)srcset="[^"]+"', r'\g<1>', DOT), "plate #thermal must offer the 600, 900 and 1200 px derivatives")
suite.case("the data-gap plate is filled with an image", PAGE, swap('<div class="plate-gap">', '<img src="/assets/proof/web005b/thm01-600.webp" alt="x" width="1200" height="1200"><div class="plate-gap">'), "plate #gap is the data gap")
suite.case("the pending plate is filled with an image", PAGE, swap('<div class="plate-pending">', '<img src="/assets/proof/web005b/alt01-600.webp" alt="x" width="1200" height="1200"><div class="plate-pending">'), "plate #iron is an asset still to be supplied")
suite.case("the pending plate stops saying so", PAGE, regex(r'(id="iron">.*?)geothermalPage\.layer\.pending', r"\g<1>geothermalPage.relief.state", DOT), "must say 'Accepted, not shown yet'")
suite.case("a foreign governed raster appears", PAGE, swap('<div class="plate-gap">', '<img src="/assets/proof/final/anything.webp" alt="" width="10" height="10"><div class="plate-gap">'), "a governed raster that is not one of the four MER-151 layers")

# ---- nothing touches a governed raster -----------------------------------------------------------
suite.case("CSS filters a governed raster", CSS, swap(".geo-plate{position:relative}", ".geo-plate{position:relative;filter:saturate(1.2)}"), "near a governed raster")
suite.case("the plate cap grows past the native grid", CSS, swap(".plate{margin:0;width:100%;max-width:600px}", ".plate{margin:0;width:100%;max-width:640px}"), "must cap a plate at 600 CSS px")
suite.case("text under 10px on the Geothermal page", CSS, swap(".geo-plate{position:relative}", ".geo-plate{position:relative;font-size:9px}"), "nothing is set under 10px")

# ---- the result ----------------------------------------------------------------------------------
suite.case("the priority plate is lost", PAGE, swap('<figure class="plate geo-priority" data-lead-visual>', '<figure class="plate geo-prio" data-lead-visual>'), "the result lost its priority plate")
suite.case("the priority plate shows another candidate set", PAGE, regex(r'(<figure class="plate geo-priority".*?)priority-600\.webp 600w, ', r"\g<1>", DOT), "the priority plate must show priority-1200.webp")
suite.case("the priority caption loses the accepted label", PAGE, regex(r'(<figure class="plate geo-priority".*?)data-i18n="label\.priority"', r'\g<1>data-i18n="label.priorityX"', DOT), "the priority plate's caption must read")
suite.case("the priority plate loses its scale bar", PAGE, swap('<div class="geo-bar" role="img"', '<div class="geo-bar"'), "must keep its legend ramp and its 10 km scale bar")
suite.case("the result loses the verbatim warning", PAGE, regex(r'(id="result".*?)data-i18n="act\.priority\.note"', r'\g<1>data-i18n="act.context.note"', DOT), "the result block must carry the verbatim priority warning")
suite.case("the relief block loses the verbatim warning", PAGE, regex(r'(id="relief".*?)data-i18n="act\.priority\.note"', r'\g<1>data-i18n="act.context.note"', DOT), "the relief block must carry the verbatim priority warning")
suite.case("the relief slot is filled before Science delivers", PAGE, swap('<div class="plate-frame" data-visual-slot="relief" data-visual-status="to-be-supplied">', '<div class="plate-frame" data-visual-slot="relief" data-visual-status="to-be-supplied"><img src="/assets/proof/web005b/priority-600.webp" alt="x" width="1200" height="1200">'), "the relief slot is an asset still to be supplied")

# ---- the ledger ----------------------------------------------------------------------------------
suite.case("the ledger loses a term", PAGE, regex(r'\s*<li data-i18n="geothermalPage\.not\.validation">[^<]*</li>', ""), "the ledger's Does not establish column holds")
suite.case("the ledger stops being the warning's own", PAGE, swap('<ul class="beam-note">', '<ul class="plain">'), "must carry beam-note")
suite.case("a ledger term drifts from the warning", JS, swap("'geothermalPage.not.reserve': 'Reserve or resource estimation'", "'geothermalPage.not.reserve': 'Reserve estimate'"), "in the English dictionary is")

# ---- the dictionary ------------------------------------------------------------------------------
suite.case("the page uses a key no language has", PAGE, swap('data-i18n="geothermalPage.relief.title"', 'data-i18n="geothermalPage.relief.nothing"'), "is used by the page but missing")
suite.case("the dictionary keeps a key nothing uses", JS, swap("    'geothermalPage.not.reserve':", "    'geothermalPage.orphan': 'x',\n    'geothermalPage.not.reserve':"), "no element of the page uses it")
suite.case("the review note disappears from the Turkish block", JS, swap("pending the CTO's language review", "reviewed"), "pending the CTO's language review")

# ---- the A1 placement records --------------------------------------------------------------------
suite.case("a layer's second home is not recorded", SOURCES, swap('"geothermal_placement": {', '"geothermal_placement_x": {'), "has no geothermal_placement record")
suite.case("a record claims the acceptance", SOURCES, regex(r'("geothermal_placement": \{.*?"acceptance": ")[^"]+', r"\g<1>A1 accepted", DOT), "say the acceptance is pending")
suite.case("a record is measured past the cap", SOURCES, regex(r'("geothermal_placement": \{.*?"max_css_width": )\d+', r"\g<1>640", DOT), "above its 1200 px native grid or the 600 CSS px cap")
suite.case("a record names another layer's file", SOURCES, regex(r'("geothermal_placement": \{.*?"selected_derivative": ")[^"]+', r"\g<1>assets/proof/web005b/priority-1200.webp", DOT), "names a derivative that is not the layer's own")
suite.case("a record upscales", SOURCES, regex(r'("geothermal_placement": \{.*?"max_upscale_factor": )[\d.]+', r"\g<1>1.3", DOT), "measured at fewer than 12 viewports or upscales")

# ---- the A1 hooks in the generic checks ----------------------------------------------------------
suite.case("a governed layer appears on a page A1 does not name", "about/index.html", swap("</main>", '<section class="page-section"><img src="/assets/proof/web005b/thm01-600.webp" alt="" width="1200" height="1200"></section></main>'), "web_005b")

if __name__ == "__main__":
    raise SystemExit(suite.run())
