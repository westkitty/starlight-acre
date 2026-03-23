# Starlight Acre — Game Design

## Core Concept

You are the Caretaker of a failing orbital greenhouse station. Your task is to restore the station's mythic crop cultivation, repair failing systems, and expand the station's capacity. The crops are not ordinary plants — they are lifeforms tied to the mythic traditions of ancient civilizations, and their growth has tangible effects on the station's systems and capabilities.

**Player fantasy:** A lone technician-cultivator tending a living, mythic ecosystem aboard a crumbling but hopeful station.

---

## Primary Game Loop

Each in-game cycle:

1. **Check station state** — power, water, nutrients, crop progress
2. **Tend crops** — interact to accelerate growth; harvest ready crops
3. **Manage resources** — use terminals to repair power, replenish water/nutrients
4. **Process output** — convert harvested produce into upgrades or station expansion
5. **Respond to hazards** — solar flares, mythic anomalies, system malfunctions
6. **Expand and unlock** — new sectors, new crop types, new agent assignments

---

## Controls

| Action | Key(s) |
|--------|--------|
| Move | A / D or ← → |
| Jump | Space / ↑ |
| Interact | E |

Movement has coyote time (0.1s) and jump buffer (0.1s) for responsive feel.

---

## Crop System

### Lifecycle
Each crop plot cycles through four states:

| State | Visual | Interaction |
|-------|--------|-------------|
| EMPTY | Gray | E to plant (costs water + nutrients) |
| PLANTED | Brown | — (waiting, brief) |
| GROWING | Green | E to tend (reduces growth timer) |
| READY | Gold/Glowing | E to harvest (yields produce) |

Growth pauses when station power reaches zero.

### Wisdom Fruit (MVP Crop)
- **Mythology:** Athena-inspired — cultivation supports research and upgrades
- **Growth time:** 30 seconds (base)
- **Tend bonus:** 20% timer reduction per tend
- **Cost:** 1 water, 1 nutrient to plant
- **Yield:** 1 Wisdom Fruit per harvest
- **Phase 2:** Sprite from `assets/sprites/crops/wisdom_fruit_states.png` (32×32px, 4 states)

### Future Crops (Post-MVP)
- **Trickster Vine** (Loki) — unstable harvest behavior, evasive
- **Lightning Vine** (Zeus) — supports energy/power systems
- **Shadow Root** (Hades) — underground or hidden-zone cultivation
- **Golden Blossom** (Freya) — efficiency buffs and station attraction

---

## Resource Economy

| Resource | Source | Sink |
|----------|--------|------|
| Water | Replenish Terminal | Planting crops |
| Nutrients | Replenish Terminal | Planting crops |
| Power | Repair Terminal | Passive drain; required for crop growth |
| Wisdom Fruit | Harvesting | Upgrades, progression currency |

**Phase 1 economy:**
- Power drains at ~0.333/second (100% lasts ~5 minutes)
- Replenish Terminal restores water to 5 and nutrients to 5
- Repair Terminal restores power to 100%

**Phase 2+ additions:** Biomass, Refined Goods, Research Data, Anomaly Residue

---

## Agent System (Phase 2+)

Agents are simple heuristic workers — not AI, not simulated people. They execute task types in assigned zones.

**Phase 2 target: Gardener Drone**
- Task types: Water, Tend, Harvest
- Assigned to a zone (one sector)
- One efficiency stat
- No scheduling complexity in Phase 2

Agent roles to follow in later phases: Engineer, Maintenance Drone, Harvester.

**Rule:** Natural-language agent creation is post-MVP. Not in Phase 1 or 2.

---

## Hazard System

### Phase 1: Power Drain (Active)
Passive power drain at 0.333/second forces the player to visit the Repair Terminal periodically. Growth halts at zero power, creating a tension between tending crops and keeping the lights on.

### Phase 2 Hazards
- **Solar Flare** — temporary power disruption, accelerated drain
- **Mythic Anomaly** — crop growth mutation (positive or negative)
- **System Malfunction** — random terminal offline for a period
- **Module Drift** — station sector connectivity issue

---

## Station Expansion (Phase 3+)

The station begins as a small greenhouse module. Expansion unlocks adjacent sectors.

| Module | Function |
|--------|----------|
| Greenhouse Sector | Starting area; crop cultivation |
| Hydroponics Wing | Water recycling; reduces replenish costs |
| Engineering Bay | Boosts repair efficiency |
| Energy Reactor | Reduces power drain rate |
| Archive Library | Unlocks research upgrades |
| Docking Bay | Enables Dexter's vendor visits |

---

## Vendor: Dexter the Stinkweasel

Dexter is a periodic visitor who arrives at the Docking Bay. He trades in rare seeds, unusual upgrades, and station components. His inventory reacts to station state and crop variety.

**Phase 2+ implementation:** Docking event trigger, trade UI, rotation stock table.

---

## Progression

| Phase | Player Goal |
|-------|-------------|
| Early | Repair basics, stabilize first crop, survive power drain |
| Mid | Unlock modules, manage multi-crop systems, exploit anomalies |
| Late | Self-sustaining mythic ecosystem, all crops cultivated |

**Win state options:**
- Soft completion: station becomes self-sustaining
- Cultivate all major mythic crops
- Complete full expansion tree
- Endless mode post-restoration milestone

---

## MVP Slice (Phase 1 — Complete)

| Element | Status |
|---------|--------|
| Player movement | ✅ Done |
| Wisdom Fruit lifecycle | ✅ Done |
| Power drain hazard | ✅ Done |
| Repair + Replenish terminals | ✅ Done |
| HUD resource display | ✅ Done |
| Interaction prompt system | ✅ Done |

## Post-MVP (Phase 2+)

- Pixel art sprite integration
- Gardener drone (1 agent, 2 task types)
- Trickster Vine (2nd crop)
- Room transitions (2 sectors)
- Dexter vendor encounter
- Save/load system
- Audio (ambience + feedback sounds)
