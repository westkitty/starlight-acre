# Orbital Mythic Farming Station Deep Research Reference Pack

## Scope and selection criteria

This research focuses on **finishable, beginner-friendly** Godot implementations that still demonstrate **clean architecture** and **system boundaries** suitable for iterative AI-assisted development (Claude Code, Codex, VS Code agents, Anti-Gravity-style workflows). The strongest pick list emphasizes repos that are (a) small enough to read end-to-end, (b) structured into obvious domains (player/world/ui/data/systems), and (c) show patterns that scale without turning into a “mega-sim.”

To keep *Orbital Mythic Farming Station* small while still feeling “deep,” the recommended architecture patterns below deliberately bias toward: **scene composition**, **signal/event decoupling**, **data-as-Resources**, and **room/sector loading** rather than one massive continuous world. Godot’s own documentation explicitly frames the engine as a **scene editor** (projects contain many scenes, with one main scene and reusable instanced scenes), which aligns well with modular iteration and AI-assisted refactors. citeturn45search5

## Starter projects and architecture patterns for Godot

### Godot architecture patterns worth adopting

**Signals for decoupling.** Godot docs describe signals as a delegation mechanism that lets one object react to another **without direct references**, reducing coupling and keeping code flexible. citeturn45search3turn45search0 For an AI-assisted codebase, this is gold: it reduces fragile “reach into the scene tree” assumptions that agents often break when adding features.

**Autoload singletons as stable “service roots.”** Godot’s Autoload system loads a script/scene into the root at runtime so it is always available; it also notes autoload nodes are not freed when changing scenes, so they’re appropriate for global services like sound, save managers, and event buses. citeturn45search1turn45search4turn45search10

**TileMapLayer-first design.** In modern Godot, `TileMapLayer` is positioned as the replacement for deprecated `TileMap`: it has a single layer, and you use **multiple TileMapLayer nodes** to get layered behavior. citeturn44search0turn44search1 This maps cleanly to your station: separate layers for “structure,” “pipes/cables,” “crops,” “decor,” “hazards,” “interaction markers,” etc.

**Event Bus / Events Autoload pattern (recommended).** GDQuest describes a commonly used pattern: a singleton (autoload) that **only emits signals**, letting distant nodes communicate without direct wiring. citeturn49search1 This is particularly effective for Orbital Mythic Farming Station because platformer exploration (player, hazards, doors) and farming/automation (crops, agents, storage) will otherwise become tightly entangled.

### Best open-source Godot starter projects (clean + AI-friendly)

**Godot Demo Projects (official).**  
**Project Name:** Godot demo projects  
**Repository/Source:** `github.com/godotengine/godot-demo-projects` citeturn31view3  
**Engine:** Godot (branches track stable vs. master; demos grouped by domain) citeturn31view3  
**System demonstrated:** Small focused demos for core engine systems (2D, GUI, loading, etc.). citeturn31view3  
**Why relevant:** Best “known-good” reference for file structure, minimal examples, and engine APIs without tutorial noise.  
**Implementation insight:** Repo organization is intentionally browsable by area (e.g., `2d/`, `gui/`, `loading/`), and the README explains how to scan/import all demos at once. citeturn31view3  
**Complexity:** Beginner → Intermediate (pick individual demos, not the whole set).

**Maaack’s Godot Game Template.**  
**Project Name:** Godot Game Template (Maaack)  
**Repository/Source:** `github.com/Maaack/Godot-Game-Template` citeturn48view1turn40view1  
**Engine:** Godot 4.6 (4.3+ compatible) citeturn48view1  
**System demonstrated:** Menus, pause/options, scene loader, persistent settings, “global config autoload,” lightweight saving/loading. citeturn48view1turn40view1  
**Why relevant:** Orbital Mythic Farming Station needs polish (menus, pause, options, saving) without you building infrastructure from scratch.  
**Implementation insight:** The README explicitly separates `base/` (core menu app), `extras/` (level loaders, win/lose, progress), and `examples/` (example game built via inherited scenes). citeturn48view1turn40view1  
**Complexity:** Intermediate (high leverage; you can use only the parts you need).

**Takin Godot Template (tooling-heavy, AI-friendly).**  
**Project Name:** Takin – Godot Template  
**Repository/Source:** `github.com/TinyTakinTeller/TakinGodotTemplate` citeturn40view0turn46view1  
**Engine:** Godot 4.4 template focus citeturn40view0  
**System demonstrated:** Save file system, localization, menu UI, project tooling/plugins, workflows/utilities. citeturn46view1  
**Why relevant:** The template’s emphasis on plugins and structured setup supports AI-assisted IDE workflows (formatters/linters reduce agent-generated style drift).  
**Implementation insight:** The “Get Started” guide explicitly instructs using the repo as a template, installing **GDScript Toolkit** for formatting/linting, enabling plugins, and restarting the project. citeturn48view0  
**Complexity:** Intermediate (excellent scaffolding; may include more tooling than you strictly need—trim aggressively).

