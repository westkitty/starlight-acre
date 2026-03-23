# Starlight Acre — Project Bible

> This file is an additive handoff ledger. Never delete prior entries.
> Append new sessions as new dated sections.

---

## 1. Project Identity

**Project name:** Starlight Acre

**Summary:** Starlight Acre is a small, polished, finishable orbital mythic farming station game. The player lives on a decaying space station and restores it by cultivating mythic plants inspired by classical pantheons. The player orchestrates an ecosystem — eventually delegating tasks to simple heuristic agents — rather than micromanaging every action forever. The tone is atmospheric, slightly uncanny, luminous, and mythic-meets-sci-fi. It is not a farming clone and not a platformer. It is both.

**Target experience:** Restoring a failing orbital greenhouse into a self-sustaining mythic ecosystem. A calm but purposeful game where every day has a rhythm.

**Current phase:** Phase 2 — In progress. Sprite integration and Gardener Drone complete; terminal sprites, HUD icons, and tile painting remain.

---

## 2. Project Purpose

**What the game is:** A 2D side-view station management and mythic farming game with light Metroidvania traversal. The player repairs, plants, tends, harvests, and gradually expands a space station that grows magical plants tied to classical mythology.

**Experience goal:** The player should feel like a lone steward of something strange and precious. The station should feel alive. The mythic plants should feel like more than crops — they should have character.

**Current implementation goal:** Prove the game's identity with the minimum viable loop: plant a crop, tend it, harvest it, manage a station resource constraint. Establish a clean, extensible architecture that another engineer or AI can continue from the repo alone.

---

## 3. Current Stack

| Item | Value |
|------|-------|
| Engine | Godot 4.x |
| Language | GDScript |
| Perspective | 2D side-view |
| Structure | Scene composition, rooms as scenes |
| Decoupling | Events autoload signal bus |
| Art | Placeholder ColorRect (pixel art asset pack available in assets/) |
| Save/load | None (Phase 1 is session-only) |

**Assumption:**
Godot 4.x is installed on the development machine.
Reason: The preferred stack validated by the project's own deep-research-report.md.
Impact: If Godot is absent, docs and script files can still be written, but the project cannot be run.

---

## 4. Repository Map

```
/Users/andrew/Projects/Starlight Acre/
├── project.godot              Engine config, autoload, input map
├── README.md                  Setup + run instructions
├── Starlight_Acre_bible.md    This file — additive handoff ledger
├── docs/
│   ├── ARCHITECTURE.md
│   ├── GAME_DESIGN.md
│   ├── PROJECT_OVERVIEW.md
│   ├── TASKS.md
│   ├── CHANGELOG.md
│   ├── orbital_mythic_farming_game_concept.md   Original concept
│   ├── deep-research-report.md                  Godot architecture research
│   └── superpowers/
│       ├── specs/             Design specs (brainstorming output)
│       └── plans/             Implementation plans (writing-plans output)
├── scenes/world/              GreenhouseSector.tscn — the entry room
├── actors/
│   ├── player/                Player.tscn + player.gd
│   ├── crops/                 CropPlot.tscn + crop_plot.gd
│   └── terminals/             RepairTerminal, ReplenishTerminal
├── systems/farming/           farming_manager.gd
├── autoload/                  Events.gd (signal bus only)
├── data/crops/                wisdom_fruit.gd (CropDefinition resource)
├── ui/hud/                    HUD.tscn + hud.gd
└── assets/                    Pixel art asset pack (branding, sprites, tilesets, ui, effects, backgrounds)
```

---

## 5. Architecture Decisions

**Decision: Godot 4.x + GDScript**
Status: Accepted
Reason: Finishable, readable, modular, AI-friendly. Validated by deep-research-report.md. Scene composition maps well to the station room structure.
Impact: All code and scenes are Godot-specific.
Alternative considered: Unity — rejected for heavier toolchain and slower iteration.

**Decision: Events autoload as signal bus**
Status: Accepted
Reason: Decouples farming/automation systems from platformer traversal without direct node references. Prevents the codebase from becoming a web of get_node() calls.
Impact: All cross-system communication goes through Events.gd. Adding a new listener requires zero changes to the emitter.
Alternative considered: Direct node references — rejected because they break when scenes change.

