"""Negative tests of the Atlas redesign: Partner and Sources (MER-278).

    python scripts/negative_tests_atlas_partner_sources.py

Empty on purpose until MER-278 lands (MER-275 created the file so the three page threads never collide on a
shared one). Add one case per check you add to your own region of scripts/validate_site.py, with the
harness in scripts/atlas_negative.py:

    suite.case("what the mutation breaks", "path/to/file", swap("old text", "new text"), "text of the expected ERROR")

Run from a detached worktree of the committed HEAD, one suite at a time.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from atlas_negative import Suite, regex, swap  # noqa: E402,F401

suite = Suite("Atlas negative tests - Partner and Sources (MER-278)")

if __name__ == "__main__":
    raise SystemExit(suite.run())
