# Starlight Acre Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a runnable Godot 4.x project where the player can move through a greenhouse room, plant a Wisdom Fruit crop, tend it, harvest it, and manage a power-drain hazard — with all handoff documentation written.

**Architecture:** Scaffold-first (folder structure → Godot project → player movement) then docs alongside, then crop mechanics, then HUD and terminals. One autoload (`Events.gd`) acts as a pure signal bus. All interactables (crop plots, terminals) are instanced scenes with Area2D entry/exit registering exactly one active interactable on the player at a time. Resource state lives in `FarmingManager`, a child node of `GreenhouseSector`.

**Tech Stack:** Godot 4.x, GDScript, 2D side-view, CharacterBody2D, Area2D, ColorRect placeholders, no external libraries.

**Spec:** `docs/superpowers/specs/2026-03-22-starlight-acre-bootstrap-design.md`

---

## File Map

| File | Role |
|------|------|
| `project.godot` | Engine config — name, main scene, autoload, input actions |
| `autoload/Events.gd` | Signal bus — emits only, no state, no logic |
| `data/crops/wisdom_fruit.gd` | `CropDefinition` Resource class with Wisdom Fruit defaults |
| `actors/player/player.gd` | CharacterBody2D movement + interactable registration |
| `actors/player/Player.tscn` | Player scene — CharacterBody2D, visual, collision |
| `actors/crops/crop_plot.gd` | Crop state machine (EMPTY→PLANTED→GROWING→READY→EMPTY) |
| `actors/crops/CropPlot.tscn` | Crop plot scene — Node2D, ColorRect, Area2D |
| `actors/terminals/repair_terminal.gd` | Restores power to 100% on interact |
| `actors/terminals/RepairTerminal.tscn` | Terminal scene — Node2D, ColorRect, Area2D |
| `actors/terminals/replenish_terminal.gd` | Restores Water + Nutrient to cap on interact |
| `actors/terminals/ReplenishTerminal.tscn` | Terminal scene — Node2D, ColorRect, Area2D |
| `systems/farming/farming_manager.gd` | Resource state (water, nutrient, power, fruit) + power drain |
| `ui/hud/hud.gd` | Listens to Events, updates 4 resource labels + prompt label |
| `ui/hud/HUD.tscn` | CanvasLayer — HUD bar + interaction prompt label |
| `scenes/world/GreenhouseSector.tscn` | Entry scene — room, player spawn, crop plots, terminals, HUD |
| `Starlight_Acre_bible.md` | Additive project ledger (created early, updated 4x) |
| `README.md` | Setup + run instructions |
| `docs/ARCHITECTURE.md` | Engine choice, folder map, autoload policy |
| `docs/GAME_DESIGN.md` | Core loop, crop system, MVP def, post-MVP list |
| `docs/PROJECT_OVERVIEW.md` | Vision, feel, non-goals |
| `docs/TASKS.md` | Next tasks + blockers |
| `docs/CHANGELOG.md` | Bootstrap entry |

---

## Chunk 1: Foundation

### Task 1: Folder Structure

**Files:**
- Create: all top-level directories
- Move: `orbital_mythic_farming_game_concept.md` → `docs/`
- Move: `deep-research-report.md` → `docs/`

- [ ] **Step 1.1: Create directory tree**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
mkdir -p scenes/world scenes/test
mkdir -p actors/player actors/crops actors/terminals
mkdir -p systems/farming
mkdir -p autoload
mkdir -p data/crops
mkdir -p ui/hud
mkdir -p assets/placeholder
```

- [ ] **Step 1.2: Move existing concept docs into docs/**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
mv orbital_mythic_farming_game_concept.md docs/
mv deep-research-report.md docs/
```

- [ ] **Step 1.3: Verify structure**

```bash
find "/Users/andrew/Projects/Starlight Acre" -type d | sort
```

Expected output: all directories above present, `docs/` contains the two moved files.

- [ ] **Step 1.4: Commit**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
git add -A
git commit -m "chore: scaffold folder structure, move concept docs to docs/"
```

---

### Task 2: project.godot + Input Actions

**Files:**
- Create: `project.godot`

`project.godot` is a plain-text INI-style config file. Write it exactly as shown — Godot will accept it and will auto-assign UIDs and additional metadata on first open.

- [ ] **Step 2.1: Write project.godot**

Create `/Users/andrew/Projects/Starlight Acre/project.godot`:

```ini
; Engine configuration file.
; Generated for Starlight Acre — edit via Project Settings in the Godot editor.

config_version=5

[application]

config/name="Starlight Acre"
config/description="Orbital mythic farming station — grow mythic crops, manage station resources, survive the void."
run/main_scene="res://scenes/world/GreenhouseSector.tscn"
config/features=PackedStringArray("4.3", "GL Compatibility")

[autoload]

Events="*res://autoload/Events.gd"

[input]

move_left={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":65,"key_label":0,"unicode":97,"location":0,"echo":false,"script":null)
, Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":4194319,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)
]
}
move_right={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":68,"key_label":0,"unicode":100,"location":0,"echo":false,"script":null)
, Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":4194321,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)
]
}
jump={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":32,"key_label":0,"unicode":32,"location":0,"echo":false,"script":null)
, Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":4194320,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)
]
}
interact={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":69,"key_label":0,"unicode":101,"location":0,"echo":false,"script":null)
]
}
```

Input bindings:
- `move_left`: A / Left Arrow
- `move_right`: D / Right Arrow
- `jump`: Space / Up Arrow
- `interact`: E

- [ ] **Step 2.2: Commit**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
git add project.godot
git commit -m "chore: add project.godot with input map and autoload declaration"
```

---

### Task 3: Events Autoload

**Files:**
- Create: `autoload/Events.gd`

This is the only autoload. It emits signals. It holds no state and runs no logic.

- [ ] **Step 3.1: Write Events.gd**

Create `autoload/Events.gd`:

```gdscript
# Events.gd
# Global signal bus. Emits signals only — no state, no logic.
# All gameplay systems communicate through these signals.
# Add new signals here as Phase 2+ features are introduced.
extends Node

## Emitted when a crop plot changes state.
## plot_id: the plot's unique string ID
## new_state: one of "EMPTY", "PLANTED", "GROWING", "READY"
signal crop_state_changed(plot_id: String, new_state: String)

## Emitted when any tracked resource changes value.
## resource_name: "water", "nutrient", "power", "wisdom_fruit"
## new_value: current numeric value
signal resource_changed(resource_name: String, new_value: float)

## Emitted by player.gd when the active interactable changes.
## prompt_text: display string like "E — Plant Wisdom Fruit"
## Empty string means no active interactable — hide the prompt.
signal interaction_prompt_changed(prompt_text: String)
```

- [ ] **Step 3.2: Commit**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
git add autoload/Events.gd
git commit -m "feat: add Events autoload signal bus"
```

---

### Task 4: Crop Definition Resource

**Files:**
- Create: `data/crops/wisdom_fruit.gd`

This file defines the `CropDefinition` class (used by `CropPlot`) and hard-codes Wisdom Fruit values. In Phase 2, this becomes a base class with separate `.tres` instances per crop.

- [ ] **Step 4.1: Write wisdom_fruit.gd**

Create `data/crops/wisdom_fruit.gd`:

```gdscript
# wisdom_fruit.gd
# CropDefinition Resource — defines all data for a crop type.
# Phase 1: this file IS the CropDefinition class AND the Wisdom Fruit data.
# Phase 2: split into CropDefinition base class + separate .tres resource files per crop.
class_name CropDefinition
extends Resource

## Human-readable name shown in HUD and logs.
var crop_name: String = "Wisdom Fruit"

## Time in seconds for the crop to grow from PLANTED to READY.
var growth_time: float = 30.0

## Fraction of remaining growth_timer removed when tending (0.2 = 20% faster).
var tend_bonus: float = 0.2

## Resources spent at planting time.
var water_cost: int = 1
var nutrient_cost: int = 1

## Number of harvest items produced per harvest.
var harvest_yield: int = 1

## Placeholder ColorRect colors per crop state.
var color_empty: Color = Color(0.45, 0.45, 0.45)
var color_planted: Color = Color(0.30, 0.20, 0.10)
var color_growing: Color = Color(0.20, 0.65, 0.20)
var color_ready: Color = Color(1.00, 0.85, 0.10)
```

- [ ] **Step 4.2: Commit**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
git add data/crops/wisdom_fruit.gd
git commit -m "feat: add CropDefinition resource class with Wisdom Fruit defaults"
```

