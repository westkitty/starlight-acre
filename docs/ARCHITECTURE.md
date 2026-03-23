# Starlight Acre — Architecture

## Engine & Language

**Godot 4.3** / **GDScript**

Rationale: Godot 4 provides scene composition, a built-in physics system, and a signal architecture well-suited to decoupled game systems. GDScript is fast to iterate in and readable end-to-end. The project is 2D side-view with room-based navigation — a sweet spot for Godot's strengths.

Alternatives considered: Unity (more tooling but heavier runtime), Pygame (too low-level for this scope), Bevy (excellent but early ecosystem).

---

## Folder Structure

```
autoload/        Stable service roots (singletons)
actors/          All scene-bound entities
  player/        CharacterBody2D, movement, interaction
  crops/         CropPlot state machine
  terminals/     RepairTerminal, ReplenishTerminal
systems/         Game logic nodes (scene children, not autoloads)
  farming/       FarmingManager — resource state, power drain
data/            Pure data: Resource subclasses, JSON, tables
  crops/         CropDefinition resource class + crop files
scenes/          Assembled game scenes
  world/         Sector scenes (entry: GreenhouseSector.tscn)
ui/              CanvasLayer UI: HUD, menus, overlays
  hud/           HUD.tscn + hud.gd
assets/          Art, audio, fonts (Phase 2 integration)
docs/            Project documentation
```

---

## Scene Strategy

### Entry scene
`scenes/world/GreenhouseSector.tscn` is the main scene (`run/main_scene` in `project.godot`).

### Scene composition
Each game entity is its own scene (Player.tscn, CropPlot.tscn, RepairTerminal.tscn, etc.) and is instanced into world scenes. This keeps files focused and replaceable.

### Room transitions (Phase 2+)
Sector scenes will connect via door trigger areas. Each room-transition will use `get_tree().change_scene_to_file()` with player state passed through a lightweight GameState autoload (not yet needed in Phase 1).

---

## Autoload Strategy

Only one autoload in Phase 1:

| Autoload | File | Purpose |
|----------|------|---------|
| `Events` | `autoload/Events.gd` | Pure signal bus — no state, no logic |

**Rule:** Do not add a second autoload until a clear need exists that cannot be served by scene references or groups. Over-autoloading is a common Godot anti-pattern.

---

## Signal Architecture

`Events.gd` is the global event bus. Signals it emits:

| Signal | Args | Purpose |
|--------|------|---------|
| `crop_state_changed` | `plot_id: String, new_state: String` | Crop plot state change |
| `resource_changed` | `resource_name: String, new_value: float` | Any resource value update |
| `interaction_prompt_changed` | `prompt_text: String` | Show/hide interaction prompt |

Nodes that need to react to these signals connect in `_ready()`. No polling.

---

## FarmingManager Pattern

`FarmingManager` is a **scene child node** of GreenhouseSector, not an autoload. Other nodes find it via:

```gdscript
get_tree().get_first_node_in_group("farming_manager")
```

This keeps the resource state scoped to the sector that owns it, making multi-sector expansion straightforward.

---

## Interaction Pattern

The player holds a `_current_interactable` reference (one at a time). Interactable scenes (CropPlot, terminals) have an `Area2D` child that calls:

```gdscript
player.register_interactable(self)    # on body_entered
player.unregister_interactable(self)  # on body_exited
```

The player emits `interaction_prompt_changed` via Events and calls `_current_interactable.interact()` on the `interact` input action.

---

## Data Strategy

Crop definitions are `Resource` subclasses (`CropDefinition` in `data/crops/wisdom_fruit.gd`). This makes them inspectable in the Godot editor and loadable via `load()`.

Item tables, vendor stock, and hazard definitions will follow the same pattern (Phase 2+). JSON is acceptable for tabular data (e.g., vendor stock rotations).

---

## Save/Load Strategy (Phase 2+)

Phase 1 has no save system. Phase 2 target:
- Simple dictionary serialization to JSON
- `FileAccess.open("user://save.json", FileAccess.WRITE)`
- Save FarmingManager state + CropPlot states + player position

---

## Collision Strategy

Phase 1 uses `StaticBody2D` nodes for floor and wall collision. TileMapLayer nodes are present in GreenhouseSector but empty — they are stubs for the visual tile pass in Phase 2.

Phase 2 target: populate TileMapLayer with the included pixel art tileset (`assets/tilesets/greenhouse_tiles.png`) and generate collision from the tile physics layer.

---

## Technical Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| TileMapLayer migration complexity | Low | StaticBody2D bridges Phase 1 cleanly |
| Asset import settings (Nearest filter) | Low | Documented in assets/docs/asset_usage_notes.md |
| FarmingManager group lookup performance | Negligible | Called sparingly, not per-frame |
| Over-autoloading as project grows | Medium | Enforce one-autoload rule until justified |
