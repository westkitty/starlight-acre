# GameState.gd
# Cross-scene state for room transitions and save/load.
# Keep this small: long-lived gameplay systems still live in scenes unless they must persist.
extends Node

const SAVE_VERSION := 1
const SAVE_PATH := "user://save.json"

var target_spawn_name: String = "PlayerSpawn"
var resources_state: Dictionary = {}
var crop_state_by_scene: Dictionary = {}
var _pending_load: Dictionary = {}


func request_transition(scene_path: String, spawn_name: String = "PlayerSpawn") -> void:
	_capture_current_scene_state()
	target_spawn_name = spawn_name
	Events.interaction_prompt_changed.emit("")
	get_tree().change_scene_to_file(scene_path)


func has_pending_load() -> bool:
	return not _pending_load.is_empty()


func get_pending_resources() -> Dictionary:
	if has_pending_load():
		return _pending_load.get("resources", {})
	return resources_state


func get_pending_crop(plot_id: String) -> Dictionary:
	var scene_path := _get_current_scene_path()
	if has_pending_load():
		var scene_data: Dictionary = _pending_load.get("scenes", {}).get(scene_path, {})
		var scene_crops: Dictionary = scene_data.get("crops", {})
		if scene_crops.has(plot_id):
			return scene_crops[plot_id]
		return _pending_load.get("crops", {}).get(plot_id, {})

	var current_scene_data: Dictionary = crop_state_by_scene.get(scene_path, {})
	var current_scene_crops: Dictionary = current_scene_data.get("crops", {})
	return current_scene_crops.get(plot_id, {})


func get_pending_player_position(default_position: Vector2) -> Vector2:
	var position_data = _pending_load.get("player_position", null)
	if typeof(position_data) == TYPE_ARRAY and position_data.size() == 2:
		return Vector2(float(position_data[0]), float(position_data[1]))
	return default_position


func save_game() -> bool:
	_capture_current_scene_state()
	var current_scene := get_tree().current_scene
	if current_scene == null:
		Events.status_message_changed.emit("Save failed")
		return false

	var data := {
		"version": SAVE_VERSION,
		"scene": current_scene.scene_file_path,
		"spawn_name": target_spawn_name,
		"resources": resources_state,
		"scenes": crop_state_by_scene,
		"crops": _collect_crops(),
		"player_position": _collect_player_position(),
	}

	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file == null:
		Events.status_message_changed.emit("Save failed")
		return false
	file.store_string(JSON.stringify(data, "\t"))
	Events.status_message_changed.emit("Station state saved")
	return true


func load_game() -> bool:
	if not FileAccess.file_exists(SAVE_PATH):
		Events.status_message_changed.emit("No save found")
		return false

	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if file == null:
		Events.status_message_changed.emit("Load failed")
		return false

	var parsed = JSON.parse_string(file.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		Events.status_message_changed.emit("Save data is invalid")
		return false
	if int(parsed.get("version", 0)) != SAVE_VERSION:
		Events.status_message_changed.emit("Save version mismatch")
		return false

	_pending_load = parsed
	resources_state = parsed.get("resources", {})
	crop_state_by_scene = parsed.get("scenes", {})
	target_spawn_name = parsed.get("spawn_name", "PlayerSpawn")
	var scene_path: String = parsed.get("scene", "")
	if scene_path.is_empty():
		Events.status_message_changed.emit("Save scene missing")
		return false
	Events.interaction_prompt_changed.emit("")
	get_tree().change_scene_to_file(scene_path)
	return true


func clear_pending_load() -> void:
	_pending_load.clear()


func _capture_current_scene_state() -> void:
	var scene_path := _get_current_scene_path()
	if scene_path.is_empty():
		return
	resources_state = _collect_resources()
	crop_state_by_scene[scene_path] = {"crops": _collect_crops()}


func _collect_resources() -> Dictionary:
	var fm := get_tree().get_first_node_in_group("farming_manager")
	if fm != null and fm.has_method("get_save_data"):
		return fm.get_save_data()
	return resources_state


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


func _get_current_scene_path() -> String:
	var current_scene := get_tree().current_scene
	if current_scene == null:
		return ""
	return current_scene.scene_file_path
