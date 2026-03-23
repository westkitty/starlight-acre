# Changelog

All notable changes to Starlight Acre are documented here.

---

## [Phase 1] — 2026-03-22 — Bootstrap Complete

### Added

**Project scaffolding**
- `project.godot` — Godot 4.3 configuration, input map, Events autoload
- `.gitignore` — excludes `.godot/`, `*.import`, `.DS_Store`, etc.
- Git repository initialized at project root

**Core systems**
- `autoload/Events.gd` — Global signal bus (crop_state_changed, resource_changed, interaction_prompt_changed)
- `systems/farming/farming_manager.gd` — Resource state manager (water, nutrients, power, wisdom_fruit); passive power drain at 0.333/sec; group "farming_manager"

**Player**
- `actors/player/player.gd` — CharacterBody2D; run/jump with coyote time (0.1s) and jump buffer (0.1s); interactable registration system
- `actors/player/Player.tscn` — Player scene (blue ColorRect placeholder)

**Crop system**
- `data/crops/wisdom_fruit.gd` — CropDefinition resource class with Wisdom Fruit defaults (30s growth, 20% tend bonus)
- `actors/crops/crop_plot.gd` — CropPlot state machine (EMPTY → PLANTED → GROWING → READY); Area2D interaction; growth pauses at zero power
- `actors/crops/CropPlot.tscn` — CropPlot scene (ColorRect placeholder, Area2D)

**Terminals**
- `actors/terminals/repair_terminal.gd` + `RepairTerminal.tscn` — Restores power to 100% (orange placeholder)
- `actors/terminals/replenish_terminal.gd` + `ReplenishTerminal.tscn` — Restores water + nutrients (blue placeholder)

**HUD**
- `ui/hud/hud.gd` — CanvasLayer; displays Water, Nutrient, Power%, Wisdom Fruit count; interaction prompt
- `ui/hud/HUD.tscn` — HUD scene

**World**
- `scenes/world/GreenhouseSector.tscn` — Entry scene; floor/wall collision (StaticBody2D); 3 CropPlots; Player; FarmingManager; HUD; both terminals; TileMapLayer stubs (empty, Phase 2)

**Documentation**
- `README.md` — Setup, controls, folder overview, MVP status, roadmap
- `Starlight_Acre_bible.md` — 12-section persistent project handoff ledger
- `docs/ARCHITECTURE.md` — Engine, folder structure, scene/signal/data strategies
- `docs/GAME_DESIGN.md` — Core loop, crops, resources, agents, hazards, progression
- `docs/PROJECT_OVERVIEW.md` — Vision, experience goals, scope, non-goals
- `docs/TASKS.md` — Immediate tasks, roadmap, priorities
- `docs/CHANGELOG.md` — This file

**Assets (included, not yet integrated)**
- `assets/` — GBA/SNES pixel art asset pack (player sheet, Wisdom Fruit sprites, terminals, HUD icons, tileset, background, VFX)
- `assets/docs/` — Style guide, asset manifest, usage notes, assumptions

### Decisions Made

- Godot 4.3 / GDScript selected as engine (no alternatives in repo)
- Single Events autoload only (no GameState autoload until Phase 3)
- FarmingManager as scene child (not autoload) for multi-sector scalability
- StaticBody2D for Phase 1 collision (TileMapLayer visual pass deferred to Phase 2)
- Internal resolution: ~480×270 with Nearest filter (assumed; not yet enforced in project settings)
- ColorRect placeholders for all sprites (pixel art integration in Phase 2)

---

*Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) conventions.*
