# Starlight Acre - Tasks

## Current Branch Status - Build Plan Implementation

Implemented on branch `codex/full-build-plan-implementation`:

- [x] Replace terminal ColorRects with `terminals.png` slices.
- [x] Replace HUD text labels with icon/value rows using `hud_icons.png`.
- [x] Add READY-state crop glow using `pixel_art_effects.png`.
- [x] Add configurable CropPlot definitions.
- [x] Add Trickster Vine as the second crop with erratic growth behavior.
- [x] Add `GameState` autoload for room transitions and save/load state.
- [x] Add save/load terminals backed by JSON at `user://save.json`.
- [x] Add a second sector: `ArchiveLibrary.tscn`.
- [x] Add door transitions between Greenhouse and Archive Library.
- [x] Add Dexter trade stub: spend 2 Wisdom Fruit to restore power, water, and nutrients.

## Validation Still Required

- [ ] Open the project in Godot 4.3 and confirm all edited `.tscn` files import cleanly.
- [ ] Run the main scene from `project.godot`.
- [ ] Smoke test movement, crop planting, tending, harvesting, terminals, HUD updates, drone behavior, Trickster Vine, save/load, and room transitions.
- [ ] Confirm Dexter trade handles both enough-resource and not-enough-resource cases cleanly.
- [ ] Inspect HUD icon sizing and prompt placement in the running viewport.
- [ ] Confirm `user://save.json` load restores resource, crop, scene, and player-position state.

## Known Blockers

- TileMapLayer tile placement still requires the Godot editor. The TileSet is configured, but this branch does not hand-author tile cell data.
- The implementation has not been runtime-verified in this environment because Godot is unavailable here.
- Trickster Vine uses the Wisdom Fruit sprite with green tint until dedicated crop art exists.
- Dexter is an interactable trade stub, not a full shop UI or rotating inventory.

## Next Godot Editor Pass

1. Open Godot 4.3 and import `project.godot`.
2. Run `scenes/world/GreenhouseSector.tscn`.
3. Paint the Greenhouse TileMapLayer using `assets/tilesets/greenhouse_tiles.png`.
4. Test Greenhouse -> Archive Library -> Greenhouse transition.
5. Test save, quit/reload, and load from both sectors.
6. Record results in `Starlight_Acre_bible.md` and update this checklist.
