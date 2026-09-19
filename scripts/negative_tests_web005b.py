"""Deliberately break each WEB-005B invariant and confirm scripts/validate_site.py catches it.

    py -3.14 scripts/negative_tests_web005b.py

Same discipline as scripts/negative_tests_web005.py: each case mutates one real file, runs the site
validator, and restores the file from the in-memory original in a `finally` block. A case counts
as CAUGHT only when the validator fails with the expected text on an ERROR line the unmutated
baseline did not already print. The run ends by proving the restored tree validates identically.
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(".").resolve()
INDEX = ROOT / "index.html"
PILOT = ROOT / "pilot" / "index.html"
SOURCES = ROOT / "assets" / "imagery" / "sources.json"
STYLES = ROOT / "styles.css"
SCRIPT = ROOT / "script.js"


def site() -> tuple[int, str]:
    r = subprocess.run([sys.executable, "scripts/validate_site.py"], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


CASES = []


def case(name, path, mutate, expect):
    CASES.append((name, path, mutate, expect))


def manifest(fn):
    def apply(t):
        d = json.loads(t)
        fn(d["web_005b"])
        return json.dumps(d, indent=2, ensure_ascii=False) + "\n"
    return apply


def layer(key, fn):
    return manifest(lambda w: fn(w["analytical"]["layers"][key]))


# ---- B-VIS-04 governed pixels ---------------------------------------------------------------
case("governed source swapped for another raster", SOURCES,
     layer("priority", lambda l: l.update(source_sha256="1" * 64)), "not the MER-108 pinned raster")
case("THM-01 re-normalized with a display window", SOURCES,
     layer("thm01", lambda l: l.update(normalization="display_window_p98")), "is not the canonical")
case("priority stretched off the fixed 0-100 range", SOURCES,
     layer("priority", lambda l: l["resolved"].update(vmax=80.0)), "fixed 0-100")
case("THM-01 centre shifted", SOURCES,
     layer("thm01", lambda l: l["resolved"].update(center=0.4)), "symmetric about a 0.0 centre")
case("palette stops reversed (value-to-colour inverted)", SOURCES,
     layer("priority", lambda l: l.update(stops=list(reversed(l["stops"])))), "LUT checksum does not match")
case("palette topology renamed", SOURCES,
     layer("alt01", lambda l: l.update(topology_id="alt_batlow_v2")), "palette topology is not")
case("analytical opacity washed out by the context", SOURCES,
     layer("priority", lambda l: l.update(analytical_opacity=0.7)), "outside 0.9-1.0")
case("a hero-only transform (unsharp) used on the homepage", SOURCES,
     manifest(lambda w: w["analytical"]["not_used"].remove("unsharp")), "hero-only transform")
case("derivative checksum drift", SOURCES,
     layer("terrain", lambda l: l["derivatives"][0].update(sha256="0" * 64)), "checksum mismatch")
case("derivative recorded above the native grid (upsampled)", SOURCES,
     layer("alt01", lambda l: l["derivatives"][0].update(width=1600)), "above the native 1200 px grid")
case("derivative recorded as a lossy encode", SOURCES,
     layer("thm01", lambda l: l["derivatives"][1].update(format="image/webp")), "not a lossless encode")

# ---- B-VIS-02 Act 2 provenance and geometry --------------------------------------------------
case("context photograph checksum drift", SOURCES,
     manifest(lambda w: w["context"]["derivatives"][0].update(sha256="0" * 64)), "checksum mismatch")
case("context photograph claims a different product", SOURCES,
     manifest(lambda w: w["context"]["source"].update(product_ids=["LC09_L2SP_179034_20250513_02_T1"])),
     "not the recorded USGS Landsat product")
case("context derivative wider than its native frame", SOURCES,
     manifest(lambda w: w["context"]["derivatives"][0].update(width=4000)), "wider than the native frame")
case("AOI corner marks drift off the analysis grid", STYLES,
     lambda t: t.replace(".aoi-mark{position:absolute;left:16.9063%", ".aoi-mark{position:absolute;left:20%", 1),
     "do not match the recorded analysis-grid")

# ---- B-VIS-05 tokens ------------------------------------------------------------------------
case("Product cyan token drifts", STYLES,
     lambda t: t.replace("--orb-cyan:#73E7FF;", "--orb-cyan:#43BFF0;", 1), "palette token --orb-cyan")
case("a palette token is redefined a second time", STYLES,
     lambda t: t.replace(".act{--act-inline:", ".act{--orb-surface:#101010;--act-inline:", 1),
     "palette token --orb-surface")

# ---- B-VIS-06 / B-VIS-08 priority semantics and legend ---------------------------------------
case("priority public label reworded", SCRIPT,
     lambda t: t.replace("'label.priority': 'Remote-Sensing Relative Priority — Experimental Baseline'",
                         "'label.priority': 'Geothermal Priority'", 1), "priority public label changed")
case("priority warning dropped from the static page", INDEX,
     lambda t: re.sub(r'(<p class="act-note beam-note" data-i18n="act.priority.note">)[^<]*(</p>)',
                      r"\1Screening only.\2", t, count=1), "lost required wording")
case("detached colour strip returns to the homepage", INDEX,
     lambda t: t.replace('<div class="priority-legend">', '<div class="scale-strip"></div><div class="priority-legend">', 1),
     "detached scientific scale strip")
case("legend moved out of the result figure", INDEX,
     lambda t: t.replace('src="assets/proof/web005b/priority-legend-ramp.png"', 'src=""', 1)
                .replace("    <!-- PILOT:", '    <img src="assets/proof/web005b/priority-legend-ramp.png" alt="" />\n    <!-- PILOT:', 1),
     "legend must sit inside the result figure")

# ---- B-VIS-07 safe density ------------------------------------------------------------------
case("result map CSS cap widened past native density", STYLES,
     lambda t: t.replace(".priority-frame{position:relative;width:100%;max-width:600px", ".priority-frame{position:relative;width:100%;max-width:800px", 1),
     "must be capped")
case("evidence placement laid out past native density", SOURCES,
     manifest(lambda w: w["placement"]["alt01"]["rendered"].update(max_css_width=700)), "above its native")

# ---- R3 delivery encoding --------------------------------------------------------------------
# Terrain is the layer that ships a lossy delivery encode; the other three stayed lossless, so the
# lossy-specific cases target terrain and the structural ones target whichever layer shows them.
def delivery(key, index, fn):
    return manifest(lambda w: fn(w["analytical"]["delivery"]["layers"][key][index]))


case("delivery file checksum drift", SOURCES,
     delivery("terrain", 0, lambda e: e.update(sha256="0" * 64)), "checksum mismatch")
case("delivery claims a fidelity it does not have", SOURCES,
     delivery("terrain", 0, lambda e: e["decoded_comparison"].update(value_shift_max_pct=9.0)),
     "exceeds the declared limit")
case("delivery colour drifts off the governed ramp (ringing)", SOURCES,
     delivery("terrain", 1, lambda e: e["decoded_comparison"].update(offramp_max=40.0)),
     "exceeds the declared limit")
case("delivery contaminates NoData with analytical colour", SOURCES,
     delivery("terrain", 2, lambda e: e["decoded_comparison"].update(nodata_chroma_max=25)),
     "exceeds the declared limit")
case("delivery is not smaller than its lossless reference", SOURCES,
     delivery("terrain", 0, lambda e: e.update(bytes=e["reference_bytes"] + 1)),
     "not smaller than the lossless")
case("delivery references another layer's raster", SOURCES,
     delivery("terrain", 0, lambda e: e.update(reference="assets/proof/web005b/thm01-1200.webp")),
     "reference is not a lossless derivative of this layer")
case("lossy delivery ships with no decoded comparison", SOURCES,
     delivery("terrain", 1, lambda e: e.pop("decoded_comparison")), "no decoded comparison")
case("a lossy delivery is recorded as lossless", SOURCES,
     delivery("terrain", 0, lambda e: e.update(format="image/webp (lossless)")),
     "must be recorded as lossy")
case("delivery recorded above the native grid", SOURCES,
     delivery("thm01", 1, lambda e: e.update(width=1600)), "above the native 1200 px grid")
case("a delivery width is dropped", SOURCES,
     manifest(lambda w: w["analytical"]["delivery"]["layers"]["alt01"].pop()),
     "does not cover the same widths")
case("the coupled legend is re-encoded lossy", SOURCES,
     manifest(lambda w: w["analytical"]["layers"]["priority"]["legend"].update(
         path="assets/proof/web005b/priority-legend-ramp.webp")),
     "legend must stay lossless")

# ---- B-VIS-14 homepage-only -----------------------------------------------------------------
case("a WEB-005B asset leaks onto /pilot/", PILOT,
     lambda t: t.replace("</main>", '<img src="/assets/proof/web005b/terrain-600.webp" alt="" /></main>', 1),
     "published beyond the homepage")


def main() -> int:
    code, baseline = site()
    print(f"Baseline (nothing mutated): site exit {code} — {'PASS' if code == 0 else 'FAIL'}")

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
