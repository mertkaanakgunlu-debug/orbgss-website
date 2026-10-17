"""MER-219 post-publication browser checks on production (headless Chrome over CDP). Read-only.

    py -3.14 evidence/mer219/browser_checks_production.py [--base https://orbgss.com]

Covers the MER-219 §5 step 5 items a headless browser can observe: hero tier/codec choice and
playback, the reduced-motion and no-JS held states, Act 03 layer switching, EN/TR, console errors,
broken images and horizontal overflow on every route at desktop and phone widths. No physical
Safari / Firefox / phone / 4K panel is exercised.
"""
import argparse
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "evidence" / "mer216" / "tools"))
from mer216_harness import Chrome  # noqa: E402

# MER-240 / Milestone 6 page set.
ROUTES = ["/", "/solutions/", "/solutions/geothermal/", "/about/", "/partner/"]
results = []


def check(ok, name, detail=""):
    results.append((bool(ok), name))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""), flush=True)


def errors_of(page):
    errs = [e["params"]["entry"]["text"] for e in page.events
            if e.get("method") == "Log.entryAdded" and e["params"]["entry"]["level"] == "error"]
    errs += [e["params"]["exceptionDetails"]["text"] for e in page.events if e.get("method") == "Runtime.exceptionThrown"]
    return errs


def settle(page, h):
    total = int(page.js("document.documentElement.scrollHeight"))
    for y in range(0, total + h, int(h * 0.8)):
        page.js(f"window.scrollTo({{top:{y},behavior:'instant'}})")
        page.pump(0.2)
    page.js("window.scrollTo({top:0,behavior:'instant'})")
    page.js("""Promise.race([Promise.all([...document.images].filter(i=>!i.complete)
        .map(i=>new Promise(r=>{i.onload=i.onerror=r}))), new Promise(r=>setTimeout(r,8000))])""")