**Awesome Godot list (discovery + curated templates).**  
**Project Name:** awesome-godot (curated list)  
**Repository/Source:** `github.com/godotengine/awesome-godot` citeturn41view0  
**Engine:** Godot ecosystem index  
**System demonstrated:** High-quality directory of templates and demos, including Maaack and Takin as explicit “Templates” entries. citeturn41view0  
**Why relevant:** Fast way to find vetted plugins (inventory, dialogue, AI tools) without random GitHub spelunking.  
**Implementation insight:** The list explicitly categorizes **Templates**, **Demos**, and **Plugins**, making it easier to keep OMFS small by picking only 1–2 foundations. citeturn41view0  
**Complexity:** Beginner (as a catalog).

## Platformer movement and traversal references

This section prioritizes controllers that are: one-file or small-module, configurable from the inspector, and consistent with modern Godot 4 `CharacterBody2D` usage (the canonical class for script-driven character movement). citeturn20search1turn45search5

### Clean, beginner-friendly controller implementations

**PlatformerController2D (formula-based jump, coyote/buffer).**  
**Project Name:** PlatformerController2D  
**Repository/Source:** `github.com/Ev01/PlatformerController2D` citeturn21view1turn22view2  
**Engine:** Godot 4.x (repo updated to 4.0 in changelog) citeturn21view1  
**System demonstrated:** Jump feel engineered from target *jump height* + *jump duration*, coyote time, jump buffer, double jump, asymmetric gravity, signals for jump/land. citeturn21view1turn22view2  
**Why relevant:** OMFS needs “Metroidvania-feel” traversal without spending months tuning physics constants. This controller encodes that tuning as parameters and formulas.  
**Implementation insight:** Uses timers created at runtime for coyote/jump-buffer windows, and exposes parameters (`max_jump_height`, `jump_duration`, etc.) while recalculating gravity/jump velocity when values change. citeturn22view2turn21view1  
**Complexity:** Intermediate (readable, but math-heavy; still beginner-usable).

**PlatformerCharacterController (single-file, toggle features in inspector).**  
**Project Name:** PlatformerCharacterController  
**Repository/Source:** `github.com/dragon1freak/PlatformerCharacterController` citeturn23view0turn26view0  
**Engine:** Godot 4.x (main branch) citeturn23view0  
**System demonstrated:** Coyote time, jump buffer, jump cancel, sprinting, wall jumping; designed as an extendable base class with overrideable functions. citeturn23view0turn26view0  
**Why relevant:** Strong fit for your “small but polished” target: one controller file, inspector toggles, and override points to customize without forking logic.  
**Implementation insight:** Splits work into `physics_tick()`, `handle_velocity()`, `handle_jump()`, etc., and implements coyote/buffer using `await get_tree().create_timer(...)` so you don’t have to manage Timer nodes manually. citeturn26view0  
**Complexity:** Beginner → Intermediate (great first controller).

**Godot2DCharacterController (feature-rich controller project).**  
**Project Name:** Godot2DCharacterController  
**Repository/Source:** `github.com/Kasu724/Godot2DCharacterController` citeturn7view1  
**Engine:** Godot (not fully verified from snippet; project layout suggests full game project) citeturn7view1  
**System demonstrated:** “Controller pack” style repo with separate `scenes/` and `scripts/` directories—useful when you want movement + interactions structured as multiple scripts instead of one file. citeturn7view1  
**Why relevant:** As OMFS grows, you’ll likely want to split “movement,” “abilities,” “interaction,” “inventory hooks” rather than a single monster `player.gd`. This repo’s folder split is a workable model.  
**Implementation insight:** Clear top-level separation (`assets/`, `scenes/`, `scripts/`) supports AI tools that navigate by folder semantics. citeturn7view1  
**Complexity:** Intermediate (evaluate before adopting; depends how complex the included controller is).

### Traversal abilities (grapple, ladders) with small implementations

**Spring grappling hook (tiny repo, readable).**  
**Project Name:** grappling-hook-2d  
**Repository/Source:** `github.com/curtjs/grappling-hook-2d` citeturn21view3turn22view0  
**Engine:** Godot 4.3 stated in repo description citeturn21view3  
**System demonstrated:** Grapple as a spring constraint using rest length, stiffness, damping. citeturn22view0  
**Why relevant:** Grappling is a classic Metroidvania upgrade; this is a compact reference that you can simplify further (e.g., no damping; fixed pull).  
**Implementation insight:** Uses a RayCast2D to acquire a target point, then applies spring force to player velocity when the rope is stretched beyond rest length; Line2D renders rope endpoint. citeturn22view0turn21view3  
**Complexity:** Intermediate (math-light; short code).

