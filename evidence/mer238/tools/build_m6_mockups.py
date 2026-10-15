"""Generate the MER-238 mockups into docs/mockups/m6/ from the live site's markup, styles and copy."""
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
OUT = ROOT / "docs" / "mockups" / "m6"

BANNER = ('<p class="m6-banner">MER-238 mockup — a proposal for review, not the implementation. '
          'English only; the Turkish pages come in MER-241.</p>')

NAV = """
  <header class="site-header" id="top">
    <a href="/docs/mockups/m6/home.html" class="brand" aria-label="OrbGSS home">
      <span class="brand-wordmark">Orb<span>GSS</span></span>
    </a>
    <button class="menu-toggle" type="button" aria-label="Open navigation" aria-controls="primary-nav" aria-expanded="false">
      <span></span><span></span>
    </button>
    <nav class="main-nav" id="primary-nav" aria-label="Primary navigation">
      <ul class="nav-list">
        <li><a href="/docs/mockups/m6/home.html"{cur_home}>Home</a></li>
        <li class="has-menu">
          <button class="nav-trigger" type="button" aria-expanded="false" aria-controls="solutions-menu"{cur_sol}>
            <span>Solutions</span><span class="chevron" aria-hidden="true"></span>
          </button>
          <div class="submenu" id="solutions-menu">
            <ul>
              <li><a href="/docs/mockups/m6/geothermal.html">Geothermal</a></li>
              <li><a href="/docs/mockups/m6/solutions.html#mining">Mining</a></li>
              <li><a href="/docs/mockups/m6/solutions.html#marine">Marine</a></li>
            </ul>
          </div>
        </li>
        <li><a href="/docs/mockups/m6/about.html"{cur_about}>About</a></li>
        <li><a href="/docs/mockups/m6/partner.html"{cur_partner}>Partner with us</a></li>
      </ul>
      <div class="lang-switch" role="group" aria-label="Language">
        <button class="lang-btn" type="button" lang="en" aria-pressed="true">EN</button>
        <span class="lang-sep" aria-hidden="true">|</span>
        <button class="lang-btn" type="button" lang="tr" aria-pressed="false">TR</button>
      </div>
    </nav>
  </header>
"""

FOOTER = """
  <footer class="site-footer">
    <div class="footer-brand">
      <img src="/assets/logo.svg" alt="OrbGSS — Orbital Geo-Spatial Solutions" width="420" height="120" />
      <span>Built by VirgaSoft</span>
    </div>
    <div class="footer-right">
      <nav aria-label="Footer navigation">
        <a href="/docs/mockups/m6/home.html">Home</a>
        <a href="/docs/mockups/m6/solutions.html">Solutions</a>
        <a href="/docs/mockups/m6/about.html">About</a>
        <a href="/docs/mockups/m6/partner.html">Partner with us</a>
      </nav>
      <p class="attribution">Landsat data courtesy of the U.S. Geological Survey. The hero is a rendered orbital sequence whose Earth texture is NASA Blue Marble with ground detail from modified Copernicus Sentinel-2 data (2025). The story panels are OrbGSS cartographic exports of the Kızıldere pilot area, derived from NASADEM elevation, Landsat thermal and Sentinel-2 alteration evidence, with Scientific colour maps v8.0 by Fabio Crameri. <a href="/docs/mockups/m6/about.html#sources">Every source is listed on the About page.</a></p>
      <p>© 2026 OrbGSS. All rights reserved.</p>
    </div>
  </footer>
"""

KIZ = ('<figcaption class="scene-label"><span>Kızıldere — Büyük Menderes graben, Denizli, Türkiye</span>'
       '<span>37.9794° N, 28.7907° E</span><span class="scene-kind">{kind}</span></figcaption>')

