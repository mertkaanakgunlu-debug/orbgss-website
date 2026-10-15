# OrbGSS website — design authority

> **WEB-001 (2026-09-15):** `docs/WEB_VNEXT_AUTHORITY.md` is the vNext authority. Where this document and that one disagree (navigation order, homepage sequence, beam contents, monospace treatment), the vNext document wins. Everything below that is not restated there still applies.

> **MER-239 (2026-10-15):** the WEB-001 structural rhythm below is superseded by the four-act homepage (WEB-005; `CLAUDE.md` design invariants) and kept as history. Navigation and Solutions labels follow `CLAUDE.md` (live) and `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md` (approved Milestone 6 target). Everything else here stays in force where `CLAUDE.md` does not say otherwise.

## Accepted direction

The desired site is a cinematic, minimal Earth-observation landing page. Think of the page as alternating horizontal layers rather than a conventional SaaS homepage.

### Structural rhythm (WEB-001 — superseded by the WEB-005 four-act homepage; history)

```text
[ NAVIGATION: OrbGSS ........ Platform  Solutions⌄  Pilot  Company  Contact | EN | TR ]

[ HERO: full-width imagery (static poster until WEB-005) + hero copy   location / coords ↘ ]

[ DARK TECHNICAL BEAM: 01 OBSERVE   statement (1–2 sentences)   MONO DESCRIPTOR ]
[ CLEAN FULL-WIDTH VISUAL PANEL — no overlay copy               location / coords ↘ ]

[ 02 TERRAIN → 03 EVIDENCE → 04 STRUCTURE → 05 PRIORITY → 06 GEOTHERMAL, same rhythm ]

[ PILOT LEDGER: geothermal active; mineral / environmental expansion directions ]
[ COMPANY + HOW WE WORK (trust list) ]
[ CONTACT BEAM ]
[ compact footer ]
```

This alternating beam/image rhythm is the core design system. Images sit directly against the beams; there is no metadata band between them (changed in ORBWEB-001.1). Since WEB-001 the sequence tells the evidence-to-intelligence story rather than listing solutions; see `docs/WEB_VNEXT_AUTHORITY.md`.

## Visual principles

### 1. Imagery first

Real high-resolution EO/satellite scenes should carry the visual character. Do not obscure them with excessive UI.

### 2. Clean images after hero

Only the hero is allowed substantial overlay copy. Subsequent solution images should remain visually clean.

### 3. Technical beams carry language

The horizontal beam between images is where the story index, uppercase title, one- or two-sentence statement and a monospace descriptor live. It spans the entire viewport and stays dark.

### 4. On-image location labels are part of the brand language

Every satellite scene carries its real-world location and coordinates **directly on the image, bottom-right**, as small uppercase tracked monospace text. Story panels that reuse gallery imagery add a third, dimmer line so the image is never mistaken for a scientific output:

```text
CRATER LAKE, OREGON, USA
42.9443° N, 122.1353° W
NATURAL-COLOR COMPOSITE
```

Rules (ORBWEB-001.1, canonical):

- no card, box, pill, semi-transparent rectangle or separate metadata band;
- a subtle text-shadow is the only readability aid allowed;
- the same system on every image, hero included;
- sensor and acquisition date are not displayed on the homepage; they remain in `assets/imagery/sources.json` and `IMAGERY_RIGHTS.md`.

Keep it subtle and technical, not badge-like.

### 5. Scale matters

On desktop, images must occupy a large vertical slice and use the full viewport width. The site should communicate geographic scale and context, not look like a gallery of cropped thumbnails.

### 6. Restraint

Avoid:

- card grids
- feature icons
- decorative dashboards
- fake GIS controls
- glowing network lines
- abstract 3D globes
- excessive cyan accents
- multiple competing CTAs
- long explanatory sections
- scroll-jacking and gratuitous motion

## Navigation

Desktop (≥ 981 px): logo far left; the whole navigation group right-aligned, never centered. Live order (until MER-240):

`Platform` → `Solutions ⌄` → `Pilot` → `Company` → `Contact` → `|` → `EN | TR`

Approved target order (MER-238): `Home` → `Solutions ⌄` → `About` → `Partner with us` → `|` → `EN | TR`.

- Every item is a plain text item resolving to a real page (live: `/platform/`, `/pilot/`, `/company/`, `/contact/`; target: `/`, `/about/`, `/partner/`). The boxed CTA lives only in the hero.
- Solutions is a compact disclosure dropdown with exactly Geothermal, Mining, Marine (WEB-005C; live → `/solutions/#geothermal`, `#mining`, `#marine`; target Geothermal → `/solutions/geothermal/`): dark surface matching the header, no icons, no descriptions, no mega menu. Hover, keyboard focus and click open it; Escape and clicking outside close it; arrow keys move through items.
- The language switch is text only (`EN | TR`), active language in the cyan accent, inactive muted; no flags, no dropdown.

Mobile (≤ 980 px): hamburger reveals a restrained stacked list in the same order; Solutions expands and collapses on tap (never hover); Escape and link selection close the menu; the language switch stays at the bottom with tap-sized targets.

## Language

The homepage is bilingual: English is the default, Turkish is the second language. Switching is instant, client-side, preserves scroll position, updates `<html lang>`, the title and meta descriptions, and persists in `localStorage`. All strings live in the `I18N` dictionary in `script.js`; a new visible string is not done until both languages exist. Turkish copy is written as professional Turkish, not literal translation.

## Palette

Current implementation variables are in `styles.css`.

- nearly-black / deep navy base
- soft white primary type
- muted gray-blue metadata
- restrained cyan accent
- Earth imagery supplies the actual chromatic variation

Do not add a broad multi-color UI palette without approval.

## Typography

Current system stack is intentional for dependency-free deployment. The intended tone is technical, editorial and premium rather than playful. Large hero text can be light/regular weight. Section beams use compact uppercase tracking. A secondary system monospace stack (`--mono`) is used for coordinates, evidence labels, metadata, status tags and technical descriptors only.

A webfont may be introduced later only if it improves the final identity and licensing/performance are handled deliberately.

## Logo

Current vector assets:

- `assets/logo.svg`
- `assets/mark.svg`

The accepted orbital mark has **no Earth/globe inside it**. Preserve that property.

## Reference image

`references/visual-direction-reference.png` records an earlier visual direction approved as a starting point. It is reference material only. The textual rules in this document represent later user feedback and therefore override any conflicting details in that image.
