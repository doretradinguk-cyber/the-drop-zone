# Neon Mansion Firefly Room Pack

Purpose: master visual reference source for the 2D click-and-point mansion and the matching 3D Godot Neon Mansion.

## Storage policy
- Keep original Adobe Firefly export ZIPs as master archives.
- Extract working copies under `retro-game-assets/firefly/neon-mansion/extracted/`.
- Generate manifests under `retro-game-assets/firefly/neon-mansion/manifests/`.
- Do not edit master ZIPs in place.
- Do not copy the entire raw Firefly export into the Godot repo.

## Downstream use
The `neon-mansion` repo contains `tools/import-firefly-rooms.ps1`, which locates the latest relevant Firefly ZIP in the local Drop Zone, archives/extracts it, generates a CSV manifest and creates local room-reference copies for Codex/Godot.

## Visual benchmark
- dark teal / charcoal architecture
- near-black doors
- hot-magenta emissive trims
- acid-green / cyan indicators
- restrained low-poly / cel-shaded retro-horror materials
- Nightmare Frequency corruption as a separate dynamic layer

## Room mapping
The 3D project uses a working 30-room internal budget plus six exterior IDs. Mapping lives in `neon-mansion/design/room-catalog.json`.
