# Buttons, tabs and interface artwork

Use matching dimensions and anchor points across a component's states:

| Component | States |
|---|---|
| Button | default, hover (desktop), pressed, disabled, keyboard-focus |
| Tab | inactive, hover, active, disabled, keyboard-focus |
| Toggle | off, on, disabled, keyboard-focus |
| Card/panel | default, hover, selected, disabled |

Example: `dash_button_play_default_v001.png`, `dash_button_play_pressed_v001.png`.
Keep a vector/PSD master, transparent PNG preview/export, and colour/font notes. Prefer code-drawn labels over words baked into buttons, so labels remain accessible and localisable. Mark scalable borders/nine-slice regions in metadata; keep shared icon padding consistent. Touch interaction must work without hover. Component animation sequences belong in dashboard/animations; state artwork belongs in dashboard/ui.
