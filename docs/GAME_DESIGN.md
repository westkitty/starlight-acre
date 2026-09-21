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
| EMPTY | Empty planter | E to plant (costs water + nutrients) |
| PLANTED | Sprout | — (waiting, brief) |
| GROWING | Growing crop | E to tend (reduces growth timer) |
| READY | Ready sprite + glow | E to harvest (yields produce) |

Growth pauses when station power reaches zero.

### Wisdom Fruit (MVP Crop)
- **Mythology:** Athena-inspired — cultivation supports research and upgrades
- **Growth time:** 30 seconds (base)
- **Tend bonus:** 20% timer reduction per tend
- **Cost:** 1 water, 1 nutrient to plant
- **Yield:** 1 Wisdom Fruit per harvest
- **Current visual:** `assets/sprites/crops/wisdom_fruit_states.png` (32×32px, 4 states) with ready-state glow from `assets/effects/pixel_art_effects.png`

### Trickster Vine (Second Crop — Implemented)
- **Mythology:** Loki-inspired — ripe fruit refuses the first clean harvest
- **Growth time:** 24 seconds (base)
- **Tend bonus:** 15% timer reduction per tend
- **Cost:** 1 water, 1 nutrient to plant
- **Ready behavior:** first harvest attempt spawns a separate Trickster Fruit entity that jumps 72px away; catch the escaped fruit to finish the harvest
- **Yield:** 1 Chaos
- **Automation rule:** Gardener Drone may tend it while growing but cannot auto-harvest/catch it
- **Persistence:** escaped fruit position/state survives room changes and save/relaunch
- **Current visual:** `assets/sprites/crops/trickster_vine_states.png` (32×32px, 4 states); fleeing fruit reuses the ready-state biological portion as its moving entity

### First Mythic Ecology Rule — Wisdom ↔ Trickster
- A GROWING Trickster Vine within 224px of a GROWING Wisdom Fruit can steal exactly one tending pulse per Trickster growth cycle.
- The stolen pulse applies the Wisdom tend's absolute time reduction to Trickster instead; Wisdom receives no reduction for that one interaction.
- This can be triggered by manual tending or Gardener Drone tending, making automation part of the ecology rather than exempt from it.
- The Trickster's spent-steal state persists across sector changes/save state and resets only on a new growth cycle.
- **Paradox Trellis** costs 3 Chaos at the Research Terminal. Once unlocked, a theft is caught and mirrored: both Wisdom and Trickster receive the tending reduction while the one-theft-per-cycle limit remains.

### Lightning Vine (Third Crop — Implemented)
- **Mythology:** Zeus-inspired — contained electrical biology grown as station infrastructure
- **Growth time:** 28 seconds (base)
- **Tend bonus:** 15% timer reduction per tend
- **Cost:** 1 water, 1 nutrient to plant
- **Yield:** 20 station power per harvest, capped at 100%
- **Solar Flare interaction:** each GROWING or READY Lightning Vine is a conductor that adds +2× to active Solar Flare drain. With one vine alive, a normal 5× flare becomes 7× until the vine is harvested or reset.
- **Automation:** Gardener Drone may tend and harvest it like an ordinary crop; this naturally shortens the conductor-risk window once it reaches READY.
- **Persistence:** growth state and remaining time use the normal plot-state save path, so conductor status survives room changes and save/relaunch as crop state.
- **Current visual:** canonical `C03_C001` at `assets/sprites/crops/lightning_vine_states.png` (32×32px, 4 states)

### Second Mythic Ecology Rule — Lightning ↔ Solar Flare
- Lightning Vine is both a renewable power source and a hazard amplifier.
- The active Solar Flare multiplier is `5 + (2 × conductive Lightning Vines)` before Efficient Grid mitigation.
- Harvesting a READY Lightning Vine immediately removes its +2× flare penalty and restores 20 power, making harvest timing matter during a warning or active flare.
- Flare warning/active station messages explicitly call out the conductive vine when present.

### Future Crops
- **Shadow Root** (Hades) — underground or hidden-zone cultivation
- **Golden Blossom** (Freya) — efficiency buffs and station attraction

---

## Resource Economy

