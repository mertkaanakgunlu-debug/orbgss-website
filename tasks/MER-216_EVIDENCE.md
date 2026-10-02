# MER-216 — Website media fidelity & runtime hardening: evidence

**Linear:** MER-216 (consolidates and supersedes MER-143, MER-144, MER-145, MER-146)
**State:** `REVIEW_READY` — Phases 1–4 evidenced; the implementation agent does not self-accept.
**Branch:** `claude/mer-216-s1r628`, created from the verified baseline `origin/main@f4f1d4d6cb6ff4acd4ad02129bb9ec13a50ade85`
**Executed on:** the CTO workstation (Windows 11, Claude Code over Remote Control), where the governed
Kızıldere rasters and the authoritative hero master exist, as the Linear "Execution-environment decision — 2026-10-02" requires.
**Evidence artifacts:** `evidence/mer216/` (raw results and the audit tooling), `hero/evidence/responsive_media.json`.
**Not done, by design:** no `main` update, deploy, DNS, Vercel or credential change, no force-push, no Linear close.

---

## 0. Phase 0 — canonical preflight (re-verified on the workstation)

| Check | Result |
| --- | --- |
| Linear | MER-216 read by ID (In Progress); MER-213 is **Done** |
| Git | `origin` = `mertkaanakgunlu-debug/orbgss-website`; `git fetch` clean; `origin/main` = `f4f1d4d6…`; `79cc2cb` (production) is an ancestor of it; working tree clean apart from one pre-existing **untracked** `AGENTS.md` (Codex bootstrap file, not touched) |
| Branch | the cloud session branch `claude/mer-216-s1r628` had never been pushed; the same name was created locally from `origin/main`, with **no upstream** configured so nothing can reach `main` by accident |
| Governed export | `geothermal-prospectivity/outputs/kizildere_mvp_v2/exports/20260917T161155Z-5e7a0e53` present (`export_manifest.json`: project `kizildere_mvp_v2`, grid EPSG:32635, 1200 × 1200, 30 m, origin 639270 / 4223040, status `succeeded`, every output `byte_copy_of_accepted_source`) |
| Raster SHA-256 (computed here, equal to `assets/imagery/sources.json → web_005b.analytical.layers`) | `top-dem.tif` `590f7432…`, `thm-thm01.tif` `6a2850f9…`, `alt-alt01.tif` `ac7f2dad…`, `score-mvp-remote-sensing-priority.tif` `15065152…` — **4 / 4 match** |
| Hero master | `hero/renders/production/frame.png`: 276 PNG frames, 2304 × 1296 RGBA (alpha 255 throughout); all 276 SHA-256 match the latest render record per frame (`render_record.json` ×69, `_pass2` ×193, `_pass3` ×14) |
| Hero source textures | `hero/assets/source/*` present; `py -3.14 hero/scripts/validate_hero.py` = **420 checks, 0 failed** (the 13 failures MER-213 saw in a cloud clone are exactly these absent files) |
| Baseline validators | `py -3.14 scripts/validate_site.py` PASS, 0 warnings |

Authority read: `STATUS.md`, `CLAUDE.md`, `docs/WEB_PUBLIC_VISUAL_NARRATIVE_AUTHORITY.md` (the binding media envelope), `hero/config/lane.json`, `assets/imagery/sources.json`, the MER-151 presentation authority as recorded in the manifest, and the MER-108 website display derivative authority `geothermal-prospectivity@11c32e8d`.

## 1. Phase 1 — analytical media fidelity: `PHASE_1_PASS`

**Finding.** The accepted homepage analytical story is *already* the output of the pipeline this phase asks for. The published Act 3 / Act 4 / inspection-aid derivatives are rendered by `scripts/build_web005b_presentation.py` straight from the governed MER-113 scalars and masks (WEB-005B R15, MER-151), not from any web render. This task therefore verified that claim end to end instead of regenerating it, and measured whether any derivative is missing for real device-pixel demand.

