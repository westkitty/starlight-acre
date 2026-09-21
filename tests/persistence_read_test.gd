extends SceneTree

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	await process_frame
	var gs := root.get_node("GameState")
	var failures: Array[String] = []
	if gs.water != 8:
		failures.append("water did not survive relaunch")
	if gs.nutrient != 7:
		failures.append("nutrient did not survive relaunch")
	if gs.wisdom_fruit != 11:
		failures.append("wisdom fruit did not survive relaunch")
	if gs.chaos != 3:
		failures.append("chaos did not survive relaunch")
	if not is_equal_approx(gs.power, 63.5):
		failures.append("power did not survive relaunch")
	if gs.emergency_resupplies != 1:
		failures.append("emergency resupplies did not survive relaunch")
	if not gs.has_upgrade("efficient_grid"):
		failures.append("efficient_grid upgrade did not survive relaunch")
	if not gs.has_upgrade("closed_loop_hydroponics"):
		failures.append("closed_loop_hydroponics upgrade did not survive relaunch")
	if not gs.has_upgrade("paradox_trellis"):
		failures.append("paradox_trellis upgrade did not survive relaunch")
	var plot: Dictionary = gs.get_plot_state("greenhouse_plot_1")
	if str(plot.get("state", "")) != "GROWING":
		failures.append("plot state did not survive relaunch")
	if not is_equal_approx(float(plot.get("growth_remaining", -1.0)), 12.25):
		failures.append("plot growth timer did not survive relaunch")
	if str(plot.get("crop_id", "")) != "wisdom_fruit":
		failures.append("plot crop id did not survive relaunch")
	var trickster_plot: Dictionary = gs.get_plot_state("greenhouse_plot_2")
	if str(trickster_plot.get("crop_id", "")) != "trickster_vine":
		failures.append("trickster crop id did not survive relaunch")
	if not bool(trickster_plot.get("runner_active", false)):
		failures.append("trickster runner state did not survive relaunch")
	if int(trickster_plot.get("ready_dodges_remaining", -1)) != 0:
		failures.append("trickster dodge count did not survive relaunch")
	if not is_equal_approx(float(trickster_plot.get("dodge_offset_x", 0.0)), 72.0):
		failures.append("trickster dodge offset did not survive relaunch")
	if gs.current_sector != "engineering":
		failures.append("current sector did not survive relaunch")
	if failures.is_empty():
		var err := change_scene_to_file("res://scenes/world/Startup.tscn")
		if err != OK:
			failures.append("Startup scene could not load")
		else:
			await process_frame
			await process_frame
			await process_frame
			if current_scene == null or current_scene.name != "EngineeringBay":
				failures.append("fresh launch did not resume the saved Engineering sector")
	if failures.is_empty():
		print("STARLIGHT_PERSISTENCE_READ_PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		quit(1)
