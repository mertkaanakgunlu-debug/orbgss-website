# Working notes that used to sit in the page source

**Why this file exists.** Until 2026-10-25 the deployed pages carried their working notes as HTML comments: the design rationale of each homepage act, how the scientific figures are prepared for display, which build scripts and records stand behind them. Anyone could read them with *view source*. The CTO's rule (2026-10-25: the public site does not explain how OrbGSS works behind the scenes) applies to the page source as much as to the page, so the comments were removed from every deployed page and `scripts/validate_site.py` now fails when an HTML comment returns. The notes are kept here, verbatim and in page order, because they record why the homepage is built the way it is. Nothing in this file is deployed (`docs/` is outside the `.vercelignore` allowlist).

Where a note names a record, the record is `assets/imagery/sources.json`, which is also no longer deployed (`.vercelignore`).

## Homepage (`index.html`)

Source: `index.html`. Comments, in document order.

### 1. WEB-004: the hero image is the LCP element, and it used to be discovered only after styles

```text
WEB-004: the hero image is the LCP element, and it used to be discovered only after styles.css
had been fetched and parsed. Preloading the same candidate set the <img> below declares lets
the browser start it during the initial HTML scan; imagesrcset/imagesizes must stay identical
to that img's srcset/sizes or the browser downloads the poster twice.
WEB-005: the LCP element is now the cinematic hero's poster frame. The video itself is never
preloaded and never eagerly fetched — script.js attaches its sources only after the poster has
painted, and only where motion and data policy allow, so the poster is the only hero image
request on first paint and mobile/reduced-data never pays for an encode at all.
WEB-005A: two posters, two jobs, one request. Where the motion is about to play the poster is
the OPENING frame, so poster -> video is continuous; where it never plays (reduced motion,
phone widths) the poster is the HELD frame the sequence ends on. The media queries here are the
<picture> below, exactly, so each visitor preloads the one still they will be shown.
```

### 2. WEB-005 FOUR-ACT HOMEPAGE (docs/WEB_PUBLIC_VISUAL_NARRATIVE_AUTHORITY.md).

```text
WEB-005 FOUR-ACT HOMEPAGE (docs/WEB_PUBLIC_VISUAL_NARRATIVE_AUTHORITY.md).

Hero -> real AOI context -> compact evidence trio -> priority/result climax. The WEB-001/002
six-scene "dark beam + full-width raster" gallery is gone: it gave every scientific state
equal weight and stretched correct cartography until it read as soft texture. Each act now
owns its own composition, and each explanation sits against the visual it describes.

WEB-005B: every scientific visual after the hero is a presentation derivative of the governed
MER-113 rasters, shipped as the exact checksummed file recorded in
assets/imagery/sources.json -> web_005b. Since R15 they are built by
scripts/build_web005b_presentation.py under MER-151 / GEO-WEB-004
(geothermal-prospectivity@e8aa5d65), which governs these homepage surfaces: canonical
normalization, a bounded display window and one fixed monotonic gamma per layer, the frozen
hero palette family, NoData transparent, lossless. Nothing is reprojected, filtered on the
page, smoothed, sharpened or rendered above its native grid, priority carries no window at
all, and none of it is baked into the hero video, where lossy encoding would change the
governed pixels. The scientific master is unchanged at 1200 x 1200 / 30 m / EPSG:32635 and
these files claim no finer ground resolution than that. Science semantics come from the
accepted authorities and are not reinterpreted here.
```

### 3. ACT 1 — CINEMATIC ACQUISITION HERO.

```text
ACT 1 — CINEMATIC ACQUISITION HERO.
The visual is the accepted WEB-HERO-001D pre-data sequence (Earth establish -> satellite
entrance -> AOI acquisition/scan -> continuous approach -> stable regional hold), rendered
against the real Kızıldere regional frame and carried forward from
feat/web-hero-001-predata-scene@e95fdcac7cac82e597d40dab4cdc96ce1a6b319e.

It is a RENDER, not sensor imagery, and says so in its own caption. Headline copy stays in
HTML inside the motion-safe region the shot was measured against, never baked into a frame.
The poster is the LCP element and the only hero image fetched on first paint.
```

