"""MER-241 browser acceptance: the static Turkish pages, in a real browser.

    python3 evidence/mer241/tools/check_mer241.py <repo root> [--quick]

Playwright + the container's Chromium (PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers) against
evidence/mer241/tools/vercel_like_server.py, which serves the repository the way the Vercel project
does (clean URLs, trailing slash, the 301s, the .vercelignore allowlist, a real 404 for unknown
paths). Local QA tooling only. Writes evidence/mer241/browser_report.json and the WebP screenshots.

What it proves
  sweep       every page, EN and TR, 10 widths (375-3840 CSS px) x DPR 1 and 2 (3 on phones): no
              horizontal overflow, no broken image, no console error, no failed request, the right
              <html lang>, and the header the same height in both languages (no wrapped Turkish labels);
  no-JS       with JavaScript off each page is complete in its own language and the EN | TR links
              navigate to the twin and back;
  preference  a leftover 'orbgss.lang' in localStorage no longer changes the language, and is removed;
  menu        the mobile menu button is labelled in the page's language, and relabels on open;
  hero        the Turkish homepage loads the same hero media as the English one (root-absolute URLs,
              nothing under /tr/assets/), every request answered 200 or 206;
  404         unknown paths, under /tr/ too, answer 404 with the page in both languages;
  shots       desktop 1440 and phone 390 screenshots of every page in both languages.
"""
from __future__ import annotations

import io
import json
import pathlib
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(sys.argv[1]).resolve()
QUICK = "--quick" in sys.argv
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from vercel_like_server import serve  # noqa: E402

OUT = ROOT / "evidence" / "mer241"
EN = ["/", "/solutions/", "/solutions/geothermal/", "/about/", "/partner/"]
TR = ["/tr/", "/tr/cozumler/", "/tr/cozumler/jeotermal/", "/tr/hakkimizda/", "/tr/is-birligi/"]
TWIN = dict(zip(EN, TR)) | dict(zip(TR, EN))
SLUG = {"/": "home", "/solutions/": "solutions", "/solutions/geothermal/": "geothermal",
        "/about/": "about", "/partner/": "partner"}
WIDTHS = [375, 390, 414, 768, 1024, 1280, 1440, 1920, 2560, 3840]
if QUICK:
    WIDTHS = [375, 768, 1440, 3840]
H1 = {"/": "OrbGSS", "/tr/": "OrbGSS"}  # the homepage h1 is checked for presence only

report: dict = {"sweep": {"loads": 0, "failures": []}, "no_js": [], "preference": [], "menu": [],
                "hero": {}, "not_found": [], "screenshots": [], "header_height": {}}
problems: list[str] = []


def check(ok: bool, message: str) -> None:
    if not ok:
        problems.append(message)
        print("  FAIL", message)


def new_context(browser, width, dpr=1, mobile=False, reduced=True, js=True):
    return browser.new_context(
        viewport={"width": width, "height": 900}, device_scale_factor=dpr, is_mobile=mobile,
        has_touch=mobile, java_script_enabled=js,
        reduced_motion="reduce" if reduced else "no-preference")


def load(page, url, settle=0.4):
    page.goto(url, wait_until="load")
    page.evaluate("""async()=>{const h=document.documentElement.scrollHeight;
      for(let y=0;y<h+900;y+=700){scrollTo({top:y,behavior:'instant'});await new Promise(r=>setTimeout(r,30))}
      scrollTo({top:0,behavior:'instant'});
      await Promise.race([Promise.all([...document.images].filter(i=>!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r}))),new Promise(r=>setTimeout(r,6000))]);}""")
    page.wait_for_timeout(int(settle * 1000))


def to_webp(png: bytes, path: pathlib.Path) -> None:
    image = Image.open(io.BytesIO(png)).convert("RGB")
    if image.height > 16000:  # WebP's hard limit is 16383 px
        image = image.crop((0, 0, image.width, 16000))
    image.save(path, "WEBP", quality=70, method=4)


