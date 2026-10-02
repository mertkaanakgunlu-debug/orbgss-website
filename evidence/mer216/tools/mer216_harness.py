#!/usr/bin/env python3
"""MER-216 measurement harness: a Range-capable static server that mirrors vercel.json caching,
plus a minimal headless-Chrome CDP driver. Local audit tooling only; never a site dependency.

    from mer216_harness import serve, Chrome
"""
from __future__ import annotations

import http.server
import json
import mimetypes
import os
import pathlib
import re
import shutil
import socket
import subprocess
import tempfile
import threading
import time
import urllib.request

import websocket  # websocket-client

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
mimetypes.add_type("video/webm", ".webm")
mimetypes.add_type("video/mp4", ".mp4")
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("application/manifest+json", ".webmanifest")


def free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


class Handler(http.server.SimpleHTTPRequestHandler):
    root = "."
    log = []          # (path, status, bytes, range)
    video_throttle = None   # (after_bytes, bytes_per_second) for .webm/.mp4 bodies

    def __init__(self, *a, **k):
        super().__init__(*a, directory=self.root, **k)

    def log_message(self, fmt, *args):
        pass

    def end_headers(self):
        p = self.path.split("?")[0]
        self.send_header("X-Content-Type-Options", "nosniff")
        if p.startswith("/assets/"):
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        else:
            self.send_header("Cache-Control", "public, max-age=0, must-revalidate")
        self.send_header("Accept-Ranges", "bytes")
        super().end_headers()

    def send_head(self):
        path = self.translate_path(self.path)
        rng = self.headers.get("Range")
        if os.path.isdir(path) or not rng:
            return super().send_head()
        m = re.match(r"bytes=(\d*)-(\d*)", rng)
        if not m or not os.path.exists(path):
            return super().send_head()
        size = os.path.getsize(path)
        start = int(m.group(1)) if m.group(1) else max(0, size - int(m.group(2)))
        end = int(m.group(2)) if (m.group(1) and m.group(2)) else size - 1
        end = min(end, size - 1)
        if start > end:
            self.send_error(416)
            return None
        f = open(path, "rb")
        f.seek(start)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        self._remaining = end - start + 1
        return f

    def copyfile(self, source, outputsrc):
        rem = getattr(self, "_remaining", None)
        thr = Handler.video_throttle if self.path.split("?")[0].endswith((".webm", ".mp4")) else None
        sent = 0
        left = rem if rem is not None else (1 << 62)
        try:
            while left > 0:
                chunk = source.read(min(8192 if thr else 65536, left))
                if not chunk:
                    break
                outputsrc.write(chunk)
                outputsrc.flush()
                sent += len(chunk)
                left -= len(chunk)
                if thr and sent > thr[0]:
                    time.sleep(len(chunk) / float(thr[1]))
        except (ConnectionResetError, BrokenPipeError, OSError):
            pass
        self._remaining = None


class Server:
    def __init__(self, root):
        Handler.root = str(root)
        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    @property
    def base(self):
        return f"http://127.0.0.1:{self.port}"

    def close(self):
        self.httpd.shutdown()


def serve(root):
    return Server(root)


class Chrome:
    def __init__(self, headless=True, extra=None):
        self.port = free_port()
        self.profile = tempfile.mkdtemp(prefix="mer216-chrome-")
        args = [CHROME, f"--remote-debugging-port={self.port}",
                f"--remote-allow-origins=http://127.0.0.1:{self.port}",
                f"--user-data-dir={self.profile}", "--no-first-run", "--no-default-browser-check",
                "--disable-extensions", "--disable-background-networking",
                "--autoplay-policy=no-user-gesture-required", "--mute-audio",
                "--hide-scrollbars", "about:blank"]
        if headless:
            args.insert(1, "--headless=new")
        if extra:
            args[1:1] = extra
        self.proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(100):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{self.port}/json/version", timeout=1) as r:
                    self.version = json.load(r)
                break
            except Exception:
                time.sleep(0.2)
        else:
            raise RuntimeError("Chrome did not start")

    def new_page(self):
        req = urllib.request.Request(f"http://127.0.0.1:{self.port}/json/new?about:blank", method="PUT")
        with urllib.request.urlopen(req, timeout=5) as r:
            info = json.load(r)
        return Page(info["webSocketDebuggerUrl"])

    def close(self):
        try:
            self.proc.terminate()
            self.proc.wait(timeout=10)
        except Exception:
            self.proc.kill()
        shutil.rmtree(self.profile, ignore_errors=True)


class Page:
    def __init__(self, ws_url):
        self.ws = websocket.create_connection(ws_url, suppress_origin=True, max_size=None, timeout=60)
        self._id = 0
        self.events = []
        for d in ("Page", "Runtime", "Network", "Log", "DOM"):
            self.send(f"{d}.enable")

    def send(self, method, params=None, timeout=60):
        self._id += 1
        mid = self._id
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        end = time.time() + timeout
        while time.time() < end:
            self.ws.settimeout(max(0.1, end - time.time()))
            try:
                msg = json.loads(self.ws.recv())
            except websocket.WebSocketTimeoutException:
                break
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})
            self.events.append(msg)
        raise TimeoutError(method)

    def pump(self, seconds):
        end = time.time() + seconds
        while time.time() < end:
            self.ws.settimeout(max(0.05, end - time.time()))
            try:
                self.events.append(json.loads(self.ws.recv()))
            except websocket.WebSocketTimeoutException:
                break

    def js(self, expr, await_promise=True, timeout=60):
        r = self.send("Runtime.evaluate", {"expression": expr, "returnByValue": True,
                                           "awaitPromise": await_promise}, timeout=timeout)
        if "exceptionDetails" in r:
            raise RuntimeError(json.dumps(r["exceptionDetails"])[:600])
        return r.get("result", {}).get("value")

    def emulate(self, width, height, dpr=1.0, mobile=False, reduced_motion=False):
        self.send("Emulation.setDeviceMetricsOverride", {"width": width, "height": height,
                  "deviceScaleFactor": dpr, "mobile": mobile})
        feats = [{"name": "prefers-reduced-motion", "value": "reduce" if reduced_motion else "no-preference"}]
        self.send("Emulation.setEmulatedMedia", {"features": feats})

    def navigate(self, url, wait=True):
        self.events.clear()
        self.send("Page.navigate", {"url": url})
        if wait:
            self.wait_load()

    def wait_load(self, timeout=30):
        end = time.time() + timeout
        while time.time() < end:
            if self.js("document.readyState") == "complete":
                return
            time.sleep(0.1)

    def screenshot(self, path, full=False, clip=None):
        import base64
        params = {"format": "png", "captureBeyondViewport": bool(full or clip)}
        if clip:
            params["clip"] = {**clip, "scale": 1}
        r = self.send("Page.captureScreenshot", params, timeout=120)
        pathlib.Path(path).write_bytes(base64.b64decode(r["data"]))

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass
