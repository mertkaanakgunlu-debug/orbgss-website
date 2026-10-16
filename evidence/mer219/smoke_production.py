"""MER-219 post-publication HTTP smoke check for orbgss.com. Read-only: GET/HEAD requests only.

    py -3.14 evidence/mer219/smoke_production.py --expect-sha <publication SHA> [--base https://orbgss.com]

Run from a checkout that contains the expected SHA. The check proves, over plain HTTP:
  * HTTPS and the apex redirects; every canonical route; a real 404;
  * the routes MER-240 retired answer with a 301 to their successors;
  * internal repository paths are not served (MER-237);
  * every route's og:image is a self-hosted image that loads (MER-237);
  * the MER-216 hero ladder is in the markup and every tier answers with the right type,
    range support and immutable caching;
  * every asset the homepage references loads;
  * production identity: the served index.html, script.js and styles.css are byte-identical to
    the expected Git commit.
Browser-level behaviour (hero playback, fallbacks, Act 03 switching, console) is a separate
checklist in tasks/MER-219_PREFLIGHT.md.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request

# MER-240 / Milestone 6 page set; the retired routes are 301 redirects (vercel.json).
ROUTES = ["/", "/solutions/", "/solutions/geothermal/", "/about/", "/partner/"]
REDIRECTS = {"/platform/": "/", "/pilot/": "/solutions/geothermal/", "/company/": "/about/", "/contact/": "/partner/"}
INTERNAL = ["/STATUS.md", "/CLAUDE.md", "/README.md", "/AGENTS.md", "/CHANGELOG.md", "/IMAGERY_RIGHTS.md",
            "/docs/HANDOFF.md", "/tasks/MER-213_POST_LAUNCH_AUDIT_EVIDENCE.md", "/tasks/", "/evidence/",
            "/scripts/validate_site.py", "/hero/config/scene.json", "/references/", "/.vercelignore",
            "/vercel.json"]
IDENTITY = ["index.html", "script.js", "styles.css"]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def fetch(url, method="GET", headers=None, follow=True):
    opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, method=method, headers={"User-Agent": "orbgss-mer219-smoke", **(headers or {})})
    try:
        with opener.open(req, timeout=30) as r:
            return r.status, dict(r.headers), r.read() if method == "GET" else b""
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read() if method == "GET" else b""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://orbgss.com")
    ap.add_argument("--expect-sha", required=True)
    a = ap.parse_args()
    base = a.base.rstrip("/")
    results = []

    def check(ok, name, detail=""):
        results.append((bool(ok), name, detail))
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))

    print(f"MER-219 production smoke — {base} — expecting {a.expect_sha}\n")
    host = base.split("://", 1)[1]
    s, h, _ = fetch(f"http://{host}/", follow=False)
    check(s in (301, 308) and h.get("Location", "").startswith(f"https://{host}"), "http redirects to https", f"{s} {h.get('Location', '')}")
    s, h, _ = fetch(f"https://www.{host}/", follow=False)
    check(s in (301, 308) and h.get("Location", "") == f"https://{host}/", "www redirects to the apex", f"{s} {h.get('Location', '')}")
    s, h, _ = fetch(base + "/")
    check("max-age" in h.get("Strict-Transport-Security", ""), "HSTS header present", h.get("Strict-Transport-Security", "missing"))

    pages = {}
    for r in ROUTES:
        s, h, body = fetch(base + r)
        pages[r] = body.decode("utf-8", "replace")
        check(s == 200 and "text/html" in h.get("Content-Type", ""), f"route {r} serves HTML", str(s))
    s, _, _ = fetch(base + "/mer219-smoke-not-a-page/")
    check(s == 404, "an unknown path returns 404", str(s))

    def same_path(location, path):
        return location in (path, base + path)

    for old, new in REDIRECTS.items():
        s, h, _ = fetch(base + old, follow=False)
        loc = h.get("Location", "")
        check(s == 301 and same_path(loc, new), f"retired route {old} answers 301 to {new}", f"{s} {loc}")
        # Without the slash, trailingSlash may answer first (308 to the slashed path) or the
        # redirect may match directly (301 to the successor); either ends on the successor.
        s, h, _ = fetch(base + old.rstrip("/"), follow=False)
        loc = h.get("Location", "")
        check((s == 308 and same_path(loc, old)) or (s == 301 and same_path(loc, new)),
              f"retired route {old.rstrip('/')} is redirected", f"{s} {loc}")

    for p in INTERNAL:
        s, _, _ = fetch(base + p, follow=False)
        check(s == 404, f"internal path {p} is not served", str(s))

    for r, html in pages.items():
        m = re.search(r'property="og:image" content="([^"]+)"', html)
        if not m:
            check(False, f"route {r} declares og:image")
            continue
        url = m.group(1)
        s, h, _ = fetch(url, method="HEAD")
        check(url.startswith(base + "/assets/") and "crater-lake" not in url and s == 200
              and h.get("Content-Type", "").startswith("image/"), f"route {r} og:image loads", f"{s} {url}")

    home = pages.get("/", "")
    m = re.search(r"data-hero-tiers='([^']+)'", home)
    check(bool(m), "homepage carries the MER-216 hero ladder (data-hero-tiers)")
    if m:
        for tier in json.loads(m.group(1)):
            for codec, ctype in (("webm", "video/webm"), ("mp4", "video/mp4")):
                url = f"{base}/{tier[codec].lstrip('/')}"
                s, h, _ = fetch(url, method="HEAD")
                check(s == 200 and h.get("Content-Type", "").startswith(ctype)
                      and "immutable" in h.get("Cache-Control", ""), f"hero {tier['id']} {codec} type and cache", f"{s} {h.get('Content-Type', '')}")
                s, h, _ = fetch(url, headers={"Range": "bytes=0-1"})
                check(s == 206 and h.get("Content-Range", "").startswith("bytes 0-1/"), f"hero {tier['id']} {codec} answers a range request", str(s))

    assets = sorted(set(re.findall(r"(?<![\w./-])/?(assets/[\w./%-]*\w)", home)))
    bad = []
    for path in assets:
        s, _, _ = fetch(f"{base}/{path}", method="HEAD")
        if s != 200:
            bad.append(f"{path} {s}")
    check(not bad, f"all {len(assets)} homepage assets load", "; ".join(bad[:5]))
    for p in ("/sitemap.xml", "/robots.txt"):
        s, _, _ = fetch(base + p)
        check(s == 200, f"{p} served", str(s))

    for f in IDENTITY:
        s, _, body = fetch(base + "/" + ("" if f == "index.html" else f))
        try:
            blob = subprocess.run(["git", "show", f"{a.expect_sha}:{f}"], capture_output=True, check=True).stdout
        except subprocess.CalledProcessError:
            check(False, f"{f} identity", "expected SHA not in this checkout")
            continue
        live, want = hashlib.sha256(body).hexdigest(), hashlib.sha256(blob).hexdigest()
        check(live == want, f"served {f} is byte-identical to {a.expect_sha[:8]}", f"live {live[:12]} / git {want[:12]}")

    failed = [n for ok, n, _ in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
