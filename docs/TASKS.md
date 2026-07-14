# Starlight Acre - Tasks

## Current Branch Status - Build Plan Implementation

Implemented on branch `codex/full-build-plan-implementation`:

- [x] Replace terminal ColorRects with `terminals.png` slices.
- [x] Replace HUD text labels with icon/value rows using `hud_icons.png`.
- [x] Add READY-state crop glow using `pixel_art_effects.png`.
- [x] Add configurable CropPlot definitions.
- [x] Add Trickster Vine as the second crop with bounded erratic behavior.
- [x] Add `GameState` autoload for room transitions, session state, and save/load state.
- [x] Add save/load terminals backed by JSON at `user://save.json`.
- [x] Add a second sector: `ArchiveLibrary.tscn`.
- [x] Add door transitions between Greenhouse and Archive Library.
- [x] Preserve resources and per-scene crop states across room transitions.
- [x] Add Dexter trade stub: spend 2 Wisdom Fruit to restore power, water, and nutrients.
- [x] Add short HUD status feedback for save/load, insufficient resources, harvests, and trades.
- [x] Add text-authored `TileVisualPass` fallback in GreenhouseSector using `greenhouse_tiles.png`.
- [x] Add `tools/validation/static_scene_audit.py` for resource/path checks.
- [x] Add `tools/validation/godot_smoke_test.gd` for Godot 4.3 headless scene smoke checks.
- [x] Add `docs/VALIDATION.md` runbook.

## Validation Still Required

- [ ] Run `python3 tools/validation/static_scene_audit.py` from a full checkout.
- [ ] Open the project in Godot 4.3 and confirm all edited `.tscn` files import cleanly.
- [ ] Run `godot4 --headless --path . --script tools/validation/godot_smoke_test.gd`.
- [ ] Run the main scene from `project.godot`.
- [ ] Smoke test movement, crop planting, tending, harvesting, terminals, HUD updates, drone behavior, Trickster Vine, save/load, and room transitions.
- [ ] Plant crops in the Greenhouse, enter Archive Library, return, and confirm Greenhouse crop/resource state persists.
- [ ] Plant or harvest in Archive Library, return to Greenhouse, revisit Archive, and confirm Archive crop state persists.
- [ ] Confirm Dexter trade handles enough-resource and not-enough-resource cases with visible HUD feedback.
- [ ] Confirm failed load with no save file shows visible HUD feedback.
- [ ] Inspect HUD icon sizing, status-message placement, prompt placement, and `TileVisualPass` readability in the running viewport.
- [ ] Confirm `user://save.json` restores resource, per-scene crop, scene, and player-position state.

## Known Blockers

- The implementation has not been runtime-verified in this environment because Godot is unavailable here.
- The text-authored `TileVisualPass` is a fallback, not a full editor-authored TileMapLayer collision pass.
- Trickster Vine uses the Wisdom Fruit sprite with green tint until dedicated crop art exists.
- Dexter is an interactable trade stub, not a full shop UI or rotating inventory.

## Next Godot Editor Pass

1. Open Godot 4.3 and import `project.godot`.
2. Run the static audit and Godot headless smoke test from `docs/VALIDATION.md`.
3. Run `scenes/world/GreenhouseSector.tscn`.
4. Inspect the `TileVisualPass`; keep it, revise it, or replace it with editor-authored TileMapLayer painting.
5. Do not remove StaticBody2D collision until TileMapLayer collision is configured and tested.
6. Test Greenhouse -> Archive Library -> Greenhouse transition with crops planted before and after transition.
7. Test save, quit/reload, and load from both sectors.
8. Confirm HUD status messages do not overlap core UI.
9. Record results in `Starlight_Acre_bible.md` and update this checklist.
