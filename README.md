## 📦 The Drop Zone

This repository serves as the central asset ingestion library for our 3D retro wave horror game. 

## 🔄 AI Workflow Instructions
When an asset zip file is dropped here, the AI assistant (Opus/Sol) must execute the following vetting and organization pipeline:

1. **Unzip & Inspect:** Extract the archive and verify the file extensions.
2. **Standardize Naming:** Convert file names to `snake_case` (e.g., `neon_car_01.fbx`).
3. **Sort to Staging:** Move the verified assets out of the root folder and catalog them into the appropriate target directory below.

## 📁 Target Directory Structure
Move assets strictly into these directories. Create them if they do not exist:

*   `🎨 Textures/` — All `.png`, `.jpg`, and `.tga` files (neon signs, grids, VHS overlays).
*   `📐 Models/` — All `.fbx`, `.obj`, or `.gltf` 3D low-poly meshes.
*   `🎬 Shaders/` — Code files for visual effects, retro CRT filters, and material shaders.
*   `🎵 Audio/` — Ambient synths, synthwave tracks, and horror sound effects (`.wav`, `.mp3`).
*   `🌌 HDRI/` — 360-degree environment maps (`.hdr`, `.exr`) used for retrowave skyboxes.

## ⚠️ Git LFS Protection
Ensure all binary formats (`.fbx`, `.png`, `.wav`, `.hdr`, `.zip`) are tracked via Git Large File Storage (LFS) to keep the repository lightweight.
