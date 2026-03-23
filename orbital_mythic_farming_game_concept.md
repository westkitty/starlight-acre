# Orbital Mythic Farming Station — Concept Document

## 1. Core Premise

A small, polished game where the player manages and expands a **space station dedicated to cultivating mythic plants** inspired by classical pantheons.

The player character lives on the station and performs hands‑on tasks while **agent-like station systems and constructs carry out assigned roles**.

The player orchestrates the ecosystem rather than micromanaging every action.

Key tone goals:

- Polished and finished feel
- Mythic + sci‑fi hybrid aesthetic
- Systems that feel alive and reactive

---

# 2. Core Gameplay Loop

Each in‑game day follows a cycle:

1. **Morning Planning Phase**

   - Player sets objectives for station agents
   - Assigns behaviors or roles
   - Determines priorities

2. **Execution Phase**

   - Agents perform their tasks automatically
   - Player character explores and interacts with the station

3. **Resource Phase**

   - Crops grow
   - Resources harvested
   - Systems powered

4. **Expansion Phase**

   - Build new station modules
   - Unlock new crops
   - Expand abilities

5. **Weekly Vendor Visit**

   - Dexter the Stinkweasel arrives as vendor
   - Sells rare items, upgrades, seeds

---

# 3. Perspective and Movement

Game is primarily:

**2D side‑view platform exploration of the station interior.**

Influence:

Metroidvania‑style navigation.

However:

- Focus is **station management + ecosystem orchestration**
- Exploration unlocks infrastructure rather than combat progression

Examples of movement abilities:

- Jet boots
- Climbing systems
- Grappling tools
- Maintenance drones

These abilities are powered by harvested crops.

---

# 4. The Station as a Character

The station is not just a location.

It acts as a **sentient or semi‑sentient system**.

Functions:

- Tutorial guidance
- Narrative flavor
- Feedback on player decisions
- Alerts for hazards

This avoids the player feeling alone in the world.

Primary characters become:

- The Player
- The Station
- Dexter the Vendor

---

# 5. Mythic Crop System

Plants are inspired by classical mythology.

Examples:

### Athena Crop

"Wisdom Fruit"

- Brain‑shaped fruit
- Used for research or upgrade systems

### Loki Crop

"Trickster Vine"

- Harvest attempts cause fruit to jump and flee

### Possible Other Pantheon Crops

- Zeus lightning vines
- Hades shadow roots
- Freya golden blossoms
- Anansi story seeds

Each plant produces:

- resources
- abilities
- upgrade materials

---

# 6. Agentic Station Systems

Agents are **not real AI models**.

They operate using **simple heuristic behaviors**.

Examples:

Agent roles:

- Gardener
- Engineer
- Maintenance drone
- Harvester

Each agent has:

- task priorities
- assigned zones
- efficiency stats

Player influence comes from:

- assigning tasks
- building tools
- upgrading modules

---

# 7. Natural Language Agent Creation

Optional advanced mechanic:

Players can describe an agent using natural language.

Example input:

"Create an agent that prioritizes harvesting Loki fruit and repairing nearby modules."

The system converts the request into:

- task priorities
- behavior weights

This bridges creative input and simple rule systems.

---

# 8. Station Expansion

The station begins as a **small orbital greenhouse module**.

Expansion unlocks new gameplay.

Possible modules:

- Hydroponics
- Mythic greenhouse domes
- Engineering bay
- Energy reactor
- Archive library
- Docking bay

Modules may introduce:

- new crops
- new hazards
- new station abilities

---

# 9. Resource Economy

Crops power the station.

Resource types:

- Energy fuel
- Ability fuel
- Construction materials
- Research points

Example usage:

Wisdom Fruit → unlock upgrades Lightning Vines → power movement tools Shadow Roots → power stealth systems

---

# 10. Hazards

Several threats challenge the station.

### Solar Flares

Temporarily disable modules.

### Cosmic Debris

Damages station sections.

### System Malfunctions

Agents behave unpredictably.

### Mythic Anomalies

Strange effects from powerful crops.

### Module Drift

Station pieces misalign and require repair.

---

# 11. Player Survival Systems

The player must maintain:

- food
- oxygen
- power

This creates stakes without overwhelming complexity.

---

# 12. Vendor System

Dexter the Stinkweasel arrives periodically.

Vendor functions:

- rare seeds
- strange upgrades
- station components

Dexter's inventory may react to:

- station growth
- crop variety
- player progress

---

# 13. Progression

Progression occurs through:

- station expansion
- crop discovery
- tool upgrades
- agent efficiency

Late game goal:

Create a **fully autonomous mythic orbital ecosystem**.