**Coyote Jump plugin (drop-in mechanic).**  
**Project Name:** Coyote Jump – Godot 4.x Plugin  
**Repository/Source:** `github.com/marianokpo/coyote_jump` citeturn21view2turn20search14  
**Engine:** Godot 4.x citeturn21view2  
**System demonstrated:** Adds coyote time and jump buffering. citeturn21view2  
**Why relevant:** If you roll your own controller, this provides a minimal target feature set for “responsive jump feel.”  
**Implementation insight:** Treated as a plugin to integrate into existing controllers (useful if you keep movement and “feel” mechanics modular). citeturn21view2  
**Complexity:** Beginner (conceptually simple), but plugin integration adds small overhead.

**Camera2D techniques writeup (smooth follow, shake, zoom).**  
**Project Name:** Camera2D Practical Techniques  
**Repository/Source:** `uhiyama-lab.com/en/notes/godot/camera2d-techniques/` citeturn20search11  
**Engine:** Godot 4.x (article context) citeturn20search11  
**System demonstrated:** Smooth follow, screen shake, dynamic zoom patterns for action/platformers. citeturn20search11  
**Why relevant:** OMFS needs “polish per dollar.” Camera work is one of the cheapest ways to improve feel.  
**Implementation insight:** Presents concrete GDScript code for common camera behaviors, suitable as a utility script/service approach. citeturn20search11  
**Complexity:** Beginner → Intermediate.

### Strong “starter kit” option

**2D Platformer – Starter Kit (Asset Library template).**  
**Project Name:** 2D Platformer – Starter Kit  
**Repository/Source:** Godot Asset Library entry `godotengine.org/asset-library/asset/2201` citeturn40view3  
**Engine:** Godot 4.4 (template category, metadata) citeturn40view3  
**System demonstrated:** “Juicy” controller, animated player, demo levels, level management, score, SFX; described as documented and beginner friendly. citeturn40view3  
**Why relevant:** If you want to get to “playable loop” fast, this template can be used as a scaffolding reference.  
**Implementation insight:** Asset metadata says scripts/functions are documented for comprehension. citeturn40view3  
**Complexity:** Beginner.  
**Flag:** **Template scope risk**—starter kits can tempt you into shipping a generic platformer; keep only movement + scene management.

## Metroidvania map, rooms, and progression references

Orbital Mythic Farming Station wants Metroidvania-style expansion, but with a station interior. The most “finishable” pattern is **room/sector scenes** + **door transitions** + **ability-gated interactions** (doors, vents, locked hatches) + **map reveal**.

### High-value metroidvania toolkit

iturn42image0

**Metroidvania System (MetSys) plugin (map editor + persistence + room transitions).**  
**Project Name:** Metroidvania System (MetSys)  
**Repository/Source:** `github.com/KoBeWi/Metroidvania-System` citeturn7view0turn30search3  
**Engine:** Godot 4.6+ (stated in README) citeturn7view0  
**System demonstrated:** Grid-room map editor, map viewer, room-to-scene association, collectible tracking, persistent object IDs, runtime save data dictionary, templates for scene transitions/minimaps/save management. citeturn7view0turn43view0  
**Why relevant:** If OMFS adopts a **grid-of-station-sectors** structure (each “module” or “wing” is a room/sector), MetSys can handle mapping and persistence scaffolding that beginners usually struggle with.  
**Implementation insight:**  
- The README describes a map editor with scene association to rooms, facilitating room transitions. citeturn7view0  
- It includes an automated persistent object ID system to track state (breakables, switches, collectibles) without hard-coded event enums. citeturn7view0  
- The wiki details map layers, symbols, cell groups, and scene assignment, supporting “parallel worlds / sub-maps” and map overlay concepts. citeturn43view0  
**Complexity:** Advanced (feature-rich).  
**Flag:** **Potential overkill** for a beginner unless you commit to a room-grid map early and use only a small subset.

### Beginner-scaled “room scenes + doors” approach (excellent for OMFS)

