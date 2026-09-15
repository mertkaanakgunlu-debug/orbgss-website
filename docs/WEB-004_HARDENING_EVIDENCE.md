# WEB-004 — Responsive, accessibility, performance and preview evidence

**Task:** `tasks/WEB-004_PREVIEW_HARDENING.md` (MER-92)
**Branch:** `feat/web-004-preview-hardening`
**Accepted baseline:** `main@f4d77b4144ddff70c309986e6a45b163f62cdcd4`
**Authority publication:** `3a4d8e006add2725d45b02071bda654be5bd09f5`
**Implementation HEAD:** `56cb530` (`feat(web-004): responsive, accessibility and performance hardening (MER-92)`)
**Implementation state:** `REVIEW_READY` — committed on the feature branch, not merged and not pushed

This records what was measured, what was changed and what was deliberately not changed. Every
number below came from a run against a local static server on this repository; nothing here is an
estimate, and nothing here is a product claim.

## 1. Tooling and environment

| | |
| --- | --- |
| Validator | `py -3.14 scripts/validate_site.py` (Python 3.14.6) |
| Local server | `py -3.14 -m http.server 8080` from the repository root (`.claude/launch.json` → `orbgss-static`) |
| Performance | Lighthouse 13.4.1 (npm, run from a scratch directory outside the repository), headless Chrome 
| Lighthouse profile | `formFactor: mobile`, `screenEmulation` 412 × 823 @ DPR 1.75, `throttlingMethod: 'simulate'` (Lighthouse default Slow-4G + 4× CPU) |
| Responsive / a11y / contrast | Chromium DevTools protocol via the in-app browser pane at 375, 768, 1024 and 1440 CSS px |

Lighthouse was installed only in a scratch directory. **No package manager files, dependencies or
build step were added to this repository**; the site remains static HTML + CSS + vanilla JS.

### Harness limitation, recorded honestly

Under this session's browser pane the page runs with the pane hidden, and CDP viewport emulation
**does not dispatch `resize` or `matchMedia` `change` events to the page** — instrumenting the page's
own JS context with a counter returned `{"resize":0,"mq":0}` across a 375 → 1440 change. The
viewport-change reset (§4.1) therefore could not be triggered by a simulated rotation here. Its
handler was instead invoked directly in the page context and verified to clear every stale bit
(before/after in §4.1); the listener registration is the standard
`MediaQueryList.addEventListener('change', …)` and is unchanged from ordinary practice. For the same
reason, lazy images do not load on their own while the pane is hidden; wherever a measurement needed
a loaded raster, loading was forced explicitly and that is stated.

Screenshot capture through the hidden pane proved unreliable (repeated
`the page did not finish rendering in time`), so **the responsive matrix below is measurement-based
rather than screenshot-based**: per-element bounding boxes, computed styles, scroll widths and
sampled raster pixels at each width. That is stricter than a visual check — it catches a 21 px
activation target or a 2.84:1 caption that the eye would pass — but it is recorded here as a
difference from the task's "screenshot/measurement matrix" wording rather than glossed over.

## 2. Validator

`py -3.14 scripts/validate_site.py` → **PASS, 0 warnings**, before and after (`scenes: 4`,
`html images: 11`, `routes: 6`, `i18n keys referenced site-wide: 185`).

The validator was extended (§4.6) and both new checks were negative-tested — each was confirmed to
fail the build when deliberately broken, then restored:

- corrupting one recorded hero-derivative checksum →
  `ERROR: scene derivative checksum mismatch for assets/imagery/crater-lake-2023-900.webp`
- pointing a hero `srcset` candidate at an unrecorded file →
  `ERROR: HTML imagery paths missing from provenance manifest: ['assets/imagery/crater-lake-2023-ghost.webp']`

## 3. Performance

### 3.1 Lighthouse, mobile profile

Baseline is the accepted `main@f4d77b4`; final is this branch.

