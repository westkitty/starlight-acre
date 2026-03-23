# Starlight Acre — Project Bible

> This file is an additive handoff ledger. Never delete prior entries.
> Append new sessions as new dated sections.

---

## 1. Project Identity

**Project name:** Starlight Acre

**Summary:** Starlight Acre is a small, polished, finishable orbital mythic farming station game. The player lives on a decaying space station and restores it by cultivating mythic plants inspired by classical pantheons. The player orchestrates an ecosystem — eventually delegating tasks to simple heuristic agents — rather than micromanaging every action forever. The tone is atmospheric, slightly uncanny, luminous, and mythic-meets-sci-fi.

**Target experience:** Restoring a failing orbital greenhouse into a self-sustaining mythic ecosystem. A calm but purposeful game where every day has a rhythm.

**Current phase:** Phase 1 — Bootstrap in progress.

---

## 2. Project Purpose

**What the game is:** A 2D side-view station management and mythic farming game with light Metroidvania traversal. The player repairs, plants, tends, harvests, and gradually expands a space station that grows magical plants tied to classical mythology.

**Experience goal:** The player should feel like a lone steward of something strange and precious. The station should feel alive. The mythic plants should feel like more than crops.

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
| Art | Placeholder ColorRect |
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
├── docs/                      All design and reference docs
│   ├── orbital_mythic_farming_game_concept.md   Original concept
│   ├── deep-research-report.md                  Godot architecture research
│   └── superpowers/
│       ├── specs/             Design specs
│       └── plans/             Implementation plans
├── scenes/world/              GreenhouseSector.tscn — entry room
├── actors/
│   ├── player/                Player.tscn + player.gd
│   ├── crops/                 (Task 8: CropPlot)
│   └── terminals/             (Task 11-12: terminals)
├── systems/farming/           (Task 7: farming_manager.gd)
├── autoload/                  Events.gd (signal bus only)
├── data/crops/                wisdom_fruit.gd (CropDefinition resource)
├── ui/hud/                    (Task 10: HUD)
└── assets/                    Pixel art asset pack (branding, sprites, tilesets, ui, effects)
```

---

## 5. Architecture Decisions

**Decision: Godot 4.x + GDScript**
Status: Accepted
Reason: Finishable, readable, modular, AI-friendly. Validated by deep-research-report.md.
Impact: All code and scenes are Godot-specific.
Alternative considered: Unity — rejected for heavier toolchain and slower iteration.

**Decision: Events autoload as signal bus**
Status: Accepted
Reason: Decouples farming/automation systems from platformer traversal without direct node references.
Impact: All cross-system communication goes through Events.gd.
Alternative considered: Direct node references — rejected because they break when scenes change.

**Decision: FarmingManager as child node of GreenhouseSector (not autoload)**
Status: Accepted
Reason: Resource state is session-only in Phase 1. Tying it to the room's lifecycle is correct.
Impact: FarmingManager is found via `get_first_node_in_group("farming_manager")`.
Alternative considered: Autoload — deferred to Phase 2 when save/load is introduced.

**Decision: Single active interactable via player registration**
Status: Accepted
Reason: Eliminates the race condition where multiple interactables emit interaction prompts simultaneously.
Impact: Each interactable has Area2D; body_entered calls player.register_interactable(self); body_exited calls player.unregister_interactable(self). Most recently entered wins.
Alternative considered: Global "nearest interactable" scan each frame — rejected for complexity.

**Decision: StaticBody2D for floor/wall collision (not TileMapLayer)**
Status: Accepted (Phase 1 only)
Reason: TileMapLayer requires a configured TileSet. Writing a TileSet in .tscn text format is error-prone.
Impact: TileMapLayer nodes exist in GreenhouseSector for architectural intent but are empty. Phase 2 will populate them.
Alternative considered: Manual TileSet setup — deferred to Phase 2.

---

## 6. Game Definition Snapshot

**Player fantasy:** You are the last steward of a failing orbital greenhouse-station. You must restore its mythic ecosystems.

**Core loop (Phase 1 MVP):**
1. Check resources (Water, Nutrient, Power)
2. Plant a crop (spend Water + Nutrient)
3. Tend crop (speed up growth)
4. Harvest crop (gain Wisdom Fruit)
5. Repair power if drained (visit RepairTerminal)
6. Replenish consumables (visit ReplenishTerminal)

**Playable space:** One greenhouse sector. One flat platform with crop plots and terminals.

**Current crop set:** Wisdom Fruit only. Athena-inspired. Placeholder gold rect when ready. Produces Wisdom Fruit resource.

**Current hazard set:** Power drain. Passive drain at ~1%/3s. Pauses crop growth at 0%.

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
| FarmingManager (resource state, power drain) | Not started |
| CropPlot state machine | Not started |
| RepairTerminal | Not started |
| ReplenishTerminal | Not started |
| HUD (resource bar + interaction prompt) | Not started |
| Full crop lifecycle end-to-end | Not started |
| All documentation | Not started |

---

## 8. Work Log

### Session 1 — 2026-03-22 — Bootstrap (in progress)

**Objective:** Take an empty repo (two concept docs) to a runnable Godot project with the full crop lifecycle.

**Actions taken so far:**
- Audited repo — found: orbital_mythic_farming_game_concept.md, deep-research-report.md, no code
- Decided: Godot 4.x + GDScript (stack indicated by research doc)
- Created folder structure: scenes/, actors/, systems/, autoload/, data/, ui/, assets/, docs/
- Moved concept docs to docs/
- Wrote project.godot with input map and Events autoload declaration
- Wrote Events.gd — 3 signals, no logic
- Wrote wisdom_fruit.gd (CropDefinition base class + Wisdom Fruit defaults)
- Wrote player.gd + Player.tscn (movement, coyote time, jump buffer, interactable registration)
- Wrote GreenhouseSector.tscn (background, TileMapLayer stubs, StaticBody2D floor/walls, FarmingManager node, Player instance)

**Files created so far:**
- project.godot
- autoload/Events.gd
- data/crops/wisdom_fruit.gd
- actors/player/player.gd, Player.tscn
- scenes/world/GreenhouseSector.tscn

**Next step:** Implement FarmingManager, CropPlot, HUD, terminals, then write all docs.

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
```

---

## 10. Known Issues and Risks

| Issue | Severity | Status |
|-------|----------|--------|
| StaticBody2D floor will need replacing with TileMapLayer in Phase 2 | Low | Known, documented |
| No save/load — progress lost on quit | Expected | By design for Phase 1 |
| No sound or music | Expected | By design for Phase 1 |
| No real art assets — placeholder ColorRects only | Expected | By design for Phase 1 |

---

## 11. Assumptions

**Assumption:** Godot 4.x installed on development machine.
Reason: Required to run the project.
Impact: Install from godotengine.org if absent.

**Assumption:** Input actions in project.godot will be accepted as written.
Reason: Godot 4 text format for input actions is verbose but valid.
Impact: If incorrect, use Godot editor Project Settings → Input Map to re-add manually.

**Assumption:** Area2D body_entered fires with CharacterBody2D.
Reason: CharacterBody2D is a PhysicsBody2D, which Area2D monitors by default.
Impact: Default collision layers (1) should work without manual configuration.

**Assumption:** `get_first_node_in_group("farming_manager")` returns FarmingManager reliably.
Reason: FarmingManager calls `add_to_group("farming_manager")` in its `_ready()`.
Impact: Guarded with null checks in all callers.

---

## 12. Next-Step Handoff

TODO: update at phase end — see Task 13 (bible will be finalized after all systems are implemented).
