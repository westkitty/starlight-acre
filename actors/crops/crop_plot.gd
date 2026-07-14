# crop_plot.gd
# Manages one crop plot lifecycle: EMPTY -> PLANTED -> GROWING -> READY -> EMPTY.
class_name CropPlot
extends Node2D

enum State { EMPTY, PLANTED, GROWING, READY }

## Unique identifier emitted with crop_state_changed signals and used by save data.
@export var plot_id: String = "plot_0"
@export_file("*.gd") var crop_definition_path: String = "res://data/crops/wisdom_fruit.gd"
@export var visual_modulate: Color = Color.WHITE

@onready var _visual: Sprite2D = $Visual
@onready var _ready_glow: Sprite2D = $ReadyGlow

var _state: State = State.EMPTY
var _growth_timer: float = 0.0
var _power_available: bool = true
var _crop: CropDefinition
var _player_in_range: Node = null


func _ready() -> void:
	_crop = _load_crop_definition()
	_visual.modulate = visual_modulate
	_ready_glow.visible = false
	Events.resource_changed.connect(_on_resource_changed)
	_apply_pending_save_data()
	_apply_visual()


func _process(delta: float) -> void:
	if _state != State.GROWING or not _power_available:
		return
	_growth_timer -= _get_growth_delta(delta)
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
		State.EMPTY:
			return "E - Plant %s (%d Water, %d Nutrient)" % [_crop.crop_name, _crop.water_cost, _crop.nutrient_cost]
		State.GROWING:
			return "E - Tend %s" % _crop.crop_name
		State.READY:
			return "E - Harvest %s" % _crop.crop_name
	return ""


func get_state() -> State:
	return _state


func get_save_data() -> Dictionary:
	return {
		"state": State.keys()[_state],
		"growth_timer": _growth_timer,
		"crop_definition_path": crop_definition_path,
	}


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
	_growth_timer -= _growth_timer * _crop.tend_bonus
	if _crop.behavior == "erratic_growth":
		_growth_timer += randf_range(-1.25, 2.0)
	_growth_timer = maxf(0.0, _growth_timer)


func _harvest() -> void:
	var fm := _get_farming_manager()
	if fm != null:
		fm.add_harvest(_crop.harvest_resource, _crop.harvest_yield)
	_set_state(State.EMPTY)


# --- State management ---

func _set_state(new_state: State) -> void:
	_state = new_state
	_apply_visual()
	Events.crop_state_changed.emit(plot_id, State.keys()[new_state])
	if _player_in_range != null:
		_player_in_range.register_interactable(self)


func _apply_visual() -> void:
	match _state:
		State.EMPTY:   _visual.frame = 0
		State.PLANTED: _visual.frame = 1
		State.GROWING: _visual.frame = 2
		State.READY:   _visual.frame = 3
	_ready_glow.visible = _state == State.READY


func _apply_pending_save_data() -> void:
	if not GameState.has_pending_load():
		return
	var data := GameState.get_pending_crop(plot_id)
	if data.is_empty():
		return
	var saved_path: String = data.get("crop_definition_path", crop_definition_path)
	if not saved_path.is_empty():
		crop_definition_path = saved_path
		_crop = _load_crop_definition()
	var state_name: String = data.get("state", "EMPTY")
	var state_index := State.keys().find(state_name)
	if state_index >= 0:
		_state = state_index as State
	_growth_timer = float(data.get("growth_timer", _growth_timer))


func _get_growth_delta(delta: float) -> float:
	if _crop.behavior == "erratic_growth":
		return delta * randf_range(0.75, 1.4)
	return delta


func _load_crop_definition() -> CropDefinition:
	var script := load(crop_definition_path)
	if script == null:
		return CropDefinition.new()
	var definition = script.new()
	if definition is CropDefinition:
		return definition
	return CropDefinition.new()


# --- Signals ---

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


# --- Helpers ---

func _get_farming_manager() -> Node:
	return get_tree().get_first_node_in_group("farming_manager")