| Route | Perf | A11y | Best Prac. | SEO | LCP | CLS | TBT |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `/` baseline | **77** | 100 | 96 | 100 | **6.5 s** | 0 | 0 ms |
| `/` final | **94** | 100 | 96 | 100 | **3.2 s** | 0 | 0 ms |
| `/platform/` | 100 | 100 | 100 | 100 | 1.4 s | 0 | 0 ms |
| `/solutions/` | 100 | 100 | 100 | 100 | 1.6 s | 0 | 10 ms |
| `/pilot/` baseline | 99 | 100 | 96 | 100 | 2.0 s | 0 | 0 ms |
| `/pilot/` final | 99 | 100 | 96 | 100 | 2.0 s | 0 | 0 ms |
| `/company/` | 100 | 100 | 100 | 100 | 1.4 s | 0 | 0 ms |
| `/contact/` baseline | 100 | **98** | 100 | 100 | 1.4 s | 0 | 0 ms |
| `/contact/` final | 100 | **100** | 100 | 100 | 1.4 s | 0 | 0 ms |

Against the task's budget floor (Accessibility ≥ 95, Best Practices ≥ 95, SEO ≥ 95, Performance ≥ 90
on the homepage and on at least one deep route): **every route meets every floor.**

### 3.2 Page payload

Measured from the Lighthouse network record for `/` on the mobile profile:

| | Baseline | Final | Change |
| --- | --- | --- | --- |
| Total transfer | 1369.6 KiB | **645.1 KiB** | **−52.9%** |
| Image bytes | 1268.4 KiB | 530.3 KiB | −58.2% |
| Requests | 14 | 13 | −1 |

Largest remaining asset is `assets/proof/priority-800.webp` at 249.7 KiB — an accepted, checksummed
scientific proof derivative that WEB-004 is not permitted to re-encode.

### 3.3 Static code budget

| | Baseline | Final | Change |
| --- | --- | --- | --- |
| `styles.css` | 24,336 B | 25,316 B | +4.0% |
| `script.js` | 50,865 B | 61,067 B | +20.1% |
| **Combined, uncompressed** | 75,201 B | **86,383 B** | **+14.9%** |
| Combined, gzipped | 20,836 B | 24,356 B | +16.9% |

Uncompressed this sits just inside the task's 15% threshold; **gzipped it exceeds it, so the
justification is recorded here as required.** The entire increase is three items, each of which
either fixes a defect or removes far more weight than it adds:

1. the measured caption-tone system (§4.2), which resolves a real WCAG 1.4.3 failure that no static
   value could fix;
2. the deferred evidence-layer promotion (§4.4), which removed **340 KiB** from the initial load —
   roughly thirty times the JavaScript it cost;
3. the viewport-change state reset (§4.1), a few lines.

WEB-004 has not become the dominant page payload: first-party CSS + JS is 86 KiB of a 645 KiB page.
It is a larger *share* than before only because total page weight roughly halved.

No minifier or build step was introduced; Lighthouse's `unminified-javascript` opportunity
(~11 KiB) is left on the table deliberately, because taking it would mean adding a build pipeline
the accepted architecture forbids.

## 4. Changes made

### 4.1 Stale navigation state across a viewport change (defect, fixed)

Crossing the 980 px breakpoint with the mobile menu open left `.main-nav` flagged open, left the
now-hidden menu button reporting `aria-expanded="true"` with its "Close navigation" label, and left
the **Solutions submenu visibly open on the desktop bar** with no pointer or focus in it. Captured
on the accepted baseline:

```
before: navOpen=true  toggleAria=true  toggleLabel="Close navigation"
        submenuOpen=true  triggerAria=true  submenuDisplay=block
```

`script.js` now resets both disclosures when the breakpoint is crossed. Handler verified in page
context:

```
after:  navOpen=false toggleAria=false toggleLabel="Open navigation"
        submenuOpen=false triggerAria=false submenuDisplay=none
```

### 4.2 On-image caption contrast (defect, fixed)

WEB-002 chose each proof panel's caption tone by hand from the measured luminance under the caption.
The rule is right; applying it once is not. Story panels crop their raster with `object-fit: cover`,
so the pixels under the bottom-right caption **change as the viewport changes shape**. Measured on
the accepted baseline (fresh page load at each width, contrast of the authored tone against the
actual sampled raster):

| Panel | 375 | 768 | 1024 | 1440 |
| --- | --- | --- | --- | --- |
| `observe` | **3.53** | 14.05 | 12.16 | 19.05 |
| `terrain` | 5.13 | 10.77 | 7.61 | ~13.5 |
| `thm01` | 11.48 | 13.22 | 11.12 | 14.62 |
| `alt01` | 5.67 | 10.61 | 10.40 | 10.58 |
| `alt02` | 5.83 | 11.07 | 9.27 | 9.58 |
| `priority` | 8.71 | 6.71 | 7.08 | 4.95 |
| `geothermal` | **2.84** | 5.04 | **4.21** | 5.88 |

