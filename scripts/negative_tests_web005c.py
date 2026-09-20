"""Deliberately break each WEB-005C taxonomy invariant and confirm validate_site.py catches it.

    py -3.14 scripts/negative_tests_web005c.py

WEB-005C / MER-149 converged the public site on one domain taxonomy — Geothermal / Mining /
Marine — and kept the superseded /solutions/ anchors (#mineral, #environment) resolvable as
aliases so existing deep links still land on the domain they always meant.

Same discipline as scripts/negative_tests_web005.py and ...web005b.py: each case mutates one real
file, runs the site validator, and restores the file from the in-memory original in a `finally`
block. A case counts as CAUGHT only when the validator fails with the expected text on an ERROR
line the unmutated baseline did not already print. The run ends by proving the restored tree
validates identically to the baseline.
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(".").resolve()
INDEX = ROOT / "index.html"
PLATFORM = ROOT / "platform" / "index.html"
COMPANY = ROOT / "company" / "index.html"
SOLUTIONS = ROOT / "solutions" / "index.html"
SCRIPT = ROOT / "script.js"


def site() -> tuple[int, str]:
    r = subprocess.run([sys.executable, "scripts/validate_site.py"], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


CASES = []


def case(name, path, old, new, expect):
    def mutate(text):
        assert text.count(old) >= 1, "mutation source not present: " + name
        return text.replace(old, new, 1)
    CASES.append((name, path, mutate, expect))


# --- route compatibility: the superseded anchors must keep resolving -------------------------
case("legacy #mineral deep link stops resolving", SOLUTIONS,
     '<span class="anchor-alias" id="mineral" aria-hidden="true"></span>\n          ', "",
     "legacy anchor #mineral no longer resolves")
case("legacy #environment deep link stops resolving", SOLUTIONS,
     '<span class="anchor-alias" id="environment" aria-hidden="true"></span>\n          ', "",
     "legacy anchor #environment no longer resolves")

# --- the canonical rows themselves ------------------------------------------------------------
case("the /solutions/ #mining row anchor drifts", SOLUTIONS,
     '<li class="ledger-row" id="mining">', '<li class="ledger-row" id="mining-exploration">',
     "no #mining row")
case("the /solutions/ #marine row anchor drifts", SOLUTIONS,
     '<li class="ledger-row" id="marine">', '<li class="ledger-row" id="marine-intelligence">',
     "no #marine row")

# --- the navigation publishes the taxonomy on every route -------------------------------------
case("the nav republishes a superseded label", INDEX,
     '<a href="/solutions/#mining" data-i18n="nav.mining">Mining</a>',
     '<a href="/solutions/#mining" data-i18n="nav.mining">Mineral Exploration</a>',
     "superseded domain label")
case("the nav taxonomy order is swapped", PLATFORM,
     '<li><a href="/solutions/#mining" data-i18n="nav.mining">Mining</a></li>\n'
     '              <li><a href="/solutions/#marine" data-i18n="nav.marine">Marine</a></li>',
     '<li><a href="/solutions/#marine" data-i18n="nav.marine">Marine</a></li>\n'
     '              <li><a href="/solutions/#mining" data-i18n="nav.mining">Mining</a></li>',
     "not the canonical taxonomy in order")
case("a nav item points away from its domain row", INDEX,
     '<a href="/solutions/#marine" data-i18n="nav.marine">Marine</a>',
     '<a href="/solutions/#mining" data-i18n="nav.marine">Marine</a>',
     "not the canonical taxonomy in order")

# --- the names themselves, in both languages ---------------------------------------------------
case("the EN domain name reverts in the dictionary", SCRIPT,
     "'nav.mining': 'Mining',", "'nav.mining': 'Mineral Exploration',",
     "not the canonical public domain name")
case("the TR domain name reverts in the dictionary", SCRIPT,
     "'nav.marine': 'Denizel',", "'nav.marine': 'Çevre ve Arazi Zekâsı',",
     "superseded domain label")
case("the /solutions/ row heading reverts in EN", SCRIPT,
     "'app.mining.title': 'Mining',", "'app.mining.title': 'Mineral Exploration',",
     "superseded domain label")
case("the /solutions/ row heading reverts in TR", SCRIPT,
     "'app.marine.title': 'Denizel',", "'app.marine.title': 'Maden Arama',",
     "superseded domain label")

# --- superseded vocabulary must not return through body copy either ----------------------------
case("a superseded label returns through /company/ body copy", COMPANY,
     "extend into mining and marine domains",
     "extend into Mineral Exploration and Environmental &amp; Land Intelligence",
     "superseded domain label")
case("a superseded label returns through the TR dictionary", SCRIPT,
     "'solutionsPage.meta.ogDescription': 'Tek bir kanıttan önceliğe deseni. "
     "Önce aktif jeotermal; ardından madencilik ve denizel.',",
     "'solutionsPage.meta.ogDescription': 'Tek bir kanıttan önceliğe deseni. "
     "Önce aktif jeotermal; ardından Maden Arama.',",
     "superseded domain label")


def main() -> int:
    print("WEB-005C negative tests — public domain taxonomy parity\n")
    rc, baseline = site()
    if rc != 0:
        print("baseline tree does not validate; refusing to run")
        print(baseline)
        return 1

    def failed_with(text, blob):
        return any(text.lower() in ln.lower() for ln in blob.splitlines() if ln.startswith("ERROR"))

    results = []
    for name, path, mutate, expect in CASES:
        original = path.read_text(encoding="utf-8")
        try:
            mutated = mutate(original)
            assert mutated != original, "mutation was a no-op: " + name
            path.write_text(mutated, encoding="utf-8")
            rc, out = site()
            caught = rc != 0 and failed_with(expect, out) and not failed_with(expect, baseline)
            results.append(caught)
            print(f"  {'CAUGHT ' if caught else 'MISSED '} {name} (exit {rc})")
            if not caught:
                print("     expected text: " + repr(expect))
                for line in out.splitlines():
                    if line.startswith("ERROR"):
                        print("     " + line[:160])
        finally:
            path.write_text(original, encoding="utf-8")
    print()
    print(f"{sum(results)}/{len(results)} deliberate regressions caught")
    rc, out = site()
    print(f"Restored tree: site exit {rc} — {'PASS' if rc == 0 else 'FAIL'} — "
          f"{'identical to baseline' if out == baseline else 'DIFFERS FROM BASELINE'}")
    return 0 if all(results) and rc == 0 and out == baseline else 1


if __name__ == "__main__":
    raise SystemExit(main())
