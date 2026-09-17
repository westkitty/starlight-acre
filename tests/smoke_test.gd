extends SceneTree

func _initialize() -> void:
	var failures: Array[String] = []
	var required := [
		"res://scenes/world/GreenhouseSector.tscn",
		"res://scenes/world/EngineeringBay.tscn",
		"res://actors/crops/CropPlot.tscn",
		"res://actors/terminals/ResearchTerminal.tscn",
		"res://data/crops/wisdom_fruit.tres"
	]
	for path in required:
		if load(path) == null:
			failures.append("failed to load %s" % path)
	var crop := load("res://data/crops/wisdom_fruit.tres") as CropDefinition
	if crop == null or crop.crop_id != "wisdom_fruit":
		failures.append("Wisdom Fruit definition invalid")
	if Engine.get_version_info().major != 4:
		failures.append("unexpected Godot major version")
	if failures.is_empty():
		print("STARLIGHT_SMOKE_PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		quit(1)