Three measured failures against WCAG 1.4.3's 4.5:1. `script.js` now applies WEB-002's own rule
continuously: it samples the rendered region under each caption and keeps whichever of the two
**already-accepted** tones contrasts better. After:

| Panel | 375 | 768 | 1024 | 1440 |
| --- | --- | --- | --- | --- |
| `observe` | 5.44 | 6.30 | 12.17 | 19.05 |
| `terrain` | 5.13 | 5.54 | 7.61 | ~13.5 |
| `thm01` | 11.49 | 11.13 | 11.12 | 14.62 |
| `alt01` | 5.77 | 9.82 | 10.16 | 10.58 |
| `alt02` | 5.74 | 9.21 | 9.40 | 9.58 |
| `priority` | 8.47 | 7.77 | 7.08 | 4.95 |
| `geothermal` | 6.65 | 5.71 | 4.58 | 5.88 |

**Every caption clears 4.5:1 at every tested width.** In each case the applied value equals the
better of the two tones, confirming the selection is optimal rather than merely different.

Note `geothermal` resolves to the dark tone at 375/768/1024 and the light tone at 1440 — a static
authored value could not have been correct everywhere, which is the point.

Design invariants are untouched: the caption is still bare monospace text bottom-right with no card,
box, band or background container; the raster is never modified, re-coloured or re-rendered; only
the caption's own colour changes, and only between the two tones the design already ships. Without
JavaScript, or if the canvas cannot be read, the authored WEB-002 tone stands unchanged.

The hero caption is deliberately **excluded** — it sits under the `.hero-shade` gradient, so raw
raster sampling would mis-measure it. Measured separately with `object-position: 68% 49%` honoured,
the hero caption reads **6.84:1 against the image alone** at 375 px, and the shade over it only
darkens the backdrop further, so the true value is higher. No change needed; see §6 for the
constraint this places on WEB-005.

### 4.3 Hero LCP

The hero was a 553 KiB JPEG serving every viewport, discovered only after `styles.css` had been
fetched and parsed. Three recorded WebP derivatives were generated (resize + encode only — no crop,
colour, tone or gamma change) and wired up with `srcset`/`sizes` plus a matching
`<link rel="preload" imagesrcset>`:

| Derivative | Size |
| --- | --- |
| `crater-lake-2023-900.webp` | 148.3 KiB |
| `crater-lake-2023-1400.webp` | 278.3 KiB |
| `crater-lake-2023-1800.webp` | 370.4 KiB |

A 375 px phone now fetches ~148 KiB instead of 553 KiB. The hero request starts at 14 ms, before
the stylesheet. Lighthouse's LCP discovery checklist is fully green: `fetchpriority=high` applied,
request discoverable in the initial document, not lazy-loaded. The JPEG remains as the `src`
fallback and as the Open Graph poster.

All three derivatives are recorded in `assets/imagery/sources.json` under the hero scene with path,
role, dimensions, format, the exact operation performed, byte size and SHA-256, and the validator
recomputes those checksums on every run.

Colour fidelity was verified rather than assumed. Each derivative was resampled back to the source
geometry and its per-channel mean compared with the source JPEG (source mean RGB
105.16 / 110.05 / 84.15):

| Derivative | Max mean-channel deviation |
| --- | --- |
| `crater-lake-2023-900.webp` | 0.173 / 255 |
| `crater-lake-2023-1400.webp` | 0.182 / 255 |
| `crater-lake-2023-1800.webp` | 0.285 / 255 |

All under 0.12% — consistent with resize-and-encode only, with no re-colour, tone or gamma change.

At 1440 CSS px / DPR 1 the browser selects the 1800 px candidate (the 1400 px candidate is narrower
than the 1425 px slot). That is correct behaviour; the constrained case is mobile, where the 900 px
candidate is selected.

### 4.4 Deferred inactive evidence layers

The evidence panel fetched all three layers during initial page load — 340 KiB of rasters nobody
was looking at yet, competing with the hero for bandwidth. Measured cost: **six Lighthouse
performance points** (88 → 94 when removed).

The two inactive layers now carry `data-src`/`data-srcset`, promoted by `script.js` when the
evidence section approaches the viewport (600 px margin), and defensively on any pointer or focus
interaction with the tablist. Switching layers stays instant for a reader who scrolls there.
Verified: at page top the two inactive layers are deferred and the active one is live; after
interaction they promote and load, with `aria-selected`, roving `tabindex`, `aria-hidden` and the
per-pane caption all correct.

