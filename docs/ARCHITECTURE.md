# Starlight Acre — Architecture

## Runtime

Godot 4.7.x / GDScript / 2D side-view.

The development Mac used for the 2026-09-17 validation pass has Godot 4.7.1 stable installed. The project metadata has been migrated from the old 4.3 feature tag to 4.7.

## State boundaries

### Events autoload
`Events.gd` remains a stateless signal bus. It owns no gameplay state.

### GameState autoload
`game_state.gd` now exists because the game has crossed the point where scene-local state is sufficient. It owns:
- water
- nutrients
- power
- Wisdom Fruit
- emergency resupply count
- permanent upgrades
- persisted crop states
- current sector
- next transition spawn
- JSON serialization to `user://save.json`

This is the justified second autoload. Do not move unrelated systems into it.

### FarmingManager
Each active sector owns a FarmingManager node. It exposes the gameplay resource interface while reading/writing persistent values through GameState. This preserves the existing interactable architecture and avoids making every actor depend directly on save-state internals.

## Crop architecture

`CropDefinition` is now a reusable Resource schema. Crop plots accept an exported CropDefinition and default to `wisdom_fruit.tres`.

Do not add crop-specific branches to `CropPlot` for every future crop. Add explicit data first; add behavior strategies/components only when genuinely required.

## Automation

The Gardener Drone may discover plots through the `crop_plots` group, but it must physically travel into interaction range before tending or harvesting. Scene-wide remote `interact()` calls are prohibited because they make the rendered drone position meaningless.

## Sector architecture

World sectors are independent scenes using `sector_controller.gd`. Doors set the next sector and spawn position in GameState before changing scenes.

Current sectors:
- Greenhouse Sector
- Engineering Bay

## Collision

Greenhouse TileMapLayer nodes remain visually unpainted. StaticBody2D floor/walls remain authoritative collision until a visually and physically verified TileMap replacement exists.

## Asset warning

The repository historically described several generated sheets as 32x48, 32x32, 16x16, etc. The actual source images inspected on 2026-09-17 are 640x640. They were also JPEG-encoded while named `.png`, which broke clean-clone imports until normalized.

Never trust the old manifest dimensions without visual verification.

## Validation

Minimum technical gate:

```bash
godot --headless --path . --editor --quit
godot --headless --path . --script tests/smoke_test.gd
godot --headless --path . --quit-after 120
git diff --check
```

A release or visual-completion claim additionally requires a manual editor playthrough and sprite-slicing inspection.
