"""Deliberately break each MER-237 deploy-set and social-preview invariant and confirm validate_site.py catches it.

    py -3.14 scripts/negative_tests_mer237.py

Until MER-237 Vercel deployed the whole repository, so orbgss.com served STATUS.md, CLAUDE.md, docs/,
tasks/, evidence/, scripts/ and hero/. .vercelignore is now a root allowlist. The contract worth
guarding: the allowlist keeps its "ignore everything first" shape; no internal path is let back in;
nothing a public page, stylesheet, manifest, sitemap or robots.txt references falls outside it; no
documentation or tooling file hides inside a deployed directory; and every route's og:image is a
deployed, self-hosted image some page actually shows (four routes advertised the retired Crater
Lake scene until MER-237).

Same discipline as scripts/negative_tests_mer216.py: each case mutates one real file (or creates
one), runs the site validator, and restores the original in a `finally` block. A case counts as
CAUGHT only when the validator fails with the expected text on an ERROR line the unmutated baseline
did not already print. The run ends by proving the restored tree validates identically.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(".").resolve()
IGNORE = ROOT / ".vercelignore"
INDEX = ROOT / "index.html"
PILOT = ROOT / "pilot" / "index.html"
PLATFORM = ROOT / "platform" / "index.html"
CONTACT = ROOT / "contact" / "index.html"
SITEMAP = ROOT / "sitemap.xml"
VALIDATOR = "scripts/validate_site.py"

CASES = []


def case(name, path, mutate, expect):
    CASES.append((name, path, mutate, expect))


def site():
    r = subprocess.run([sys.executable, VALIDATOR], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def drop_rule(rule):
    return lambda t: re.sub(rf"(?m)^{re.escape(rule)}\r?\n", "", t, count=1)


def add_rule(rule):
    return lambda t: t.rstrip("\r\n") + "\n" + rule + "\n"


def swap(old, new):
    return lambda t: t.replace(old, new, 1)


OG = '<meta property="og:image" content="https://orbgss.com/assets/hero/hero-poster-1600.webp" />'

# ---- the allowlist's shape ---------------------------------------------------------------------
case("the allowlist is emptied (Vercel would deploy the whole repository again)", IGNORE,
     lambda t: "# nothing ignored\n",
     "the first rule must be '/*'")
case("the ignore-everything rule is removed (the allowlist becomes a blocklist)", IGNORE,
     drop_rule("/*"),
     "the first rule must be '/*'")
case("a glob rule the validator cannot model is added", IGNORE,
     add_rule("!assets/**"),
     "unsupported rule")
case("a plain ignore line is added after the allowlist", IGNORE,
     add_rule("*.md"),
     "unsupported rule")
case("the allowlist names an entry that does not exist", IGNORE,
     add_rule("!about"),
     "which does not exist")

# ---- internal paths let back in ----------------------------------------------------------------
for entry, shown in (("STATUS.md", "STATUS.md"), ("CLAUDE.md", "CLAUDE.md"), ("docs", "docs/"),
                     ("tasks", "tasks/"), ("evidence", "evidence/"), ("scripts", "scripts/"),
                     ("hero", "hero/"), ("references", "references/")):
    case(f"{entry} is re-included", IGNORE, add_rule("!" + entry),
         f"internal path {shown} would be deployed")

# ---- public entries dropped --------------------------------------------------------------------
case("vercel.json is dropped (the project configuration would not reach Vercel)", IGNORE,
     drop_rule("!vercel.json"),
     "vercel.json is not deployed")
case("404.html is dropped", IGNORE, drop_rule("!404.html"), "404.html is not deployed")
case("a public route directory is dropped", IGNORE, drop_rule("!pilot"),
     "public route file pilot/index.html is not deployed")
case("styles.css is dropped while every page links it", IGNORE, drop_rule("!styles.css"),
     "references styles.css, which .vercelignore does not deploy")
case("assets/ is dropped while every page shows it", IGNORE, drop_rule("!assets"),
     "references assets/")
case("sitemap.xml is dropped while robots.txt points at it", IGNORE, drop_rule("!sitemap.xml"),
     "robots.txt: references sitemap.xml, which .vercelignore does not deploy")

# ---- references that leave the deploy set ------------------------------------------------------
case("a page links an internal document", INDEX,
     swap("</body>", '<a href="/STATUS.md">status</a></body>'),
     "references STATUS.md, which .vercelignore does not deploy")
case("the sitemap lists a path outside the deploy set", SITEMAP,
     swap("</urlset>", "<url><loc>https://orbgss.com/docs/</loc></url></urlset>"),
     "references docs/index.html, which .vercelignore does not deploy")
case("a sub-route uses a document-relative asset path (it resolves under the route)", PILOT,
     lambda t: re.sub(r'src="/assets/', 'src="assets/', t, count=1),
     "references pilot/assets/")
case("a page references a deployed path that does not exist", PLATFORM,
     swap("</body>", '<img src="/assets/imagery/missing-scene.webp" alt="" /></body>'),
     "references assets/imagery/missing-scene.webp, which does not exist")
case("a Markdown note is left inside a deployed directory", ROOT / "assets" / "NOTES.md",
     lambda t: "# internal note\n",
     "deploy set contains an internal file: assets/NOTES.md")
case("a Python tool is left inside a deployed route directory", ROOT / "contact" / "build.py",
     lambda t: "print('internal')\n",
     "deploy set contains an internal file: contact/build.py")

# ---- social previews ---------------------------------------------------------------------------
case("a route advertises the retired Crater Lake scene again", PLATFORM,
     swap(OG, '<meta property="og:image" content="https://orbgss.com/assets/imagery/crater-lake-2023.jpg" />'),
     "is not an image any page shows")
case("a route loses its og:image", CONTACT,
     swap(OG, ""),
     "og:image is missing")
case("a route's og:image is hosted elsewhere", CONTACT,
     swap(OG, '<meta property="og:image" content="https://example.com/preview.jpg" />'),
     "og:image is missing or is not a self-hosted")
case("a route's og:image points at a file that does not exist", PLATFORM,
     swap(OG, '<meta property="og:image" content="https://orbgss.com/assets/hero/hero-poster-9999.webp" />'),
     "og:image assets/hero/hero-poster-9999.webp does not exist")


def main() -> int:
    print("MER-237 negative tests — deploy set and social previews\n")
    rc, baseline = site()
    if rc != 0:
        print("baseline tree does not validate; refusing to run")
        print(baseline)
        return 1

    def failed_with(text, blob):
        return any(text.lower() in ln.lower() for ln in blob.splitlines() if ln.startswith("ERROR"))

    results = []
    for name, path, mutate, expect in CASES:
        existed = path.exists()
        original = path.read_bytes().decode("utf-8") if existed else ""
        try:
            mutated = mutate(original)
            assert mutated != original, "mutation was a no-op: " + name
            path.write_bytes(mutated.encode("utf-8"))
            rc, out = site()
            caught = rc != 0 and failed_with(expect, out) and not failed_with(expect, baseline)
            results.append(caught)
            print(f"  {'CAUGHT ' if caught else 'MISSED '} {name} (exit {rc})")
            if not caught:
                print("     expected text: " + repr(expect))
                for line in out.splitlines():
                    if line.startswith("ERROR"):
                        print("     " + line[:170])
        finally:
            if existed:
                path.write_bytes(original.encode("utf-8"))
            else:
                path.unlink(missing_ok=True)
    print()
    print(f"{sum(results)}/{len(results)} deliberate regressions caught")
    rc, out = site()
    print(f"Restored tree: site exit {rc} — {'PASS' if rc == 0 else 'FAIL'} — "
          f"{'identical to baseline' if out == baseline else 'DIFFERS FROM BASELINE'}")
    return 0 if all(results) and rc == 0 and out == baseline else 1


if __name__ == "__main__":
    raise SystemExit(main())
