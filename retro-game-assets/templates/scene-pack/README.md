# Layered PNG scene pack template

Copy this folder into `working/dashboard/<scene_id>/v001/` (or working/game) before editing. This template contains no images; referenced filenames are placeholders, not ready runtime assets. Rename scene.template.json to scene.json in the working copy and fill its dimensions and provenance.

- `base/base-scene.png`: fixed opaque background containing sky, skyline, road, palms, car and static reflections.
- `overlays/frame-01.png` through `frame-04.png`: transparent overlays showing the lights, streaks, twinkles or reflection changes for that frame only.
- All five PNGs use the same canvas size, registration/origin and sRGB colour space. Preserve alpha; do not flatten overlays or add the base image to them.
- Composite base + ONE current overlay. Replace the overlay every 140 ms; never accumulate frames. Pause while hidden and show the base for reduced motion.
- The 140 ms setting is this template's starting value, not a requirement for every animation.
- `editable/`: portable editable master copies/exports; also keep the final durable project in sources/editable or an archived package.
- `previews/`: small contact sheet and looping preview. `audio/`: optional separately documented audio.
- `metadata/`: provenance, version notes, canvas dimensions and licence information.

When ready, archive the complete package ZIP with --category scenes (to keep the scene together) or packages (to preserve an incoming original). Ingest/promote each runtime PNG separately, then include all five printed asset IDs in one sync command. The consumer lock contains the exact hashed runtime filenames: map base and overlay order to those filenames explicitly in the application's scene definition. This descriptive template is not an automatic loader and the pipeline does not yet export a scene pack as one atomic asset. Scene/shader/application code and scene.json require normal reviewed integration.
