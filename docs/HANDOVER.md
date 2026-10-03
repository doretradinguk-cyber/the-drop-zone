# Studio foundation handover — 3 October 2026

## User direction

Build the dashboard first. Dashboard, game and Drop Zone are separate repositories. Each tool gets its own dashboard page. Existing Photo to Game remains separate; an audio tool comes later. The game direction is full first-person (option B) with neon illustrated horror visuals. The user will upload the old Dore Trading dashboard and symbol-rain background references to Drop Zone before final visual design.

## Delivered foundation

- `seumas-lewis-dashboard`, branch `feat/studio-foundation`: responsive six-page static dashboard, canvas symbol rain, original CSS portal illustration, emerald/violet settings, persisted launch URLs, searchable catalogue with JSON import, repository links and independent tool launch pages.
- `the-drop-zone`, branch `feat/asset-pipeline`: preserved original category directories plus inbox, archives, staging, sprites, animations, backgrounds, text, blueprints, fonts, references, previews and per-target exports. LFS tracking, ingestion, checksum catalogue, constrained ZIP extraction, explicit export preparation, selected sync, exact-version rehydration and metadata publishing.
- `retro-wave-game`, branch `feat/asset-contract`: asset lock and documented first-person scope only. No game implementation.

## Verification

Delivery recheck: all 10 pipeline tests pass. Browser smoke rerun is unavailable in this environment because the Playwright Chromium executable is missing; browser results below are the archived foundation verification, not a fresh rerun.

- 10 Python tests passed: deduplication, original preservation, selected copies, tamper rejection, missing exports, size budget, safe/unsafe ZIP handling, LFS pointer rejection, path containment, metadata-only publication and exact-version restore (some tests cover multiple checks).
- Headless Chromium 134: six routes at 1440px and 390px, no page overflow or JavaScript errors, preferences persist across reload, launch URLs open separate tabs, catalogue filtering and invalid input handling, HTML escaping, reduced-motion settings.
- Desktop and mobile screenshots visually reviewed.
- JavaScript syntax checks and empty-catalogue integrity checks passed.
- No Android native build, gameplay, real content assets, live photo-tool integration or external deployment has been tested.

## GitHub delivery status

The owning doretradinguk-cyber account is connected with write access. This delivery publishes the prepared foundation to main. The dashboard remains a local static app; no hosting deployment is included. The Photo to Game repository is doretradinguk-cyber/ai-photo-to-game-generator; its live launch URL still needs configuration.

## Next steps

1. Fetch and pull main in GitHub Desktop for the dashboard, Drop Zone and game repositories.
2. Receive old dashboard code/screenshots/background references in Drop Zone inbox. Archive and inspect, preserving original files and licences.
3. Iterate dashboard appearance from that reference; current portal is a provisional original foundation.
4. Set the actual photo-tool launch URL. Do not replace a running URL with a GitHub source URL.
5. Identify target PC/phone; then build the first-person game vertical slice separately.

## Runtime cautions

The dashboard does not upload/archive through its browser UI; use the Drop Zone Python scripts and GitHub Desktop. Prepared exports require manual optimisation in an editor. LFS uses account storage/bandwidth. Tool links need running/hosted addresses. Runtime caches are ignored, so builds must rehydrate their locks and package only the selected files. The development server is local-only by default.