### 4. Startup poster vs held base (WEB-005A, docs/web-005-polish-authority@1437fbb). The poster 

```text
Startup poster vs held base (WEB-005A, docs/web-005-polish-authority@1437fbb). The poster a
visitor sees before the motion is the sequence's OPENING frame; showing the ending first read
as a reverse-story flash (held target -> Earth establish). Where the motion never plays the
<source> swaps in the HELD frame instead, which is what those visitors end on anyway.
```

### 5. preload="none" and no <source> children on purpose. script.js attaches the encodes only

```text
preload="none" and no <source> children on purpose. script.js attaches the encodes only
when the visitor is not on a reduced-motion, reduced-data or small-screen profile, so
exactly one encode is ever fetched and often none is. With JavaScript disabled the
poster is the hero, which is an intentional state rather than a failure.
```

### 6. The held base: the frame the video ends on, and the ONLY frame the drape states register

```text
The held base: the frame the video ends on, and the ONLY frame the drape states register
with. Every static state (Save-Data, slow network, autoplay blocked, stalled or failed
playback, no JavaScript) lays it over the startup poster before the payoff appears, so the
priority surface is never composited on the opening Earth. data-src: a visitor whose
motion plays never fetches it, because their video ends on this very frame.
```

### 7. The analytical payoff (WEB-005A final production). The motion video ends on one held frame

```text
The analytical payoff (WEB-005A final production). The motion video ends on one held frame
and carries no governed analytical pixel: a lossy encode would change the colours those
pixels are read by. What follows the hold is composited here instead. Each state is the
true 36 km analysis footprint raised into DEM relief and draped with one prepared 4K
display layer, rendered on its own from the same scene and the same held camera through a
Standard view, and shipped as a lossless full-frame RGBA PNG (checksums and source-texture
checksums in assets/imagery/sources.json, web_005.hero_drape_states). The images share the
poster's own fit rule, so they register with the video pixel for pixel at every hero size
with no placement maths. script.js cross-fades Terrain, THM-01, ALT-01 and the priority
surface in the accepted order and leaves the priority surface alone; every static state
shows the priority surface at once. Where a layer has no analytical support the Terrain
context shows through; nothing is filled in. There is deliberately no colour bar, legend,
card or label here (Product decision b9579ef section 4): Acts 3 and 4 carry the exact
public labels and mandatory warnings. Every state is data-src: script.js promotes the
priority state on the desktop reveal and the transitional states only when motion plays,
so a phone fetches none of them and a static desktop visitor fetches one. With JavaScript
off the noscript image is the payoff. Desktop layout only: below 981 px the copy spans the frame and
a bright surface behind it would cost the copy its contrast.

The relief RISES into the Terrain state (docs/web-005-polish-authority@0e87675): the hero-drape-rise
images are the scene's own frames between the held frame (276) and Terrain (292), rendered
like a state (lossless WebP, checksums in web_005.hero_relief_rise), and script.js
interpolates between successive ones on the scene's 24 fps clock -- 0.667 s, eased by the
scene itself, outline and contact shadow rising with the block. Motion path only: they
are data-src, fetched while the video plays, and never by a static or phone visitor.
```

### 8. ACT 2 — THE REAL PLACE, BEFORE ANALYSIS (WEB-005B R11, accepted final Claude Design).

