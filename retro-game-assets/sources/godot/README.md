# Godot reference handoffs

Godot 4 is the game engine; active game code and resources are canonical in the retro-wave-game repository. This folder archives supplied examples, handoff packages and reference resources only.

- scenes: supplied `.tscn` scene examples or scene packages.
- scripts: reference `.gd` examples, archived with source/licence; do not execute unreviewed code.
- resources: reference `.tres` materials, environments and themes.
- shaders: reference `.gdshader`/`.gdshaderinc` code.
- addons: supplied editor plugin packages and licences.
- import-presets: reference importer/export configuration with credentials removed.

Keep relative dependencies intact inside scene/addon packages. Record engine version and dependencies in metadata/godot. Archive with `python scripts/pipeline.py --collection retro-game-assets ingest FILE --category godot-reference`; use tags for type. Pipeline IDs do not imply Godot import/readiness. Scene/script/shader integration remains a reviewed source change in the game repo; these formats are deliberately not added to automatic runtime promotion.

Production sources stay in their existing image/model/audio/Adobe folders. PNG/WebP/audio/GLB prepared exports go through the selected-asset pipeline; Godot then imports them from the game's assets/runtime folder. Never archive `.godot/` cache or export credentials.
