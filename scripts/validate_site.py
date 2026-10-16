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
    ".vercelignore",
    "robots.txt",
    "sitemap.xml",
    "404.html",
    # MER-240 / Milestone 6 public routes (docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md section 2)
    "solutions/index.html",
    "solutions/geothermal/index.html",
    "about/index.html",
    "partner/index.html",
]

# Canonical public route -> its file, relative to ROOT. "" is the homepage. MER-240 replaced the
# WEB-003 set (platform, pilot, company, contact); those routes are 301 redirects now (REDIRECTS).
ROUTES = {
    "": "index.html",
    "solutions": "solutions/index.html",
    "solutions/geothermal": "solutions/geothermal/index.html",
    "about": "about/index.html",
    "partner": "partner/index.html",
}
# Served pages that are not canonical routes: no canonical URL, no sitemap entry, but the same
# navigation, links and EN/TR parity as every route.
AUX_PAGES = {"404": "404.html"}


def canonical_url(route: str) -> str:
    return f"https://orbgss.com/{route + '/' if route else ''}"

# MER-237: the deployed file set. Vercel uploads and serves every repository file .vercelignore does
# not exclude, so before MER-237 orbgss.com also served STATUS.md, CLAUDE.md, docs/, tasks/,
# evidence/, scripts/ and hero/. .vercelignore is now a root allowlist; the validator models exactly
# that form (one "/*" rule, then "!<root entry>" lines) and refuses any other syntax rather than
# guess how Vercel would read it.
DEPLOY_IGNORE = ".vercelignore"
# vercel.json is project configuration: Vercel needs it in the upload but does not serve it.
DEPLOY_REQUIRED_ENTRIES = ["index.html", "404.html", "vercel.json"]
DEPLOY_EXCLUDED_PATHS = [
    "STATUS.md", "CLAUDE.md", "AGENTS.md", "README.md", "CHANGELOG.md", "IMAGERY_RIGHTS.md",
    "CLAUDE_SESSION_BOOTSTRAP.txt", "preview-local.bat", DEPLOY_IGNORE,
    "docs/", "tasks/", "evidence/", "scripts/", "hero/", "references/",
]
# Documentation and tooling, never site content, wherever they sit.
DEPLOY_INTERNAL_SUFFIXES = {".md", ".py", ".pyc", ".bat", ".ps1", ".sh", ".blend"}
# Public text files whose references the browser (or a crawler) follows.
DEPLOY_TEXT_SUFFIXES = {".html", ".css", ".js", ".webmanifest", ".xml", ".txt"}
# A root-relative or absolute orbgss.com path in an attribute: "/", "/pilot/#x", "/styles.css".
_ROOT_PATH_REF = re.compile(r"""(?<![\w-])(?:href|src|poster|content|data-src)=["'](?:https://orbgss\.com)?/([^"'#?\s]*)""")
# A document-relative path in an attribute ("styles.css" on the homepage); resolved against the
# referring file's directory, exactly as the browser does.
_RELATIVE_PATH_REF = re.compile(r"""(?<![\w-])(?:href|src|poster|data-src)=["'](?![a-zA-Z][\w+.-]*:|/|#)([^"'#?\s]+)""")
# Any assets/ path, relative or absolute, including srcset tokens and the hero ladder's JSON.
_ASSET_REF = re.compile(r"(?<![\w./-])(?:https://orbgss\.com)?/?(assets/[\w./%-]*\w)")
# Sitemap entries and the robots.txt sitemap pointer.
_SITEMAP_REF = re.compile(r"(?:<loc>|^Sitemap:\s*)https://orbgss\.com/([^<\s#?]*)", re.M)
_CSS_URL_REF = re.compile(r"""url\(\s*["']?([^"')\s]+)["']?\s*\)""")

# WEB-005 four-act structure: the act anchors, the evidence trio, the data-gap note, the pilot
# ledger and the trust/contact zone. The WEB-001/002 six-scene gallery anchors (observe/platform,
# geothermal as separate full-width scenes) are deliberately gone.
# WEB-005B R13 / WEB-005C: the public domain taxonomy is Geothermal / Mining / Marine, on the
# homepage and on /solutions/ alike. WEB-005C converged the two: the superseded application-ledger
# labels are gone from visible copy, and #mineral / #environment survive only as compatibility
# aliases on their renamed /solutions/ rows so existing deep links keep resolving.
# WEB-005B R14: the section is "Solutions" and carries the #solutions anchor; it is no longer
# framed as a pilot panel, so there is no #pilot section on the homepage.
# MER-240: Method (#proof) and Company (#company) moved to /about/; #contact stays as the one
# Partner line, so existing /#contact links still land.
REQUIRED_SECTION_IDS = {
    "hero", "context", "evidence", "terrain", "thermal", "alteration", "structure", "priority",
    "solutions", "geothermal", "mining", "marine", "contact",
}
RETIRED_HOMEPAGE_SECTION_IDS = {"proof", "company"}
# WEB-005: the homepage's primary visual hierarchy is exactly these four acts, in this order.
REQUIRED_ACTS = ["1", "2", "3", "4"]
# WEB-005C / MER-149: the canonical public domain taxonomy, its route destinations, and the
# superseded labels that may never reappear in visible public copy. The Solutions submenu is the
# one place all three names are published together on every route, so it is pinned in order.
PUBLIC_TAXONOMY = [
    ("geothermal", "nav.geothermal", "Geothermal", "Jeotermal"),
    ("mining", "nav.mining", "Mining", "Madencilik"),
    ("marine", "nav.marine", "Marine", "Denizel"),
]
# Superseded /solutions/ row anchors. They must stay resolvable on /solutions/ (as aliases on the
# renamed rows) so an existing external deep link is not broken by the rename.
LEGACY_DOMAIN_ANCHORS = ["mineral", "environment"]
# WEB-005C R2: the three homepage Solutions cards are navigation surfaces. Each is a native link to
# its domain's home, named by its own card title, so it works with JavaScript disabled and is
# reachable and announced by keyboard. A card that loses its link silently stops being one.
# MER-240: Geothermal's home is its own page; Mining and Marine are bands on the hub.
NAV_TARGETS = {
    "geothermal": "/solutions/geothermal/",
    "mining": "/solutions/#mining",
    "marine": "/solutions/#marine",
}
# Retired domain labels, EN and TR. Matched case-sensitively so the lowercase activity wording the
# Mining row legitimately keeps ("... relevant to mineral targeting") is untouched.
RETIRED_DOMAIN_LABELS = [
    "Mineral Exploration", "Environmental & Land Intelligence",
    "Environmental &amp; Land Intelligence", "Maden Arama", "Çevre ve Arazi Zekâsı",
]
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
    # R15 tonal hierarchy: the lifted and the settled ground the page moves between. Pinned for the
    # same reason as the rest -- a quiet edit here changes the whole page's depth.
    "--orb-lift": "#061420", "--orb-deep": "#020810",
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
# MER-151 / GEO-WEB-004 (geothermal-prospectivity@e8aa5d65) authorizes PRESENTATION derivatives of
# the same 1200 x 1200 / 30 m scientific master for the homepage Evidence, Result and inspection
# surfaces: one final RGBA Lanczos3 resize, 0.50-4.00x per axis, 4800 px per axis at most, with
# bounded display windows and one fixed monotonic gamma per layer. Everything below is a numeric
# bound out of that authority, so a derivative cannot quietly drift past it.
WEB005B_PRESENTATION_CEILING_PX = 4800
WEB005B_PRESENTATION_SCALE = (0.50, 4.00)
WEB005B_WINDOW_BOUNDS = {"q_low": (0.0, 0.02), "q_high": (0.98, 1.0), "min_span": 0.94,
                         "q_abs": (0.98, 1.0), "min_M": 0.70}
WEB005B_GAMMA_BOUNDS = {"terrain": (0.75, 1.35), "alt01": (0.75, 1.35),
                        "priority": (0.75, 1.35), "thm01": (0.80, 1.25)}
# MER-151 section 4: the homepage profile does NOT inherit these from the hero amendment, and
# percentile/window clipping stays prohibited for priority specifically (section 3).
# WEB-005B R14: the wording the domain-photography footnote may not lose. The per-card captions
# that used to carry this are gone, so this footnote is the whole of the honesty now.
DOMAIN_FOOTNOTE_TERMS = {
    "en": ["not OrbGSS analytical outputs", "not results", "not the Kızıldere pilot area"],
    "tr": ["OrbGSS analitik çıktısı değildir", "sonuç değildir", "Kızıldere pilot alanı değildir"],
}
# Transforms the terminal amendment allows for the hero surface only; a homepage derivative that
# records using one of them is outside 11c32e8d.
WEB005B_HERO_ONLY = ("ai_super_resolution", "scalar_space_interpolation", "gaussian smoothing",
                     "unsharp", "clahe_or_local_tone_mapping", "per_crop_autoscaling")

