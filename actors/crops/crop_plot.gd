class_name CropPlot
extends Node2D

enum State { EMPTY, PLANTED, GROWING, READY }

const TRICKSTER_FRUIT_SCENE := preload("res://actors/crops/TricksterFruit.tscn")
const ECOLOGY_STEAL_RADIUS := 224.0

@export var plot_id: String = "plot_0"
@export var crop_definition: CropDefinition = preload("res://data/crops/wisdom_fruit.tres")
@export var crop_texture: Texture2D = preload("res://assets/sprites/crops/wisdom_fruit_states.png")

@onready var _visual: Sprite2D = $Visual
@onready var _ready_glow: GPUParticles2D = $ReadyGlow

var _state: State = State.EMPTY
var _growth_timer: float = 0.0
var _power_available := true
var _player_in_range: Node = null
var _ready_dodges_remaining := 0
var _runner_active := false
var _dodge_offset_x := 0.0
var _ecology_steal_available := false
var _runner: Node = null

func _ready() -> void:
	_visual.texture = crop_texture
	Events.resource_changed.connect(_on_resource_changed)
	var saved := GameState.get_plot_state(plot_id)
	if not saved.is_empty() and str(saved.get("crop_id", "")) == crop_definition.crop_id:
		var restored_state = State.get(str(saved.get("state", "EMPTY")))
		if restored_state != null:
			_state = restored_state
		_growth_timer = float(saved.get("growth_remaining", 0.0))
		if _state == State.GROWING and crop_definition.crop_id == "trickster_vine":
			_ecology_steal_available = bool(saved.get("ecology_steal_available", true))
		if _state == State.READY:
			_ready_dodges_remaining = int(saved.get("ready_dodges_remaining", crop_definition.ready_dodge_count))
			_runner_active = bool(saved.get("runner_active", false))
			_dodge_offset_x = float(saved.get("dodge_offset_x", 0.0))
	_apply_visual()
	if _state == State.READY and _runner_active:
		_spawn_runner(false)

func _process(delta: float) -> void:
	if _state != State.GROWING or not _power_available:
		return
	_growth_timer -= delta
	if _growth_timer <= 0.0:
		_set_state(State.READY)

func interact() -> void:
	match _state:
		State.EMPTY:
			_try_plant()
		State.GROWING:
			_tend()
		State.READY:
			if not _runner_active:
				_harvest()

func get_prompt() -> String:
	match _state:
		State.EMPTY:
			return "E - Plant %s (%d Water, %d Nutrient)" % [crop_definition.crop_name, crop_definition.water_cost, crop_definition.nutrient_cost]
		State.GROWING:
			return "E - Tend %s" % crop_definition.crop_name
		State.READY:
			if _runner_active:
				return ""
			return "E - Harvest %s" % _harvest_name()
	return ""

func get_state() -> State:
	return _state

func can_drone_tend() -> bool:
	return _state == State.GROWING

func can_drone_harvest() -> bool:
	return _state == State.READY and crop_definition.drone_can_harvest and not _runner_active

func drone_interact() -> void:
	if _state == State.GROWING:
		_tend()
	elif can_drone_harvest():
		_harvest()

func _try_plant() -> void:
	var fm := _get_farming_manager()
	if fm == null or not fm.can_plant(crop_definition.water_cost, crop_definition.nutrient_cost):
		return
	fm.spend_water(crop_definition.water_cost)
	fm.spend_nutrient(crop_definition.nutrient_cost)
	_growth_timer = crop_definition.growth_time
	_set_state(State.PLANTED)
	await get_tree().create_timer(0.5).timeout
	if _state == State.PLANTED:
		_set_state(State.GROWING)

func _tend() -> void:
	var reduction := _growth_timer * crop_definition.tend_bonus
	if crop_definition.crop_id == "wisdom_fruit" and _redirect_tend_to_trickster(reduction):
		if GameState.has_upgrade("paradox_trellis"):
			_growth_timer = maxf(0.0, _growth_timer - reduction)
		_persist()
		return
	_growth_timer = maxf(0.0, _growth_timer - reduction)
	_persist()

func _redirect_tend_to_trickster(reduction: float) -> bool:
	var thief: CropPlot = null
	var best_distance := INF
	for node in get_tree().get_nodes_in_group("crop_plots"):
		var plot := node as CropPlot
		if plot == null or plot == self or not plot._can_steal_wisdom_tend():
			continue
		var distance := global_position.distance_to(plot.global_position)
		if distance <= ECOLOGY_STEAL_RADIUS and distance < best_distance:
			thief = plot
			best_distance = distance
	if thief == null:
		return false
	return thief._steal_wisdom_tend(reduction)

