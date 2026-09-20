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
# WEB-005B R13: the homepage domain taxonomy is Geothermal / Mining / Marine. The #mineral and
# #environment anchors belong to /solutions/, which keeps its own application-ledger vocabulary and
# is still the target of every nav link; an existing route anchor is not authority to rename a
# published homepage domain.
REQUIRED_SECTION_IDS = {
    "hero", "context", "evidence", "terrain", "thermal", "alteration", "structure", "priority",
    "pilot", "solutions", "geothermal", "mining", "marine", "company", "contact",
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
# WEB-005A final production: the analytical drape states are lossless by rule (a lossy encode
# changes the colours they are read by), so they are bounded per file instead of being compressed.
HERO_DRAPE_STATE_CEILING = 1.25 * 1024 * 1024
HERO_DRAPE_LAYERS = ["terrain", "thm01", "alt01", "priority"]
# WEB-005A relief rise (docs/web-005-polish-authority@0e87675): 6-12 lossless states, 0.45-0.70 s.
# WEB-005B / MER-109. The Product palette (tasks/WEB-005B_HOMEPAGE_VISUAL_FIDELITY_PALETTE.md
# section 5) is pinned here so a quiet token edit fails the build (B-VIS-05).
WEB005B_TOKENS = {
    "--orb-bg": "#030B12", "--orb-surface": "#08131D", "--orb-panel": "#0D1B27",
    "--orb-divider": "#183245", "--orb-text-primary": "#EAF2F8", "--orb-text-secondary": "#9EB1C1",
    "--orb-meta": "#6F8597", "--orb-cyan": "#73E7FF", "--orb-cyan-glow": "#8AF1FF",
    "--orb-beam-core": "#7FEFFF", "--orb-beam-glow": "#3CCBFF", "--orb-target-frame": "#98F5FF",
}
# MER-108 governed-source pins and website-derivative bounds (B-VIS-04). The source SHA-256s are
# the MER-113 identities in the terminal authority; normalization is d3a163bd's canonical kind per
# layer; analytical opacity is 11c32e8d section 6. None of these may drift without Science.
WEB005B_SOURCES = {
    "terrain": ("590f74322c6ad942e0d36b79446934da7a0938c7d87c06ab8c9bd27da73fb694", "linear_min_max", (0.85, 1.0)),
    "thm01": ("6a2850f9915c08ed56ae2731d54881d55ca145db6cda11a21ed7e6191e629583", "diverging_symmetric_from_data", (0.85, 1.0)),
    "alt01": ("ac7f2dade5274d9fd81b7fdbc8bcf7ae828bb958de5c74b9847e6332675fbf14", "linear_min_max", (0.85, 1.0)),
    "priority": ("15065152f6f21eaf66236d51d6814acfb32326c5698bc2433dcb69653d8a9d1e", "fixed_range_0_100", (0.90, 1.0)),
}
WEB005B_TOPOLOGY = {
    "terrain": "terrain_natural_earth_relief_v1", "thm01": "thm_cool_neutral_warm_red_v1",
    "alt01": "alt_violet_blue_cyan_green_yellow_v1", "priority": "priority_deep_purple_red_orange_yellow_v1",
}
WEB005B_NATIVE_PX = 1200
# Transforms the terminal amendment allows for the hero surface only; a homepage derivative that
# records using one of them is outside 11c32e8d.
WEB005B_HERO_ONLY = ("display window", "gamma / tone transfer", "gaussian smoothing", "unsharp", "upsampling")

HERO_RISE_STATE_CEILING = 512 * 1024
HERO_RISE_TOTAL_CEILING = int(2.5 * 1024 * 1024)
HERO_STATIC_POSTER_MEDIA = "(prefers-reduced-motion: reduce), (max-width: 780px)"
HERO_MOTION_POSTER_MEDIA = "(prefers-reduced-motion: no-preference) and (min-width: 781px)"
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
        # WEB-005: data-act on each major act section, in document order.
        self.acts: list[str] = []
        # WEB-005B R11: the accepted final design replaced the rejected three-equal-card gallery
        # with ONE shared geographic frame holding three cross-faded plates and three selector
        # tabs. Counting all three keeps the composition checkable in both directions: a fourth
        # layer, a missing tab, or a second frame (a gallery by another name) all fail.
        self.evidence_plates = 0
        self.evidence_tabs = 0
        self.evidence_frames = 0
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
        classes = str(data.get("class") or "").split()
        if tag == "figure" and "evidence-plate" in classes:
            self.evidence_plates += 1
        if tag == "label" and "evidence-tab" in classes:
            self.evidence_tabs += 1
        if "evidence-frame" in classes:
            self.evidence_frames += 1
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

    web005b = manifest.get("web_005b", {})
    for deriv in web005b.get("context", {}).get("derivatives", []):
        if deriv.get("path"):
            package_context_paths.add(str(deriv["path"]))
    if web005b.get("context", {}).get("master", {}).get("file"):
        package_context_paths.add(str(web005b["context"]["master"]["file"]))

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
    # WEB-005B R11: Act 3 is ONE shared geographic frame read through exactly three layers. The
    # frame is what makes the layers comparable, so there is exactly one of it; three plates and
    # three tabs is the accepted composition. Three separately framed panels — the rejected
    # three-equal-card gallery — would show up here as three frames.
    if parser.evidence_frames != 1:
        fail(f"the evidence act must hold exactly ONE shared frame, found "
             f"{parser.evidence_frames}; separate frames per layer are the rejected gallery",
             errors)
    if parser.evidence_plates != 3 or parser.evidence_tabs != 3:
        fail(f"the evidence act must hold exactly three layer plates and three selector tabs, "
             f"found {parser.evidence_plates} plates and {parser.evidence_tabs} tabs", errors)
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
    web005b_science_paths: set[str] = set()
    web005b_analytical = manifest.get("web_005b", {}).get("analytical", {})
    for layer in web005b_analytical.get("layers", {}).values():
        for deriv in layer.get("derivatives", []):
            web005b_science_paths.add(str(deriv.get("path", "")))
        if layer.get("legend", {}).get("path"):
            web005b_science_paths.add(str(layer["legend"]["path"]))
    # WEB-005B R3: what the page actually fetches may be a lossy delivery encode of a lossless
    # reference. Both are recorded science.
    for entries in web005b_analytical.get("delivery", {}).get("layers", {}).values():
        for entry in entries:
            web005b_science_paths.add(str(entry.get("path", "")))
    recorded_science_paths = proof_paths | package_derivative_paths | web005b_science_paths

    def science_srcs(route_parser: SiteParser) -> set[str]:
        srcs = route_parser.img_srcs + route_parser.img_srcsets
        return {s.lstrip("/") for s in srcs if s.lstrip("/").startswith("assets/proof/")}

    all_proof_srcs: set[str] = set()
    for route_parser in route_parsers.values():
        all_proof_srcs |= science_srcs(route_parser)
    unrecorded_site_wide = all_proof_srcs - recorded_science_paths
    if unrecorded_site_wide:
        fail(f"scientific imagery referenced with no provenance record in web_002.proof_assets, "
             f"geo_web_002.assets or web_005b.analytical: {sorted(unrecorded_site_wide)}", errors)

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

    # ------------------------------------------------------------------
    # WEB-005B / MER-109: homepage Acts 2-4 (web_005b in the manifest).
    #   B-VIS-02  the Act 2 photograph is a recorded, checksummed USGS Landsat derivative, never
    #             wider than its native frame, and its AOI corner marks are the recorded geometry.
    #   B-VIS-04  every Act 3/4 pixel is a MER-108 website derivative of a pinned governed source:
    #             canonical normalization, the pinned palette topology, a LUT recomputed here from
    #             the recorded stops, bounded analytical opacity, lossless, never above the native
    #             grid, and none of the hero-only transforms.
    #   B-VIS-05  the Product palette tokens are defined once and hold their pinned values.
    #   B-VIS-06  the priority public label is exact; its warning terms are bound per placement.
    #   B-VIS-07  every placement's CSS width x DPR stays within its native pixels.
    #   B-VIS-08  the priority legend lives inside the result figure; no detached strip.
    #   B-VIS-14  web_005b assets are placed on the homepage only.
    # ------------------------------------------------------------------
    def web005b_lut(stops: list[str], size: int = 256) -> bytes:
        """The build script's LUT (numpy linspace + interp + uint8 truncation), in plain floats."""
        pts = [tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)) for h in stops]
        n = len(pts)
        xp = [j * (1.0 / (n - 1)) for j in range(n - 1)] + [1.0]
        out = bytearray()
        for i in range(size):
            x = 1.0 if i == size - 1 else i * (1.0 / (size - 1))
            j = max(k for k in range(n - 1) if xp[k] <= x) if x < 1.0 else n - 2
            for c in range(3):
                if x >= 1.0:
                    v = float(pts[-1][c])
                else:
                    slope = (pts[j + 1][c] - pts[j][c]) / (xp[j + 1] - xp[j])
                    v = slope * (x - xp[j]) + pts[j][c]
                out.append(int(min(max(v, 0.0), 255.0)))
        return bytes(out)

    def web005b_file(label: str, rec: dict) -> str | None:
        rel = str(rec.get("path") or rec.get("file") or "")
        if not rel:
            fail(f"{label}: record without a path", errors)
            return None
        path = ROOT / rel
        if not path.exists():
            fail(f"{label}: {rel} is missing from the repository", errors)
            return None
        if sha256_of(path) != str(rec.get("sha256", "")):
            fail(f"{label}: checksum mismatch for {rel}", errors)
        if rec.get("bytes") != path.stat().st_size:
            fail(f"{label}: byte size mismatch for {rel}", errors)
        return rel

    w5b = manifest.get("web_005b", {})
    css_text = (ROOT / "styles.css").read_text(encoding="utf-8")
    home = route_html[""]
    w5b_own: dict[str, set[str]] = {}
    if not w5b:
        fail("manifest web_005b is missing", errors)
    else:
        ctx = w5b.get("context", {})
        for key in ("source", "frame", "derivation", "master", "derivatives", "max_safe_rendered_px",
                    "rights_basis", "attribution_requirement", "mandatory_warning_i18n_key"):
            if not ctx.get(key):
                fail(f"web_005b.context missing field: {key}", errors)
        if "LC08_L2SP_179034_20250505_02_T1" not in ctx.get("source", {}).get("product_ids", []):
            fail("web_005b.context is not the recorded USGS Landsat product", errors)
        ctx_ceiling = ctx.get("max_safe_rendered_px", {}).get("device_px")
        own = set()
        for rec in [ctx.get("master", {})] + list(ctx.get("derivatives", [])):
            rel = web005b_file("web_005b.context", rec)
            if rel:
                own.add(rel)
            width = rec.get("width") or (rec.get("dimensions") or [None])[0]
            if isinstance(width, int) and isinstance(ctx_ceiling, int) and width > ctx_ceiling:
                fail(f"web_005b.context {rel} is wider than the native frame", errors)
        w5b_own["context"] = own
        aoi = ctx.get("frame", {}).get("aoi_in_frame", {})
        mark = re.search(r"\.aoi-mark\{position:absolute;left:([\d.]+)%;right:([\d.]+)%;"
                         r"top:([\d.]+)%;bottom:([\d.]+)%", css_text)
        if not mark or not aoi:
            fail("Act 2 AOI corner marks or their recorded geometry are missing", errors)
        else:
            expect = (aoi["x0"] * 100, (1 - aoi["x1"]) * 100, aoi["y0"] * 100, (1 - aoi["y1"]) * 100)
            if any(abs(float(got) - want) > 0.001 for got, want in zip(mark.groups(), expect)):
                fail(f"Act 2 AOI corner marks {mark.groups()} do not match the recorded analysis-grid "
                     f"bounds {tuple(round(v, 4) for v in expect)}", errors)

        ana = w5b.get("analytical", {})
        layers = ana.get("layers", {})
        if set(layers) != set(WEB005B_SOURCES):
            fail(f"web_005b.analytical layers {sorted(layers)} != {sorted(WEB005B_SOURCES)}", errors)
        for item in WEB005B_HERO_ONLY:
            if item not in ana.get("not_used", []):
                fail(f"web_005b.analytical does not record that the hero-only transform "
                     f"{item!r} is unused", errors)
        for key, (src_sha, norm, (olo, ohi)) in WEB005B_SOURCES.items():
            layer = layers.get(key, {})
            label = f"web_005b.analytical.{key}"
            if layer.get("source_sha256") != src_sha:
                fail(f"{label}: governed source is not the MER-108 pinned raster", errors)
            if layer.get("normalization") != norm:
                fail(f"{label}: normalization {layer.get('normalization')!r} is not the canonical {norm!r}", errors)
            if layer.get("topology_id") != WEB005B_TOPOLOGY[key]:
                fail(f"{label}: palette topology is not {WEB005B_TOPOLOGY[key]!r}", errors)
            opacity = layer.get("analytical_opacity")
            if not isinstance(opacity, (int, float)) or not olo <= opacity <= ohi:
                fail(f"{label}: analytical opacity {opacity} is outside {olo}-{ohi}", errors)
            stops = layer.get("stops") or []
            if hashlib.sha256(web005b_lut(stops)).hexdigest() != layer.get("lut_sha256"):
                fail(f"{label}: recorded LUT checksum does not match its recorded stops", errors)
            resolved = layer.get("resolved", {})
            if key == "priority" and (resolved.get("vmin"), resolved.get("vmax")) != (0.0, 100.0):
                fail(f"{label}: priority must stay on the fixed 0-100 range", errors)
            if key == "thm01" and (resolved.get("center") != 0.0 or resolved.get("vmin") != -resolved.get("vmax", 0)):
                fail(f"{label}: THM-01 must stay symmetric about a 0.0 centre", errors)
            own = set()
            for deriv in layer.get("derivatives", []):
                rel = web005b_file(label, deriv)
                if rel:
                    own.add(rel)
                if not isinstance(deriv.get("width"), int) or deriv["width"] > WEB005B_NATIVE_PX:
                    fail(f"{label}: {rel} is above the native {WEB005B_NATIVE_PX} px grid", errors)
                if "lossless" not in str(deriv.get("format", "")):
                    fail(f"{label}: {rel} is not a lossless encode", errors)
            if key == "priority":
                rel = web005b_file(f"{label}.legend", layer.get("legend", {}))
                if rel:
                    own.add(rel)
            w5b_own[key] = own

        # ------------------------------------------------------------------
        # WEB-005B R3 delivery encoding. The lossless derivative stays in the repository as the
        # reference; what the page fetches may be a lossy re-encode of it, but only under MER-108
        # section 8 — same dimensions, same pixels to the eye, no false class, clean NoData. Every
        # claim in that record is re-checked here against the file on disk, and the decoded
        # comparison must stay inside the limits the record itself declares.
        # ------------------------------------------------------------------
        delivery = ana.get("delivery", {})
        delivery_paths: set[str] = set()
        if delivery:
            for key in ("authority", "science", "codec", "limits", "quality_ladder", "layers"):
                if not delivery.get(key):
                    fail(f"web_005b.analytical.delivery missing field: {key}", errors)
            limits = delivery.get("limits", {})
            for layer_key, entries in delivery.get("layers", {}).items():
                own_refs = {str(d.get("path", "")) for d in layers.get(layer_key, {}).get("derivatives", [])}
                widths = {int(d.get("width", 0)) for d in layers.get(layer_key, {}).get("derivatives", [])}
                if {int(e.get("width", 0)) for e in entries} != widths:
                    fail(f"web_005b delivery for {layer_key!r} does not cover the same widths as its "
                         f"lossless derivatives", errors)
                for entry in entries:
                    label = f"web_005b delivery {layer_key}-{entry.get('width')}"
                    if str(entry.get("reference", "")) not in own_refs:
                        fail(f"{label}: reference is not a lossless derivative of this layer", errors)
                    rel = web005b_file(label, entry)
                    if rel:
                        delivery_paths.add(rel)
                        w5b_own.setdefault(layer_key, set()).add(rel)
                    if int(entry.get("width", 0)) > WEB005B_NATIVE_PX:
                        fail(f"{label}: above the native {WEB005B_NATIVE_PX} px grid", errors)
                    if rel == str(entry.get("reference", "")):
                        # kept lossless: nothing more to prove than the checksum above
                        if "lossless" not in str(entry.get("format", "")):
                            fail(f"{label}: keeps the reference file but is not recorded as lossless", errors)
                        continue
                    if "lossy" not in str(entry.get("format", "")):
                        fail(f"{label}: a separate delivery file must be recorded as lossy", errors)
                    if not entry.get("reduction", 0) > 0:
                        fail(f"{label}: a lossy delivery must record a real payload reduction", errors)
                    if entry.get("bytes", 0) >= entry.get("reference_bytes", 0):
                        fail(f"{label}: is not smaller than the lossless reference it replaces", errors)
                    measured = entry.get("decoded_comparison")
                    if not measured:
                        fail(f"{label}: no decoded comparison against the lossless reference", errors)
                        continue
                    for metric, limit in limits.items():
                        if metric not in measured:
                            fail(f"{label}: decoded comparison does not report {metric}", errors)
                        elif measured[metric] > limit:
                            fail(f"{label}: {metric}={measured[metric]} exceeds the declared limit {limit} "
                                 f"— that is a visible or interpretive change, not a delivery encode", errors)
            # The coupled legend is canonical and never lossy.
            legend = layers.get("priority", {}).get("legend", {})
            if not str(legend.get("path", "")).endswith(".png"):
                fail("the priority legend must stay lossless/canonical (PNG)", errors)
            if any(str(legend.get("path", "")) == p for p in delivery_paths):
                fail("the priority legend must not be re-encoded as a delivery candidate", errors)
        placements = w5b.get("placement", {})
        if set(placements) != set(w5b_own):
            fail(f"web_005b.placement covers {sorted(placements)}, expected {sorted(w5b_own)}", errors)
        for key, rec in placements.items():
            own = w5b_own.get(key, set())
            shown_on = [r for r, rp in route_parsers.items() if all_srcs(rp) & own]
            if rec.get("status") == "placed" and "" not in shown_on:
                fail(f"web_005b asset {key!r} claims a homepage placement but is not on the homepage", errors)
            if [r for r in shown_on if r != ""]:
                fail(f"web_005b asset {key!r} is published beyond the homepage: "
                     f"{[ROUTES[r] for r in shown_on if r != '']}", errors)
            if rec.get("visible_warning"):
                check_warning_coverage("web_005b asset", key, rec["visible_warning"], shown_on)
            else:
                fail(f"web_005b asset {key!r} has no visible_warning binding", errors)
            rendered = rec.get("rendered", {})
            css_w, dpr, native = (rendered.get("max_css_width"), rendered.get("device_pixel_ratio_considered"),
                                  rendered.get("native_px"))
            if not all(isinstance(v, (int, float)) for v in (css_w, dpr, native)):
                fail(f"web_005b asset {key!r} placement.rendered is incomplete", errors)
            elif css_w * dpr > native:
                fail(f"web_005b asset {key!r} is laid out at {css_w} CSS px = {int(css_w * dpr)} device px "
                     f"at {dpr}x, above its native {native} px", errors)
            if str(rendered.get("selected_derivative", "")) not in own:
                fail(f"web_005b asset {key!r} names a selected derivative that is not its own", errors)
        # The CSS caps that make those records true. WEB-005B R11 renamed the Act-3 panel to the
        # one shared frame and added the inspection aid, which draws the same governed rasters and
        # therefore carries the same cap.
        for selector, cap in ((".context-band", 1600), (".evidence-frame", 600),
                              (".priority-frame", 600), (".inspect-frame", 600)):
            block = re.search(re.escape(selector) + r"\{[^}]*max-width:(\d+)px", css_text)
            if not block or int(block.group(1)) != cap:
                fail(f"{selector} must be capped at max-width:{cap}px (native density)", errors)

        # ------------------------------------------------------------------
        # WEB-005B R11 inspection aid. Its whole claim is that both sides of the wipe are the SAME
        # 36 x 36 km ground, which is only true if the photograph is scaled and offset by the
        # recorded analysis-grid fractions. The prototype could only promise "approximate common
        # framing"; these four numbers are what turns that into a fact, so they are recomputed here
        # from the manifest rather than trusted as authored constants.
        # ------------------------------------------------------------------
        if aoi:
            span_x, span_y = aoi["x1"] - aoi["x0"], aoi["y1"] - aoi["y0"]
            want = (-aoi["x0"] / span_x * 100, -aoi["y0"] / span_y * 100, 100 / span_x, 100 / span_y)
            got = re.search(r"\.inspect-base>img\{position:absolute;left:(-?[\d.]+)%;top:(-?[\d.]+)%;"
                            r"width:([\d.]+)%;height:([\d.]+)%", css_text)
            if not got:
                fail("the inspection aid does not register its photograph against the recorded "
                     "analysis-grid fractions; without that the two sides are not the same ground",
                     errors)
            elif any(abs(float(a) - b) > 0.01 for a, b in zip(got.groups(), want)):
                fail(f"inspection-aid registration {got.groups()} does not match the recorded "
                     f"analysis-grid bounds {tuple(round(v, 4) for v in want)}", errors)
            if int(round(span_x * 3200)) != int(round(span_y * 1800)):
                fail("the recorded analysis grid is not square inside the context frame; the "
                     "inspection aid's square wipe would not be the same ground", errors)

    # ------------------------------------------------------------------
    # WEB-005B R11 domain cards. The three illustrative Landsat scenes were retired from the
    # homepage by WEB-002 and are placed again by the accepted final design — as photography
    # beside a domain, never as evidence. Each declares that placement, and the layout may not
    # ask a 2x display for more pixels than the widest candidate it is offered.
    # ------------------------------------------------------------------
    for scene in scenes:
        own = {str(d.get("path", "")) for d in scene.get("derivatives", [])}
        shown_on = [r for r, rp in route_parsers.items() if all_srcs(rp) & own]
        placement = scene.get("web_005b_placement")
        sid = scene.get("id", "<unknown>")
        if not shown_on:
            if placement and placement.get("status") == "placed":
                fail(f"scene {sid!r} claims a WEB-005B placement but appears on no route", errors)
            continue
        if not placement:
            continue  # a scene placed by an earlier task keeps that task's contract
        if [r for r in shown_on if r != ""]:
            fail(f"scene {sid!r} is placed for the homepage but also appears on "
                 f"{[ROUTES[r] for r in shown_on if r != '']}", errors)
        rendered = placement.get("rendered", {})
        for field in ("max_css_width", "device_pixel_ratio_considered", "widest_candidate_px",
                      "selected_derivative"):
            if rendered.get(field) in (None, ""):
                fail(f"scene {sid!r} web_005b_placement.rendered missing {field}", errors)
        css_w, dpr = rendered.get("max_css_width"), rendered.get("device_pixel_ratio_considered")
        widest = rendered.get("widest_candidate_px")
        if all(isinstance(v, (int, float)) for v in (css_w, dpr, widest)) and css_w * dpr > widest:
            fail(f"scene {sid!r} is laid out at {css_w} CSS px = {int(css_w * dpr)} device px at "
                 f"{dpr}x, above its widest {widest} px candidate", errors)
        if str(rendered.get("selected_derivative", "")) not in own:
            fail(f"scene {sid!r} names a selected derivative that is not its own", errors)
        # An illustrative photograph that loses its "this is not a result" framing is exactly the
        # kind of drift the imagery policy exists to stop.
        for key in placement.get("visible_label_i18n_keys", []):
            if key not in parser.i18n_keys:
                fail(f"scene {sid!r} is placed on the homepage but its label key {key!r} is not "
                     f"rendered there", errors)
        for lang in ("en", "tr"):
            if dictionary_value(lang, "domains.illustrative") is None:
                fail(f"the domain photography footnote is missing from the {lang!r} dictionary",
                     errors)

        root_block = re.search(r":root\{(.*?)\n\}", css_text, re.S)
        for name, value in WEB005B_TOKENS.items():
            defs = re.findall(re.escape(name) + r":\s*(#[0-9A-Fa-f]{6})\s*;", css_text)
            if len(defs) != 1 or not root_block or f"{name}:{value}" not in root_block.group(1).replace(" ", ""):
                fail(f"palette token {name} must be defined once in :root as {value}", errors)

        if dictionary_value("en", "label.priority") != "Remote-Sensing Relative Priority — Experimental Baseline":
            fail("the priority public label changed", errors)
        if 'class="scale-strip"' in home or "priority-scale.png" in home:
            fail("a detached scientific scale strip is on the homepage", errors)
        figure = re.search(r'<figure class="priority-stage".*?</figure>', home, re.S)
        if not figure or "priority-legend-ramp.png" not in figure.group(0):
            fail("the priority legend must sit inside the result figure", errors)

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
        poster_paths = {path for path in poster_paths if not path.startswith("assets/hero/drape/")}
        unrecorded_poster = poster_paths - recorded_media
        if unrecorded_poster:
            fail(f"hero imagery missing from web_005.hero_media: {sorted(unrecorded_poster)}",
                 errors)
    elif parser.hero_media:
        fail("index.html declares hero media but the manifest has no web_005.hero_media record",
             errors)

    # ------------------------------------------------------------------
    # WEB-005A final production hero payoff. Product passed the preview gates and decided the
    # delivery (docs/web-005-polish-authority c7c6cb1 section 3, b9579ef sections 3-4): the motion
    # video ends on one held frame and carries no analytical pixel; Terrain, THM-01, ALT-01 and the
    # priority surface are lossless full-frame drape states composited by the page over that frame,
    # ending on the priority surface alone; and the hero carries NO colour bar, legend, card or
    # layer label -- Acts 3 and 4 do. What is checkable here:
    #   - the anchor the markup carries matches the audit of the held frame (true 36 km AOI), and
    #     the states share the poster's fit rule, which is what registers them with no placement;
    #   - exactly the four states, in the accepted order, each a recorded, checksummed, lossless
    #     8-bit RGBA PNG at the delivered frame size, tied to the display texture it was draped with;
    #   - every state is data-src (a phone fetches none, a static desktop visitor only the payoff),
    #     with a <noscript> image of the payoff for visitors without JavaScript;
    #   - none of the retired chrome is back.
    # ------------------------------------------------------------------
    home = route_html.get("", "")
    css_text = (ROOT / "styles.css").read_text(encoding="utf-8")
    anchor_match = re.search(r"data-hero-anchor='([^']+)'", home)
    if not anchor_match:
        fail("index.html hero declares no data-hero-anchor; the copy column cannot yield to the "
             "analytical payoff", errors)
    else:
        try:
            anchor = json.loads(anchor_match.group(1))
        except json.JSONDecodeError as error:
            anchor = None
            fail(f"data-hero-anchor is not valid JSON: {error}", errors)
        audit_path = ROOT / "hero" / "evidence" / "shot_audit_production.json"
        if anchor is not None and not audit_path.exists():
            fail("hero/evidence/shot_audit_production.json is missing; the hero anchor has "
                 "nothing to be checked against", errors)
        elif anchor is not None:
            audit = json.loads(audit_path.read_text(encoding="utf-8"))
            measured = audit.get("handoff_anchor", {})
            if audit.get("failed") not in (0, None) or not audit.get("passed"):
                fail("hero/evidence/shot_audit_production.json records a failing production audit", errors)
            if measured.get("fixture") != "kizildere_analysis" or anchor.get("fixture") != "kizildere_analysis":
                fail("hero anchor must be the audited 36 km analysis AOI (fixture kizildere_analysis) "
                     "in both the markup and the production audit", errors)
            for key in ("x", "y", "extent"):
                got = anchor.get(key)
                want = measured.get(key)
                if not isinstance(got, (int, float)) or not isinstance(want, (int, float)):
                    fail(f"hero anchor {key} missing in markup or audit", errors)
                elif abs(float(got) - float(want)) > 0.006:
                    fail(f"hero anchor {key} = {got} drifts from the audited held frame "
                         f"({want}); re-run the production audit and update data-hero-anchor", errors)
            corners_got = anchor.get("corners")
            corners_want = measured.get("corners")
            if not (isinstance(corners_got, list) and isinstance(corners_want, list)
                    and len(corners_got) == 4 and len(corners_want) == 4
                    and all(isinstance(c, list) and len(c) == 2 for c in corners_got)
                    and all(abs(float(a[0]) - float(b[0])) <= 0.006 and abs(float(a[1]) - float(b[1])) <= 0.006
                            for a, b in zip(corners_got, corners_want))):
                fail(f"hero anchor corners {corners_got} drift from the audited analysis AOI corners "
                     f"{corners_want}", errors)
            if list(anchor.get("frame", [])) != [1920, 1080]:
                fail("hero anchor frame size must be the delivered 1920 x 1080", errors)
            position = re.search(r"\.hero-poster,\.hero-held,\.hero-video\{[^}]*object-position:center (\d+)%", css_text)
            if not position:
                fail("styles.css no longer declares the hero object-position the anchor assumes", errors)
            elif abs(float(anchor.get("position", -1)) - int(position.group(1)) / 100.0) > 1e-6:
                fail(f"hero anchor position {anchor.get('position')} does not match the CSS "
                     f"object-position ({position.group(1)}%)", errors)
            else:
                drape_rule = re.search(r"\.hero-drape-layer\{([^}]*)\}", css_text)
                rule = drape_rule.group(1) if drape_rule else ""
                if not ("object-fit:cover" in rule and f"object-position:center {position.group(1)}%" in rule
                        and "inset:0" in rule and "width:100%" in rule and "height:100%" in rule):
                    fail("styles.css: .hero-drape-layer must share the poster's box, object-fit and "
                         "object-position exactly; that is the only thing that registers the states", errors)
                if "filter:none" not in rule:
                    fail("styles.css must declare the hero drape states unfiltered (filter:none)", errors)

    hero_markup = re.search(r'<section class="hero".*?</section>', home, re.S)
    hero_html = hero_markup.group(0) if hero_markup else ""
    drape = re.search(r'<div class="hero-drape" data-hero-drape hidden>(.*?)</div>', hero_html, re.S)
    drape_records = {str(m.get("layer", "")): m for m in manifest.get("web_005", {}).get("hero_drape_states", [])}
    if not drape:
        fail("index.html has no data-hero-drape block inside the hero (or it is not hidden until script.js "
             "reveals it)", errors)
    else:
        drape_body = drape.group(1)
        fallback = re.search(r'<noscript>(.*?)</noscript>', drape_body, re.S)
        drape_body = re.sub(r'<noscript>.*?</noscript>', '', drape_body, flags=re.S)
        priority_record = drape_records.get("priority", {})
        if not fallback or f'src="{priority_record.get("path")}"' not in fallback.group(1):
            fail("hero drape has no <noscript> image of the recorded priority state; with JavaScript off "
                 "the payoff would be missing", errors)
        layers = re.findall(r'<img\b([^>]*?)/?>', drape_body, re.S)
        order = [re.search(r'data-layer="([^"]+)"', body).group(1) for body in layers
                 if re.search(r'data-layer="([^"]+)"', body)]
        if order != HERO_DRAPE_LAYERS:
            fail(f"hero drape states are {order}; the accepted order is {HERO_DRAPE_LAYERS} "
                 f"(context, thermal, alteration, then the priority payoff)", errors)
        for body in layers:
            name_match = re.search(r'data-layer="([^"]+)"', body)
            if not name_match:
                continue
            name = name_match.group(1)
            src = re.search(r'(?<![-\w])src="([^"]+)"', body)
            deferred = re.search(r'data-src="([^"]+)"', body)
            url = (src or deferred).group(1) if (src or deferred) else ""
            record = drape_records.get(name)
            if not record or record.get("path") != url:
                fail(f"hero drape state {name!r} shows {url!r}, which is not its recorded "
                     f"web_005.hero_drape_states file", errors)
            if name == "priority":
                if "hero-drape-payoff" not in body:
                    fail("the priority drape state must be the payoff (class hero-drape-payoff)", errors)
                if 'data-i18n-alt="alt.heroPriority"' not in body:
                    fail("the priority drape state must carry its localized alt text (alt.heroPriority)", errors)
            if src or not deferred:
                fail(f"hero drape state {name!r} must be data-src only: script.js promotes it on the desktop "
                     f"reveal, so a phone never fetches it and a static visitor fetches only the payoff", errors)
    if len(drape_records) != len(HERO_DRAPE_LAYERS) or list(drape_records) != HERO_DRAPE_LAYERS:
        fail(f"web_005.hero_drape_states must record exactly {HERO_DRAPE_LAYERS}, in that order", errors)
    ingest_path = ROOT / "hero" / "evidence" / "web005a_r3_preview" / "analytical_asset_ingest.json"
    ingested = {}
    if ingest_path.exists():
        ingested = {str(e.get("materialized")): e for e in json.loads(ingest_path.read_text(encoding="utf-8")).get("files", [])}
    for name, record in drape_records.items():
        rel = str(record.get("path", ""))
        path = ROOT / rel
        for key in ("layer", "path", "bytes", "sha256", "width", "height", "encoding", "scene", "rendered_frame",
                    "view_transform", "display_texture", "display_texture_sha256"):
            if record.get(key) in (None, ""):
                fail(f"hero drape state {name!r} missing field: {key}", errors)
        if not rel.startswith("assets/hero/drape/") or not path.exists():
            fail(f"hero drape state missing from repository: {rel}", errors)
            continue
        data = path.read_bytes()
        if sha256_of(path) != str(record.get("sha256", "")) or len(data) != record.get("bytes"):
            fail(f"hero drape state checksum or size mismatch for {rel}", errors)
        # Lossless by rule: an 8-bit RGBA PNG at the delivered frame size, nothing else.
        is_png = data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR"
        width = int.from_bytes(data[16:20], "big") if is_png else 0
        height = int.from_bytes(data[20:24], "big") if is_png else 0
        if not is_png or (width, height) != (1920, 1080) or data[24] != 8 or data[25] != 6:
            fail(f"hero drape state {rel} is not a lossless 8-bit RGBA PNG at 1920 x 1080; a lossy encode "
                 f"changes the colours the layer is read by", errors)
        if len(data) > HERO_DRAPE_STATE_CEILING:
            fail(f"hero drape state {rel} is {len(data) / 1048576:.2f} MiB, over the "
                 f"{HERO_DRAPE_STATE_CEILING / 1048576:.2f} MiB per-state ceiling", errors)
        if record.get("view_transform") != "Standard" or record.get("denoise") not in (False,):
            fail(f"hero drape state {name!r} must be rendered through a Standard view with no denoiser", errors)
        texture = ingested.get(str(record.get("display_texture")), {})
        if texture.get("use") != "display_texture" or texture.get("sha256") != record.get("display_texture_sha256"):
            fail(f"hero drape state {name!r} is not tied to an ingested prepared display texture "
                 f"({record.get('display_texture')})", errors)

    # ------------------------------------------------------------------
    # WEB-005A startup poster vs held base (docs/web-005-polish-authority@1437fbb). Showing the held
    # frame before the motion read as a reverse-story flash, so the startup poster is the OPENING
    # frame wherever the motion is about to play. The held frame stays a separate still: the poster
    # where the motion never plays, and the base every static state lays over the startup poster
    # before the payoff -- the drape states register with the held frame and with nothing else.
    # ------------------------------------------------------------------
    media_by_role = {str(m.get("role", "")): m for m in manifest.get("web_005", {}).get("hero_media", [])}
    opening, held_wide, held_narrow = (media_by_role.get(r, {}) for r in
                                       ("hero-poster-opening", "hero-poster", "hero-poster-narrow"))
    if not opening:
        fail("web_005.hero_media has no 'hero-poster-opening' record: the startup poster must be the opening "
             "frame, separate from the held base", errors)
    else:
        if not re.search(r"_f1\.png$", str(opening.get("source_frame", ""))):
            fail("the startup poster (hero-poster-opening) must be made from the first motion frame", errors)
        if not re.search(r"_f276\.png$", str(held_wide.get("source_frame", ""))):
            fail("the held base (hero-poster) must be made from the held frame the video ends on", errors)
        held_srcset = f'{held_narrow.get("path")} 900w, {held_wide.get("path")} 1600w'
        picture = re.search(r'<picture>(.*?)</picture>', hero_html, re.S)
        poster_img = re.search(r'<img\b[^>]*class="panel-image hero-poster"[^>]*>', picture.group(1), re.S) if picture else None
        source = re.search(r'<source\b[^>]*>', picture.group(1), re.S) if picture else None
        if not poster_img or f'src="{opening.get("path")}"' not in poster_img.group(0) or "srcset=" in poster_img.group(0):
            fail("the hero poster <img> must be the recorded startup poster (hero-poster-opening) inside a <picture>; "
                 "a held-frame startup poster flashes the ending before the Earth establish", errors)
        if not source or f'media="{HERO_STATIC_POSTER_MEDIA}"' not in source.group(0) \
                or f'srcset="{held_srcset}"' not in source.group(0):
            fail("the hero <picture> must swap in the held frame exactly where the motion never plays "
                 f"({HERO_STATIC_POSTER_MEDIA}); those visitors end on it", errors)
        preloads = re.findall(r'<link\b[^>]*rel="preload"[^>]*as="image"[^>]*>', home, re.S)
        motion_preload = [l for l in preloads if f'href="{opening.get("path")}"' in l]
        static_preload = [l for l in preloads if f'imagesrcset="{held_srcset}"' in l]
        if len(motion_preload) != 1 or f'media="{HERO_MOTION_POSTER_MEDIA}"' not in motion_preload[0]:
            fail("the startup poster preload must exist once and carry the complement of the <picture> source "
                 f"media ({HERO_MOTION_POSTER_MEDIA}), or a visitor preloads a still they are never shown", errors)
        if len(static_preload) != 1 or f'media="{HERO_STATIC_POSTER_MEDIA}"' not in static_preload[0]:
            fail("the held-frame preload must exist once and carry the <picture> source media exactly", errors)
        held_img = re.search(r'<img\b[^>]*data-hero-held[^>]*>', hero_html, re.S)
        if not held_img or f'data-src="{held_wide.get("path")}"' not in held_img.group(0) \
                or f'data-srcset="{held_srcset}"' not in held_img.group(0) \
                or re.search(r'(?<![-\w])src="', held_img.group(0)):
            fail("the hero needs a deferred held base (img[data-hero-held], data-src = the recorded held frame): "
                 "static states must never lay the payoff over the opening Earth", errors)
        if not re.search(r'<noscript><img class="hero-held is-on" src="' + re.escape(str(held_wide.get("path"))) + '"', hero_html):
            fail("the hero needs a <noscript> held base under the <noscript> payoff", errors)
        held_rule = re.search(r"\.hero-poster,\.hero-held,\.hero-video\{([^}]*)\}", css_text)
        if not held_rule or "object-fit:cover" not in held_rule.group(1):
            fail("styles.css: the held base must share the poster's and the video's box and fit rule", errors)

    # ------------------------------------------------------------------
    # WEB-005A relief rise (docs/web-005-polish-authority@0e87675): the DEM relief rises between the
    # held frame and the Terrain state as 6-12 lossless rendered states over 0.45-0.70 s, outline and
    # shadow rising with it; motion path only; Terrain -> THM-01 -> ALT-01 -> priority unchanged.
    # ------------------------------------------------------------------
    rise = manifest.get("web_005", {}).get("hero_relief_rise") or {}
    rise_states = rise.get("states") or []
    if not rise_states:
        fail("web_005.hero_relief_rise is missing: without it the relief jumps from the flat held frame to the "
             "fully raised Terrain state", errors)
    else:
        frames = [int(state.get("frame", -1)) for state in rise_states]
        if not 6 <= len(frames) <= 12:
            fail(f"hero relief rise has {len(frames)} states; the authorized transition is 6-12", errors)
        if frames != sorted(set(frames)) or frames[0] <= int(rise.get("held_frame", 10**6)) \
                or frames[-1] >= int(rise.get("terrain_state_frame", -1)):
            fail("hero relief rise frames must increase strictly between the held frame and the Terrain state frame", errors)
        span = (int(rise.get("terrain_state_frame", 0)) - int(rise.get("held_frame", 0))) / float(rise.get("frame_rate") or 1)
        if not 0.45 <= span <= 0.70 or abs(span - float(rise.get("duration_seconds", -1))) > 1e-3:
            fail(f"hero relief rise lasts {span:.3f} s; the authorized duration is 0.45-0.70 s", errors)
        if rise.get("view_transform") != "Standard" or rise.get("denoise") not in (False,):
            fail("hero relief rise states must be rendered through a Standard view with no denoiser", errors)
        terrain_record = drape_records.get("terrain", {})
        if rise.get("display_texture_sha256") != terrain_record.get("display_texture_sha256") \
                or int(rise.get("terrain_state_frame", -1)) != int(terrain_record.get("rendered_frame", -2)):
            fail("hero relief rise must end on the recorded Terrain state (same display texture, same frame)", errors)
        total = 0
        for state in rise_states:
            rel = str(state.get("path", ""))
            path = ROOT / rel
            if not rel.startswith("assets/hero/drape/") or not path.exists():
                fail(f"hero relief rise state missing from repository: {rel}", errors)
                continue
            data = path.read_bytes()
            total += len(data)
            if sha256_of(path) != str(state.get("sha256", "")) or len(data) != state.get("bytes"):
                fail(f"hero relief rise state checksum or size mismatch for {rel}", errors)
            # Lossless by rule: a VP8L (lossless) WebP with alpha at the delivered frame size.
            is_vp8l = data[:4] == b"RIFF" and data[8:12] == b"WEBP" and data[12:16] == b"VP8L" and data[20] == 0x2F
            bits = int.from_bytes(data[21:25], "little") if is_vp8l else 0
            if not is_vp8l or ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1) != (1920, 1080) or not (bits >> 28) & 1:
                fail(f"hero relief rise state {rel} is not a lossless (VP8L) RGBA WebP at 1920 x 1080", errors)
            if len(data) > HERO_RISE_STATE_CEILING:
                fail(f"hero relief rise state {rel} is over the {HERO_RISE_STATE_CEILING // 1024} KiB per-state ceiling", errors)
        if total != rise.get("total_bytes") or total > HERO_RISE_TOTAL_CEILING:
            fail(f"hero relief rise payload is {total} bytes; it must match the record and stay under "
                 f"{HERO_RISE_TOTAL_CEILING / 1048576:.1f} MiB", errors)
        if drape:
            body = re.sub(r'<noscript>.*?</noscript>', '', drape.group(1), flags=re.S)
            imgs = re.findall(r'<img\b([^>]*?)/?>', body, re.S)
            kinds = ["rise" if "data-rise-frame=" in img else "layer" for img in imgs]
            if kinds != ["rise"] * len(rise_states) + ["layer"] * len(HERO_DRAPE_LAYERS):
                fail("the hero drape must hold the recorded rise states first, then the four drape states", errors)
            for img, state in zip([i for i in imgs if "data-rise-frame=" in i], rise_states):
                if f'data-rise-frame="{state.get("frame")}"' not in img or f'data-src="{state.get("path")}"' not in img \
                        or "hero-drape-rise" not in img:
                    fail(f"hero relief rise markup does not match the recorded state for frame {state.get('frame')}", errors)
                if re.search(r'(?<![-\w])src="', img):
                    fail("hero relief rise states must be data-src only: they belong to the desktop motion path and a "
                         "static or phone visitor must never fetch them", errors)
        if "isolation:isolate" not in (re.search(r"\.hero-drape\{([^}]*)\}", css_text) or [None, ""])[1]:
            fail("styles.css: .hero-drape must be an isolated group, or the rise interpolation adds itself to the video", errors)
        rise_rule = re.search(r"\.hero-drape-rise,[^{]*\{mix-blend-mode:plus-lighter\}", css_text)
        if not rise_rule or ".hero-drape-rise,.hero-drape.is-rising .hero-drape-layer{transition:none}" not in css_text:
            fail("styles.css: the rise states must interpolate with plus-lighter and no CSS transition "
                 "(a plain cross-fade of partly transparent states dips in the middle)", errors)
        script_rise = (ROOT / "script.js").read_text(encoding="utf-8")
        if "function playRise(" not in script_rise or "riseReady()" not in script_rise:
            fail("script.js must play the relief rise (playRise) and fall back when it is not decoded (riseReady)", errors)
        if script_rise.count("riseImages().forEach(promote)") != 1:
            fail("script.js may promote the rise states in exactly one place (warmLayers, the motion path)", errors)
        if "showHeldBase(() => revealPayoff(true))" not in script_rise \
                or re.search(r"function settleStatic\(reason\) \{(?:(?!\n  \}).)*?\n    revealPayoff\(true\);", script_rise, re.S):
            fail("script.js: every static state must lay the held base over the startup poster before the payoff "
                 "(showHeldBase), never reveal the payoff directly", errors)

    # Retired chrome may not come back (Product decision b9579ef section 4; CLAUDE.md design invariants).
    for token, what in (
        ("data-hero-stage", "the CSS-homography evidence stage"),
        ("data-hero-handoff", "the floating handoff card"),
        ("hero-handoff", "the floating handoff card"),
        ("hero-layer-legend", "an in-hero legend"),
        ("priority-legend", "an in-hero legend"),
        ("hero-ledger", "the layer ledger"),
        ("beam-note", "a warning caption"),
        ('data-i18n="label.', "a layer label"),
        ("data-hero-target", "the R2 marker/leader handoff"),
        ("hero-target-marker", "the R2 marker/leader handoff"),
    ):
        if token in hero_html:
            fail(f"the hero contains {what} ({token}); the final hero is visual-only and Acts 3-4 carry "
                 f"labels, warnings and legend", errors)
    script_hero = (ROOT / "script.js").read_text(encoding="utf-8")
    if "revealPayoff" not in script_hero or "squareToQuad" in script_hero or "hero-handoff" in script_hero:
        fail("script.js must drive the drape states (revealPayoff) and carry none of the retired "
             "homography / handoff logic", errors)

    # Sensing lines are attention, not physics (A-HERO-04): the hero's own copy may not claim an
    # instrument. Checked on the dictionary in both languages and on the static markup.
    physics = ("radar", "lidar", "hyperspectral", "multispectral", "spectrometer", "swath",
               "wavelength", "backscatter", "radiometer", "sar ")
    script_text = (ROOT / "script.js").read_text(encoding="utf-8")
    hero_strings = re.findall(r"'((?:hero\.|scene\.hero\.|alt\.hero)[a-zA-Z.]*)':\s*'((?:[^'\\]|\\.)*)'", script_text)
    hero_copy = " ".join(v.lower() for _, v in hero_strings)
    hero_markup = re.search(r'<section class="hero".*?</section>', home, re.S)
    hero_copy += " " + (hero_markup.group(0).lower() if hero_markup else "")
    for term in physics:
        if term in hero_copy:
            fail(f"hero copy claims sensing physics: {term.strip()!r}", errors)

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