---

# 14. Possible Win Conditions

Possible completion states:

1. Fully self‑sustaining station
2. Cultivate every mythic crop
3. Complete full station expansion

---

# 15. Why This Idea Works

Compared to typical farming games:

This concept adds:

- orbital setting
- mythic crop themes
- station expansion
- agent orchestration
- exploration platform gameplay

The result is a hybrid of:

- farming
- automation
- exploration

---

# 16. Development Strategy

Recommended order of development:

1. Basic station platform map
2. Simple crop growth system
3. Harvesting mechanics
4. Agent task system
5. Station expansion modules
6. Hazard events
7. Vendor system
8. Visual polish

Focus on **mechanics first, visuals later**.

---

# 17. Key Design Goal

A **small, finishable game** that feels alive, unusual, and polished.

---

# 18. Core Gameplay Loop Diagram

```mermaid
flowchart LR

A[Morning Planning]
B[Agents Execute Tasks]
C[Player Exploration]
D[Resource Harvest]
E[Station Expansion]
F[Weekly Vendor Visit]

A --> B
B --> C
C --> D
D --> E
E --> A
E --> F
F --> A
```

This loop keeps the game structured while allowing emergent behavior from agents.

---

# 19. Station Module Tree

Example progression tree:

```
Orbital Greenhouse (Starting Module)
│
├─ Hydroponics Wing
│   ├─ Athena Research Garden
│   └─ Zeus Lightning Cultivation Bay
│
├─ Engineering Bay
│   ├─ Drone Workshop
│   └─ Reactor Maintenance
│
├─ Energy Reactor
│   ├─ Solar Amplifier
│   └─ Mythic Energy Converter
│
└─ Docking Bay
    ├─ Dexter Vendor Dock
    └─ Trade Cargo Module
```

Each module unlocks:

- new crops
- new agent roles
- new hazards

---

# 20. Crop Pantheon Table

| Crop           | Pantheon | Behavior              | Gameplay Use      |
| -------------- | -------- | --------------------- | ----------------- |
| Wisdom Fruit   | Athena   | Brain-shaped fruit    | Research upgrades |
| Trickster Vine | Loki     | Fruits run away       | Chaos resource    |
| Lightning Vine | Zeus     | Emits electrical arcs | Power systems     |
| Shadow Root    | Hades    | Grows underground     | Stealth systems   |
| Golden Blossom | Freya    | Attracts agents       | Efficiency buffs  |

These crops create both **visual identity** and **mechanical variety**.

---

# 21. Minimal Godot Prototype Plan (First 2 Weeks)

### Week 1 — Core Movement + Station

Goals:

- Basic 2D player movement
- Simple station interior
- Basic plant growth timer

Tasks:

1. Create player controller
2. Create one greenhouse room
3. Implement plant object
4. Add growth timer
5. Allow harvesting

End of Week 1 Result:

Player can walk around a station and harvest a crop.

---

### Week 2 — Basic Systems

Goals:

- Simple agent prototype
- Resource storage
- Station expansion tile

Tasks:

1. Create basic agent behavior
2. Implement simple task system
3. Add resource inventory
4. Allow building one new module

End of Week 2 Result:

Player can:

- harvest crops
- assign one agent task
- build one new station module

---

# 22. Mechanics Risk Analysis

### Risk 1 — Agent Complexity

Agent systems can spiral into large simulation complexity.

Mitigation:

Keep agents extremely simple.

Use priority lists instead of complex AI.

---

### Risk 2 — Scope Expansion

Station modules and crop systems can grow endlessly.

Mitigation:

Limit initial release to:

- 5 crops
- 6 station modules

---

### Risk 3 — Visual Overhead

Large station art requirements could slow development.

Mitigation:

Use modular tile sets.

Reuse assets heavily.

---

### Risk 4 — Player Isolation

Only having player + Dexter risks an empty world.

Mitigation:

Station AI acts as narrative voice.

Agents have personality hints.

---

### Risk 5 — Mechanic Clarity

Players may not understand the orchestration system.

Mitigation:

Station tutorial voice guides early gameplay.

---

# 23. Honest Scope Evaluation

**Short answer: yes, the idea as currently described is somewhat overscoped.**

However, the *core of the idea is not.*

The dangerous expansions are:

- complex agent orchestration
- natural language agent creation
- large mythic crop systems
- full station expansion trees

A **finishable version** would be:

- 1 station
- 3 crops
- 2 hazards
- 1 agent type
- Dexter vendor

That version is realistic for a first project.

Everything else should be treated as **future expansion ideas**, not part of the first release.

If scoped correctly, this could still be a **very strong beginner Godot project**.