```text
ACT 2 — THE REAL PLACE, BEFORE ANALYSIS (WEB-005B R11, accepted final Claude Design).

The act the hero hands to, and the one cinematic moment below the fold: a single contained
Landsat band with the copy inside the photograph's protected left/bottom zone rather than in
a row above it (R10 section 8 — "the accepted large Landsat context composition with
integrated text/protected readable zone"). The protection is a gradient over the class-A
photograph only; Acts 3 and 4 are governed rasters and no gradient ever touches them.

The frame is the same USGS product as GEO-WEB-002, re-cropped wider at native 30 m
(3200 x 1800 px, 96 x 54 km) and tone-rendered on one common reflectance scale so colour is
the sensor's, not a per-band stretch — sources.json -> web_005b.context. The 3200 px master
fills a 1600 CSS px band on a 2x display at native density; nothing is upscaled.

R14: the AOI corner marks are GONE. The recorded analysis grid spans x 0.169-0.544 of this
frame and the copy column covers the left ~49% of it, so the square measured 72-100% hidden
behind the copy at every desktop width, and no crop can separate them: pushing the square
right of the copy requires cropping its own left edge away. A half-visible piece of governed
geometry is worse than none, so it is removed rather than left ambiguous. The geometry itself
is still recorded, still exercised by the validator, and still drawn by the inspection aid.
This act is CONTEXT: not evidence, not a scored input, and its acquisition date is not the
acquisition date of any THM or ALT evidence layer.
```

### 9. ACT 3 — ONE GROUND, READ THROUGH SEVERAL LAYERS (WEB-005B R11, accepted final Claude Desig

```text
ACT 3 — ONE GROUND, READ THROUGH SEVERAL LAYERS (WEB-005B R11, accepted final Claude Design;
language simplified in R14).

The accepted composition replaces the rejected three-equal-card gallery with ONE shared
geographic frame: the same 36 x 36 km square on the same 30 m grid, in the same place on the
page, with only the evidence inside it changing. That is the point the three cards could not
make — the frame never moves, so the layers are actually comparable.

Selection is three radio inputs, so it works with no JavaScript, with the keyboard (arrow
keys inside the group) and with touch. The selected state is carried by an underline rule, the
label colour AND a "Shown" marker, never by colour alone. The plates share one grid cell and
cross-fade; the reading column stacks in one cell too, so switching never shifts the layout.

Pixels are MER-151 presentation derivatives built by scripts/build_web005b_presentation.py
from the governed MER-113 rasters: canonical normalization, a bounded display window and one
fixed gamma per layer, the frozen hero palette family, NoData transparent over a neutral DEM
hillshade, lossless — sources.json -> web_005b.analytical. R15: the display window is what
finally makes the Alteration layer legible; 99.9% of its governed valid cells sit in the
bottom 8.3% of the canonical range, so the unwindowed render spent the whole palette on
outliers. Terrain and the priority result carry no transfer at all and are byte-identical to
what the accepted hero payoff ends on.
Structure/geology stays the subordinate data-gap footnote below; it is not a fourth layer.

R14 simplifies what the UI SAYS, not what it shows. The layer ids (THM-01, ALT-01) and the
specialist descriptors are gone from the visible labels because this is a homepage, not a
report; they remain the accepted identifiers in the manifest. The mandatory scientific
warnings are carried through VERBATIM — they are the honesty anchors and are not the place to
economize on words. The per-plate metadata strip is gone because it repeated, word for word,
the extent/grid/projection line the reading column already carries.
```

### 10. ACT 4 — THE RESULT (WEB-005B R11, accepted final Claude Design).

```text
ACT 4 — THE RESULT (WEB-005B R11, accepted final Claude Design).

The payoff composition: a large centred headline, the priority surface alone as the dominant
object in the section, and a four-part definition structure underneath that ends on what the
score is NOT. Its dominance comes from scale, centring and silence around it — not from a
different page background (R10 section 6).

Same palette the hero payoff ended on (MER-108 priority_deep_purple_red_orange_yellow_v1,
fixed 0-100, never windowed). The map is capped at 600 CSS px because its native grid is
1200 px: a 2x display is served at, never above, native density. The cyan corners are the
Product-owned target frame (the hero's lock, carried to the result) and are not data. The
legend is the unblended 256-entry LUT the map was coloured with, coupled directly beneath the
map inside the same figure — never a detached page-level colour strip.
```

### 11. INSPECTION AID (WEB-005B R11, accepted final Claude Design).

