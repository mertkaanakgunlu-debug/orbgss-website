"""Deliberately break each MER-216 media-delivery invariant and confirm validate_site.py catches it.

    py -3.14 scripts/negative_tests_mer216.py

MER-216 replaced the single hero WebM/MP4 pair with a two-tier delivery ladder of the same master
frames (hero/evidence/responsive_media.json), chosen at runtime by script.js before any video byte
is requested. The contract worth guarding: every tier is a recorded, hash-named file; the markup's
ladder is exactly the recorded one; the bare data-hero-webm / data-hero-mp4 pair stays the middle
tier; MP4s are faststart; and script.js keeps the selection and resilience behaviour (one source
attach, decoder and network signals, show-after-first-frame, stall and dropped-frame fallbacks).

Same discipline as scripts/negative_tests_web005*.py: each case mutates one real file, runs the site
validator, and restores the file from the in-memory original in a `finally` block. A case counts as
CAUGHT only when the validator fails with the expected text on an ERROR line the unmutated baseline
did not already print. The run ends by proving the restored tree validates identically.
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(".").resolve()
INDEX = ROOT / "index.html"
SCRIPT = ROOT / "script.js"
SOURCES = ROOT / "assets" / "imagery" / "sources.json"
VALIDATOR = "scripts/validate_site.py"

CASES = []


def case(name, path, mutate, expect):
    CASES.append((name, path, mutate, expect))


def swap(old, new):
    return lambda t: t.replace(old, new, 1)


def site():
    r = subprocess.run([sys.executable, VALIDATOR], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def sources_edit(fn):
    def apply(t):
        d = json.loads(t)
        fn(d["web_005"]["hero_media"])
        return json.dumps(d, indent=2, ensure_ascii=False).replace("\n", "\r\n") + "\r\n"
    return apply


def _rec(media, role):
    return next(m for m in media if m["role"] == role)


# ---- the markup's ladder -----------------------------------------------------------------------
case("the delivery ladder attribute is removed", INDEX,
     lambda t: __import__("re").sub(r"\s*data-hero-tiers='[^']*'", "", t, count=1),
     "delivery ladder")
case("the ladder is not valid JSON", INDEX,
     lambda t: t.replace("data-hero-tiers='[{", "data-hero-tiers='[{{", 1),
     "delivery ladder")
case("a ladder entry points at another tier's file", INDEX,
     lambda t: __import__("re").sub(r'("id":"md","w":1920,"webm":")[^"]+', lambda m: m.group(1) + "assets/hero/" +
                                    __import__("re").search(r'orbgss-hero-1280-[0-9a-f]{8}\.webm', t).group(0), t, count=1),
     "does not match web_005.hero_media")
case("the ladder loses its ascending order", INDEX,
     lambda t: t.replace('"id":"sm","w":1280', '"id":"sm","w":2560', 1),
     "ascending width")
case("the bare webm fallback stops being the 1920 tier", INDEX,
     lambda t: __import__("re").sub(r'data-hero-webm="[^"]+"', lambda m: 'data-hero-webm="assets/hero/' +
                                    __import__("re").search(r'orbgss-hero-1280-[0-9a-f]{8}\.webm', t).group(0) + '"', t, count=1),
     "must be the 1920 (md) tier")

# ---- the records -------------------------------------------------------------------------------
case("an encode's recorded hash no longer matches its immutable-cache file name", SOURCES,
     sources_edit(lambda media: _rec(media, "hero-webm-md").__setitem__("sha256", "0" * 64)),
     "must be named orbgss-hero-")
case("a tier record is dropped", SOURCES,
     sources_edit(lambda media: media.remove(_rec(media, "hero-mp4-sm"))),
     "has no 'hero-mp4-sm' record")
case("the 1920 WebM is recorded over the binding 3.0 MiB envelope", SOURCES,
     sources_edit(lambda media: _rec(media, "hero-webm-md").__setitem__("bytes", 4 * 1024 * 1024)),
     "byte size mismatch")
case("a ladder codec string drifts from the recorded encode", SOURCES,
     sources_edit(lambda media: _rec(media, "hero-webm-sm").__setitem__("codec_string", "vp09.00.10.08")),
     "codec string differs")

# ---- the runtime -------------------------------------------------------------------------------
for token, expect in (
    ("mediaCapabilities", "mediaCapabilities"),
    ("connection.downlink", "connection.downlink"),
    ("requestVideoFrameCallback", "requestVideoFrameCallback"),
    ("settleStatic('buffering')", "buffering"),
    ("settleStatic('dropped-frames')", "dropped-frames"),
    ("settleStatic('no-video-frame')", "no-video-frame"),
):
    case(f"script.js loses {token}", SCRIPT,
         (lambda tok: lambda t: t.replace(tok, "ZZ" + tok[2:]))(token),
         expect)
case("script.js drops the network gate from the candidate loop (an alternate codec could skip its 1.5x margin)", SCRIPT,
     lambda t: t.replace("if (!networkOk(candidate.tier, candidate.codec)) {", "if (false) {", 1),
     "gate every candidate on networkOk")
case("script.js drops the decoder verdict from the candidate loop (an alternate codec could skip its capability check)", SCRIPT,
     lambda t: t.replace("return decoderAccepts(candidate, deadline).then((ok) => {", "return Promise.resolve(true).then((ok) => {", 1),
     "gate every candidate on networkOk")
case("script.js returns a second delivery straight from a failed query", SCRIPT,
     lambda t: t.replace("refusal = 'decoder-refused';", "refusal = 'decoder-refused'; return { tier: candidate.tier, codec: candidate.codec, src: candidate.tier[candidate.codec], type: 'video/mp4' };", 1),
     "exactly one place")
case("script.js attaches a hero video source in a second place", SCRIPT,
     lambda t: t.replace("    video.muted = true;", "    video.setAttribute('src', choice.src);\r\n    video.muted = true;", 1),
     "exactly one place")


def main() -> int:
    print("MER-216 negative tests — media delivery ladder and runtime contract\n")
    rc, baseline = site()
    if rc != 0:
        print("baseline tree does not validate; refusing to run")
        print(baseline)
        return 1

    def failed_with(text, blob):
        return any(text.lower() in ln.lower() for ln in blob.splitlines() if ln.startswith("ERROR"))

    results = []
    for name, path, mutate, expect in CASES:
        original = path.read_bytes().decode("utf-8")
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
            path.write_bytes(original.encode("utf-8"))
    print()
    print(f"{sum(results)}/{len(results)} deliberate regressions caught")
    rc, out = site()
    print(f"Restored tree: site exit {rc} — {'PASS' if rc == 0 else 'FAIL'} — "
          f"{'identical to baseline' if out == baseline else 'DIFFERS FROM BASELINE'}")
    return 0 if all(results) and rc == 0 and out == baseline else 1


if __name__ == "__main__":
    raise SystemExit(main())