| Gate item | Evidence |
| --- | --- |
| Deterministic rebuild | `scripts/build_web005b_presentation.py` re-run in a fresh venv pinned to the recorded renderer (Python 3.14.6, numpy 2.5.3, rasterio 1.5.1, Pillow 12.3.0, libwebp 1.6.0): **all 12 derivatives + the legend ramp reproduce byte for byte**; `git status` after the rebuild shows no change; record vs `sources.json`: 0 mismatches (`evidence/mer216/phase1/deterministic_rebuild_record.json`) |
| Governed origin | the 4 source SHA-256 above; `export_manifest.json` identifies them as byte copies of the accepted sources; **no PNG/WebP was used as a source** |
| Independent re-derivation | `evidence/mer216/tools/verify_phase1_independent.py` does **not** import the build script. It re-implements normalization, the MER-151 window/gamma, the LUT, the neutral hillshade and the blend, and compares every native-grid derivative to the published file: **0 differing pixels in all four layers**; every published 600 / 900 rung is exactly the area (box) downsample of its native rung (0 differing pixels) (`phase1/independent_rederivation.json`) |
| Palette / legend | each layer's 256-entry LUT hash equals the recorded `lut_sha256`; the priority legend ramp equals the unblended priority LUT |
| Mask / NoData | NoData cells: THM-01 4,522, ALT-01 229,932, priority 239,187 (terrain has none). In every one of them the published pixel is **exactly the neutral hillshade** (0 bad pixels, chroma 0) — no analytical colour, fill, dilation or erosion crosses the governed mask |
| Lossy delivery rung | `scripts/build_web005b_delivery.py` re-evaluated: same decision as recorded — only Terrain passes the MER-108 §8 gates (q98), THM-01 / ALT-01 / priority stay lossless; nothing written |
| Validators | `validate_site.py` re-derives the LUTs, checksums and every MER-151 bound: PASS |

**Render boxes measured** (real Chrome, 12 viewport/DPR classes from 375 × 812 @3x to 3840 × 2160 @1x, plus a 25-width × 4-height layout sweep: `phase1/render_box_vs_demand_baseline.json`, `phase1/box_width_sweep.json`).
Every analytical surface is capped at 598 CSS px (Act 3 and the inspection aid) or ≤ 598 CSS px (Act 4, which tracks the viewport height). The device-pixel demand and the rung the browser picks:

| Class | Demand (px) | Selected rung |
| --- | --- | --- |
| 375 / 390 phone @3x | 903–1032 | 1200 |
| 768 tablet @2x | 1196 | 1200 |
| 1024 @1x / @2x | 410–485 / 820–969 | 600 / 1200 |
| 1440 @1x / @2x | 542–598 / 1084–1196 | 600 / 1200 |
| 1920 @1x / @2x (4K at 200 %) | 598 / 1196 | 600 / 1200 |
| 2560 @1.5x (4K at 150 %) | 897 | 900 |
| 3840 @1x (4K at 100 %) | 598 | 600 |

The browser's pick is within one rung of demand everywhere and **never an upscale of a governed raster**. The highest demand any class produces is 1196 device px, which the native 1200 px grid serves 1:1. A 4K / HiDPI enlargement would therefore add only bytes (MER-151 permits it, `CLAUDE.md` keeps it unpublished, and MER-108 forbids presenting it as finer evidence), so **no new analytical derivative family is warranted and none was added**. The Context ↔ Priority compare module exists (the inspection aid) and already shares these exact files, so no separate pair was produced.

One tuning was tried and rejected on evidence: re-fitting the Act 3 / Act 4 `sizes` attributes to the exactly measured boxes selected the same rungs everywhere except priority at 1024 @2x, where the Act 4 figure and the inspection aid then asked for two different files and the page transferred **1.5 MB more** (12.2 MB vs 10.7 MB). It was reverted; `index.html` analytical markup is unchanged.

## 2. Phase 2 — hero media hardening: `PHASE_2_PASS`

