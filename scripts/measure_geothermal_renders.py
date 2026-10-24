#!/usr/bin/env python3
"""Measure how large the four MER-151 derivatives are drawn on the Geothermal page, in a real browser (MER-276).

    python3 scripts/measure_geothermal_renders.py            # measure and print
    python3 scripts/measure_geothermal_renders.py --write    # ... and record it in sources.json

Local QA tooling (Playwright + Chromium), never a site runtime dependency and never run on Vercel.
It serves the working tree with Vercel's cleanUrls/trailingSlash behaviour, loads `/solutions/geothermal/`
at 19 widths from 360 to 3840 CSS px and two device pixel ratios, and for each Class-B layer reads the drawn
CSS width, the candidate the browser actually selected (`currentSrc`) and that file's native width. The result
is written to `web_005b.placement[layer].geothermal_placement.rendered`, the record `scripts/validate_site.py`
holds to the 600 CSS px cap, the native 1200 px grid and "never upscaled" (atlas:geothermal, A1).
"""
from __future__ import annotations

import json
import math
import os
import pathlib
import sys
import urllib.parse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from measure_interior_renders import DPRS, MANIFEST, VIEWPORTS, serve  # noqa: E402

ROUTE = "/solutions/geothermal/"
ROUTE_FILE = "solutions/geothermal/index.html"
PLATES = {"terrain": "elevation", "thm01": "thermal", "alt01": "alteration", "priority": "priority"}


def main(argv: list[str]) -> int:
    from playwright.sync_api import sync_playwright

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    layers = manifest["web_005b"]["analytical"]["layers"]
    # file name -> (layer, pixel width). The pixel width comes from the record: `img.naturalWidth` is the
    # width in CSS px at the density of the selected candidate, so a 2x candidate would read half its width.
    delivery = manifest["web_005b"]["analytical"].get("delivery", {}).get("layers", {})
    owner = {pathlib.PurePosixPath(d["path"]).name: (layer, d["width"])
             for layer in PLATES for d in layers[layer]["derivatives"] + delivery.get(layer, [])}

    server, base = serve()
    worst: dict[str, dict] = {}
    try:
        with sync_playwright() as pw:
            kwargs = {"args": ["--no-sandbox"]}
            exe = os.environ.get("CHROMIUM_PATH") or ("/opt/pw-browsers/chromium"
                                                      if pathlib.Path("/opt/pw-browsers/chromium").exists() else None)
            if exe:
                kwargs["executable_path"] = exe
            browser = pw.chromium.launch(**kwargs)
            for width, height in VIEWPORTS:
                for dpr in DPRS:
                    ctx = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=dpr,
                                              is_mobile=width < 600, has_touch=width < 1000)
                    page = ctx.new_page()
                    page.goto(base + ROUTE, wait_until="load")
                    page.add_style_tag(content="html{scroll-behavior:auto!important}")
                    total = page.evaluate("document.documentElement.scrollHeight")
                    y = 0
                    while y < total:
                        page.evaluate(f"window.scrollTo(0,{y})")
                        page.wait_for_timeout(80)
                        y += int(height * 0.8)
                    page.wait_for_function("[...document.images].every(i => i.complete)", timeout=20000)
                    rows = page.evaluate("""() => [...document.images].map(i => {
                        const r = i.getBoundingClientRect();
                        return {src: i.currentSrc, css: r.width, nat: i.naturalWidth,
                                fit: getComputedStyle(i).objectFit, xform: getComputedStyle(i).transform,
                                filter: getComputedStyle(i).filter}; })""")
                    for row in rows:
                        name = pathlib.PurePosixPath(urllib.parse.urlsplit(row["src"]).path).name
                        if name not in owner or row["nat"] == 0:
                            continue
                        layer, pixels = owner[name]
                        if row["xform"] not in ("none", "") or row["filter"] not in ("none", ""):
                            print(f"{layer}: transform or filter on a governed raster at {width}x{height}", file=sys.stderr)
                            return 1
                        upscale = row["css"] * dpr / pixels
                        rec = worst.setdefault(layer, {"max_css": 0.0, "max_upscale": 0.0, "at": "", "selected": "",
                                                       "selected_at_max": "", "at_max_css": ""})
                        if row["css"] > rec["max_css"]:
                            rec["max_css"] = row["css"]
                            rec["selected_at_max"] = urllib.parse.urlsplit(row["src"]).path.lstrip("/")
                            rec["at_max_css"] = f"{width}x{height} @{dpr}x"
                        if upscale > rec["max_upscale"]:
                            rec["max_upscale"] = upscale
                            rec["at"] = f"{width}x{height} @{dpr}x"
                            rec["selected"] = urllib.parse.urlsplit(row["src"]).path.lstrip("/")
                    page.close()
                    ctx.close()
            browser.close()
    finally:
        server.shutdown()

    for layer, rec in sorted(worst.items()):
        print(f"{layer:9} max {rec['max_css']:.1f} CSS px ({rec['at_max_css']}), "
              f"worst upscale {rec['max_upscale']:.3f}x at {rec['at']}")
    missing = [layer for layer in PLATES if layer not in worst]
    if missing:
        print(f"not measured on the Geothermal page: {missing}", file=sys.stderr)
        return 1
    if "--write" not in argv:
        return 0

    viewports = [f"{w}x{h}" for w, h in VIEWPORTS]
    for layer, rec in worst.items():
        css = math.ceil(rec["max_css"])
        placement = manifest["web_005b"]["placement"][layer]
        placement["geothermal_placement"] = {
            "status": "preview",
            "consumer": "MER-276 / Atlas Geothermal page",
            "acceptance": "A1 - preview only, pending the CTO's acceptance before any publish",
            "route": ROUTE_FILE,
            "plate": PLATES[layer],
            "rendered": {
                "tool": "scripts/measure_geothermal_renders.py",
                "measurement_method": "Headless Chromium on the English route at 19 viewport widths from 360 to 3840 CSS px at "
                                      "DPR 1 and 2; the drawn width of the image and the candidate the browser selected "
                                      "(currentSrc) are recorded, never the sizes attribute.",
                "viewports_measured": viewports,
                "device_pixel_ratios_measured": list(DPRS),
                "max_css_width": css,
                "device_pixel_ratio_considered": 2,
                "max_device_px": css * 2,
                "native_px": 1200,
                "selected_derivative": rec["selected_at_max"],
                "max_upscale_factor": round(rec["max_upscale"], 3),
                "max_upscale_at": rec["at"],
            },
        }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("sources.json updated")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
