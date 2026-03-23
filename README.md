# Starlight Acre

A small, polished orbital mythic farming station game built in Godot 4.x.

You restore and cultivate a failing orbital greenhouse-station that grows mythic lifeforms inspired by classical pantheons. Explore the station side-view, tend crops, manage power, and build toward a self-sustaining ecosystem.

---

## Status

**Phase 1 — Bootstrap:** In planning. Implementation plan ready.

See `docs/superpowers/plans/2026-03-22-starlight-acre-bootstrap.md` for the full plan.

---

## Stack

| Item | Choice |
|------|--------|
| Engine | Godot 4.x |
| Language | GDScript |
| Perspective | 2D side-view |
| Art | Placeholder colored rects |

---

## Setup

1. Install [Godot 4.x](https://godotengine.org/download/)
2. Clone this repo
3. Open Godot → Import → select `project.godot`
4. Run the entry scene (`scenes/world/GreenhouseSector.tscn`)

> **Note:** `project.godot` does not exist yet — Phase 1 implementation is in progress.

---

## Folder Overview

```
actors/       Player, crops, terminals
autoload/     Events.gd signal bus
data/         Crop definitions (CropDefinition resource)
docs/         Architecture, game design, project overview, changelog
scenes/       World rooms and test scenes
systems/      FarmingManager (power drain + resource state)
ui/           HUD
assets/       Placeholder art
```

---

## MVP

Phase 1 delivers:
- Player moves left/right, jumps (coyote time + jump buffer)
- Wisdom Fruit crop lifecycle: plant → grow → tend → harvest
- Power drains passively; repair terminal restores it
- Replenish terminal restores Water + Nutrient
- HUD shows all resources

Full done criteria: `docs/superpowers/specs/2026-03-22-starlight-acre-bootstrap-design.md` § 11

---

## Roadmap

- **Phase 1:** Bootstrap — scaffold + player movement + crop loop + power hazard
- **Phase 2:** Room transitions, second crop, vertical traversal
- **Phase 3:** Agents / drones, station expansion modules
- **Phase 4:** Dexter vendor, save/load, progression
