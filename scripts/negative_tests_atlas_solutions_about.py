"""Negative tests of the Atlas redesign: Solutions and About (MER-277).

    python scripts/negative_tests_atlas_solutions_about.py

The checks being proved live in the atlas:solutions-about region of scripts/validate_site.py: the grounds the approved
palette page assigns (Solutions and About open on Orbit, the Mining and Marine pair sits on Lift, the About statement
and the six principles sit on Paper), the three-row domain index, the pilot index, the six principles, the layer
index, and the rule that a governed raster appears on these two pages only as an index thumbnail of at most 160 CSS px
with no filter, transform or opacity on it. Each case breaks exactly one of them in memory and checks that
scripts/validate_site.py names it. Run from a detached worktree of the committed HEAD, one suite at a time
(scripts/atlas_negative.py).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from atlas_negative import Suite, regex, swap  # noqa: E402

suite = Suite("Atlas negative tests - Solutions and About (MER-277)")
CSS, JS = "styles.css", "script.js"
SOL, ABOUT = "solutions/index.html", "about/index.html"
TR_SOL, TR_ABOUT = "tr/cozumler/index.html", "tr/hakkimizda/index.html"

# ---- the grounds ---------------------------------------------------------------------------------
suite.case("the Solutions opening moves to Paper", SOL,
           swap('<section class="page-hero is-ledger"', '<section class="page-hero is-ledger ground-paper"'),
           "the page opening must sit on Orbit")
suite.case("the About opening moves to Lift", ABOUT,
           swap('<section class="page-hero is-statement"', '<section class="page-hero is-statement ground-lift"'),
           "the page opening must sit on Orbit")
suite.case("the Mining and Marine pair leaves Lift", SOL,
           swap('<section class="domain-pair ground ground-lift"', '<section class="domain-pair ground ground-orbit"'),
           "the Mining and Marine pair must sit on Lift")
suite.case("the pair is repainted by its own rule", CSS,
           swap(".domain-pair{position:relative;padding:", ".domain-pair{position:relative;background:var(--ground);padding:"),
           ".domain-pair paints its own background")
suite.case("the footnote leaves the pair's Lift ground", CSS,
           swap(".page-solutions .page-note{padding:0 var(--pad) clamp(56px,6vw,88px);background:var(--ground-lift)}",
                ".page-solutions .page-note{padding:0 var(--pad) clamp(56px,6vw,88px);background:var(--ground)}"),
           "must sit on the pair's Lift ground")
suite.case("a Paper band appears on Solutions", SOL,
           swap('<section class="domain-feature" id="geothermal"', '<section class="domain-feature ground ground-paper" id="geothermal"'),
           "Solutions has no Paper ground")
suite.case("the About statement moves to Orbit", ABOUT,
           swap('<section class="about-position ground ground-paper"', '<section class="about-position ground ground-orbit"'),
           "#position must sit on Paper")
suite.case("the six principles move to Lift", ABOUT,
           swap('<section class="about-principles ground ground-paper"', '<section class="about-principles ground ground-lift"'),
           "#principles must sit on Paper")
suite.case("the About problem moves to Paper", ABOUT,
           swap('<section class="about-problem ground ground-orbit"', '<section class="about-problem ground ground-paper"'),
           "#problem must sit on Orbit")
suite.case("the page CSS hook is dropped from About", ABOUT,
           swap('<body class="interior page-about">', '<body class="interior">'),
           "the page's CSS hangs on page-about")
suite.case("the Turkish Solutions page loses its CSS hook", TR_SOL,
           swap('<body class="interior page-solutions">', '<body class="interior">'),
           "the page's CSS hangs on page-solutions")

# ---- Solutions: the domain index and the pilot index ----------------------------------------------
suite.case("the domain index loses its Marine row", SOL,
           regex(r'\s*<li>\s*<a class="index-row" href="#marine">.*?</a>\s*</li>', "", __import__("re").S),
           "the domain index must be three native links")
suite.case("a domain row points somewhere else", SOL,
           swap('<a class="index-row" href="#mining">', '<a class="index-row" href="#minerals">'),
           "the domain index must be three native links")
suite.case("the Geothermal row loses its thumbnail", SOL,
           regex(r'<span class="index-thumb"><img class="thumb row-thumb"[^>]*/></span>', '<span class="index-thumb"></span>'),
           "leads with a thumbnail")
suite.case("an expansion direction row gains an image", SOL,
           swap('<span class="index-thumb is-none" aria-hidden="true"><span data-i18n="solutionsPage.thumb.none">None yet</span></span>',
                '<span class="index-thumb is-none" aria-hidden="true"><img class="thumb row-thumb" src="/assets/proof/web005b/priority-600.webp" alt="x" data-i18n-alt="solutionsPage.thumb.priority" width="112" height="112" loading="lazy" /></span>'),
           "shows no image, only the 'none yet' frame")
suite.case("a domain row loses its status label", SOL,
           regex(r'\s*<span class="domain-status mono" data-i18n="app\.marine\.status">Expansion direction</span>', ""),
           "every domain index row carries its name and its status label")
suite.case("the pilot index loses a link", SOL,
           regex(r'\s*<a href="/solutions/geothermal/#layers"><span data-i18n="solutionsPage.pilotnav.atlas">.*?</a>', ""),
           "the pilot index must link the pilot record")
suite.case("the pilot index leaves the Geothermal page", SOL,
           swap('<a href="/solutions/geothermal/#glance">', '<a href="/about/#glance">'),
           "the pilot index must link the pilot record")
suite.case("the Geothermal band loses its lead photograph", SOL,
           swap("<img\n          data-lead-visual\n          src=\"/assets/imagery/yellowstone-2013-1400.webp\"", "<img\n          src=\"/assets/imagery/yellowstone-2013-1400.webp\""),
           "#geothermal must be the Geothermal band")
suite.case("the footnote no longer follows the pair", SOL,
           regex(r'(\s*<div class="page-note">.*?</div>\s*</div>)(\s*<div class="page-closing">)', r'\2\1', __import__("re").S),
           "the illustrative footnote (div.page-note) must follow the pair directly")
suite.case("the Solutions title loses its tone clause", SOL,
           swap('<span class="tone" data-i18n="solutionsPage.title.tail">', '<span data-i18n="solutionsPage.title.tail">'),
           "the page title is two clauses")

# ---- governed rasters: an index thumbnail and nothing else ---------------------------------------------
suite.case("a layer thumbnail loses its thumbnail class", ABOUT,
           swap('<img class="thumb row-thumb" src="/assets/proof/web005b/thm01-600.webp"', '<img class="row-thumb" src="/assets/proof/web005b/thm01-600.webp"'),
           "it may appear only as an index thumbnail")
suite.case("a layer thumbnail is declared at full size", ABOUT,
           swap('src="/assets/proof/web005b/alt01-600.webp" alt="Thumbnail: alteration signal" data-i18n-alt="aboutPage.thumb.alteration" width="88" height="88"',
                'src="/assets/proof/web005b/alt01-600.webp" alt="Thumbnail: alteration signal" data-i18n-alt="aboutPage.thumb.alteration" width="600" height="600"'),
           "it may appear only as an index thumbnail")
suite.case("a governed raster is shown full size on Solutions", SOL,
           swap("    <div class=\"page-closing\">", "    <section class=\"page-section\"><img data-lead-visual src=\"/assets/proof/web005b/priority-600.webp\" alt=\"\" width=\"600\" height=\"600\" /></section>\n    <div class=\"page-closing\">"),
           "it may appear only as an index thumbnail")
suite.case("a thumbnail gets a CSS filter", CSS,
           swap("img.row-thumb{display:block;aspect-ratio:1/1;", "img.row-thumb{filter:saturate(1.4);display:block;aspect-ratio:1/1;"),
           "puts a filter, transform or opacity on a thumbnail")
suite.case("a thumbnail gets a transform", CSS,
           swap(".layer-thumbs{display:flex;gap:10px}", ".layer-thumbs{display:flex;gap:10px;transform:scale(1.2)}"),
           "puts a filter, transform or opacity on a thumbnail")
suite.case("an index thumbnail is sized past 160px", CSS,
           swap(".index-thumb{display:block;width:clamp(72px,8vw,112px);", ".index-thumb{display:block;width:clamp(72px,8vw,240px);"),
           "an index thumbnail is at most 160 CSS px")

# ---- About: the principles, the statement, the layer index, the data link ----------------------------------
suite.case("a seventh principle appears", ABOUT,
           swap("          <li>\n            <h3 data-i18n=\"proof.decision.title\">", "          <li><h3>Extra</h3><p>An extra principle.</p></li>\n          <li>\n            <h3 data-i18n=\"proof.decision.title\">"),
           "the principles are six items")
suite.case("a principle loses its sentence", ABOUT,
           regex(r'\n\s*<p data-i18n="aboutPage.principle.decision">.*?</p>', ""),
           "the principles are six items")
suite.case("the published principle loses its tone sentence", ABOUT,
           swap('<span class="tone" data-i18n="aboutPage.position.statement.tail">', '<span data-i18n="aboutPage.position.statement.tail">'),
           "the published principle is two sentences")
suite.case("the layer index loses a thumbnail", ABOUT,
           regex(r'\s*<img class="thumb row-thumb" src="/assets/proof/web005b/terrain-600-d.webp"[^>]*/>', ""),
           "holding five thumbnails")
suite.case("the layer index leaves the layer atlas", ABOUT,
           swap('<a class="layer-index" href="/solutions/geothermal/#layers">', '<a class="layer-index" href="/solutions/geothermal/">'),
           "holding five thumbnails")
suite.case("the data section stops linking the Sources page", ABOUT,
           swap('<p class="chapter-link"><a class="text-link" href="/sources/">', '<p class="chapter-link"><a class="text-link" href="/solutions/">'),
           "links to the Sources page")
suite.case("the Turkish data link points at the English Sources page", TR_ABOUT,
           swap('<p class="chapter-link"><a class="text-link" href="/tr/kaynaklar/">', '<p class="chapter-link"><a class="text-link" href="/sources/">'),
           "links to the Sources page")

# ---- the group opts into the type rules --------------------------------------------------------------------
suite.case("a caption-size rule drops under 10px in the Solutions and About region", CSS,
           swap(".index-thumb.is-none{display:flex;align-items:center;justify-content:center;border:1px dashed var(--rule);font-family:var(--mono);font-variant-ligatures:none;font-size:var(--t-caption);",
                ".index-thumb.is-none{display:flex;align-items:center;justify-content:center;border:1px dashed var(--rule);font-family:var(--mono);font-variant-ligatures:none;font-size:9px;"),
           "nothing is set under 10px")
suite.case("capitals in the region take a second tracking", CSS,
           swap(".pilot-index>*{display:inline-flex;align-items:center;gap:12px;min-height:64px;font-family:var(--mono);font-variant-ligatures:none;font-size:var(--t-label);letter-spacing:var(--track);",
                ".pilot-index>*{display:inline-flex;align-items:center;gap:12px;min-height:64px;font-family:var(--mono);font-variant-ligatures:none;font-size:var(--t-label);letter-spacing:.24em;"),
           "caps use one tracking")
suite.case("a Solutions string loses its Turkish value", JS,
           regex(r"\n    'solutionsPage\.pilotnav\.result': 'Sonuç ve sınırları',", ""),
           "has no Turkish value")

if __name__ == "__main__":
    raise SystemExit(suite.run())
