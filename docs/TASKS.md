# Starlight Acre — Tasks

## Verified in the 2026-09-17 upgrade pass

- [x] Recover legitimate Phase 2 terminal/HUD/VFX changes from reverted commit `defaecd`
- [x] Repair invalid PNG encoding across repository assets
- [x] Load project successfully in installed Godot 4.7.1
- [x] Data-drive Wisdom Fruit via `CropDefinition` + `.tres`
- [x] Give Wisdom Fruit real spend paths
- [x] Replace infinite free resupply with emergency/paid/upgrade economy
- [x] Add Efficient Grid research upgrade
- [x] Add Closed-Loop Hydroponics research upgrade
- [x] Make Gardener Drone travel to target crops before acting
- [x] Add Engineering Bay and bidirectional sector transitions
- [x] Add persistent GameState + JSON save/load
- [x] Add headless smoke test
- [x] Pass headless editor load, smoke test, and 120-frame main-scene run

## Next: visual truth pass

- [ ] Open in Godot editor and visually inspect every recovered sprite slice
- [ ] Correct player/crop/HUD/terminal slicing against the actual 640x640 generated source images
- [ ] Paint greenhouse TileMapLayer
- [ ] Add tested TileMap collision before removing StaticBody2D collision stubs
- [ ] Play the complete loop manually: plant -> drone/manual tend -> harvest -> paid resupply -> research -> Engineering -> return -> restart

## Next: Mythic Ecology

- [ ] Add a second crop only after crop visuals are trustworthy
- [ ] Give each crop a station-law effect rather than only different costs/timers
- [ ] Implement one cross-crop interaction as the proof slice
- [ ] Candidate: Lightning Vine produces power but increases flare vulnerability
- [ ] Candidate: Shadow Root benefits from blackout state
- [ ] Candidate: Trickster Vine relocates or steals a neighboring effect

## Later

- [ ] Dexter docking-bay vendor
- [ ] audio and station ambience
- [ ] anomaly event framework
- [ ] additional sectors
- [ ] accessibility/options screen
- [ ] release/export configuration