HERO_RISE_STATE_CEILING = 512 * 1024
HERO_RISE_TOTAL_CEILING = int(2.5 * 1024 * 1024)
HERO_STATIC_POSTER_MEDIA = "(prefers-reduced-motion: reduce), (max-width: 780px)"
HERO_MOTION_POSTER_MEDIA = "(prefers-reduced-motion: no-preference) and (min-width: 781px)"
# MER-216: the WEB-004 / WEB-005 envelope (WebM <= 3.0 MiB, MP4 <= 4.5 MiB) binds the 1920 tier; the
# 1280 tier exists to cost less and carries smaller ceilings of its own.
HERO_MEDIA_CEILINGS = {
    "hero-webm-md": 3.0 * 1024 * 1024,
    "hero-mp4-md": 4.5 * 1024 * 1024,
    "hero-webm-sm": 2.0 * 1024 * 1024,
    "hero-mp4-sm": 3.0 * 1024 * 1024,
    "hero-poster": 180 * 1024,
}
HERO_TIER_WIDTHS = {"sm": 1280, "md": 1920}
# WEB-002 claim discipline: wording that would overstate the accepted MVP score if it ever
# appeared in visible homepage copy. The accepted profile is an AOI-relative screening surface.
PROHIBITED_SCORE_COPY = [
    "full prospectivity",
    "probability of geothermal",
    "drilling success",
    "proven reserve",
    "validated accuracy",
]


# ---------------------------------------------------------------------------------------------
# MER-240 / Milestone 6 (docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md). The page set, navigation,
# redirects and the content rules R1-R5 and R8, enforced on the reworked routes.
# ---------------------------------------------------------------------------------------------
# Primary navigation, right-aligned, in exactly this order (authority section 2). None is the
# Solutions menu trigger, which is a button, not a link.
PRIMARY_NAV = [("/", "nav.home"), (None, "nav.solutions"), ("/about/", "nav.about"),
               ("/partner/", "nav.partner")]
FOOTER_NAV = [("/", "nav.home"), ("/solutions/", "nav.solutions"), ("/about/", "nav.about"),
              ("/partner/", "nav.partner")]
NAV_LABELS = {"nav.home": ("Home", "Ana Sayfa"), "nav.solutions": ("Solutions", "Çözümler"),
              "nav.about": ("About", "Hakkımızda"), "nav.partner": ("Partner with us", "İş Birliği")}
# Which navigation entries say aria-current="page" on each page ("menu" is the Solutions trigger).
NAV_CURRENT = {
    "": {"/"},
    "solutions": {"menu"},
    "solutions/geothermal": {"menu", "/solutions/geothermal/"},
    "about": {"/about/"},
    "partner": {"/partner/"},
    "404": set(),
}
# Section 6: the retired routes answer with a permanent redirect, so no inbound link breaks.
REDIRECTS = {
    "/platform/": "/",
    "/pilot/": "/solutions/geothermal/",
    "/company/": "/about/",
    "/contact/": "/partner/",
}
REDIRECT_STATUS = 301
# The fragments old /pilot/ links carry land on the Geothermal page (G3 is absent until MER-242,
# so its aliases sit on G2).
GEOTHERMAL_ANCHORS = ["glance", "layers", "outputs", "gap", "pilot-observe", "pilot-terrain",
                      "pilot-evidence", "pilot-priority", "pilot-geothermal", "pilot-structure"]
# R8: one status vocabulary, everywhere.
M6_STATUS = {
    "app.geothermal.status": ("Active · First application", "Aktif · İlk uygulama"),
    "app.mining.status": ("Expansion direction", "Genişleme yönü"),
    "app.marine.status": ("Expansion direction", "Genişleme yönü"),
}
RETIRED_STATUS_LABELS = ["In development", "Geliştirme aşamasında"]
# R5 text budgets (EN; TR may run up to 15 % longer).
M6_BUDGET = {"headline": 8, "intro": 30, "section": 40, "cell": 12, "rows": 7, "page": 250}
M6_PAGE_BUDGET = {"solutions/geothermal": 350}
M6_TR_ALLOWANCE = 1.15
# R6: fixed texts travel with what they qualify and are exempt from R1 and R5.
M6_FIXED_CLASSES = {"beam-note", "scene-label", "act-footnote", "domain-status", "company-parent"}
# R4: what may lead a section. A table, an image, a map or chart, or the two drawn blocks the
# authority names (the empty data-gap frame and the address block).
LEAD_VISUAL_TAGS = {"table", "img", "figure", "svg", "picture", "video", "canvas"}
LEAD_VISUAL_CLASSES = {"gap-frame", "mail-address"}
# Blocks that may sit in <main> outside a section: the one closing link and the footnote.
M6_LOOSE_BLOCKS = {"page-closing", "page-note"}
# R2: a thumbnail is at most 160 CSS px on its long side.
THUMB_MAX_CSS_PX = 160
# R3: no software or development detail on the reworked routes. Layer codes stay out of visible
# copy as well (authority 4.3), as they have on the homepage since WEB-005B R14.
M6_SOFTWARE_TERMS = [
    "workflow", "pipeline", "workbench", "geo-039", "export path", "thm-01", "alt-01", "alt-02",
    "mvp_remote_sensing", "kizildere_mvp", "geotiff", "stac", "blender", "ffmpeg", "github",
    "python", "javascript", "how the layers are built", "how it's built", "iş akışı",
]
# R1: a sentence this long is a claim; it may be stated on one route only.
M6_CLAIM_MIN_WORDS = 6
WORD_RE = re.compile(r"[^\W_]", re.UNICODE)


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
        self.hero_tiers: str = ""
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
            if data.get("data-hero-tiers"):
                self.hero_tiers = str(data["data-hero-tiers"])
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


class DomNode:
    """A minimal element tree, enough for the M6 structure and text-budget rules."""

    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag: str, attrs: dict, parent: "DomNode | None") -> None:
        self.tag = tag
        self.attrs = attrs
        self.children: list = []
        self.parent = parent

    @property
    def classes(self) -> set[str]:
        return set(str(self.attrs.get("class") or "").split())

    def iter(self):
        yield self
        for child in self.children:
            if isinstance(child, DomNode):
                yield from child.iter()

    def find_all(self, pred) -> list["DomNode"]:
        return [node for node in self.iter() if pred(node)]

    def text(self, skip=None) -> str:
        parts: list[str] = []
        for child in self.children:
            if isinstance(child, str):
                parts.append(child)
            elif not (skip and skip(child)) and child.attrs.get("aria-hidden") != "true":
                parts.append(child.text(skip))
        return " ".join(" ".join(parts).split())

    def ancestors(self):
        node = self.parent
        while node is not None:
            yield node
            node = node.parent


