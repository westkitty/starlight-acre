class_name CropPlot
extends Node2D

enum State { EMPTY, PLANTED, GROWING, READY }

@export var plot_id: String = "plot_0"
@export var crop_definition: CropDefinition = preload("res://data/crops/wisdom_fruit.tres")

@onready var _visual: Sprite2D = $Visual
@onready var _ready_glow: GPUParticles2D = $ReadyGlow
var _state: State = State.EMPTY
var _growth_timer: float = 0.0
var _power_available := true
var _player_in_range: Node = null

func _ready() -> void:
	Events.resource_changed.connect(_on_resource_changed)
	var saved := GameState.get_plot_state(plot_id)
	if not saved.is_empty():
		_state = State.get(str(saved.get("state", "EMPTY")))
		_growth_timer = float(saved.get("growth_remaining", 0.0))
	_apply_visual()

func _process(delta: float) -> void:
	if _state != State.GROWING or not _power_available:
		return
	_growth_timer -= delta
	if _growth_timer <= 0.0:
		_set_state(State.READY)

func interact() -> void:
	match _state:
		State.EMPTY: _try_plant()
		State.GROWING: _tend()
		State.READY: _harvest()

func get_prompt() -> String:
	match _state:
		State.EMPTY:
			return "E - Plant %s (%d Water, %d Nutrient)" % [crop_definition.crop_name, crop_definition.water_cost, crop_definition.nutrient_cost]
		State.GROWING:
			return "E - Tend %s" % crop_definition.crop_name
		State.READY:
			return "E - Harvest %s" % crop_definition.crop_name
	return ""

func get_state() -> State:
	return _state

func can_drone_tend() -> bool:
	return _state == State.GROWING

func can_drone_harvest() -> bool:
	return _state == State.READY

func drone_interact() -> void:
	if _state == State.GROWING:
		_tend()
	elif _state == State.READY:
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
	_growth_timer = maxf(0.0, _growth_timer - (_growth_timer * crop_definition.tend_bonus))
	_persist()

func _harvest() -> void:
	var fm := _get_farming_manager()
	if fm != null:
		fm.add_wisdom_fruit(crop_definition.harvest_yield)
	_set_state(State.EMPTY)

func _set_state(new_state: State) -> void:
	_state = new_state
	_apply_visual()
	_persist()
	Events.crop_state_changed.emit(plot_id, State.keys()[new_state])
	if _player_in_range != null:
		_player_in_range.register_interactable(self)

func _persist() -> void:
	GameState.set_plot_state(plot_id, State.keys()[_state], _growth_timer, crop_definition.crop_id)

func _apply_visual() -> void:
	match _state:
		State.EMPTY: _visual.frame = 0
		State.PLANTED: _visual.frame = 1
		State.GROWING: _visual.frame = 2
		State.READY: _visual.frame = 3
	_ready_glow.emitting = _state == State.READY

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
