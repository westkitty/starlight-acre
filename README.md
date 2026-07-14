# Starlight Acre

A small, polished orbital mythic farming station game. You restore and cultivate a failing greenhouse aboard a deep-space station, tending mythic lifeforms drawn from ancient pantheons while managing power, water, and the station's fragile systems.

**Engine:** Godot 4.3 · **Language:** GDScript · **View:** 2D side-view

---

## Current Status

**Prototype build branch:** `codex/full-build-plan-implementation`

Implemented on this branch:
- Player with animated sprite (idle/walk/jump/fall/land/interact)
- Wisdom Fruit crop lifecycle with sprite states (plant -> tend -> harvest)
- Trickster Vine second crop with bounded erratic behavior
- Power drain hazard (passive drain; growth pauses at zero power)
- Repair Terminal + Replenish Terminal using terminal sprites
- Save/load terminals using JSON at `user://save.json`
- HUD icon/value rows for Water, Nutrient, Power, Wisdom Fruit, and Trickster Vine
- HUD status messages for save/load, insufficient resources, harvests, and trades
- Interaction prompt system
- Background art + TileSet configured
- Text-authored `TileVisualPass` fallback using `greenhouse_tiles.png`
- Gardener Drone agent (patrols greenhouse, tends and harvests automatically)
- Archive Library second sector with door transitions
- Dexter trade stub: spend 2 Wisdom Fruit to restore power and consumables
- Static and Godot headless validation scripts in `tools/validation/`

Still requires Godot editor/runtime validation:
- Full smoke test in Godot 4.3
- Optional editor-authored TileMapLayer painting and collision migration
- Dedicated Trickster Vine art
- Full Dexter shop UI and rotating stock

---

## Setup

### Requirements
- [Godot 4.3](https://godotengine.org/download/) (standard download, not Mono)

### Open the project
1. Launch Godot 4.3
2. Click **Import**
3. Navigate to this folder and select `project.godot`
4. Click **Import & Edit**

### Run
Press **F5** or click the Play button. The entry scene is `scenes/world/GreenhouseSector.tscn`.

### Validate
From a full checkout, run:

```bash
python3 tools/validation/static_scene_audit.py
godot4 --headless --path . --script tools/validation/godot_smoke_test.gd
```

See `docs/VALIDATION.md` for the complete manual smoke path and evidence requirements.

---

## Controls

| Action | Keys |
|--------|------|
| Move | A / D or Left / Right |
| Jump | Space or Up |
| Interact | E |

---

## Folder Overview

```
autoload/        Global Events signal bus and GameState transition/save state
actors/          Player, crop plots, terminals, transitions, vendors
systems/         FarmingManager resource and power-drain logic
scenes/          Game scenes; entry scene is scenes/world/GreenhouseSector.tscn
data/            Crop definitions
tools/           Validation scripts
ui/              HUD and overlays
assets/          Pixel art asset pack
docs/            Project documentation and validation notes
```

---

## MVP Definition

**Current prototype proves after validation:**
- Mythic orbital farming identity
- Player movement + interaction
- Crop lifecycle and resource costs
- Power drain tension
- Drone automation
- Second crop behavior variation
- First room transition
- Minimal trade/progression hook
- Basic save/load persistence

**Not release-ready:**
- No clean-machine export evidence
- No platform packaging
- No accessibility validation
- No license/release gate review
- No public release approval

---

## Documentation

- `docs/ARCHITECTURE.md` - Engine choice, folder structure, scene strategy
- `docs/GAME_DESIGN.md` - Core loop, crop system, resource economy, hazards
- `docs/PROJECT_OVERVIEW.md` - Vision, goals, MVP scope, non-goals
- `docs/TASKS.md` - Immediate tasks, blockers, and validation checklist
- `docs/VALIDATION.md` - Validation commands, smoke path, and evidence requirements
- `docs/CHANGELOG.md` - Change history
- `Starlight_Acre_bible.md` - Persistent project handoff ledger

---

*Tone: Mythic Sci-Fi. Restrained Wonder. A station that remembers.*
