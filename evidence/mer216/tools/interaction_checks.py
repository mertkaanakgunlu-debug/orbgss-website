#!/usr/bin/env python3
"""Interaction + navigation checks (EN/TR): evidence radios, inspection pairs and wipe, desktop nav, mobile menu."""
import json, sys, time
sys.path.insert(0, __file__.rsplit("\\", 1)[0])
from mer216_harness import Chrome, serve

CONN = "Object.defineProperty(navigator,'connection',{configurable:true,get:()=>({effectiveType:'4g',downlink:10,rtt:50,saveData:false,addEventListener(){},removeEventListener(){}})});"
RADIO = r"""
(async (id) => {
  const label = document.querySelector('label[for="'+id+'"]');
  label.scrollIntoView({block:'center', behavior:'instant'});
  await new Promise(r => setTimeout(r, 400));
  label.click();
  await new Promise(r => setTimeout(r, 800));
  const el = document.getElementById(id);
  const scope = el.closest('section') || document;
  const imgs = Array.from(scope.querySelectorAll('img')).filter(im => { const cs = getComputedStyle(im); const r = im.getBoundingClientRect();
    let p = im, vis = true; while (p && p !== scope) { const s = getComputedStyle(p); if (s.visibility === 'hidden' || s.opacity === '0' || s.display === 'none') { vis = false; break; } p = p.parentElement; } return vis && r.width > 0; });
  return {checked: el.checked, visible: imgs.length, loaded: imgs.every(im => im.complete && im.naturalWidth > 0)};
})(%s)
"""
WIPE = r"""
(async () => {
  const frame = document.querySelector('.inspect-frame'); const range = frame.querySelector('.inspect-range');
  frame.scrollIntoView({block:'center', behavior:'instant'}); await new Promise(r => setTimeout(r, 300));
  const out = {live: frame.classList.contains('is-live')};
  for (const v of [0, 25, 50, 75, 100]) { range.value = v; range.dispatchEvent(new Event('input', {bubbles:true})); await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); out['pos'+v] = frame.style.getPropertyValue('--pos'); }
  return out;
})()
"""
NAV = r"""
(() => {
  const nav = document.querySelector('.site-header nav, header nav');
  const links = Array.from(document.querySelectorAll('.site-header a')).filter(a => a.offsetParent !== null).map(a => a.textContent.trim().replace(/\s+/g,' ') + ' -> ' + a.getAttribute('href'));
  return {links, toggle: !!document.querySelector('.site-header [aria-expanded]')};
})()
"""
MOBILE = r"""
(async () => {
  const btn = document.querySelector('.menu-toggle, .nav-toggle, button[aria-controls]');
  if (!btn) return {error: 'no menu button'};
  btn.click(); await new Promise(r => setTimeout(r, 400));
  const open = btn.getAttribute('aria-expanded');
  const vis = Array.from(document.querySelectorAll('.site-header a')).filter(a => a.offsetParent !== null).map(a => a.getAttribute('href'));
  return {expanded: open, visibleLinks: vis};
})()
"""
srv = serve(sys.argv[1]); chrome = Chrome(); out = {}
try:
    for lang in ("en", "tr"):
        page = chrome.new_page()
        page.send("Page.addScriptToEvaluateOnNewDocument", {"source": CONN})
        page.send("Page.addScriptToEvaluateOnNewDocument", {"source": f"try{{localStorage.setItem('orbgss.lang','{lang}')}}catch(e){{}}"})
        page.emulate(1440, 900, 2.0, False, True)
        page.navigate(srv.base + "/"); time.sleep(0.8)
        r = {"h1": page.js("document.querySelector('h1').textContent.trim()"), "lang": page.js("document.documentElement.lang")}
        r["nav"] = page.js(NAV)
        ids = page.js("Array.from(document.querySelectorAll('input[type=radio][id^=ev-],input[type=radio][id^=cp-]')).map(e=>e.id)")
        r["radios"] = {i: page.js(RADIO % json.dumps(i)) for i in ids}
        r["wipe"] = page.js(WIPE)
        out[lang] = r
        page.close()
    page = chrome.new_page()
    page.send("Page.addScriptToEvaluateOnNewDocument", {"source": CONN})
    page.emulate(375, 812, 3.0, True, True)
    page.navigate(srv.base + "/"); time.sleep(0.6)
    out["mobile_menu"] = page.js(MOBILE)
    page.close()
finally:
    chrome.close(); srv.close()
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
bad = [(l, i, v) for l in ("en", "tr") for i, v in out[l]["radios"].items() if not (v["checked"] and v["loaded"] and v["visible"] > 0)]
print("radio failures:", bad); print("wipe:", out["en"]["wipe"]); print("mobile:", out["mobile_menu"]); print("h1:", out["en"]["h1"], "|", out["tr"]["h1"])