**Heartbeast Metroidvania Godot 4 project (minimal event bus + doors + rooms + save stations).**  
**Project Name:** metroidvania-godot-4  
**Repository/Source:** `github.com/uheartbeast/metroidvania-godot-4` citeturn31view0turn35view0turn38view0  
**Engine:** Godot 4.x (Godot 4-style APIs + `CharacterBody2D`; MIT licensed) citeturn31view0turn34view1  
**System demonstrated:**  
- **Room-as-scene** world layout with door transitions and “matching door connection” logic. citeturn36view0turn38view0  
- **Events bus** (`Events.gd`) that centralizes signals (screenshake, door entered, camera limit changes, player died). citeturn33view0turn31view0  
- Simple JSON save/load using a “WorldStash” key-value dictionary and `FileAccess`. citeturn33view1turn33view2  
- Checkpoint/save station that refills + saves on body entered. citeturn36view1  
**Why relevant:** This repo is a near-perfect blueprint for **station sectors**: each sector is a scene; doors connect sectors; sector scenes emit camera limits; save stations are interactable terminals; an Events autoload glues pieces without tight coupling.  
**Implementation insight:**  
- `Door` triggers only when the player overlaps *and* moves in the door’s direction (raycasts determine side), reducing accidental transitions. citeturn36view0  
- `World.change_levels()` loads the destination scene and uses a shared “connection” resource to find the matching destination door, then offsets player position—simple but robust. citeturn38view0turn36view0  
- The Events autoload is literally “signals only,” matching the GDQuest event-bus guidance. citeturn33view0turn49search1  
**Complexity:** Intermediate (very digestible; strong reference).

### Metroidvania demos and larger references (use selectively)

**GDQuest Open 2D Platformer (metroidvania-inspired, scope discipline).**  
**Project Name:** Godot Open 2D Platformer  
**Repository/Source:** `github.com/gdquest-demos/godot-platformer-2d` citeturn32view0  
**Engine:** Godot (original course references `KinematicBody2D`, indicating older Godot 3 era) citeturn32view0  
**System demonstrated:** Metroidvania-inspired room world, strong project organization, and a written philosophy emphasizing scope limits and focusing on controls and a small interconnected area. citeturn32view0  
**Why relevant:** The project’s design philosophy (avoid feature creep; focus on controls) matches OMFS constraints. citeturn32view0  
**Implementation insight:** Includes a `docs/` directory and concept doc within repo; strongly process-oriented. citeturn32view0  
**Complexity:** Intermediate.  
**Flag:** Uses older Godot architecture; use as design reference more than code reference.

**Toziuha Night (large open-source metroidvania).**  
**Project Name:** Toziuha Night – Order of the Alchemists  
**Repository/Source:** `github.com/dannygaray60/toziuha-night-oota` citeturn39view0  
**Engine:** Godot (published as Godot-made metroidvania) citeturn39view0  
**System demonstrated:** Full metroidvania game structure (non-linear maps, skills, enemies). citeturn39view0  
**Why relevant:** Good “what a bigger version looks like” reference—use for system inspiration (menus, progression, content packaging).  
**Implementation insight:** Repo notes **source code under MIT**, but assets are not free and the repo is archived/read-only—so treat as study material only. citeturn39view0  
**Complexity:** Advanced.  
**Flag:** **Overly complex** relative to OMFS goals.

## Farming, crops, inventory, and resources

For OMFS, the ideal farming system is **tile-based planting + timer-based growth + harvesting output** feeding into simple storage/automation. Avoid “realistic agronomy simulation.”

### Farming/crop systems implemented in Godot projects

**Pupi’s Farm (learning project with modular managers).**  
**Project Name:** Pupi’s Farm / 2D-Topdown-Farming-Game  
**Repository/Source:** `github.com/rehawild/2D-Topdown-Farming-Game` citeturn8view0  
**Engine:** Godot (GDScript) citeturn8view0  
**System demonstrated:** Plant/grow/harvest crops, inventory manager, tool manager, day/night cycle manager, scene manager, save/load system, NPC interactions. citeturn8view0  
**Why relevant:** The repo explicitly labels “game_manager,” “scene_manager,” “inventory_manager,” and a “growth_cycle_component,” which maps directly to OMFS needs. citeturn8view0  
**Implementation insight:** The README lists each system script by name, which is unusually helpful for AI assistants to locate the right file quickly. citeturn8view0  
**Complexity:** Beginner → Intermediate.  
**Flag:** No explicit license in repo (README states no license), so treat as inspiration only—don’t reuse code directly. citeturn8view0

