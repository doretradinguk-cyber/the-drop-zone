# Nightmare Frequency — Code Rain Overlay

Reusable activation effect for **Neo-Gothic Glitch / Retro Wave Game**.

## Behaviour lock

This effect is **OFF during normal reality**. It activates only when the Nightmare Frequency is present or being broadcast. It can appear as a full-screen/background corruption pass or be masked to specific world surfaces such as station signs, monitors, windows, sky areas, tunnel walls, holograms and corrupted props.

## Visual layers

- falling numerals / binary-like streams
- druid/rune-like glyphs
- Egyptian-inspired symbols
- Mayan-like numeral/glyph motifs
- tiny text fragments
- odd emoji corruption
- cyan, magenta, violet and acid-green signal glow
- scanlines, pulses and light flicker

## Required frame files

Place these generated transparent PNGs in `assets/`:

- `nightmare-rain-01.png`
- `nightmare-rain-02.png`
- `nightmare-rain-03.png`
- `nightmare-rain-04.png`

The included HTML/CSS/JS cycles the four frames and provides activation, intensity and speed controls.

## Recommended runtime use

For the browser test, 180–260 ms per frame gives an unstable signal pulse. For Godot, keep this PNG sequence for stylised bursts/sign corruption while using scrolling shaders/particles for continuous rain. Apply masks to signs and background regions so the effect can appear locally instead of always covering the complete screen.

## Source package

The four PNG originals and ready-to-test ZIP were generated in the ChatGPT project session on 4 October 2026. Add the binary frame files through GitHub Desktop / Git LFS so the repository keeps the original image bytes.