---

## Chunk 2: Player + Room

### Task 5: Player Script + Scene

**Files:**
- Create: `actors/player/player.gd`
- Create: `actors/player/Player.tscn`

The player is a `CharacterBody2D` with:
- Left/right movement at 200 px/s
- Jump with 0.1s coyote time and 0.1s jump buffer
- A `current_interactable` reference updated by Area2D enter/exit signals from interactable scenes
- `register_interactable` / `unregister_interactable` methods called by interactables
- `_unhandled_input` fires `current_interactable.interact()` on `interact` press

- [ ] **Step 5.1: Write player.gd**

Create `actors/player/player.gd`:

```gdscript
# player.gd
# CharacterBody2D — handles movement, jumping, and interactable registration.
# Interactables (CropPlot, terminals) call register/unregister_interactable()
# when the player enters or exits their Area2D.
extends CharacterBody2D

const SPEED := 200.0
const JUMP_VELOCITY := -420.0
const GRAVITY := 980.0
const COYOTE_DURATION := 0.1
const JUMP_BUFFER_DURATION := 0.1

var _coyote_timer := 0.0
var _jump_buffer_timer := 0.0
var _current_interactable: Node = null


func _physics_process(delta: float) -> void:
	# Apply gravity when airborne.
	if not is_on_floor():
		velocity.y += GRAVITY * delta

	# Coyote time: allows jumping briefly after walking off a ledge.
	if is_on_floor():
		_coyote_timer = COYOTE_DURATION
	else:
		_coyote_timer -= delta

	# Jump buffer: queues a jump if Space is pressed slightly before landing.
	if Input.is_action_just_pressed("jump"):
		_jump_buffer_timer = JUMP_BUFFER_DURATION
	else:
		_jump_buffer_timer -= delta

	# Execute jump when buffer is active and coyote window is open.
	if _jump_buffer_timer > 0.0 and _coyote_timer > 0.0:
		velocity.y = JUMP_VELOCITY
		_coyote_timer = 0.0
		_jump_buffer_timer = 0.0

	# Horizontal movement.
	velocity.x = Input.get_axis("move_left", "move_right") * SPEED

	move_and_slide()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("interact") and _current_interactable != null:
		_current_interactable.interact()


## Called by an interactable's Area2D body_entered signal.
## Sets this as the active interactable and updates the interaction prompt.
func register_interactable(node: Node) -> void:
	_current_interactable = node
	Events.interaction_prompt_changed.emit(node.get_prompt())


## Called by an interactable's Area2D body_exited signal.
## Clears the active interactable only if it is the one that just exited.
func unregister_interactable(node: Node) -> void:
	if _current_interactable == node:
		_current_interactable = null
		Events.interaction_prompt_changed.emit("")
```

- [ ] **Step 5.2: Write Player.tscn**

Create `actors/player/Player.tscn`:

```
[gd_scene load_steps=3 format=3]

[ext_resource type="Script" path="res://actors/player/player.gd" id="1_player"]

[sub_resource type="CapsuleShape2D" id="CapsuleShape2D_body"]
radius = 14.0
height = 42.0

[node name="Player" type="CharacterBody2D" groups=["player"]]
script = ExtResource("1_player")

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
position = Vector2(0, -21)
shape = SubResource("CapsuleShape2D_body")

[node name="Visual" type="ColorRect" parent="."]
offset_left = -14.0
offset_top = -42.0
offset_right = 14.0
offset_bottom = 0.0
color = Color(0.25, 0.55, 1.0, 1.0)
```

Note on scene format: Godot will assign UIDs and may adjust minor formatting on first open. This is expected and harmless.

- [ ] **Step 5.3: Commit**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
git add actors/player/
git commit -m "feat: add Player scene and script with movement, coyote time, jump buffer"
```

---

### Task 6: GreenhouseSector Room

**Files:**
- Create: `scenes/world/GreenhouseSector.tscn`

This is the entry scene. It contains:
- Background `ColorRect` (dark teal, full viewport)
- Three `TileMapLayer` nodes (empty/placeholder — replaced with real tiles in Phase 2)
- `StaticBody2D` floor platform (wide, solid, provides collision)
- `StaticBody2D` left and right wall boundaries
- `FarmingManager` node (child of this scene — see Task 7)
- `Player` instance
- A `Marker2D` spawn point
- Slots for CropPlot and Terminal instances (added in Tasks 8–12)

**Why StaticBody2D instead of TileMapLayer for collision:** TileMapLayer requires a configured TileSet to paint collision tiles. Setting up a TileSet programmatically in a text scene file is error-prone. The `StaticBody2D` approach gives solid collision immediately, and TileMapLayer nodes are present for visual layering in Phase 2. This is documented in `ARCHITECTURE.md`.

- [ ] **Step 6.1: Write GreenhouseSector.tscn**

Create `scenes/world/GreenhouseSector.tscn`:

```
[gd_scene load_steps=3 format=3]

