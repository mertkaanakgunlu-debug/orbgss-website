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
import re
import subprocess
import sys

ROOT = pathlib.Path(".").resolve()
INDEX = ROOT / "index.html"
SOURCES = ROOT / "assets" / "imagery" / "sources.json"
SCENE = ROOT / "hero" / "config" / "scene.json"
STYLES = ROOT / "styles.css"


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
    aoi["border"]["emphasis"] = [[f, min(v, 1.2)] for f, v in aoi["border"]["emphasis"]]
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("target frame lock intensification removed", SCENE, lock_pulse_removed,
     hero, "visible lock intensification")


def anchor_drift(t):
    return re.sub(r'(data-hero-anchor=\'\{[^\']*?"x":)(\d\.\d+)', lambda m: m.group(1) + "0.31", t, count=1)


case("hero anchor moved away from the audited held frame", INDEX, anchor_drift,
     site, "drifts from the audited held frame")


# ---- WEB-005A final production: the visual-only payoff has to fail loudly too -----------------
PAYOFF_IMG = 'data-layer="priority"\n'


case("a layer label returns to the hero", INDEX,
     lambda t: t.replace('<noscript><style>.hero-drape[hidden]',
                         '<span data-i18n="label.priority">x</span><noscript><style>.hero-drape[hidden]', 1),
     site, "a layer label")


case("an in-hero legend returns", INDEX,
     lambda t: t.replace('<noscript><style>.hero-drape[hidden]',
                         '<img class="hero-layer-legend" src="assets/proof/final/priority-legend.png" alt="" /><noscript><style>.hero-drape[hidden]', 1),
     site, "an in-hero legend")


case("the floating handoff card returns", INDEX,
     lambda t: t.replace('<noscript><style>.hero-drape[hidden]',
                         '<figure class="hero-handoff" data-hero-handoff hidden></figure><noscript><style>.hero-drape[hidden]', 1),
     site, "the floating handoff card")


def drop_payoff(t):
    a = t.index('<img\n            class="hero-drape-layer hero-drape-payoff"')
    b = t.index('/>', a) + 2
    return t[:a] + t[b:]


case("hero drape loses the priority payoff state", INDEX, drop_payoff, site, "the accepted order")


case("hero drape state swapped for an unrecorded file", INDEX,
     lambda t: t.replace('data-src="assets/hero/drape/hero-drape-priority-1920.png"',
                         'data-src="assets/proof/final/priority-1249.webp"', 1),
     site, "not its recorded")


def reorder_layers(t):
    return (t.replace('data-layer="thm01" data-src', 'data-layer="__tmp__" data-src', 1)
             .replace('data-layer="alt01" data-src', 'data-layer="thm01" data-src', 1)
             .replace('data-layer="__tmp__" data-src', 'data-layer="alt01" data-src', 1))


case("hero drape states out of the accepted evidence order", INDEX, reorder_layers, site, "the accepted order")


case("a drape state made eager (phones and static visitors would fetch it)", INDEX,
     lambda t: t.replace('data-layer="terrain" data-src=', 'data-layer="terrain" src=', 1),
     site, "data-src only")

case("no-JavaScript payoff removed", INDEX,
     lambda t: re.sub(r'\s*<noscript><img class="hero-drape-layer is-on"[^\n]*</noscript>', '', t, count=1),
     site, "no <noscript> image of the recorded priority state")


def corrupt_drape(t):
    d = json.loads(t)
    d["web_005"]["hero_drape_states"][3]["sha256"] = "0" * 64
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("drape state checksum drift", SOURCES, corrupt_drape, site, "checksum or size mismatch")


def denoised_drape(t):
    d = json.loads(t)
    d["web_005"]["hero_drape_states"][3]["denoise"] = True
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("drape state recorded as denoised (a colour filter on thematic pixels)", SOURCES, denoised_drape,
     site, "no denoiser")


def untied_drape(t):
    d = json.loads(t)
    d["web_005"]["hero_drape_states"][3]["display_texture_sha256"] = "f" * 64
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("drape state not tied to the ingested 4K display texture", SOURCES, untied_drape,
     site, "not tied to an ingested prepared display texture")


case("drape states stop sharing the poster's fit rule", STYLES,
     lambda t: t.replace("object-fit:cover;object-position:center 46%;filter:none;opacity:0", "object-fit:cover;object-position:center 50%;filter:none;opacity:0", 1),
     site, "share the poster's box")