W = {
    "context": "Earth-observation context only. This is a natural-colour photographic composite of the area, not analytical evidence, not a scored input, and not the acquisition date of any evidence layer.",
    "terrain": "Context and display only. Terrain is not a scored predictor and carries no universal geothermal-favourability direction.",
    "thermal": "Evidence layer only. Do not describe it as geothermal probability, reserve, discovery, or drilling-success evidence.",
    "alteration": "Broad Sentinel-2 spectral alteration proxy; not mineral identification and not proof of hydrothermal alteration.",
    "priority": "AOI-relative experimental screening only. Not probability, reserve/resource estimation, discovery likelihood, drilling-success likelihood, Full Prospectivity, or a calibrated cross-AOI score.",
    "firstapp": "First-application proof, not field validation, discovery, reserve or resource, drilling-target or drilling-success proof.",
    "structure": "Structure and geology are optional support and score-invariant. Their absence does not change the remote-sensing priority baseline.",
}


def page(title, body, current):
    cur = {k: "" for k in ("cur_home", "cur_sol", "cur_about", "cur_partner")}
    cur[current] = ' aria-current="page"'
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="robots" content="noindex" />
  <title>{title} — MER-238 mockup</title>
  <link rel="icon" href="/assets/mark.svg" type="image/svg+xml" />
  <link rel="stylesheet" href="/styles.css" />
  <link rel="stylesheet" href="/docs/mockups/m6/mockup.css" />
