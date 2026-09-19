#!/usr/bin/env python3
"""WEB-005B B-VIS-13: prove the homepage's visible copy was not rewritten.

    py -3.14 scripts/check_copy_preservation.py [baseline-ref]

Repository copy is frozen input for WEB-005B: the visual work may re-lay it out, but not reword
it. This compares the working tree against a baseline commit (default: the terminal WEB-005A
implementation HEAD) on three axes and prints every difference, so any change has to be declared
rather than discovered:

1. every EN and TR dictionary value in script.js;
2. every data-i18n* key the homepage references, and the static text it renders for each;
3. the homepage's visible text nodes, normalised for whitespace.

Exit status is 0 when nothing changed, 1 when something did. A non-zero exit is not automatically
a failure — an accessibility-driven alt-text change is legitimate — but it must appear in the
review package.
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASELINE = "1135e7a7e0b0f6db6348dee139d505550d8ca8b9"
SKIP_TEXT_IN = {"script", "style", "title"}


def at(ref: str, path: str) -> str:
    out = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT, capture_output=True)
    if out.returncode:
        raise SystemExit(f"cannot read {path} at {ref}: {out.stderr.decode(errors='replace')}")
    return out.stdout.decode("utf-8").replace("\r\n", "\n")


def now(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").replace("\r\n", "\n")


def dictionaries(script: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for lang in ("en", "tr"):
        block = re.search(rf"\n  {lang}: \{{(.*?)\n  \}},?\n", script, re.S)
        out[lang] = dict(re.findall(r"^\s+'([^']+)':\s*(?:'(.*?)'|\"(.*?)\"),?\s*$", block.group(1), re.M)
                         and [(k, a or b) for k, a, b in
                              re.findall(r"^\s+'([^']+)':\s*(?:'(.*?)'|\"(.*?)\"),?\s*$", block.group(1), re.M)])
    return out


class Copy(HTMLParser):
    """Visible text and the i18n binding of every element that carries one."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.bound: dict[str, str] = {}
        self.attrs_by_key: dict[str, str] = {}
        self.text: list[str] = []
        self._key: list[str | None] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.stack.append(tag)
        self._key.append(a.get("data-i18n"))
        for name, value in a.items():
            if name.startswith("data-i18n") and name != "data-i18n":
                target = {"data-i18n-alt": "alt", "data-i18n-aria-label": "aria-label",
                          "data-i18n-content": "content", "data-i18n-href": "href"}.get(name, name)
                self.attrs_by_key[f"{value} -> @{target}"] = a.get(target, "")
        if tag in ("br", "img", "meta", "link", "input", "source"):
            self.stack.pop()
            self._key.pop()

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
            self._key.pop()

    def handle_data(self, data):
        if any(t in SKIP_TEXT_IN for t in self.stack):
            return
        clean = " ".join(data.split())
        if not clean:
            return
        self.text.append(clean)
        for key in reversed(self._key):
            if key:
                self.bound[key] = (self.bound.get(key, "") + " " + clean).strip()
                break


def report(title: str, old: dict[str, str], new: dict[str, str]) -> int:
    changes = 0
    for key in sorted(set(old) | set(new)):
        a, b = old.get(key), new.get(key)
        if a == b:
            continue
        changes += 1
        if a is None:
            print(f"  ADDED   {title} {key!r}\n            + {b}")
        elif b is None:
            print(f"  REMOVED {title} {key!r}\n            - {a}")
        else:
            print(f"  CHANGED {title} {key!r}\n            - {a}\n            + {b}")
    return changes


def main() -> int:
    ref = sys.argv[1] if len(sys.argv) > 1 else BASELINE
    print(f"Copy preservation: working tree vs {ref[:12]}")
    changes = 0

    old_dict, new_dict = dictionaries(at(ref, "script.js")), dictionaries(now("script.js"))
    for lang in ("en", "tr"):
        changes += report(f"{lang} dictionary", old_dict[lang], new_dict[lang])

    old_page, new_page = Copy(), Copy()
    old_page.feed(at(ref, "index.html"))
    new_page.feed(now("index.html"))
    changes += report("homepage element", old_page.bound, new_page.bound)
    changes += report("homepage attribute", old_page.attrs_by_key, new_page.attrs_by_key)

    old_text, new_text = old_page.text, new_page.text
    if old_text != new_text:
        removed = [t for t in old_text if t not in new_text]
        added = [t for t in new_text if t not in old_text]
        reordered = sorted(old_text) == sorted(new_text)
        if removed or added:
            changes += len(removed) + len(added)
            for t in removed:
                print(f"  REMOVED homepage text\n            - {t}")
            for t in added:
                print(f"  ADDED   homepage text\n            + {t}")
        elif reordered:
            print("  NOTE    homepage text is identical but appears in a different document order")

    print(f"\n{changes} visible-copy difference(s)")
    return 0 if changes == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
