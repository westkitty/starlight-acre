# Starlight Acre

A small, polished orbital mythic farming station game. You restore and cultivate a failing greenhouse aboard a deep-space station, tending mythic lifeforms drawn from ancient pantheons while managing power, water, and the station's fragile systems.

**Engine:** Godot 4.3 · **Language:** GDScript · **View:** 2D side-view

---

## Current Status

**Phase 1 — Bootstrap complete.**

Playable vertical slice:
- Player movement (run, jump, coyote time, jump buffer)
- One crop lifecycle: Wisdom Fruit (plant → tend → harvest)
- Power drain hazard (passive drain; growth pauses at zero power)
- Repair Terminal (restores power) and Replenish Terminal (restores water + nutrients)
- HUD showing Water, Nutrient, Power, Wisdom Fruit count
- Interaction prompt system

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

---

## Controls

| Action | Keys |
|--------|------|
| Move   | A / D or ← → |
| Jump   | Space or ↑ |
| Interact | E |

---

## Folder Overview

```
autoload/        Global signal bus (Events.gd)
actors/          Player, crop plots, terminals
  player/        CharacterBody2D with movement + interaction
  crops/         CropPlot state machine (EMPTY→PLANTED→GROWING→READY)
  terminals/     RepairTerminal, ReplenishTerminal
systems/         FarmingManager (resources, power drain)
  farming/
scenes/          Game scenes
  world/         GreenhouseSector.tscn (entry scene)
data/            Content definitions
  crops/         CropDefinition resource + wisdom_fruit.gd
ui/              HUD and overlays
  hud/
assets/          Art, pixel art asset pack (Phase 2 integration)
  branding/
  sprites/
  ui/
  backgrounds/
  tilesets/
  effects/
  docs/
docs/            Project documentation
```

---

## MVP Definition

**In scope (Phase 1 complete):**
- 1 station sector (Greenhouse)
- 1 player character
- 1 crop: Wisdom Fruit (plant → tend → harvest)
- 1 resource loop: water + nutrients → grow → harvest → produce
- 1 hazard: passive power drain
- 2 terminals: Repair (power) and Replenish (water + nutrients)
- HUD resource display

**Post-MVP (Phase 2+):**
- Pixel art sprite integration (asset pack is included in `assets/`)
- Gardener drone agent
- Second crop: Trickster Vine
- Room transitions to adjacent sectors
- Dexter the Stinkweasel vendor encounter
- TileMapLayer visual pass

---

## Short Roadmap

| Phase | Goal |
|-------|------|
| ✅ Phase 1 | Runnable vertical slice with core loop |
| Phase 2 | Pixel art integration + gardener drone |
| Phase 3 | Second sector + room transitions |
| Phase 4 | Vendor (Dexter) + progression unlock |
| Phase 5 | Polish, audio, save/load |

---

## Documentation

- `docs/ARCHITECTURE.md` — Engine choice, folder structure, scene strategy
- `docs/GAME_DESIGN.md` — Core loop, crop system, resource economy, hazards
- `docs/PROJECT_OVERVIEW.md` — Vision, goals, MVP scope, non-goals
- `docs/TASKS.md` — Immediate tasks and roadmap
- `Starlight_Acre_bible.md` — Persistent project handoff ledger

---

## Pixel Art Assets

A GBA/SNES-style pixel art asset pack is included in `assets/`. Integration is planned for Phase 2.

Assets include: player sprite sheet (32×48px, 15 frames), Wisdom Fruit states (32×32px, 4 states), terminals (32×64px), HUD icons (16×16px), tileset, background, VFX effects.

See `assets/docs/` for slicing dimensions and Godot import settings.

---

*Tone: Mythic Sci-Fi. Restrained Wonder. A station that remembers.*