srv = serve(ROOT)
with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium",
                                 args=["--no-sandbox", "--autoplay-policy=no-user-gesture-required"])
    try:
        # ---------------------------------------------------------------- sweep
        for url in EN + TR:
            for dpr in (1, 2, 3):
                for width in WIDTHS:
                    if dpr == 3 and width > 768:
                        continue
                    ctx = new_context(browser, width, dpr, mobile=width < 768)
                    page = ctx.new_page()
                    errors, bad = [], []
                    page.on("console", lambda m, e=errors: m.type == "error" and e.append(m.text))
                    page.on("pageerror", lambda x, e=errors: e.append(str(x)))
                    page.on("response", lambda r, b=bad: r.status >= 400 and b.append((r.url, r.status)))
                    load(page, srv.base + url)
                    r = page.evaluate("""()=>({ox: document.documentElement.scrollWidth - innerWidth,
                      broken: [...document.images].filter(i=>i.complete && i.naturalWidth===0 && i.currentSrc).length,
                      lang: document.documentElement.lang,
                      header: Math.round(document.querySelector('.site-header').getBoundingClientRect().height),
                      h1: (document.querySelector('h1')||{}).textContent})""")
                    report["sweep"]["loads"] += 1
                    want_lang = "tr" if url in TR else "en"
                    row = {"page": url, "width": width, "dpr": dpr, **r, "errors": errors, "bad": bad}
                    if r["ox"] > 0 or r["broken"] or errors or bad or r["lang"] != want_lang:
                        report["sweep"]["failures"].append(row)
                        print("  FAIL sweep", row)
                    report["header_height"][f"{url}@{width}x{dpr}"] = r["header"]
                    ctx.close()
        check(not report["sweep"]["failures"], f"{len(report['sweep']['failures'])} sweep failures")
        # Turkish labels must not wrap the header: same height as the English twin at every width.
        for en_url, tr_url in zip(EN, TR):
            for dpr in (1, 2, 3):
                for width in WIDTHS:
                    a = report["header_height"].get(f"{en_url}@{width}x{dpr}")
                    b = report["header_height"].get(f"{tr_url}@{width}x{dpr}")
                    if a is not None and b is not None:
                        check(a == b, f"header height differs EN {a} vs TR {b} at {width}px x{dpr} ({tr_url})")

        # ---------------------------------------------------------------- no JavaScript
        ctx = new_context(browser, 1280, js=False)
        page = ctx.new_page()
        for en_url, tr_url in zip(EN, TR):
            row = {"en": en_url, "tr": tr_url}
            page.goto(srv.base + en_url)
            row["en_lang"] = page.get_attribute("html", "lang")
            tr_link = page.locator('.lang-switch a[hreflang="tr"]')
            en_title = page.title()
            tr_link.click()
            page.wait_for_load_state("load")
            row["after_click"] = page.url.replace(srv.base, "")
            row["tr_lang"] = page.get_attribute("html", "lang")
            row["tr_title"] = page.title()
            row["tr_h1"] = page.inner_text("h1")
            row["tr_nav"] = page.inner_text(".nav-list").split()
            row["tr_hreflang"] = page.eval_on_selector_all(
                'link[rel="alternate"]', "els => els.map(e => [e.hreflang, e.href])")
            check(row["after_click"] == tr_url, f"no-JS: EN switch on {en_url} went to {row['after_click']}")
            check(row["en_lang"] == "en" and row["tr_lang"] == "tr", f"no-JS: lang on {en_url} / {tr_url}")
            check(row["tr_title"] != en_title, f"no-JS: {tr_url} title is the English title")
            page.locator('.lang-switch a[hreflang="en"]').click()
            page.wait_for_load_state("load")
            row["back"] = page.url.replace(srv.base, "")
            check(row["back"] == en_url, f"no-JS: TR switch on {tr_url} went to {row['back']}")
            report["no_js"].append(row)
        ctx.close()

        # ---------------------------------------------------------------- stored preference retired
        for stored, url, want in (("tr", "/about/", "en"), ("tr", "/", "en"), ("en", "/tr/hakkimizda/", "tr")):
            ctx = new_context(browser, 1280)
            ctx.add_init_script(f"try{{localStorage.setItem('orbgss.lang','{stored}')}}catch(e){{}}")
            page = ctx.new_page()
            page.goto(srv.base + url)
            page.wait_for_timeout(500)
            got = {"stored": stored, "page": url, "lang": page.get_attribute("html", "lang"),
                   "h1": page.inner_text("h1"),
                   "left_in_storage": page.evaluate("localStorage.getItem('orbgss.lang')")}
            report["preference"].append(got)
            check(got["lang"] == want, f"preference: {url} with stored {stored} shows lang {got['lang']}")
            check(got["left_in_storage"] is None, f"preference: 'orbgss.lang' still in storage on {url}")
            ctx.close()

        # ---------------------------------------------------------------- mobile menu label
        for url, closed, opened in (("/about/", "Open navigation", "Close navigation"),
                                    ("/tr/hakkimizda/", "Menüyü aç", "Menüyü kapat")):
            ctx = new_context(browser, 390, 2, mobile=True)
            page = ctx.new_page()
            page.goto(srv.base + url)
            before = page.get_attribute(".menu-toggle", "aria-label")
            page.click(".menu-toggle")
            after = page.get_attribute(".menu-toggle", "aria-label")
            switch_visible = page.locator('.lang-switch a[hreflang="tr"]').is_visible()
            report["menu"].append({"page": url, "closed": before, "open": after, "switch_visible": switch_visible})
            check((before, after) == (closed, opened), f"menu: {url} labels {before!r}/{after!r}")
            check(switch_visible, f"menu: the EN | TR switch is not reachable in the open menu on {url}")
            ctx.close()

        # ---------------------------------------------------------------- hero media on /tr/
        loads = {}
        for url in ("/", "/tr/"):
            ctx = new_context(browser, 1440, 1, reduced=False)
            # The container reports a 1.45 Mbit/s downlink, which script.js reads as a slow network
            # and answers with the held still; an emulated fast connection exercises the video path.
            ctx.add_init_script("Object.defineProperty(navigator,'connection',{configurable:true,"
                                "value:{effectiveType:'4g',downlink:10,saveData:false}})")
            page = ctx.new_page()
            seen = []
            page.on("response", lambda r, s=seen: s.append((r.url.replace(srv.base, ""), r.status)))
            page.goto(srv.base + url, wait_until="load")
            page.wait_for_timeout(7000)
            state = page.evaluate("({state: hero.dataset.heroState, tier: hero.dataset.heroTier, "
                                  "codec: hero.dataset.heroCodec, reason: hero.dataset.heroReason || null})"
                                  .replace("hero.", "document.getElementById('hero')."))
            media = sorted({u for u, _ in seen if u.startswith("/assets/hero/") and u.endswith((".webm", ".mp4"))})
            bad = [(u, s) for u, s in seen if s >= 400]
            nested = [u for u, _ in seen if u.startswith("/tr/assets/") or u.startswith("/tr/styles") or u.startswith("/tr/script")]
            loads[url] = {"hero_media": media, "state": state, "bad": bad, "nested": nested,
                          "assets": sorted({u for u, _ in seen if u.startswith("/assets/")})}
            ctx.close()
        report["hero"] = {u: {k: v for k, v in d.items() if k != "assets"} for u, d in loads.items()}
        check(not loads["/tr/"]["bad"] and not loads["/tr/"]["nested"], f"hero: /tr/ requests {loads['/tr/']['bad']} {loads['/tr/']['nested']}")
        check(bool(loads["/tr/"]["hero_media"]), "hero: no hero video was requested on /tr/")
        check(loads["/tr/"]["hero_media"] == loads["/"]["hero_media"], "hero: /tr/ chose different hero media than /")
        check(loads["/tr/"]["state"] == loads["/"]["state"] and loads["/tr/"]["state"]["tier"],
              f"hero: /tr/ ended in {loads['/tr/']['state']}, / in {loads['/']['state']}")
        report["hero"]["same_asset_requests"] = loads["/"]["assets"] == loads["/tr/"]["assets"]

        # ---------------------------------------------------------------- 404 in both languages
        ctx = new_context(browser, 1280)
        page = ctx.new_page()
        for url in ("/no-such-page/", "/tr/yok/", "/tr/cozumler/yok/", "/STATUS.md", "/tr/index.html.bak"):
            resp = page.goto(srv.base + url)
            row = {"url": url, "status": resp.status, "h1": page.inner_text("h1"),
                   "tr_line": page.inner_text('p[lang="tr"]'),
                   "links": page.eval_on_selector_all(".not-found-links a", "els => els.map(e => e.getAttribute('href'))")}
            report["not_found"].append(row)
            check(resp.status == 404, f"404: {url} answered {resp.status}")
            check(row["links"] == ["/", "/tr/"], f"404: {url} links {row['links']}")
            check("ilgi alanının" in row["tr_line"], f"404: {url} lost its Turkish line")
        ctx.close()

        # ---------------------------------------------------------------- screenshots
        shots = [("desktop-1440", 1440, 1, False), ("mobile-390", 390, 2, True)]
        for tag, width, dpr, mobile in shots:
            ctx = new_context(browser, width, dpr, mobile=mobile)
            page = ctx.new_page()
            for url in EN + TR + ["/no-such-page/"]:
                lang = "tr" if url in TR else "en"
                name = "404" if url == "/no-such-page/" else SLUG.get(url) or SLUG[TWIN[url]]
                load(page, srv.base + url)
                path = OUT / f"{name}-{tag}-{lang}.webp"
                to_webp(page.screenshot(full_page=True), path)
                report["screenshots"].append(path.name)
            ctx.close()
    finally:
        browser.close()
        srv.close()

OUT.mkdir(parents=True, exist_ok=True)
report["problems"] = problems
(OUT / "browser_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({"loads": report["sweep"]["loads"], "sweep_failures": len(report["sweep"]["failures"]),
                  "no_js_pages": len(report["no_js"]), "problems": problems}, indent=1, ensure_ascii=False))
sys.exit(1 if problems else 0)
