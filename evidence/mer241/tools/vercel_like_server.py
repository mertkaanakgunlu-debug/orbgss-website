"""A local static server that behaves like the Vercel project for the routes MER-241 touches.

    from vercel_like_server import serve
    srv = serve(ROOT); srv.base  # "http://127.0.0.1:PORT"

It reads the repository's own vercel.json and .vercelignore: only the allowlisted root entries are
served (so an internal path answers 404, as in production); trailingSlash redirects (308), cleanUrls
(/about/index.html -> /about/ with a 308), the 301 redirects, the headers, and 404.html answered with
a real 404 status for every unknown path, /tr/... included. Range requests are honoured (the hero
video needs them). Local QA tooling only; never a site dependency.
"""
from __future__ import annotations

import http.server
import json
import mimetypes
import pathlib
import socket
import threading
import urllib.parse

mimetypes.add_type("video/webm", ".webm")
mimetypes.add_type("video/mp4", ".mp4")
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("application/manifest+json", ".webmanifest")


def _allowlist(root: pathlib.Path) -> set[str]:
    rules = [ln.strip() for ln in (root / ".vercelignore").read_text(encoding="utf-8").splitlines()]
    return {ln[1:] for ln in rules if ln.startswith("!")}


class _Handler(http.server.BaseHTTPRequestHandler):
    root: pathlib.Path
    allowed: set[str]
    config: dict
    log: list  # (path, status)

    def log_message(self, *_a):
        pass

    def _send(self, status, body=b"", ctype="text/html; charset=utf-8", extra=None, head=False):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "public, max-age=0, must-revalidate")
        for key, value in (extra or {}).items():
            self.send_header(key, value)
        self.end_headers()
        if not head:
            self.wfile.write(body)
        self.log.append((self.path, status))

    def _redirect(self, status, location, head=False):
        self.send_response(status)
        self.send_header("Location", location)
        self.send_header("Content-Length", "0")
        self.end_headers()
        self.log.append((self.path, status))

    def _resolve(self, path):
        rel = path.lstrip("/")
        if rel.split("/", 1)[0] not in self.allowed and rel != "":
            return None
        if rel == "" or rel.endswith("/"):
            candidate = self.root / rel / "index.html"
        else:
            candidate = self.root / rel
        candidate = candidate.resolve()
        if self.root not in candidate.parents and candidate != self.root:
            return None
        return candidate if candidate.is_file() else None

    def _handle(self, head):
        parsed = urllib.parse.urlsplit(self.path)
        path, query = urllib.parse.unquote(parsed.path), ("?" + parsed.query if parsed.query else "")
        for rule in self.config.get("redirects", []):
            if path == rule["source"]:
                return self._redirect(rule.get("statusCode", 307), rule["destination"] + query, head)
        # cleanUrls: /x/index.html and /x.html -> /x/ ; trailingSlash: /x -> /x/
        if path.endswith("/index.html"):
            return self._redirect(308, path[: -len("index.html")] + query, head)
        last = path.rsplit("/", 1)[-1]
        if "." not in last and not path.endswith("/"):
            if self._resolve(path + "/") is not None:
                return self._redirect(308, path + "/" + query, head)
        target = self._resolve(path)
        if target is None:
            page = self.root / "404.html"
            return self._send(404, page.read_bytes(), head=head)
        data = target.read_bytes()
        ctype = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        if target.suffix == ".html":
            ctype = "text/html; charset=utf-8"
        extra = {}
        if path.startswith("/assets/"):
            extra["Cache-Control"] = "public, max-age=31536000, immutable"
        rng = self.headers.get("Range")
        if rng and rng.startswith("bytes="):
            start_s, _, end_s = rng[6:].partition("-")
            start = int(start_s) if start_s else 0
            end = int(end_s) if end_s else len(data) - 1
            end = min(end, len(data) - 1)
            extra["Content-Range"] = f"bytes {start}-{end}/{len(data)}"
            return self._send(206, data[start:end + 1], ctype, extra, head)
        return self._send(200, data, ctype, extra, head)

    def do_GET(self):
        self._handle(False)

    def do_HEAD(self):
        self._handle(True)


class Server:
    def __init__(self, root: pathlib.Path):
        handler = type("H", (_Handler,), {
            "root": root.resolve(), "allowed": _allowlist(root),
            "config": json.loads((root / "vercel.json").read_text(encoding="utf-8")), "log": [],
        })
        sock = socket.socket()
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
        sock.close()
        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
        self.log = handler.log
        self.base = f"http://127.0.0.1:{port}"
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def close(self):
        self.httpd.shutdown()


def serve(root) -> Server:
    return Server(pathlib.Path(root))
