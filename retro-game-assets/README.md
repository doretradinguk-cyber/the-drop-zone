# Retro game assets

A dedicated source and export collection for the first-person retrowave game and Seumas & Lewis dashboard. Originals and editable masters stay here; only selected, prepared exports enter the consuming repositories. Existing root-level archives remain valid and are not moved.

## Where to put files

| Folder | What belongs here |
|---|---|
| `inbox/game/`, `inbox/dashboard/`, `inbox/shared/`, `inbox/packages/` | New unprocessed deliveries from GitHub Desktop |
| `sources/backgrounds/` | Static PNG art and layered background originals |
| `sources/scenes/` | Complete archived scene packs and their dependencies |
| `sources/textures/`, `sources/materials/`, `sources/hdri/` | Seamless textures, PBR maps, materials and environment lighting |
| `sources/models/` | Characters, environment pieces, props and weapons; retain linked files together |
| `sources/sprites/`, `sources/animations/`, `sources/vfx/` | Sprite art, frame sequences, sprite sheets, rigs, particles and overlays |
| `sources/ui/` | Game HUD, inventory, menus, icons and cursors |
| `sources/audio/` | Music, ambience, sound effects, foley, voices and editable stems |
| `sources/dashboard/` | Dashboard backgrounds, animations, buttons, tabs, cards, icons, branding and audio |
| `sources/editable/` | Durable Photoshop, Illustrator, After Effects and audio project masters |
| `sources/blueprints/`, `sources/text/`, `sources/fonts/`, `sources/references/` | Level plans, game design, dialogue, localisation, fonts and references |
| `archives/original-packages/` | Unmodified source ZIP/packages |
| `archives/superseded/` | Optional old unindexed deliveries; do not move indexed sources here (their paths are pinned) |
| `working/`, `staging/` | Ignored scratch edits and extracted files; never the sole copy of valuable work |
| `review/` | Contact sheets, preview videos and approval notes |
| `exports/game/`, `exports/dashboard/` | Pipeline-managed immutable prepared versions |
| `catalog/catalog.json` | Pipeline-managed source IDs, checksums, licences, tags and export versions |
| `metadata/` | Human-readable provenance, licence evidence and palette notes |
| `templates/` | Scene pack, asset record and button/tab state conventions |

The category subfolders are authoring/organisation guides. The pipeline archives each ingested item into its category as `<snake_case_name>_<hash>/<snake_case_filename>`. Use tags for subtypes such as buttons, tabs, voices or props. Do not manually move files once indexed. Keep linked scene/model folders inside one package; do not flatten their references.

## Our pipeline

1. **Drop:** copy originals to the correct inbox folder in your local clone. Include provenance/licence notes.
2. **Inspect and archive:** use the collection option below; ZIP extraction is inspected and source bytes remain unchanged.
3. **Edit:** use Adobe or other authoring tools. Keep durable masters in sources/editable, separate from optimised PNG/WebP/audio/GLB output. Record source/model/prompt where relevant; Adobe availability does not automatically establish a file's licence.
4. **Review:** confirm artwork, transparency, dimensions, animation order, audio levels/loops and target suitability. Save review notes.
5. **Prepare:** explicitly promote already-optimised files with a reviewed licence. The script does not perform optimisation or artwork approval.
6. **Select:** sync only chosen asset IDs to dashboard/game. Commit the resulting lock and use rehydrate on fresh checkouts.

Run from the **Drop Zone repository root**. `--collection` comes before the command. Paths supplied as file/project arguments remain relative to your current terminal directory, not the collection.

```powershell
# Check collection and archive a dashboard PNG.
python scripts/pipeline.py --collection retro-game-assets verify
python scripts/pipeline.py --collection retro-game-assets ingest "retro-game-assets/inbox/dashboard/base-scene.png" --category dashboard-backgrounds --licence "Original artwork" --tags scene base

# Preserve a source pack before inspecting a temporary extraction.
python scripts/pipeline.py --collection retro-game-assets ingest "retro-game-assets/inbox/packages/scene.zip" --category scenes
python scripts/pipeline.py --collection retro-game-assets unpack "retro-game-assets/inbox/packages/scene.zip"

# Replace ASSET_ID with the ID printed by ingest; prepare output in your editor first.
python scripts/pipeline.py --collection retro-game-assets promote ASSET_ID "retro-game-assets/working/dashboard/base-scene.webp" --target dashboard
python scripts/pipeline.py --collection retro-game-assets sync --target dashboard --project ../seumas-lewis-dashboard --ids ASSET_ID
python scripts/pipeline.py --collection retro-game-assets publish-catalog --project ../seumas-lewis-dashboard

# Restores the exact locked collection exports, not the latest versions.
python scripts/pipeline.py --collection retro-game-assets rehydrate --target dashboard --project ../seumas-lewis-dashboard
```

For game assets use `--target game --project ../retro-wave-game`. Supply all selected IDs together: sync replaces the selection lock, not merges it. Publishing a catalogue replaces the dashboard catalogue snapshot with this collection only. Mixing root/collection selections in one consumer lock is not supported; retain the current selection until all its required assets are prepared in the same collection. Running without --collection keeps the original root pipeline behaviour.

Runtime formats remain deliberately limited to self-contained images, audio, fonts and game GLB. SVG/JSON/shaders/material resources/code can be archived but need reviewed integration rather than automatic copying into the app. A PNG sequence requires all its frame IDs plus explicit ordering in the consumer; see templates/scene-pack.

## Naming, revisions and PNGs

- Use descriptive lower-case names: `game_corridor_wall_albedo_v001.png`, `dash_tab_assets_active_v001.png`, `sfx_door_open_01_v001.wav`.
- Preserve original incoming names/bytes inside original packages. Keep dependency paths intact.
- Keep PNGs with their purpose (background, sprite, UI, overlay), not one mixed PNG dump.
- Save revisions rather than overwriting approved masters. Prepared exports receive automatic v1, v2… directories and hashes.
- Add dimensions, alpha intent, palette, source and licence notes. For meshes record units/scale, pivot, dependencies, LODs and collision intent.
- For audio record sample rate, channels, duration, loop points, loudness notes and attribution. Keep original WAV/stems; prepare compressed runtime copies separately.

## Desktop and large files

Fetch/Pull this structure first in GitHub Desktop. Ensure `git lfs install` has been run before staging large files. Repository LFS rules cover images, meshes, audio, archives and common Adobe/native project formats, including uppercase extensions. Keep JSON, Markdown, SVG and shader source as reviewable text. Cloud Adobe projects should have a project URL in metadata plus a portable export; an online link alone is not an archive.

All folders are tracked with .gitkeep or README files so they appear after cloning. No artwork/audio has been generated, moved or imported in this structure commit. The catalogue is intentionally empty. Git LFS quotas and root repository visibility still apply.
