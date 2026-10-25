#!/usr/bin/env python3
"""Generate the static Turkish pages under /tr/ from the English pages and the I18N dictionary.

    py -3.14 scripts/build_tr_pages.py            # write /tr/, sitemap.xml and the 404 Turkish lines
    py -3.14 scripts/build_tr_pages.py --check    # exit 1 if anything on disk differs from a fresh build

MER-241 (docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md, decision D2). Local tooling in the same spirit as
scripts/build_web005b_presentation.py: Python standard library only, never a site runtime
dependency, and nothing runs on Vercel. The committed output is what is deployed.

Inputs
    * the six English route files (index.html, solutions/index.html, ...). Each translatable
      string in them is a data-i18n* attribute plus its English fallback text;
    * the `I18N` dictionary in script.js. It stays the single source of both languages. The browser
      no longer applies it (MER-241); this script does, once, at build time.

Outputs (all committed)
    * tr/index.html, tr/cozumler/index.html, tr/cozumler/jeotermal/index.html,
      tr/hakkimizda/index.html, tr/is-birligi/index.html, tr/kaynaklar/index.html (MER-255) - the English markup with every
      data-i18n* string replaced by its Turkish value, <html lang="tr">, Turkish canonical /
      og:url / og:locale, every internal link pointing at the Turkish equivalent, the EN | TR
      switch pointing at the English twin, and root-absolute asset URLs (the homepage uses
      document-relative ones, which would break one directory down);
    * sitemap.xml - both languages, with xhtml:link alternates;
    * the Turkish lines of 404.html (the elements marked lang="tr"): one 404 serves every path on
      Vercel, so it answers in both languages instead of being duplicated under /tr/.

No generated-file comment. The pages carry no HTML comment at all (CTO, 2026-10-25: the page source does not
publish working notes); the "generated, do not edit by hand" rule is in CLAUDE.md and in the validator's
byte-identity check.

Strictness. A missing Turkish key, an internal link with no Turkish equivalent, or a document-
relative URL the script cannot make root-absolute stops the build; nothing falls back to English
silently. The output is deterministic (no clock, no environment): a second run is byte-identical.
"""
from __future__ import annotations

import pathlib
import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = "https://orbgss.com"
# The date the language pair last changed meaningfully. A constant, not the clock: the output must
# be reproducible. Bump it when a page's content changes.
SITEMAP_LASTMOD = "2026-10-19"


@dataclass(frozen=True)
class Page:
    route: str       # "" for the homepage, otherwise "solutions/geothermal"
    en_file: str     # English source, relative to the repository root
    en_url: str      # "/solutions/geothermal/"
    tr_url: str      # "/tr/cozumler/jeotermal/"

    @property
    def tr_file(self) -> str:
        return self.tr_url.strip("/") + "/index.html"


# MER-238 decision D2 (2026-10-15): Turkish slugs, ASCII only. Anchor ids are never translated, so
# every alias (#mineral, #pilot-structure, ...) keeps working under /tr/ unchanged.
PAGES = (
    Page("", "index.html", "/", "/tr/"),
    Page("solutions", "solutions/index.html", "/solutions/", "/tr/cozumler/"),
    Page("solutions/geothermal", "solutions/geothermal/index.html", "/solutions/geothermal/",
         "/tr/cozumler/jeotermal/"),
    Page("about", "about/index.html", "/about/", "/tr/hakkimizda/"),
    Page("partner", "partner/index.html", "/partner/", "/tr/is-birligi/"),
    # MER-255: the Data sources and attributions register (footer link target).
    Page("sources", "sources/index.html", "/sources/", "/tr/kaynaklar/"),
)
EN_TO_TR = {p.en_url: p.tr_url for p in PAGES}
TR_DIR = "tr"
ERROR_PAGE = "404.html"

