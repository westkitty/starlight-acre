# Starlight Acre — Bootstrap Phase Design Spec

**Date:** 2026-03-22
**Phase:** Phase 1 — Big Bootstrap (scaffold + docs + first mechanic)
**Approach:** Scaffold-first, docs alongside, mechanic last
**Status:** Approved for implementation planning

---

## 1. Phase Goal

Produce a runnable Godot 4.x project that:
- Opens cleanly in the Godot editor
- Has a defined entry scene
- Has a player character that moves with good feel
- Has one complete crop lifecycle (plant → grow → tend → harvest)
- Has one station resource constraint (power drain + repair)
- Has all required handoff documentation written
- Has the project bible initialized and populated

This phase ends when a stranger can open the repo, read the bible, run the scene, and play the full crop loop without any guidance.

---

## 2. Repo Context

**Location:** `/Users/andrew/Projects/Starlight Acre`
**Current state at design time:** Two concept/research docs only — no code, no Godot project, no git history specific to this project.

Existing files to preserve:
- `orbital_mythic_farming_game_concept.md` — move to `docs/` (do not delete)
- `deep-research-report.md` — move to `docs/` (do not delete)

---

## 3. Stack

| Item | Choice | Rationale |
|------|--------|-----------|
| Engine | Godot 4.x | Finishable, modular, AI-friendly, validated by research doc |
| Language | GDScript | Idiomatic for Godot, readable, no compile step |
| Perspective | 2D side-view | Matches Metroidvania-lite + farming hybrid |
| Structure | Scene composition | Rooms as scenes, actors as instanced scenes |
| Decoupling | Events autoload (signal bus) | Prevents tight coupling between gameplay and UI |
| Art | Placeholder colored rects | No art blocker; silhouette-readable |
| Save/load | None (session state only) | Out of scope for Phase 1 |

**Assumption:**
Godot 4.x is installed and accessible on the development machine.
Reason: Research doc references Godot 4.x patterns and this is the preferred stack.
Impact: If Godot is not installed, the runnable-state goal cannot be met; docs and scaffold can still be completed.

---

## 4. Project Structure

Scaffold created before any gameplay code:

```
/Users/andrew/Projects/Starlight Acre/
├── project.godot                  ← entry scene: scenes/world/GreenhouseSector.tscn
├── README.md
├── Starlight_Acre_bible.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── GAME_DESIGN.md
│   ├── PROJECT_OVERVIEW.md
│   ├── TASKS.md
│   ├── CHANGELOG.md
│   ├── orbital_mythic_farming_game_concept.md   ← moved from root
│   ├── deep-research-report.md                  ← moved from root
│   └── superpowers/specs/
│       └── 2026-03-22-starlight-acre-bootstrap-design.md  ← this file
├── scenes/
│   ├── world/
│   │   └── GreenhouseSector.tscn   ← the one playable room
│   └── test/                       ← empty, reserved for test scenes
├── actors/
│   ├── player/
│   │   ├── Player.tscn
│   │   └── player.gd
│   ├── crops/
│   │   ├── CropPlot.tscn
│   │   └── crop_plot.gd
│   └── terminals/
│       ├── RepairTerminal.tscn     ← restores Power to 100%
│       ├── repair_terminal.gd
│       ├── ReplenishTerminal.tscn  ← restores Water + Nutrient to cap
│       └── replenish_terminal.gd
├── systems/
│   └── farming/
│       └── farming_manager.gd     ← child node of GreenhouseSector (not autoload)
├── autoload/
│   └── Events.gd
├── data/
│   └── crops/
│       └── wisdom_fruit.gd         ← CropDefinition resource
├── ui/
│   └── hud/
│       ├── HUD.tscn
│       └── hud.gd
└── assets/
    └── placeholder/                ← colored rect textures, no real art required
```

---

## 5. Architecture Constraints

