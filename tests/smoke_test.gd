extends SceneTree

func _initialize() -> void:
	var failures: Array[String] = []
	var required := [
		"res://scenes/world/Startup.tscn",
		"res://scenes/world/GreenhouseSector.tscn",
		"res://scenes/world/EngineeringBay.tscn",
		"res://actors/crops/CropPlot.tscn",
		"res://actors/terminals/ResearchTerminal.tscn",
		"res://systems/hazards/SolarFlareController.tscn",
		"res://data/crops/wisdom_fruit.tres",
		"res://data/crops/trickster_vine.tres"
	]
	for path in required:
		if load(path) == null:
			failures.append("failed to load %s" % path)
	var crop := load("res://data/crops/wisdom_fruit.tres") as CropDefinition
	if crop == null or crop.crop_id != "wisdom_fruit":
		failures.append("Wisdom Fruit definition invalid")
	var trickster := load("res://data/crops/trickster_vine.tres") as CropDefinition
	if trickster == null or trickster.crop_id != "trickster_vine" or trickster.ready_dodge_count != 1:
		failures.append("Trickster Vine definition invalid")
	if Engine.get_version_info().major != 4:
		failures.append("unexpected Godot major version")
	if failures.is_empty():
		print("STARLIGHT_SMOKE_PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		quit(1)
