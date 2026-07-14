# GameState.gd
# Cross-scene state for room transitions and save/load.
# Keep this small: long-lived gameplay systems still live in scenes unless they must persist.
extends Node

const SAVE_VERSION := 1
const SAVE_PATH := "user://save.json"

var target_spawn_name: String = "PlayerSpawn"
var _pending_load: Dictionary = {}


func request_transition(scene_path: String, spawn_name: String = "PlayerSpawn") -> void:
	target_spawn_name = spawn_name
	Events.interaction_prompt_changed.emit("")
	get_tree().change_scene_to_file(scene_path)


func has_pending_load() -> bool:
	return not _pending_load.is_empty()


func get_pending_resources() -> Dictionary:
	return _pending_load.get("resources", {})


func get_pending_crop(plot_id: String) -> Dictionary:
	return _pending_load.get("crops", {}).get(plot_id, {})


func get_pending_player_position(default_position: Vector2) -> Vector2:
	var position_data = _pending_load.get("player_position", null)
	if typeof(position_data) == TYPE_ARRAY and position_data.size() == 2:
		return Vector2(float(position_data[0]), float(position_data[1]))
	return default_position


func save_game() -> bool:
	var current_scene := get_tree().current_scene
	if current_scene == null:
		return false

	var data := {
		"version": SAVE_VERSION,
		"scene": current_scene.scene_file_path,
		"spawn_name": target_spawn_name,
		"resources": _collect_resources(),
		"crops": _collect_crops(),
		"player_position": _collect_player_position(),
	}

	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file == null:
		return false
	file.store_string(JSON.stringify(data, "\t"))
	return true


func load_game() -> bool:
	if not FileAccess.file_exists(SAVE_PATH):
		return false

	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if file == null:
		return false

	var parsed = JSON.parse_string(file.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		return false
	if int(parsed.get("version", 0)) != SAVE_VERSION:
		return false

	_pending_load = parsed
	target_spawn_name = parsed.get("spawn_name", "PlayerSpawn")
	var scene_path: String = parsed.get("scene", "")
	if scene_path.is_empty():
		return false
	get_tree().change_scene_to_file(scene_path)
	return true


func clear_pending_load() -> void:
	_pending_load.clear()


func _collect_resources() -> Dictionary:
	var fm := get_tree().get_first_node_in_group("farming_manager")
	if fm != null and fm.has_method("get_save_data"):
		return fm.get_save_data()
	return {}


func _collect_crops() -> Dictionary:
	var crops := {}
	for plot in get_tree().get_nodes_in_group("crop_plots"):
		if plot.has_method("get_save_data"):
			crops[plot.plot_id] = plot.get_save_data()
	return crops


func _collect_player_position() -> Array:
	var player := get_tree().get_first_node_in_group("player")
	if player == null:
		return []
	return [player.global_position.x, player.global_position.y]
