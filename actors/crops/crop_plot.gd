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
