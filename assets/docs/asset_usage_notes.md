# Asset Usage Notes & Integration Guide

## Player Character (`player_sheet.png`)
- **Frame Size**: 32x48 pixels (recommended for Godot `SpriteFrames` or `AnimationPlayer`).
- **Animations**:
    - **Idle**: Frames 0-3 (looping).
    - **Walk**: Frames 4-9 (looping).
    - **Jump**: Frame 10.
    - **Fall**: Frame 11.
    - **Land**: Frame 12.
    - **Interact**: Frames 13-14 (one-shot).

## Wisdom Fruit (`wisdom_fruit_states.png`)
- **Slicing**: 32x32 pixels per state.
- **States**: 
    - 0: Empty (Planter only)
    - 1: Seedling
    - 2: Growing
    - 3: Ready (Glowing)
- **Tip**: Add a `GpuParticles2D` node over the "Ready" state using the `growth_glow` effect for extra polish.

## Terminals (`terminals.png`)
- **Slicing**: 32x64 pixels.
- **Usage**: Both terminals are static but have "active" regions. You can overlay the `terminal_active_glow.png` (if generated) or use a `CanvasItem` modulate to suggest activity.

## Tileset (`greenhouse_tiles.png`)
- **Cell Size**: 16x16 or 32x32.
- **9-Slice**: The floor and wall panels are designed for 3x3 9-slice behavior. Ensure you set the `Region` correctly in the Godot `TextureRect` or `Panel`.

## UI & Icons (`hud_icons.png`)
- **Slicing**: 16x16 pixels.
- **Interaction**: The "E" icon should be placed in its own `Sprite2D` and float above interactable objects (Terminals, Crops) with a small sine-wave vertical offset.

## Background (`greenhouse_sector_bg.png`)
- **Parallax**: If using `ParallaxBackground`, set this as the furthest layer. The scale is 1920x1080, but it works well down to 1280x720.
