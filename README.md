# The Drop Zone

Central source archive for Seumas & Lewis. The dashboard, game and tools stay separate; only reviewed, selected runtime exports enter their builds.

## Retro game and dashboard collection

Use [`retro-game-assets/`](retro-game-assets/README.md) for the dedicated game/dashboard asset structure, editable masters, layered PNG scene template and collection-specific catalogue/exports. Run the existing script with `--collection retro-game-assets` before the command to select it. Existing root archives are preserved.

## Folder contract

| Folder | Purpose |
|---|---|
| `inbox/` | Drop new files here using Explorer/Finder in your GitHub Desktop clone |
| `🎨 Textures/` | Archived textures and layered artwork |
| `📐 Models/` | Archived meshes and models |
| `🎬 Shaders/` | Archived shader source; reviewed before manual integration |
| `🎵 Audio/` | Original sound, music and speech |
| `🌌 HDRI/` | Original environment maps |
| `Sprites/`, `Animations/`, `Backgrounds/` | Additional visual source categories |
| `Blueprints/`, `Text/`, `Fonts/`, `References/` | Plans, scripts, fonts and visual references |
| `Archives/` | Original ZIP and other source packages |
| `staging/` | Temporary extracted packages; ignored by Git |
| `exports/dashboard/`, `exports/game/` | Explicitly prepared runtime files, versioned and tracked with LFS |
| `catalog/catalog.json` | IDs, checksums, origin, licence, tags and export versions |
| `previews/` | Future small previews; not loaded automatically |

The five original emoji folders are preserved. Generated archive filenames use snake_case. ZIP contents retain their original relative paths during inspection so glTF/OBJ/material links are not silently broken. Keep linked model packages archived together; export self-contained GLB for the game.

## First-time setup (Windows + GitHub Desktop)

1. Clone all three repositories alongside each other.
2. Pull this structure **before adding large files**. GitHub Desktop includes Git LFS; in its repository terminal run `git lfs install`.
3. Install Python 3.10+ if unavailable (`python --version`; Windows may use `py` instead).
4. Put new files into `inbox/`. Add a note describing their source/licence and intended use. Existing old dashboard code can be archived as a ZIP plus screenshots.
5. Run the commands below from the Drop Zone directory. Inspect the Changes list in Desktop, commit and push.

This repository is public. Files pushed here are public too. LFS storage and bandwidth are limited by your GitHub account; LFS is not unlimited free storage. Ordinary GitHub files have a 100 MiB limit. For very large collections, retain this catalogue and move original payloads to dedicated object storage later.

## Pipeline commands

```powershell
# Archive a single source. Replace the example filenames with yours.
python scripts/pipeline.py ingest "inbox/neon-wall.png" --category textures --licence "Original Dore Trading artwork" --tags corridor emerald
# The command prints the asset ID. Use that exact ID below.

# Preserve a package, then safely inspect a copy. ZIP is never executed.
python scripts/pipeline.py ingest "inbox/old-dashboard.zip" --category packages
python scripts/pipeline.py unpack "inbox/old-dashboard.zip"

# Prepare a smaller image/audio/GLB in your editor, then register it.
python scripts/pipeline.py promote ASSET_ID "staging/neon-wall.webp" --target game
python scripts/pipeline.py sync --target game --project ../retro-wave-game --ids ASSET_ID

# Dashboard background exports use a separate target.
python scripts/pipeline.py promote ASSET_ID "staging/neon-wall.webp" --target dashboard
python scripts/pipeline.py sync --target dashboard --project ../seumas-lewis-dashboard --ids ASSET_ID

# Publish the metadata only; the dashboard can also load this JSON manually.
python scripts/pipeline.py publish-catalog --project ../seumas-lewis-dashboard
python scripts/pipeline.py verify
```

Ingest **copies** and verifies originals; it does not remove inbox files. After verifying the catalogue, remove the duplicate inbox copy before committing if you no longer need it there. SHA-256 deduplication prevents re-archiving identical files. Nothing automatically converts images, retopologises meshes, generates audio or approves licensing. Supply a reviewed licence when promoting an unreviewed source.

Archive active code as source only. The runtime pipeline intentionally rejects JS, HTML, shader code and arbitrary executables; integrate reviewed code through normal source changes. Images and model formats still need visual/content review. ZIP extraction rejects traversal, links, duplicate paths and excessive expansion; limits are in the script.

## Reproducible asset selection

`sync` copies the latest prepared version for each explicitly selected ID and writes `assets.lock.json` with exact paths, versions, sizes and hashes. Commit that lock with the consumer. Runtime payload folders are ignored by consumers to avoid duplicating the source archive in Git. A fresh checkout must rehydrate before packaging: `python scripts/pipeline.py rehydrate --target game --project ../retro-wave-game` (or `--target dashboard --project ../seumas-lewis-dashboard`). Run `git lfs pull` in Drop Zone first. Unlike sync, rehydrate restores the exact locked versions even after newer exports are prepared. Old unselected cached files remain locally; the current lock controls the selection, and release packaging must include **only files listed in the lock**, not the entire cache.

Default starting budgets: dashboard 8 MiB/file, 32 MiB selected total; game 32 MiB/file, 200 MiB selected total. These are adjustable development budgets, not measured performance guarantees.

Only one pipeline process should write the catalogue at a time. Pull first, run commands, review and commit. Resolve catalogue conflicts before further ingestion.

## Git LFS checks

```powershell
git lfs ls-files
python scripts/check_git_assets.py
```

The check reads Git's staged blobs, so stage changes in Desktop first. If a binary was committed without LFS, stop and fix tracking before pushing; this scaffold does not rewrite history.

Sources: https://docs.github.com/en/desktop/configuring-and-customizing-github-desktop/about-git-large-file-storage-and-github-desktop and https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage
