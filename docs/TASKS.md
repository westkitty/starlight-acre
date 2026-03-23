# Starlight Acre — Tasks

## Immediate (Phase 2 Start)

- [ ] Replace player ColorRect with `player_sheet.png` sprite (32×48px, AnimatedSprite2D)
- [ ] Connect player animation states to movement code
- [ ] Replace CropPlot ColorRect with `wisdom_fruit_states.png` (32×32px, 4 frames)
- [ ] Replace terminal ColorRects with `terminals.png` slices (32×64px)
- [ ] Replace HUD icons with `hud_icons.png` sprites (16×16px)
- [ ] Populate greenhouse TileMapLayer with `greenhouse_tiles.png`
- [ ] Add background: `backgrounds/greenhouse_sector_bg.png` (1920×1080)
- [ ] Set all pixel art imports to Filter: Nearest, Compress: Lossless

## Next Milestone (Phase 2 Complete)

- [ ] Gardener drone: Node2D agent, patrol area, tend and harvest tasks
- [ ] Trickster Vine: second crop with unpredictable growth speed
- [ ] Room transition: door trigger area, second sector scene
- [ ] Dexter the Stinkweasel: docking event, trade UI stub
- [ ] Save/load: JSON serialization of FarmingManager + CropPlot states + player position
- [ ] GpuParticles2D: growth_glow effect over READY crop state

## Short-Term Roadmap

| Phase | Status | Goal |
|-------|--------|------|
| Phase 1 | ✅ Complete | Runnable vertical slice |
| Phase 2 | 🔲 Next | Pixel art + gardener drone |
| Phase 3 | 🔲 Future | Second sector + room transitions |
| Phase 4 | 🔲 Future | Dexter vendor + progression unlock |
| Phase 5 | 🔲 Future | Polish, audio, save/load |

## Known Blockers

None currently. Phase 1 is complete and the codebase is in a clean state.

## Prioritized Checklist (Phase 2 Entry)

1. **Asset import setup** — Configure Godot import settings for all pixel art
2. **Player sprite** — Most visible win; proves the art direction is working
3. **Crop sprites** — Second most visible; the crop lifecycle needs its mythic look
4. **Background + tileset** — Sets the atmospheric tone
5. **Gardener drone** — First agent; core to the game's identity beyond pure platformer
6. **Trickster Vine** — Second crop; proves the crop system is extensible
7. **Room transitions** — Unlocks spatial exploration
8. **Dexter** — Narrative and economy hook
9. **Save/load** — Makes the game retainable

## Deferred (Post-Phase 2)

- Audio: synthetic ambience, station hum, harvest feedback sounds
- Station voice: tutorial overlay, narrative flavor text
- Parallax background layers (background is single composite in Phase 1/2)
- Normal maps (not planned — 16-bit aesthetic relies on baked shading)
- Additional character variants (only Caretaker in current asset pack)
- Alternate crop sprites beyond Wisdom Fruit (Trickster Vine needs new art)