func _can_steal_wisdom_tend() -> bool:
	return crop_definition.crop_id == "trickster_vine" and _state == State.GROWING and _ecology_steal_available

func _steal_wisdom_tend(reduction: float) -> bool:
	if not _can_steal_wisdom_tend():
		return false
	_ecology_steal_available = false
	_growth_timer = maxf(0.0, _growth_timer - reduction)
	if _growth_timer <= 0.0:
		_set_state(State.READY)
	else:
		_persist()
	if GameState.has_upgrade("paradox_trellis"):
		Events.station_message.emit("Paradox Trellis caught the theft: both crops keep the tending pulse.")
	else:
		Events.station_message.emit("Trickster Vine stole the Wisdom tending pulse.")
	return true

func _harvest() -> void:
	if _ready_dodges_remaining > 0:
		_dodge_ready_crop()
		return
	_complete_harvest()

func _complete_harvest() -> void:
	var fm := _get_farming_manager()
	if fm == null:
		return
	if not fm.add_crop_yield(crop_definition.harvest_resource_id, crop_definition.harvest_yield):
		return
	if crop_definition.harvest_resource_id == "chaos":
		Events.station_message.emit("Caught %s. Chaos: %d." % [_harvest_name(), fm.chaos])
	_set_state(State.EMPTY)

func _dodge_ready_crop() -> void:
	_ready_dodges_remaining -= 1
	_runner_active = true
	var direction := 1.0
	if is_instance_valid(_player_in_range):
		direction = -1.0 if _player_in_range.global_position.x >= global_position.x else 1.0
	elif abs(plot_id.hash()) % 2 == 0:
		direction = -1.0
	_dodge_offset_x = direction * crop_definition.ready_dodge_distance
	_apply_visual()
	_spawn_runner(true)
	_persist()
	Events.station_message.emit("%s jumps away. Catch it!" % _harvest_name())
	if is_instance_valid(_player_in_range):
		_player_in_range.unregister_interactable(self)

func _spawn_runner(animate_jump: bool) -> void:
	if is_instance_valid(_runner):
		_runner.queue_free()
	_runner = TRICKSTER_FRUIT_SCENE.instantiate()
	add_child(_runner)
	_runner.caught.connect(_on_runner_caught)
	_runner.configure(crop_texture, _harvest_name(), _dodge_offset_x, animate_jump)

func _on_runner_caught() -> void:
	_runner_active = false
	_dodge_offset_x = 0.0
	_runner = null
	_complete_harvest()

func _set_state(new_state: State) -> void:
	var previous_state := _state
	_state = new_state
	if new_state == State.GROWING and previous_state != State.GROWING and crop_definition.crop_id == "trickster_vine":
		_ecology_steal_available = true
	elif new_state != State.GROWING:
		_ecology_steal_available = false
	if new_state == State.READY and previous_state != State.READY:
		_ready_dodges_remaining = crop_definition.ready_dodge_count
		_runner_active = false
		_dodge_offset_x = 0.0
	elif new_state != State.READY:
		_ready_dodges_remaining = 0
		_runner_active = false
		_dodge_offset_x = 0.0
		if is_instance_valid(_runner):
			_runner.queue_free()
			_runner = null
	_apply_visual()
	_persist()
	Events.crop_state_changed.emit(plot_id, State.keys()[new_state])
	if _player_in_range != null:
		_player_in_range.register_interactable(self)

func _persist() -> void:
	GameState.set_plot_state(
		plot_id,
		State.keys()[_state],
		_growth_timer,
		crop_definition.crop_id,
		{
			"ready_dodges_remaining": _ready_dodges_remaining,
			"runner_active": _runner_active,
			"dodge_offset_x": _dodge_offset_x,
			"ecology_steal_available": _ecology_steal_available
		}
	)

func _apply_visual() -> void:
	if _state == State.READY and _runner_active:
		_visual.frame = 2
		_ready_glow.emitting = false
		return
	match _state:
		State.EMPTY:
			_visual.frame = 0
		State.PLANTED:
			_visual.frame = 1
		State.GROWING:
			_visual.frame = 2
		State.READY:
			_visual.frame = 3
	_ready_glow.emitting = _state == State.READY

func _harvest_name() -> String:
	if crop_definition.harvest_name.is_empty():
		return crop_definition.crop_name
	return crop_definition.harvest_name

func _on_resource_changed(resource_name: String, value: float) -> void:
	if resource_name == "power":
		_power_available = value > 0.0

func _on_area_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		_player_in_range = body
		body.register_interactable(self)

func _on_area_body_exited(body: Node2D) -> void:
	if body.is_in_group("player"):
		_player_in_range = null
		body.unregister_interactable(self)

func _get_farming_manager() -> Node:
	return get_tree().get_first_node_in_group("farming_manager")
