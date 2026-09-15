# OrbGSS cinematic hero production workspace

This folder is the isolated source workspace for `WEB-HERO-001` and later accepted hero-production phases.

Canonical authority: `docs/WEB_HERO_001_AUTHORITY.md` and the linked Drive CURRENT authority.

## Current state

`WEB-HERO-001` is pre-data. Build the scene, Earth, satellite, orbit, AOI geometry, scan system and continuous animatic here. Do not integrate the live homepage or fabricate scientific layers.

## Isolation rule

Until a later Product authority explicitly joins this work into `WEB-005`, hero production must not modify the public-site HTML/CSS/JS, proof imagery, deployment configuration or DNS.

## Expected production properties

- Blender Python/configuration is the reproducible source of scene truth.
- Earth is true 3D spherical geometry.
- AOI geometry conforms to the sphere and is configuration-driven.
- Scan beams/corner locks target the actual 3D footprint.
- Global-to-regional shots preserve continuous AOI registration and scale.
- External source assets are rights/provenance recorded in `hero/assets/manifest.json`.
- Large renders are local/ignored unless a task explicitly publishes bounded evidence.

See the task contracts under `tasks/WEB-HERO-001*.md` for exact phase scope and acceptance.