- **One autoload only:** `Events.gd` — a pure signal bus, no game logic
- **Entry scene:** `project.godot` points to `scenes/world/GreenhouseSector.tscn`
- **Player:** `CharacterBody2D` with coyote time (0.1s) and jump buffer (0.1s)
- **Crop plots:** Scene-instanced interactables, not embedded in tile data
- **TileMapLayer:** Three separate nodes in GreenhouseSector — `FloorLayer`, `WallLayer`, `BackgroundLayer`
- **`farming_manager.gd`:** A plain Node child of GreenhouseSector (not an autoload). Owns the `_process` power drain timer and holds session resource state. Added to GreenhouseSector scene tree as `FarmingManager`.
- **Terminals:** Standalone scene files in `actors/terminals/`. Instanced into GreenhouseSector the same way as CropPlots — not embedded node scripts. This keeps them reusable for future rooms.
- **Single active interactable rule:** At any moment, exactly one interactable can be "active" for the player. Implemented via Area2D enter/exit on each interactable: when the player enters an Area2D, that interactable registers itself as active; on exit, it deregisters. If two areas overlap, the most recently entered wins. `E` always fires on the single registered active interactable only. This rule is enforced in `player.gd` — player holds a reference `current_interactable` that is set/cleared by area signals.
- **No save/load** in this phase
- **No room transitions** in this phase — one room only
- **No agents** in this phase — documented as next priority in GAME_DESIGN.md

---

## 6. Docs Deliverables

Each doc is written after its corresponding reality exists:

| File | Written when | Key contents |
|------|-------------|--------------|
| `Starlight_Acre_bible.md` | First, before any code | Audit results, stack decision, initial work log, assumptions, handoff |
| `README.md` | After `project.godot` exists | Setup, run instructions, folder overview, MVP status |
| `docs/ARCHITECTURE.md` | After folder structure created | Engine rationale, folder map, autoload policy, scene strategy |
| `docs/GAME_DESIGN.md` | After first room exists | Core loop, crop system, MVP definition, post-MVP list |
| `docs/PROJECT_OVERVIEW.md` | After first room exists | Vision, feel, non-goals |
| `docs/TASKS.md` | After mechanic is implemented | Immediate next tasks, blockers |
| `docs/CHANGELOG.md` | Last | Bootstrap entry, all files created, decisions |

**Mandatory bible update triggers:**
1. After Godot scaffold and folder structure created
2. After player movement works in GreenhouseSector
3. After full crop lifecycle works end-to-end
4. At phase end — final handoff section must be accurate

---

## 7. First Mechanic: Wisdom Fruit Crop Loop

### Why Wisdom Fruit
Chosen over Trickster Vine. Trickster Vine's "fruit flees on harvest" behavior requires a secondary movement system for the fruit entity. That is a second mechanic, not a first mechanic. Wisdom Fruit has clean, predictable behavior that proves the loop without scope creep.

### Crop States
```
EMPTY → PLANTED → GROWING → READY → EMPTY
```

### Player Interactions
| Context | Key | Cost | Effect |
|---------|-----|------|--------|
| Near EMPTY plot | `E` | 1 Water + 1 Nutrient | Transitions to PLANTED |
| Near GROWING plot | `E` | None | Reduces growth timer by 20% (tending) |
| Near READY plot | `E` | None | Harvests — yields 1 Wisdom Fruit, resets to EMPTY |

### Resources (session only, no persistence)
| Resource | Start | Cap | Source | Sink |
|----------|-------|-----|--------|------|
| Water | 5 | 10 | Replenish terminal | Planting |
| Nutrient | 5 | 10 | Replenish terminal | Planting |
| Wisdom Fruit | 0 | — | Harvest | (spend in Phase 2) |
| Power | 100% | 100% | Repair terminal | Passive drain over time |

### First Hazard: Power Drain
- Power drains passively (e.g. 1% every 3 seconds)
- When Power hits 0%, crop growth pauses
- A repair terminal in the room restores Power to 100% on `E` press
- HUD shows Power % at all times
- No dramatic animation required — the readable resource bar IS the hazard communication

### HUD
Single bar across the top:
```
[Water: 5/10]  [Nutrient: 5/10]  [Power: 87%]  [Wisdom Fruit: 0]
```
Crop plot color states (placeholder art):
- Grey rect = EMPTY
- Dark brown rect = PLANTED
- Green rect = GROWING
- Gold rect = READY

### Interaction Prompt
A simple label near the player's feet: "E — [action]" that updates based on what the player is near. Nothing near: label hidden.

---

## 8. GreenhouseSector Layout

Single room, side-view. Approximate structure:
- Floor platform (TileMapLayer)
- Two wall boundaries (TileMapLayer)
- Background with faint orbital window suggestion (TileMapLayer or plain ColorRect)
- 2–3 CropPlot instances placed on the floor
- 1 repair terminal (interactable node)
- 1 replenish terminal (restores Water + Nutrient, same interaction model as repair)
- Player spawn point

No vertical complexity in Phase 1. One flat platform. Movement upgrades and vertical traversal are Phase 2+.

---

## 9. Events Autoload

`autoload/Events.gd` emits signals only. No state, no logic.

