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
]

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
        self._note_depth = 0
        self._open: list[bool] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        # A mandatory scientific warning is allowed to name what the score is NOT; ordinary
        # marketing copy is not allowed to use those phrases at all.
        is_note = "beam-note" in str(data.get("class") or "").split()
        self._open.append(is_note)
        if is_note:
            self._note_depth += 1
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

    def handle_data(self, data: str) -> None:
        self.text.append(data)
        if self._note_depth == 0:
            self.claim_text.append(data)


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

    print("OrbGSS site validation")
    print(f"  scenes: {len(scenes)}")
    print(f"  html images: {len(parser.img_srcs)}")
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