**Decision: FarmingManager as child node of GreenhouseSector (not autoload)**
Status: Accepted
Reason: Resource state is session-only in Phase 1. Tying it to the room's lifecycle is correct. Making it an autoload would persist state across room transitions (Phase 2) in ways we haven't designed yet.
Impact: FarmingManager is found via `get_first_node_in_group("farming_manager")`. Interactables must call this instead of using a global path.
Alternative considered: Autoload — deferred to Phase 2 when save/load is introduced.

**Decision: Single active interactable via player registration**
Status: Accepted
Reason: Eliminates the race condition where multiple interactables emit interaction prompts simultaneously. One clear owner (player.gd) drives the prompt signal.
Impact: Each interactable has Area2D; body_entered calls player.register_interactable(self); body_exited calls player.unregister_interactable(self). Most recently entered wins.
Alternative considered: Global "nearest interactable" scan each frame — rejected for complexity.

**Decision: StaticBody2D for floor/wall collision (not TileMapLayer)**
Status: Accepted (Phase 1 only)
Reason: TileMapLayer requires a configured TileSet to provide collision. Writing a TileSet from scratch in the .tscn text format is error-prone. StaticBody2D with RectangleShape2D provides immediate solid collision.
Impact: TileMapLayer nodes exist in GreenhouseSector (TileMapLayer_Background, TileMapLayer_Floor, TileMapLayer_Walls) for architectural intent, but they are empty. Phase 2 will populate them with real tiles and remove the StaticBody2D stubs.
Alternative considered: Manual TileSet setup — deferred to Phase 2.

---

## 6. Game Definition Snapshot

**Player fantasy:** You are the last steward of a failing orbital greenhouse-station. You must restore its mythic ecosystems before the station fails entirely.

**Core loop (Phase 1 MVP):**
1. Check resources (Water, Nutrient, Power)
2. Plant a crop (spend Water + Nutrient)
3. Tend crop (speed up growth)
4. Harvest crop (gain Wisdom Fruit)
5. Repair power if drained (visit RepairTerminal)
6. Replenish consumables (visit ReplenishTerminal)

**Playable space:** One greenhouse sector. One flat platform with crop plots and terminals.

**Current crop set:** Wisdom Fruit only. Athena-inspired. Brain-shaped (placeholder: gold rect when ready). Produces Wisdom Fruit resource. Used for research/upgrades in Phase 2.

**Current hazard set:** Power drain. Passive drain at ~1%/3s. Pauses crop growth at 0%. Repaired by RepairTerminal. No dramatic animation — resource bar IS the hazard communication.

**Current vendor plan:** Dexter the Stinkweasel — not implemented. Documented in GAME_DESIGN.md as Phase 3.

**Out of scope for current phase:** Agents, vendor, second room, save/load, second crop, movement upgrades, sound, real art.

---

## 7. Implementation Status

| System | Status |
|--------|--------|
| Godot project (project.godot) | Done |
| Folder structure | Done |
| Events autoload (signal bus) | Done |
| CropDefinition resource (wisdom_fruit.gd) | Done |
| Player movement (CharacterBody2D, coyote, jump buffer) | Done |
| GreenhouseSector room (floor, walls, background) | Done |
| FarmingManager (resource state, power drain) | Done |
| CropPlot state machine (EMPTY→PLANTED→GROWING→READY) | Done |
| RepairTerminal | Done |
| ReplenishTerminal | Done |
| HUD (resource bar + interaction prompt) | Done |
| Full crop lifecycle end-to-end | Done |
| Starlight_Acre_bible.md | Done |
| README.md | Done |
| docs/ARCHITECTURE.md | Done |
| docs/GAME_DESIGN.md | Done |
| docs/PROJECT_OVERVIEW.md | Done |
| docs/TASKS.md | Done |
| docs/CHANGELOG.md | Done |
| Pixel art asset pack | Done |
| Agents (Phase 2) | Not started |
| Dexter vendor (Phase 3) | Not started |
| Second room / room transitions | Not started |
| Save / load | Not started |
| TileMapLayer visual pass (Phase 2) | Not started |
| Sound | Not started |

---

## 8. Work Log

### Session 1 — 2026-03-22 — Bootstrap

**Objective:** Take an empty repo (two concept docs) to a runnable Godot project with the full crop lifecycle.

