# godot_smoke_test.gd
# Run with: godot4 --headless --path . --script tools/validation/godot_smoke_test.gd
extends SceneTree

var _failures: Array[String] = []


func _initialize() -> void:
	_check_resource_exists("res://scenes/world/GreenhouseSector.tscn")
	_check_resource_exists("res://scenes/world/ArchiveLibrary.tscn")
	_check_resource_exists("res://autoload/GameState.gd")
	_check_resource_exists("res://autoload/Events.gd")
	_check_resource_exists("res://ui/hud/HUD.tscn")
	_check_resource_exists("res://actors/transitions/DoorTransition.tscn")
	_check_resource_exists("res://actors/vendors/DexterTerminal.tscn")
	_check_resource_exists("res://data/crops/trickster_vine.gd")

	_check_scene("res://scenes/world/GreenhouseSector.tscn", [
		"Player",
		"FarmingManager",
		"CropPlot0",
		"TricksterPlot",
		"ArchiveDoor",
		"SaveTerminal",
		"LoadTerminal",
		"TileVisualPass",
	])
	_check_scene("res://scenes/world/ArchiveLibrary.tscn", [
		"Player",
		"FarmingManager",
		"TricksterPlot",
		"DexterTerminal",
		"GreenhouseDoor",
		"SaveTerminal",
		"LoadTerminal",
	])
	_check_scene("res://ui/hud/HUD.tscn", [
		"TopBar",
		"StatusLabel",
		"PromptLabel",
	])

	if _failures.is_empty():
		print("Godot smoke test passed.")
		quit(0)
	else:
		push_error("Godot smoke test failed.")
		for failure in _failures:
			push_error(failure)
		quit(1)


func _check_resource_exists(path: String) -> void:
	if not ResourceLoader.exists(path):
		_failures.append("Missing resource: %s" % path)


func _check_scene(path: String, expected_nodes: Array[String]) -> void:
	var packed := load(path)
	if packed == null:
		_failures.append("Could not load scene: %s" % path)
		return
	var scene = packed.instantiate()
	if scene == null:
		_failures.append("Could not instantiate scene: %s" % path)
		return
	root.add_child(scene)
	for node_name in expected_nodes:
		if scene.find_child(node_name, true, false) == null:
			_failures.append("%s missing node %s" % [path, node_name])
	scene.queue_free()