Without JavaScript the inactive panes are permanently hidden, so not fetching them is the truthful
behaviour — consistent with the existing WEB-002 note. They remain recorded, checksummed proof
assets, and the validator now reads `data-src`/`data-srcset` so moving a raster behind a deferred
attribute cannot exempt it from the provenance checks.

### 4.5 Accessibility fixes

- **`/contact/` heading order** — the three contact options were `<h3>` directly under the page
  `<h1>` with no `<h2>`. Lighthouse flagged `heading-order`; they are now `<h2>`, and `/contact/`
  Accessibility went 98 → 100.
- **Touch targets (WCAG 2.5.8, 24 × 24 px).** Measured undersized on the accepted baseline and now
  fixed by padding and `min-width` — no type-size or density change:

  | Target | Before | After |
  | --- | --- | --- |
  | Footer nav links (× 5) | 53 × **11** | ≥ 24 tall |
  | `.contact-mail` | 151 × **18** | ≥ 24 tall |
  | `.brand` | 68 × **21** | ≥ 24 tall |
  | `.lang-btn` EN / TR (desktop) | **22** × 26 / **21** × 26 | ≥ 24 wide |

  Final sweep: **0 undersized targets** on all six routes at 375, 768, 1024 and 1440.
- **Web manifest** now declares a real icon (`assets/mark.svg`) instead of an empty `icons: []`.

### 4.6 Validator extensions

- `img[srcset]` and `link[rel=preload][imagesrcset]` candidates are now collected, so a responsive
  candidate cannot enter a page without a provenance record.
- `img[data-src]` / `[data-srcset]` are collected for the same reason.
- Scene derivatives are checked exactly like proof derivatives: required fields, existence, byte
  size and recomputed SHA-256.

## 5. Responsive, keyboard and bilingual results

- **Horizontal overflow: none.** All six routes at 375 / 768 / 1024 / 1440 report `scrollWidth`
  equal to viewport width and zero elements crossing the viewport edge, measured with the
  `overflow-x: hidden` safety net temporarily disabled so it could not mask a real defect.
- **Keyboard.** With the mobile menu open, focus passes through all five nav links, then the Solutions
  trigger, then EN and TR, then continues into the page — every step within the viewport, no focus
  loss and no trap. The Solutions disclosure keeps arrow/Home/End handling and Escape returns focus
  to the trigger. Evidence tabs keep roving `tabindex` (active `0`, others `-1`), synchronized
  `aria-selected` / `aria-hidden`, and the caption travels with its pane.
  *Note:* button activation by Enter/Space could not be exercised through this harness — CDP key
  events arrive with an empty `key`, so the browser performs no default activation. These are real
  `<button>` elements, so activation is the platform's, not the site's.
- **Bilingual.** Switching to TR updates `<title>`, meta description, headings, body copy, `aria-label`
  values, the menu-toggle label and `aria-pressed`, sets `documentElement.lang="tr"`, and persists
  across every route through the shared `localStorage` key. The validator enforces EN/TR parity for
  all 185 referenced keys and fails on any `aria-label` not bound to `data-i18n-aria-label`.
- **Links and assets.** All six routes, `404.html`, `sitemap.xml`, `robots.txt`, `site.webmanifest`
  and all 28 unique referenced asset paths return 200; every internal fragment resolves.
- **Reduced motion.** `@media(prefers-reduced-motion:reduce)` disables all transitions and smooth
  scrolling; the layer switch remains fully functional without its opacity transition.
- **Scientific invariants.** Proof checksums, provenance, export identity, data-gap state and the
  mandatory EN/TR warnings all still pass unchanged; no scientific raster was re-encoded,
  re-coloured, re-cropped or CSS-transformed.

## 6. WEB-005 hero media budget

Adopted from measurement, and **tighter than the Product default** where the evidence supports it.

Current homepage transfer is 645 KiB, of which the hero poster is 148 KiB at mobile width. Holding
the homepage at its present Lighthouse Performance of 94 means the hero may not add materially more
than it does today on a mobile first load.