</head>
<body>
  {BANNER}
{NAV.format(**cur)}
  <main id="main">
{body}
  </main>
{FOOTER}
</body>
</html>
"""


def header(kicker, h1, intro, extra=""):
    return f"""    <section class="page-hero">
      <div class="page-hero-inner">
        <p class="kicker mono">{kicker}</p>
        <h1>{h1}</h1>
        <p class="page-hero-copy">{intro}</p>{extra}
      </div>
    </section>"""


def section(head_title, head_copy, inner, deep=False, sid=None, aliases=()):
    alias = "".join(f'<span class="anchor-alias" id="{a}" aria-hidden="true"></span>' for a in aliases)
    sid_attr = f' id="{sid}"' if sid else ""
    copy = f"<p>{head_copy}</p>" if head_copy else ""
    return f"""    <section class="m6-section{' is-deep' if deep else ''}"{sid_attr}>{alias}
      <div class="m6-shell">
        <div class="m6-head"><h2>{head_title}</h2>{copy}</div>
{inner}
      </div>
    </section>"""


# ---- /solutions/ ---------------------------------------------------------------------------------
def band(sid, img, srcset, title, status, active, place, coords, link="", aliases=()):
    alias = "".join(f'<span class="anchor-alias" id="{a}" aria-hidden="true"></span>' for a in aliases)
    link_html = (f'<a class="text-link" href="{link[0]}"><span>{link[1]}</span> <span aria-hidden="true">→</span></a>'
                 if link else "")
    return f"""    <section class="m6-band" id="{sid}">{alias}
      <img src="{img}" srcset="{srcset}" sizes="100vw" alt="" loading="lazy" decoding="async" />
      <div class="m6-band-copy">
        <h2>{title}</h2>
        <p class="domain-status mono{' is-active' if active else ''}">{status}</p>
        {link_html}
      </div>
      <p class="scene-label"><span>{place}</span><span>{coords}</span><span class="scene-kind">Natural-color composite</span></p>
    </section>"""


solutions = "\n".join([
    header("Solutions", "Where OrbGSS works today, and where next.",
           "Geothermal is active, with a published pilot. Mining and marine are expansion directions: nothing is published for them yet."),
    section("At a glance", "", """        <table class="m6-table">
          <thead><tr><th>Domain</th><th>Status</th><th>Ground it reads</th><th>Published today</th></tr></thead>
          <tbody>
            <tr><td>Geothermal</td><td class="mono is-active">Active · First application</td><td>Geothermal exploration ground</td><td><a href="/docs/mockups/m6/geothermal.html">The Kızıldere pilot →</a></td></tr>
            <tr><td>Mining</td><td class="mono">Expansion direction</td><td>Mineral exploration targets</td><td>Nothing yet</td></tr>
            <tr><td>Marine</td><td class="mono">Expansion direction</td><td>Coastal and marine ground</td><td>Nothing yet</td></tr>
          </tbody>
        </table>"""),
    band("geothermal", "/assets/imagery/yellowstone-2013-1800.webp",
         "/assets/imagery/yellowstone-2013-900.webp 900w, /assets/imagery/yellowstone-2013-1400.webp 1400w, /assets/imagery/yellowstone-2013-1800.webp 1800w, /assets/imagery/yellowstone-2013-2400.webp 2400w",
         "Geothermal", "Active · First application", True, "Yellowstone National Park, USA", "44.4604° N, 110.8282° W",
         ("/docs/mockups/m6/geothermal.html", "See the Kızıldere pilot")),
    band("mining", "/assets/imagery/chuquicamata-2024-1800.webp",
         "/assets/imagery/chuquicamata-2024-900.webp 900w, /assets/imagery/chuquicamata-2024-1400.webp 1400w, /assets/imagery/chuquicamata-2024-1800.webp 1800w",
         "Mining", "Expansion direction", False, "Chuquicamata, Antofagasta, Chile", "22.3150° S, 68.9010° W", aliases=("mineral",)),
    band("marine", "/assets/imagery/ili-delta-2020-1800.webp",
         "/assets/imagery/ili-delta-2020-900.webp 900w, /assets/imagery/ili-delta-2020-1400.webp 1400w, /assets/imagery/ili-delta-2020-1800.webp 1800w",
         "Marine", "Expansion direction", False, "Ili River Delta &amp; Lake Balkhash, Kazakhstan", "45.0600° N, 74.5200° E",
         aliases=("environment",)),
    """    <section class="m6-section">
      <div class="m6-shell">
        <p class="m6-flag">V4 — a coastal scene replaces the inland Ili Delta in MER-240</p>
        <p class="act-footnote domains-note"><span class="mono">Illustrative</span> <span>The three photographs above are public-domain Landsat scenes of other places, chosen to show the kind of ground each domain reads. They are not OrbGSS analytical outputs, not results, and not the Kızıldere pilot area.</span></p>
      </div>
    </section>""",
])

# ---- /solutions/geothermal/ ----------------------------------------------------------------------
layer_rows = [
    ("/assets/imagery/kizildere-aoi-context-2025-natural-800.webp", "Natural colour", "Landsat 8 OLI, 2025-05-05", "Context", W["context"]),
    ("/assets/proof/web005b/terrain-600-d.webp", "Elevation", "NASADEM", "Context", W["terrain"]),
    ("/assets/proof/web005b/thm01-600.webp", "Thermal anomaly", "Landsat thermal bands", "Evidence", W["thermal"]),
    ("/assets/proof/web005b/alt01-600.webp", "Alteration signal", "Sentinel-2", "Evidence", W["alteration"]),
    ("/assets/proof/final/alt02-800.webp", "Second alteration signal (iron)", "Sentinel-2", "Evidence", W["alteration"]),
    ("/assets/proof/web005b/priority-600.webp", "Priority", "The evidence layers", "Score", W["priority"]),
]
rows = "\n".join(
    f'            <tr><td class="m6-thumb-cell"><img class="m6-thumb" src="{src}" alt="" loading="lazy" /></td>'
    f'<td class="is-key">{name}</td><td>{frm}</td><td class="mono">{role}</td><td class="is-warning">{warn}</td></tr>'
    for src, name, frm, role, warn in layer_rows)

geothermal = "\n".join([
    header("Geothermal · Active · First application", "Kızıldere: the first published pilot.",
           "Everything published for the pilot, in one place: where it is, which layers it holds, what each layer is not, and what is still missing.",
           """
        <div class="m6-locator" style="margin-top:36px"><span>V1 locator map placeholder — Türkiye outline from Natural Earth (public domain), Denizli and the 36 × 36 km area of interest. Built in MER-240.</span><i class="m6-aoi"></i></div>"""),
    section("The pilot at a glance", "", """        <table class="m6-table is-facts">
          <tbody>
            <tr><td>Area</td><td>36 × 36 km</td></tr>
            <tr><td>Place</td><td>Büyük Menderes graben, Denizli, Türkiye</td></tr>
            <tr><td>Centre</td><td>37.9794° N, 28.7907° E</td></tr>
            <tr><td>Grid</td><td>30 m, EPSG:32635, 1,200 × 1,200 cells</td></tr>
            <tr><td>Layers</td><td>2 context, 3 evidence, 1 priority surface</td></tr>
            <tr><td>Score</td><td>Remote-Sensing Relative Priority — Experimental Baseline, 0–100 within the area</td></tr>
            <tr><td>Not available</td><td>Structure and geology</td></tr>
          </tbody>
        </table>""", sid="glance", aliases=("pilot-observe",)),
    section("Every layer, and what it is not", "", f"""        <table class="m6-table">
          <thead><tr><th></th><th>Layer</th><th>From</th><th>Role</th><th>What it is not</th></tr></thead>
          <tbody>
{rows}
          </tbody>
        </table>""", deep=True, sid="layers", aliases=("pilot-terrain", "pilot-evidence")),
    section("Priority over relief", "", f"""        <div class="m6-split">
          <figure class="m6-figure">
            <img src="/assets/proof/geothermal-1400.webp" alt="Relative priority surface over shaded NASADEM relief across the Kızıldere area of interest" loading="lazy" />
            {KIZ.format(kind="Remote-Sensing Relative Priority — Experimental Baseline")}
          </figure>
          <div class="m6-copy">
            <p class="m6-flag">D1 — interim WEB-002 composite (report palette)</p>
            <p>The priority surface read over NASADEM relief, so ranked ground can be seen against the valleys and ridges it sits on.</p>
            <div class="m6-legend"><span>0</span><img src="/assets/proof/geothermal-scale.png" alt="" /><span>100</span></div>
            <p class="beam-note">{W["firstapp"]} {W["priority"]}</p>
          </div>
        </div>""", sid="relief", aliases=("pilot-priority", "pilot-geothermal")),
    section("The second alteration signal", "", f"""        <div class="m6-split">
          <figure class="m6-figure">
            <img src="/assets/proof/final/alt02-800.webp" alt="Iron alteration proxy map of the Kızıldere area of interest" loading="lazy" />
            {KIZ.format(kind="ALT-02 Alteration Proxy — ferric/iron")}
          </figure>
          <div class="m6-copy">
            <p class="m6-flag">D1 — interim GEO-WEB-002 export (report palette)</p>
            <p>A second Sentinel-2 proxy, sensitive to iron-bearing surfaces, mapped on the same frame.</p>
            <div class="m6-legend"><img src="/assets/proof/final/alt02-legend.png" alt="" style="width:240px;height:auto" /></div>
            <p class="beam-note">{W["alteration"]}</p>
          </div>
        </div>""", deep=True, sid="iron"),
    section("What the pilot produced", "", """        <table class="m6-table">
          <thead><tr><th>Output</th><th>What it is</th></tr></thead>
          <tbody>
            <tr><td>Area definition</td><td>One boundary, grid and projection for every layer</td></tr>
            <tr><td>Context layers</td><td>Natural colour and elevation, for orientation only</td></tr>
            <tr><td>Evidence layers</td><td>Mapped remote-sensing signals, each with its limits</td></tr>
            <tr><td>Data-gap statement</td><td>What is missing, stated instead of filled</td></tr>
            <tr><td>Priority surface</td><td>One within-area ranking, 0 to 100</td></tr>
            <tr><td>Provenance record</td><td>The source and export behind every visual</td></tr>
          </tbody>
        </table>""", sid="outputs"),
    section("Not available: structure and geology", "", f"""        <div class="m6-split">
          <div class="m6-gap"><p>No public-safe fault or lithology layer</p></div>
          <div class="m6-copy">
            <p>No public-safe fault or lithology layer is authorized for this pilot. The gap is shown, not filled, and it does not change the priority: structure and geology are optional support and score-invariant.</p>
            <p class="beam-note">{W["structure"]}</p>
          </div>
        </div>""", deep=True, sid="gap", aliases=("pilot-structure",)),
    """    <section class="m6-closing"><a class="text-link" href="/docs/mockups/m6/partner.html"><span>Discuss a pilot</span> <span aria-hidden="true">→</span></a></section>""",
])

# ---- /about/ -------------------------------------------------------------------------------------
principles = [
    ("Evidence-backed screening", "Priorities come from mapped layers, not an unexplained model output.", ("/docs/mockups/m6/home.html#evidence", "The three layers")),
    ("Traceable provenance", "Every published visual maps back to a source and a recorded export.", ("#sources", "Data sources")),
    ("Explicit data gaps", "A missing layer is published as missing, never invented.", ("/docs/mockups/m6/geothermal.html#gap", "Structure and geology")),
    ("AOI-first analysis", "One declared area, projection and grid before any interpretation.", ("/docs/mockups/m6/geothermal.html#glance", "The pilot at a glance")),
    ("Remote narrowing", "Large areas are ordered from orbit before field time is committed.", ("/docs/mockups/m6/home.html#priority", "Where to look first")),
    ("Decision support", "Helps decide where to investigate; field investigation remains necessary.", None),
]
prow = "\n".join(
    f'            <tr><td>{t}</td><td>{c}</td><td>{f"<a href={chr(34)}{l[0]}{chr(34)}>{l[1]} →</a>" if l else "—"}</td></tr>'
    for t, c, l in principles)
about = "\n".join([
    header("About", "OrbGSS — Orbital Geo-Spatial Solutions",
           "OrbGSS is a geospatial-intelligence platform built by VirgaSoft. It exists to make exploration and land decisions evidence-based, traceable and easier to prioritize.",
           '\n        <p class="company-parent mono">Built by VirgaSoft</p>'),
    section("How OrbGSS publishes", "", f"""        <table class="m6-table">
          <thead><tr><th>Principle</th><th>What it means</th><th>See it</th></tr></thead>
          <tbody>
{prow}
          </tbody>
        </table>
        <p class="m6-foot">No accuracy, performance, deployment, customer or scale figures are published for this baseline.</p>""",
            sid="principles"),
    section("Data and imagery sources", "", """        <table class="m6-table">
          <thead><tr><th>Source</th><th>Used for</th><th>Credit</th></tr></thead>
          <tbody>
            <tr><td>Landsat 8 (USGS)</td><td>Natural colour, thermal evidence, domain photographs</td><td>Courtesy of the U.S. Geological Survey; public domain</td></tr>
            <tr><td>NASADEM (NASA)</td><td>Elevation and relief</td><td>NASA Earthdata</td></tr>
            <tr><td>Copernicus Sentinel-2</td><td>Alteration evidence; hero ground detail</td><td>Contains modified Copernicus Sentinel data (2025)</td></tr>
            <tr><td>NASA Blue Marble</td><td>The rendered hero's Earth texture</td><td>NASA; public domain</td></tr>
            <tr><td>Scientific colour maps v8.0</td><td>Map palettes</td><td>Fabio Crameri; MIT</td></tr>
          </tbody>
        </table>
        <p class="m6-foot">Wording follows IMAGERY_RIGHTS.md exactly in MER-240.</p>""", deep=True, sid="sources"),
    """    <section class="m6-closing"><a class="text-link" href="/docs/mockups/m6/partner.html"><span>Partner with us</span> <span aria-hidden="true">→</span></a></section>""",
])

# ---- /partner/ -----------------------------------------------------------------------------------
def mail(subject):
    return f"mailto:contact@orbgss.com?subject={subject.replace(' ', '%20')}"


partner = "\n".join([
    header("Partner with us", "Let’s talk about where to look next.",
           "OrbGSS is available for pilot, partnership and technical conversations. Reach out directly by email — there is no form to fill in."),
    section("Which conversation", "", f"""        <table class="m6-table">
          <thead><tr><th>Conversation</th><th>What it covers</th><th>Write</th></tr></thead>
          <tbody>
            <tr><td>Pilot</td><td>A geothermal pilot, or a first application in a new area.</td><td><a href="{mail('OrbGSS Pilot Inquiry')}">Write →</a></td></tr>
            <tr><td>Partnership</td><td>A partnership or collaboration with OrbGSS.</td><td><a href="{mail('OrbGSS Partnership Inquiry')}">Write →</a></td></tr>
            <tr><td>Technical</td><td>The evidence, its limits, or how a pilot would be scoped.</td><td><a href="{mail('OrbGSS Technical Inquiry')}">Write →</a></td></tr>
          </tbody>
        </table>"""),
    section("Direct", "", """        <p class="m6-address">contact@orbgss.com</p>
        <p class="m6-flag" style="margin-top:22px">Gate — the CTO confirms this mailbox receives mail before MER-240 ships</p>""",
            deep=True),
])

# ---- the homepage, from the real index.html --------------------------------------------------------
home = (ROOT / "index.html").read_text(encoding="utf-8")


def cut(text, start_pat, label):
    m = re.search(start_pat, text)
    assert m, label
    end = text.index("</section>", m.start()) + len("</section>")
    return text[:m.start()] + text[end:]


home = home.replace("<head>", '<head>\n  <base href="/" />\n  <meta name="robots" content="noindex" />', 1)
home = home.replace('<link rel="stylesheet" href="styles.css" />',
                    '<link rel="stylesheet" href="styles.css" />\n  <link rel="stylesheet" href="/docs/mockups/m6/mockup.css" />', 1)
assert "/docs/mockups/m6/mockup.css" in home, "stylesheet link"
home = re.sub(r"<header class=\"site-header\".*?</header>", NAV.format(cur_home=' aria-current="page"', cur_sol="", cur_about="", cur_partner="").strip(), home, count=1, flags=re.S)
home = re.sub(r"(<body[^>]*>)", r"\1\n  " + BANNER, home, count=1)
# hero partner call -> /partner/
home = home.replace('href="mailto:contact@orbgss.com?subject=OrbGSS%20Partnership%20Inquiry" data-i18n-href="mail.partner">',
                    'href="/docs/mockups/m6/partner.html">')
# solutions cards: image + name + status only, new targets, one status vocabulary
home = re.sub(r'\s*<p data-i18n="domain\.(geothermal|mining|marine)\.copy">[^<]*</p>', "", home)
home = home.replace('href="/solutions/#geothermal"', 'href="/docs/mockups/m6/geothermal.html"', 1)
home = home.replace('href="/solutions/#mining"', 'href="/docs/mockups/m6/solutions.html#mining"', 1)
home = home.replace('href="/solutions/#marine"', 'href="/docs/mockups/m6/solutions.html#marine"', 1)
home = home.replace('data-i18n="domain.mining.status">In development', 'data-i18n="app.mining.status">Expansion direction', 1)
home = home.replace('data-i18n="domain.marine.status">In development', 'data-i18n="app.marine.status">Expansion direction', 1)
# the two deep links into /pilot/ move to the Geothermal page
home = home.replace('href="/pilot/"><span data-i18n="act.evidence.deeper">How the layers are built',
                    'href="/docs/mockups/m6/geothermal.html#layers"><span>See every layer', 1)
home = home.replace('href="/pilot/"><span data-i18n="act.priority.deeper">Read the pilot method',
                    'href="/docs/mockups/m6/geothermal.html"><span>See the Kızıldere pilot', 1)
# Method and Company leave the homepage; Contact becomes one Partner line
home = cut(home, r'<section[^>]*id="proof"', "proof")
home = cut(home, r'<section[^>]*id="company"', "company")
m = re.search(r'<section[^>]*id="contact"', home)
assert m, "contact"
end = home.index("</section>", m.start()) + len("</section>")
home = home[:m.start()] + ('<section id="contact" class="m6-closing"><a class="text-link" href="/docs/mockups/m6/partner.html">'
                           '<span data-i18n="contact.cta">Partner With Us</span> <span aria-hidden="true">→</span></a></section>') + home[end:]
home = re.sub(r"<footer class=\"site-footer\">.*?</footer>", FOOTER.strip(), home, count=1, flags=re.S)
home = home.replace("<title>", "<title>Home — MER-238 mockup · ", 1)
import re as _re
left = _re.findall(r'href="(/platform/|/pilot/|/company/|/contact/|mailto:[^"]*)"', home)
assert not left, left

OUT.mkdir(parents=True, exist_ok=True)
for name, content in (("home.html", home),
                      ("solutions.html", page("Solutions", solutions, "cur_sol")),
                      ("geothermal.html", page("Geothermal", geothermal, "cur_sol")),
                      ("about.html", page("About", about, "cur_about")),
                      ("partner.html", page("Partner with us", partner, "cur_partner"))):
    (OUT / name).write_text(content, encoding="utf-8", newline="\n")
    print("wrote", (OUT / name).relative_to(ROOT), len(content))