Signals needed in Phase 1:
```gdscript
signal crop_state_changed(plot_id: String, new_state: String)
signal resource_changed(resource_name: String, new_value: float)
signal interaction_prompt_changed(prompt_text: String)  # empty string = hide prompt
```

HUD listens to `resource_changed`. Interaction prompt label listens to `interaction_prompt_changed` — empty string means hide the label. Crop plots emit `crop_state_changed` when their state transitions.

`interaction_prompt_changed` is emitted by `player.gd` when `current_interactable` changes, not by the interactables themselves. This ensures only one source drives the prompt at a time, eliminating the race condition that would arise if multiple interactables each emitted the signal independently.

---

## 10. Out of Scope for This Phase

These are explicitly excluded. Document them in GAME_DESIGN.md as next priorities:
- Agents / drones of any kind
- Dexter the Stinkweasel vendor
- Room transitions / second room
- Save / load
- Any second crop
- Movement upgrades (jet boots, grapple, etc.)
- Natural language anything
- Vertical traversal complexity
- Sound / music
- Real art assets

---

## 11. Phase Done Criteria

The phase is complete when all of the following are true:

**Runnable:**
- [ ] `project.godot` exists and opens in Godot 4 without errors
- [ ] Running the entry scene shows GreenhouseSector
- [ ] Player moves left/right, jumps with coyote time and jump buffer

**Mechanic:**
- [ ] Player can plant Wisdom Fruit (costs Water + Nutrient)
- [ ] Crop grows over time through PLANTED → GROWING → READY states
- [ ] Player can tend a GROWING crop to reduce its timer
- [ ] Player can harvest a READY crop (yields Wisdom Fruit in HUD)
- [ ] Power drains passively; growth pauses at 0%
- [ ] Player can repair power at the terminal
- [ ] Player can replenish Water and Nutrient at the terminal
- [ ] HUD accurately reflects all resources at all times
- [ ] Interaction prompt updates correctly near each interactable

**Docs:**
- [ ] `Starlight_Acre_bible.md` exists with real content in all 12 required sections:
  1. Project Identity
  2. Project Purpose
  3. Current Stack
  4. Repository Map
  5. Architecture Decisions
  6. Game Definition Snapshot
  7. Implementation Status
  8. Work Log (additive — at least 3 entries from this phase)
  9. Commands Used
  10. Known Issues and Risks
  11. Assumptions
  12. Next-Step Handoff
- [ ] Bible's Section 12 (Next-Step Handoff) accurately describes the repo state a stranger would find
- [ ] Final handoff section is accurate
- [ ] `README.md` has setup + run instructions that actually work
- [ ] `docs/ARCHITECTURE.md`, `GAME_DESIGN.md`, `PROJECT_OVERVIEW.md`, `TASKS.md`, `CHANGELOG.md` all exist with real content
- [ ] Existing concept docs moved to `docs/`
- [ ] No doc says something is implemented that isn't

---

## 12. Implementation Sequence (for writing-plans)

Execute in this order to minimize broken states:

1. Create folder structure + move existing docs to `docs/`
2. Initialize `project.godot` with correct settings
3. Create `autoload/Events.gd`
4. Create `data/crops/wisdom_fruit.gd` (CropDefinition resource)
5. Create `actors/player/Player.tscn` + `player.gd` (movement only)
6. Create `scenes/world/GreenhouseSector.tscn` (TileMapLayers + player spawn)
7. Verify player moves in editor
8. Write `Starlight_Acre_bible.md` (sections 1–8, work log entry 1)
9. Write `README.md` and `docs/ARCHITECTURE.md`
10. Create `actors/crops/CropPlot.tscn` + `crop_plot.gd` (state machine + Area2D)
11. Place crop plots in GreenhouseSector, wire to Events
12. Create `systems/farming/farming_manager.gd` as child of GreenhouseSector (power drain timer + resource state)
13. Create `ui/hud/HUD.tscn` + `hud.gd`, wire to Events.resource_changed
14. Create `actors/terminals/RepairTerminal.tscn` + `repair_terminal.gd` and `ReplenishTerminal.tscn` + `replenish_terminal.gd` (both use Area2D + same interaction model as CropPlot); place in GreenhouseSector
15. Verify full crop loop end-to-end in editor
16. Write `docs/GAME_DESIGN.md`, `PROJECT_OVERVIEW.md`
17. Write `docs/TASKS.md`, `CHANGELOG.md`
18. Update `Starlight_Acre_bible.md` — sections 7, 8 (final work log), section 12 (handoff)
19. Final runthrough of all done criteria
