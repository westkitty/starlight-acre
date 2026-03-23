# Starlight Acre Asset Manifest

This manifest lists every asset generated for the startup pack. All assets use a Game Boy Advance / SNES pixel art aesthetic.

## Branding
- **starlight_acre_logo.svg**: Vector source for the main logo.
- **starlight_acre_emblem.svg**: Vector source for the compact emblem.
- **starlight_acre_emblem.png**: Compact emblem for small use.
- **starlight_acre_title_screen.png**: Main title screen illustration.
- **starlight_acre_banner_1280x640.png**: Documentation banner.
- **starlight_acre_app_icon_1024.png**: High-resolution app icon.

## Sprites
- **sprites/player/player_sheet.png**: Character sprite sheet. 
    - Row 1: Idle (4 frames)
    - Row 2: Walk (6 frames)
    - Row 3: Jump/Fall/Land (3 frames)
    - Row 4: Interact (2 frames)
- **sprites/player/player_preview.png**: High-quality portrait for documentation.
- **sprites/crops/wisdom_fruit_states.png**: 4 states of Wisdom Fruit in a planter tray (Empty, Planted, Growing, Ready).
- **sprites/crops/wisdom_fruit_preview.png**: Detailed "Ready" state preview.
- **sprites/terminals/terminals.png**: Repair and Replenish terminal visuals.

## UI
- **ui/icons/hud_icons.png**: Resource icons (Water, Nutrient, Power, Wisdom Fruit, Interaction Prompt). 16x16 pixels.

## Environment
- **backgrounds/greenhouse_sector_bg.png**: Main Greenhouse background (1920x1080 style).
- **tilesets/greenhouse_tiles.png**: GBA-style tileset and props (Floor, Wall, Beam, Planter, Crate, Light, Vent).

## Effects
- **effects/pixel_art_effects.png**: VFX set (Harvest burst, Repair spark, Growth glow, Interaction ping).

## Integration Notes (Godot 4.x)
- **Import Settings**: For all pixel art, set `Import > Texture > Filter` to `Nearest` and `Compress > Mode` to `Lossless`.
- **9-Slice**: Use `StyleBoxTexture` for the UI panels if needed.
- **Sprite Animation**: Use `AnimatedSprite2D` or `AnimationPlayer` with the grid offsets provided in the sheets.