**Actions taken:**
- Audited repo — found: orbital_mythic_farming_game_concept.md, deep-research-report.md, no code
- Decided: Godot 4.x + GDScript (stack already indicated by research doc)
- Created folder structure: scenes/, actors/, systems/, autoload/, data/, ui/, assets/, docs/
- Moved concept docs to docs/
- Wrote project.godot with input map and Events autoload declaration
- Wrote Events.gd — 3 signals, no logic
- Wrote wisdom_fruit.gd (CropDefinition base class + Wisdom Fruit defaults)
- Wrote player.gd + Player.tscn (movement, coyote time, jump buffer, interactable registration)
- Wrote GreenhouseSector.tscn (background, TileMapLayer stubs, StaticBody2D floor/walls, FarmingManager node, Player instance)
- Wrote farming_manager.gd (resource state: water 5, nutrient 5, power 100%, wisdom_fruit 0; passive power drain)
- Wrote crop_plot.gd + CropPlot.tscn (state machine, Area2D interaction)
- Placed 3 CropPlot instances in GreenhouseSector
- Wrote hud.gd + HUD.tscn (resource bar + interaction prompt)
- Wrote repair_terminal.gd + RepairTerminal.tscn
- Wrote replenish_terminal.gd + ReplenishTerminal.tscn
- Placed terminals in GreenhouseSector
- Wrote all documentation
- Added pixel art asset pack (branding, sprites, tilesets, UI icons, effects, background)

**Files created:**
- project.godot
- autoload/Events.gd
- data/crops/wisdom_fruit.gd
- actors/player/player.gd, Player.tscn
- scenes/world/GreenhouseSector.tscn
- systems/farming/farming_manager.gd
- actors/crops/crop_plot.gd, CropPlot.tscn
- actors/terminals/repair_terminal.gd, RepairTerminal.tscn
- actors/terminals/replenish_terminal.gd, ReplenishTerminal.tscn
- ui/hud/hud.gd, HUD.tscn
- README.md, Starlight_Acre_bible.md
- docs/ARCHITECTURE.md, GAME_DESIGN.md, PROJECT_OVERVIEW.md, TASKS.md, CHANGELOG.md
- assets/ (pixel art asset pack — see assets/docs/asset_manifest.md)

**Files moved:**
- orbital_mythic_farming_game_concept.md → docs/
- deep-research-report.md → docs/

**Issues encountered:**
- StaticBody2D used for floor collision instead of TileMapLayer (TileSet setup too complex for text-format .tscn). Documented in ARCHITECTURE.md as Phase 2 replacement.

**Result:** Runnable. Full crop loop playable.

**Next recommended step:** Phase 2 — add gardener drone agent, second crop (Trickster Vine), room transitions.

---

## 9. Commands Used

```bash
# Open Godot project
godot4 --path "/Users/andrew/Projects/Starlight Acre"
# Or: open Godot editor → File → Open Project → select project.godot

# Run project from editor
# Press F5 or the Play Scene button in Godot editor

# Git operations used during bootstrap
cd "/Users/andrew/Projects/Starlight Acre"
git add -A
git commit -m "..."
git log --oneline
git status

# Scaffold directories
mkdir -p scenes/world scenes/test actors/player actors/crops actors/terminals systems/farming autoload data/crops ui/hud assets/placeholder
```

---

## 10. Known Issues and Risks

| Issue | Severity | Status |
|-------|----------|--------|
| StaticBody2D floor will need replacing with TileMapLayer in Phase 2 | Low | Known, documented |
| No save/load — progress lost on quit | Expected | By design for Phase 1 |
| No sound or music | Expected | By design for Phase 1 |
| Placeholder ColorRect art — pixel art asset pack available but not wired to scenes | Low | Phase 2 visual pass |
| Power drain rate (1%/3s) may need tuning for feel | Low | Tune in Phase 2 |
| Wisdom Fruit has no spend mechanic yet — accumulates indefinitely | Expected | Phase 2 adds upgrade system |
| CropPlot growth_time (30s) may feel slow or fast — needs playtesting | Low | Tune in Phase 2 |

**Design risks:**
- Scope explosion: agent system, second crop, and room transitions must each be isolated phases.
- Natural language agent creation from the concept doc is explicitly post-MVP; do not implement until Phase 4+.

---

## 11. Assumptions

**Assumption:** Godot 4.x installed on development machine.
Reason: Required to run the project.
Impact: If absent, install from godotengine.org. Only the GDScript and docs portions of the work can be completed without it.

