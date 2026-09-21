extends Node

const SAVE_PATH := "user://save.json"

var water: int = 5
var nutrient: int = 5
var wisdom_fruit: int = 0
var chaos: int = 0
var power: float = 100.0
var emergency_resupplies: int = 2
var upgrades: Dictionary = {}
var plot_states: Dictionary = {}
var current_sector: String = "greenhouse"
var next_player_position: Vector2 = Vector2.ZERO

# Transient hazard state persists across sector transitions within a run but is
# deliberately not serialized. Reloading the game always starts from a calm window.
var solar_flare_phase: String = "calm"
var solar_flare_time_remaining: float = 30.0

func _ready() -> void:
	load_game()

func power_drain_multiplier() -> float:
	return 0.6 if upgrades.get("efficient_grid", false) else 1.0

func hazard_power_drain_multiplier() -> float:
	return 5.0 if solar_flare_phase == "active" else 1.0

func reset_transient_hazards() -> void:
	solar_flare_phase = "calm"
	solar_flare_time_remaining = 30.0

func water_cap() -> int:
	return 15 if upgrades.get("closed_loop_hydroponics", false) else 10

func nutrient_cap() -> int:
	return 15 if upgrades.get("closed_loop_hydroponics", false) else 10

func has_upgrade(id: String) -> bool:
	return bool(upgrades.get(id, false))

func unlock_upgrade(id: String) -> void:
	upgrades[id] = true
	Events.upgrade_unlocked.emit(id)
	save_game()

func set_plot_state(plot_id: String, state_name: String, growth_remaining: float, crop_id: String, extra: Dictionary = {}) -> void:
	var state_data := {
		"state": state_name,
		"growth_remaining": growth_remaining,
		"crop_id": crop_id
	}
	for key in extra:
		state_data[key] = extra[key]
	plot_states[plot_id] = state_data
	save_game()

func get_plot_state(plot_id: String) -> Dictionary:
	return plot_states.get(plot_id, {})

func save_game() -> void:
	var payload := {
		"version": 2,
		"water": water,
		"nutrient": nutrient,
		"wisdom_fruit": wisdom_fruit,
		"chaos": chaos,
		"power": power,
		"emergency_resupplies": emergency_resupplies,
		"upgrades": upgrades,
		"plot_states": plot_states,
		"current_sector": current_sector
	}
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file != null:
		file.store_string(JSON.stringify(payload))

func load_game() -> void:
	if not FileAccess.file_exists(SAVE_PATH):
		return
	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if file == null:
		return
	var parsed = JSON.parse_string(file.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		return
	water = int(parsed.get("water", water))
	nutrient = int(parsed.get("nutrient", nutrient))
	wisdom_fruit = int(parsed.get("wisdom_fruit", wisdom_fruit))
	chaos = int(parsed.get("chaos", chaos))
	power = float(parsed.get("power", power))
	emergency_resupplies = int(parsed.get("emergency_resupplies", emergency_resupplies))
	upgrades = parsed.get("upgrades", {})
	plot_states = parsed.get("plot_states", {})
	current_sector = str(parsed.get("current_sector", current_sector))

func set_transition(target_sector: String, spawn_position: Vector2) -> void:
	current_sector = target_sector
	next_player_position = spawn_position
	save_game()

func consume_spawn(default_position: Vector2) -> Vector2:
	if next_player_position == Vector2.ZERO:
		return default_position
	var result := next_player_position
	next_player_position = Vector2.ZERO
	return result