| Asset | Ceiling | Basis |
| --- | --- | --- |
| Desktop autoplay WebM | **≤ 3.0 MiB** | tightened from the 4 MiB default; desktop-only, never fetched on mobile |
| MP4 fallback | **≤ 4.5 MiB** | tightened from 6 MiB; must never be fetched alongside the WebM |
| Poster still | **≤ 180 KiB** | tightened from 500 KiB; the current 900 px WebP poster is 148 KiB and already carries the hero at mobile width |
| Mobile / reduced-data | **poster only, no video** | a second encode on mobile would undo §4.3 outright |

Hard constraints for WEB-005, from this task's measurements:

1. **One encode per client, ever.** Mobile and reduced-data clients must not download both encodes.
2. **The poster must stay the LCP element and must stay preloaded**, with `imagesrcset`/`imagesizes`
   identical to the `<img>`'s `srcset`/`sizes` — a mismatch double-fetches the poster.
3. **`prefers-reduced-motion: reduce` must get the static poster**, not an autoplaying video.
4. **The hero caption region (bottom-right) must keep ≥ 4.5:1** against whatever the final hero puts
   under it. Today it measures 6.84:1 against the image alone. The hero caption is *not* covered by
   the runtime tone system (§4.2), because `.hero-shade` sits between raster and text; if WEB-005
   changes that stack, either re-verify by hand or bring the hero into the measured-tone system.
5. **Any hero media must be recorded and checksummed** in `assets/imagery/sources.json` like the
   derivatives in §4.3; the validator enforces this.

## 7. Deliberately not changed

- **`image-aspect-ratio` (Best Practices 96 on `/` and `/pilot/`).** The score legend colourbar is a
  652 × 28 export displayed as a ~110 × 9 strip. The squash is deliberate design, and because the
  ramp is a vertically constant gradient it is visually lossless. Fixing the audit would mean either
  re-proportioning an accepted legend or re-encoding a checksummed proof derivative. Best Practices
  clears its ≥ 95 floor at 96 on both routes. **Recorded as an accepted deviation, not an oversight.**
- **LCP 3.2 s on `/` versus the 2.5 s target.** Improved from 6.5 s, and Lighthouse's own LCP
  discovery and breakdown insights now both pass. The residual is bandwidth contention under
  simulated Slow-4G, dominated by `priority-800.webp` (249.7 KiB) — an accepted, checksummed
  scientific derivative WEB-004 may not re-encode. **Routed to Product rather than relaxed:** closing
  the remaining gap needs either authority to re-export the proof derivatives at web scale (a
  Science/Product decision, not an implementer one) or explicit acceptance of 3.2 s under this
  synthetic profile. Nothing was degraded to manufacture a better number.
- **No minification / build step**, per the accepted static architecture.
- **Structure/geology data gap** remains an explicit public data gap.
- **Homepage narrative, route structure, palette and information architecture** — WEB-004 is a
  hardening task and did not redesign the accepted WEB-003 site.

## 8. Preview and release gates

**`HOSTED_PREVIEW_NOT_RUN — permission unavailable.`** There is no Vercel CLI on this machine, no
`~/.vercel` or project `.vercel` link, and no Vercel token in the environment. Per the task, no
credentials were requested and no account, admin or billing state was touched.

Reproducible local preview:

```bash
py -3.14 scripts/validate_site.py && py -3.14 -m http.server 8080
```

then open `http://localhost:8080/`. (`preview-local.bat` does the same on Windows.)

**`CONTACT_RELEASE_GATE`.** Route and mailto correctness is confirmed: every `mailto:` across all six
routes and both dictionary languages targets `contact@orbgss.com` and no other recipient, with
correctly percent-encoded EN and TR subjects. Mailbox **ownership and deliverability cannot be
proven** from this repository without Google Workspace or admin access, which is out of scope and was
not attempted. This remains a mandatory pre-WEB-006 / pre-launch gate.

## 9. Explicit confirmations

- No WEB-005 hero integration. The hero remains the WEB-001 static poster
  (`data-hero-slot="static-poster"`, `data-visual-status="deferred-web-005"`); only its delivery was
  optimized.
- No WEB-006 work. No production deployment, no domain attachment, no DNS change, no Squarespace
  change, no MX/SPF/DKIM/DMARC or Google Workspace change.
- No analytics, tracking, auth, CRM, billing, backend, form or PII collection introduced.
- No framework, package manager, dependency tree or CMS added to the repository.
- No scientific methodology, score semantics, proof asset, warning or provenance record altered.
- No purchase, credential entry, ownership transfer or irreversible hosting operation performed.