**farmer-game (SimFarm-inspired crop model, likely too deep).**  
**Project Name:** farmer-game  
**Repository/Source:** `github.com/nilold/farmer-game` citeturn8view1  
**Engine:** Godot (GDScript) citeturn8view1  
**System demonstrated:** “Realistic” crop/environment/economic modeling (soil, weather, disease, etc.) with a dedicated `Crop.gd` and diagrams in docs. citeturn8view1  
**Why relevant:** Useful to study how someone tries to structure extensible crop logic and separate crop “cultivars,” but this is beyond OMFS scope. citeturn8view1  
**Implementation insight:** Repo has a strong engineering layout (`docs/`, tests, `.vscode`, diagrams), but the author explicitly notes performance/architecture pain when instantiating many crops. citeturn8view1  
**Complexity:** Advanced.  
**Flag:** **Overly complex** for OMFS; use only to learn what *not* to simulate.

### Inventory and resource systems suitable for a small-but-polished game

**GLoot (universal inventory system, strong documentation + examples).**  
**Project Name:** GLoot  
**Repository/Source:** `github.com/peter-kish/gloot` citeturn9view0  
**Engine:** Godot 4.4+ (stated) citeturn9view0  
**System demonstrated:** Item stacks, prototyped item definitions (“prototrees”), inventory constraints (grid/weight/item count), item slots, basic UI controls. citeturn9view0  
**Why relevant:** OMFS needs small inventory + storage (seed packets, harvest outputs, crafting parts). GLoot is modular: you can start with the simplest Inventory + Item stacks and ignore constraints/UI until later.  
**Implementation insight:** Item prototypes are stored in JSON and loaded as a Godot JSON resource; inventory UI controls are provided but optional. citeturn9view0  
**Complexity:** Intermediate (wide feature set, but can be adopted incrementally).

**Inventory System (expressobits) – explicit “logic vs UI separation.”**  
**Project Name:** Inventory System (Asset Library)  
**Repository/Source:** Godot Asset Library `godotengine.org/asset-library/asset/1650` citeturn9view2  
**Engine:** Godot 4.4 (metadata) citeturn9view2  
**System demonstrated:** Modular node-based inventory, items as Resources, multiplayer-compatible, explicitly “separate logic from UI.” citeturn9view2  
**Why relevant:** “Separate logic from UI” is a core principle for an AI-assisted codebase (agents can change mechanics without breaking UI scenes).  
**Implementation insight:** Asset description emphasizes Resources for item definitions and modular nodes. citeturn9view2  
**Complexity:** Beginner → Intermediate.

**GoGoGodot Inventory System (very advanced, architecture-heavy).**  
**Project Name:** Inventory System for Godot Engine 4 (GoGoGodot)  
**Repository/Source:** `inventory.gogogodot.io` citeturn9view1  
**Engine:** Godot 4 (site) citeturn9view1  
**System demonstrated:** Component-based architecture, data-driven configuration, multiplayer-first “server authoritative” orientation. citeturn9view1  
**Why relevant:** Architecture reference for clean boundaries and static typing discipline—not for direct implementation in OMFS unless multiplayer is planned.  
**Implementation insight:** The site emphasizes component-based composition and inspector configurability. citeturn9view1  
**Complexity:** Advanced.  
**Flag:** Likely **overkill** for OMFS (polish-first singleplayer).

## Building, automation, agents, and events

The key to keeping OMFS small is to treat these as **thin vertical slices**:

- Building placement: grid + validation + place/remove  
- Automation/agents: 2–3 job types, shallow priority, obvious UI  
- Events/vendors/hazards: events bus + dialogue + simple quest hooks  
- Save/load: JSON dictionary, later upgrade if needed

### Building/base construction (tile/grid placement)

**In-game Building System (GodotInGameBuildingSystem).**  
**Project Name:** GodotInGameBuildingSystem  
**Repository/Source:** `github.com/MarkoDM/GodotInGameBuildingSystem` citeturn49search2turn49search7  
**Engine:** Godot 4 (asset metadata says 4.3 template) citeturn49search7  
**System demonstrated:** Grid-based and free-form building, event bus communication, save/load (JSON default, supports encryption), basic UI, extensible architecture. citeturn49search2turn49search7  
**Why relevant:** Closest “station building” match: hybrid placement lets you keep crops on a grid while allowing decorative/utility placement later.  
**Implementation insight:** README-level notes emphasize a robust save/load system (JSON default + encryption) and an event bus for inter-system communication. citeturn49search2  
**Complexity:** Advanced for a beginner.  
**Flag:** Adopt **concepts** (event bus + placeable definitions + save/load boundaries), but avoid importing the entire system early.