def page_state(page):
    return page.js("""(()=>({
        overflow: document.documentElement.scrollWidth - innerWidth,
        broken: [...document.images].filter(i=>i.complete && i.naturalWidth===0 && i.currentSrc).map(i=>i.currentSrc),
        videoRequests: performance.getEntriesByType('resource').map(e=>e.name).filter(n=>/\\.(webm|mp4)(\\?|$)/.test(n)),
    }))()""")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://orbgss.com")
    base = ap.parse_args().base.rstrip("/")
    print(f"MER-219 production browser checks — {base}\n")
    chrome = Chrome()
    try:
        # 1. Every route, desktop and phone: console, broken images, overflow.
        for w, h, mobile in ((1440, 900, False), (390, 844, True)):
            for r in ROUTES:
                p = chrome.new_page()
                p.emulate(w, h, 1.0, mobile=mobile, reduced_motion=True)
                p.navigate(base + r)
                settle(p, h)
                p.pump(0.5)
                s = page_state(p)
                errs = errors_of(p)
                check(not errs and not s["broken"] and s["overflow"] <= 0,
                      f"{r} at {w}px: no console errors, broken images or overflow",
                      f"errors={len(errs)} broken={len(s['broken'])} overflow={s['overflow']}")
                p.close()

        # 2a. Hero on a fresh headless profile: Chrome's first downlink estimate (~1.5 Mbit/s) is
        # below the smallest tier's margin, so MER-216's network gate keeps the held still and
        # requests no video. That is the designed slow-link fallback, checked as such.
        p = chrome.new_page()
        p.emulate(1440, 900, 1.0, mobile=False, reduced_motion=False)
        p.navigate(base + "/")
        p.pump(6.0)
        hs = p.js("(()=>{const h=document.querySelector('[data-hero-state]');return h?{state:h.getAttribute('data-hero-state'),reason:h.dataset.heroReason,down:(navigator.connection||{}).downlink}:null})()")
        reqs0 = page_state(p)["videoRequests"]
        check(bool(hs) and (hs["state"] in ("playing", "held") or (hs["state"] == "static" and hs["reason"] and not reqs0)),
              "hero settles cleanly on the browser's own network estimate (plays, or held still with a reason and no video bytes)",
              json.dumps(hs))
        p.close()

        # 2b. Hero, motion allowed, a 50 Mbit/s link: one tier + codec chosen, playing, one source.
        p = chrome.new_page()
        p.send("Network.emulateNetworkConditions", {"offline": False, "latency": 20, "downloadThroughput": 50e6 / 8,
                                                    "uploadThroughput": 10e6 / 8, "connectionType": "wifi"})
        p.emulate(1440, 900, 1.0, mobile=False, reduced_motion=False)
        p.navigate(base + "/")
        p.pump(8.0)
        v = p.js("""(()=>{const v=document.querySelector('video');if(!v)return null;
            return {src:v.currentSrc, sources:v.querySelectorAll('source').length + (v.getAttribute('src')?1:0),
                    t:v.currentTime, paused:v.paused, ready:v.readyState, shown:getComputedStyle(v).opacity}})()""")
        reqs = page_state(p)["videoRequests"]
        check(bool(v) and v["src"] and "orbgss-hero-" in v["src"], "hero chose a ladder tier", (v or {}).get("src", "no video"))
        check(bool(v) and v["t"] > 0, "hero video advanced (playing or ended on the held frame)", json.dumps(v))
        check(len({r.split('?')[0] for r in reqs}) == 1, "exactly one hero media file requested", "; ".join(reqs))
        check(not errors_of(p), "no console errors with motion on")
        p.close()

        # 3. Reduced motion: no video bytes, held still shown.
        p = chrome.new_page()
        p.emulate(1440, 900, 1.0, mobile=False, reduced_motion=True)
        p.navigate(base + "/")
        p.pump(4.0)
        st = page_state(p)
        held = p.js("!!document.querySelector('.hero-held') && [...document.querySelectorAll('.hero-held')].some(i=>i.complete&&i.naturalWidth>0)")
        check(not st["videoRequests"] and held, "reduced motion: held still, no video requested", "; ".join(st["videoRequests"]))
        p.close()

        # 4. No JavaScript: the noscript held frame renders.
        p = chrome.new_page()
        p.send("Emulation.setScriptExecutionDisabled", {"value": True})
        p.emulate(1440, 900, 1.0, mobile=False, reduced_motion=False)
        p.navigate(base + "/")
        p.pump(3.0)
        n = p.send("Runtime.evaluate", {"expression": "document.images.length", "returnByValue": True})
        check(n.get("result", {}).get("value", 0) > 0, "no-JS: page renders images", str(n.get("result", {}).get("value")))
        p.close()

        # 5. Act 03 switching and EN/TR.
        p = chrome.new_page()
        p.emulate(1440, 900, 1.0, mobile=False, reduced_motion=True)
        p.navigate(base + "/")
        p.pump(2.0)
        radios = p.js("[...document.querySelectorAll('#evidence input[type=radio]')].map(r=>r.id||r.value)")
        switched = []
        for rid in radios or []:
            ok = p.js(f"""(()=>{{const r=document.getElementById({json.dumps(rid)})||[...document.querySelectorAll('#evidence input[type=radio]')].find(x=>x.value=={json.dumps(rid)});
                r.click(); return r.checked}})()""")
            switched.append(bool(ok))
        check(len(switched) == 3 and all(switched), "Act 03: all three layers can be selected", str(radios))
        # MER-241: the switch is two real links between static pages, not a script that rewrites text.
        before = p.js("document.documentElement.lang")
        p.js("document.querySelector('.lang-switch a[hreflang=tr]').click()")
        p.wait_load()
        p.pump(0.5)
        after = p.js("document.documentElement.lang")
        path = p.js("location.pathname")
        title = p.js("(document.querySelector('#context-title')||{}).textContent||''")
        check(before == "en" and after == "tr" and path == "/tr/" and title and "real area" not in title.lower(), "EN → TR switch opens the static Turkish page", f"{before}->{after} {path} '{title[:40]}'")
        p.js("document.querySelector('.lang-switch a[hreflang=en]').click()")
        p.wait_load()
        p.pump(0.5)
        check(p.js("location.pathname") == "/" and p.js("document.documentElement.lang") == "en", "TR → EN switch returns to the English page")
        p.close()
    finally:
        chrome.close()
    failed = [n for ok, n in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} browser checks passed")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
