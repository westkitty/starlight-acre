# Starlight Acre — Tasks

## Immediate (Phase 2 — remaining)

- [x] Replace player ColorRect with `player_sheet.png` sprite (32×48px, AnimatedSprite2D)
- [x] Connect player animation states to movement code
- [x] Replace CropPlot ColorRect with `wisdom_fruit_states.png` sprite states (32×32px, 4 frames)
- [x] Add background: `backgrounds/greenhouse_sector_bg.png` (1920×1080)
- [x] Set all pixel art imports to Filter: Nearest (via project.godot global setting)
- [x] Gardener drone: Node2D agent, patrol area, tend and harvest tasks
- [x] Replace terminal ColorRects with `terminals.png` slices (32×64px)
- [x] Replace HUD text-only resource labels with `hud_icons.png` icon/value pairs (16×16px)
- [x] Add ready-crop glow effect using `effects/pixel_art_effects.png`
- [ ] Populate greenhouse TileMapLayer with actual tiles (requires editor — TileSet configured, no tiles placed)

## Next Milestone (Phase 2 Complete → Phase 3)

- [ ] Trickster Vine: second crop with unpredictable growth speed
- [ ] Room transition: door trigger area, second sector scene
- [ ] Dexter the Stinkweasel: docking event, trade UI stub
- [ ] Save/load: JSON serialization of FarmingManager + CropPlot states + player position

## Short-Term Roadmap

| Phase | Status | Goal |
|-------|--------|------|
| Phase 1 | ✅ Complete | Runnable vertical slice |
| Phase 2 | 🔄 Mostly complete | Pixel art + gardener drone; tile painting remains |
| Phase 3 | 🔲 Future | Second sector + room transitions |
| Phase 4 | 🔲 Future | Dexter vendor + progression unlock |
| Phase 5 | 🔲 Future | Polish, audio, save/load |

## Known Blockers

- TileMapLayer tile placement requires the Godot editor open. The TileSet is configured (`greenhouse_tiles.png`, 16×16 cells) but no tiles have been painted.

## Remaining Phase 2 Checklist

1. **Tile painting** — Open Godot editor, select TileMapLayer_Background, paint floor/wall/beam tiles.
2. **Tile collision migration** — Keep StaticBody2D floor/walls until TileMapLayer collision is configured and tested.

## Recommended Path To Finished

1. Finish the Greenhouse presentation pass: tile painting, tile collision, terminal placement polish, and crop glow tuning.
2. Add one new mechanic at a time: Trickster Vine first, then room transition, then Dexter trade stub.
3. Make progression real: Wisdom Fruit should buy one station upgrade before more crops or rooms are added.
4. Add persistence only after the second sector exists, so save/load covers real state instead of a throwaway prototype.
5. Add audio and short feedback animations after mechanics stabilize.

## Deferred (Post-Phase 2)

- Audio: synthetic ambience, station hum, harvest feedback sounds
- Station voice: tutorial overlay, narrative flavor text
- Parallax background layers (background is single composite in Phase 1/2)
- Normal maps (not planned — 16-bit aesthetic relies on baked shading)
- Additional character variants (only Caretaker in current asset pack)
- Alternate crop sprites beyond Wisdom Fruit (Trickster Vine needs new art)
