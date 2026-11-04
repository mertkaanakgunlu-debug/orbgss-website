#!/usr/bin/env python3
"""Measure how large the MER-151 derivatives (and the two MER-242 ones) are drawn on the Geothermal page, in a real browser (MER-276).

    python3 scripts/measure_geothermal_renders.py            # measure and print
    python3 scripts/measure_geothermal_renders.py --write    # ... and record it in sources.json

Local QA tooling (Playwright + Chromium), never a site runtime dependency and never run on Vercel.
It serves the working tree with Vercel's cleanUrls/trailingSlash behaviour, loads `/solutions/geothermal/`
at 19 widths from 360 to 3840 CSS px and two device pixel ratios, and for each Class-B layer reads the drawn
CSS width, the candidate the browser actually selected (`currentSrc`) and that file's native width. The result
is written to `web_005b.placement[layer].geothermal_placement.rendered` (and, for the two MER-242 surfaces,
`mer_242.surfaces[name].geothermal_placement.rendered`), the record `scripts/validate_site.py` holds to the 600 CSS px
cap, the native 1200 px grid and "never upscaled" (atlas:geothermal, A1 and MER-242).

Interior cleanup (CTO, 2026-11-04): the priority map is no longer a plate on the Geothermal page (the result figure is the
priority over shaded relief, MER-242). It has a second recorded home in the Geothermal band of `/solutions/` (the one named
R2 exception, 600 CSS px at most), measured the same way and written to
`web_005b.placement.priority.solutions_placement.rendered`.
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
SOLUTIONS_ROUTE = "/solutions/"
SOLUTIONS_FILE = "solutions/index.html"
PLATES = {"terrain": "elevation", "thm01": "thermal", "alt01": "alteration"}
DESKTOP_MIN = 1180  # the narrowest measured viewport on which the Solutions band sets its copy beside the map
MER242 = {"alt02": "iron", "relief": "relief"}  # surface -> the plate or section that shows it


def main(argv: list[str]) -> int:
    from playwright.sync_api import sync_playwright

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    layers = manifest["web_005b"]["analytical"]["layers"]
    # file name -> (layer, pixel width). The pixel width comes from the record: `img.naturalWidth` is the
    # width in CSS px at the density of the selected candidate, so a 2x candidate would read half its width.
    delivery = manifest["web_005b"]["analytical"].get("delivery", {}).get("layers", {})
    owner = {pathlib.PurePosixPath(d["path"]).name: (layer, d["width"])
             for layer in PLATES for d in layers[layer]["derivatives"] + delivery.get(layer, [])}

    for surface, rec in manifest["mer_242"]["surfaces"].items():
        for d in rec["derivatives"]:
            if d["width"] >= 600:  # the 160 / 320 px files are Sources thumbnails, measured by the interior tool
                owner[pathlib.PurePosixPath(d["path"]).name] = (surface, d["width"])

    priority_owner = {pathlib.PurePosixPath(d["path"]).name: ("priority", d["width"])
                      for d in layers["priority"]["derivatives"] + delivery.get("priority", [])}

    def measure(browser, base: str, route: str, owner: dict) -> dict:
        worst: dict[str, dict] = {}
        for width, height in VIEWPORTS:
            for dpr in DPRS:
                ctx = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=dpr,
                                          is_mobile=width < 600, has_touch=width < 1000)
                page = ctx.new_page()
                page.goto(base + route, wait_until="load")
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
                    return {src: i.currentSrc, css: r.width, nat: i.naturalWidth, inMap: !!i.closest('figure.pilot-map'),
                            fit: getComputedStyle(i).objectFit, xform: getComputedStyle(i).transform,
                            filter: getComputedStyle(i).filter}; })""")
                for row in rows:
                    name = pathlib.PurePosixPath(urllib.parse.urlsplit(row["src"]).path).name
                    if name not in owner or row["nat"] == 0:
                        continue
                    layer, pixels = owner[name]
                    if row["xform"] not in ("none", "") or row["filter"] not in ("none", ""):
                        raise SystemExit(f"{layer}: transform or filter on a governed raster at {width}x{height}")
                    upscale = row["css"] * dpr / pixels
                    rec = worst.setdefault(layer, {"max_css": 0.0, "max_upscale": 0.0, "at": "", "selected": "",
                                                   "selected_at_max": "", "at_max_css": ""})
                    # The two-column Geothermal band of /solutions/ holds from 1101 CSS px up. The smallest drawn width there is
                    # recorded as well: the band once squeezed the map to 225 px at 1920 and to nothing at 2560 (review, 2026-11-04).
                    if width >= DESKTOP_MIN and row["inMap"] and row["css"] < rec.get("min_css_desktop", 1e9):
                        rec["min_css_desktop"] = row["css"]
                        rec["at_min_css_desktop"] = f"{width}x{height} @{dpr}x"
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
        return worst

    server, base = serve()
    try:
        with sync_playwright() as pw:
            kwargs = {"args": ["--no-sandbox"]}
            exe = os.environ.get("CHROMIUM_PATH") or ("/opt/pw-browsers/chromium"
                                                      if pathlib.Path("/opt/pw-browsers/chromium").exists() else None)
            if exe:
                kwargs["executable_path"] = exe
            browser = pw.chromium.launch(**kwargs)
            worst = measure(browser, base, ROUTE, owner)
            solutions_worst = measure(browser, base, SOLUTIONS_ROUTE, priority_owner)
            browser.close()
    finally:
        server.shutdown()

    for layer, rec in sorted(solutions_worst.items()):
        print(f"{layer:9} max {rec['max_css']:.1f} CSS px on {SOLUTIONS_ROUTE} ({rec['at_max_css']}), "
              f"worst upscale {rec['max_upscale']:.3f}x at {rec['at']}, "
              f"min from {DESKTOP_MIN} px up {rec.get('min_css_desktop', 0):.1f} CSS px ({rec.get('at_min_css_desktop', '-')})")
    for layer, rec in sorted(worst.items()):
        print(f"{layer:9} max {rec['max_css']:.1f} CSS px ({rec['at_max_css']}), "
              f"worst upscale {rec['max_upscale']:.3f}x at {rec['at']}")
    missing = [layer for layer in [*PLATES, *MER242] if layer not in worst]
    if missing:
        print(f"not measured on the Geothermal page: {missing}", file=sys.stderr)
        return 1
    if "priority" not in solutions_worst:
        print("the priority map was not measured on /solutions/", file=sys.stderr)
        return 1
    if "priority" in worst:
        print("the priority map is drawn on the Geothermal page; only its legend ramp may be (interior cleanup)",
              file=sys.stderr)
        return 1
    if "--write" not in argv:
        return 0

    viewports = [f"{w}x{h}" for w, h in VIEWPORTS]
    for layer, rec in worst.items():
        css = math.ceil(rec["max_css"])
        if layer in MER242:
            placement = manifest["mer_242"]["surfaces"][layer]
            placement["placement_status"] = ("placed on /solutions/geothermal/ (preview only, pending independent review and "
                                             "the CTO's acceptance before any publish)")
        else:
            placement = manifest["web_005b"]["placement"][layer]
        placement["geothermal_placement"] = {
            "status": "preview",
            "consumer": "MER-242 / Geothermal page" if layer in MER242 else "MER-276 / Atlas Geothermal page",
            "acceptance": ("MER-242 - preview only, pending independent review and the CTO's acceptance before any publish"
                           if layer in MER242 else "A1 - preview only, pending the CTO's acceptance before any publish"),
            "route": ROUTE_FILE,
            "plate": MER242.get(layer) or PLATES[layer],
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
    prec = solutions_worst["priority"]
    pcss = math.ceil(prec["max_css"])
    manifest["web_005b"]["placement"]["priority"].pop("geothermal_placement", None)
    manifest["web_005b"]["placement"]["priority"]["solutions_placement"] = {
        "status": "preview",
        "consumer": "Interior cleanup B5 / the Geothermal band of /solutions/",
        "acceptance": ("CTO decision of 2026-11-04: the one named R2 exception. The priority map is drawn at full size on "
                       "the homepage and on /solutions/ (600 CSS px at most) and nowhere else; the Geothermal page "
                       "borrows only its legend ramp."),
        "route": SOLUTIONS_FILE,
        "plate": "pilot-map",
        "rendered": {
            "tool": "scripts/measure_geothermal_renders.py",
            "measurement_method": "Headless Chromium on the English route at 19 viewport widths from 360 to 3840 CSS px at "
                                  "DPR 1 and 2; the drawn width of the image and the candidate the browser selected "
                                  "(currentSrc) are recorded, never the sizes attribute.",
            "viewports_measured": viewports,
            "device_pixel_ratios_measured": list(DPRS),
            "max_css_width": pcss,
            "device_pixel_ratio_considered": 2,
            "max_device_px": pcss * 2,
            "native_px": 1200,
            "selected_derivative": prec["selected_at_max"],
            "max_upscale_factor": round(prec["max_upscale"], 3),
            "max_upscale_at": prec["at"],
            "min_css_width_desktop": math.floor(prec.get("min_css_desktop", 0)),
            "min_css_width_desktop_at": prec.get("at_min_css_desktop", ""),
            "min_css_width_desktop_note": f"The smallest drawn width of the map at the measured viewports of {DESKTOP_MIN} CSS px and "
                                          "wider, where the copy sits beside the map. It must not shrink with the window.",
        },
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("sources.json updated")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
