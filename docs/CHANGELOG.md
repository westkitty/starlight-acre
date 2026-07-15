# Changelog

All notable changes to Starlight Acre are documented here.

---

## [Phase 2 — Asset Integration Follow-up] — 2026-07-15

### Added

- `actors/terminals/RepairTerminal.tscn` — Replaced orange ColorRect placeholder with the repair slice from `assets/sprites/terminals/terminals.png`.
- `actors/terminals/ReplenishTerminal.tscn` — Replaced blue ColorRect placeholder with the replenish slice from `assets/sprites/terminals/terminals.png`.
- `ui/hud/HUD.tscn` — Replaced text-only resource bar with icon/value pairs from `assets/ui/icons/hud_icons.png`; added prompt icon.
- `actors/crops/CropPlot.tscn` — Added `GPUParticles2D` ready-crop glow using `assets/effects/pixel_art_effects.png`.

### Changed

- `ui/hud/hud.gd` — Updated node paths and label text to drive the icon-led HUD layout.
- `actors/crops/crop_plot.gd` — Ready crop state now toggles the glow effect on; non-ready states keep it off.
- `README.md` and `docs/TASKS.md` — Updated Phase 2 status so completed asset integrations are no longer listed as pending.

### Still Pending (Phase 2)

- TileMapLayer tile painting and TileMap collision migration. This still requires opening the project in the Godot editor for visual tile placement and smoke testing.

---

## [Phase 2 — Partial] — 2026-03-23 — Sprite Integration + Gardener Drone

### Added

**Pixel art integration**
- `actors/player/Player.tscn` — AnimatedSprite2D replacing ColorRect placeholder; 15 AtlasTexture frames, 6 animations (idle/walk/jump/fall/land/interact)
- `actors/crops/CropPlot.tscn` — Sprite2D replacing ColorRect; `wisdom_fruit_states.png` 4-frame horizontal strip driven by crop state
- `scenes/world/GreenhouseSector.tscn` — Background ColorRect replaced with Sprite2D (`greenhouse_sector_bg.png`); TileMapLayer_Background wired to TileSet (`greenhouse_tiles.png`, 16×16 cells)
- `project.godot` — Global 2D texture filter set to Nearest for pixel art crispness

**Player animation**
- `actors/player/player.gd` — `_update_animation()` drives idle/walk/jump/fall/land/interact states; `flip_h` tracks facing direction; `_land_timer` locks animations to completion

**Gardener Drone agent**
- `actors/agents/gardener_drone.gd` — Patrols ±300px at 80px/s; scans every 5s; tends GROWING plots and harvests READY plots via `CropPlot.interact()`
- `actors/agents/GardenerDrone.tscn` — Teal ColorRect placeholder; instanced in GreenhouseSector at (0, 180)

**CropPlot improvements**
- `actors/crops/crop_plot.gd` — Added `class_name CropPlot`, `get_state() -> State`, and `groups=["crop_plots"]` for drone discovery

### Fixed (Bug Sweep)

- `crop_plot.gd` — Interaction prompt now refreshes on state change while player is in range; fixes Gardener Drone harvesting a READY plot causing stale "E — Harvest" prompt that silently planted
- `farming_manager.gd` — Power drain signal no longer emits every frame once power reaches zero
- `crop_plot.gd` — Removed unused `_area: Area2D` @onready variable
- `player.gd` — Animation lock guard now fires before landing detection; interact animation can no longer be interrupted by a concurrent landing event
- `wisdom_fruit.gd` — Removed dead `color_*` fields superseded by sprite frames

### Still Pending (Phase 2)

- Terminal sprite integration (`terminals.png`)
- HUD icon integration (`hud_icons.png`)
- TileMapLayer tile painting (requires Godot editor)
- Trickster Vine second crop
- GpuParticles2D growth_glow effect

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