# data-i18n-<x> attribute -> the attribute it fills. data-i18n fills the text, data-i18n-html the
# inner markup (static, trusted strings), exactly as script.js used to at runtime.
ATTR_MAP = (
    ("data-i18n-alt", "alt"),
    ("data-i18n-aria-label", "aria-label"),
    ("data-i18n-content", "content"),
    ("data-i18n-href", "href"),
)
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param",
             "source", "track", "wbr"}
# Attributes whose value is (or contains) a URL the browser resolves against the document. On the
# homepage some of them are document-relative ("assets/hero/..."); one directory down they must be
# root-absolute.
URL_ATTRS = ("href", "src", "srcset", "imagesrcset", "poster", "data-src", "data-srcset",
             "data-hero-webm", "data-hero-mp4", "data-hero-tiers")
ROOT_FILES = ("styles.css", "script.js", "site.webmanifest")


class BuildError(Exception):
    pass


# ---------------------------------------------------------------------------------------------
# The dictionary
# ---------------------------------------------------------------------------------------------
_ENTRY = re.compile(
    r"""^\s*'(?P<key>[^']+)':\s*(?:'(?P<single>(?:[^'\\]|\\.)*)'|"(?P<double>(?:[^"\\]|\\.)*)"|(?P<const>[A-Za-z_]\w*))\s*,?\s*$"""
)
_ESCAPES = {"n": "\n", "t": "\t", "'": "'", '"': '"', "\\": "\\"}


def _unescape(raw: str) -> str:
    return re.sub(r"\\(.)", lambda m: _ESCAPES.get(m.group(1), m.group(1)), raw)


def load_dictionary(script_text: str) -> dict[str, dict[str, str]]:
    """Read `const I18N = { en: {...}, tr: {...} }` from script.js (a flat key -> string map each)."""
    consts = {name: _unescape(value) for name, _, value in
              re.findall(r"const\s+([A-Za-z_]\w*)\s*=\s*(['\"])(.*?)\2\s*;", script_text)}
    dictionary: dict[str, dict[str, str]] = {}
    for lang in ("en", "tr"):
        match = re.search(rf"\n  {lang}: \{{(.*?)\n  \}},?\n", script_text, re.S)
        if not match:
            raise BuildError(f"could not locate the {lang!r} block of the I18N dictionary in script.js")
        block = re.sub(r"/\*.*?\*/", "", match.group(1), flags=re.S)
        entries: dict[str, str] = {}
        for line in block.splitlines():
            if not line.strip() or line.strip().startswith("//"):
                continue
            entry = _ENTRY.match(line)
            if not entry:
                raise BuildError(f"unrecognised line in the {lang!r} dictionary: {line.strip()[:100]!r}")
            if entry.group("const") is not None:
                if entry.group("const") not in consts:
                    raise BuildError(f"{entry.group('key')!r} names the unknown constant "
                                     f"{entry.group('const')!r}")
                value = consts[entry.group("const")]
            else:
                value = _unescape(entry.group("single") if entry.group("single") is not None
                                  else entry.group("double"))
            entries[entry.group("key")] = value
        dictionary[lang] = entries
    return dictionary