def analysis_span(t):
    d = json.loads(t)
    d["aoi_injection_interface"]["fixtures"]["kizildere_analysis"]["span_km"] = 40.0
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("analysis frame drawn at a span that is not the accepted 36 km", SCENE, analysis_span,
     hero, "accepted 36 km analysis extent")


def constant_rate(t):
    d = json.loads(t)
    sat = next(o for o in d["scenes"]["hero_production_kizildere"]["objects"] if o["id"] == "satellite")
    sat["orbit_intent"].pop("rate_profile", None)
    sat["orbit_intent"]["rate_deg_per_frame"] = 0.7
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("satellite pass no longer settles (constant rate)", SCENE, constant_rate, hero, "time-remapped")


def _production(d):
    scene = d["scenes"]["hero_production_kizildere"]
    return scene, next(o for o in scene["objects"] if o["id"] == "aoi")


def _scene_case(mutate):
    def apply(t):
        d = json.loads(t)
        mutate(*_production(d), d)
        return json.dumps(d, indent=2, ensure_ascii=False) + "\n"
    return apply


# ---- WEB-005A final production: the accepted choreography and the split delivery ---------------------
case("motion render extended into the analytical reveal (analytical pixels in a lossy encode)", SCENE,
     _scene_case(lambda scene, aoi, d: scene["animation"]["delivery"].__setitem__("motion_video_frames", [1, 300])),
     hero, "before any analytical pixel exists")

case("preview-gate alias diverges from the production scene", SCENE,
     _scene_case(lambda scene, aoi, d: d["scenes"]["hero_r3_preview_gate"].__setitem__("frame", 12)),
     hero, "one definition of the choreography")

case("visible lines moved back onto the true 36 km corners (reads as one beam to the middle)", SCENE,
     _scene_case(lambda scene, aoi, d: aoi["beams"].__setitem__("anchor", "true")),
     hero, "four corners of the presentation reticle")

case("reticle starts to tighten while lines are still attached", SCENE,
     _scene_case(lambda scene, aoi, d: aoi["presentation"]["screen_intent"]["morph_frames"].__setitem__(0, 170)),
     hero, "never moves a line anchor while a line is attached")

case("reticle resolves after the lines (target appears afterwards)", SCENE,
     _scene_case(lambda scene, aoi, d: aoi["border"].update({"appear_start_frame": 120, "appear_end_frame": 130})),
     hero, "resolves the reticle before the lines")

case("lines fade in instead of drawing on", SCENE,
     _scene_case(lambda scene, aoi, d: aoi["beams"].pop("draw")),
     hero, "never a fade-in")

case("scan fan no longer between the four lines", SCENE,
     _scene_case(lambda scene, aoi, d: aoi["scan_fan"]["top"].__setitem__("half_length_km", 190.0)),
     hero, "exactly between the four lines")

case("platform resumes its pass while lines are attached", SCENE,
     _scene_case(lambda scene, aoi, d: next(o for o in scene["objects"] if o["id"] == "satellite")["orbit_intent"]["rate_profile"].__setitem__(3, [160, 0.015])),
     hero, "station-keeping rate for as long as any line is attached")

case("caption region shrunk to the bare caption box", SCENE,
     _scene_case(lambda scene, aoi, d: scene["camera"]["composition"]["caption_safe_region_1440"].__setitem__("y1", 0.134)),
     hero, "protects the bottom-right caption")

case("platform-exit bound loosened", SCENE,
     _scene_case(lambda scene, aoi, d: scene["camera"]["composition"]["satellite_exit"].__setitem__("max_width_fraction", 0.29)),
     hero, "fly-by bound at or under 22 percent")

case("masked analytical ground back to a dark neutral", SCENE,
     _scene_case(lambda scene, aoi, d: scene["materials"]["aoi_relief_layers"].pop("underlay_layer")),
     hero, "shows the Terrain context through masked analytical ground")

case("scan palette made pale / milky", SCENE,
     _scene_case(lambda scene, aoi, d: d["palette"].__setitem__("scan_cyan", [0.6, 0.9, 1.0])),
     hero, "is a saturated cyan / teal")

case("analytical sequence stretched into a slideshow", SCENE,
     _scene_case(lambda scene, aoi, d: scene["animation"]["timing_envelope"].__setitem__("analytical_sequence_frames", [276, 398])),
     hero, "timing envelope inside the approved one")


def recolour_gain(t):
    d = json.loads(t)
    d["scenes"]["hero_production_kizildere"]["materials"]["earth_surface"]["detail_sharpen"]["strength"] = 2.5
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


case("Earth detail multiplier pushed beyond a structure gain", SCENE, recolour_gain, hero, "structure gain")


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