**MarkoDM InGameBuildingSystem documentation note (import scripts + resource generation).**  
**Project Name:** markodm-GodotInGameBuildingSystem (doc/readme mirror)  
**Repository/Source:** `github.com/jaegerpicker/markodm-GodotInGameBuildingSystem/blob/main/Readme.md` citeturn49search0  
**Engine:** Godot  
**System demonstrated:** Asset import helper (`import_objects.gd`) that creates scenes/resources for placeables. citeturn49search0turn49search4  
**Why relevant:** OMFS will have repeated placeables (planters, pipes, machines). “Generate resource + scene wrapper for each placeable” is a scalable workflow.  
**Implementation insight:** The readme explicitly recommends wrapping each imported model in its own scene with a parent node—and mentions an import script that automates resource creation. citeturn49search4turn49search0  
**Complexity:** Intermediate.

**Grid Placement Plugin (commercial, but extremely relevant patterns).**  
**Project Name:** Grid Placement Plugin for Godot 4 (Chris’ Tutorials)  
**Repository/Source:** `chris-tutorials.itch.io/grid-placement-godot` citeturn49search3 and feature list `ko-fi.com/s/be6831ac01` citeturn49search6  
**Engine:** Godot 4 (TileMapLayer-based) citeturn49search3turn49search6  
**System demonstrated:** Grid-snapped placement, rotate/flip/move/demolish, placement validation rules, demo projects (top-down/isometric/platformer), API docs/tests. citeturn49search6turn49search3  
**Why relevant:** This is almost exactly the OMFS station-building need (grid placement in a platformer view).  
**Implementation insight:** The plugin touts centralized config (GBConfig), dependency injection, and extensive automated tests—signals strong modular design even if you don’t buy it. citeturn49search6turn49search3  
**Complexity:** Intermediate → Advanced.  
**Flag:** Not open-source; treat as “design reference” unless you choose to purchase.

**Colony Sim tutorial grid layer approach (multiple TileMapLayer + blueprint).**  
**Project Name:** colony-sim-tutorial  
**Repository/Source:** `github.com/davisbrandon02/colony-sim-tutorial` citeturn12view0turn19view0  
**Engine:** Godot 4 (stated in tutorial series; uses `TileMapLayer`) citeturn11search9turn19view0  
**System demonstrated:** Grid service that synchronizes multiple TileMapLayers (floor/building/plant/item/zone/blueprint) using a shared cell dictionary. citeturn19view0  
**Why relevant:** This is the best open reference found for “base-building layers” that could be adapted to a station interior.  
**Implementation insight:**  
- The grid script iterates used cells across layers, builds `Cell` objects, matches tile source IDs to “Type registries,” and updates the TileMapLayers accordingly. citeturn19view0  
- Uses a blueprint layer for unbuilt structures (a strong UX pattern for construction gameplay). citeturn19view0  
- Emits signals on tile click for selection/movement commands (clean separation between input detection and consumer systems). citeturn19view0  
**Complexity:** Intermediate.

### Automation/agents and “RimWorld-lite” task patterns

**Colony Sim tutorial task and pathfinding (small, instructive).**  
**Project Name:** colony-sim-tutorial (tasks + pathfinding modules)  
**Repository/Source:** same as above citeturn16view1turn18view0turn18view2  
**Engine:** Godot 4  
**System demonstrated:**  
- `Task` as a plain Object with `workRemaining` and a `workOnTask()` method; example subclass `HarvestTask`. citeturn18view0  
- Pathfinding service using `AStar2D`, mapping grid tiles to AStar point IDs, connecting navigable neighbors, optional debug draw. citeturn18view2  
**Why relevant:** OMFS automation can be kept small by using: `Task{type, target, work_remaining}` + `Agent{can_do_tags, speed}` + `TaskBoard` selection.  
**Implementation insight:** The tutorial’s folder organization separates domains (`scripts/Entity`, `scripts/Service`, `scripts/Task`), which is ideal for AI navigation and future refactors. citeturn14view0turn16view0turn16view1  
**Complexity:** Intermediate.

**Conceptual inspiration: RimWorld work priorities + ONI chore categories.**  
**Project Name:** RimWorld Work system (concept)  
**Source:** RimWorld Wiki “Work” citeturn10search1  
**System demonstrated:** Work types, manual priorities, assignment patterns. citeturn10search1  
**Why relevant:** OMFS can implement a simplified “work type priority” panel for station agents (e.g., Watering, Harvesting, Hauling).  
**Complexity:** Conceptual reference (no code).

**Project Name:** Oxygen Not Included choregroups (concept taxonomy)  
**Source:** ONI IDs “Choregroups” listing citeturn10search2  
**System demonstrated:** Clear categorical grouping of chores (build, tidy, farm, haul, etc.). citeturn10search2  
**Why relevant:** Useful as a checklist for **which job types not to implement** at first—pick 2–4 and stop.  
**Complexity:** Conceptual reference.