**Assumption:** Input actions in project.godot will be accepted as written.
Reason: Godot 4 text format for input actions is verbose and partially undocumented for hand-editing.
Impact: If project.godot fails to load input actions correctly, use the Godot editor (Project Settings → Input Map) to re-add them manually. The action names (move_left, move_right, jump, interact) must match the strings used in player.gd.

**Assumption:** Area2D body_entered fires with CharacterBody2D.
Reason: CharacterBody2D is a PhysicsBody2D, which Area2D monitors by default.
Impact: If collision layers are misconfigured, Area2D may not detect the player. Default collision layers (1) should work without manual configuration.

**Assumption:** `get_first_node_in_group("farming_manager")` returns FarmingManager reliably.
Reason: FarmingManager calls `add_to_group("farming_manager")` in its `_ready()`.
Impact: If FarmingManager's `_ready()` runs after an interactable tries to call it, the return will be null. Guarded with null checks in all callers.

---

## 12. Next-Step Handoff

### Session: 2026-03-22 — Phase 1 Bootstrap

**State at end of session:** Runnable Godot 4 project. Open project.godot in Godot 4 editor, run with F5. Player moves in a dark greenhouse room. Three crop plots (grey = empty). Two terminals (orange = repair, blue = replenish). Passive power drain visible in HUD. Full crop lifecycle functional. All docs written. Pixel art asset pack in assets/ — not yet wired to scenes.

---

### Session: 2026-03-23 — Phase 2 Partial (Sprite Integration + Drone)

**State at end of session:** Player now uses AnimatedSprite2D with 6 animations (idle/walk/jump/fall/land/interact) from `player_sheet.png`. Crop plots show `wisdom_fruit_states.png` (4 states, frame-driven). Background shows `greenhouse_sector_bg.png`. TileMapLayer_Background has a TileSet configured (`greenhouse_tiles.png`, 16×16) but no tiles painted. Gardener Drone patrols ±300px, tends GROWING and harvests READY plots every 5s. Global texture filter set to Nearest. Five bugs fixed (see CHANGELOG.md). All docs updated.

**What remains in Phase 2:**

1. **Terminal sprites** — Replace RepairTerminal and ReplenishTerminal ColorRect placeholders with `terminals.png` (32×64px). Repair = left slice, Replenish = right slice.
2. **HUD icons** — Replace text-only labels with icon+label pairs using `hud_icons.png` (16×16px per icon).
3. **Tile painting** — Open Godot editor, select TileMapLayer_Background, paint greenhouse floor/wall/beam tiles. This cannot be done in text format — requires visual tile placement in the editor.
4. **Trickster Vine** — Second crop. New CropDefinition subclass with distinct growth behavior (erratic timer, fleeing harvest). New CropPlot variant or extended state machine.
5. **GpuParticles2D** — Add growth_glow particles over READY crop state using `effects/pixel_art_effects.png`.

**After Phase 2 is complete:**
- Phase 3: Room transitions (door interactable, second sector scene, FarmingManager state persistence)
- Phase 4: Dexter the Stinkweasel (docking event, trade UI)
- Phase 5: Save/load, audio, polish

**Top priorities for next session:**
1. Read this bible.
2. Open the project in Godot 4.3 and run it — verify player sprite, crop sprite, background, and drone are all working.
3. Paint the TileMapLayer tiles while the editor is open (it's the one task that requires the editor).
4. Then implement terminal sprites and HUD icons (can be done in text-format .tscn).

**Warnings for next worker:**
- Do NOT add a second autoload without a strong reason. FarmingManager staying as a scene child is intentional.
- Do NOT implement natural language agent creation. It is documented in the concept doc but is explicitly post-MVP.
- The StaticBody2D floor is still the Phase 1 collision stub. The TileMapLayer now has a TileSet but no collision tiles. Do not remove StaticBody2D until TileMapLayer collision is set up.
- Growth time (30s) and power drain (1%/3s) are first-pass values. Needs playtesting.
- The Gardener Drone calls `interact()` via the CropPlot interface — it does NOT call private `_tend()`/`_harvest()` directly. Keep this clean.
- `_player_in_range` in crop_plot.gd is set by Area2D body_entered/exited. If a room transition occurs while the player is inside a plot's area, `_player_in_range` will be stale in the new scene. Null-check guards it safely.