[ext_resource type="PackedScene" path="res://actors/player/Player.tscn" id="1_player"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_floor"]
size = Vector2(1200, 32)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_wall"]
size = Vector2(32, 600)

[node name="GreenhouseSector" type="Node2D"]

[node name="Background" type="ColorRect" parent="."]
offset_left = -600.0
offset_top = -400.0
offset_right = 600.0
offset_bottom = 400.0
color = Color(0.05, 0.10, 0.12, 1.0)

[node name="TileMapLayer_Background" type="TileMapLayer" parent="."]

[node name="TileMapLayer_Floor" type="TileMapLayer" parent="."]

[node name="TileMapLayer_Walls" type="TileMapLayer" parent="."]

[node name="Floor" type="StaticBody2D" parent="."]
position = Vector2(0, 280)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Floor"]
shape = SubResource("RectangleShape2D_floor")

[node name="FloorVisual" type="ColorRect" parent="Floor"]
offset_left = -600.0
offset_top = -16.0
offset_right = 600.0
offset_bottom = 16.0
color = Color(0.20, 0.30, 0.25, 1.0)

[node name="WallLeft" type="StaticBody2D" parent="."]
position = Vector2(-616, 0)

[node name="CollisionShape2D" type="CollisionShape2D" parent="WallLeft"]
shape = SubResource("RectangleShape2D_wall")

[node name="WallRight" type="StaticBody2D" parent="."]
position = Vector2(616, 0)

[node name="CollisionShape2D" type="CollisionShape2D" parent="WallRight"]
shape = SubResource("RectangleShape2D_wall")

[node name="PlayerSpawn" type="Marker2D" parent="."]
position = Vector2(-400, 230)

[node name="Player" parent="." instance=ExtResource("1_player")]
position = Vector2(-400, 230)

[node name="FarmingManager" type="Node" parent="."]
```

Note: `FarmingManager` node has no script yet — the script is attached in Task 7.

- [ ] **Step 6.2: Verify player movement**

Open Godot 4 editor:
```
File → Open Project → navigate to /Users/andrew/Projects/Starlight Acre → select project.godot
```

Run the project (F5 or the Play button). Expected:
- Dark teal room visible
- Player (blue rectangle) spawns on the left side of the floor
- A/D or Left/Right arrow keys move the player
- Space or Up arrow jumps; walk off floor edge and tap Space just after leaving — player still jumps (coyote time)
- Player cannot pass through floor or walls

If errors appear in the Godot Output panel, fix them before continuing.

- [ ] **Step 6.3: Write initial Starlight_Acre_bible.md (Work Log entry 1)**

After the room and player are verified, create `Starlight_Acre_bible.md` at the repo root with the following 12 section headings. Fill sections 1–8 with what is known at this point. Leave section 12 as a stub ("TODO: update at phase end"). Task 13 will complete and finalize the document.

Minimum content for each section at this stage:
- **Section 1 — Project Identity:** Name, one-paragraph summary, target experience, "Phase 1 in progress"
- **Section 2 — Project Purpose:** What the game is, what experience it delivers, current implementation goal
- **Section 3 — Current Stack:** Table of engine/language/perspective/structure/decoupling/art/save choices with rationale
- **Section 4 — Repository Map:** Annotated folder tree reflecting what currently exists
- **Section 5 — Architecture Decisions:** At minimum: engine choice, Events autoload, FarmingManager as child node, single active interactable rule, StaticBody2D for collision
- **Section 6 — Game Definition Snapshot:** Player fantasy, initial playable space, first crop (Wisdom Fruit), first hazard (power drain), out-of-scope list
- **Section 7 — Implementation Status:** Table with Done/In Progress/Not Started for every planned system
- **Section 8 — Work Log:** Entry for this session — date, objective, actions taken so far, files created, next step
- **Section 9 — Commands Used:** Stub with `godot4 --path "..."` and git commands used so far
- **Section 10 — Known Issues and Risks:** StaticBody2D stub, no save/load, no art — with severity
- **Section 11 — Assumptions:** At minimum: Godot 4.x installed, Area2D default layers, `farming_manager` group
- **Section 12 — Next-Step Handoff:** `TODO: update at phase end`

- [ ] **Step 6.4: Commit**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
git add scenes/world/GreenhouseSector.tscn Starlight_Acre_bible.md
git commit -m "feat: add GreenhouseSector entry scene with floor, walls, player spawn"
```

---

## Chunk 3: Crop System + Farming Manager

### Task 7: FarmingManager

**Files:**
- Create: `systems/farming/farming_manager.gd`

`FarmingManager` is a plain `Node` child of `GreenhouseSector` (not an autoload). It owns:
- Session resource state (water, nutrient, wisdom_fruit, power)
- The passive power drain (`_process`)
- Methods called by crop plots and terminals to modify state

Crop plots and terminals access it via `get_tree().get_first_node_in_group("farming_manager")`. The node must be added to the `farming_manager` group in the scene.

- [ ] **Step 7.1: Write farming_manager.gd**

Create `systems/farming/farming_manager.gd`:

```gdscript
# farming_manager.gd
# Owns all session resource state and the passive power drain.
# Lives as a child Node of GreenhouseSector (not an autoload).
# Added to group "farming_manager" so interactables can find it without direct wiring.
extends Node

const WATER_MAX := 10
const NUTRIENT_MAX := 10
const POWER_DRAIN_PER_SECOND := 0.333  # ~1% per 3 seconds

var water: int = 5
var nutrient: int = 5
var wisdom_fruit: int = 0
var power: float = 100.0


func _ready() -> void:
	add_to_group("farming_manager")
	_broadcast_all()


func _process(delta: float) -> void:
	power = maxf(0.0, power - POWER_DRAIN_PER_SECOND * delta)
	Events.resource_changed.emit("power", power)


# --- Read ---

func can_plant(water_cost: int, nutrient_cost: int) -> bool:
	return water >= water_cost and nutrient >= nutrient_cost


# --- Write ---

func spend_water(amount: int) -> void:
	water = maxi(0, water - amount)
	Events.resource_changed.emit("water", float(water))


func spend_nutrient(amount: int) -> void:
	nutrient = maxi(0, nutrient - amount)
	Events.resource_changed.emit("nutrient", float(nutrient))


func add_wisdom_fruit(amount: int) -> void:
	wisdom_fruit += amount
	Events.resource_changed.emit("wisdom_fruit", float(wisdom_fruit))


func restore_power() -> void:
	power = 100.0
	Events.resource_changed.emit("power", power)


func replenish_consumables() -> void:
	water = WATER_MAX
	nutrient = NUTRIENT_MAX
	Events.resource_changed.emit("water", float(water))
	Events.resource_changed.emit("nutrient", float(nutrient))


func _broadcast_all() -> void:
	Events.resource_changed.emit("water", float(water))
	Events.resource_changed.emit("nutrient", float(nutrient))
	Events.resource_changed.emit("wisdom_fruit", float(wisdom_fruit))
	Events.resource_changed.emit("power", power)
```

- [ ] **Step 7.2: Attach script to FarmingManager node**

Open `scenes/world/GreenhouseSector.tscn` in the Godot editor. Select the `FarmingManager` node. In the Inspector, attach the script `res://systems/farming/farming_manager.gd`. Save the scene.

Alternatively, add the script reference directly in the `.tscn` file. Append this line to the `[node name="FarmingManager" ...]` entry:

```
[node name="FarmingManager" type="Node" parent="."]
script = preload("res://systems/farming/farming_manager.gd")
```

In Godot 4 text scenes, preload does not work in `.tscn` directly — use the editor to assign the script, or modify the `.tscn` to reference it as an ext_resource:

Add to the ext_resource section:
```
[ext_resource type="Script" path="res://systems/farming/farming_manager.gd" id="2_fm"]
```

Update the FarmingManager node line:
```
[node name="FarmingManager" type="Node" parent="."]
script = ExtResource("2_fm")
```

Update `load_steps` in the header from 4 to 5.

- [ ] **Step 7.3: Commit**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
git add systems/farming/farming_manager.gd scenes/world/GreenhouseSector.tscn
git commit -m "feat: add FarmingManager with resource state and power drain"
```

---

### Task 8: CropPlot Scene + Script

**Files:**
- Create: `actors/crops/crop_plot.gd`
- Create: `actors/crops/CropPlot.tscn`

State machine: `EMPTY → PLANTED → GROWING → READY → EMPTY`

The CropPlot:
- Has a `ColorRect` visual that changes color per state
- Has an `Area2D` with a `RectangleShape2D` — when the player body enters, calls `player.register_interactable(self)`; on exit, calls `player.unregister_interactable(self)`
- Loads a `CropDefinition` instance from `wisdom_fruit.gd`
- Accesses `FarmingManager` via group lookup
- Pauses growth when power = 0 (listens to `Events.resource_changed`)
- Emits `Events.crop_state_changed` on every state transition

- [ ] **Step 8.1: Write crop_plot.gd**

Create `actors/crops/crop_plot.gd`:

```gdscript
# crop_plot.gd
# Manages a single crop plot's lifecycle: EMPTY → PLANTED → GROWING → READY → EMPTY.
# Interactable: register/unregister called by Area2D body signals.
# Visual: ColorRect changes color per state.
# Growth pauses when FarmingManager's power reaches 0.
extends Node2D

enum State { EMPTY, PLANTED, GROWING, READY }

## Unique identifier emitted with crop_state_changed signals.
@export var plot_id: String = "plot_0"

@onready var _visual: ColorRect = $Visual
@onready var _area: Area2D = $Area2D

var _state: State = State.EMPTY
var _growth_timer: float = 0.0
var _power_available: bool = true
var _crop: CropDefinition


func _ready() -> void:
	_crop = CropDefinition.new()  # Wisdom Fruit defaults
	Events.resource_changed.connect(_on_resource_changed)
	_apply_visual()


func _process(delta: float) -> void:
	if _state != State.GROWING or not _power_available:
		return
	_growth_timer -= delta
	if _growth_timer <= 0.0:
		_set_state(State.READY)


# --- Interactable interface ---

func interact() -> void:
	match _state:
		State.EMPTY:   _try_plant()
		State.GROWING: _tend()
		State.READY:   _harvest()


func get_prompt() -> String:
	match _state:
		State.EMPTY:   return "E — Plant Wisdom Fruit (1 Water, 1 Nutrient)"
		State.GROWING: return "E — Tend"
		State.READY:   return "E — Harvest"
	return ""


# --- Actions ---

func _try_plant() -> void:
	var fm := _get_farming_manager()
	if fm == null:
		return
	if not fm.can_plant(_crop.water_cost, _crop.nutrient_cost):
		return
	fm.spend_water(_crop.water_cost)
	fm.spend_nutrient(_crop.nutrient_cost)
	_growth_timer = _crop.growth_time
	_set_state(State.PLANTED)
	# Brief PLANTED pause before growth begins, giving visual feedback.
	await get_tree().create_timer(0.5).timeout
	if _state == State.PLANTED:
		_set_state(State.GROWING)


func _tend() -> void:
	# Reduce remaining growth time by tend_bonus fraction.
	_growth_timer -= _growth_timer * _crop.tend_bonus
	_growth_timer = maxf(0.0, _growth_timer)


func _harvest() -> void:
	var fm := _get_farming_manager()
	if fm != null:
		fm.add_wisdom_fruit(_crop.harvest_yield)
	_set_state(State.EMPTY)


# --- State management ---

func _set_state(new_state: State) -> void:
	_state = new_state
	_apply_visual()
	Events.crop_state_changed.emit(plot_id, State.keys()[new_state])


func _apply_visual() -> void:
	match _state:
		State.EMPTY:   _visual.color = _crop.color_empty
		State.PLANTED: _visual.color = _crop.color_planted
		State.GROWING: _visual.color = _crop.color_growing
		State.READY:   _visual.color = _crop.color_ready


# --- Signals ---

func _on_resource_changed(resource_name: String, value: float) -> void:
	if resource_name == "power":
		_power_available = value > 0.0


func _on_area_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.register_interactable(self)


func _on_area_body_exited(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.unregister_interactable(self)


# --- Helpers ---

func _get_farming_manager() -> Node:
	return get_tree().get_first_node_in_group("farming_manager")
```

- [ ] **Step 8.2: Write CropPlot.tscn**

Create `actors/crops/CropPlot.tscn`:

```
[gd_scene load_steps=3 format=3]

[ext_resource type="Script" path="res://actors/crops/crop_plot.gd" id="1_cropplot"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_crop"]
size = Vector2(40, 40)

[node name="CropPlot" type="Node2D"]
script = ExtResource("1_cropplot")

[node name="Visual" type="ColorRect" parent="."]
offset_left = -20.0
offset_top = -40.0
offset_right = 20.0
offset_bottom = 0.0
color = Color(0.45, 0.45, 0.45, 1.0)

[node name="Area2D" type="Area2D" parent="."]

[node name="CollisionShape2D" type="CollisionShape2D" parent="Area2D"]
shape = SubResource("RectangleShape2D_crop")

[connection signal="body_entered" from="Area2D" to="." method="_on_area_body_entered"]
[connection signal="body_exited" from="Area2D" to="." method="_on_area_body_exited"]
```

- [ ] **Step 8.3: Commit**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
git add actors/crops/
git commit -m "feat: add CropPlot scene and state machine (EMPTY→PLANTED→GROWING→READY)"
```

---

### Task 9: Place Crop Plots in GreenhouseSector

**Files:**
- Modify: `scenes/world/GreenhouseSector.tscn`

Add three CropPlot instances to the room, positioned on the floor. Each gets a unique `plot_id`.

- [ ] **Step 9.1: Update GreenhouseSector.tscn — add CropPlot instances**

Add CropPlot as an ext_resource and add three instances. Modify `GreenhouseSector.tscn`:

At the top, add to the ext_resource section:
```
[ext_resource type="PackedScene" path="res://actors/crops/CropPlot.tscn" id="3_cropplot"]
```

Update `load_steps` to reflect the new count.

At the bottom, add:
```
[node name="CropPlot0" parent="." instance=ExtResource("3_cropplot")]
position = Vector2(-200, 238)
plot_id = "plot_0"

[node name="CropPlot1" parent="." instance=ExtResource("3_cropplot")]
position = Vector2(0, 238)
plot_id = "plot_1"

[node name="CropPlot2" parent="." instance=ExtResource("3_cropplot")]
position = Vector2(200, 238)
plot_id = "plot_2"
```

Note: `plot_id` is an `@export` property on the CropPlot script. Set it in the scene as shown.

- [ ] **Step 9.2: Verify crop plots appear in editor**

Open the scene in the Godot editor. The three crop plots (grey rectangles) should appear on the floor platform.

- [ ] **Step 9.3: Commit**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
git add scenes/world/GreenhouseSector.tscn
git commit -m "feat: place three CropPlot instances in GreenhouseSector"
```

---

## Chunk 4: HUD + Terminals

### Task 10: HUD

**Files:**
- Create: `ui/hud/hud.gd`
- Create: `ui/hud/HUD.tscn`

HUD is a `CanvasLayer` (always rendered on top). It contains:
- A top bar with four `Label` nodes: Water, Nutrient, Power, Wisdom Fruit
- An interaction prompt `Label` near the bottom center (hidden when `prompt_text` is empty)

Listens to `Events.resource_changed` and `Events.interaction_prompt_changed`.

- [ ] **Step 10.1: Write hud.gd**

Create `ui/hud/hud.gd`:

```gdscript
# hud.gd
# Renders the resource bar (Water, Nutrient, Power, Wisdom Fruit)
# and the interaction prompt label.
# Driven entirely by Events signals — no direct coupling to game nodes.
extends CanvasLayer

@onready var _water_label: Label = $TopBar/WaterLabel
@onready var _nutrient_label: Label = $TopBar/NutrientLabel
@onready var _power_label: Label = $TopBar/PowerLabel
@onready var _fruit_label: Label = $TopBar/FruitLabel
@onready var _prompt_label: Label = $PromptLabel


func _ready() -> void:
	Events.resource_changed.connect(_on_resource_changed)
	Events.interaction_prompt_changed.connect(_on_prompt_changed)
	_prompt_label.visible = false


func _on_resource_changed(resource_name: String, value: float) -> void:
	match resource_name:
		"water":
			_water_label.text = "Water: %d/10" % int(value)
		"nutrient":
			_nutrient_label.text = "Nutrient: %d/10" % int(value)
		"power":
			_power_label.text = "Power: %d%%" % int(value)
		"wisdom_fruit":
			_fruit_label.text = "Wisdom Fruit: %d" % int(value)


func _on_prompt_changed(prompt_text: String) -> void:
	_prompt_label.visible = not prompt_text.is_empty()
	_prompt_label.text = prompt_text
```

- [ ] **Step 10.2: Write HUD.tscn**

Create `ui/hud/HUD.tscn`:

```
[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://ui/hud/hud.gd" id="1_hud"]

[node name="HUD" type="CanvasLayer"]
script = ExtResource("1_hud")
layer = 10

[node name="TopBar" type="HBoxContainer" parent="."]
anchor_right = 1.0
offset_top = 8.0
offset_bottom = 40.0
offset_left = 8.0
offset_right = -8.0

[node name="WaterLabel" type="Label" parent="TopBar"]
size_flags_horizontal = 3
text = "Water: 5/10"

[node name="NutrientLabel" type="Label" parent="TopBar"]
size_flags_horizontal = 3
text = "Nutrient: 5/10"

[node name="PowerLabel" type="Label" parent="TopBar"]
size_flags_horizontal = 3
text = "Power: 100%"

[node name="FruitLabel" type="Label" parent="TopBar"]
size_flags_horizontal = 3
text = "Wisdom Fruit: 0"

[node name="PromptLabel" type="Label" parent="."]
anchor_left = 0.5
anchor_right = 0.5
anchor_bottom = 1.0
anchor_top = 1.0
offset_left = -150.0
offset_right = 150.0
offset_top = -60.0
offset_bottom = -30.0
horizontal_alignment = 1
text = ""
visible = false
```

- [ ] **Step 10.3: Add HUD to GreenhouseSector**

Add to `GreenhouseSector.tscn` ext_resource section:
```
[ext_resource type="PackedScene" path="res://ui/hud/HUD.tscn" id="4_hud"]
```

Add instance at the bottom of the node list:
```
[node name="HUD" parent="." instance=ExtResource("4_hud")]
```

Update `load_steps` count.

- [ ] **Step 10.4: Commit**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
git add ui/hud/ scenes/world/GreenhouseSector.tscn
git commit -m "feat: add HUD with resource bar and interaction prompt"
```

---

### Task 11: Repair Terminal

**Files:**
- Create: `actors/terminals/repair_terminal.gd`
- Create: `actors/terminals/RepairTerminal.tscn`

Restores power to 100% when the player interacts. Uses the same Area2D pattern as CropPlot.

- [ ] **Step 11.1: Write repair_terminal.gd**

Create `actors/terminals/repair_terminal.gd`:

```gdscript
# repair_terminal.gd
# Interactable terminal that restores power to 100% when activated.
# Uses Area2D body_entered/exited to register with the player.
extends Node2D


func interact() -> void:
	var fm := get_tree().get_first_node_in_group("farming_manager")
	if fm != null:
		fm.restore_power()


func get_prompt() -> String:
	return "E — Repair Power Systems"


func _on_area_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.register_interactable(self)


func _on_area_body_exited(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.unregister_interactable(self)
```

- [ ] **Step 11.2: Write RepairTerminal.tscn**

Create `actors/terminals/RepairTerminal.tscn`:

```
[gd_scene load_steps=3 format=3]

[ext_resource type="Script" path="res://actors/terminals/repair_terminal.gd" id="1_repair"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_repair"]
size = Vector2(36, 48)

[node name="RepairTerminal" type="Node2D"]
script = ExtResource("1_repair")

[node name="Visual" type="ColorRect" parent="."]
offset_left = -18.0
offset_top = -48.0
offset_right = 18.0
offset_bottom = 0.0
color = Color(0.9, 0.4, 0.1, 1.0)

[node name="Area2D" type="Area2D" parent="."]

[node name="CollisionShape2D" type="CollisionShape2D" parent="Area2D"]
shape = SubResource("RectangleShape2D_repair")

[connection signal="body_entered" from="Area2D" to="." method="_on_area_body_entered"]
[connection signal="body_exited" from="Area2D" to="." method="_on_area_body_exited"]
```

- [ ] **Step 11.3: Commit**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
git add actors/terminals/repair_terminal.gd actors/terminals/RepairTerminal.tscn
git commit -m "feat: add RepairTerminal (restores power)"
```

---

### Task 12: Replenish Terminal

**Files:**
- Create: `actors/terminals/replenish_terminal.gd`
- Create: `actors/terminals/ReplenishTerminal.tscn`

Restores Water and Nutrient to cap when the player interacts.

- [ ] **Step 12.1: Write replenish_terminal.gd**

Create `actors/terminals/replenish_terminal.gd`:

```gdscript
# replenish_terminal.gd
# Interactable terminal that restores Water and Nutrient to cap.
# Uses Area2D body_entered/exited to register with the player.
extends Node2D


func interact() -> void:
	var fm := get_tree().get_first_node_in_group("farming_manager")
	if fm != null:
		fm.replenish_consumables()


func get_prompt() -> String:
	return "E — Replenish Water & Nutrients"


func _on_area_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.register_interactable(self)


func _on_area_body_exited(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.unregister_interactable(self)
```

- [ ] **Step 12.2: Write ReplenishTerminal.tscn**

Create `actors/terminals/ReplenishTerminal.tscn`:

```
[gd_scene load_steps=3 format=3]

[ext_resource type="Script" path="res://actors/terminals/replenish_terminal.gd" id="1_replenish"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_replenish"]
size = Vector2(36, 48)

[node name="ReplenishTerminal" type="Node2D"]
script = ExtResource("1_replenish")

[node name="Visual" type="ColorRect" parent="."]
offset_left = -18.0
offset_top = -48.0
offset_right = 18.0
offset_bottom = 0.0
color = Color(0.2, 0.6, 0.9, 1.0)

[node name="Area2D" type="Area2D" parent="."]

[node name="CollisionShape2D" type="CollisionShape2D" parent="Area2D"]
shape = SubResource("RectangleShape2D_replenish")

[connection signal="body_entered" from="Area2D" to="." method="_on_area_body_entered"]
[connection signal="body_exited" from="Area2D" to="." method="_on_area_body_exited"]
```

- [ ] **Step 12.3: Place terminals in GreenhouseSector**

Add both terminals as ext_resources in `GreenhouseSector.tscn`:
```
[ext_resource type="PackedScene" path="res://actors/terminals/RepairTerminal.tscn" id="5_repair"]
[ext_resource type="PackedScene" path="res://actors/terminals/ReplenishTerminal.tscn" id="6_replenish"]
```

Add instances (positioned right of the crop plots, on the floor):
```
[node name="RepairTerminal" parent="." instance=ExtResource("5_repair")]
position = Vector2(420, 232)

[node name="ReplenishTerminal" parent="." instance=ExtResource("6_replenish")]
position = Vector2(500, 232)
```

Update `load_steps` count.

- [ ] **Step 12.4: Full end-to-end verification**

Run the project in Godot. Work through this checklist manually:

1. HUD shows: Water 5/10, Nutrient 5/10, Power 100%, Wisdom Fruit 0
2. Watch Power — it should decrease over time
3. Walk player to a grey crop plot — prompt appears: "E — Plant Wisdom Fruit (1 Water, 1 Nutrient)"
4. Press E — plot turns dark brown (PLANTED), Water and Nutrient drop to 4/10 in HUD
5. After ~0.5s, plot turns green (GROWING)
6. Stand near the green plot, press E — plot stays green but growth will complete sooner
7. Wait for plot to turn gold (READY)
8. Press E near gold plot — HUD shows Wisdom Fruit: 1; plot returns to grey (EMPTY)
9. Walk to the orange terminal (RepairTerminal) — prompt: "E — Repair Power Systems"
10. Press E — Power jumps back to 100%
11. Walk to the blue terminal (ReplenishTerminal) — prompt: "E — Replenish Water & Nutrients"
12. Press E — Water returns to 10/10, Nutrient returns to 10/10
13. Plant again — no resources wasted; prompt hides when player walks away

If any step fails, debug before proceeding to documentation.

- [ ] **Step 12.5: Commit**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
git add actors/terminals/ scenes/world/GreenhouseSector.tscn
git commit -m "feat: add ReplenishTerminal, complete interactable system and crop loop"
```

---

## Chunk 5: Documentation

### Task 13: Starlight_Acre_bible.md (Full + Final Update)

**Files:**
- Create/Update: `Starlight_Acre_bible.md`

Write all 12 required sections. The early sections were started in Task 6 — now complete the full document including the final Work Log entries (this session) and Section 12 (Next-Step Handoff).

- [ ] **Step 13.1: Write Starlight_Acre_bible.md**

Create `/Users/andrew/Projects/Starlight Acre/Starlight_Acre_bible.md` with all 12 sections:

```markdown
# Starlight Acre — Project Bible

> This file is an additive handoff ledger. Never delete prior entries.
> Append new sessions as new dated sections.

---

## 1. Project Identity

**Project name:** Starlight Acre

**Summary:** Starlight Acre is a small, polished, finishable orbital mythic farming station game. The player lives on a decaying space station and restores it by cultivating mythic plants inspired by classical pantheons. The player orchestrates an ecosystem — eventually delegating tasks to simple heuristic agents — rather than micromanaging every action forever. The tone is atmospheric, slightly uncanny, luminous, and mythic-meets-sci-fi. It is not a farming clone and not a platformer. It is both.

**Target experience:** Restoring a failing orbital greenhouse into a self-sustaining mythic ecosystem. A calm but purposeful game where every day has a rhythm.

**Current phase:** Phase 1 — Bootstrap complete. First vertical slice implemented.

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
└── assets/placeholder/        No art assets yet
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
Impact: TileMapLayer nodes exist in GreenhouseSector (FloorLayer, WallLayer, BackgroundLayer) for architectural intent, but they are empty. Phase 2 will populate them with real tiles and remove the StaticBody2D stubs.
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

**Current hazard set:** Power drain. Passive drain at ~1%/3s. Pauses crop growth at 0%. Repaired by RepairTerminal. No dramatic event, no animation — resource bar IS the hazard communication.

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
| Agents (Phase 2) | Not started |
| Dexter vendor (Phase 3) | Not started |
| Second room / room transitions | Not started |
| Save / load | Not started |
| Real art / tiles | Not started |
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
- Verified full crop loop end-to-end in Godot editor
- Wrote all documentation

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
| No real art assets — placeholder ColorRects only | Expected | By design for Phase 1 |
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

**Current repo state:** Runnable Godot 4 project. Open project.godot in Godot 4 editor, run with F5. Player moves in a dark greenhouse room. Three crop plots (grey = empty). Two terminals (orange = repair, blue = replenish). Passive power drain. Full crop lifecycle functional. All docs written.

**What should happen next (Phase 2 priorities):**

1. **Gardener drone agent** — One simple heuristic agent that tends and harvests crops on a timer. No deep scheduling. One task type only (Water/Tend). This proves the orchestration identity of the game.
2. **TileMapLayer visual pass** — Set up a basic TileSet, paint the floor and walls with proper tiles, remove StaticBody2D stubs (or keep for collision and add TileMapLayer for visuals above them).
3. **Second crop: Trickster Vine** — Implement the fleeing harvest behavior as a separate mechanic. Requires a new CropDefinition and a new CropPlot variant or subclass.
4. **Room transitions** — Add one adjacent sector. Implement door interactable that loads the new scene. Player retains inventory state (requires moving FarmingManager to a scene-persistent location or introducing a lightweight GameState autoload).
5. **Dexter the Stinkweasel** — Simple trade UI. Appears on a timer. Sells seeds. No inventory management depth needed yet.

**Top priorities for next session:**
1. Read this bible before doing anything.
2. Play through the current crop loop once to feel what needs tuning.
3. Then start the gardener drone — it is the first thing that will prove this is not just a farming game.

**Warnings for next worker:**
- Do NOT add a second autoload without a strong reason. FarmingManager staying as a scene child is intentional.
- Do NOT implement natural language agent creation. It is documented in the concept doc but is explicitly post-MVP.
- The StaticBody2D floor is a Phase 1 stub. Replace it with TileMapLayer collision in Phase 2, not Phase 1.
- Growth time (30s) and power drain (1%/3s) are first-pass values. They need playtesting before being considered final.
```

- [ ] **Step 13.2: Commit bible**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
git add Starlight_Acre_bible.md
git commit -m "docs: write Starlight_Acre_bible.md — full 12-section project ledger"
```

---

### Task 14: README.md

**Files:**
- Create: `README.md`

- [ ] **Step 14.1: Write README.md**

Create `README.md` at the project root:

```markdown
# Starlight Acre

A small, polished, finishable orbital mythic farming station game.

You are the last steward of a failing orbital greenhouse. Restore it by cultivating mythic plants inspired by classical pantheons — Wisdom Fruit, Trickster Vine, Lightning Vine — while managing the station's survival and orchestrating simple constructs to carry out tasks you can't do alone.

---

## Status

**Phase 1 — Bootstrap complete.** Playable vertical slice: player movement, one crop lifecycle (plant → tend → harvest), power drain hazard, repair and replenish terminals, HUD.

---

## Stack

- **Engine:** Godot 4.x
- **Language:** GDScript
- **Perspective:** 2D side-view

---

## Setup

1. Install Godot 4.x from [godotengine.org](https://godotengine.org) if not already installed.
2. Clone or download this repository to your local machine.
3. Open the Godot editor.
4. Choose **File → Open Project** and navigate to this folder.
5. Select `project.godot` and click **Open**.

## Run

- Press **F5** in the Godot editor, or click the **Play** button.
- The game opens in `GreenhouseSector` — the first greenhouse sector.

## Controls

| Action | Key |
|--------|-----|
| Move left | A / Left Arrow |
| Move right | D / Right Arrow |
| Jump | Space / Up Arrow |
| Interact | E |

---

## Folder Overview

| Folder | Contents |
|--------|----------|
| `scenes/world/` | Room scenes (GreenhouseSector is the entry scene) |
| `actors/player/` | Player scene + movement script |
| `actors/crops/` | CropPlot scene + state machine |
| `actors/terminals/` | RepairTerminal and ReplenishTerminal scenes |
| `systems/farming/` | FarmingManager — resource state and power drain |
| `autoload/` | Events.gd — global signal bus |
| `data/crops/` | CropDefinition resources |
| `ui/hud/` | HUD scene + script |
| `docs/` | All design, architecture, and game design documents |

---

## MVP Status

- [x] Player moves (coyote time, jump buffer)
- [x] One crop lifecycle: plant → grow → tend → harvest
- [x] Power drain hazard
- [x] Repair and Replenish terminals
- [x] HUD: Water, Nutrient, Power, Wisdom Fruit
- [ ] Gardener drone agent (Phase 2)
- [ ] Second crop: Trickster Vine (Phase 2)
- [ ] Room transitions (Phase 2)
- [ ] Dexter the Stinkweasel vendor (Phase 3)
- [ ] Save / load (Phase 3)

---

## Roadmap Snapshot

| Phase | Goal |
|-------|------|
| 1 — Bootstrap | Runnable, full crop loop, all docs ✅ |
| 2 — Agent + Expansion | Gardener drone, second crop, second room |
| 3 — Station Systems | Save/load, Dexter vendor, progression |
| 4 — Polish | Real art, sound, movement upgrades |

---

See `Starlight_Acre_bible.md` for the full project ledger.
```

- [ ] **Step 14.2: Commit README**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
git add README.md
git commit -m "docs: write README with setup, run instructions, folder overview, roadmap"
```

---

### Task 15: ARCHITECTURE.md + GAME_DESIGN.md

**Files:**
- Create: `docs/ARCHITECTURE.md`
- Create: `docs/GAME_DESIGN.md`

- [ ] **Step 15.1: Write docs/ARCHITECTURE.md**

Create `docs/ARCHITECTURE.md`:

```markdown
# Architecture — Starlight Acre

## Engine and Language

**Godot 4.x, GDScript, 2D.**

Rationale: Godot's scene composition model maps directly to the station's room-based structure. GDScript is readable, fast to iterate, and idiomatic for Godot. The engine is free, open-source, and AI-development friendly (small files, explicit scene trees). See `deep-research-report.md` for the full research backing.

## Folder Structure

```
autoload/     Events.gd — signal bus only
scenes/       Room scenes. One scene = one room/sector.
actors/       Instanced scene entities: player, crops, terminals, agents, hazards
systems/      Stateless or stateful managers: FarmingManager, (future) AgentManager, TimeSystem
data/         Resource definitions: crops, items, events. No runtime logic.
ui/           HUD, menus, overlays. Driven by Events signals only.
assets/       Art, audio, fonts, placeholders.
docs/         All design and technical documentation.
```

## Scene Strategy

- **Entry scene:** `scenes/world/GreenhouseSector.tscn`
- **Room = scene:** Each sector is its own `.tscn` file. Room transitions load a new scene.
- **Actors are instanced:** `Player.tscn`, `CropPlot.tscn`, `RepairTerminal.tscn` are all instanced into room scenes. They are not embedded as unique child scripts.
- **No monolithic scenes:** Every gameplay entity that could be reused across rooms is its own scene file in `actors/`.

## Autoload Policy

**One autoload in Phase 1: `Events.gd`.**

Events.gd is a pure signal bus. It emits signals. It holds no state. It runs no logic. Adding game state to autoloads is explicitly forbidden in Phases 1–2.

When to add a second autoload: Only when a service is required to persist across room transitions AND must be accessible from scenes that cannot have direct references. The threshold is high. `FarmingManager` is deliberately NOT an autoload for this reason — it lives as a child of the room scene and its state resets on room change (Phase 1 behavior).

## Signal Architecture

All cross-system communication uses `Events.gd` signals:

| Signal | Emitter | Listener |
|--------|---------|----------|
| `resource_changed(name, value)` | FarmingManager | HUD |
| `crop_state_changed(plot_id, state)` | CropPlot | (future: AgentManager, Objectives) |
| `interaction_prompt_changed(text)` | player.gd | HUD |

New signals should be added to Events.gd. Do not create per-node signals for cross-scene communication.

## Interactable Pattern

Every interactable (CropPlot, terminals, future doors/agents) follows this contract:
- Has an `Area2D` child with `body_entered` / `body_exited` signals
- `body_entered` calls `player.register_interactable(self)` if body is in group "player"
- `body_exited` calls `player.unregister_interactable(self)` if body is in group "player"
- Implements `interact() -> void`
- Implements `get_prompt() -> String`

Player holds exactly one `_current_interactable` at all times. `E` fires `_current_interactable.interact()`. This eliminates multi-interactable ambiguity.

## Data Strategy

Crop definitions live in `data/crops/` as GDScript `Resource` classes. In Phase 1, `wisdom_fruit.gd` IS the `CropDefinition` class with defaults for Wisdom Fruit. In Phase 2, refactor to a base `CropDefinition` class + separate `.tres` resource instances per crop.

No JSON files are used in Phase 1. Resource classes are preferred because Godot's inspector can edit them and they integrate with the export system.

## Save / Load Strategy

**Phase 1:** No save/load. All state resets on quit. `FarmingManager` is session-only.

**Phase 2 plan:** Introduce a lightweight `SaveManager` autoload. Save a dictionary of resource values and crop states to `user://save.json`. Load on startup. Do not introduce complex serialization until it is necessary.

## Room Structure (Phase 1)

GreenhouseSector uses:
- `StaticBody2D` + `RectangleShape2D` for floor/wall collision (Phase 1 only)
- `TileMapLayer` nodes (FloorLayer, WallLayer, BackgroundLayer) — present but empty; will hold actual tiles in Phase 2
- `FarmingManager` as a child Node (not autoload)

## Technical Risks

| Risk | Mitigation |
|------|-----------|
| Agent system complexity | Keep Phase 2 agent to 1 type, 2 task types, no scheduling |
| Scope explosion | See docs/TASKS.md — enforce one phase = one isolated concern |
| TileMapLayer setup | Deferred to Phase 2; StaticBody2D covers Phase 1 collision |
| Signal bus growing large | Audit Events.gd at each phase; remove unused signals |
```

- [ ] **Step 15.2: Write docs/GAME_DESIGN.md**

Create `docs/GAME_DESIGN.md`:

```markdown
# Game Design — Starlight Acre

## Core Concept

A 2D side-view station management and mythic farming game. The player restores a failing orbital greenhouse by cultivating mythic plants, managing station resources, delegating tasks to simple constructs, and occasionally dealing with cosmic events and a peculiar vendor.

The key identity: **this is not a farming game that happens to be in space. The mythic plants have mechanical character. The station is a character. The orchestration is the game.**

## Player Fantasy

You are restoring a failing orbital greenhouse-station that grows mythic lifeforms. You are the last keeper. The station recognizes you. The plants respond to care. Gradually, the station comes back to life.

## Core Loop (Phase 1 MVP)

```
Check resources → Plant → Tend → Harvest → Manage power → Repeat
```

Each day structure (Phase 2+):
1. Morning: set agent priorities
2. Agents execute tasks
3. Player explores, tends, interacts
4. Crops grow, hazards occur
5. Harvest, process, upgrade
6. Periodic: Dexter arrives

## Station Role

The station is not just a setting. In Phase 2+, it acts as:
- Tutorial/hint voice (ambient text or simple UI callouts)
- Hazard alert source ("Power critical. Repair recommended.")
- Narrative flavor ("This sector smells of ozone and old starlight.")

In Phase 1, this is not implemented. The HUD and prompt system are the first step toward the station voice.

## Crop System

Each crop has:
- A mythic identity (pantheon, name, personality)
- A growth timer (affected by tending and power state)
- A harvest behavior (most crops: simple yield; Trickster Vine: harvest event)
- A resource output (used in the economy)

### Phase 1 Crop

| Crop | Pantheon | Behavior | Output |
|------|----------|----------|--------|
| Wisdom Fruit | Athena | Predictable growth, tended for faster yield | Wisdom Fruit (research currency in Phase 2) |

### Phase 2+ Crops

| Crop | Pantheon | Behavior | Output |
|------|----------|----------|--------|
| Trickster Vine | Loki | Harvest triggers fruit-flee event | Chaos resource |
| Lightning Vine | Zeus | Emits arc at maturity | Energy boost |
| Shadow Root | Hades | Grows underground, invisible progress | Stealth resource |
| Golden Blossom | Freya | Attracts nearby agents when ready | Efficiency buff |

## Resource System

### Phase 1 Resources

| Resource | Start | Cap | Source | Sink |
|----------|-------|-----|--------|------|
| Water | 5 | 10 | ReplenishTerminal | Planting |
| Nutrient | 5 | 10 | ReplenishTerminal | Planting |
| Power | 100% | 100% | RepairTerminal | Passive drain |
| Wisdom Fruit | 0 | — | Harvest | Phase 2: upgrade spending |

### Phase 2+ Resources

- Biomass (processed harvest output)
- Construction materials (build modules)
- Research data (unlock upgrades)
- Anomaly residue (from mythic events)

## Agent System

**Agents are simple heuristic workers. They are NOT AI models.**

Each agent has:
- Task priority list (e.g., [Water, Tend, Harvest])
- Assigned zone (which sector)
- Efficiency stat (how fast they complete tasks)

### Phase 2 Agent: Gardener Drone
- One task type: Tend/Harvest crops in assigned zone
- Runs on a timer; walks to nearest ready crop
- No pathfinding beyond a simple left/right seek
- Player assigns zone in a simple UI

### Future Agent Roles
- Engineer (repairs modules)
- Maintenance Drone (general upkeep)
- Harvester (dedicated harvest)

**Natural language agent creation is POST-MVP. Do not implement until Phase 4+.**

## Hazard System

### Phase 1 Hazard: Power Drain
Passive. Power drains at ~1%/3s. Crop growth pauses at 0%. Player must visit RepairTerminal.

### Phase 2+ Hazards
- **Solar flare:** Sudden power loss, brief window to repair before crop damage
- **Mythic anomaly:** Random crop growth modifier, positive or negative
- **System malfunction:** Agent temporarily non-functional
- **Cosmic debris:** Module damage requiring engineer repair

## Progression

**Early game:** Repair basic systems → stabilize first sector → grow first viable crop.
**Mid game:** Unlock modules → manage multiple sectors → survive or exploit anomalies.
**Late game:** Self-sustaining mythic orbital ecosystem.

**Win condition options:**
- Soft completion: station becomes self-sustaining (all systems stable)
- Collect all major mythic crops
- Complete full expansion tree
- Or: endless mode after restoration milestone

## Vendor System: Dexter the Stinkweasel

Dexter is a periodic vendor who arrives at the docking bay with:
- Rare seeds (new crop types)
- Unusual upgrades (module enhancers)
- Station components (construction materials)

Dexter's inventory reacts to: station size, crop variety, player progress. He has personality. He is not reliable. He is worth waiting for.

**Phase 1:** Not implemented. Documented stub. Implement in Phase 3.

## Sector Layout Concept

```
[Engineering Bay] — [Docking Bay / Dexter] — [Greenhouse Sector A] — [Mythic Dome]
                                                        |
                                               [Support Sector]
```

Phase 1 scope: Greenhouse Sector A only.

## MVP Slice Definition (Phase 1)

In scope:
- One room (GreenhouseSector)
- Player movement with coyote time and jump buffer
- One crop: Wisdom Fruit (plant → grow → tend → harvest)
- Two resources spent at plant time: Water, Nutrient
- One hazard: passive power drain
- Two terminals: RepairTerminal, ReplenishTerminal
- HUD: Water, Nutrient, Power, Wisdom Fruit

Out of scope for Phase 1:
- Agents
- Vendor
- Second room
- Save/load
- Second crop
- Sound / music
- Real art

## Post-MVP Ideas (Do Not Implement Until Planned)

- Gardener drone agent
- Trickster Vine + its flee mechanic
- Room transitions and door interactables
- GameState autoload for cross-room persistence
- Save/load via SaveManager
- Dexter trade UI
- Station voice callouts
- Solar flare hazard event
- TileMapLayer visual pass
- Movement upgrades (jet boots)
- Natural language agent configuration
```

- [ ] **Step 15.3: Commit**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
git add docs/ARCHITECTURE.md docs/GAME_DESIGN.md
git commit -m "docs: write ARCHITECTURE.md and GAME_DESIGN.md"
```

---

### Task 16: PROJECT_OVERVIEW.md + TASKS.md + CHANGELOG.md

**Files:**
- Create: `docs/PROJECT_OVERVIEW.md`
- Create: `docs/TASKS.md`
- Create: `docs/CHANGELOG.md`

- [ ] **Step 16.1: Write docs/PROJECT_OVERVIEW.md**

Create `docs/PROJECT_OVERVIEW.md`:

```markdown
# Project Overview — Starlight Acre

## Vision

A small, polished, finishable orbital mythic farming station game that feels alive, unusual, and complete — not a demo, not a jam prototype, not a clone.

## Intended Feel

Atmospheric and slightly uncanny. Luminous greenhouse interiors. Orbital silhouettes through viewport windows. The station feels like it knows you. The plants feel like more than crops. The rhythm of the game is calm but purposeful — there is always something to tend, something to improve, something to discover.

**Not:** grimdark, parody, aggressively cutesy, or a generic Stardew Valley clone.

## Player Experience Goals

1. The player understands the core loop within the first two minutes.
2. The player feels like the station is alive and responding to their choices.
3. The mythic plants feel distinct — not just different crop timers.
4. Delegating tasks to agents should feel satisfying, not like watching a spreadsheet.
5. The game should be completable. There is an end state. It means something.

## MVP Scope

One room. One crop lifecycle. One hazard. One repair loop. Player moves, plants, tends, harvests. HUD is legible. Prompt is clear. Power drains. Station can be repaired.

That is enough to prove this is the right game.

## Non-Goals

- Not a colony sim. The simulation depth stops at "simple heuristic agents."
- Not a survival game. Light resource pressure, not overwhelming stakes.
- Not a procedural generation showcase. Content is authored.
- Not a multiplayer game. Ever.
- Not a live-service product.
- Natural language agent creation is a speculative post-MVP idea.

## Implementation Priorities

1. **Playability first.** If it is not fun to move around in, nothing else matters.
2. **Loop legibility.** The player should never be confused about what to do next.
3. **Identity.** Every system should reinforce: this is an orbital mythic farming station.
4. **Finishability.** Resist scope expansion. One complete game is worth ten abandoned prototypes.
```

- [ ] **Step 16.2: Write docs/TASKS.md**

Create `docs/TASKS.md`:

```markdown
# Tasks — Starlight Acre

## Immediate (Phase 2 Kickoff)

- [ ] Playtest Phase 1 crop loop — tune growth_time and power drain rate
- [ ] Decide on Phase 2 scope: gardener drone OR second crop first (recommend drone)
- [ ] Set up TileMapLayer visual pass (replace StaticBody2D stubs with real tiles)
- [ ] Implement Gardener Drone (Phase 2, Task 1)

## Next Milestone: Phase 2 — Agent + Expansion

- [ ] Gardener Drone agent (1 type, 2 task types: Tend + Harvest)
- [ ] Zone assignment UI (simple: click to assign drone to a sector)
- [ ] Second crop: Trickster Vine + flee behavior
- [ ] Room transition: one door interactable → one adjacent sector
- [ ] GameState or SaveManager decision (needed for cross-room persistence)

## Short-Term Roadmap

| Phase | Focus | Key Deliverable |
|-------|-------|-----------------|
| 2 | Agent + Expansion | Drone, second crop, second room |
| 3 | Station Systems | Save/load, Dexter vendor, upgrade spending |
| 4 | Polish | Real art, sound, movement upgrades, station voice |

## Known Blockers

- No real art assets — all placeholder. Phase 4.
- No sound — Phase 4.
- TileMapLayer tiles not configured — Phase 2 visual pass.
- Wisdom Fruit has no spend mechanic — Phase 2 upgrade system.

## Prioritized Checklist

1. Playtest crop loop timing
2. TileMapLayer visual pass
3. Gardener Drone
4. Trickster Vine
5. Room transition + door
6. Save/load scaffold
7. Dexter stub → trade UI
```

- [ ] **Step 16.3: Write docs/CHANGELOG.md**

Create `docs/CHANGELOG.md`:

```markdown
# Changelog — Starlight Acre

## [Phase 1] — 2026-03-22 — Bootstrap

### Added
- `project.godot` — Godot 4 project config with input map (move_left, move_right, jump, interact) and Events autoload
- `autoload/Events.gd` — global signal bus (crop_state_changed, resource_changed, interaction_prompt_changed)
- `data/crops/wisdom_fruit.gd` — CropDefinition resource class with Wisdom Fruit defaults
- `actors/player/player.gd` + `Player.tscn` — CharacterBody2D movement, coyote time (0.1s), jump buffer (0.1s), interactable registration
- `scenes/world/GreenhouseSector.tscn` — entry scene, dark greenhouse room, StaticBody2D floor/walls, TileMapLayer stubs, 3 CropPlots, 2 terminals, HUD
- `systems/farming/farming_manager.gd` — resource state (water, nutrient, power, wisdom_fruit), passive power drain
- `actors/crops/crop_plot.gd` + `CropPlot.tscn` — crop state machine (EMPTY→PLANTED→GROWING→READY), Area2D interaction
- `actors/terminals/repair_terminal.gd` + `RepairTerminal.tscn` — restores power
- `actors/terminals/replenish_terminal.gd` + `ReplenishTerminal.tscn` — restores water + nutrient
- `ui/hud/hud.gd` + `HUD.tscn` — resource bar + interaction prompt
- `README.md`
- `Starlight_Acre_bible.md`
- `docs/ARCHITECTURE.md`, `GAME_DESIGN.md`, `PROJECT_OVERVIEW.md`, `TASKS.md`, `CHANGELOG.md`

### Moved
- `orbital_mythic_farming_game_concept.md` → `docs/`
- `deep-research-report.md` → `docs/`

### Decisions
- Stack: Godot 4.x + GDScript (validated by research doc)
- One autoload: Events.gd signal bus only
- FarmingManager: child node of GreenhouseSector, not autoload (session state, Phase 1 only)
- Floor collision: StaticBody2D (TileMapLayer deferred to Phase 2)
- First crop: Wisdom Fruit (Trickster Vine deferred — flee mechanic is a second system)
- Single active interactable: player.gd owns current_interactable reference
```

- [ ] **Step 16.4: Final commit**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
git add docs/PROJECT_OVERVIEW.md docs/TASKS.md docs/CHANGELOG.md
git commit -m "docs: write PROJECT_OVERVIEW, TASKS, CHANGELOG — Phase 1 bootstrap complete"
```

---

### Task 17: Final Done-Criteria Check

- [ ] **Step 17.1: Run through the full done-criteria checklist**

Open the project in Godot. Work through each item:

**Runnable:**
- [ ] `project.godot` opens in Godot 4 without errors
- [ ] Entry scene shows GreenhouseSector
- [ ] Player moves left/right
- [ ] Player jumps; coyote time works (walk off edge, jump just after)
- [ ] Jump buffer works (press Space just before landing, jump fires)

**Mechanic:**
- [ ] Player near empty plot sees prompt "E — Plant Wisdom Fruit (1 Water, 1 Nutrient)"
- [ ] Press E → plot turns dark brown (PLANTED), HUD drops Water and Nutrient by 1
- [ ] ~0.5s later → plot turns green (GROWING)
- [ ] Press E near GROWING plot → plot stays green (tended, timer shortened)
- [ ] Wait → plot turns gold (READY)
- [ ] Press E near READY plot → HUD shows Wisdom Fruit: 1; plot returns to grey (EMPTY)
- [ ] Power in HUD drains over time
- [ ] When Power = 0%, plant a crop → it does not grow
- [ ] Press E at RepairTerminal (orange) → Power jumps to 100%; crop resumes growing
- [ ] Press E at ReplenishTerminal (blue) → Water and Nutrient return to 10/10
- [ ] Walk away from interactable → prompt disappears

**Docs:**
- [ ] `Starlight_Acre_bible.md` has all 12 sections with real content
- [ ] `README.md` setup instructions accurate
- [ ] All 5 docs in `docs/` exist with real content
- [ ] Concept docs at `docs/orbital_mythic_farming_game_concept.md` and `docs/deep-research-report.md`
- [ ] No doc claims anything is implemented that isn't

- [ ] **Step 17.2: Final commit if any last fixes**

```bash
cd "/Users/andrew/Projects/Starlight Acre"
git add -A
git commit -m "chore: Phase 1 bootstrap complete — all done criteria verified"
```

---

## Execution Notes

- **Godot version:** If the project fails to open, check that the installed Godot version is 4.x. The `config/features` line in `project.godot` targets 4.3.
- **UID warnings:** Godot may warn about missing UIDs in `.tscn` files on first open. This is harmless — Godot will generate them. Accept any "fix" prompts the editor offers.
- **load_steps count:** The `load_steps` value in `.tscn` headers must match the number of `[ext_resource]` + `[sub_resource]` entries + 1. If Godot reports a parse error on a `.tscn` file, check this count first.
- **Area2D collision layers:** By default, Area2D monitors physics layer 1. CharacterBody2D occupies layer 1 by default. No manual layer configuration should be needed. If body_entered does not fire, check that both the Area2D's "Monitorable" and "Monitoring" are enabled (default: on).
- **FarmingManager group:** `farming_manager.gd` calls `add_to_group("farming_manager")` in `_ready()`. If interactables return null from `get_first_node_in_group()`, confirm the FarmingManager node has the script attached and its `_ready()` has run (it must be in the scene tree before interactables call it).