**LibColony (task scheduling library; study concepts only).**  
**Project Name:** libcolony  
**Repository/Source:** `github.com/mafik/libcolony` citeturn10search12  
**Engine:** C++/JS library (not Godot) citeturn10search12  
**System demonstrated:** General task scheduling for colony sims to reduce micromanagement. citeturn10search12  
**Why relevant:** Good mental model for a future “agent autonomy” upgrade (not for initial implementation).  
**Complexity:** Advanced.  
**Flag:** Not beginner-Godot-friendly; treat as reading.

### Event, vendor, hazard, and quest systems (keep these decoupled)

**Dialogue Manager (stateless branching dialogue; vendors).**  
**Project Name:** Dialogue Manager  
**Repository/Source:** `github.com/nathanhoad/godot_dialogue_manager` citeturn28search0turn28search4  
**Engine:** Godot 4.4+ (stated) citeturn28search0  
**System demonstrated:** Branching dialogue editor + runtime, “stateless” dialogue design. citeturn28search0  
**Why relevant:** Vendors and station events become easy: dialogue triggers fire signals; game systems respond via Events bus.  
**Implementation insight:** Repository includes `addons/dialogue_manager` and emphasizes structured tool/runtime separation. citeturn28search0turn28search12  
**Complexity:** Intermediate (powerful but well-trodden).

**QuestSystem (resource-based quests, modular).**  
**Project Name:** QuestSystem  
**Repository/Source:** `github.com/ShomyKohai/quest-system` citeturn28search1  
**Engine:** Godot 4.4+ (stated) citeturn28search1  
**System demonstrated:** Resource-based quests with modular addon design; intended compatibility with other addons. citeturn28search1  
**Why relevant:** OMFS “station expansion goals” can be expressed as small quest-like milestones (e.g., “Grow 10 mythic wheat,” “Power up Hydroponics Bay”).  
**Implementation insight:** The repo explicitly calls itself minimal/modular and resource-based. citeturn28search1  
**Complexity:** Intermediate.

**SignalBus plugin (global signals).**  
**Project Name:** SignalBus  
**Repository/Source:** `github.com/wokidoo/SignalBus` citeturn28search2  
**Engine:** Godot 4 (plugin) citeturn28search2  
**System demonstrated:** Create global signals accessible from anywhere. citeturn28search2  
**Why relevant:** Alternative to writing your own Events autoload; can standardize event naming and reduce wiring.  
**Implementation insight:** Directly described as enabling creation of global signals. citeturn28search2  
**Complexity:** Beginner → Intermediate.  
**Flag:** Plugins can hide complexity; for a beginner, a hand-written `Events.gd` like Heartbeast’s may be simpler. citeturn33view0

**Godot-in-practice Event Bus write-ups.**  
**Project Name:** GDQuest “Events bus singleton” article  
**Source:** gdquest.com tutorial citeturn49search1  
**System demonstrated:** Events autoload pattern rationale/benefits. citeturn49search1  
**Why relevant:** Provides “why” and “how” guidance for the exact decoupling OMFS needs.  
**Complexity:** Intermediate (design pattern reading).

**Project Name:** “Game Events” script article (Event Bus for Godot 4)  
**Source:** Nicola Dau blog post citeturn49search12  
**System demonstrated:** Loose coupling through global signals; cautions about complexity. citeturn49search12  
**Why relevant:** Reinforces the “use judiciously” warning—important for keeping OMFS small.  
**Complexity:** Beginner-friendly read.

### Saving/loading patterns (small game, reliable)

**Godot serialization demo (ConfigFile + JSON).**  
**Project Name:** Saving and Loading (Serialization) Demo  
**Repository/Source:** Godot Asset Library entry citeturn28search3 and demo folder in official demos citeturn28search7turn31view3  
**Engine:** Godot 4.2 demo (metadata) citeturn28search3  
**System demonstrated:** Save a simple game using ConfigFile and JSON formats. citeturn28search3turn28search7  
**Why relevant:** OMFS can start with dictionary→JSON saves (station layout, crop states, inventory) and evolve later.  
**Complexity:** Beginner.

**Heartbeast save model (JSON.stringify + WorldStash).**  
**Project Name:** metroidvania-godot-4 save/load  
**Repository/Source:** SaveManager + WorldStash scripts citeturn33view1turn33view2  
**Engine:** Godot 4  
**System demonstrated:** Simple save dictionary, stringify to file, load to restore level path and player position. citeturn33view1turn33view2  
**Why relevant:** This is a very “OMFS sized” save system—enough for a polished small game without building a full serialization framework.  
**Complexity:** Beginner → Intermediate.

