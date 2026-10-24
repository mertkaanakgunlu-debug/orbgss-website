"""Shared harness of the Atlas redesign's negative tests (MER-275).

Each negative_tests_atlas_<group>.py declares cases on a Suite and ends with `raise SystemExit(suite.run())`.
A case mutates ONE real file in memory, runs scripts/validate_site.py and restores the file in a
`finally` block. It counts as CAUGHT only when the validator fails with the expected text on an ERROR
line the unmutated baseline did not already print. The run ends by proving the restored tree validates
identically. Run one suite at a time, from a detached worktree of the committed HEAD, never in parallel.
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(".").resolve()
VALIDATOR = "scripts/validate_site.py"


def site() -> tuple[int, str]:
    r = subprocess.run([sys.executable, VALIDATOR], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def swap(old: str, new: str):
    """Replace the first occurrence of `old`; the case fails loudly when `old` is not there."""
    def apply(text: str) -> str:
        if old not in text:
            raise AssertionError(f"mutation target not found: {old[:70]!r}")
        return text.replace(old, new, 1)
    return apply


def regex(pattern: str, new: str, flags: int = 0):
    def apply(text: str) -> str:
        out, n = re.subn(pattern, new, text, count=1, flags=flags)
        if not n:
            raise AssertionError(f"mutation pattern not found: {pattern[:70]!r}")
        return out
    return apply


class Suite:
    def __init__(self, title: str):
        self.title = title
        self.cases: list[tuple[str, pathlib.Path, object, str]] = []

    def case(self, name: str, path: str | pathlib.Path, mutate, expect: str) -> None:
        self.cases.append((name, ROOT / path, mutate, expect))

    def run(self) -> int:
        print(self.title + "\n")
        rc, baseline = site()
        if rc != 0:
            print("baseline tree does not validate; refusing to run")
            print(baseline)
            return 1

        def failed_with(text: str, blob: str) -> bool:
            return any(text.lower() in ln.lower() for ln in blob.splitlines() if ln.startswith("ERROR"))

        results = []
        for name, path, mutate, expect in self.cases:
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
        print(f"Restored tree: site exit {rc} - {'PASS' if rc == 0 else 'FAIL'} - "
              f"{'identical to baseline' if out == baseline else 'DIFFERS FROM BASELINE'}")
        return 0 if all(results) and rc == 0 and out == baseline else 1