```text
INSPECTION AID (WEB-005B R11, accepted final Claude Design).

Present in the final accepted design at exactly this placement and role: its own quiet
section between the result and the domains, comparing the photograph with ONE derived layer.
It is a way to look, not a published figure — the published figures are Acts 3 and 4 above.

The prototype wiped the square 36 km rasters against the wide 96 x 54 km photograph and had to
caveat that as "approximate common framing". It does not have to be approximate: the manifest
records the analysis grid's exact bounds inside the context frame
(web_005b.context.frame.aoi_in_frame = x 0.169063-0.544063, y 0.166667-0.833333), which is
exactly 1200 x 1200 of the 3200 x 1800 master — the same 36 x 36 km at the same 30 m. The CSS
below scales and offsets the photograph by those recorded fractions, so the two sides are
genuinely the same ground. Nothing is re-projected, re-sampled beyond presentation scaling,
filtered or re-coloured; both sides are the files Acts 2-4 publish.

No JavaScript: the wipe rests at a static 50/50 split and still reads. With JavaScript the
range input drives it; the whole frame is the drag target, so the touch area is the figure.
```

### 12. SOLUTIONS (WEB-005B R11 composition, renamed and simplified in R14).

```text
SOLUTIONS (WEB-005B R11 composition, renamed and simplified in R14).

The accepted hierarchy: the active domain leads at full width, the two expansion directions
sit beneath it at half width, and every card states its own status. All three cards use one
composition — title and status, lower-left — with identical padding (R14 A). MER-240 moved
each card's description sentence to the /solutions/ hub table, its one home (M6 rule R1).

The photographs are illustrative locked WEB-001 Landsat scenes, not OrbGSS outputs and not
the pilot area. Their per-card location/coordinate/kind captions were removed for this
revision at Product's instruction; the footnote below the cards is now the sole carrier of
that honesty and says plainly what the three images are. Do not delete it: without it these
photographs read as OrbGSS results from the pilot area, which is what the captions were
preventing. Their provenance stays fully recorded in assets/imagery/sources.json.

The taxonomy is Geothermal / Mining / Marine (R13 section 2). The card titles keep their own
`domain.*.title` strings; the status labels use the shared `app.*.status` keys, so Mining and
Marine read "Expansion direction" on every page (M6 rule R8).

Each card is a native link to its domain's home (WEB-005C R2; MER-240 targets): Geothermal to
/solutions/geothermal/, Mining and Marine to their /solutions/ bands. The link wraps the copy
block and stretches over the whole card through its ::after, so the entire card is the click
target without a CTA, an arrow or any change to the imagery, spacing, status or hierarchy.
aria-labelledby points at the card title, so the accessible name is the domain name rather
than the whole card read aloud. Navigation needs no JavaScript.
```

### 13. CONTACT — one centred line (MER-240, M6 authority 4.1). Method and Company live on /about/

```text
CONTACT — one centred line (MER-240, M6 authority 4.1). Method and Company live on /about/,
and the conversation types and the address live on /partner/, their one home (rule R1).
The id stays, so existing /#contact links still land here.
```

## Data sources page (`sources/index.html`)

Source: `sources/index.html`. Comments, in document order.

### 1. The copyright line below carries no year on purpose: no source reachable from the build en

```text
The copyright line below carries no year on purpose: no source reachable from the build environment states the year of the v8.0 release file, and the one secondary source seen (the PyPI cmcrameri licence) says 2020 for its own copy. Take the exact line from the licence file of the Zenodo release (doi:10.5281/zenodo.8035877) before publication; the record is web_m6.licence_notices in assets/imagery/sources.json.
```

## Generated Turkish pages

Each file under `tr/` used to open with a comment that said it was generated by `scripts/build_tr_pages.py` from its English page and the `I18N` dictionary in `script.js` (MER-241) and must not be edited by hand. The comment is gone from the pages; the rule stands and is stated in `CLAUDE.md`, and `scripts/validate_site.py` fails when `tr/` is not byte-identical to the generator's output.