# ---------------------------------------------------------------------------------------------
# Small markup helpers
# ---------------------------------------------------------------------------------------------
def escape_text(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def escape_attr(value: str) -> str:
    return value.replace("&", "&amp;").replace('"', "&quot;")


def _attr_pattern(name: str) -> re.Pattern[str]:
    return re.compile(rf"""(?<![\w-]){re.escape(name)}\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+)""", re.S)


def set_attr(tag: str, name: str, value: str) -> str:
    """Set (or add) attribute `name` on the raw start tag `tag`, written with double quotes."""
    rendered = f'{name}="{escape_attr(value)}"'
    pattern = _attr_pattern(name)
    if pattern.search(tag):
        return pattern.sub(lambda _m: rendered, tag, count=1)
    end = len(tag) - (2 if tag.endswith("/>") else 1)
    head = tag[:end].rstrip()
    return f"{head} {rendered}{' /' if tag.endswith('/>') else ''}>"


def drop_attr(tag: str, name: str) -> str:
    pattern = re.compile(rf"""\s+{re.escape(name)}(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+))?(?=[\s/>])""")
    return pattern.sub("", tag, count=1)


def make_root_absolute(value: str) -> str:
    """Turn document-relative URLs inside one attribute value into root-absolute ones."""
    value = re.sub(r"(?<![\w./%:@#?&=-])(assets/)", r"/\1", value)
    if value in ROOT_FILES:
        return "/" + value
    return value


def map_internal_href(href: str) -> str:
    """The Turkish equivalent of an English internal link, fragment and query kept."""
    if not href.startswith("/") or href.startswith("//"):
        return href
    path, sep, rest = href.partition("#")
    path, qsep, query = path.partition("?")
    if path in EN_TO_TR:
        return EN_TO_TR[path] + (qsep + query if qsep else "") + (sep + rest if sep else "")
    if path.startswith(("/assets/",)) or path in ("/" + f for f in ROOT_FILES) or "." in path.rsplit("/", 1)[-1]:
        return href
    raise BuildError(f"internal link {href!r} has no Turkish equivalent (add its page to PAGES)")


# ---------------------------------------------------------------------------------------------
# The rewriter
# ---------------------------------------------------------------------------------------------
class _Rewriter(HTMLParser):
    """Collect (start, end, replacement) edits over the source text; the source is never re-serialised,
    so everything the script does not touch stays byte-identical."""

    def __init__(self, source: str, dictionary: dict[str, dict[str, str]], page: Page | None,
                 mode: str) -> None:
        super().__init__(convert_charrefs=False)
        self.source = source
        self.dictionary = dictionary
        self.page = page
        self.mode = mode  # "page": translate a whole English page; "sync": only lang="tr" elements
        self.edits: list[tuple[int, int, str]] = []
        self.keys_used: set[str] = set()
        self._line_starts = [0]
        for match in re.finditer(r"\n", source):
            self._line_starts.append(match.end())
        # (tag, inner_start, key, kind) for an element whose content this run replaces; None for the rest.
        self._stack: list[tuple[str, int, str | None, str | None, str | None]] = []

    # -- positions ------------------------------------------------------------------------------
    def _offset(self) -> int:
        line, col = self.getpos()
        return self._line_starts[line - 1] + col

    # -- language of the current element (sync mode) --------------------------------------------
    def _effective_lang(self) -> str:
        for entry in reversed(self._stack):
            if entry[4]:
                return entry[4]
        return "en"

    def _tr(self, key: str) -> str:
        try:
            value = self.dictionary["tr"][key]
        except KeyError:
            raise BuildError(f"i18n key {key!r} has no Turkish value; nothing falls back to English") from None
        self.keys_used.add(key)
        return value

    # -- start tags -----------------------------------------------------------------------------
    def _start(self, tag: str, attrs: list[tuple[str, str | None]], void: bool) -> None:
        raw = self.get_starttag_text()
        start = self._offset()
        if self.source[start:start + len(raw)] != raw:
            raise BuildError(f"internal error: tag position mismatch near {raw[:60]!r}")
        data = {name: (value if value is not None else "") for name, value in attrs}
        lang = data.get("lang") if tag != "html" else None
        effective = lang or self._effective_lang()
        translate = self.mode == "page" or (self.mode == "sync" and effective == "tr")

        new = raw
        if self.mode == "page":
            new = self._rewrite_tag(tag, data, raw)
        elif translate:
            for data_attr, target in ATTR_MAP:
                if data_attr in data:
                    new = set_attr(new, target, self._tr(data[data_attr]))
        if new != raw:
            self.edits.append((start, start + len(raw), new))

        key = data.get("data-i18n")
        html_key = data.get("data-i18n-html")
        inner_key = key or html_key
        if not void and not raw.endswith("/>"):
            self._stack.append((tag, start + len(raw), inner_key if translate else None,
                                "text" if key else ("html" if html_key else None), lang))
        elif inner_key and translate:
            raise BuildError(f"{raw[:60]!r}: a void element cannot carry text")

    def handle_starttag(self, tag, attrs):  # noqa: D401
        self._start(tag, attrs, tag in VOID_TAGS)

    def handle_startendtag(self, tag, attrs):
        self._start(tag, attrs, True)

    def handle_endtag(self, tag):
        # Close the nearest open element of this name (the site's markup closes every element).
        for index in range(len(self._stack) - 1, -1, -1):
            if self._stack[index][0] == tag:
                break
        else:
            return
        entries = self._stack[index:]
        del self._stack[index:]
        _, inner_start, key, kind, _lang = entries[0]
        if key is None:
            return
        inner_end = self._offset()
        original = self.source[inner_start:inner_end]
        if kind == "text" and "<" in original:
            raise BuildError(f"data-i18n={key!r} element holds markup; data-i18n replaces text only")
        value = self._tr(key)
        self.edits.append((inner_start, inner_end, escape_text(value) if kind == "text" else value))

    # -- the whole-page rewrite of one start tag ------------------------------------------------
    def _rewrite_tag(self, tag: str, data: dict[str, str], raw: str) -> str:
        page = self.page
        assert page is not None
        new = raw
        if tag == "html":
            return set_attr(new, "lang", "tr")
        for data_attr, target in ATTR_MAP:
            if data_attr in data:
                new = set_attr(new, target, self._tr(data[data_attr]))
        rel = data.get("rel", "").lower()
        prop = data.get("property", "")
        if tag == "link" and rel == "canonical":
            new = set_attr(new, "href", SITE + page.tr_url)
        elif tag == "meta" and prop == "og:url":
            new = set_attr(new, "content", SITE + page.tr_url)
        elif tag == "meta" and prop == "og:locale":
            new = set_attr(new, "content", "tr_TR")
        elif tag == "meta" and prop == "og:locale:alternate":
            new = set_attr(new, "content", "en_US")
        elif tag == "a" and "lang-btn" in data.get("class", "").split():
            # The EN | TR switch: the English link goes to this page's English twin, the Turkish one
            # to the page itself and carries the current-language mark.
            if data.get("hreflang") == "en":
                new = drop_attr(set_attr(new, "href", page.en_url), "aria-current")
            elif data.get("hreflang") == "tr":
                new = set_attr(set_attr(new, "href", page.tr_url), "aria-current", "true")
            else:
                raise BuildError(f"language link without hreflang: {raw[:80]!r}")
        elif tag == "a" and "href" in data and not (tag == "a" and "data-i18n-href" in data):
            mapped = map_internal_href(data["href"])
            if mapped != data["href"]:
                new = set_attr(new, "href", mapped)
        # Document-relative URLs -> root-absolute, keeping each attribute's own quoting.
        for name in URL_ATTRS:
            pattern = re.compile(rf"""(?<![\w-])({re.escape(name)}\s*=\s*)("[^"]*"|'[^']*')""", re.S)
            match = pattern.search(new)
            if not match:
                continue
            quoted = match.group(2)
            fixed = quoted[0] + make_root_absolute(quoted[1:-1]) + quoted[-1]
            if fixed != quoted:
                new = new[:match.start(2)] + fixed + new[match.end(2):]
        return new


def _apply(source: str, edits: list[tuple[int, int, str]]) -> str:
    ordered = sorted(edits, key=lambda e: e[0])
    for (s1, e1, _), (s2, _e2, _) in zip(ordered, ordered[1:]):
        if s2 < e1:
            raise BuildError("internal error: overlapping edits (a data-i18n element nests another)")
    out = source
    for start, end, replacement in reversed(ordered):
        out = out[:start] + replacement + out[end:]
    return out


def _run(source: str, dictionary, page: Page | None, mode: str) -> tuple[str, set[str]]:
    rewriter = _Rewriter(source, dictionary, page, mode)
    rewriter.feed(source)
    rewriter.close()
    if rewriter._stack:
        raise BuildError(f"unclosed elements at the end of the document: "
                         f"{[entry[0] for entry in rewriter._stack]}")
    return _apply(source, rewriter.edits), rewriter.keys_used


# ---------------------------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------------------------
def render_page(page: Page, en_html: str, dictionary: dict[str, dict[str, str]]) -> str:
    """The Turkish twin of one English page."""
    en_html = en_html.replace("\r\n", "\n")
    out, _ = _run(en_html, dictionary, page, "page")
    if not out.startswith("<!doctype html>\n"):
        raise BuildError(f"{page.en_file}: the page must start with <!doctype html>")
    return out


def sync_error_page(html: str, dictionary: dict[str, dict[str, str]]) -> str:
    """404.html: fill the lang="tr" elements from the Turkish dictionary; everything else is left alone."""
    html = html.replace("\r\n", "\n")
    out, _ = _run(html, dictionary, None, "sync")
    return out


def render_sitemap() -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
             'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for language_urls in ((p, p.en_url) for p in PAGES), ((p, p.tr_url) for p in PAGES):
        for page, url in language_urls:
            lines.append("  <url>")
            lines.append(f"    <loc>{SITE}{url}</loc>")
            lines.append(f"    <lastmod>{SITEMAP_LASTMOD}</lastmod>")
            lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{page.en_url}" />')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="tr" href="{SITE}{page.tr_url}" />')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{page.en_url}" />')
            lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def build(root: pathlib.Path = ROOT) -> dict[str, str]:
    """Every file this script owns, as {relative path: LF text}."""
    dictionary = load_dictionary((root / "script.js").read_text(encoding="utf-8"))
    files: dict[str, str] = {}
    for page in PAGES:
        files[page.tr_file] = render_page(page, (root / page.en_file).read_text(encoding="utf-8"),
                                          dictionary)
    files["sitemap.xml"] = render_sitemap()
    files[ERROR_PAGE] = sync_error_page((root / ERROR_PAGE).read_text(encoding="utf-8"), dictionary)
    return files


def _read(path: pathlib.Path) -> str | None:
    if not path.is_file():
        return None
    return path.read_bytes().decode("utf-8").replace("\r\n", "\n")


def stale_files(root: pathlib.Path, files: dict[str, str]) -> list[str]:
    tr_root = root / TR_DIR
    if not tr_root.is_dir():
        return []
    return sorted(p.relative_to(root).as_posix() for p in tr_root.rglob("*")
                  if p.is_file() and p.relative_to(root).as_posix() not in files)


def main(argv: list[str]) -> int:
    check = "--check" in argv
    try:
        files = build()
    except BuildError as exc:
        print(f"build_tr_pages: {exc}", file=sys.stderr)
        return 2
    drift = [rel for rel, text in files.items() if _read(ROOT / rel) != text]
    stale = stale_files(ROOT, files)
    if check:
        for rel in drift:
            print(f"differs from a fresh build: {rel}")
        for rel in stale:
            print(f"not produced by the build: {rel}")
        print("build_tr_pages --check: " + ("OK, byte-identical" if not (drift or stale) else "DRIFT"))
        return 0 if not (drift or stale) else 1
    for rel in stale:
        (ROOT / rel).unlink()
    for rel in drift:
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(files[rel].encode("utf-8"))
        print(f"wrote {rel}")
    for directory in sorted((ROOT / TR_DIR).rglob("*"), reverse=True) if (ROOT / TR_DIR).is_dir() else []:
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()
    print(f"build_tr_pages: {len(files)} files, {len(drift)} written, {len(stale)} removed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
