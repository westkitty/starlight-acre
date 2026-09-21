# Starlight Acre

A compact orbital mythic farming-station game built in Godot 4.7. The player restores a failing station by cultivating mythic crops, managing finite emergency resources, automating repetitive work, researching station upgrades, and reopening adjacent sectors.

**Engine:** Godot 4.7.x
**Language:** GDScript
**View:** 2D side-view

## Current State

The repository now contains a runnable multi-sector progression slice.

Implemented:
- responsive player movement with coyote time and jump buffering
- data-driven crop definitions using Godot Resources
- Wisdom Fruit plant -> grow -> tend -> harvest lifecycle
- finite emergency resupplies, paid resupply fallback, and power repair cost
- two research upgrades paid with Wisdom Fruit
- recovered terminal sprites, HUD icons, and ready-crop VFX from the reverted July Phase 2 work
- Gardener Drone that physically travels to crops before tending or harvesting
- Greenhouse Sector plus Engineering Bay with bidirectional doors
- persistent resources, upgrades, crop state, current sector, and transition spawn state
- JSON save state at `user://save.json`
- Trickster Vine second crop with fleeing fruit, persistent Chaos resource, and one-shot Wisdom↔Trickster Mythic Ecology
- Paradox Trellis research upgrade (3 Chaos) that converts the Trickster theft into a shared tending pulse
- Godot 4.7.1 headless editor, smoke, and main-scene runtime validation
- normalized repository image assets so `.png` files contain actual PNG bytes
- canonical Greenhouse TileMap floor/walls with TileSet collision; obsolete StaticBody2D room stubs removed after regression proof
- 640×360 internal pixel-art viewport with a bounded player-follow camera and camera-synced sector backgrounds
- first recurring station hazard: Solar Flare (5s warning, 8s active, 5× active power drain, 45s recovery), with Efficient Grid mitigation and canonical hazard-VFX HUD feedback

Still incomplete:
- human visual QA of the promoted canonical sprite sheets and scene composition
- Dexter vendor
- audio and final feedback polish
- manual end-to-end playthrough in the Godot editor

## Core Loop

1. Check water, nutrients, power, and Wisdom Fruit.
2. Plant Wisdom Fruit using water and nutrients.
3. Tend crops manually or let the Gardener Drone travel to a valid crop.
4. Harvest Wisdom Fruit.
5. Spend produce on resupply, deep power repair, or research.
6. Enter Engineering and buy permanent station upgrades.
7. Return to the greenhouse with state preserved.

### Economy

The Replenish Terminal is no longer an infinite free fountain:
- two emergency resupplies are available initially;
- after they are exhausted, a full resupply costs 1 Wisdom Fruit;
- Closed-Loop Hydroponics makes resupply free and raises water/nutrient caps to 15.

Repairing power below 50% costs 1 Wisdom Fruit.

### Research

Engineering Bay contains the Research Terminal:
- **Efficient Grid** — 4 Wisdom Fruit, reduces passive power drain by 40%.
- **Closed-Loop Hydroponics** — 6 Wisdom Fruit, raises water/nutrient caps and removes resupply cost.

## Controls

| Action | Keys |
|---|---|
| Move | A / D or Left / Right |
| Jump | Space or Up |
| Interact | E |

## Run

```bash
godot --path .
```

Headless validation:

```bash
godot --headless --path . --editor --quit
godot --headless --path . --script tests/smoke_test.gd
godot --headless --path . --quit-after 120
```

## Architecture

```
autoload/
  Events.gd             signal bus only
  game_state.gd         persistent station state + JSON save/load
actors/
  agents/               spatial Gardener Drone
  crops/                crop plot lifecycle
  player/
  terminals/
data/crops/
  crop_definition.gd    reusable crop schema
  wisdom_fruit.tres     current crop data
systems/
  farming/
  world/                sector controller + doors
scenes/world/
  GreenhouseSector.tscn
  EngineeringBay.tscn
ui/hud/
tests/
```

Read `OPERATIONAL_STATE.md` first for current truth and `Starlight_Acre_bible.md` for additive project history.

*Tone: Mythic Sci-Fi. Restrained Wonder. A station that remembers.*
