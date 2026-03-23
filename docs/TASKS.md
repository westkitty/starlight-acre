# Starlight Acre — Tasks

## Immediate (Phase 2 — remaining)

- [x] Replace player ColorRect with `player_sheet.png` sprite (32×48px, AnimatedSprite2D)
- [x] Connect player animation states to movement code
- [x] Replace CropPlot ColorRect with `wisdom_fruit_states.png` (32×32px, 4 frames)
- [x] Add background: `backgrounds/greenhouse_sector_bg.png` (1920×1080)
- [x] Set all pixel art imports to Filter: Nearest (via project.godot global setting)
- [x] Gardener drone: Node2D agent, patrol area, tend and harvest tasks
- [ ] Replace terminal ColorRects with `terminals.png` slices (32×64px)
- [ ] Replace HUD text labels with `hud_icons.png` sprites (16×16px)
- [ ] Populate greenhouse TileMapLayer with actual tiles (requires editor — TileSet configured, no tiles placed)

## Next Milestone (Phase 2 Complete → Phase 3)

- [ ] Trickster Vine: second crop with unpredictable growth speed
- [ ] Room transition: door trigger area, second sector scene
- [ ] Dexter the Stinkweasel: docking event, trade UI stub
- [ ] Save/load: JSON serialization of FarmingManager + CropPlot states + player position
- [ ] GpuParticles2D: growth_glow effect over READY crop state

## Short-Term Roadmap

| Phase | Status | Goal |
|-------|--------|------|
| Phase 1 | ✅ Complete | Runnable vertical slice |
| Phase 2 | 🔄 In Progress | Pixel art + gardener drone |
| Phase 3 | 🔲 Future | Second sector + room transitions |
| Phase 4 | 🔲 Future | Dexter vendor + progression unlock |
| Phase 5 | 🔲 Future | Polish, audio, save/load |

## Known Blockers

- TileMapLayer tile placement requires the Godot editor open. The TileSet is configured (`greenhouse_tiles.png`, 16×16 cells) but no tiles have been painted.

## Remaining Phase 2 Checklist

1. **Terminal sprites** — Replace orange/blue ColorRect placeholders with `terminals.png` (32×64px; Repair = left half, Replenish = right half)
2. **HUD icons** — Replace text-only labels with icon+label combos using `hud_icons.png` (16×16px)
3. **Tile painting** — Open Godot editor, select TileMapLayer_Background, paint floor/wall/beam tiles
4. **Trickster Vine** — Second crop with distinct behavior; requires new CropDefinition + CropPlot variant
5. **GpuParticles2D** — growth_glow effect on READY crop state using `effects/pixel_art_effects.png`

## Deferred (Post-Phase 2)

- Audio: synthetic ambience, station hum, harvest feedback sounds
- Station voice: tutorial overlay, narrative flavor text
- Parallax background layers (background is single composite in Phase 1/2)
- Normal maps (not planned — 16-bit aesthetic relies on baked shading)
- Additional character variants (only Caretaker in current asset pack)
- Alternate crop sprites beyond Wisdom Fruit (Trickster Vine needs new art)