| Resource | Source | Sink |
|----------|--------|------|
| Water | Replenish Terminal | Planting crops |
| Nutrients | Replenish Terminal | Planting crops |
| Power | Repair Terminal; Lightning Vine harvest (+20) | Passive drain; Solar Flare surge; required for crop growth |
| Wisdom Fruit | Wisdom Fruit harvest | Upgrades, progression currency |
| Chaos | Catching escaped Trickster Fruit | Paradox Trellis research (3 Chaos) |

**Current economy:**
- Power drains at ~0.333/second (100% lasts ~5 minutes)
- Replenish Terminal restores water and nutrients to their current caps of 10
- Repair Terminal restores power to 100%

**Planned additions:** Biomass, Refined Goods, Research Data, Anomaly Residue

---

## Agent System

Agents are simple heuristic workers — not AI, not simulated people. They execute task types in assigned zones.

**Current agent: Gardener Drone**
- Patrols the greenhouse
- Scans crop plots for actionable work
- Tends GROWING plots and harvests ordinary READY plots through public crop behavior
- Will tend Trickster Vine while growing but intentionally will not auto-catch its escaped fruit
- Does not water, schedule, pathfind across obstacles, or manage multiple sectors yet

Agent roles to follow in later phases: Engineer, Maintenance Drone, Harvester.

**Rule:** Natural-language agent creation is post-MVP. Not in Phase 1 or 2.

---

## Hazard System

### Current: Power Drain
Passive power drain at 0.333/second forces the player to visit the Repair Terminal periodically. Growth halts at zero power, creating a tension between tending crops and keeping the lights on.

### Solar Flare (Implemented)
- **Cadence:** 30s initial calm → 5s warning → 8s active flare → 45s recovery, then repeat.
- **Effect:** while active, station power drains at 5× the normal rate. Crop growth is affected indirectly only if power reaches zero; the flare does not delete crops or cause permanent random damage.
- **Mitigation:** Efficient Grid's existing 0.6 power-drain multiplier still applies during a flare.
- **Lightning Vine coupling:** each GROWING or READY Lightning Vine adds +2× to the active flare multiplier; one vine therefore raises 5× to 7× until harvested/reset.
- **Feedback:** station messages announce warning / active / clear states and the HUD displays the canonical V02 Solar Flare effect (cell 1 of `assets/effects/hazard_vfx.png`) during warning and active phases.
- **Continuity:** flare phase and remaining time survive sector transitions within the current run, but hazard timing is intentionally transient and is not serialized across quit/relaunch.

### Planned Hazards
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

**Planned implementation:** Docking event trigger, trade UI, rotating stock table.

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

## Current Phase 2 Work

| Element | Status |
|---------|--------|
| Player, crop, terminal, HUD, background sprite integration | ✅ Done |
| Gardener drone | ✅ Done |
| Ready-crop VFX | ✅ Done |
| Trickster Vine + flee/catch + Chaos output | ✅ Done |
| Wisdom ↔ Trickster Mythic Ecology + Paradox Trellis | ✅ Done |
| Lightning Vine + renewable power + Solar Flare conductor risk | ✅ Done |
| Greenhouse TileMapLayer painting and collision migration | ✅ Done and regression-verified |

## Post-MVP Roadmap

- **Trickster Vine (2nd crop)** — ✅ implemented: one bounded flee, separate catchable fruit entity, Chaos output, persisted escape state
- **Room transitions (2 sectors)** — ✅ implemented and regression-verified Greenhouse <-> Engineering
- **Dexter vendor encounter** — pending
- **Research progression** — ✅ implemented: Efficient Grid (4 Wisdom), Closed-Loop Hydroponics (6 Wisdom), Paradox Trellis (3 Chaos)
- **First Mythic Ecology proof** — ✅ implemented: one-shot Trickster theft of a neighboring Wisdom tend, upgraded to a shared pulse by Paradox Trellis
- **Save/load system** — ✅ implemented and regression-verified across a real quit/relaunch, including saved-sector resume
- **First station hazard: Solar Flare** — ✅ implemented: warning/active/recovery cadence, 5× active power drain, Efficient Grid mitigation, canonical V02 HUD feedback, cross-sector transient continuity
- **Lightning Vine (3rd crop)** — ✅ implemented: +20 renewable power harvest and +2× active-flare conductor risk while GROWING/READY
- **Audio (ambience + feedback sounds)** — pending
