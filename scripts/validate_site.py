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

# WEB-005 four-act structure: the act anchors, the evidence trio, the data-gap note, the pilot
# ledger and the trust/contact zone. The WEB-001/002 six-scene gallery anchors (observe/platform,
# geothermal as separate full-width scenes) are deliberately gone.
REQUIRED_SECTION_IDS = {
    "hero", "context", "evidence", "terrain", "thermal", "alteration", "structure", "priority",
    "pilot", "solutions", "mineral", "environment", "company", "contact",
}
# WEB-005: the homepage's primary visual hierarchy is exactly these four acts, in this order.
REQUIRED_ACTS = ["1", "2", "3", "4"]
REQUIRED_ACT_SECTION_IDS = ["hero", "context", "evidence", "priority"]
PROHIBITED_COPY = ["how it works"]
# Temporary gallery panels must never be labelled as scientific outputs (WEB-001 acceptance 9).
REQUIRED_TEMP_PANEL_STATUS = "temporary-gallery"
# WEB-002: a story slot is real product proof, an explicit data gap, or still temporary gallery.
# WEB-005 adds the cinematic hero and the class-A Earth-observation context act.
ALLOWED_PANEL_STATUS = {
    REQUIRED_TEMP_PANEL_STATUS, "product-proof", "data-gap", "cinematic-hero", "eo-context",
}
# WEB-005: the exact visual slots the four-act homepage publishes, in order, after the hero.
EXPECTED_HOMEPAGE_SLOTS = ["context", "terrain", "thermal", "alteration", "priority"]
# WEB-005 hero media envelope, inherited from WEB-004 and not relaxed here.
HERO_MEDIA_CEILINGS = {
    "hero-webm": 3.0 * 1024 * 1024,
    "hero-mp4": 4.5 * 1024 * 1024,
    "hero-poster": 180 * 1024,
}
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
        # Responsive candidates from img[srcset] and link[rel=preload][imagesrcset] (WEB-004).
        self.img_srcsets: list[str] = []
        self.links: list[str] = []
        self.text: list[str] = []
        self.claim_text: list[str] = []
        self.visual_slots: list[tuple[str, str]] = []
        # WEB-005: data-act on each major act section, in document order, and the evidence cards
        # inside the one permitted card composition.
        self.acts: list[str] = []
        self.evidence_cards = 0
        # <video> elements and the hero media URLs they declare, so the media envelope and the
        # "never download both encodes" rule can be checked from the markup.
        self.video_count = 0
        self.eager_video_sources: list[str] = []
        self.hero_media: dict[str, str] = {}
        # Static text carried by each data-i18n element, so warning coverage can be proved for a
        # reader with JavaScript disabled, not just for the dictionary.
        self.i18n_text: dict[str, str] = {}
        # Every data-i18n* key this file references, regardless of which attribute carries it
        # (text content, alt, aria-label, meta content, href) — used for site-wide EN/TR parity.
        self.i18n_keys: set[str] = set()
        # aria-label values with no data-i18n-aria-label on the same element (MER-91): a
        # human-readable aria-label that only ever exists in English is exactly the kind of gap
        # that reads fine in a spot-check and then fails EN/TR parity for a screen-reader user.
        self.untranslated_aria_labels: list[str] = []
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
        aria_label = data.get("aria-label")
        if aria_label and aria_label.strip() and not data.get("data-i18n-aria-label"):
            self.untranslated_aria_labels.append(str(aria_label))
        if data.get("id"):
            self.ids.add(str(data["id"]))
        if data.get("data-visual-slot"):
            self.visual_slots.append((str(data["data-visual-slot"]), str(data.get("data-visual-status") or "")))
        if data.get("data-act"):
            self.acts.append(str(data["data-act"]))
        if tag == "li" and "evidence-card" in str(data.get("class") or "").split():
            self.evidence_cards += 1
        # WEB-005 hero media. The encodes are attached by script.js at runtime, so the markup
        # carries them as data- attributes; a <source> child or a src here would mean the browser
        # starts fetching video during parse, which is exactly what the media contract forbids.
        if tag == "video":
            self.video_count += 1
            for attr in ("data-hero-webm", "data-hero-mp4"):
                if data.get(attr):
                    self.hero_media[attr] = str(data[attr])
            if data.get("src"):
                self.eager_video_sources.append(str(data["src"]))
        if tag == "source" and data.get("src") and "video" in str(data.get("type") or ""):
            self.eager_video_sources.append(str(data["src"]))
        if tag == "img" and data.get("src"):
            self.img_srcs.append(str(data["src"]))
        # WEB-004: a deferred layer (data-src, promoted by script.js when the section is reached)
        # is still imagery this page publishes, so it stays inside the provenance checks. Without
        # this, moving a proof raster to data-src would silently exempt it from them.
        if tag == "img" and data.get("data-src"):
            self.img_srcs.append(str(data["data-src"]))
        if data.get("data-srcset"):
            for candidate in str(data["data-srcset"]).split(","):
                url = candidate.strip().split()[0] if candidate.strip() else ""
                if url:
                    self.img_srcsets.append(url)
        # WEB-004: responsive candidates are real shipped imagery too. Collecting them keeps a
        # derivative from entering the page without a provenance/checksum record just because it
        # was referenced from srcset rather than src.
        if data.get("srcset"):
            for candidate in str(data["srcset"]).split(","):
                url = candidate.strip().split()[0] if candidate.strip() else ""
                if url:
                    self.img_srcsets.append(url)
        if tag == "link" and str(data.get("rel") or "").lower() == "preload" and data.get("imagesrcset"):
            for candidate in str(data["imagesrcset"]).split(","):
                url = candidate.strip().split()[0] if candidate.strip() else ""
                if url:
                    self.img_srcsets.append(url)
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

    # ------------------------------------------------------------------
    # WEB-004 scene derivatives: the responsive hero candidates are resize-and-encode copies of a
    # recorded scene, so they carry the same discipline as the WEB-002 proof derivatives — recorded
    # path, byte size and SHA-256, recomputed here on every run. A derivative that is edited,
    # re-encoded or swapped without updating the manifest fails the build rather than shipping as
    # unprovenanced imagery.
    # ------------------------------------------------------------------
    scene_derivative_paths: set[str] = set()
    for scene in scenes:
        for deriv in scene.get("derivatives", []):
            rel = str(deriv.get("path", ""))
            sid = scene.get("id", "<unknown>")
            if not rel:
                fail(f"scene {sid!r} has a derivative without a path", errors)
                continue
            scene_derivative_paths.add(rel)
            for key in ("role", "width_px", "format", "operation", "bytes", "sha256"):
                if deriv.get(key) in (None, ""):
                    fail(f"scene derivative {rel} missing field: {key}", errors)
            path = ROOT / rel
            if not path.exists():
                fail(f"scene derivative missing from repository: {rel}", errors)
                continue
            recorded = str(deriv.get("sha256", ""))
            actual = sha256_of(path)
            if recorded != actual:
                fail(f"scene derivative checksum mismatch for {rel}: "
                     f"manifest {recorded[:12]}… != file {actual[:12]}…", errors)
            if deriv.get("bytes") not in (None, path.stat().st_size):
                fail(f"scene derivative byte size mismatch for {rel}", errors)

    # WEB-005 Act 2 publishes the accepted GEO-WEB-002 natural-colour context master, which is
    # recorded under geo_web_002 rather than in the four locked WEB-001 scenes. It carries the
    # same record shape and is checksummed by the package block further down, so it is valid
    # provenance for an <img> here too.
    package_context_paths: set[str] = set()
    for group in ("context_scenes", "assets"):
        for entry in manifest.get("geo_web_002", {}).get(group, []):
            if entry.get("local_file"):
                package_context_paths.add(str(entry["local_file"]))
            for deriv in entry.get("derivatives", []):
                if deriv.get("path"):
                    package_context_paths.add(str(deriv["path"]))

    manifest_html_paths = {
        src for src in parser.img_srcs + parser.img_srcsets if src.startswith("assets/imagery/")
    }
    extra = manifest_html_paths - scene_paths - scene_derivative_paths - package_context_paths
    if extra:
        fail(f"HTML imagery paths missing from provenance manifest: {sorted(extra)}", errors)

    # Internal fragment links should resolve to an ID (except #top, which is present today).
    for href in parser.links:
        if href.startswith("#") and len(href) > 1 and href[1:] not in parser.ids:
            fail(f"broken internal fragment link: {href}", errors)

    # Every panel is a declared visual slot; temporary panels carry the temporary status so
    # WEB-002 can find them and so nobody silently promotes a gallery image to an evidence output.
    story_slots = [slot for slot in parser.visual_slots if slot[0] != "hero"]
    if [slot for slot, _ in story_slots] != EXPECTED_HOMEPAGE_SLOTS:
        fail(f"homepage visual slots out of order or missing: "
             f"{[slot for slot, _ in story_slots]} != {EXPECTED_HOMEPAGE_SLOTS}", errors)
    for slot, status in parser.visual_slots:
        if status not in ALLOWED_PANEL_STATUS:
            fail(f"visual slot {slot!r} has unknown data-visual-status {status!r}", errors)

    # ------------------------------------------------------------------
    # WEB-005: the homepage's primary visual hierarchy is exactly four major acts, in the locked
    # order Hero -> real AOI context -> compact evidence trio -> priority/result climax. This is
    # the check that keeps a fifth full-width scene, or a reordering, from creeping back in: the
    # superseded six-scene gallery is precisely what happens when nothing enforces the count.
    # ------------------------------------------------------------------
    if parser.acts != REQUIRED_ACTS:
        fail(f"homepage must publish exactly four acts in order; found {parser.acts}", errors)
    for section_id in REQUIRED_ACT_SECTION_IDS:
        if section_id not in parser.ids:
            fail(f"missing act anchor: #{section_id}", errors)
    # Act 3 is the ONE deliberate card composition on the site, and it is exactly three evidence
    # cards. Four would be a card wall; two would not be the accepted composition.
    if parser.evidence_cards != 3:
        fail(f"the evidence act must hold exactly three cards, found {parser.evidence_cards}",
             errors)
    # The superseded rhythm, named so it cannot come back by accident.
    for retired in ("story-section", "story-beam", "layer-switch"):
        if f'class="{retired}' in html or f' {retired}"' in html:
            fail(f"superseded WEB-001/002 homepage component {retired!r} is back on the homepage",
                 errors)

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

    # The warning-coverage check needs every route's parse, so it runs further down, once
    # route_parsers exists — a mandatory warning has to be visible wherever its asset is shown,
    # which after WEB-005 is no longer always the homepage.

    # Data-gap slots are declared, so an absent layer can never be quietly filled later.
    gap_slots = {str(gap.get("homepage_slot")) for gap in web002.get("data_gaps", [])}
    for slot, status in story_slots:
        if status == "data-gap" and slot not in gap_slots:
            fail(f"slot {slot!r} is marked data-gap but has no web_002.data_gaps record", errors)

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

    # Accessibility-text parity (MER-91): a human-readable aria-label on a canonical public route
    # must be bound to data-i18n-aria-label, exactly like every other visible/AT-exposed string on
    # the site — otherwise it silently stays English-only no matter what language is selected.
    for route, route_parser in route_parsers.items():
        label = ROUTES[route]
        for aria_label in route_parser.untranslated_aria_labels:
            fail(f"{label}: aria-label {aria_label!r} has no data-i18n-aria-label "
                 f"(untranslated accessibility text)", errors)

    # Social-preview truthfulness (MER-91): /pilot/ must not borrow the homepage hero's Crater Lake
    # image for its own Open Graph preview — its og:image must be a real Kızıldere asset (either an
    # accepted WEB-002 proof derivative or the homepage's own on-topic imagery), never the hero.
    pilot_html = route_html.get("pilot", "")
    if 'property="og:image" content="https://orbgss.com/assets/imagery/crater-lake-2023.jpg"' in pilot_html:
        fail("pilot/index.html: og:image reuses the Crater Lake hero image, not a Kızıldere pilot visual", errors)
    if pilot_html and not re.search(r'property="og:image" content="https://orbgss\.com/assets/(proof|imagery)/', pilot_html):
        fail("pilot/index.html: og:image is not a self-hosted approved asset", errors)

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

    # ------------------------------------------------------------------
    # Scientific imagery provenance, site-wide. Every scientific raster on any public route must
    # be a recorded derivative — of the accepted WEB-002 proof package, or of the accepted
    # GEO-WEB-002 final visual master package that WEB-005 binds. Both carry the same discipline
    # (export id, master checksum, per-derivative checksum), so both are valid provenance; what
    # is not valid is a scientific-looking file that belongs to neither.
    # ------------------------------------------------------------------
    package_derivative_paths: set[str] = set()
    for asset in manifest.get("geo_web_002", {}).get("assets", []):
        for deriv in asset.get("derivatives", []):
            if deriv.get("path"):
                package_derivative_paths.add(str(deriv["path"]))
    recorded_science_paths = proof_paths | package_derivative_paths

    def science_srcs(route_parser: SiteParser) -> set[str]:
        srcs = route_parser.img_srcs + route_parser.img_srcsets
        return {s.lstrip("/") for s in srcs if s.lstrip("/").startswith("assets/proof/")}

    all_proof_srcs: set[str] = set()
    for route_parser in route_parsers.values():
        all_proof_srcs |= science_srcs(route_parser)
    unrecorded_site_wide = all_proof_srcs - recorded_science_paths
    if unrecorded_site_wide:
        fail(f"scientific imagery referenced with no provenance record in web_002.proof_assets "
             f"or geo_web_002.assets: {sorted(unrecorded_site_wide)}", errors)

    # ------------------------------------------------------------------
    # Mandatory scientific warnings must be visible on EVERY route that shows the asset, in both
    # languages, and in the static HTML as well as the dictionary — so they survive with
    # JavaScript disabled and cannot be quietly dropped by a later copy edit. Before WEB-005 this
    # was an index.html check; the homepage is no longer the only place these assets appear, and
    # an asset shown on /pilot/ with its warning left behind on the homepage would be worse than
    # the original gap.
    # ------------------------------------------------------------------
    def check_warning_coverage(label: str, aid: str, coverage: dict, where: list[str]) -> None:
        key = str(coverage.get("i18n_key", ""))
        if not key:
            fail(f"{label} {aid!r} visible_warning has no i18n_key", errors)
            return
        for lang in ("en", "tr"):
            value = dictionary_value(lang, key)
            if value is None:
                fail(f"warning key {key!r} is missing from the {lang!r} dictionary", errors)
                continue
            for term in coverage.get(f"required_terms_{lang}", []):
                if term not in value:
                    fail(f"{label} {aid!r}: {lang} warning lost required wording {term!r}", errors)
        for route in where:
            static_text = route_parsers[route].i18n_text.get(key)
            if static_text is None:
                fail(f"{label} {aid!r} is shown on {ROUTES[route]} but its warning key {key!r} "
                     f"is not rendered there", errors)
                continue
            for term in coverage.get("required_terms_en", []):
                if term not in static_text:
                    fail(f"{label} {aid!r}: static HTML warning under {key!r} lost required "
                         f"wording {term!r} on {ROUTES[route]} (no-JS readers would not see it)",
                         errors)

    for asset in proof_assets:
        aid = asset.get("id", "<unknown>")
        coverage = asset.get("visible_warning")
        if not coverage:
            fail(f"proof asset {aid!r} has no visible_warning record; every mandatory warning "
                 f"must be bound to visible page copy", errors)
            continue
        own = {str(d.get("path", "")) for d in asset.get("derivatives", [])}
        shown_on = [r for r, rp in route_parsers.items() if science_srcs(rp) & own]
        check_warning_coverage("proof asset", aid, coverage, shown_on)

    # ------------------------------------------------------------------
    # WEB-005: what the homepage actually binds from the accepted GEO-WEB-002 package. Placement
    # is where a publication record stops being paperwork: an asset may only appear on a route if
    # it declares that placement, carries its mandatory warning as visible copy there, and is
    # given a CSS width that keeps it at or under the device-pixel ceiling its own record calls
    # honest — including on a 2x display, which is where "looks crisp on my laptop" quietly
    # becomes browser upscaling.
    # ------------------------------------------------------------------
    def all_srcs(route_parser: SiteParser) -> set[str]:
        return {s.lstrip("/") for s in route_parser.img_srcs + route_parser.img_srcsets}

    for asset in manifest.get("geo_web_002", {}).get("assets", []):
        aid = asset.get("id", "<unknown>")
        own = {str(d.get("path", "")) for d in asset.get("derivatives", [])}
        if asset.get("master", {}).get("file"):
            own.add(str(asset["master"]["file"]))
        # The Act-2 context master lives under assets/imagery/, not assets/proof/, so placement
        # is resolved against every image a route publishes rather than the proof prefix alone.
        shown_on = [r for r, rp in route_parsers.items() if all_srcs(rp) & own]
        placement = asset.get("web_005_placement")
        if not shown_on:
            if placement and placement.get("status") == "placed":
                fail(f"geo_web_002 asset {aid!r} claims a WEB-005 placement but appears on no "
                     f"route", errors)
            continue
        if not placement:
            fail(f"geo_web_002 asset {aid!r} is published on {[ROUTES[r] for r in shown_on]} "
                 f"with no web_005_placement record", errors)
            continue
        for key in ("status", "act", "homepage_slot", "visible_warning", "rendered"):
            if not placement.get(key):
                fail(f"geo_web_002 asset {aid!r} web_005_placement missing field: {key}", errors)
        if placement.get("visible_warning"):
            check_warning_coverage("geo_web_002 asset", aid, placement["visible_warning"],
                                   shown_on)
        # The safe-density decision, checked rather than asserted.
        ceiling = asset.get("max_safe_rendered_px", {}).get("device_px")
        rendered = placement.get("rendered", {})
        for field in ("max_css_width", "device_pixel_ratio_considered", "selected_derivative"):
            if rendered.get(field) in (None, ""):
                fail(f"geo_web_002 asset {aid!r} web_005_placement.rendered missing {field}",
                     errors)
        css_width = rendered.get("max_css_width")
        dpr = rendered.get("device_pixel_ratio_considered")
        if isinstance(ceiling, int) and isinstance(css_width, int) and isinstance(dpr, (int, float)):
            if css_width * dpr > ceiling:
                fail(f"geo_web_002 asset {aid!r} is laid out at {css_width} CSS px, which is "
                     f"{int(css_width * dpr)} device px at {dpr}x and exceeds its declared "
                     f"{ceiling} px ceiling", errors)
        selected = str(rendered.get("selected_derivative", ""))
        if selected and selected not in own:
            fail(f"geo_web_002 asset {aid!r} names a selected derivative that is not its own: "
                 f"{selected}", errors)
        # A detached homepage colour bar is exactly what the presentation authority prohibits.
        if asset.get("id") == "priority" and "" in shown_on:
            home = route_html[""]
            if 'class="scale-strip"' in home:
                fail("a detached scientific scale strip is back on the homepage; a necessary "
                     "legend belongs inside its own visual frame", errors)

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

    # ------------------------------------------------------------------
    # WEB-005 hero media contract. The ceilings are WEB-004's and are not relaxed here. Two things
    # beyond size matter and are checkable from the markup and the manifest:
    #   - no browser may be made to download both encodes, so neither a <source> child nor a src
    #     attribute may appear on the hero video — the encodes are attached at runtime, one only;
    #   - every shipped media file is recorded with codec, dimensions, rate, duration, bytes and
    #     SHA-256, recomputed here, exactly like every raster on the site.
    # ------------------------------------------------------------------
    hero_media = manifest.get("web_005", {}).get("hero_media", [])
    if parser.eager_video_sources:
        fail(f"hero video declares eager sources {parser.eager_video_sources}; a <source> child "
             f"or src attribute makes the browser fetch an encode during parse, and with both "
             f"encodes declared it can fetch both", errors)
    if hero_media:
        media_by_role = {str(m.get("role", "")): m for m in hero_media}
        for role, ceiling in HERO_MEDIA_CEILINGS.items():
            if role not in media_by_role:
                fail(f"web_005.hero_media has no {role!r} record", errors)
        for media in hero_media:
            role = str(media.get("role", "<unknown>"))
            rel = str(media.get("path", ""))
            required = ["role", "path", "container", "codec", "width", "height",
                        "frame_rate", "duration_seconds", "bytes", "sha256"]
            # A poster is a still: frame rate and duration are meaningless for it. Every poster
            # candidate is a poster, including the narrow one a phone is served.
            is_poster = role.startswith("hero-poster")
            if is_poster:
                required = [k for k in required if k not in ("frame_rate", "duration_seconds")]
            for key in required:
                if media.get(key) in (None, ""):
                    fail(f"hero media {role!r} missing field: {key}", errors)
            path = ROOT / rel
            if not rel or not path.exists():
                fail(f"hero media missing from repository: {rel}", errors)
                continue
            actual = sha256_of(path)
            if str(media.get("sha256", "")) != actual:
                fail(f"hero media checksum mismatch for {rel}: "
                     f"manifest {str(media.get('sha256',''))[:12]}… != file {actual[:12]}…",
                     errors)
            size = path.stat().st_size
            if media.get("bytes") not in (None, size):
                fail(f"hero media byte size mismatch for {rel}", errors)
            # Every poster candidate is held to the poster ceiling, not just the widest one:
            # a phone that is served an oversized poster is exactly the case the budget exists for.
            ceiling = HERO_MEDIA_CEILINGS.get(
                role, HERO_MEDIA_CEILINGS["hero-poster"] if is_poster else None)
            if ceiling is not None and size > ceiling:
                fail(f"hero media {rel} is {size / 1048576:.2f} MiB, over the "
                     f"{ceiling / 1048576:.2f} MiB ceiling for {role!r}", errors)
        # Everything the markup points at must be one of those recorded files.
        recorded_media = {str(m.get("path", "")) for m in hero_media}
        for attr, url in parser.hero_media.items():
            if url.lstrip("/") not in recorded_media:
                fail(f"hero {attr} points at {url!r}, which has no web_005.hero_media record",
                     errors)
        # The poster is real shipped imagery and the LCP element; it is checked like any other.
        poster_paths = {src.lstrip("/") for src in parser.img_srcs + parser.img_srcsets
                        if src.lstrip("/").startswith("assets/hero/")}
        unrecorded_poster = poster_paths - recorded_media
        if unrecorded_poster:
            fail(f"hero imagery missing from web_005.hero_media: {sorted(unrecorded_poster)}",
                 errors)
    elif parser.hero_media:
        fail("index.html declares hero media but the manifest has no web_005.hero_media record",
             errors)

    # sitemap.xml must list every canonical public route.
    sitemap_path = ROOT / "sitemap.xml"
    if sitemap_path.exists():
        sitemap_text = sitemap_path.read_text(encoding="utf-8")
        for route in ROUTES:
            url = canonical_url(route)
            if f"<loc>{url}</loc>" not in sitemap_text:
                fail(f"sitemap.xml is missing {url!r}", errors)

    # ------------------------------------------------------------------
    # GEO-WEB-002 / MER-102: the final homepage visual master package. These assets are published
    # for WEB-005 and are deliberately not placed on any route yet, so the checks here are about
    # the publication record itself — every shipped file recorded, checksummed and byte-sized;
    # every asset declaring its role, rights, attribution, warning and maximum safe rendered size;
    # and no derivative wider than the size its own record says is honest.
    # ------------------------------------------------------------------
    package = manifest.get("geo_web_002", {})
    package_paths: set[str] = set()
    if package:
        for key in ("task", "state", "consumer", "package_document", "presentation_authority",
                    "science_authority", "scoring_identity", "rule", "resolution_rule",
                    "context_scenes", "assets"):
            if not package.get(key):
                fail(f"geo_web_002 package missing field: {key}", errors)
        doc = str(package.get("package_document", ""))
        if doc and not (ROOT / doc).exists():
            fail(f"geo_web_002 package_document does not exist: {doc}", errors)

        for asset in package.get("assets", []):
            aid = asset.get("id", "<unknown>")
            for key in ("id", "homepage_act", "public_role", "scientific_state", "asset_class",
                        "public_label", "derivation", "max_safe_rendered_px", "rights_basis",
                        "attribution_requirement", "mandatory_warning", "derivatives"):
                if not asset.get(key):
                    fail(f"geo_web_002 asset {aid!r} missing field: {key}", errors)
            if asset.get("public_role") not in {"context", "evidence", "derived score"}:
                fail(f"geo_web_002 asset {aid!r} must state whether it is context, evidence or "
                     f"a derived score, not {asset.get('public_role')!r}", errors)
            if not asset.get("derivation", {}).get("no_upscale"):
                fail(f"geo_web_002 asset {aid!r} does not declare derivation.no_upscale", errors)

            # Class B assets are cartographic exports: master pointer and master checksum are the
            # provenance, exactly as for the accepted WEB-002 proof assets.
            if str(asset.get("asset_class", "")).startswith("B"):
                export = asset.get("export", {})
                for key in ("export_id", "export_manifest", "master_file", "master_sha256",
                            "master_dimensions", "renderer_revision", "plan_sha256"):
                    if not export.get(key):
                        fail(f"geo_web_002 asset {aid!r} missing export.{key}", errors)
                master = str(export.get("master_sha256", ""))
                if not re.fullmatch(r"[0-9a-f]{64}", master):
                    fail(f"geo_web_002 asset {aid!r} master_sha256 is not a sha256 digest", errors)
                for key in ("layer_ids", "source_project", "grid", "style_id"):
                    if not asset.get(key):
                        fail(f"geo_web_002 asset {aid!r} missing field: {key}", errors)
            else:
                master = asset.get("master", {})
                for key in ("file", "format", "dimensions", "bytes", "sha256"):
                    if not master.get(key):
                        fail(f"geo_web_002 asset {aid!r} missing master.{key}", errors)
                master_file = str(master.get("file", ""))
                master_path = ROOT / master_file
                if not master_file or not master_path.exists():
                    fail(f"geo_web_002 asset {aid!r} master file is missing: {master_file}", errors)
                else:
                    # A class-A master ships in this repository, so its checksum is verifiable
                    # here — unlike a class-B cartographic master, which stays in the Science
                    # repository and is pinned by its own export manifest.
                    actual_master = sha256_of(master_path)
                    if str(master.get("sha256", "")) != actual_master:
                        fail(f"geo_web_002 asset {aid!r} master checksum mismatch for "
                             f"{master_file}", errors)
                    if master.get("bytes") not in (None, master_path.stat().st_size):
                        fail(f"geo_web_002 asset {aid!r} master byte size mismatch for "
                             f"{master_file}", errors)

            safe = asset.get("max_safe_rendered_px", {})
            for key in ("device_px", "basis"):
                if not safe.get(key):
                    fail(f"geo_web_002 asset {aid!r} missing max_safe_rendered_px.{key}", errors)
            ceiling = safe.get("device_px")

            for deriv in asset.get("derivatives", []):
                rel = str(deriv.get("path", ""))
                if not rel:
                    fail(f"geo_web_002 asset {aid!r} has a derivative without a path", errors)
                    continue
                package_paths.add(rel)
                for key in ("role", "width", "height", "format", "operation", "bytes", "sha256"):
                    if deriv.get(key) in (None, ""):
                        fail(f"geo_web_002 derivative {rel} missing field: {key}", errors)
                path = ROOT / rel
                if not path.exists():
                    fail(f"geo_web_002 derivative missing from repository: {rel}", errors)
                    continue
                recorded = str(deriv.get("sha256", ""))
                actual = sha256_of(path)
                if recorded != actual:
                    fail(f"geo_web_002 derivative checksum mismatch for {rel}: "
                         f"manifest {recorded[:12]}… != file {actual[:12]}…", errors)
                if deriv.get("bytes") not in (None, path.stat().st_size):
                    fail(f"geo_web_002 derivative byte size mismatch for {rel}", errors)
                # The whole point of the package: never ship a derivative wider than the size the
                # asset itself declares honest, or the softness WEB-005 must avoid is baked in.
                if isinstance(ceiling, int) and deriv.get("role", "").startswith(("panel", "act2")):
                    if int(deriv.get("width", 0)) > ceiling:
                        fail(f"geo_web_002 derivative {rel} is {deriv.get('width')} px wide but "
                             f"{aid!r} declares a {ceiling} px ceiling", errors)

        # The Act-2 context scene is rebuilt by scripts/build_imagery.py from its own production
        # block, so its derivative list must stay identical to the one published in the asset
        # record; two divergent copies of the same provenance would be worse than one.
        for scene in package.get("context_scenes", []):
            sid = scene.get("id", "<unknown>")
            for key in ("id", "role", "location", "coordinates", "acquired", "sensor",
                        "source_data", "local_file", "production"):
                if not scene.get(key):
                    fail(f"geo_web_002 context scene {sid!r} missing field: {key}", errors)
            local = str(scene.get("local_file", ""))
            if local and not (ROOT / local).exists():
                fail(f"geo_web_002 context master is missing: {local}", errors)
            linked = [a for a in package.get("assets", []) if a.get("context_scene_id") == sid]
            for asset in linked:
                if asset.get("derivatives") != scene.get("derivatives"):
                    fail(f"geo_web_002 context scene {sid!r} and asset {asset.get('id')!r} "
                         f"publish different derivative records", errors)

    print("OrbGSS site validation")
    print(f"  scenes: {len(scenes)}")
    print(f"  html images: {len(parser.img_srcs)}")
    print(f"  routes: {len(route_parsers)}")
    print(f"  i18n keys referenced site-wide: {len(all_i18n_keys)}")
    print(f"  geo-web-002 package assets: {len(package.get('assets', []))} "
          f"({len(package_paths)} files)")
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
