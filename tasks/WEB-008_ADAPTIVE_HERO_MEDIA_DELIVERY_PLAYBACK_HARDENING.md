# WEB-008 — Adaptive Hero Media Delivery & Playback Hardening

**Linear:** MER-144  
**State:** READY_FOR_CTO_APPROVAL — DO NOT START  
**Start dependency:** WEB-006 / MER-95 terminal public-launch acceptance  
**Accepted visual baseline:** WEB-005A hero @ 1135e7a7e0b0f6db6348dee139d505550d8ca8b9

## Outcome

Preserve the accepted hero appearance/choreography while delivering the highest perceptual quality each target device can play smoothly.

## Source authority

First resolve the highest-quality **accepted** hero master/render actually available. Do not infer that a 4K source exists from chat history. If a validated 4K/high-resolution master exists, bind it exactly. If not, do not manufacture a new master under this task.

## Delivery family

From the accepted master, benchmark a bounded set appropriate to the source:
- baseline desktop encode;
- higher-resolution / higher-bitrate desktop encode for large/high-DPR displays when source quality warrants it;
- lighter mobile / constrained-network encode when needed;
- browser-compatible WebM path plus MP4/H.264 fallback.

Codec/bitrate selection is based on:
- perceptual quality at real render size;
- decode cost;
- dropped frames;
- transfer size;
- browser support.

Do not optimize by file size alone.

## Loading/runtime behavior

- high-quality opening poster is the LCP/initial visual;
- full video does not block initial page paint;
- choose the source before playback from viewport/DPR plus safe reduced-data/network signals;
- do not swap source mid-playback because viewport changed;
- muted + playsinline;
- reduced-motion keeps the accepted poster/static path;
- failure/slow-start state remains a complete poster, never blank/black.

## Hard boundaries

No:
- Blender work;
- choreography/camera/satellite/scan changes;
- visual redesign;
- rerender solely to change delivery;
- fabricated high-resolution detail;
- universal 4K download to all clients.

## Acceptance

Capture representative browser evidence for mobile, 1440/1920 desktop and available 4K/high-DPR:
- selected source;
- transfer bytes;
- decoded dimensions;
- render dimensions/DPR;
- startup continuity;
- dropped-frame/playback evidence where available;
- reduced-motion path;
- fallback/content-type correctness.

The accepted hero must remain visually equivalent to WEB-005A.

**Terminal:** REVIEW_READY.