class DomBuilder(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source",
            "track", "wbr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = DomNode("#root", {}, None)
        self._cur = self.root

    def handle_starttag(self, tag: str, attrs) -> None:
        node = DomNode(tag, dict(attrs), self._cur)
        self._cur.children.append(node)
        if tag not in self.VOID:
            self._cur = node

    def handle_startendtag(self, tag: str, attrs) -> None:
        self._cur.children.append(DomNode(tag, dict(attrs), self._cur))

    def handle_endtag(self, tag: str) -> None:
        node = self._cur
        while node is not self.root and node.tag != tag:
            node = node.parent
        if node is not self.root:
            self._cur = node.parent

    def handle_data(self, data: str) -> None:
        if self._cur.tag not in ("script", "style"):
            self._cur.children.append(data)


def build_dom(text: str) -> DomNode:
    builder = DomBuilder()
    builder.feed(text)
    return builder.root


def positioned_css_classes(css: str) -> set[str]:
    """Classes an unconditional top-level rule positions (`.page-section{position:relative;...}`).

    Only a rule whose whole selector is one class counts, and nothing inside an at-rule does: a
    @media block applies at some widths only, so it cannot be what an alias relies on.
    """
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    found: set[str] = set()
    pos = 0
    while True:
        opened = css.find("{", pos)
        if opened < 0:
            break
        prelude = css[pos:opened].strip()
        depth, end = 1, opened + 1
        while end < len(css) and depth:
            depth += {"{": 1, "}": -1}.get(css[end], 0)
            end += 1
        body = css[opened + 1:end - 1]
        pos = end
        if prelude.startswith("@"):
            continue
        if re.search(r"(?:^|;)\s*position\s*:\s*(?:relative|absolute|fixed|sticky)\b", body):
            for selector in prelude.split(","):
                single = re.fullmatch(r"\.([\w-]+)", selector.strip())
                if single:
                    found.add(single.group(1))
    return found


def count_words(text: str) -> int:
    return sum(1 for token in text.split() if WORD_RE.search(token))


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def deploy_target(path: str) -> str:
    """Map a site path to the repository file Vercel serves for it (cleanUrls, trailingSlash)."""
    path = path.split("#", 1)[0].split("?", 1)[0].lstrip("/")
    if path == "" or path.endswith("/"):
        return path + "index.html"
    if "." not in path.rsplit("/", 1)[-1]:
        return path + "/index.html"
    return path


def public_references(rel: str, text: str) -> set[str]:
    """Repository paths the public text file `rel` makes the browser or a crawler request."""
    base = rel.rsplit("/", 1)[0] + "/" if "/" in rel else ""
    found = {deploy_target(m.group(1)) for m in _ROOT_PATH_REF.finditer(text)}
    found |= {deploy_target(base + m.group(1)) for m in _RELATIVE_PATH_REF.finditer(text)}
    found |= {deploy_target(m.group(1)) for m in _SITEMAP_REF.finditer(text)}
    found |= {m.group(1) for m in _ASSET_REF.finditer(text)}
    for m in _CSS_URL_REF.finditer(text):
        url = m.group(1)
        if not url.startswith(("data:", "http:", "https:", "#")):
            found.add(deploy_target(url if url.startswith("/") else base + url))
    return found


def check_deploy_set(errors: list[str]) -> tuple[set[str], int]:
    """MER-237: only the public site is deployed, and everything it references is.

    Returns the allowed root entries and the number of deployed files.
    """
    ignore = ROOT / DEPLOY_IGNORE
    if not ignore.exists():
        return set(), 0
    rules = [ln.strip() for ln in ignore.read_text(encoding="utf-8").splitlines()]
    rules = [ln for ln in rules if ln and not ln.startswith("#")]
    if not rules or rules[0] != "/*":
        fail(f"{DEPLOY_IGNORE}: the first rule must be '/*' (ignore the whole root, then allow "
             f"each public entry), so nothing new is deployed by default", errors)
        return set(), 0
    allowed: set[str] = set()
    for rule in rules[1:]:
        name = rule[1:]
        if not rule.startswith("!") or not name or any(c in name for c in "/\\*?[]!"):
            fail(f"{DEPLOY_IGNORE}: unsupported rule {rule!r}; only '!<root file or directory>' "
                 f"lines are modelled by the validator", errors)
            continue
        if not (ROOT / name).exists():
            fail(f"{DEPLOY_IGNORE}: allows {name!r}, which does not exist", errors)
        allowed.add(name)

    def deployed(rel: str) -> bool:
        return rel.split("/", 1)[0] in allowed

    for name in DEPLOY_REQUIRED_ENTRIES:
        if name not in allowed:
            fail(f"{DEPLOY_IGNORE}: {name} is not deployed", errors)
    for rel in ROUTES.values():
        if not deployed(rel):
            fail(f"{DEPLOY_IGNORE}: public route file {rel} is not deployed", errors)
    for rel in DEPLOY_EXCLUDED_PATHS:
        if deployed(rel):
            fail(f"{DEPLOY_IGNORE}: internal path {rel} would be deployed and publicly served", errors)

    files: list[pathlib.Path] = []
    for name in sorted(allowed):
        entry = ROOT / name
        if entry.is_file():
            files.append(entry)
        elif entry.is_dir():
            files.extend(sorted(p for p in entry.rglob("*") if p.is_file()))
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() in DEPLOY_INTERNAL_SUFFIXES or "__pycache__" in path.parts:
            fail(f"deploy set contains an internal file: {rel}", errors)
    for path in files:
        if path.suffix.lower() not in DEPLOY_TEXT_SUFFIXES:
            continue
        rel = path.relative_to(ROOT).as_posix()
        for target in sorted(public_references(rel, path.read_text(encoding="utf-8", errors="ignore"))):
            if not deployed(target):
                fail(f"{rel}: references {target}, which {DEPLOY_IGNORE} does not deploy", errors)
            elif not (ROOT / target).is_file():
                fail(f"{rel}: references {target}, which does not exist", errors)
    return allowed, len(files)


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

    # Collected, not fatal here: a deploy-set error must not hide the rest of the validation.
    deploy_allowed, deploy_files = check_deploy_set(errors)

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
    # The 404 page is served for every unknown path, so its links, navigation and EN/TR keys are
    # held to the same standard as a route's, without the canonical/sitemap duties.
    aux_html: dict[str, str] = {}
    aux_parsers: dict[str, SiteParser] = {}
    for name, rel in AUX_PAGES.items():
        aux_html[name] = (ROOT / rel).read_text(encoding="utf-8")
        aux_parsers[name] = SiteParser()
        aux_parsers[name].feed(aux_html[name])

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

    # Social-preview truthfulness, every route (MER-237): the og:image is a deployed, self-hosted
    # image that some page actually shows. Until MER-237 four routes still advertised the retired
    # Crater Lake scene, which no page places any more.
    placed_assets: set[str] = set()
    for text in route_html.values():
        placed_assets |= {m.group(1) for m in _ASSET_REF.finditer(re.sub(r"<meta\b[^>]*>", "", text))}
    for route, text in route_html.items():
        label = ROUTES[route]
        og_image = re.search(r'property="og:image" content="https://orbgss\.com/(assets/[^"]+)"', text)
        if not og_image:
            fail(f"{label}: og:image is missing or is not a self-hosted https://orbgss.com/assets/ image",
                 errors)
            continue
        target = og_image.group(1)
        if not (ROOT / target).is_file():
            fail(f"{label}: og:image {target} does not exist", errors)
        elif target.split("/", 1)[0] not in deploy_allowed:
            fail(f"{label}: og:image {target} is not deployed", errors)
        elif target not in placed_assets:
            fail(f"{label}: og:image {target} is not an image any page shows (retired or unused imagery)",
                 errors)

    # Internal links: every root-relative href must resolve to a real canonical route, and any
    # #fragment it carries must resolve to a real id — on the target page for a "/route/#frag"
    # link, or on the current page for a bare "#frag" link.
    for route, route_parser in list(route_parsers.items()) + list(aux_parsers.items()):
        label = ROUTES.get(route) or AUX_PAGES[route]
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
    for route_parser in list(route_parsers.values()) + list(aux_parsers.values()):
        all_i18n_keys |= route_parser.i18n_keys
    for key in sorted(all_i18n_keys):
        for lang in ("en", "tr"):
            if dictionary_value(lang, key) is None:
                fail(f"i18n key {key!r} is missing from the {lang!r} dictionary", errors)

    # ------------------------------------------------------------------
    # WEB-005C / MER-149: one public domain taxonomy across the whole site. A visitor must not meet
    # Geothermal / Mining / Marine on the homepage and a different set of top-level domain names in
    # the navigation or on /solutions/.
    # ------------------------------------------------------------------
    submenu_re = re.compile(r'<div class="submenu"[^>]*>(.*?)</div>', re.S)
    item_re = re.compile(r'<a href="(/solutions/[^"]*)" data-i18n="([^"]+)"(?: aria-current="page")?>([^<]+)</a>')
    for route, text in list(route_html.items()) + list(aux_html.items()):
        label = ROUTES.get(route) or AUX_PAGES[route]
        menu = submenu_re.search(text)
        if not menu:
            fail(f"{label}: no Solutions submenu; the public domain taxonomy is not published", errors)
            continue
        got = item_re.findall(menu.group(1))
        want = [(NAV_TARGETS[anchor], key, en) for anchor, key, en, _ in PUBLIC_TAXONOMY]
        if got != want:
            fail(f"{label}: Solutions submenu is not the canonical taxonomy in order; "
                 f"expected {want}, found {got}", errors)

    # The names themselves, in both languages, exactly as Product publishes them.
    for _, key, en_name, tr_name in PUBLIC_TAXONOMY:
        for lang, want_name in (("en", en_name), ("tr", tr_name)):
            got_name = dictionary_value(lang, key)
            if got_name != want_name:
                fail(f"{key!r} in the {lang!r} dictionary is {got_name!r}, not the canonical "
                     f"public domain name {want_name!r}", errors)

    # /solutions/ publishes a band per domain, and keeps the superseded anchors resolvable.
    solutions_ids = route_parsers.get("solutions", SiteParser()).ids
    for anchor_id, _, en_name, _ in PUBLIC_TAXONOMY:
        if anchor_id not in solutions_ids:
            fail(f"solutions/index.html: no #{anchor_id} band for the {en_name!r} domain", errors)
    for legacy in LEGACY_DOMAIN_ANCHORS:
        if legacy not in solutions_ids:
            fail(f"solutions/index.html: legacy anchor #{legacy} no longer resolves; existing deep "
                 f"links to it would break (WEB-005C keeps it as an alias on the renamed row)", errors)

    # No surface may still publish a superseded domain label -- not visible route copy, not the
    # EN/TR dictionary, not a translated aria-label or meta description.
    for route, text in route_html.items():
        for retired in RETIRED_DOMAIN_LABELS:
            if retired in text:
                fail(f"{ROUTES[route]}: publishes the superseded domain label {retired!r}; the public "
                     f"taxonomy is Geothermal / Mining / Marine", errors)
    for lang in ("en", "tr"):
        for retired in RETIRED_DOMAIN_LABELS:
            if retired in lang_blocks.get(lang, ""):
                fail(f"the {lang!r} dictionary still carries the superseded domain label "
                     f"{retired!r}; the public taxonomy is Geothermal / Mining / Marine", errors)

    # WEB-005C R2: every homepage Solutions card navigates to its domain's home (NAV_TARGETS), as a
    # native link (no JavaScript), named by its own title (no whole-card read-aloud, no untranslated
    # label).
    card_re = re.compile(r'<li class="domain-card[^"]*" id="([^"]+)"(.*?)</li>', re.S)
    cards = {m.group(1): m.group(2) for m in card_re.finditer(html)}
    for anchor_id, _, en_name, _ in PUBLIC_TAXONOMY:
        body = cards.get(anchor_id)
        if body is None:
            fail(f"index.html: no Solutions card for the {en_name!r} domain", errors)
            continue
        link = re.search(r'<a class="domain-link" href="([^"]+)" aria-labelledby="([^"]+)">', body)
        if not link:
            fail(f"index.html: the {en_name!r} card is not a native link to its domain's home "
                 f"(WEB-005C R2: the card itself is the link, and it must work without JavaScript)",
                 errors)
            continue
        want_href = NAV_TARGETS[anchor_id]
        if link.group(1) != want_href:
            fail(f"index.html: the {en_name!r} card links to {link.group(1)!r}, not {want_href!r}", errors)
        labelled_by = link.group(2)
        if not re.search(r'<h3 id="%s"' % re.escape(labelled_by), body):
            fail(f"index.html: the {en_name!r} card link is labelled by #{labelled_by}, which is not "
                 f"its own title; its accessible name would not be the domain name", errors)
    # The focus state has to exist and actually DRAW something, or the card is a mouse-only
    # control: a keyboard reader would tab onto it with nothing on screen to say where they are.
    focus_rules = re.findall(r"\.domain-link:focus-visible(?:::after)?\s*\{([^}]*)\}",
                             (ROOT / "styles.css").read_text(encoding="utf-8"))
    if not any(re.search(r"outline:\s*\d", rule) for rule in focus_rules):
        fail("styles.css declares no visible focus state for the Solutions card links "
             "(WEB-005C R2 requires one consistent with the design system)", errors)

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
    #             the recorded stops, bounded analytical opacity, lossless, and none of the
    #             transforms MER-151 section 4 withholds from the homepage profile.
    #   B-VIS-15  MER-151 presentation conformance: a derivative above the native grid is a single
    #             Lanczos3 RGBA enlargement inside 0.50-4.00x and 4800 px per axis; every display
    #             window and gamma sits inside its own numeric bound; priority carries neither.
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
        if not aoi:
            fail("web_005b.context has no recorded analysis-grid geometry (frame.aoi_in_frame)",
                 errors)
        # WEB-005B R14 removed the Act 2 AOI overlay: the copy column hid 72-100% of it at every
        # desktop width and no crop separates them. The rule is now conditional rather than deleted
        # -- if an overlay ever comes back it must still be drawn from the recorded fractions and
        # not from eyeballed ones, and it may not come back as bare markup with no geometry behind
        # it. The recorded geometry itself is still checked, below, against the inspection aid.
        mark = re.search(r"\.aoi-mark\{position:absolute;left:([\d.]+)%;right:([\d.]+)%;"
                         r"top:([\d.]+)%;bottom:([\d.]+)%", css_text)
        if mark and aoi:
            expect = (aoi["x0"] * 100, (1 - aoi["x1"]) * 100, aoi["y0"] * 100, (1 - aoi["y1"]) * 100)
            if any(abs(float(got) - want) > 0.001 for got, want in zip(mark.groups(), expect)):
                fail(f"Act 2 AOI corner marks {mark.groups()} do not match the recorded analysis-grid "
                     f"bounds {tuple(round(v, 4) for v in expect)}", errors)
        elif "aoi-mark" in home:
            fail("index.html draws an .aoi-mark overlay but styles.css no longer positions it from "
                 "the recorded analysis-grid fractions", errors)

        ana = w5b.get("analytical", {})
        layers = ana.get("layers", {})
        layer_widest: dict[str, int] = {}
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
            widest = 0
            for deriv in layer.get("derivatives", []):
                rel = web005b_file(label, deriv)
                if rel:
                    own.add(rel)
                width = deriv.get("width")
                if not isinstance(width, int) or width <= 0:
                    fail(f"{label}: {rel} records no usable width", errors)
                    continue
                widest = max(widest, width)
                scale = width / WEB005B_NATIVE_PX
                lo, hi = WEB005B_PRESENTATION_SCALE
                if width > WEB005B_PRESENTATION_CEILING_PX:
                    fail(f"{label}: {rel} is {width} px, above the MER-151 "
                         f"{WEB005B_PRESENTATION_CEILING_PX} px per-axis ceiling", errors)
                if not lo <= scale <= hi:
                    fail(f"{label}: {rel} is a {scale:.2f}x resize, outside the MER-151 "
                         f"{lo}-{hi} per-axis bound", errors)
                if width > WEB005B_NATIVE_PX and "Lanczos3" not in str(deriv.get("resize", "")):
                    fail(f"{label}: {rel} is above the native {WEB005B_NATIVE_PX} px grid without "
                         f"recording the single final RGBA Lanczos3 enlargement MER-151 requires "
                         f"— an enlarged governed raster is only a presentation derivative when it "
                         f"was made that one way", errors)
                if "lossless" not in str(deriv.get("format", "")):
                    fail(f"{label}: {rel} is not a lossless encode", errors)
            layer_widest[key] = widest or WEB005B_NATIVE_PX

            # ---- MER-151 bounded transfer (B-VIS-15) ---------------------------------------
            win, gam = layer.get("display_window"), layer.get("gamma")
            if win is None or gam is None:
                fail(f"{label}: records no MER-151 display-window / gamma decision; 'disabled' is a "
                     f"decision and has to be stated", errors)
            if key == "priority" and win != "disabled":
                fail(f"{label}: priority carries a display window — percentile/window clipping is "
                     f"prohibited on the fixed 0-100 score (MER-151 section 3)", errors)
            if isinstance(win, dict):
                b = WEB005B_WINDOW_BOUNDS
                if win.get("kind") == "quantile":
                    q_low, q_high = win.get("q_low"), win.get("q_high")
                    ok = (isinstance(q_low, (int, float)) and isinstance(q_high, (int, float))
                          and b["q_low"][0] <= q_low <= b["q_low"][1]
                          and b["q_high"][0] <= q_high <= b["q_high"][1]
                          and q_high - q_low >= b["min_span"])
                    if not ok:
                        fail(f"{label}: display window {q_low}/{q_high} is outside the MER-151 "
                             f"quantile bounds or below the {b['min_span']} span floor", errors)
                elif win.get("kind") == "symmetric_abs_quantile":
                    q_abs, m = win.get("q_abs"), win.get("resolved_M")
                    if not (isinstance(q_abs, (int, float)) and b["q_abs"][0] <= q_abs <= b["q_abs"][1]):
                        fail(f"{label}: q_abs {q_abs} is outside the MER-151 {b['q_abs']} bound", errors)
                    if not (isinstance(m, (int, float)) and m >= b["min_M"]):
                        fail(f"{label}: resolved M {m} is below the mandatory {b['min_M']} floor", errors)
                    if win.get("center") != 0.0 or win.get("independent_signed_windows") is not False:
                        fail(f"{label}: the THM-01 window must keep the scientific centre at exactly "
                             f"0 and may not window the two signs independently", errors)
                else:
                    fail(f"{label}: unknown display-window kind {win.get('kind')!r}", errors)
            if isinstance(gam, dict):
                g, (glo, ghi) = gam.get("gamma"), WEB005B_GAMMA_BOUNDS[key]
                if not (isinstance(g, (int, float)) and glo <= g <= ghi):
                    fail(f"{label}: gamma {g} is outside the MER-151 {glo}-{ghi} bound for {key}", errors)
                if gam.get("adaptive") is not False:
                    fail(f"{label}: gamma must be one fixed value per layer family, never local or "
                         f"adaptive", errors)
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
                    if int(entry.get("width", 0)) > layer_widest.get(layer_key, WEB005B_NATIVE_PX):
                        fail(f"{label}: wider than any lossless derivative of this layer — a "
                             f"delivery encode re-encodes a rendered file, it never adds pixels", errors)
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
                     f"at {dpr}x, above the {native} px it publishes", errors)
            elif key in layer_widest and native > layer_widest[key]:
                fail(f"web_005b asset {key!r} claims {native} px of published density but its widest "
                     f"derivative is {layer_widest[key]} px", errors)
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
    # MER-240: the same scenes are the full-size bands of the /solutions/ hub, declared by a second
    # placement record (web_m6_placement) held to the same pixel bound.
    # ------------------------------------------------------------------
    for scene in scenes:
        own = {str(d.get("path", "")) for d in scene.get("derivatives", [])}
        shown_on = [r for r, rp in route_parsers.items() if all_srcs(rp) & own]
        placement = scene.get("web_005b_placement")
        m6_placement = scene.get("web_m6_placement") or {}
        sid = scene.get("id", "<unknown>")
        if not shown_on:
            if placement and placement.get("status") == "placed":
                fail(f"scene {sid!r} claims a WEB-005B placement but appears on no route", errors)
            if m6_placement.get("status") == "placed":
                fail(f"scene {sid!r} claims a MER-240 placement but appears on no route", errors)
            continue
        if not placement:
            continue  # a scene placed by an earlier task keeps that task's contract
        m6_routes = [str(r) for r in m6_placement.get("routes", [])]
        stray = [r for r in shown_on if r != "" and ROUTES[r] not in m6_routes]
        if stray:
            fail(f"scene {sid!r} is placed for the homepage and {m6_routes or 'no other route'} but "
                 f"also appears on {[ROUTES[r] for r in stray]}", errors)
        for route in shown_on:
            if route and m6_placement.get("status") != "placed":
                fail(f"scene {sid!r} appears on {ROUTES[route]} without a placed web_m6_placement",
                     errors)
        if m6_placement:
            m6_rendered = m6_placement.get("rendered", {})
            for field in ("max_css_width", "device_pixel_ratio_considered", "widest_candidate_px",
                          "selected_derivative"):
                if m6_rendered.get(field) in (None, ""):
                    fail(f"scene {sid!r} web_m6_placement.rendered missing {field}", errors)
            m_css, m_dpr = m6_rendered.get("max_css_width"), m6_rendered.get("device_pixel_ratio_considered")
            m_widest = m6_rendered.get("widest_candidate_px")
            if all(isinstance(v, (int, float)) for v in (m_css, m_dpr, m_widest)) and m_css * m_dpr > m_widest:
                fail(f"scene {sid!r} is laid out on the hub at {m_css} CSS px = {int(m_css * m_dpr)} "
                     f"device px at {m_dpr}x, above its widest {m_widest} px candidate", errors)
            if str(m6_rendered.get("selected_derivative", "")) not in own:
                fail(f"scene {sid!r} web_m6_placement names a selected derivative that is not its own",
                     errors)
            widths = {int(d.get("width_px", 0)) for d in scene.get("derivatives", [])}
            if isinstance(m_widest, int) and m_widest not in widths:
                fail(f"scene {sid!r} web_m6_placement claims a {m_widest} px candidate it does not ship",
                     errors)
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
        # kind of drift the imagery policy exists to stop. WEB-005B R14 removed the per-card
        # location/coordinate/kind captions at Product's instruction, which makes the section
        # footnote the SOLE carrier of that framing — so it is checked harder than the captions
        # were: it must be rendered on the page, it must be in both dictionaries, and it must still
        # say the three things that make it work.
        for key in placement.get("visible_framing_i18n_keys", []):
            for route in shown_on:
                if key not in route_parsers[route].i18n_keys:
                    fail(f"scene {sid!r} is shown on {ROUTES[route]} but its framing key {key!r} is "
                         f"not rendered there", errors)
        for lang in ("en", "tr"):
            note = dictionary_value(lang, "domains.illustrative")
            if note is None:
                fail(f"the domain photography footnote is missing from the {lang!r} dictionary",
                     errors)
                continue
            for term in DOMAIN_FOOTNOTE_TERMS[lang]:
                if term not in note:
                    fail(f"the {lang!r} domain photography footnote lost required wording "
                         f"{term!r}; it is the only thing left telling a reader these photographs "
                         f"are not OrbGSS results from the pilot area", errors)

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
        # MER-216 delivery ladder. Every tier is a recorded, hash-named file; the markup's ladder
        # (data-hero-tiers, read by script.js) must be exactly the recorded tiers, in both codecs;
        # the bare data-hero-webm / data-hero-mp4 pair is the 1920 tier; assets are immutable-cached,
        # so a file name that does not carry its own SHA-256 prefix could be served stale; and an MP4
        # must be faststart (moov before mdat) or a browser needs a second range request to start.
        try:
            ladder = json.loads(parser.hero_tiers) if parser.hero_tiers else []
        except ValueError:
            ladder = None
        if ladder is None or not ladder:
            fail("the hero <video> must declare its delivery ladder as valid JSON in data-hero-tiers", errors)
        else:
            by_tier = {}
            for m in hero_media:
                role = str(m.get("role", ""))
                if role.startswith(("hero-webm-", "hero-mp4-")):
                    by_tier.setdefault(role.rsplit("-", 1)[1], {})[role.split("-")[1]] = m
                    stem = pathlib.PurePosixPath(str(m.get("path", ""))).name
                    if not re.fullmatch(r"orbgss-hero-\d+-" + str(m.get("sha256", ""))[:8] + r"\.(webm|mp4)", stem):
                        fail(f"{stem}: an immutable-cached hero encode must be named orbgss-hero-<width>-<first 8 hex of its SHA-256>", errors)
                    if m.get("width") * 9 != m.get("height") * 16:
                        fail(f"{stem}: hero encodes must be 16:9", errors)
                    if role.startswith("hero-mp4-") and (ROOT / str(m.get("path", ""))).exists():
                        head = (ROOT / str(m["path"])).read_bytes()[:64 * 1024]
                        if b"moov" not in head:
                            fail(f"{stem}: the MP4 is not faststart (no moov atom in the first 64 KiB)", errors)
            if set(by_tier) != set(HERO_TIER_WIDTHS):
                fail(f"web_005.hero_media must record the tiers {sorted(HERO_TIER_WIDTHS)} in WebM and MP4; found {sorted(by_tier)}", errors)
            widths = [t.get("w") for t in ladder]
            if widths != sorted(widths) or len(set(widths)) != len(widths):
                fail("data-hero-tiers must be ordered by ascending width, one entry per tier", errors)
            for t in ladder:
                rec = by_tier.get(str(t.get("id")))
                if not rec or set(rec) != {"webm", "mp4"}:
                    fail(f"data-hero-tiers entry {t.get('id')!r} has no matching WebM and MP4 record", errors)
                    continue
                for codec in ("webm", "mp4"):
                    if str(t.get(codec, "")).lstrip("/") != rec[codec].get("path") or t.get("w") != rec[codec].get("width"):
                        fail(f"data-hero-tiers {t.get('id')!r} {codec} does not match web_005.hero_media", errors)
                    if (t.get("codecs") or {}).get(codec) != rec[codec].get("codec_string"):
                        fail(f"data-hero-tiers {t.get('id')!r} {codec} codec string differs from the recorded encode", errors)
                    if not isinstance((t.get("kbps") or {}).get(codec), int) or t["kbps"][codec] <= 0:
                        fail(f"data-hero-tiers {t.get('id')!r} needs an integer kbps for {codec}", errors)
            md = by_tier.get("md", {})
            if md and (parser.hero_media.get("data-hero-webm", "").lstrip("/") != md.get("webm", {}).get("path")
                       or parser.hero_media.get("data-hero-mp4", "").lstrip("/") != md.get("mp4", {}).get("path")):
                fail("data-hero-webm / data-hero-mp4 must be the 1920 (md) tier, the fallback when the ladder is unreadable", errors)
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

    # MER-216 runtime contract. The hero chooses ONE tier and codec before requesting any video byte
    # (ladder + downlink hint + decoder capability), shows the video only after it has presented a
    # real frame, never swaps a source mid-play, and ends in the held still when playback stalls or
    # drops frames.
    for token, why in (
        ("data-hero-tiers", "read the delivery ladder"),
        ("mediaCapabilities", "ask the decoder whether the chosen tier plays smoothly"),
        ("connection.downlink", "weigh the network's downlink hint before choosing a tier"),
        ("requestVideoFrameCallback", "show the video only after it has presented a real frame"),
        ("settleStatic('buffering')", "end in the held still when playback stalls"),
        ("settleStatic('dropped-frames')", "end in the held still when the decoder drops frames"),
        ("settleStatic('no-video-frame')", "never show a video that has painted no frame"),
    ):
        if token not in script_hero:
            fail(f"script.js must {why} ({token!r} is missing)", errors)
    # Review revision: a codec may only be returned once it has passed BOTH the network margin and the
    # decoder verdict, in the same candidate loop (a codec must never be returned straight from a
    # failed capability query for another one).
    if not re.search(r"networkOk\(candidate\.tier, candidate\.codec\)[\s\S]{0,400}decoderAccepts\(candidate, deadline\)", script_hero):
        fail("script.js pickDelivery must gate every candidate on networkOk and then decoderAccepts before it can be returned", errors)
    if "function decoderAccepts" not in script_hero or script_hero.count("src: candidate.tier[candidate.codec]") != 1:
        fail("script.js must build a delivery only from a candidate that passed the gates (exactly one place)", errors)
    if script_hero.count("setAttribute('src'") != 1:
        fail("script.js must attach a hero video source in exactly one place: a tier is chosen once, "
             "before playback, and never swapped mid-play", errors)

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

    # sitemap.xml lists every canonical public route, with a date, and nothing else: a retired
    # route is a redirect now and has no place in it (MER-240).
    sitemap_path = ROOT / "sitemap.xml"
    if sitemap_path.exists():
        sitemap_text = sitemap_path.read_text(encoding="utf-8")
        listed = re.findall(r"<url><loc>([^<]+)</loc><lastmod>(\d{4}-\d{2}-\d{2})</lastmod></url>", sitemap_text)
        listed_urls = [url for url, _ in listed]
        want_urls = [canonical_url(route) for route in ROUTES]
        for url in want_urls:
            if url not in listed_urls:
                fail(f"sitemap.xml is missing {url!r} (or its <lastmod>)", errors)
        for url in listed_urls:
            if url not in want_urls:
                fail(f"sitemap.xml lists {url!r}, which is not a canonical route", errors)
        if sitemap_text.count("<loc>") != len(listed):
            fail("sitemap.xml has an entry without a <lastmod> date", errors)

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

    # ------------------------------------------------------------------
    # MER-240 / Milestone 6 (docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md). The page set is Home,
    # Solutions, Geothermal, About and Partner with us; the retired routes redirect; and the
    # reworked routes are held to the content rules R1-R5 and R8.
    # ------------------------------------------------------------------
    m6_pages = dict(route_html)
    m6_pages.update(aux_html)
    m6_label = lambda name: ROUTES.get(name) or AUX_PAGES[name]  # noqa: E731
    doms = {name: build_dom(text) for name, text in m6_pages.items()}

    def first(node: DomNode, pred) -> DomNode | None:
        found = node.find_all(pred)
        return found[0] if found else None

    def tr_words(node: DomNode, skip) -> int:
        """Word count of a block as the Turkish dictionary renders it."""
        total = 0

        def walk(n: DomNode) -> None:
            nonlocal total
            for child in n.children:
                if isinstance(child, str):
                    total += count_words(child)
                    continue
                if skip(child) or child.attrs.get("aria-hidden") == "true":
                    continue
                key = child.attrs.get("data-i18n")
                if key:
                    value = dictionary_value("tr", str(key))
                    total += count_words(value or "")
                else:
                    walk(child)

        key = node.attrs.get("data-i18n")
        if key:
            return count_words(dictionary_value("tr", str(key)) or "")
        walk(node)
        return total

    def is_fixed(n: DomNode) -> bool:
        return bool(n.classes & M6_FIXED_CLASSES)

    def first_content(node: DomNode):
        """The first thing a reader meets in a section after its heading block."""
        for child in node.children:
            if isinstance(child, str):
                if child.strip():
                    return ("text", None)
                continue
            if child.classes & {"page-section-head", "anchor-alias"} or child.tag in ("h1", "h2", "h3"):
                continue
            if "data-lead-visual" in child.attrs:
                return ("lead", child)
            if child.tag in ("p", "ul", "ol", "dl", "blockquote", "table", "a", "figure", "img"):
                return ("text", child)
            inner = first_content(child)
            if inner is not None:
                return inner
        return None

    # Navigation: the same four entries and the Solutions menu on every page, in order, with the
    # current page marked; the footer lists the same pages.
    for name, dom in doms.items():
        label = m6_label(name)
        nav_list = first(dom, lambda n: n.tag == "ul" and "nav-list" in n.classes)
        if nav_list is None:
            fail(f"{label}: no primary navigation list", errors)
            continue
        items = [c for c in nav_list.children if isinstance(c, DomNode) and c.tag == "li"]
        got = []
        current = set()
        for li in items:
            link = next((c for c in li.children if isinstance(c, DomNode) and c.tag == "a"), None)
            trigger = first(li, lambda n: n.tag == "button" and "nav-trigger" in n.classes)
            if link is not None:
                key = link.attrs.get("data-i18n")
                got.append((link.attrs.get("href"), key))
                if link.attrs.get("aria-current") == "page":
                    current.add(str(link.attrs.get("href")))
            elif trigger is not None:
                span = first(trigger, lambda n: n.attrs.get("data-i18n"))
                got.append((None, span.attrs.get("data-i18n") if span else None))
                if trigger.attrs.get("aria-current") == "page":
                    current.add("menu")
        if got != PRIMARY_NAV:
            fail(f"{label}: primary navigation is {got}, not {PRIMARY_NAV} (Home, Solutions, About, "
                 f"Partner with us)", errors)
        for sub_link in first(nav_list, lambda n: "submenu" in n.classes).find_all(lambda n: n.tag == "a") \
                if first(nav_list, lambda n: "submenu" in n.classes) else []:
            if sub_link.attrs.get("aria-current") == "page":
                current.add(str(sub_link.attrs.get("href")))
        if current != NAV_CURRENT.get(name, set()):
            fail(f"{label}: navigation marks {sorted(current)} as the current page, expected "
                 f"{sorted(NAV_CURRENT.get(name, set()))}", errors)
        footer = first(dom, lambda n: n.tag == "footer")
        footer_nav = first(footer, lambda n: n.tag == "nav") if footer else None
        got_footer = [(a.attrs.get("href"), a.attrs.get("data-i18n"))
                      for a in footer_nav.find_all(lambda n: n.tag == "a")] if footer_nav else []
        if got_footer != FOOTER_NAV:
            fail(f"{label}: footer navigation is {got_footer}, not {FOOTER_NAV}", errors)
        sources_link = first(footer, lambda n: n.tag == "a" and n.attrs.get("href") == "/about/#sources") \
            if footer else None
        if sources_link is None or sources_link.attrs.get("data-i18n") != "footer.sources":
            fail(f"{label}: the footer attribution does not end with the link to /about/#sources", errors)
    for key, (en_label, tr_label) in NAV_LABELS.items():
        for lang, want in (("en", en_label), ("tr", tr_label)):
            if dictionary_value(lang, key) != want:
                fail(f"{key!r} in the {lang!r} dictionary is {dictionary_value(lang, key)!r}, not "
                     f"{want!r}", errors)

    # Section 6: the retired routes are permanent redirects, their files are gone, and nothing
    # still links to them.
    try:
        vercel = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        vercel = {}
        fail(f"vercel.json could not be read: {exc}", errors)
    got_redirects = {}
    for rule in vercel.get("redirects", []):
        source, dest = str(rule.get("source", "")), str(rule.get("destination", ""))
        if source in got_redirects:
            fail(f"vercel.json redirects {source!r} twice", errors)
        got_redirects[source] = dest
        if rule.get("statusCode") != REDIRECT_STATUS or "permanent" in rule:
            fail(f"vercel.json redirect {source!r} must carry statusCode {REDIRECT_STATUS} "
                 f"(a 301, as the authority sets; 'permanent' would answer 308)", errors)
    if got_redirects != REDIRECTS:
        fail(f"vercel.json redirects are {got_redirects}, not {REDIRECTS}", errors)
    for source in REDIRECTS:
        old = source.strip("/")
        if (ROOT / old).exists():
            fail(f"{old}/ still exists; a redirected route must not also be served", errors)
        if old in deploy_allowed:
            fail(f".vercelignore still deploys the retired route {old}/", errors)
    for source, dest in got_redirects.items():
        if dest.strip("/") not in ROUTES:
            fail(f"redirect {source!r} points at {dest!r}, which is not a canonical route", errors)

    # Section 6: the Geothermal page carries the ids old /pilot/ links land on.
    geo_ids = route_parsers.get("solutions/geothermal", SiteParser()).ids
    for anchor in GEOTHERMAL_ANCHORS:
        if anchor not in geo_ids:
            fail(f"solutions/geothermal/index.html: no #{anchor}; links to /pilot/#{anchor} or the "
                 f"page's own sections would land at the top", errors)

    # Section 6: an alias must also land. .anchor-alias is position:absolute at its container's
    # origin; in a container that styles.css leaves static it resolves against the page, and every
    # /pilot/#pilot-* link then scrolls to the top instead of its section (MER-240 review, B1). A
    # static check cannot scroll, so it requires the next best thing: the alias's own parent is
    # positioned by an unconditional rule. tasks/MER-240_EVIDENCE.md records the browser check.
    positioned = positioned_css_classes(css_text)
    for name, dom in doms.items():
        for alias in dom.find_all(lambda n: "anchor-alias" in n.classes):
            holder = alias.parent
            if holder is None or not (holder.classes & positioned):
                where = f"<{holder.tag} class=\"{' '.join(sorted(holder.classes))}\">" if holder else "the page"
                fail(f"{m6_label(name)}: #{alias.attrs.get('id')} sits in {where}, which styles.css "
                     f"does not position; the absolutely positioned .anchor-alias would resolve "
                     f"against the page and its link would land at the top", errors)

    # Section 4.1: the homepage changes.
    for retired_id in sorted(RETIRED_HOMEPAGE_SECTION_IDS & parser.ids):
        fail(f"index.html: #{retired_id} is back; Method and Company content lives on /about/", errors)
    if "mailto:" in html:
        fail("index.html carries a mailto: link; the homepage's Partner calls point to /partner/", errors)
    home_dom = doms[""]
    contact = first(home_dom, lambda n: n.attrs.get("id") == "contact")
    contact_links = contact.find_all(lambda n: n.tag == "a") if contact else []
    if not contact or [a.attrs.get("href") for a in contact_links] != ["/partner/"] \
            or count_words(contact.text()) > M6_BUDGET["headline"]:
        fail("index.html: #contact must be the one Partner line, a single link to /partner/", errors)
    for key, href in (("act.evidence.deeper", "/solutions/geothermal/#layers"),
                      ("act.priority.deeper", "/solutions/geothermal/")):
        span = first(home_dom, lambda n, k=key: n.attrs.get("data-i18n") == k)
        link = next((a for a in span.ancestors() if a.tag == "a"), None) if span else None
        if link is None or link.attrs.get("href") != href:
            fail(f"index.html: the {key!r} link must point to {href}", errors)
    for card in home_dom.find_all(lambda n: n.tag == "li" and "domain-card" in n.classes):
        copy = first(card, lambda n: "domain-copy" in n.classes)
        extra = [c for c in (copy.children if copy else []) if isinstance(c, DomNode)
                 and c.tag not in ("h3",) and "domain-status" not in c.classes]
        if extra:
            fail(f"index.html: the {card.attrs.get('id')!r} card carries more than its name and status "
                 f"(its description lives on /solutions/, rule R1)", errors)

    # R8: one status vocabulary. Every status label is one of the three shared keys, worded as
    # pinned, and the retired "In development" wording is gone from pages and dictionary alike.
    for key, (en_value, tr_value) in M6_STATUS.items():
        for lang, want in (("en", en_value), ("tr", tr_value)):
            if dictionary_value(lang, key) != want:
                fail(f"R8: {key!r} in the {lang!r} dictionary is {dictionary_value(lang, key)!r}, "
                     f"not {want!r}", errors)
    for name, dom in doms.items():
        for status in dom.find_all(lambda n: "domain-status" in n.classes):
            if status.attrs.get("data-i18n") not in M6_STATUS:
                fail(f"R8: {m6_label(name)}: a status label uses {status.attrs.get('data-i18n')!r}, "
                     f"not one of {sorted(M6_STATUS)}", errors)
        for retired in RETIRED_STATUS_LABELS:
            if retired in m6_pages[name]:
                fail(f"R8: {m6_label(name)} still says {retired!r}; Mining and Marine are an "
                     f"expansion direction", errors)
    for lang in ("en", "tr"):
        for retired in RETIRED_STATUS_LABELS:
            if retired in lang_blocks.get(lang, ""):
                fail(f"R8: the {lang!r} dictionary still carries {retired!r}", errors)

    # The reworked routes (everything but the homepage, whose acts do not change).
    m6_routes = [name for name in m6_pages if name != ""]
    for name in m6_routes:
        label = m6_label(name)
        dom = doms[name]
        main = first(dom, lambda n: n.tag == "main")
        if main is None:
            fail(f"{label}: no <main>", errors)
            continue

        # R4: every content section opens with its lead visual. Only the page header may be text
        # alone, and outside sections <main> holds nothing but the closing link and the footnote.
        for block in [c for c in main.children if isinstance(c, DomNode)]:
            if block.tag == "section" and "page-hero" in block.classes:
                continue
            if block.tag == "div" and block.classes & M6_LOOSE_BLOCKS:
                if "page-closing" in block.classes and \
                        len(block.find_all(lambda n: n.tag == "a")) != 1:
                    fail(f"R4: {label}: the closing block holds more than one link", errors)
                if "page-note" in block.classes and not first(block, lambda n: "act-footnote" in n.classes):
                    fail(f"R4: {label}: a page note that is not the fixed footnote", errors)
                continue
            if block.tag != "section":
                fail(f"R4: {label}: <{block.tag} class={sorted(block.classes)}> sits in <main> outside "
                     f"a section", errors)
                continue
            found = first_content(block)
            section_name = block.attrs.get("id") or block.attrs.get("aria-labelledby") or block.tag
            if found is None or found[0] != "lead":
                what = f"<{found[1].tag}>" if found and found[1] is not None else "nothing"
                fail(f"R4: {label}: section {section_name!r} opens with {what}, not a marked lead "
                     f"visual (table, image, map, chart)", errors)
            elif found[1].tag not in LEAD_VISUAL_TAGS and not (found[1].classes & LEAD_VISUAL_CLASSES):
                fail(f"R4: {label}: section {section_name!r} marks <{found[1].tag}> as its lead visual",
                     errors)

        # R5: text budgets. Fixed texts (R6) and the lead visuals' own captions are exempt.
        budget_page = M6_PAGE_BUDGET.get(name, M6_BUDGET["page"])
        skip = lambda n: is_fixed(n) or n.tag in ("figcaption",)  # noqa: E731
        for heading in main.find_all(lambda n: n.tag in ("h1", "h2", "h3")):
            for lang, words, limit in (("en", count_words(heading.text(skip)), M6_BUDGET["headline"]),
                                       ("tr", tr_words(heading, skip), M6_BUDGET["headline"] * M6_TR_ALLOWANCE)):
                if words > limit:
                    fail(f"R5: {label}: headline {heading.text(skip)!r} is {words} words in {lang} "
                         f"(at most {limit:g})", errors)
        for intro in main.find_all(lambda n: "page-hero-copy" in n.classes):
            for lang, words, limit in (("en", count_words(intro.text(skip)), M6_BUDGET["intro"]),
                                       ("tr", tr_words(intro, skip), M6_BUDGET["intro"] * M6_TR_ALLOWANCE)):
                if words > limit:
                    fail(f"R5: {label}: the page intro is {words} words in {lang} (at most {limit:g})",
                         errors)
        for section in main.find_all(lambda n: n.tag == "section" and "page-hero" not in n.classes):
            body = [p_ for p_ in section.find_all(lambda n: n.tag == "p")
                    if not is_fixed(p_) and not any(is_fixed(a) or a.tag in ("table", "figure")
                                                     or "data-lead-visual" in a.attrs
                                                     for a in p_.ancestors())
                    and "data-lead-visual" not in p_.attrs]
            en_words = sum(count_words(p_.text(skip)) for p_ in body)
            tr_body = sum(tr_words(p_, skip) for p_ in body)
            if en_words > M6_BUDGET["section"] or tr_body > M6_BUDGET["section"] * M6_TR_ALLOWANCE:
                fail(f"R5: {label}: section {section.attrs.get('id') or section.attrs.get('aria-labelledby')!r} "
                     f"body is {en_words} words in en / {tr_body} in tr (at most "
                     f"{M6_BUDGET['section']})", errors)
        for table in main.find_all(lambda n: n.tag == "table"):
            rows = table.find_all(lambda n: n.tag == "tr" and n.parent is not None and n.parent.tag == "tbody")
            if len(rows) > M6_BUDGET["rows"]:
                fail(f"R5: {label}: a table has {len(rows)} rows (at most {M6_BUDGET['rows']})", errors)
            for cell in table.find_all(lambda n: n.tag in ("td", "th")):
                en_cell = count_words(cell.text(skip))
                tr_cell = tr_words(cell, skip)
                if en_cell > M6_BUDGET["cell"] or tr_cell > M6_BUDGET["cell"] * M6_TR_ALLOWANCE:
                    fail(f"R5: {label}: table cell {cell.text(skip)!r} is {en_cell} words in en / "
                         f"{tr_cell} in tr (at most {M6_BUDGET['cell']})", errors)
        page_en = count_words(main.text(skip))
        page_tr = tr_words(main, skip)
        if page_en > budget_page or page_tr > budget_page * M6_TR_ALLOWANCE:
            fail(f"R5: {label} carries {page_en} budgeted words in en / {page_tr} in tr (at most "
                 f"{budget_page})", errors)

        # R3: no software or development detail, in either language.
        page_keys = (route_parsers.get(name) or aux_parsers[name]).i18n_keys
        visible = (main.text() + " " + " ".join(
            dictionary_value(lang, k) or "" for k in page_keys if not k.startswith("mail.")
            for lang in ("en", "tr"))).lower()
        for term in M6_SOFTWARE_TERMS:
            if re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", visible):
                fail(f"R3: {label} mentions {term!r}; software and development detail stays off the "
                     f"public pages", errors)

    # R1: one home per fact. A sentence long enough to be a claim is stated on one route only;
    # fixed texts (R6) travel with their visuals and are exempt.
    claim_routes: dict[str, set[str]] = {}
    for name in route_html:
        main = first(doms[name], lambda n: n.tag == "main")
        if main is None:
            continue
        blocks = main.find_all(lambda n: n.tag in ("p", "li", "td", "th", "dd", "h1", "h2", "h3"))
        for block in blocks:
            if is_fixed(block) or any(is_fixed(a) for a in block.ancestors()):
                continue
            if any(c.tag in ("p", "li", "td", "th", "dd") for c in block.iter() if c is not block):
                continue
            for sentence in re.split(r"(?<=[.!?])\s+", block.text(lambda n: is_fixed(n))):
                normal = " ".join(sentence.lower().strip(" .!?").split())
                if count_words(normal) >= M6_CLAIM_MIN_WORDS:
                    claim_routes.setdefault(normal, set()).add(name)
    for sentence, where in sorted(claim_routes.items()):
        if len(where) > 1:
            fail(f"R1: {sentence!r} is stated on {sorted(ROUTES[r] for r in where)}; a fact has one "
                 f"home and is linked to from elsewhere", errors)

    # R2: one full-size appearance per visual. A homepage domain card is the accepted exception
    # (authority 4.2: the hub is the photographs' home and the cards link to the domains).
    visual_of: dict[str, str] = {}
    for scene in scenes:
        for deriv in scene.get("derivatives", []):
            visual_of[str(deriv.get("path", ""))] = f"scene:{scene.get('id')}"
        visual_of[str(scene.get("local_file", ""))] = f"scene:{scene.get('id')}"
    for layer_id, layer in manifest.get("web_005b", {}).get("analytical", {}).get("layers", {}).items():
        for deriv in layer.get("derivatives", []):
            visual_of[str(deriv.get("path", ""))] = f"web005b:{layer_id}"
    for asset in proof_assets:
        for deriv in asset.get("derivatives", []):
            visual_of[str(deriv.get("path", ""))] = f"proof:{asset.get('id')}"
    for asset in manifest.get("geo_web_002", {}).get("assets", []):
        for deriv in asset.get("derivatives", []):
            visual_of[str(deriv.get("path", ""))] = f"geo:{asset.get('id')}"
    locator = manifest.get("web_m6", {}).get("locator_map", {})
    if locator.get("path"):
        visual_of[str(locator["path"])] = "map:locator"
    full_size: dict[str, set[str]] = {}
    for name in route_html:
        for img in doms[name].find_all(lambda n: n.tag == "img"):
            if any("domain-card" in a.classes for a in img.ancestors()):
                continue
            candidates = [str(img.attrs.get("src") or img.attrs.get("data-src") or "")]
            candidates += [c.strip().split()[0] for c in str(img.attrs.get("srcset") or "").split(",") if c.strip()]
            ids = {visual_of.get(c.lstrip("/")) for c in candidates} - {None}
            is_thumb = "thumb" in img.classes and str(img.attrs.get("width", "")).isdigit() \
                and int(img.attrs["width"]) <= THUMB_MAX_CSS_PX
            for vid in ids:
                if not is_thumb:
                    full_size.setdefault(vid, set()).add(name)
    for vid, where in sorted(full_size.items()):
        if len(where) > 1:
            fail(f"R2: {vid} appears at full size on {sorted(ROUTES[r] for r in where)}; elsewhere a "
                 f"visual may only be a thumbnail of at most {THUMB_MAX_CSS_PX} CSS px", errors)

    # V1: the locator map is recorded, checksummed, deployed and shown with its caption.
    if not locator:
        fail("sources.json has no web_m6.locator_map record for the Geothermal locator map", errors)
    else:
        lpath = ROOT / str(locator.get("path", ""))
        for field in ("path", "sha256", "bytes", "source", "source_sha256", "license", "generator",
                      "asset_class"):
            if not locator.get(field):
                fail(f"web_m6.locator_map is missing {field}", errors)
        if not lpath.is_file():
            fail(f"the locator map {locator.get('path')} does not exist", errors)
        else:
            if sha256_of(lpath) != locator.get("sha256"):
                fail("the locator map does not match its recorded SHA-256", errors)
            if lpath.stat().st_size != locator.get("bytes"):
                fail("the locator map does not match its recorded byte size", errors)
            if locator.get("sha256", "")[:8] not in lpath.name:
                fail("the locator map is not content-hash named (/assets/ is immutable-cached)", errors)
        geo_dom = doms.get("solutions/geothermal")
        shown = geo_dom.find_all(lambda n: n.tag == "img" and str(n.attrs.get("src", "")).lstrip("/")
                                 == str(locator.get("path"))) if geo_dom else []
        if len(shown) != 1:
            fail("the Geothermal page must show the recorded locator map exactly once", errors)
        else:
            fig = next((a for a in shown[0].ancestors() if a.tag == "figure"), None)
            caption = first(fig, lambda n: n.tag == "figcaption" and "scene-label" in n.classes) if fig else None
            spans = [c for c in caption.children if isinstance(c, DomNode)] if caption else []
            if len(spans) != 3 or "scene-kind" not in spans[-1].classes:
                fail("the locator map must carry the bottom-right caption: place, coordinates, kind",
                     errors)
        for name in route_html:
            if name != "solutions/geothermal" and locator.get("path", "") in route_html[name]:
                fail(f"the locator map appears on {ROUTES[name]}; its home is the Geothermal page", errors)

    # Partner with us: three conversations, one table, each a mailto with its own subject; the
    # address set large. The page is the one home of the conversation types and the address.
    partner_dom = doms.get("partner")
    if partner_dom is not None:
        table = first(partner_dom, lambda n: n.tag == "table")
        mails = [a.attrs.get("data-i18n-href") for a in table.find_all(
            lambda n: n.tag == "a" and str(n.attrs.get("href", "")).startswith("mailto:"))] if table else []
        if mails != ["mail.pilot", "mail.partner", "mail.technical"]:
            fail(f"partner/index.html: the conversation table's mail links are {mails}", errors)
        if not first(partner_dom, lambda n: "mail-address" in n.classes):
            fail("partner/index.html: no address block", errors)
    for name in route_html:
        if name != "partner" and "mailto:" in route_html[name]:
            fail(f"{ROUTES[name]} carries a mailto: link; conversations start on /partner/ (R1)", errors)

    print("OrbGSS site validation")
    print(f"  scenes: {len(scenes)}")
    print(f"  html images: {len(parser.img_srcs)}")
    print(f"  routes: {len(route_parsers)}")
    print(f"  i18n keys referenced site-wide: {len(all_i18n_keys)}")
    print(f"  geo-web-002 package assets: {len(package.get('assets', []))} "
          f"({len(package_paths)} files)")
    print(f"  deploy set: {len(deploy_allowed)} root entries, {deploy_files} files")
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
