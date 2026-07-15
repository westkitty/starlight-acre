# Starlight Acre — Project Overview

## Vision

Starlight Acre is a small, polished, finishable orbital mythic farming station game. The player restores and cultivates a failing greenhouse aboard a deep-space station — tending mythic lifeforms drawn from ancient pantheons, managing fragile station systems, and gradually expanding into a self-sustaining mythic ecosystem.

This is not a generic farming clone, not a parody, and not a prototype. It is a serious indie project with a distinct identity: mythic sci-fi, restrained wonder, a station that remembers.

---

## Intended Feel

- **Atmospheric:** The station is a character. It hums, alerts, reacts.
- **Luminous:** Crops glow. The greenhouse is alive with bioluminescent light.
- **Purposeful:** Every action feeds the loop. Tending crops has meaning.
- **Restrained:** No grimdark, no aggressive humor, no overwhelming systems.
- **Mythic:** The plants are not ordinary. They are lifeforms tied to ancient powers.

---

## Player Experience Goals

1. Open the game and immediately understand: I am the caretaker of something fragile and extraordinary.
2. Within two minutes: plant a crop, watch it grow, harvest it.
3. Within five minutes: feel the tension of power drain against crop growth timing.
4. Within ten minutes: make your first meaningful station management decision.
5. Long-term: experience the satisfaction of a self-sustaining mythic orbital ecosystem.

---

## Current Implementation (Phase 1)

Phase 1 delivers a runnable vertical slice that proves the core identity of the game:

| System | Status | Notes |
|--------|--------|-------|
| Player movement | ✅ Done | Run, jump, coyote time, jump buffer |
| Wisdom Fruit lifecycle | ✅ Done | EMPTY→PLANTED→GROWING→READY→EMPTY |
| Power drain hazard | ✅ Done | Passive drain; growth halts at zero |
| Repair Terminal | ✅ Done | Restores power to 100% |
| Replenish Terminal | ✅ Done | Restores water + nutrients |
| HUD resource display | ✅ Done | Water, Nutrients, Power%, Wisdom Fruit count |
| Interaction prompt | ✅ Done | Context-sensitive E-prompt per interactable |
| Signal architecture | ✅ Done | Events autoload, decoupled systems |
| Project documentation | ✅ Done | Bible, architecture, game design docs |

---

## MVP Scope

The MVP proves these things and no more:
- This is a mythic orbital farming game
- The core resource tension (power drain vs. crop growth) is legible
- The interaction system (plant, tend, harvest, repair, replenish) is in place
- A new developer can open the project, read the docs, and understand what to build next

**The MVP is not:**
- A complete game
- A polished visual experience (Phase 2 integrates the pixel art asset pack)
- A multi-room experience (Phase 3)
- A multiplayer or networking project (never)

---

## Non-Goals (Permanent)

These are explicitly out of scope for all phases of this project:

- Multiplayer or networking
- Procedural generation of the station or crops
- Natural-language agent creation or LLM integration
- Deep colony simulation (agents are simple heuristic workers)
- Live-service features, DLC infrastructure, or analytics
- Complex natural-physics liquid simulation (use GPUParticles2D)
- Generic farming mechanics without mythic identity

---

## Implementation Priorities (Phase 2)

Ordered by value:

1. **Pixel art integration** — replace ColorRect placeholders with sprites from `assets/`
2. **TileMapLayer visual pass** — populate greenhouse tileset
3. **Gardener drone agent** — one agent type, two task types (tend + harvest)
4. **Trickster Vine** — second crop with distinct behavior
5. **Room transitions** — door triggers between two sectors
6. **Dexter the Stinkweasel** — docking event + simple trade UI
7. **Save/load** — JSON serialization of game state

---

## Technical Identity

| Property | Value |
|----------|-------|
| Engine | Godot 4.3 |
| Language | GDScript |
| View | 2D side-view |
| Art style | GBA/SNES pixel art (16-bit aesthetic) |
| Internal resolution | ~480×270 scaled up with Nearest filter |
| Structure | Room-as-scene, scene composition |
| Event system | Single Events autoload signal bus |
| Data format | Resource subclasses; JSON for tabular data |
