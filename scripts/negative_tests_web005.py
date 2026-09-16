"""Deliberately break each WEB-005 invariant and confirm the validators catch it.

    py -3.14 scripts/negative_tests_web005.py

A check nobody has seen fail is a check nobody has tested. WEB-005 added a dozen invariants to
`scripts/validate_site.py` and `hero/scripts/validate_hero.py` -- the four-act contract, the
safe-display-density rule, the hero media envelope, the "no governed raster inside a lossy
encode" rule, the narrowed pre-data guarantee -- and each one is only worth the line it occupies
if it actually fails the build when violated.

Each case mutates one real file, runs the relevant validator, and restores the file from the
in-memory original in a `finally` block, so an exception cannot leave the tree mutated. The
restored-tree check at the end proves that: both validators must produce byte-identical output
to the baseline run.

A case counts as CAUGHT only when the validator emits the expected text on an ERROR/FAIL line
that the baseline run did not already contain -- the hero validator echoes every check label on
success too, so a bare substring match would score a passing check as a caught regression.
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(".").resolve()
INDEX = ROOT / "index.html"
SOURCES = ROOT / "assets" / "imagery" / "sources.json"
SCENE = ROOT / "hero" / "config" / "scene.json"


def run(validator: str) -> tuple[int, str]:
    r = subprocess.run([sys.executable, validator], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def site():
    return run("scripts/validate_site.py")


def hero():
    return run("hero/scripts/validate_hero.py")


CASES = []


def case(name, path, mutate, validator, expect):
    CASES.append((name, path, mutate, validator, expect))


# ---- site validator -------------------------------------------------------------------------
case("act count: drop Act 2's data-act", INDEX,
     lambda t: t.replace(' aria-labelledby="context-title" data-act="2"',
                         ' aria-labelledby="context-title"', 1),
     site, "exactly four acts")

case("evidence trio: add a fourth card", INDEX,
     lambda t: t.replace('<li class="evidence-card" id="alteration"',
                         '<li class="evidence-card" id="extra"></li>\n        '
                         '<li class="evidence-card" id="alteration"', 1),
     site, "exactly three cards")

case("superseded component returns", INDEX,
     lambda t: t.replace('<section id="context" class="act act-context"',
                         '<section id="context" class="act act-context story-section"', 1),
     site, "superseded WEB-001/002 homepage component")

case("hero video gets an eager <source>", INDEX,
     lambda t: t.replace('          tabindex="-1"\n        ></video>',
                         '          tabindex="-1"\n        ><source src="assets/hero/orbgss-hero.webm" '
                         'type="video/webm"></video>', 1),
     site, "eager sources")

case("missing act anchor", INDEX,
     lambda t: t.replace('<section id="priority" class="act act-priority"',
                         '<section id="priority-x" class="act act-priority"', 1),
     site, "missing required section ids")


def widen_placement(t):
    d = json.loads(t)
    for a in d["geo_web_002"]["assets"]:
        if a["id"] == "priority":
            a["web_005_placement"]["rendered"]["max_css_width"] = 900   # 1800 device px at 2x
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("safe density: lay out the priority map past its ceiling", SOURCES, widen_placement,
     site, "exceeds its declared")


def drop_placement(t):
    d = json.loads(t)
    for a in d["geo_web_002"]["assets"]:
        if a["id"] == "thm01":
            a.pop("web_005_placement", None)
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("placed package asset with no placement record", SOURCES, drop_placement,
     site, "no web_005_placement record")


def corrupt_derivative(t):
    d = json.loads(t)
    for a in d["geo_web_002"]["assets"]:
        if a["id"] == "priority":
            a["derivatives"][0]["sha256"] = "0" * 64
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("accepted derivative checksum drift", SOURCES, corrupt_derivative,
     site, "checksum mismatch")


# ---- hero validator -------------------------------------------------------------------------
def bake_science(t):
    d = json.loads(t)
    slot = d["aoi_injection_interface"]["layer_slots"][0]
    slot["render_surface"] = "baked_into_render"
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("layer slot claims the science is baked into the render", SCENE, bake_science,
     hero, "composited in the page, never baked")


def claim_analysis_aoi(t):
    d = json.loads(t)
    d["aoi_injection_interface"]["fixtures"]["kizildere_regional"]["is_analysis_aoi"] = True
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("production fixture claims to be the analysis AOI", SCENE, claim_analysis_aoi,
     hero, "disclaims being the analysis AOI")


def reclassify_design_fixture(t):
    d = json.loads(t)
    d["aoi_injection_interface"]["fixtures"]["design_primary"]["classification"] = "production_regional_frame"
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("accepted design fixture quietly reclassified", SCENE, reclassify_design_fixture,
     hero, "still classified a design fixture")


def science_into_accepted_scene(t):
    d = json.loads(t)
    d["scenes"]["hero_predata_animatic"]["objects"].append({"id": "priority_score_overlay"})
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("scientific layer smuggled into an accepted pre-data scene", SCENE, science_into_accepted_scene,
     hero, "accepted pre-data scenes still declare no scientific layer")


# ---- WEB-005A R2: the visual-fidelity contract has to fail loudly too ----------------------
def faint_lines(t):
    d = json.loads(t)
    d["scenes"]["hero_production_kizildere"]["materials"]["aoi_beam"]["tip_alpha"] = 0.05
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("sensing lines faded to near-invisible", SCENE, faint_lines,
     hero, "sensing-line core is legible")


def slab_lines(t):
    d = json.loads(t)
    aoi = next(o for o in d["scenes"]["hero_production_kizildere"]["objects"] if o["id"] == "aoi")
    aoi["beams"]["tip_radius_km"] = 90.0
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("sensing lines thickened into a slab", SCENE, slab_lines,
     hero, "sensing-line core is thin")


def sensor_claim(t):
    d = json.loads(t)
    sat = next(o for o in d["scenes"]["hero_production_kizildere"]["objects"] if o["id"] == "satellite")
    sat["note"] = sat.get("note", "") + " Depicts a radar swath."
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("production scene claims sensing physics", SCENE, sensor_claim,
     hero, "makes no sensing-physics claim")


def orbit_drift(t):
    d = json.loads(t)
    sat = next(o for o in d["scenes"]["hero_production_kizildere"]["objects"] if o["id"] == "satellite")
    sat["location_keyframes"][3]["location"][0] += 0.05
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("satellite keyframe typed off its derived orbit", SCENE, orbit_drift,
     hero, "match their orbit derivation")


def lock_pulse_removed(t):
    d = json.loads(t)
    aoi = next(o for o in d["scenes"]["hero_production_kizildere"]["objects"] if o["id"] == "aoi")
    aoi["border"]["emphasis"] = [[124, 1.0], [276, 1.0]]
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("target frame lock intensification removed", SCENE, lock_pulse_removed,
     hero, "visible lock intensification")


def anchor_drift(t):
    return t.replace('"x":0.72', '"x":0.62', 1)


case("handoff anchor moved away from the audited frame", INDEX, anchor_drift,
     site, "drifts from the audited last frame")


case("handoff loses the exact public label", INDEX,
     lambda t: t.replace('<span class="hero-handoff-label" data-i18n="label.priority">',
                         '<span class="hero-handoff-label">', 1),
     site, "exact public label")


case("handoff warning detached from the mandatory-warning class", INDEX,
     lambda t: t.replace('class="hero-handoff-note beam-note"', 'class="hero-handoff-note"', 1),
     site, "mandatory priority warning")


def main() -> int:
    # The baseline may legitimately be red while the hero media is still being produced, so the
    # test is not "mutation fails" but "mutation introduces THIS error, which the baseline lacks".
    print("Baseline (nothing mutated):")
    baseline_out = {}
    for label, fn in (("site", site), ("hero", hero)):
        code, out = fn()
        baseline_out[label] = out
        print(f"  {label}: exit {code} — {'PASS' if code == 0 else 'FAIL'}")

    results = []
    for name, path, mutate, validator, expect in CASES:
        original = path.read_text(encoding="utf-8")
        try:
            mutated = mutate(original)
            assert mutated != original, "mutation was a no-op: " + name
            path.write_text(mutated, encoding="utf-8")
            code, out = validator()
            label = "site" if validator is site else "hero"
            # Match the FAILURE line specifically. The hero validator echoes every check label on
            # success too, so a bare substring match would find the expected text in a PASS line.
            def failed_with(text, blob):
                needle = text.lower()
                return any(
                    needle in ln.lower()
                    for ln in blob.splitlines()
                    if ln.startswith("ERROR") or ln.lstrip().startswith("FAIL")
                )
            caught = (code != 0 and failed_with(expect, out)
                      and not failed_with(expect, baseline_out[label]))
            results.append((name, caught, code))
            print(f"  {'CAUGHT ' if caught else 'MISSED '} {name} (exit {code})")
            if not caught:
                print("     expected text: " + repr(expect))
                for line in out.splitlines():
                    if line.startswith("ERROR") or line.startswith("  FAIL"):
                        print("     " + line[:160])
        finally:
            path.write_text(original, encoding="utf-8")

    print()
    caught = sum(1 for _, ok, _ in results if ok)
    print(f"{caught}/{len(results)} deliberate regressions caught")

    print("Restored tree:")
    for label, fn in (("site", site), ("hero", hero)):
        code, out = fn()
        same = out == baseline_out[label]
        print(f"  {label}: exit {code} — {'PASS' if code == 0 else 'FAIL'}"
              f" — {'identical to baseline' if same else 'DIFFERS FROM BASELINE'}")
    return 0 if caught == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