**Master used.** The highest-quality accepted source actually available: the 276 rendered 2304 × 1296 frames (§0). No Blender re-render, no change to choreography, camera, content, posters, held frame, drape or rise states.

**Measurement method (and a trap that was found and fixed).** Fidelity is PSNR / SSIM / VMAF of the delivered file against the master resized to the comparison size, with both sides written first as lossless constant-24-fps files and paired **by frame index**. Pairing the WebM directly against the PNG sequence by timestamp mis-pairs frames during camera motion (WebM carries millisecond timestamps) and made a healthy encode look broken in the first attempt; the cfr-safe method is in `hero/scripts/encode_responsive_media.py` and `evidence/mer216/tools/bench_video.py`.

**What the accepted encodes measured** (1920 reference): WebM 2.83 MiB PSNR 44.65 / SSIM 0.9833 / VMAF 89.45 (worst frame 77.3); MP4 4.05 MiB PSNR 44.51 / SSIM 0.9832 / VMAF 90.27 (worst 83.7). The MP4's atoms are `ftyp free mdat moov`: the `moov` sits **after** 4.2 MB of media, so a browser needs a second range request to start (measured: three requests for one MP4 playthrough).

**Tiers built** (FFmpeg 7.1, two-pass `libvpx-vp9` and CRF + maxrate `libx264`, Lanczos from the master, bt709 / tv tagged, keyframe every 48 frames; every argument list is recorded in `hero/evidence/responsive_media.json`):

| Role | File | Bytes | Avg kbps | PSNR | SSIM | VMAF (worst frame) | Envelope |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `hero-webm-sm` 1280 × 720 | `orbgss-hero-1280-21da1079.webm` | 1,646,519 (1.57 MiB) | 1145 | 46.04 | 0.9867 | 95.3 (83.0) | ≤ 2.0 MiB |
| `hero-mp4-sm` 1280 × 720 | `orbgss-hero-1280-164c957f.mp4` | 2,062,118 (1.97 MiB) | 1435 | 45.71 | 0.9869 | 95.5 (82.2) | ≤ 3.0 MiB |
| `hero-webm-md` 1920 × 1080 | `orbgss-hero-1920-ca741624.webm` | 2,920,385 (2.79 MiB) | 2032 | 46.83 | 0.9883 | 95.6 (81.3) | ≤ 3.0 MiB (binding) |
| `hero-mp4-md` 1920 × 1080 | `orbgss-hero-1920-c8db4a5a.mp4` | 3,584,878 (3.42 MiB) | 2494 | 46.16 | 0.9874 | 95.2 (85.5) | ≤ 4.5 MiB (binding) |

