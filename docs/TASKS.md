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

## Visual truth pass

- [x] Ratify and promote the canonical sprite/background/tileset assets at their documented live dimensions
- [x] Verify player/crop/HUD/terminal atlas regions against the promoted canonical sheets
- [x] Paint the Greenhouse floor and wall TileMapLayers from the canonical E01 tileset
- [x] Prove TileMap collision independently, then remove the obsolete Greenhouse StaticBody2D collision stubs
- [x] Enforce the 640×360 internal viewport and add a bounded player-follow camera with camera-synced sector backgrounds
- [ ] Human-review the promoted scene composition and sprite animation feel
- [ ] Play the complete loop manually: plant -> drone/manual tend -> harvest -> paid resupply -> research -> Engineering -> return -> restart

## Next: Mythic Ecology

- [x] Add a second crop only after crop visuals are trustworthy — Trickster Vine
- [x] Give the Wisdom/Trickster pair a station-law interaction rather than only different costs/timers
- [x] Implement one cross-crop interaction as the proof slice — Trickster steals one neighboring Wisdom tend per growth cycle
- [ ] Candidate: Lightning Vine produces power but increases flare vulnerability
- [ ] Candidate: Shadow Root benefits from blackout state
- [x] Trickster Vine relocates/steals a neighboring Wisdom tending effect; Paradox Trellis turns it into a shared pulse

## Later

- [ ] Dexter docking-bay vendor
- [ ] audio and station ambience
- [ ] anomaly event framework
- [ ] additional sectors
- [ ] accessibility/options screen
- [ ] release/export configuration
