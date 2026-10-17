"""Deliberately break each MER-240 / Milestone 6 invariant and confirm validate_site.py catches it.

    py -3.14 scripts/negative_tests_mer240.py

MER-240 rebuilt the site to the approved information architecture
(docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md): Home / Solutions (Geothermal, Mining, Marine) / About /
Partner with us, with /platform/, /pilot/, /company/ and /contact/ answering with 301 redirects.
The contract worth guarding: the navigation and footer are the same on every page and mark the
current one; the retired routes stay retired and redirected; old /pilot/ fragments still land; the
homepage keeps its light trim; and the reworked pages obey the content rules — one home per fact
(R1), one full-size appearance per visual (R2), no software detail (R3), a lead visual first in
every section (R4), the text budgets in both languages (R5) and one status vocabulary (R8). The
locator map is recorded and captioned, and the conversation types live on /partner/ alone.

Same discipline as scripts/negative_tests_mer237.py: each case mutates one real file (or creates
one), runs the site validator, and restores the original in a `finally` block. A case counts as
CAUGHT only when the validator fails with the expected text on an ERROR line the unmutated baseline
did not already print. The run ends by proving the restored tree validates identically.
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
SCRIPT = ROOT / "script.js"
STYLES = ROOT / "styles.css"
VERCEL = ROOT / "vercel.json"
SITEMAP = ROOT / "sitemap.xml"
SOURCES = ROOT / "assets" / "imagery" / "sources.json"
VALIDATOR = "scripts/validate_site.py"

CASES = []


def case(name, path, mutate, expect):
    CASES.append((name, path, mutate, expect))


def site():
    r = subprocess.run([sys.executable, VALIDATOR], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def swap(old, new):
    def mutate(t):
        assert old in t, "mutation source not present: " + old[:80]
        return t.replace(old, new, 1)
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


def scene(data, sid):
    return next(s for s in data["scenes"] if s["id"] == sid)


LONG = " ".join(["extra"] * 40)

# ---- navigation and footer, on every page ------------------------------------------------------
case("About and Solutions swap places in the primary navigation", ABOUT,
     regex(r'(<li class="has-menu">.*?</li>\s*</ul>\s*</div>\s*</li>)(\s*)(<li><a href="/about/"[^\n]*</li>)',
           r"\3\2\1"),
     "primary navigation is")
case("a retired route returns to the navigation", PARTNER,
     swap('<li><a href="/about/" data-i18n="nav.about">About</a></li>',
          '<li><a href="/about/" data-i18n="nav.about">About</a></li><li><a href="/" data-i18n="nav.pilot">Pilot</a></li>'),
     "primary navigation is")
case("a page marks the wrong item as current", ABOUT,
     swap('data-i18n="nav.partner">Partner with us</a></li>',
          'data-i18n="nav.partner" aria-current="page">Partner with us</a></li>'),
     "as the current page")
case("the Geothermal page stops marking itself in the menu", GEOTHERMAL,
     swap('data-i18n="nav.geothermal" aria-current="page">', 'data-i18n="nav.geothermal">'),
     "as the current page")
case("the footer loses About", PARTNER,
     swap('<a href="/about/" data-i18n="nav.about">About</a>\n        <a href="/partner/"',
          '<a href="/partner/"'),
     "footer navigation is")
case("the footer attribution loses its link to the sources table", GEOTHERMAL,
     swap(' <a href="/about/#sources" data-i18n="footer.sources">Every source is listed on the About page.</a>', ""),
     "does not end with the link to /about/#sources")
case("the Turkish Partner label drifts", SCRIPT,
     swap("'nav.partner': 'İş Birliği',", "'nav.partner': 'Bize Ulaşın',"),
     "'nav.partner' in the 'tr' dictionary")

# ---- redirects and retired routes --------------------------------------------------------------
case("a retired route loses its redirect", VERCEL,
     as_json(lambda d: d["redirects"].pop(1)),
     "vercel.json redirects are")
case("a redirect becomes a 308 (permanent: true)", VERCEL,
     as_json(lambda d: d["redirects"][0].update(permanent=True)),
     "must carry statusCode 301")
case("a redirect points at a page that does not exist", VERCEL,
     as_json(lambda d: d["redirects"][1].update(destination="/geothermal/")),
     "not a canonical route")
case("a retired route directory comes back", ROOT / "pilot" / "index.html",
     lambda t: "<!doctype html><title>Pilot</title>\n",
     "pilot/ still exists")
case("the sitemap lists a retired route", SITEMAP,
     swap("</urlset>", "  <url>\n    <loc>https://orbgss.com/pilot/</loc>\n    <lastmod>2026-10-17</lastmod>\n  </url>\n</urlset>"),
     "which is not a canonical route")
case("a sitemap entry loses its date", SITEMAP,
     regex(r"(<loc>https://orbgss.com/about/</loc>)\s*<lastmod>[^<]+</lastmod>", r"\1"),
     "<lastmod>")
case("an old /pilot/ fragment stops landing", GEOTHERMAL,
     swap('<span class="anchor-alias" id="pilot-structure" aria-hidden="true"></span>', ""),
     "no #pilot-structure")
case("an old /pilot/ fragment lands at the top: its container is not positioned", STYLES,
     swap(".page-section{position:relative;", ".page-section{"),
     "which styles.css does not position")

# ---- the homepage's light trim (authority 4.1) ---------------------------------------------------
case("the Company section returns to the homepage", INDEX,
     swap('<div id="contact" class="sec sec-contact">',
          '<section id="company" class="sec"><h2>Company</h2></section>\n    <div id="contact" class="sec sec-contact">'),
     "#company is back")
case("the hero's Partner call becomes a mailto again", INDEX,
     swap('<a class="text-link" href="/partner/"><span data-i18n="hero.secondary">',
          '<a class="text-link" href="mailto:contact@orbgss.com"><span data-i18n="hero.secondary">'),
     "carries a mailto: link")
case("the Partner line grows a second link", INDEX,
     regex(r'(<div id="contact" class="sec sec-contact">\s*<div class="shell">)',
           r'\1<a href="/about/">About</a>'),
     "#contact must be the one Partner line")
case("the Act 3 deep link goes back to the build story", INDEX,
     swap('href="/solutions/geothermal/#layers"', 'href="/solutions/geothermal/"'),
     "must point to /solutions/geothermal/#layers")
case("a homepage card regains its description sentence", INDEX,
     swap('<h3 id="domain-mining-title" data-i18n="domain.mining.title">Mining</h3>',
          '<h3 id="domain-mining-title" data-i18n="domain.mining.title">Mining</h3><p>Mineral targets.</p>'),
     "carries more than its name and status")

# ---- R8 one status vocabulary --------------------------------------------------------------------
case("a homepage card says In development again", INDEX,
     swap('<p class="domain-status mono" data-i18n="app.mining.status">Expansion direction</p>',
          '<p class="domain-status mono" data-i18n="domain.mining.status">In development</p>'),
     "R8:")
case("the Turkish Marine status drifts", SCRIPT,
     regex(r"(\n  tr: \{.*?'app\.marine\.status': )'Genişleme yönü'", r"\1'Geliştirme aşamasında'"),
     "R8: 'app.marine.status' in the 'tr' dictionary")

# ---- R4 show first --------------------------------------------------------------------------------
case("a paragraph opens a section before its table", GEOTHERMAL,
     swap('<table class="data-table" aria-labelledby="outputs-title" data-lead-visual>',
          '<p>Here is what the pilot produced.</p><table class="data-table" aria-labelledby="outputs-title" data-lead-visual>'),
     "opens with <p>")
case("a section loses its lead visual", ABOUT,
     swap('<table class="data-table" aria-labelledby="sources-title" data-lead-visual>',
          '<table class="data-table" aria-labelledby="sources-title">'),
     "not a marked lead")
case("text sits in <main> outside a section", PARTNER,
     swap("  </main>", '    <div class="intro-text"><p>Write to us.</p></div>\n  </main>'),
     "outside a section")
case("a paragraph is passed off as the lead visual", PARTNER,
     swap('<p class="mail-address mono" data-lead-visual>', '<p class="mono" data-lead-visual>'),
     "marks <p> as its lead visual")

# ---- R5 text budgets -------------------------------------------------------------------------------
case("a headline runs past eight words", SOLUTIONS,
     swap(">Where OrbGSS works today, and where next.</h1>",
          ">Where OrbGSS works today, and where it is going next year.</h1>"),
     "R5: solutions/index.html: headline")
case("the page intro runs past thirty words", GEOTHERMAL,
     swap("and what is still missing.</p>", "and what is still missing, " + " ".join(["more"] * 12) + ".</p>"),
     "the page intro is")
case("a section body runs past forty words", GEOTHERMAL,
     swap("structure and geology are optional support and score-invariant.</p>",
          "structure and geology are optional support and score-invariant. " + " ".join(["more"] * 12) + ".</p>"),
     "body is")
case("a table cell runs past twelve words", PARTNER,
     swap(">A partnership or collaboration with OrbGSS.</td>",
          ">A partnership or collaboration with OrbGSS, on any ground, in any country, at any scale.</td>"),
     "R5: partner/index.html: table cell")
case("a table grows past seven rows", GEOTHERMAL,
     swap("<tr><th scope=\"row\" data-i18n=\"geothermalPage.output.area\">",
          "<tr><th scope=\"row\">One</th><td>Row</td></tr><tr><th scope=\"row\">Two</th><td>Row</td></tr>"
          "<tr><th scope=\"row\" data-i18n=\"geothermalPage.output.area\">"),
     "a table has 8 rows")
case("only the Turkish copy runs past the budget", SCRIPT,
     swap("Boşluk doldurulmaz, gösterilir ve önceliği değiştirmez: yapı ve jeoloji isteğe bağlı destektir, skoru etkilemez.",
          "Boşluk doldurulmaz, gösterilir ve önceliği değiştirmez: yapı ve jeoloji isteğe bağlı destektir, skoru etkilemez. "
          + " ".join(["ek"] * 24) + "."),
     "in tr (at most")
case("a page runs past its total budget", ABOUT,
     regex(r'(</section>\s*)(<div class="page-closing">)',
           r"\1" + "".join(
               f'<section class="page-section"><div class="shell"><table class="data-table" data-lead-visual><tbody>'
               f'<tr><th scope="row">Row {i}</th><td>{" ".join(["word"] * 10)}</td><td>{" ".join(["word"] * 10)}</td></tr>'
               f'</tbody></table></div></section>\n    ' for i in range(6)) + r"\2"),
     "budgeted words")

# ---- R1 one home per fact ---------------------------------------------------------------------------
case("the company sentence is repeated on Partner", PARTNER,
     swap('<p class="mail-address mono" data-lead-visual><a href="mailto:contact@orbgss.com">contact@orbgss.com</a></p>',
          '<p class="mail-address mono" data-lead-visual><a href="mailto:contact@orbgss.com">contact@orbgss.com</a></p>'
          "<p>OrbGSS is a geospatial-intelligence platform built by VirgaSoft.</p>"),
     "R1:")
case("a principle is restated on the Geothermal page", GEOTHERMAL,
     swap("structure and geology are optional support and score-invariant.</p>",
          "structure and geology are optional support and score-invariant. A missing layer is published as missing, never invented.</p>"),
     "R1: 'a missing layer is published as missing, never invented'")

# ---- R2 one full-size appearance per visual ------------------------------------------------------------
case("a hub photograph is shown full size on another page", GEOTHERMAL,
     swap("  </main>", '    <section class="page-section"><img data-lead-visual src="/assets/imagery/yellowstone-2013-1400.webp" alt="" data-i18n-alt="alt.yellowstone" /></section>\n  </main>'),
     "R2: scene:yellowstone-2013 appears at full size")

# ---- R3 no software detail ----------------------------------------------------------------------------------
case("the About page talks about the workflow", ABOUT,
     swap(">Priorities come from mapped layers, not an unexplained model output.</td>",
          ">Priorities come from the mapped-layer workflow, not a model output.</td>"),
     "mentions 'workflow'")
case("a layer code reaches the Geothermal page", GEOTHERMAL,
     swap(">Landsat thermal bands</td>", ">Landsat thermal bands (THM-01)</td>"),
     "mentions 'thm-01'")

# ---- V1 the locator map ----------------------------------------------------------------------------------
case("the locator map record loses its checksum", SOURCES,
     as_json(lambda d: d["web_m6"]["locator_map"].update(sha256="0" * 64)),
     "does not match its recorded SHA-256")
case("the locator map loses the kind line of its caption", GEOTHERMAL,
     swap('<span class="scene-kind" data-i18n="scene.kind.locator">Locator map — Natural Earth</span>', ""),
     "must carry the bottom-right caption")
case("the locator map is shown on another page", ABOUT,
     regex(r'(<section class="page-section" id="principles"[^>]*>\s*<div class="shell">)',
           r'\1<img src="/assets/maps/kizildere-locator-23c85f44.svg" alt="" data-i18n-alt="alt.locator" width="1200" height="574" />'),
     "its home is the Geothermal page")

# ---- Partner with us is the one home of the conversations -----------------------------------------------
case("a conversation link loses its translated subject", PARTNER,
     swap(' data-i18n-href="mail.technical"', ""),
     "the conversation table's mail links")
case("another page starts a conversation itself", ABOUT,
     swap('<a href="#sources">', '<a href="mailto:contact@orbgss.com">'),
     "conversations start on /partner/")

# ---- the hub bands (illustrative photographs, contained) -----------------------------------------------------
case("a hub band loses its placement record", SOURCES,
     as_json(lambda d: scene(d, "chuquicamata-2024").pop("web_m6_placement")),
     "without a placed web_m6_placement")
case("a hub band is laid out wider than its pixels allow", SOURCES,
     as_json(lambda d: scene(d, "ili-delta-2020")["web_m6_placement"]["rendered"].update(max_css_width=1800)),
     "above its widest 2880 px candidate")
case("the hub loses the illustrative footnote", SOLUTIONS,
     regex(r'\s*<div class="page-note">.*?</div>\s*</div>', ""),
     "framing key 'domains.illustrative' is not rendered there")


def main() -> int:
    print("MER-240 negative tests — Milestone 6 pages, navigation, redirects and content rules\n")
    rc, baseline = site()
    if rc != 0:
        print("baseline tree does not validate; refusing to run")
        print(baseline)
        return 1

    def failed_with(text, blob):
        return any(text.lower() in ln.lower() for ln in blob.splitlines() if ln.startswith("ERROR"))

    results = []
    for name, path, mutate, expect in CASES:
        existed = path.exists()
        original = path.read_bytes().decode("utf-8") if existed else ""
        created_dir = None if path.parent.exists() else path.parent
        try:
            # The cases are written against LF text. A checkout may hold CRLF (Windows,
            # core.autocrlf), so mutate the LF form and write the file's own line ending back.
            crlf = "\r\n" in original
            text = original.replace("\r\n", "\n")
            mutated = mutate(text)
            assert mutated != text, "mutation was a no-op: " + name
            if crlf:
                mutated = mutated.replace("\n", "\r\n")
            path.parent.mkdir(parents=True, exist_ok=True)
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
            if existed:
                path.write_bytes(original.encode("utf-8"))
            else:
                path.unlink(missing_ok=True)
                if created_dir is not None:
                    created_dir.rmdir()
    print()
    print(f"{sum(results)}/{len(results)} deliberate regressions caught")
    rc, out = site()
    print(f"Restored tree: site exit {rc} — {'PASS' if rc == 0 else 'FAIL'} — "
          f"{'identical to baseline' if out == baseline else 'DIFFERS FROM BASELINE'}")
    return 0 if all(results) and rc == 0 and out == baseline else 1


if __name__ == "__main__":
    raise SystemExit(main())
