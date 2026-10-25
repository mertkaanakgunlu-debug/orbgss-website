"""Deliberately break each MER-255 / interior-redesign invariant and confirm validate_site.py catches it.

    py -3.14 scripts/negative_tests_mer255.py

MER-255 rebuilt the five interior pages (docs/WEB_INTERIOR_REDESIGN_AUTHORITY.md): one visual grammar
(`body.interior`) with a different opening on each page, four recorded Class A crops of the Kızıldere
master in place of text and tables, ruled lists in place of tables, and the attribution moved from an About table to its own
/sources/ page. The contract worth guarding: the grammar stays on the interior routes and off the
homepage; every crop is recorded, checksummed and never drawn above its own pixels (record, CSS caps
and browser measurement agree); thumbnails are small recorded images; the interior pages collect nothing and load nothing third-party;
and /sources/ keeps every source, credit line, reference DOI and the unchanged MIT licence text.

Same discipline as scripts/negative_tests_mer240.py: each case mutates one real file, runs the site
validator, and restores the original in a `finally` block. A case counts as CAUGHT only when the
validator fails with the expected text on an ERROR line the unmutated baseline did not already print.
The run ends by proving the restored tree validates identically.
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(".").resolve()
INDEX = ROOT / "index.html"
SOLUTIONS = ROOT / "solutions" / "index.html"
GEOTHERMAL = ROOT / "solutions" / "geothermal" / "index.html"
ABOUT = ROOT / "about" / "index.html"
PARTNER = ROOT / "partner" / "index.html"
SOURCES_PAGE = ROOT / "sources" / "index.html"
TR_SOURCES = ROOT / "tr" / "kaynaklar" / "index.html"
SCRIPT = ROOT / "script.js"
STYLES = ROOT / "styles.css"
MANIFEST = ROOT / "assets" / "imagery" / "sources.json"
RIGHTS = ROOT / "IMAGERY_RIGHTS.md"
VALIDATOR = "scripts/validate_site.py"

CASES = []


def case(name, path, mutate, expect):
    CASES.append((name, path, mutate, expect))


def site():
    r = subprocess.run([sys.executable, VALIDATOR], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def swap(old, new, every=False):
    def mutate(t):
        assert old in t, "mutation source not present: " + old[:80]
        return t.replace(old, new) if every else t.replace(old, new, 1)
    return mutate


def regex(pattern, new):
    def mutate(t):
        out, n = re.subn(pattern, new, t, count=1, flags=re.S)
        assert n == 1, "pattern not found: " + pattern[:80]
        return out
    return mutate


def as_json(edit):
    def mutate(t):
        data = json.loads(t)
        edit(data)
        return json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    return mutate


def crop(data, cid):
    return next(c for c in data["web_m6"]["interior_crops"] if c["id"] == cid)


# ---- one grammar, five openings ---------------------------------------------------------------
case("the homepage takes the interior grammar", INDEX,
     swap('<body class="home">', '<body class="home interior">'), "carries <body class=\"interior\">")
case("an interior page loses the interior grammar", GEOTHERMAL,
     swap('<body class="interior page-geothermal">', '<body class="page-geothermal">'), "lacks <body class=\"interior\">")
case("two pages open with the same composition", PARTNER,
     swap('class="page-hero is-split ground-orbit"', 'class="page-hero is-register ground-orbit"'), "expected 'is-split'")

# ---- the crops: recorded, checksummed, honest -----------------------------------------------------
case("a crop derivative loses its checksum", MANIFEST,
     as_json(lambda d: crop(d, "kizildere-stage")["derivatives"][0].update(sha256="0" * 64)),
     "does not match its recorded SHA-256 / size")
case("a crop's parent master changes", MANIFEST,
     as_json(lambda d: crop(d, "kizildere-aoi")["parent"].update(sha256="0" * 64)),
     "parent does not match its recorded SHA-256")
case("a crop stops recording that nothing is upscaled", MANIFEST,
     as_json(lambda d: crop(d, "kizildere-terrain").update(operations_not_used=["tone or colour change"])),
     "must record that no upscaling is used")
case("a crop's analysis-grid overlap is misstated", MANIFEST,
     as_json(lambda d: crop(d, "kizildere-valley").update(analysis_grid_overlap_px2=0)),
     "records an analysis-grid overlap")
case("a crop's measured upscale exceeds the bound", MANIFEST,
     as_json(lambda d: crop(d, "kizildere-stage")["rendered"].update(max_upscale_factor=1.45)),
     "the bound is")
case("a crop's recorded width exceeds its pixels", MANIFEST,
     as_json(lambda d: crop(d, "kizildere-terrain")["rendered"].update(max_css_width=1200)),
     "above its 1459 px widest candidate")
case("a crop's record claims a candidate it does not ship", MANIFEST,
     as_json(lambda d: crop(d, "kizildere-aoi")["rendered"].update(widest_candidate_px=2400)),
     "claims a 2400 px candidate")
case("a crop is shown full size on a second page", PARTNER,
     swap("  </main>",
          '    <section class="page-section"><img data-lead-visual src="/assets/imagery/kizildere-terrain-984f936e-1000.webp" '
          'alt="" data-i18n-alt="alt.terrain" width="1000" height="615" /></section>\n  </main>'),
     "recorded for 'about' alone")
case("the About figure is allowed to grow past its crop", STYLES,
     swap(".wide-figure{position:relative;width:100%;max-width:728px;", ".wide-figure{position:relative;width:100%;max-width:900px;"),
     "is capped at 900 CSS px")
case("the Partner figure is allowed to grow past its crop", STYLES,
     swap(".split-figure{position:relative;width:100%;max-width:500px;", ".split-figure{position:relative;width:100%;max-width:640px;"),
     "is capped at 640 CSS px")
case("the Geothermal stage can be drawn taller than its crop allows", STYLES,
     swap("min-height:clamp(460px,38vw,550px)", "min-height:clamp(460px,38vw,640px)"),
     "the stage hero can draw its crop")

# ---- captions: the coordinates on an image name ground the image shows (review B3) ---------------------------
case("the About crop is captioned with the pilot point again", SCRIPT,
     swap("'scene.terrain.coords': '38.0936° N, 29.2483° E',", "'scene.terrain.coords': '37.9794° N, 28.7907° E',"),
     "outside its crop box")
case("the Partner caption names the pilot place and point again", PARTNER,
     swap('data-i18n="scene.valley.place">South-west of the Kızıldere pilot area, Türkiye</span><span data-i18n="scene.valley.coords">37.8744° N, 28.5695° E</span>',
          'data-i18n="scene.context.place">Kızıldere — Büyük Menderes graben, Denizli, Türkiye</span><span data-i18n="scene.context.coords">37.9794° N, 28.7907° E</span>'),
     "is captioned with")
case("a crop's recorded label point drifts from its caption", MANIFEST,
     as_json(lambda d: crop(d, "kizildere-terrain")["label_point"].update(lat=38.5)),
     "records label_point")
case("a crop loses its label point", MANIFEST,
     as_json(lambda d: crop(d, "kizildere-valley").pop("label_point")),
     "records no caption keys or no label_point")
case("the Turkish caption coordinate drifts from the English one", SCRIPT,
     swap("'scene.valley.coords': '37.8744° K, 28.5695° D',", "'scene.valley.coords': '37.8744° K, 28.5700° D',"),
     "names different coordinates in en and tr")

# ---- the expansion-direction figures are captioned photographs, not cards (review decision 2) ---------------
case("an expansion-direction figure gets a frame again", STYLES,
     swap(".panel-figure{position:relative;margin:0;aspect-ratio:16/10;overflow:hidden;background:var(--ground)}",
          ".panel-figure{position:relative;margin:0;aspect-ratio:16/10;overflow:hidden;background:var(--ground);border:1px solid var(--rule)}"),
     "captioned photographs, not cards")
case("an expansion-direction panel gains a shadow", STYLES,
     swap(".domain-panel{position:relative;display:flex;", ".domain-panel{box-shadow:0 8px 24px #000;position:relative;display:flex;"),
     "captioned photographs, not cards")
case("an expansion-direction panel becomes a link", SOLUTIONS,
     swap('<span class="anchor-alias" id="mineral" aria-hidden="true"></span>',
          '<span class="anchor-alias" id="mineral" aria-hidden="true"></span><a href="/solutions/geothermal/">More</a>'),
     "carry a link")

# ---- thumbnails ----------------------------------------------------------------------------------------
case("a thumbnail is declared larger than 160 CSS px", SOURCES_PAGE,
     swap('width="160" height="90"', 'width="240" height="135"'), "at most 160 x 160 CSS px")
case("a thumbnail is not a recorded image", SOURCES_PAGE,
     swap('src="/assets/imagery/yellowstone-2013-900.webp" alt="Thumbnail of the Yellowstone',
          'src="/assets/brand/orbgss-logo-dark.9085b960.svg" alt="Thumbnail of the Yellowstone'),
     "is not a recorded image in sources.json")
case("a thumbnail stops being lazy", SOURCES_PAGE,
     swap('width="160" height="90" loading="lazy"', 'width="160" height="90"'), "must be loaded lazily")
case("the thumbnail rule stops capping its width", STYLES,
     swap(".thumb{width:160px;", ".thumb{width:320px;"), "does not cap thumbnails")

# ---- Geothermal: the MER-255 diagram, ruler and "no governed raster" cases are retired ------------------------
# MER-276 (Atlas, A1 and A6) replaced the schematic layer diagram, the neutral ruler and the rule that no governed
# raster reaches the page. The cases that guard what replaced them (the six plates, the four MER-151 layers, the
# legend and scale bar, the warnings) are in scripts/negative_tests_atlas_geothermal.py.

# ---- nothing collected, nothing third-party ------------------------------------------------------------------
case("a form appears on Partner", PARTNER,
     swap("  </main>", '    <form action="/send" method="post"><input name="email" /></form>\n  </main>'),
     "the interior pages collect nothing")
case("a third-party script loads on About", ABOUT,
     swap('<script src="/script.js" defer></script>',
          '<script src="/script.js" defer></script><script src="https://analytics.example.com/a.js"></script>'),
     "the only script is /script.js")
case("an interior page links over plain http", SOLUTIONS,
     swap("  </main>", '    <p><a href="http://example.com/">x</a></p>\n  </main>'), "over plain http")

# ---- About: a note, not a register --------------------------------------------------------------------------------
case("the About trust note loses its link to the sources page", ABOUT,
     swap('<p class="chapter-link"><a class="text-link" href="/sources/">', '<p class="chapter-link"><a class="text-link" href="/solutions/">'),
     "must remain as the short trust note")
case("the About trust note becomes a register again", ABOUT,
     swap('<ul class="source-names mono lead-set" data-lead-visual>',
          '<dl class="source-names mono lead-set" data-lead-visual><dt>Landsat</dt><dd>USGS</dd></dl><ul class="source-names mono lead-set">'),
     "became a register again")

# ---- /sources/: every source, credit, reference and licence -----------------------------------------------------------
case("a source record is dropped", SOURCES_PAGE,
     regex(r'\s*<article class="source-record" id="src-scm">.*?</article>', ""), "may not be dropped from the credits")
case("a source loses its official link", SOURCES_PAGE,
     swap('href="https://dataspace.copernicus.eu/"', 'href="https://example.com/"'), "does not link its official page")
case("a credit line loses its required wording", SCRIPT,
     swap("'sourcesPage.landsat.credit': 'Landsat data courtesy of the U.S. Geological Survey.'",
          "'sourcesPage.landsat.credit': 'Landsat data from the USGS.'"),
     "credit line lost its required wording")
case("a reference DOI is dropped", SOURCES_PAGE,
     swap('href="https://doi.org/10.1038/s41467-020-19160-7"', 'href="https://example.com/crameri"'),
     "no longer lists the reference")
case("an external link loses rel=noopener", SOURCES_PAGE,
     swap('href="https://www.naturalearthdata.com/" target="_blank" rel="noopener"', 'href="https://www.naturalearthdata.com/" target="_blank"'),
     "must open with target=_blank rel=noopener")
case("a source loses its terms entry", SOURCES_PAGE,
     swap('<li id="terms-naturalearth">', "<li>"), "has no terms entry")
case("an image credit names no source", SOURCES_PAGE,
     regex(r'(<li class="credit-row">\s*<img class="thumb" src="/assets/imagery/chuquicamata-2024-900.webp".*?)<p class="credit-sources">.*?</p>', r"\1"),
     "an image credit on /sources/ names no source record")
case("the sources index points at a missing section", SOURCES_PAGE,
     swap('<a href="#references" data-i18n="sourcesPage.index.references">', '<a href="#papers" data-i18n="sourcesPage.index.references">'),
     "the /sources/ index links")
case("the English MIT text is shortened", SCRIPT,
     swap("shall be included in all copies or substantial portions of the Software.", "shall be included in all copies of the Software.", every=False),
     "the 'en' MIT licence text")
case("the Turkish MIT text is translated", SCRIPT,
     regex(r"(\n  tr: \{.*?'sourcesPage\.mit\.warranty': 'THE SOFTWARE IS PROVIDED )\"AS IS\"", r'\1"OLDUĞU GİBİ"'),
     "the 'tr' MIT licence text")
case("the licence copyright notice is malformed", SCRIPT,
     swap("'sourcesPage.mit.copyright': 'Copyright (c) Fabio Crameri',", "'sourcesPage.mit.copyright': 'Copyright Fabio Crameri',", every=True),
     "copyright notice is")
case("a copyright year appears on the page without a verified source", SCRIPT,
     swap("'sourcesPage.mit.copyright': 'Copyright (c) Fabio Crameri',", "'sourcesPage.mit.copyright': 'Copyright (c) 2023, Fabio Crameri',", every=True),
     "the licence record publishes")
case("the licence record publishes a year it never verified", MANIFEST,
     as_json(lambda d: d["web_m6"]["licence_notices"]["scientific-colour-maps-v8.0"].update(
         copyright_line_published="Copyright (c) 2023, Fabio Crameri")),
     "a copyright year is published without a verified source")
case("the licence record is removed", MANIFEST,
     as_json(lambda d: d["web_m6"].pop("licence_notices")),
     "is missing licence")
case("the MIT text takes typographic quotes", SCRIPT,
     swap('(the "Software")', "(the “Software”)"),
     "the 'en' MIT licence text")
case("the footer attribution loses the Sentinel credit", SCRIPT,
     swap("'footer.attribution': 'Landsat data courtesy of the U.S. Geological Survey. Contains modified Copernicus Sentinel data (2025).',",
          "'footer.attribution': 'Landsat data courtesy of the U.S. Geological Survey.',"),
     "footer attribution lost")
case("the licence block is removed", SOURCES_PAGE,
     regex(r'\s*<article class="licence-block" id="licence-scm">.*?</article>', ""), "licence block is missing")
case("IMAGERY_RIGHTS.md stops recording a crop", RIGHTS,
     swap("kizildere-valley", "kizildere-v", every=True), "does not record the interior crop")


def main() -> int:
    print("MER-255 negative tests — interior redesign, crops, Geothermal honesty and the sources page\n")
    rc, baseline = site()
    if rc != 0:
        print("baseline tree does not validate; refusing to run")
        print(baseline)
        return 1

    def failed_with(text, blob):
        return any(text.lower() in ln.lower() for ln in blob.splitlines() if ln.startswith("ERROR"))

    results = []
    for name, path, mutate, expect in CASES:
        original = path.read_bytes().decode("utf-8")
        try:
            crlf = "\r\n" in original
            text = original.replace("\r\n", "\n")
            mutated = mutate(text)
            assert mutated != text, "mutation was a no-op: " + name
            if crlf:
                mutated = mutated.replace("\n", "\r\n")
            path.write_bytes(mutated.encode("utf-8"))
            rc, out = site()
            caught = rc != 0 and failed_with(expect, out) and not failed_with(expect, baseline)
            results.append(caught)
            print(f"  {'CAUGHT ' if caught else 'MISSED '} {name} (exit {rc})")
            if not caught:
                print("     expected text: " + repr(expect))
                for line in out.splitlines():
                    if line.startswith("ERROR"):
                        print("     " + line[:170])
        finally:
            path.write_bytes(original.encode("utf-8"))
    print()
    print(f"{sum(results)}/{len(results)} deliberate regressions caught")
    rc, out = site()
    print(f"Restored tree: site exit {rc} — {'PASS' if rc == 0 else 'FAIL'} — "
          f"{'identical to baseline' if out == baseline else 'DIFFERS FROM BASELINE'}")
    return 0 if all(results) and rc == 0 and out == baseline else 1


if __name__ == "__main__":
    raise SystemExit(main())
