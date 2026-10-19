#!/usr/bin/env python3
"""Real-browser QA of the MER-255 interior pages (local tooling; Playwright + Chromium, never deployed).

    python3 evidence/mer255/qa_browser.py http://127.0.0.1:8102 [out.json]

The base URL must serve the working tree with Vercel's cleanUrls / trailingSlash behaviour
(scripts/measure_interior_renders.py contains a minimal server). For every interior route in English and
Turkish and 11 viewports (360 to 2560 CSS px, DPR 1 and 2 on phones) it reports: horizontal overflow,
console / page errors, failed or 4xx requests, broken images after a scroll-through, layout shift (CLS),
heading structure, missing alt attributes, and text contrast on opaque backgrounds. Internal links and
in-page anchors are resolved once per route. Text drawn over a photograph is not computed here; it is
listed as "over image" and was judged on the screenshots.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/")
OUT = sys.argv[2] if len(sys.argv) > 2 else None
ROUTES = {
    "en": {"solutions": "/solutions/", "geothermal": "/solutions/geothermal/", "about": "/about/",
           "partner": "/partner/", "sources": "/sources/"},
    "tr": {"solutions": "/tr/cozumler/", "geothermal": "/tr/cozumler/jeotermal/", "about": "/tr/hakkimizda/",
           "partner": "/tr/is-birligi/", "sources": "/tr/kaynaklar/"},
}
VIEWS = [(360, 740, 2), (390, 844, 2), (414, 896, 2), (600, 1000, 1), (768, 1024, 1), (834, 1112, 1),
         (1024, 768, 1), (1280, 800, 1), (1440, 900, 1), (1920, 1080, 1), (2560, 1440, 1)]

CONTRAST_JS = r"""
() => {
  const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(s => parseFloat(s)); return {r:p[0], g:p[1], b:p[2], a: p.length > 3 ? p[3] : 1}; };
  const lin = v => { v /= 255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); };
  const lum = c => 0.2126*lin(c.r) + 0.7152*lin(c.g) + 0.0722*lin(c.b);
  const over = (f, b) => ({r: f.r*f.a + b.r*(1-f.a), g: f.g*f.a + b.g*(1-f.a), b: f.b*f.a + b.b*(1-f.a), a: 1});
  const fails = [], skipped = {n: 0}; let checked = 0;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  while (walker.nextNode()) {
    const node = walker.currentNode; if (!node.nodeValue.trim()) continue;
    const el = node.parentElement; if (!el || seen.has(el)) continue; seen.add(el);
    if (el.closest('script,style,noscript,[aria-hidden="true"]')) continue;
    const cs = getComputedStyle(el); const r = el.getBoundingClientRect();
    if (cs.visibility === 'hidden' || cs.display === 'none' || r.width === 0 || r.height === 0) continue;
    // background: first opaque ancestor background; any image / gradient on the way means "over image"
    let bg = null, overImage = false, opacity = 1, a = el;
    while (a && a !== document.documentElement) {
      const s = getComputedStyle(a); opacity *= parseFloat(s.opacity);
      if (s.backgroundImage && s.backgroundImage !== 'none') { overImage = true; }
      if (!bg) { const c = parse(s.backgroundColor); if (c && c.a > 0) { bg = c.a < 1 ? {c, partial: true} : {c}; } }
      if (bg && !bg.partial) break;
      a = a.parentElement;
    }
    if (el.closest('.scene-label, .stage-shade, .page-hero.is-stage, .domain-band, .wide-figure, .split-figure, .aoi-figure, .locator-figure')) overImage = true;
    if (overImage) { skipped.n++; continue; }
    const base = parse(getComputedStyle(document.body).backgroundColor) || {r:3,g:11,b:18,a:1};
    let back = bg ? (bg.partial ? over(bg.c, base) : bg.c) : base;
    let fg = parse(cs.color); if (!fg) continue; fg.a *= opacity; fg = over(fg, back);
    const L1 = lum(fg), L2 = lum(back); const ratio = (Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
    const size = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight) >= 700;
    const large = size >= 24 || (size >= 18.66 && bold); const need = large ? 3 : 4.5;
    checked++;
    if (ratio < need) fails.push({text: node.nodeValue.trim().slice(0,50), ratio: +ratio.toFixed(2), need, size, cls: (el.className||'').toString().slice(0,40)});
  }
  return {checked, skippedOverImage: skipped.n, fails};
}
"""

HEADINGS_JS = r"""
() => {
  const hs = [...document.querySelectorAll('main h1, main h2, main h3, main h4')].map(h => +h.tagName[1]);
  const issues = [];
  if (hs.filter(x => x === 1).length !== 1) issues.push('h1 count ' + hs.filter(x => x === 1).length);
  for (let i = 1; i < hs.length; i++) if (hs[i] - hs[i-1] > 1) issues.push(`heading jumps h${hs[i-1]} -> h${hs[i]}`);
  const noAlt = [...document.images].filter(i => !i.hasAttribute('alt')).map(i => i.getAttribute('src'));
  if (noAlt.length) issues.push('img without alt: ' + noAlt.join(','));
  const emptyLinks = [...document.querySelectorAll('a[href]')].filter(a => !(a.textContent.trim() || a.getAttribute('aria-label') || a.querySelector('img[alt]:not([alt=""])'))).map(a => a.getAttribute('href'));
  if (emptyLinks.length) issues.push('links without a name: ' + emptyLinks.join(','));
  if (!document.documentElement.lang) issues.push('no lang');
  if (!document.title.trim()) issues.push('no title');
  if (!document.querySelector('meta[name="description"]')) issues.push('no meta description');
  if (!document.querySelector('main#main')) issues.push('no main#main');
  return issues;
}
"""


def fetch(url):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # noqa: BLE001
        return 0, str(e)


def check_links(route_url, html, cache):
    problems = []
    for href in sorted(set(re.findall(r'(?<![-\w])href="([^"#][^"]*|#[^"]+)"', html))):
        if href.startswith(("mailto:", "http://", "https://", "tel:")):
            if href.startswith("http://"):
                problems.append(f"plain http link {href}")
            continue
        target = urllib.parse.urljoin(BASE + route_url, href)
        path, _, frag = target.partition("#")
        if path not in cache:
            cache[path] = fetch(path)
        status, body = cache[path]
        if status != 200:
            problems.append(f"{href} -> {status}")
        elif frag and not path.endswith((".css", ".js")) and f'id="{frag}"' not in body:
            problems.append(f"{href} -> no id={frag}")
    return problems


def main():
    results, bad = [], 0
    link_cache = {}
    with sync_playwright() as pw:
        exe = "/opt/pw-browsers/chromium" if os.path.exists("/opt/pw-browsers/chromium") else None
        browser = pw.chromium.launch(args=["--no-sandbox"], **({"executable_path": exe} if exe else {}))
        for lang, routes in ROUTES.items():
            for name, url in routes.items():
                status, html = fetch(BASE + url)
                links = check_links(url, html, link_cache)
                for w, h, dpr in VIEWS:
                    ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr,
                                              is_mobile=w < 600, has_touch=w < 1000)
                    page = ctx.new_page()
                    errors, failed = [], []
                    page.on("console", lambda m, e=errors: e.append(m.text) if m.type == "error" else None)
                    page.on("pageerror", lambda e_, e=errors: e.append(str(e_)))
                    page.on("response", lambda r, f=failed: f.append(f"{r.status} {r.url}") if r.status >= 400 else None)
                    page.on("requestfailed", lambda r, f=failed: f.append(f"failed {r.url}"))
                    page.add_init_script("""window.__cls = 0; new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({type:'layout-shift', buffered:true});""")
                    page.goto(BASE + url, wait_until="load")
                    page.add_style_tag(content="html{scroll-behavior:auto!important}")
                    total = page.evaluate("document.documentElement.scrollHeight")
                    y = 0
                    while y < total:
                        page.evaluate(f"window.scrollTo(0,{y})")
                        page.wait_for_timeout(60)
                        y += int(h * 0.8)
                        total = page.evaluate("document.documentElement.scrollHeight")
                    page.wait_for_function("[...document.images].every(i => i.complete)", timeout=20000)
                    page.evaluate("window.scrollTo(0,0)")
                    row = {
                        "lang": lang, "page": name, "viewport": f"{w}x{h}@{dpr}",
                        "overflow_x": page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth"),
                        "broken_images": page.evaluate("[...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src'))"),
                        "cls": round(page.evaluate("window.__cls"), 4),
                        "errors": errors, "bad_responses": failed,
                    }
                    if (w, h, dpr) in ((390, 844, 2), (1440, 900, 1)):
                        row["structure"] = page.evaluate(HEADINGS_JS)
                        contrast = page.evaluate(CONTRAST_JS)
                        row["contrast"] = {"checked": contrast["checked"], "over_image_skipped": contrast["skippedOverImage"],
                                           "fails": contrast["fails"]}
                        row["links"] = links
                    ok = (row["overflow_x"] <= 0 and not row["broken_images"] and not errors and not failed
                          and row["cls"] < 0.02 and not row.get("structure") and not row.get("links")
                          and not row.get("contrast", {}).get("fails"))
                    row["ok"] = ok
                    bad += 0 if ok else 1
                    results.append(row)
                    if not ok:
                        print("FAIL", json.dumps(row, ensure_ascii=False)[:600])
                    ctx.close()
        browser.close()
    summary = {"combinations": len(results), "failing": bad,
               "max_cls": max(r["cls"] for r in results), "max_overflow_x": max(r["overflow_x"] for r in results)}
    print(json.dumps(summary))
    if OUT:
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump({"summary": summary, "results": results}, fh, ensure_ascii=False, indent=1)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