**Godot docs: saving games complexity warning.**  
**Project Name:** Godot “Saving games” documentation  
**Source:** docs.godotengine.org citeturn49search17  
**System demonstrated:** Guidance that save games can become complicated and should scale with game complexity. citeturn49search17  
**Why relevant:** Validates OMFS’s need to start small and structure save data so it can grow later.  
**Complexity:** Beginner.

## Canvas append package

Below is **append-only content** designed to paste into **“Orbital Mythic Farming Station — Concept Document”** as new sections. It does **not** rewrite any existing text.

### Research Insight

**Systems and repos most aligned with OMFS constraints (small + finishable):**

A practical, beginner-feasible path is to combine (1) a clean `CharacterBody2D` controller with coyote/buffer, (2) room/sector scene loading with door transitions, and (3) a TileMapLayer-based station grid for crops/buildables. The strongest “small but polished” references are:

- `uheartbeast/metroidvania-godot-4` for **room scenes, doors, Events bus, camera limits, save stations, JSON save/load**. citeturn38view0turn36view0turn33view1turn33view0  
- `Ev01/PlatformerController2D` or `dragon1freak/PlatformerCharacterController` for **jump feel mechanics (coyote, buffer, wall jump, sprint) with clean override points**. citeturn22view2turn26view0  
- `davisbrandon02/colony-sim-tutorial` for **TileMapLayer multi-layer grids, blueprint layer, task objects, and AStar2D pathfinding structure**. citeturn19view0turn18view0turn18view2

### Architecture Reference

**Suggested OMFS repo layout (AI-assisted workflow friendly):**

Adopt folder semantics like:

- `scenes/` (gameplay scenes only; each station sector/room is a scene)  
- `actors/` (player, agents, hazards)  
- `systems/` (save/load, time, inventory, farming, construction, events)  
- `data/` (Resource definitions: crops, items, machines)  
- `ui/` (HUD, menus; keep UI scripts separate from gameplay logic)  
- `autoload/` (Events bus, SaveManager, maybe GameState)

This aligns with proven splits in tutorial repos that separate `scripts/Entity`, `scripts/Service`, and `scripts/Task` for readability and modularity. citeturn14view0turn16view0turn16view1

**Core decoupling rule:** Prefer signals/events over direct node references where possible. Godot describes signals as a method to reduce coupling, and an Events autoload pattern is widely used to broadcast global events cleanly. citeturn45search3turn49search1

### Implementation Pattern

**Minimal “Metroidvania station sectors” pattern (recommended):**

- Each station sector is a `Node2D` scene (“room-as-scene”).  
- Doors are `Area2D` with: `@export_file("*.tscn") var new_level_path` and a shared `connection` resource used to find matching destination doors; transition only triggers when the player moves into the door direction. citeturn36view0turn38view0  
- A lightweight `Events.gd` autoload defines global signals like `door_entered`, `camera_limits_changed`, `player_died`. citeturn33view0  
- Camera bounds are defined per-room using a hidden `Control`/`Panel` that emits bounds on `_ready()`. citeturn36view2

**Minimal station build + crop layer pattern (recommended):**

Use multiple `TileMapLayer` nodes rather than one complex TileMap (TileMap is deprecated; layered TileMapLayer is the modern approach). citeturn44search0turn44search1  
Mirror the colony-sim pattern: floor/building/plant/item/zone/blueprint layers with a single “Grid” service that updates tiles consistently and emits selection signals. citeturn19view0turn44search0

**Minimal automation/agents pattern (recommended):**

- Define `Task` as a plain Object with `workRemaining` and a completion callback/signal. citeturn18view0  
- Start with 2–3 task types (Water, Harvest, Haul).  
- Agents poll a `TaskManager` for the best available task based on distance + priority tag.

### Design Inspiration

**Polish-first traversal:** Implement coyote time + jump buffer (either via a controller base class or a small mechanic module) because it noticeably improves “feel” early. citeturn22view2turn26view0turn21view2

**Checkpoint terminals:** Save stations that trigger on area enter and call save/refill are a proven small-metroidvania pattern. citeturn36view1turn33view1

**Dialogue-driven vendors:** Dialogue Manager provides a stateless branching system suitable for vendor interactions (seed shop, mythic archivist, station AI). citeturn28search0turn28search4

### Future Expansion

**Optional “bigger map system” upgrade (only if needed):** MetSys provides a full map editor, persistent object IDs, room-to-scene linking, and VCS-friendly map data. It is powerful but likely overkill until OMFS has a stable room grid. citeturn7view0turn43view0

**Inventory scaling path:** Start with a minimal inventory (items as Resources + stacks). If you outgrow it, GLoot offers prototyped items and constraints with examples and UI controls you can adopt gradually. citeturn9view0turn9view2