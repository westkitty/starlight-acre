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
- Internal resolution: 640×360 with Nearest filter, enforced in project settings; default desktop window is 1280×720 (2×)
- ColorRect placeholders for all sprites (pixel art integration in Phase 2)

---

*Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) conventions.*


---

## [Progression + Persistence Upgrade] — 2026-09-17

### Added
- GameState persistence and JSON save/load
- data-driven CropDefinition resources
- Engineering Bay and reusable sector doors
- Research Terminal with Efficient Grid and Closed-Loop Hydroponics
- finite emergency-resupply economy and Wisdom Fruit sinks
- spatial Gardener Drone target travel
- headless smoke test
- OPERATIONAL_STATE.md

### Recovered
- Terminal sprites, HUD icons, and READY-crop VFX from reverted commit defaecd for renewed validation.

### Fixed
- Repository .png files that actually contained JPEG bytes; normalized to real PNG encoding so Godot can import them on a clean clone.

### Migrated
- Project feature target from Godot 4.3 to Godot 4.7.

### Validation
- Godot 4.7.1 headless editor load: PASS
- smoke test: PASS
- 120-frame main-scene headless run: PASS

### Known limitation
- Generated image dimensions do not match historical sprite-sheet dimension claims; visual slicing still requires manual QA.

---

## [Greenhouse Environment Gate] — 2026-09-21

### Changed
- Painted the Greenhouse floor and side walls from the canonical `E01_GREENHOUSE_TILESET` atlas using real `TileMapLayer` cell data.
- Added TileSet physics to the painted Greenhouse tiles and removed the obsolete `Floor`, `WallLeft`, and `WallRight` StaticBody2D collision stubs after independent collision proof.
- Standardized the live internal viewport at 640×360 with a default 1280×720 desktop window and nearest-neighbor pixel filtering.
- Added a bounded player-follow `Camera2D`; horizontal travel clamps to the room limits while the vertical frame keeps the full 32px floor slab visible.
- Sector backgrounds now track the active camera center so a 640×360 canonical background remains screen-filling while the room scrolls.
- Visual QA capture now runs at the actual 640×360 game viewport. The report builder accepts a completed successful `report.json` as capture evidence when an outer launcher interruption prevents the wrapper `.rc` marker from being written.

### Validation
- Greenhouse floor cells: 150; wall cells: 136.
- With all legacy collision stubs gone, the real player lands on the TileMap floor at y=264 and is blocked by both TileMap side walls.
- Camera contract regression checks pass at left, center, and right room positions with the background synchronized to the camera center.
- `tests/run_core_systems.sh`: PASS after the migration.
- Real Godot 4.7.1 Greenhouse and Engineering captures: 640×360, status OK; 34/34 visual QA crops extracted.

---

## [First Station Hazard — Solar Flare] — 2026-09-21

### Added
- `systems/hazards/SolarFlareController.tscn` + `solar_flare_controller.gd`: recurring Solar Flare lifecycle with 30s initial calm, 5s warning, 8s active phase, and 45s recovery.
- `Events.hazard_state_changed` as the hazard-state notification surface.
- Transient in-run Solar Flare phase/time on `GameState`; it survives sector transitions but is intentionally excluded from save serialization.
- HUD Solar Flare indicator using the canonical V02 cell 1 from `assets/effects/hazard_vfx.png`.

### Changed
- Active Solar Flare multiplies normal station power drain by 5×. Existing Efficient Grid mitigation remains multiplicative at 0.6.
- Both playable sectors instance the same Solar Flare controller so hazard state continues through Greenhouse <-> Engineering transitions.
- Core-system regression coverage now verifies warning/active/recovery transitions, HUD state, exact drain rates, Efficient Grid mitigation, normal cross-sector continuity, and the exact-zero transition boundary.

### Validation
- Godot 4.7.1 core-system Solar Flare lifecycle test: PASS.
- Real 640×360 active-flare capture: PASS.
- Exact V02 render check: all 297 nontransparent pixels from canonical Solar Flare cell 1 produced exactly 297 changed pixels in the 32×32 HUD rectangle, with no spill outside the intended indicator surface.

---

## [Lightning Vine + Flare Ecology] — 2026-09-21

### Added
- `data/crops/lightning_vine.tres`: Zeus/storm crop using canonical C03 art, 28s growth, 15% tend bonus, 1 Water + 1 Nutrient cost, and a direct +20 power harvest.
- The left Greenhouse plot now uses `assets/sprites/crops/lightning_vine_states.png`; Wisdom remains center and Trickster remains right, preserving the existing 200px Wisdom↔Trickster ecology radius.
- `GameState.conductive_lightning_vine_count()` and a second Mythic Ecology rule: each GROWING or READY Lightning Vine adds +2× to active Solar Flare drain.

### Changed
- Active Solar Flare multiplier is now `5 + (2 × conductive Lightning Vines)`; one live vine therefore raises the flare from 5× to 7× before Efficient Grid mitigation.
- Solar Flare warning/active messages explicitly call out Lightning Vine conduction when present.
- Crop harvest output now supports direct station-power yield through the existing FarmingManager path; Lightning harvest restores 20 power and respects the 100% cap.
- Gardener regression coverage now targets the preserved Wisdom plot explicitly, so its travel + ordinary-harvest proof remains semantically correct after CropPlot0 became Lightning.

### Validation
- Godot 4.7.1 Lightning regression: PASS for crop contract, 7× flare amplification, exact 20-power harvest, 100% cap, immediate removal of conductor risk after harvest, and cross-sector crop-state persistence.
- Smoke test now loads and validates `lightning_vine.tres`.
- Real 640×360 Lightning + active-flare capture: PASS.
- Canonical C03 READY-frame slicing/alignment diagnostic: **596/596 nontransparent source pixels matched the live 32×32 sprite exactly** when the READY particle layer alone was hidden; the earlier normal READY capture differed only where particles overlaid the sprite.
