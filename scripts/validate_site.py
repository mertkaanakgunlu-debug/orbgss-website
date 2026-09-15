#!/usr/bin/env python3
"""Fast dependency-free validation for the OrbGSS static website.

This intentionally checks only repository invariants that should remain stable
across routine visual/content edits. It is not a substitute for browser QA.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
HTML = ROOT / "index.html"
MANIFEST = ROOT / "assets" / "imagery" / "sources.json"

REQUIRED_FILES = [
    "index.html",
    "styles.css",
    "script.js",
    "assets/logo.svg",
    "assets/mark.svg",
    "assets/imagery/sources.json",
    "IMAGERY_RIGHTS.md",
    "vercel.json",
    "robots.txt",
    "sitemap.xml",
    # WEB-003 public routes
    "platform/index.html",
    "solutions/index.html",
    "pilot/index.html",
    "company/index.html",
    "contact/index.html",
]

# WEB-003: canonical public route -> its file, relative to ROOT. "" is the homepage.
ROUTES = {
    "": "index.html",
    "platform": "platform/index.html",
    "solutions": "solutions/index.html",
    "pilot": "pilot/index.html",
    "company": "company/index.html",
    "contact": "contact/index.html",
}


def canonical_url(route: str) -> str:
    return f"https://orbgss.com/{route + '/' if route else ''}"

# WEB-001 vNext structure: story anchors, the pilot ledger and the trust/contact zone.
REQUIRED_SECTION_IDS = {
    "platform", "terrain", "evidence", "structure", "priority", "geothermal",
    "pilot", "solutions", "mineral", "environment", "company", "contact",
}
PROHIBITED_COPY = ["how it works"]
# Temporary gallery panels must never be labelled as scientific outputs (WEB-001 acceptance 9).
REQUIRED_TEMP_PANEL_STATUS = "temporary-gallery"
# WEB-002: a story slot is real product proof, an explicit data gap, or still temporary gallery.
ALLOWED_PANEL_STATUS = {REQUIRED_TEMP_PANEL_STATUS, "product-proof", "data-gap"}
# WEB-002 claim discipline: wording that would overstate the accepted MVP score if it ever
# appeared in visible homepage copy. The accepted profile is an AOI-relative screening surface.
PROHIBITED_SCORE_COPY = [
    "full prospectivity",
    "probability of geothermal",
    "drilling success",
    "proven reserve",
    "validated accuracy",
]


def sha256_of(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.img_srcs: list[str] = []
        self.links: list[str] = []
        self.text: list[str] = []
        self.claim_text: list[str] = []
        self.visual_slots: list[tuple[str, str]] = []
        # Static text carried by each data-i18n element, so warning coverage can be proved for a
        # reader with JavaScript disabled, not just for the dictionary.
        self.i18n_text: dict[str, str] = {}
        # Every data-i18n* key this file references, regardless of which attribute carries it
        # (text content, alt, aria-label, meta content, href) — used for site-wide EN/TR parity.
        self.i18n_keys: set[str] = set()
        self._note_depth = 0
        self._open: list[bool] = []
        self._key_stack: list[str | None] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        # A mandatory scientific warning is allowed to name what the score is NOT; ordinary
        # marketing copy is not allowed to use those phrases at all.
        is_note = "beam-note" in str(data.get("class") or "").split()
        self._open.append(is_note)
        if is_note:
            self._note_depth += 1
        key = data.get("data-i18n")
        self._key_stack.append(str(key) if key else None)
        for i18n_attr in ("data-i18n", "data-i18n-alt", "data-i18n-aria-label", "data-i18n-content", "data-i18n-href"):
            attr_key = data.get(i18n_attr)
            if attr_key:
                self.i18n_keys.add(str(attr_key))
        if data.get("id"):
            self.ids.add(str(data["id"]))
        if data.get("data-visual-slot"):
            self.visual_slots.append((str(data["data-visual-slot"]), str(data.get("data-visual-status") or "")))
        if tag == "img" and data.get("src"):
            self.img_srcs.append(str(data["src"]))
        if tag == "a" and data.get("href"):
            self.links.append(str(data["href"]))

    def handle_endtag(self, tag: str) -> None:
        if self._open and self._open.pop():
            self._note_depth -= 1
        if self._key_stack:
            self._key_stack.pop()

    def handle_data(self, data: str) -> None:
        self.text.append(data)
        if self._note_depth == 0:
            self.claim_text.append(data)
        for key in self._key_stack:
            if key:
                self.i18n_text[key] = self.i18n_text.get(key, "") + data


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            fail(f"missing required file: {rel}", errors)

    if errors:
        for item in errors:
            print(f"ERROR: {item}")
        return 1

    html = HTML.read_text(encoding="utf-8")
    parser = SiteParser()
    parser.feed(html)

    missing_ids = REQUIRED_SECTION_IDS - parser.ids
    if missing_ids:
        fail(f"missing required section ids: {sorted(missing_ids)}", errors)

    normalized_text = " ".join(parser.text).lower()
    for phrase in PROHIBITED_COPY:
        if phrase in normalized_text:
            fail(f"prohibited section/copy detected: {phrase!r}", errors)

    if 'href="https://orbgss.com/"' not in html and 'content="https://orbgss.com/"' not in html:
        warnings.append("canonical orbgss.com URL was not detected")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    scenes = manifest.get("scenes", [])
    if len(scenes) != 4:
        fail(f"expected exactly 4 locked scenes, found {len(scenes)}", errors)

    scene_paths: set[str] = set()
    for scene in scenes:
        required = ["id", "role", "location", "coordinates", "acquired", "sensor", "source_data", "local_file"]
        missing = [key for key in required if not scene.get(key)]
        if missing:
            fail(f"scene {scene.get('id', '<unknown>')} missing fields: {missing}", errors)
            continue
        local = str(scene["local_file"])
        scene_paths.add(local)
        # WEB-002 retired the three gallery scenes that used to fill story slots; they keep their
        # provenance and rights but are no longer placed on the homepage.
        placed = str(scene.get("web_vnext_placement", {}).get("status", "")) != "retired-from-homepage"
        if placed and local not in parser.img_srcs:
            fail(f"manifest local_file not referenced by index.html: {local}", errors)
        path = ROOT / local
        if not path.exists():
            warnings.append(f"production imagery not populated yet: {local}")
        elif path.stat().st_size < 50_000:
            fail(f"production imagery unexpectedly small: {local}", errors)

    manifest_html_paths = {src for src in parser.img_srcs if src.startswith("assets/imagery/")}
    extra = manifest_html_paths - scene_paths
    if extra:
        fail(f"HTML imagery paths missing from provenance manifest: {sorted(extra)}", errors)

    # Internal fragment links should resolve to an ID (except #top, which is present today).
    for href in parser.links:
        if href.startswith("#") and len(href) > 1 and href[1:] not in parser.ids:
            fail(f"broken internal fragment link: {href}", errors)

    # Every story panel is a declared visual slot; temporary panels carry the temporary status so
    # WEB-002 can find them and so nobody silently promotes a gallery image to an evidence output.
    story_slots = [slot for slot in parser.visual_slots if slot[0] != "hero"]
    expected_slots = ["observe", "terrain", "evidence", "structure", "priority", "geothermal"]
    if [slot for slot, _ in story_slots] != expected_slots:
        fail(f"story visual slots out of order or missing: {[slot for slot, _ in story_slots]}", errors)
    for slot, status in story_slots:
        if status not in ALLOWED_PANEL_STATUS:
            fail(f"visual slot {slot!r} has unknown data-visual-status {status!r}", errors)

    # ------------------------------------------------------------------
    # WEB-002 product proof: every scientific visual on the page must be an
    # OrbGSS cartographic export recorded here with its export id, the master
    # checksum from that export's manifest, and a checksum of the file we ship.
    # ------------------------------------------------------------------
    web002 = manifest.get("web_002", {})
    proof_assets = web002.get("proof_assets", [])
    proof_paths: set[str] = set()
    if not proof_assets:
        fail("manifest web_002.proof_assets is missing or empty", errors)

    for asset in proof_assets:
        aid = asset.get("id", "<unknown>")
        for key in ("id", "homepage_slot", "public_label", "mandatory_warning", "layer_ids",
                    "source_project", "export", "derivation", "derivatives", "rights_basis"):
            if not asset.get(key):
                fail(f"proof asset {aid!r} missing field: {key}", errors)
        export = asset.get("export", {})
        for key in ("export_id", "export_manifest", "master_file", "master_sha256"):
            if not export.get(key):
                fail(f"proof asset {aid!r} missing export.{key}", errors)
        master = str(export.get("master_sha256", ""))
        if len(master) != 64 or not re.fullmatch(r"[0-9a-f]{64}", master):
            fail(f"proof asset {aid!r} master_sha256 is not a sha256 digest", errors)

        for deriv in asset.get("derivatives", []):
            rel = str(deriv.get("path", ""))
            if not rel:
                fail(f"proof asset {aid!r} has a derivative without a path", errors)
                continue
            proof_paths.add(rel)
            path = ROOT / rel
            if not path.exists():
                fail(f"proof derivative missing from repository: {rel}", errors)
                continue
            recorded = str(deriv.get("sha256", ""))
            actual = sha256_of(path)
            if recorded != actual:
                fail(f"proof derivative checksum mismatch for {rel}: "
                     f"manifest {recorded[:12]}… != file {actual[:12]}…", errors)
            if deriv.get("bytes") not in (None, path.stat().st_size):
                fail(f"proof derivative byte size mismatch for {rel}", errors)

    # ------------------------------------------------------------------
    # Mandatory scientific warnings must be visible on the page, in both languages, and in the
    # static HTML as well as the dictionary — so they survive with JavaScript disabled and cannot
    # be quietly dropped by a later copy edit.
    # ------------------------------------------------------------------
    script = (ROOT / "script.js").read_text(encoding="utf-8")
    lang_blocks: dict[str, str] = {}
    for lang in ("en", "tr"):
        match = re.search(rf"\n  {lang}: \{{(.*?)\n  \}},?\n", script, re.S)
        if match:
            lang_blocks[lang] = match.group(1)
        else:
            fail(f"could not locate the {lang!r} block of the I18N dictionary", errors)

    # A handful of dictionary entries (mailto links) point at a top-level const instead of an
    # inline literal, e.g. 'mail.partner': MAIL_EN — resolve those the same way a JS engine would.
    const_values: dict[str, str] = {}
    for cname, cquote, cvalue in re.findall(r"const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(['\"])(.*?)\2\s*;", script):
        const_values[cname] = cvalue

    def dictionary_value(lang: str, key: str) -> str | None:
        # Keys are always single-quoted (dots make them invalid bare identifiers); values are
        # single-quoted except where the copy itself needs an apostrophe, so try both delimiters.
        block = lang_blocks.get(lang)
        if block is None:
            return None
        escaped_key = re.escape(key)
        for value_quote in ("'", '"'):
            vq = re.escape(value_quote)
            found = re.search(rf"^\s+'{escaped_key}':\s*{vq}(.*?){vq},?\s*$", block, re.M)
            if found:
                return found.group(1)
        const_ref = re.search(rf"^\s+'{escaped_key}':\s*([A-Za-z_][A-Za-z0-9_]*),\s*$", block, re.M)
        if const_ref:
            return const_values.get(const_ref.group(1))
        return None

    for asset in proof_assets:
        aid = asset.get("id", "<unknown>")
        coverage = asset.get("visible_warning")
        if not coverage:
            fail(f"proof asset {aid!r} has no visible_warning record; every mandatory warning "
                 f"must be bound to visible page copy", errors)
            continue
        key = str(coverage.get("i18n_key", ""))
        if not key:
            fail(f"proof asset {aid!r} visible_warning has no i18n_key", errors)
            continue
        static_text = parser.i18n_text.get(key)
        if static_text is None:
            fail(f"proof asset {aid!r} warning key {key!r} is not rendered by index.html", errors)
            continue
        for lang in ("en", "tr"):
            value = dictionary_value(lang, key)
            if value is None:
                fail(f"warning key {key!r} is missing from the {lang!r} dictionary", errors)
                continue
            for term in coverage.get(f"required_terms_{lang}", []):
                if term not in value:
                    fail(f"proof asset {aid!r}: {lang} warning lost required wording {term!r}",
                         errors)
        for term in coverage.get("required_terms_en", []):
            if term not in static_text:
                fail(f"proof asset {aid!r}: static HTML warning under {key!r} lost required "
                     f"wording {term!r} (no-JS readers would not see it)", errors)

    # Nothing scientific may be shown that is not recorded above.
    html_proof_paths = {src for src in parser.img_srcs if src.startswith("assets/proof/")}
    unrecorded = html_proof_paths - proof_paths
    if unrecorded:
        fail(f"HTML proof imagery missing from web_002.proof_assets: {sorted(unrecorded)}", errors)

    # Data-gap slots are declared, so an absent layer can never be quietly filled later.
    gap_slots = {str(gap.get("homepage_slot")) for gap in web002.get("data_gaps", [])}
    for slot, status in story_slots:
        if status == "data-gap" and slot not in gap_slots:
            fail(f"slot {slot!r} is marked data-gap but has no web_002.data_gaps record", errors)
        if status == "product-proof" and not any(
            asset.get("homepage_slot") == slot for asset in proof_assets
        ):
            fail(f"slot {slot!r} is marked product-proof but has no proof asset", errors)

    claim_text = " ".join(parser.claim_text).lower()
    for phrase in PROHIBITED_SCORE_COPY:
        if phrase in claim_text:
            fail(f"overstated score claim outside a mandatory warning: {phrase!r}", errors)

    # Basic anti-regression guard against accidentally reintroducing common card-grid class names.
    suspicious = re.findall(r'class="[^"]*\b(?:card-grid|feature-grid|icon-grid)\b[^"]*"', html, flags=re.I)
    if suspicious:
        fail("generic card/icon grid class detected; conflicts with locked design", errors)

    # ------------------------------------------------------------------
    # WEB-003: public-site depth. Every check above this point is homepage/WEB-002-specific and
    # stays scoped to index.html. Everything below applies across all six canonical public routes,
    # so a new page can never quietly ship a broken link, thin metadata or an EN/TR gap.
    # ------------------------------------------------------------------
    route_parsers: dict[str, SiteParser] = {}
    route_html: dict[str, str] = {"": html}
    route_parsers[""] = parser
    for route, rel in ROUTES.items():
        if route == "":
            continue
        path = ROOT / rel
        if not path.exists():
            continue  # already reported as a missing required file above
        text = path.read_text(encoding="utf-8")
        route_html[route] = text
        route_parser = SiteParser()
        route_parser.feed(text)
        route_parsers[route] = route_parser

    # Metadata: every route needs a truthful, route-specific title/description/canonical/OG url.
    for route, text in route_html.items():
        label = ROUTES[route]
        url = canonical_url(route)
        if "<title" not in text:
            fail(f"{label}: missing <title>", errors)
        if 'name="description"' not in text:
            fail(f"{label}: missing meta description", errors)
        if f'rel="canonical" href="{url}"' not in text:
            fail(f"{label}: canonical link does not match {url!r}", errors)
        if f'property="og:url" content="{url}"' not in text:
            fail(f"{label}: og:url does not match {url!r}", errors)
        if 'property="og:title"' not in text or 'property="og:description"' not in text:
            fail(f"{label}: missing Open Graph title/description", errors)

    # Internal links: every root-relative href must resolve to a real canonical route, and any
    # #fragment it carries must resolve to a real id — on the target page for a "/route/#frag"
    # link, or on the current page for a bare "#frag" link.
    for route, route_parser in route_parsers.items():
        label = ROUTES[route]
        for href in route_parser.links:
            if href.startswith(("mailto:", "tel:", "http://", "https://")):
                continue
            if href.startswith("#"):
                if len(href) > 1 and href[1:] not in route_parser.ids:
                    fail(f"{label}: broken internal fragment link: {href}", errors)
                continue
            if href.startswith("/"):
                path_part, _, frag = href.partition("#")
                target_route = path_part.strip("/")
                if target_route not in ROUTES:
                    fail(f"{label}: broken internal route link: {href!r}", errors)
                    continue
                if frag and target_route in route_parsers and frag not in route_parsers[target_route].ids:
                    fail(f"{label}: {href!r} fragment #{frag} not found on {ROUTES[target_route]}", errors)
                continue
            fail(f"{label}: unrecognized internal link shape: {href!r}", errors)

    # EN/TR parity: every data-i18n* key referenced anywhere on the public site must have a
    # value in BOTH dictionary languages, so a route can never ship half-translated.
    all_i18n_keys: set[str] = set()
    for route_parser in route_parsers.values():
        all_i18n_keys |= route_parser.i18n_keys
    for key in sorted(all_i18n_keys):
        for lang in ("en", "tr"):
            if dictionary_value(lang, key) is None:
                fail(f"i18n key {key!r} is missing from the {lang!r} dictionary", errors)

    # Reused WEB-002 proof imagery on any deeper route must still be recorded provenance —
    # extends the index.html-only provenance check above across every public page.
    all_proof_srcs: set[str] = set()
    for route_parser in route_parsers.values():
        all_proof_srcs |= {src.lstrip("/") for src in route_parser.img_srcs if src.lstrip("/").startswith("assets/proof/")}
    unrecorded_site_wide = all_proof_srcs - proof_paths
    if unrecorded_site_wide:
        fail(f"proof imagery referenced outside web_002.proof_assets: {sorted(unrecorded_site_wide)}", errors)

    # Claim discipline and the card/icon-grid guard apply to every public route, not just the
    # homepage (which was already scanned above, with its beam-note exclusion).
    for route, text in route_html.items():
        if route == "":
            continue
        label = ROUTES[route]
        # PROHIBITED_COPY must never appear at all; PROHIBITED_SCORE_COPY is checked the same way
        # index.html is above — allowed inside a mandatory .beam-note warning, nowhere else.
        lowered_route_text = " ".join(route_parsers[route].text).lower()
        for phrase in PROHIBITED_COPY:
            if phrase in lowered_route_text:
                fail(f"{label}: prohibited section/copy detected: {phrase!r}", errors)
        lowered_route_claims = " ".join(route_parsers[route].claim_text).lower()
        for phrase in PROHIBITED_SCORE_COPY:
            if phrase in lowered_route_claims:
                fail(f"{label}: prohibited phrase detected: {phrase!r}", errors)
        suspicious_route = re.findall(r'class="[^"]*\b(?:card-grid|feature-grid|icon-grid)\b[^"]*"', text, flags=re.I)
        if suspicious_route:
            fail(f"{label}: generic card/icon grid class detected; conflicts with locked design", errors)

    # sitemap.xml must list every canonical public route.
    sitemap_path = ROOT / "sitemap.xml"
    if sitemap_path.exists():
        sitemap_text = sitemap_path.read_text(encoding="utf-8")
        for route in ROUTES:
            url = canonical_url(route)
            if f"<loc>{url}</loc>" not in sitemap_text:
                fail(f"sitemap.xml is missing {url!r}", errors)

    print("OrbGSS site validation")
    print(f"  scenes: {len(scenes)}")
    print(f"  html images: {len(parser.img_srcs)}")
    print(f"  routes: {len(route_parsers)}")
    print(f"  i18n keys referenced site-wide: {len(all_i18n_keys)}")
    print(f"  warnings: {len(warnings)}")
    for item in warnings:
        print(f"WARN: {item}")
    if errors:
        for item in errors:
            print(f"ERROR: {item}")
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