- The 1920 tier is **better and not larger**: WebM +6.1 VMAF at 2.79 vs 2.83 MiB, MP4 +4.9 VMAF at 3.42 vs 4.05 MiB. Old vs new decoded 1920 WebM agree at PSNR 45.3 (worst frame 41.1), and frames 120 / 222 / 276 were compared by eye (no visible difference in the Earth, the cyan analysis frame or the motion blur). All four files decode to exactly 276 frames at 24 fps.
- Both MP4s are **faststart** (`moov` before `mdat`, checked by `validate_site.py`): one request instead of three.
- File names carry the first 8 hex digits of their own SHA-256, because `vercel.json` serves `/assets/` as one-year `immutable`; `validate_site.py` fails when a name and its content drift apart.
- **A 2304 × 1296 tier (the master's native size) was built and measured and is not published.** At 3.29 MiB it scored VMAF 95.5 against the 2304 reference, versus 94.5 for the 1920 tier at 3.27 MiB: +1 point for +35 % pixels, and inside the binding 3.0 MiB envelope it cannot beat 1920. Trials: `evidence/mer216/phase2/encode_trials_*.jsonl` (VP9 1280 @1000/1400, 1920 @1500/1950/2300, 2304 @2300; H.264 1920 CRF 22/25, 1280 CRF 21).
- "Source quality supports them": 1280 and 1920 are at or below the master's 2304; nothing is an enlargement.

Playback was measured in real Chrome (§4): 276 / 276 frames presented in every class, 0–6 dropped frames (the 6 occur on the first run of the first class in both old and new trees, i.e. decoder warm-up).

**Gate evidence for fallbacks** is in §3 (resilience matrix).

## 3. Phase 3 — responsive integration: `PHASE_3_PASS`

Changed in `script.js` (the hero IIFE only; the markup change is `data-hero-tiers` and the two bare attributes now naming the 1920 tier):

1. **One choice, before any video byte.** Tier = the smallest encode at least 92 % as wide as the device pixels the 16:9 cover-fit frame must fill (`max(width, height × 16/9) × DPR`); codec = VP9 where the browser is confident, else H.264. The network `downlink` hint can only move a visitor **down** (a tier needs 1.5× its own average bitrate; measured below), and `navigator.mediaCapabilities.decodingInfo` (1.2 s time-boxed) steps down a tier when the decoder reports "not smooth" and falls back to the other codec when it reports "unsupported". Missing APIs (Safari, Firefox) mean no cap. Nothing is ever swapped mid-play: `setAttribute('src')` appears once (enforced by the validator).
2. **No blank / black hero.** The video becomes visible only on its first *presented* frame (`requestVideoFrameCallback`, or `playing` where absent) and only if `videoWidth > 0`; the poster stays underneath.
3. **Playback that goes wrong ends in the held still, not in a frozen frame.** A stall (`waiting`) of 3 s, or > 40 % dropped frames at 4.5 s, pauses the video and takes the existing static path (held base, then the priority payoff). Reasons are recorded on `data-hero-reason` / `data-hero-tier` / `data-hero-codec`.
4. `play()` rejections are told apart (`NotAllowedError` → `autoplay-blocked`, anything else → `encode-error`).

Resilience matrix (`evidence/mer216/phase3/hero_scenarios_after.json` vs `…_baseline.json`; real Chrome, `localhost`, hero given 8–30 s, luminance sampled 5–7 times; **0 blank samples in any scenario**):

| Scenario | New tree | Baseline (`f4f1d4d`) |
| --- | --- | --- |
| 1920 @1x, fast | `held`, md WebM, 2,920,385 B, 1 request | `held`, 2,967,086 B |
| WebM unsupported | md MP4, 3,584,878 B, **1 request** | 4,260,468 B in **3 requests** (tail range for `moov`) |
| WebM unsupported, 1280 | sm MP4, 2,062,118 B | n/a (single 1920) |
| downlink 4 Mbps | md, `held` | not measured separately (DSL 4 Mbps class in §4) |
| downlink 1.6 Mbps | **still**, 0 video bytes (`slow-network`) | starts, stalls, `static / stalled` only after the 15 s watchdog having fetched 706 KB |
| downlink 1.0 Mbps, effectiveType 3g, Save-Data, reduced motion, 375 @3x | still, **0 video bytes**, reason recorded | (3g, Save-Data, reduced motion, phone already static) |
| decoder: 1920 not smooth | sm WebM (1.57 MiB) | n/a |
| `mediaCapabilities` absent / never answers | md, plays, no delay | n/a |
| encode 404 | `static / encode-error` | `static`, mislabelled `autoplay-blocked` |
| autoplay refused | `static / autoplay-blocked` | same |
| decoder reports `playing`, paints nothing (`videoWidth` 0) | `static / no-video-frame` | stays `playing` (video shown over the poster) |
| 60 % dropped frames | `static / dropped-frames` | plays on |
| network collapses mid-play (server throttled to 15 kB/s after 400 kB) | `static / buffering` after 3 s, payoff on the held base, 843,776 B fetched | **stays `playing` frozen** at 20 s, payoff never shown |
| no JavaScript | poster is the hero (`hero-opening-1600.webp` / held poster on phone), 0 video requests | same |

The 1.5× margin is measured, not assumed: with a 1.2× margin a 1.6 Mbit/s link was admitted to the 1280 tier and stalled mid-play; at 1.5× it is served the still and never downloads video it cannot play. Note for reviewers: Chrome evidently does not sample `localhost` for its network estimator and reports a conservative default (`4g`, 1.45 Mbit/s) on a cold profile, so the measurements that need a realistic hint inject one (`navigator.connection` = 4g / 10 Mbit/s); a real visitor has a measured value.

**Act 03 layer switching and the inspection aid.** Unchanged. A bounded predecode of the three Act 3 layers and the three inspection layers (`img.decode()` in idle slots when the stage nears the viewport) was implemented and measured and **was removed**: with 3 runs per class the worst first-switch frame gap at 4× CPU throttling was 30–42 ms with it versus 12–24 ms without (`phase4/layer_switch_predecode_experiment_run*.json` vs `layer_switch_baseline_run*.json`), i.e. no benefit and a possible cost, so it is not shipped. The final tree's switching, wipe drag and radios are therefore the baseline code path, and measure the same within noise: worst first-switch frame gap 12–42 ms (baseline) vs 12–30 ms (final) across 4× / 6× CPU throttling and 390 @3x (`layer_switch_after_run*.json`; the headless compositor ticks in 6.25 ms steps). Switching is compositor-only (opacity / visibility) and never touches a raster.

Validators changed with the contract: `scripts/validate_site.py` now requires the tier records, hash-named files, faststart MP4s, a ladder in the markup that equals the records, the 1920 tier as the bare fallback, per-tier ceilings, and the runtime tokens above; `scripts/negative_tests_mer216.py` proves 16 / 16 deliberate regressions are caught.

## 4. Phase 4 — terminal browser / 4K-HiDPI acceptance: `PHASE_4_PASS`

Environment: Chrome (headless, `--headless=new`) over CDP on the CTO workstation (Windows 11, i9-14900HX, RTX 4070 laptop GPU), with `Emulation.setDeviceMetricsOverride` for viewport and DPR, CPU throttling for slow-device classes. Real **physical** phones and a physical 4K panel were **not available**: 375 / 390 @3x are emulated, and 3840 × 2160 / 2560 @1.5x / 1920 @2x emulate the three 4K scaling modes. `serve()` mirrors `vercel.json`'s immutable `/assets/` cache and supports Range requests. Tooling: `evidence/mer216/tools/` (never a site dependency).

| Class | Overflow (7 routes) | Broken img | Console errors | Hero (state / tier / codec) | Home image bytes after vs baseline |
| --- | --- | --- | --- | --- | --- |
| 375 @3x | 0 | 0 | 0 | still (small screen) | 8,489,455 vs 8,489,455 |
| 768 @2x | 0 | 0 | 0 | still (small screen) | 9,411,884 vs 9,411,884 |
| 1024 @1x | 0 | 0 | 0 | held / sm / WebM | 4,483,110 vs 4,483,110 |
| 1024 @2x | 0 | 0 | 0 | held / md / WebM | 10,679,214 vs 10,679,214 |
| 1440 @1x | 0 | 0 | 0 | held / md / WebM | 4,208,176 vs 4,208,176 |
| 1440 @2x | 0 | 0 | 0 | held / md / WebM | 9,970,178 vs 9,970,178 |
| 1920 @1x | 0 | 0 | 0 | held / md / WebM | 4,208,176 vs 4,208,176 |
| 1920 @2x (4K @200 %) | 0 | 0 | 0 | held / md / WebM | 9,970,178 vs 9,970,178 |
| 2560 @1.5x (4K @150 %) | 0 | 0 | 0 | held / md / WebM | 7,546,808 vs 7,546,808 |
| 3840 @1x (4K @100 %) | 0 | 0 | 0 | held / md / WebM | 4,208,176 vs 4,208,176 |

(`evidence/mer216/phase4/browser_audit_after.json` / `…_baseline.json`: 7 routes × 10 classes each, overflow, broken images, console and unhandled-rejection errors, layout shift, image selection per `<img>`.)

- **Selected source and bytes.** Image bytes are identical to the baseline in every class (the analytical markup is unchanged). Hero bytes: 1280-class laptops (≤ 1366 CSS px) 1,646,824 B vs 2,967,391 B (**−44 %**); all wider classes 2,920,690 B vs 2,967,391 B (−1.6 %) at +6 VMAF; the MP4 path 3,584,878 B in one request vs 4,260,468 B in three.
- **Decoded vs rendered dimensions; no analytical upscale.** §1 table: in every class the selected rung is at least the device-pixel demand (rung ≥ demand; the closest is 897 px of demand served by the 900 rung), and none is a stretched governed raster. The hero video is a render, labelled as one (`Rendered orbital sequence — not sensor imagery`), and 1920 / 1280 are not enlargements of the 2304 master.
- **Startup / poster / held-state continuity.** Unchanged markup and logic: opening poster → video → hold → relief rise → Terrain → THM-01 → ALT-01 → priority (`data-hero-layer` ends `priority` in every desktop class); static states take the held base first.
- **Playback smoothness** (`phase4/hero_playback_after.json` vs `…_baseline.json`, 16 s hold): 276 / 276 frames presented with 0 dropped in 1440 / 1920 / 3840 and 2560 @1.5x classes (1 dropped at 2560 and at 1920 with 6× CPU throttle); 1 dropped at 1366, 6 at 1280 (decoder warm-up, same 6 in the baseline). 1440 @2x with 4× CPU throttle: 0 dropped (baseline 4). 1920 @1x with 6× CPU throttle: completes with 1 dropped (baseline: still at frame 210 after 16 s, 12 dropped). DSL 4 Mbps: 188 frames and 8 dropped at 16 s, same as the baseline's 181 / 8 (the transfer, not the decoder, is the limit). Slow 4G (1.6 Mbit/s): still, versus the baseline stuck at frame 48 with 5 dropped.
- **Act 03 smoothness, compare interaction:** §3. Evidence radios (3), inspection pairs (3) and the wipe (0 → 100 %) verified in EN and TR (`phase4/interaction_checks_after.json`): all radios checked, visible layers loaded, `--pos` follows the range at 0 / 25 / 50 / 75 / 100 %.
- **Late-media layout shift:** the homepage measured CLS **0 in 6 / 6 runs on both trees** at 3840 × 2160 (`phase4/cls_repeat_3840.json`). Whole-site audit values (all routes, one run) stay ≤ 0.034 in both trees and vary run to run within that band; none is attributable to this change (the hero is the only touched surface and it is on the homepage).
- **Cache / preload / content type:** assets are served with `Cache-Control: public, max-age=31536000, immutable` (mirroring `vercel.json`) and the new hero files are hash-named; content types `video/webm`, `video/mp4`; the LCP poster preload and `<picture>` are untouched; video is never preloaded and is requested once.
- **No palette / mask / NoData drift:** Phase 1 independent re-derivation (§1) on the final tree; `validate_site.py` recomputes LUTs and checksums.
- **Navigation, EN / TR, reduced motion, no-JS:** desktop nav order and mobile menu (5 links, `aria-expanded`), `lang` and h1 switch in EN and TR, reduced motion → still with 0 video bytes, no-JS → poster visible with 0 video requests.
- **Bounded Phase 4 fixes applied:** codec / tier thresholds, the downlink margin (1.2× → 1.5×, §3), the 1.2 s capability timeout, asset naming (hash), and `faststart`. No design, copy or science semantics changed.

## 5. Changed-file inventory

| Phase | Path | Change |
| --- | --- | --- |
| 1 | — | none (verification only); tooling under `evidence/mer216/tools/` and results under `evidence/mer216/phase1/` |
| 2 | `hero/scripts/encode_responsive_media.py` | new: master verification, tier encodes, fidelity bench |
| 2 | `assets/hero/orbgss-hero-1280-21da1079.webm`, `…-164c957f.mp4`, `orbgss-hero-1920-ca741624.webm`, `…-c8db4a5a.mp4` | new |
| 2 | `assets/hero/orbgss-hero.webm`, `orbgss-hero.mp4` | removed (superseded; no longer referenced; history keeps them) |
| 2 | `hero/evidence/responsive_media.json` | new record (FFmpeg version, arguments, hashes, fidelity) |
| 2 | `hero/README.md`, `hero/config/lane.json` | ladder documented; integration gate re-opened for MER-216 (see §6) |
| 2/3 | `assets/imagery/sources.json` | `web_005.hero_media`: tier records replace the single pair |
| 3 | `index.html` | `data-hero-tiers`; bare `data-hero-webm` / `data-hero-mp4` = 1920 tier |
| 3 | `script.js` | adaptive tier / codec choice, capability and network signals, show-after-first-frame, stall / dropped-frame fallback |
| 3 | `scripts/validate_site.py`, `scripts/negative_tests_mer216.py` | ladder + runtime contract checks; 16 negative cases |
| 4 | `evidence/mer216/**`, `tasks/MER-216_EVIDENCE.md`, `STATUS.md`, `CLAUDE.md` | evidence and canonical-doc reconciliation |

Not changed: `styles.css`, every other route, the posters, held frame, drape and rise states, all analytical rasters and derivatives, `vercel.json`, the Landsat context imagery.

## 6. Decisions and deviations the reviewer should look at

1. **FFmpeg instead of Blender's encoder** for the new ladder (`hero/README.md`, MER-216 section). It is local production tooling like Blender; the exact build (`7.1-essentials_build-www.gyan.dev`, obtained as the `imageio-ffmpeg` wheel into a scratch venv) and arguments are recorded. The earlier accepted files came from Blender and are replaced, not edited.
2. **`hero/config/lane.json`** said "no hero file may change again on this lane". MER-216 explicitly authorizes Phase 2 hero media hardening, so `phase`, `lane`, `branch`, `integration_task` and `integration_authority` now name MER-216 (the previous text is preserved inside `integration_task`). The write surface and baseline pin are unchanged; `validate_hero.py` is 420 / 0.
3. **No 2304 tier and no 4K analytical derivative** — measured, not assumed (§1, §2). Both can be added later without Science re-entry if Product wants them; the binding envelope would need Product's revision for the video.
4. **Old encodes deleted.** `orbgss-hero.webm|mp4` had no other consumer (`grep` clean; `hero/evidence/production_media.json` is kept unchanged as the historical Blender record).
5. **Evidence limitations:** headless Chrome, no physical phone or 4K panel, no Safari / Firefox engine (their code paths — no `connection`, no `mediaCapabilities`, no `requestVideoFrameCallback` on older versions — are covered by the "absent" scenarios, not by those engines). Production Vercel behaviour (HTTP/2, Range, brotli) is not exercised; nothing was deployed.
6. **Pre-existing, not touched:** untracked `AGENTS.md` in the workspace; `STATUS.md` open gates (`main` publication, information architecture, `CONTACT_RELEASE_GATE`).

## 7. Verification commands and results (final tree)

| Command | Result |
| --- | --- |
| `py -3.14 scripts/validate_site.py` | PASS, 0 warnings |
| `py -3.14 hero/scripts/validate_hero.py` | 420 checks, 0 failed |
| `py -3.14 scripts/negative_tests_web005.py` | 72 / 72 caught, restored tree identical |
| `py -3.14 scripts/negative_tests_web005b.py` | 55 / 55 caught |
| `py -3.14 scripts/negative_tests_web005c.py` | 18 / 18 caught |
| `py -3.14 scripts/negative_tests_mer216.py` | 16 / 16 caught |
| `node --check script.js` | exit 0 |
| `scripts/build_web005b_presentation.py` (pinned venv) | 0 byte changes vs the committed derivatives |
| `evidence/mer216/tools/verify_phase1_independent.py` | PASS, 0 differing pixels |
| `hero/scripts/encode_responsive_media.py --bench` | 4 / 4 encodes within their ceilings, 276 frames each, MP4s faststart |
