import os
import functools, http.server, pathlib, socketserver, sys, threading, json
from playwright.sync_api import sync_playwright
root = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2])
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x): pass
class TS(socketserver.ThreadingTCPServer): allow_reuse_address = True; daemon_threads = True
srv = TS(("127.0.0.1", 0), functools.partial(Q, directory=str(root))); base = f"http://127.0.0.1:{srv.server_address[1]}"
threading.Thread(target=srv.serve_forever, daemon=True).start()
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None, args=["--no-sandbox"])
    pg = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1).new_page()
    pg.goto(base + "/", wait_until="load"); pg.add_style_tag(content=".skip-link{display:none!important}"); pg.wait_for_timeout(800)
    sec = pg.locator("#solutions"); sec.scroll_into_view_if_needed(); pg.wait_for_timeout(900)
    cards = pg.locator("#solutions a.domain-link"); print("cards", cards.count())
    first = cards.nth(1); first.scroll_into_view_if_needed(); pg.wait_for_timeout(500)
    first.hover(); pg.wait_for_timeout(600)
    box = sec.bounding_box(); sec.screenshot(path=str(out / "hover-solutions-cards.jpg"), type="jpeg", quality=90)
    pg.mouse.move(2, 2)
    pg.evaluate("document.activeElement && document.activeElement.blur()")
    pg.evaluate("document.querySelectorAll('#solutions a.domain-link')[1].focus({focusVisible:true})")
    pg.keyboard.press("Shift+Tab"); pg.keyboard.press("Tab"); pg.wait_for_timeout(600)
    print(pg.evaluate("document.activeElement.className + ' ' + document.activeElement.getAttribute('href')"))
    sec.screenshot(path=str(out / "focus-solutions-cards.jpg"), type="jpeg", quality=90)
    b.close()
srv.shutdown()
