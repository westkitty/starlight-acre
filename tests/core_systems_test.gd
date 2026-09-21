extends SceneTree

var failures: Array[String] = []

func _initialize() -> void:
	call_deferred("_run")

func _gs() -> Node:
	return root.get_node("GameState")

func _run() -> void:
	_reset_state()
	await _test_sector_round_trip()
	await _test_solar_flare_lifecycle()
	await _test_lightning_vine()
	await _test_camera_contract()
	await _test_greenhouse_tilemap_collision()
	await _test_startup_fallback()
	await _test_research_progression()
	await _test_mythic_ecology()
	await _test_trickster_vine()
	await _test_gardener_travel_and_harvest()
	if failures.is_empty():
		print("STARLIGHT_CORE_SYSTEMS_PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		quit(1)

func _reset_state() -> void:
	if current_scene != null:
		current_scene.process_mode = Node.PROCESS_MODE_DISABLED
	var gs := _gs()
	gs.water = 5
	gs.nutrient = 5
	gs.wisdom_fruit = 0
	gs.chaos = 0
	gs.power = 100.0
	gs.emergency_resupplies = 2
	gs.upgrades = {}
	gs.plot_states = {}
	gs.current_sector = "greenhouse"
	gs.next_player_position = Vector2.ZERO
	gs.reset_transient_hazards()
	gs.save_game()

func _test_sector_round_trip() -> void:
	var gs := _gs()
	var err := change_scene_to_file("res://scenes/world/GreenhouseSector.tscn")
	if err != OK:
		failures.append("could not enter GreenhouseSector")
		return
	await process_frame
	await process_frame
	var greenhouse := current_scene
	if greenhouse == null or greenhouse.name != "GreenhouseSector":
		failures.append("GreenhouseSector did not become current scene")
		return
	var door := greenhouse.get_node_or_null("EngineeringDoor")
	if door == null:
		failures.append("EngineeringDoor missing")
		return
	door.interact()
	await process_frame
	await process_frame
	var engineering := current_scene
	if engineering == null or engineering.name != "EngineeringBay":
		failures.append("EngineeringDoor did not enter EngineeringBay")
		return
	if gs.current_sector != "engineering":
		failures.append("engineering transition did not update current_sector")
	var engineering_player := engineering.get_node_or_null("Player") as Node2D
	if engineering_player == null or absf(engineering_player.position.x + 420.0) > 0.1 or engineering_player.position.y < 230.0 or engineering_player.position.y > 260.0:
		failures.append("engineering spawn position was not consumed correctly")
	var return_door := engineering.get_node_or_null("ReturnDoor")
	if return_door == null:
		failures.append("ReturnDoor missing")
		return
	return_door.interact()
	await process_frame
	await process_frame
	var returned := current_scene
	if returned == null or returned.name != "GreenhouseSector":
		failures.append("ReturnDoor did not return to GreenhouseSector")
		return
	if gs.current_sector != "greenhouse":
		failures.append("return transition did not update current_sector")
	var returned_player := returned.get_node_or_null("Player") as Node2D
	if returned_player == null or absf(returned_player.position.x - 350.0) > 0.1 or returned_player.position.y < 230.0 or returned_player.position.y > 260.0:
		failures.append("greenhouse return spawn position was not consumed correctly")

func _test_solar_flare_lifecycle() -> void:
	_reset_state()
	var gs := _gs()
	var err := change_scene_to_file("res://scenes/world/GreenhouseSector.tscn")
	if err != OK:
		failures.append("could not load GreenhouseSector for Solar Flare test")
		return
	await process_frame
	await process_frame
	var greenhouse := current_scene
	var controller := greenhouse.get_node_or_null("SolarFlareController")
	var manager := greenhouse.get_node_or_null("FarmingManager")
	var hud := greenhouse.get_node_or_null("HUD")
	var indicator := hud.get_node_or_null("FlareIndicator") as TextureRect if hud != null else null
	if controller == null or manager == null or indicator == null:
		failures.append("Solar Flare controller/HUD indicator missing in Greenhouse")
		return

	gs.solar_flare_phase = "calm"
	gs.solar_flare_time_remaining = 0.0
	controller.call("_process", 0.0)
	if gs.solar_flare_phase != "warning" or absf(gs.solar_flare_time_remaining - 5.0) > 0.01:
		failures.append("Solar Flare did not enter the 5-second warning phase")
	if not indicator.visible or indicator.modulate.a > 0.7:
		failures.append("Solar Flare warning indicator is not visible/dimmed")

	gs.solar_flare_time_remaining = 0.0
	controller.call("_process", 0.0)
	if gs.solar_flare_phase != "active" or absf(gs.solar_flare_time_remaining - 8.0) > 0.01:
		failures.append("Solar Flare did not enter the 8-second active phase")
	if absf(gs.hazard_power_drain_multiplier() - 5.0) > 0.001:
		failures.append("Solar Flare active power multiplier is not 5x")
	if not indicator.visible or indicator.modulate.a < 0.99:
		failures.append("Solar Flare active indicator is not fully visible")

	manager.set_process(false)
	gs.upgrades = {}
	gs.power = 100.0
	manager.call("_process", 1.0)
	if absf(gs.power - 98.335) > 0.02:
		failures.append("Solar Flare did not apply 5x base power drain")
	gs.upgrades = {"efficient_grid": true}
	gs.power = 100.0
	manager.call("_process", 1.0)
	if absf(gs.power - 99.001) > 0.02:
		failures.append("Efficient Grid did not mitigate Solar Flare power drain")

	gs.solar_flare_time_remaining = 0.0
	controller.call("_process", 0.0)
	if gs.solar_flare_phase != "calm" or absf(gs.solar_flare_time_remaining - 45.0) > 0.01:
		failures.append("Solar Flare did not return to the 45-second recovery phase")
	if indicator.visible or absf(gs.hazard_power_drain_multiplier() - 1.0) > 0.001:
		failures.append("Solar Flare clear state did not hide the indicator/reset drain")

	gs.solar_flare_phase = "warning"
	gs.solar_flare_time_remaining = 3.0
	var door := greenhouse.get_node_or_null("EngineeringDoor")
	if door == null:
		failures.append("EngineeringDoor missing during Solar Flare transition test")
		return
	door.interact()
	await process_frame
	await process_frame
	if current_scene == null or current_scene.name != "EngineeringBay":
		failures.append("Solar Flare transition test did not reach EngineeringBay")
		return
	if gs.solar_flare_phase != "warning" or gs.solar_flare_time_remaining <= 0.0 or gs.solar_flare_time_remaining > 3.0:
		failures.append("Solar Flare transient state did not survive sector transition")
	var engineering_controller := current_scene.get_node_or_null("SolarFlareController")
	var engineering_hud := current_scene.get_node_or_null("HUD")
	var engineering_indicator := engineering_hud.get_node_or_null("FlareIndicator") as TextureRect if engineering_hud != null else null
	if engineering_controller == null or engineering_indicator == null or not engineering_indicator.visible:
		failures.append("Solar Flare controller/indicator did not resume in EngineeringBay")

	# Boundary case: changing sectors exactly as the warning expires must advance
	# into the active flare, not reset the transient hazard to calm.
	gs.solar_flare_phase = "warning"
	gs.solar_flare_time_remaining = 0.0
	var return_door := current_scene.get_node_or_null("ReturnDoor")
	if return_door == null:
		failures.append("ReturnDoor missing during Solar Flare boundary test")
		return
	return_door.interact()
	await process_frame
	await process_frame
	if current_scene == null or current_scene.name != "GreenhouseSector":
		failures.append("Solar Flare boundary test did not return to Greenhouse")
		return
	if gs.solar_flare_phase != "active" or absf(gs.solar_flare_time_remaining - 8.0) > 0.1:
		failures.append("zero-time warning reset instead of advancing across a sector transition")

func _test_lightning_vine() -> void:
	_reset_state()
	var gs := _gs()
	var err := change_scene_to_file("res://scenes/world/GreenhouseSector.tscn")
	if err != OK:
		failures.append("could not load GreenhouseSector for Lightning Vine test")
		return
	await process_frame
	await process_frame
	var greenhouse := current_scene
	var plot := greenhouse.get_node_or_null("CropPlot0")
	var manager := greenhouse.get_node_or_null("FarmingManager")
	if plot == null or manager == null:
		failures.append("Lightning Vine plot/FarmingManager missing")
		return
	if plot.crop_definition == null or plot.crop_definition.crop_id != "lightning_vine":
		failures.append("CropPlot0 is not configured as Lightning Vine")
		return
	if plot.crop_definition.growth_time != 28.0 or plot.crop_definition.harvest_resource_id != "power" or plot.crop_definition.harvest_yield != 20:
		failures.append("Lightning Vine crop contract drifted")

	manager.set_process(false)
	plot.set("_growth_timer", 12.0)
	plot.call("_set_state", 2)
	if gs.conductive_lightning_vine_count() != 1:
		failures.append("GROWING Lightning Vine did not register as one flare conductor")
	gs.solar_flare_phase = "active"
	gs.solar_flare_time_remaining = 8.0
	if absf(gs.hazard_power_drain_multiplier() - 7.0) > 0.001:
		failures.append("one conductive Lightning Vine should amplify active flare drain from 5x to 7x")
	gs.power = 40.0
	manager.call("_process", 1.0)
	if absf(gs.power - 37.669) > 0.02:
		failures.append("7x Lightning-amplified Solar Flare drain is incorrect")

	gs.power = 40.0
	plot.call("_set_state", 3)
	plot.interact()
	if int(plot.get_state()) != 0:
		failures.append("harvesting Lightning Vine did not reset the plot")
	if absf(gs.power - 60.0) > 0.01:
		failures.append("Lightning Vine harvest did not restore exactly 20 station power")
	if gs.conductive_lightning_vine_count() != 0 or absf(gs.hazard_power_drain_multiplier() - 5.0) > 0.001:
		failures.append("harvesting Lightning Vine did not immediately remove its flare vulnerability")

	gs.power = 95.0
	plot.call("_set_state", 3)
	plot.interact()
	if absf(gs.power - 100.0) > 0.01:
		failures.append("Lightning Vine power harvest did not respect the 100% power cap")

	plot.set("_growth_timer", 12.0)
	plot.call("_set_state", 2)
	err = change_scene_to_file("res://scenes/world/EngineeringBay.tscn")
	if err != OK:
		failures.append("could not leave Greenhouse during Lightning Vine persistence test")
		return
	await process_frame
	await process_frame
	err = change_scene_to_file("res://scenes/world/GreenhouseSector.tscn")
	if err != OK:
		failures.append("could not reload Greenhouse during Lightning Vine persistence test")
		return
	await process_frame
	await process_frame
	plot = current_scene.get_node_or_null("CropPlot0")
	if plot == null or plot.crop_definition == null or plot.crop_definition.crop_id != "lightning_vine":
		failures.append("Lightning Vine plot did not survive sector reload")
		return
	var saved: Dictionary = gs.get_plot_state("greenhouse_plot_0")
	if str(saved.get("state", "")) != "GROWING" or str(saved.get("crop_id", "")) != "lightning_vine":
		failures.append("Lightning Vine growth state did not persist across sector reload")
	if gs.conductive_lightning_vine_count() != 1 or absf(gs.hazard_power_drain_multiplier() - 7.0) > 0.001:
		failures.append("reloaded Lightning Vine lost its active-flare conductor effect")

func _test_camera_contract() -> void:
	if int(ProjectSettings.get_setting("display/window/size/viewport_width", 0)) != 640:
		failures.append("internal viewport width is not 640")
	if int(ProjectSettings.get_setting("display/window/size/viewport_height", 0)) != 360:
		failures.append("internal viewport height is not 360")
	_reset_state()
	var err := change_scene_to_file("res://scenes/world/GreenhouseSector.tscn")
	if err != OK:
		failures.append("could not load GreenhouseSector for camera test")
		return
	await process_frame
	await process_frame
	await physics_frame
	var greenhouse := current_scene
	var player := greenhouse.get_node_or_null("Player") as CharacterBody2D
	var background := greenhouse.get_node_or_null("Background") as Sprite2D
	var camera := player.get_node_or_null("Camera2D") as Camera2D if player != null else null
	if player == null or background == null or camera == null:
		failures.append("Greenhouse camera/background contract nodes missing")
		return
	if not camera.enabled:
		failures.append("player Camera2D is not enabled")
	var center := camera.get_screen_center_position()
	if absf(center.x + 280.0) > 1.0 or absf(center.y - 116.0) > 1.0:
		failures.append("left-spawn camera center is not clamped to (-280, 116)")
	if background.global_position.distance_to(center) > 1.0:
		failures.append("Greenhouse background does not follow the camera center")
	var screen_x := player.global_position.x - center.x + 320.0
	if screen_x < 0.0 or screen_x > 640.0:
		failures.append("left-spawn player is outside the 640px camera view")

	player.global_position.x = 0.0
	await process_frame
	await physics_frame
	center = camera.get_screen_center_position()
	if absf(center.x) > 1.0 or absf(center.y - 116.0) > 1.0:
		failures.append("center-room camera did not follow the player")
	if background.global_position.distance_to(center) > 1.0:
		failures.append("Greenhouse background lost camera sync at room center")

	player.global_position.x = 500.0
	await process_frame
	await physics_frame
	center = camera.get_screen_center_position()
	if absf(center.x - 280.0) > 1.0 or absf(center.y - 116.0) > 1.0:
		failures.append("right-side camera center is not clamped to (280, 116)")
	if background.global_position.distance_to(center) > 1.0:
		failures.append("Greenhouse background lost camera sync at right limit")
	screen_x = player.global_position.x - center.x + 320.0
	if screen_x < 0.0 or screen_x > 640.0:
		failures.append("right-side player is outside the 640px camera view")

func _test_greenhouse_tilemap_collision() -> void:
	_reset_state()
	var err := change_scene_to_file("res://scenes/world/GreenhouseSector.tscn")
	if err != OK:
		failures.append("could not load GreenhouseSector for TileMap collision test")
		return
	await process_frame
	await physics_frame
	var greenhouse := current_scene
	var floor_tiles := greenhouse.get_node_or_null("TileMapLayer_Floor") as TileMapLayer
	var wall_tiles := greenhouse.get_node_or_null("TileMapLayer_Walls") as TileMapLayer
	if floor_tiles == null or wall_tiles == null:
		failures.append("painted Greenhouse TileMap layers missing")
		return
	if floor_tiles.get_used_cells().size() != 150:
		failures.append("Greenhouse floor TileMap should contain exactly 150 painted cells")
	if wall_tiles.get_used_cells().size() != 136:
		failures.append("Greenhouse wall TileMap should contain exactly 136 painted cells")
	if floor_tiles.tile_set == null or floor_tiles.tile_set.get_physics_layers_count() < 1:
		failures.append("Greenhouse TileSet has no physics layer")
		return

	for obsolete_node in ["Floor", "WallLeft", "WallRight"]:
		if greenhouse.get_node_or_null(obsolete_node) != null:
			failures.append("obsolete StaticBody collision stub still present: %s" % obsolete_node)
	await physics_frame

	var player := greenhouse.get_node_or_null("Player") as CharacterBody2D
	if player == null:
		failures.append("Player missing from Greenhouse TileMap collision test")
		return
	player.position = Vector2(0, 190)
	player.velocity = Vector2.ZERO
	for _i in range(90):
		await physics_frame
	if not player.is_on_floor():
		failures.append("player did not land on TileMap floor with collision stubs disabled")
	if absf(player.position.y - 264.0) > 1.5:
		failures.append("TileMap floor collision does not align to y=264")

	player.set_physics_process(false)
	player.position = Vector2(500, 264)
	var right_hit := player.move_and_collide(Vector2(200, 0))
	if right_hit == null or player.position.x > 587.0:
		failures.append("right TileMap wall did not block the player")
	player.position = Vector2(-500, 264)
	var left_hit := player.move_and_collide(Vector2(-200, 0))
	if left_hit == null or player.position.x < -587.0:
		failures.append("left TileMap wall did not block the player")

func _test_startup_fallback() -> void:
	var gs := _gs()
	gs.current_sector = "not_a_real_sector"
	gs.next_player_position = Vector2(999, 999)
	var err := change_scene_to_file("res://scenes/world/Startup.tscn")
	if err != OK:
		failures.append("could not load Startup for fallback test")
		return
	await process_frame
	await process_frame
	await process_frame
	if current_scene == null or current_scene.name != "GreenhouseSector":
		failures.append("invalid saved sector did not fall back to GreenhouseSector")
	if gs.current_sector != "greenhouse":
		failures.append("invalid saved sector was not normalized to greenhouse")

func _test_research_progression() -> void:
	var gs := _gs()
	gs.wisdom_fruit = 10
	gs.chaos = 3
	gs.upgrades = {}
	var err := change_scene_to_file("res://scenes/world/EngineeringBay.tscn")
	if err != OK:
		failures.append("could not load EngineeringBay for research test")
		return
	await process_frame
	await process_frame
	var terminal := current_scene.get_node_or_null("ResearchTerminal")
	if terminal == null:
		failures.append("ResearchTerminal missing")
		return
	terminal.interact()
	if not gs.has_upgrade("efficient_grid"):
		failures.append("Efficient Grid purchase failed")
	if gs.wisdom_fruit != 6:
		failures.append("Efficient Grid cost was not exactly 4 Wisdom Fruit")
	if not is_equal_approx(gs.power_drain_multiplier(), 0.6):
		failures.append("Efficient Grid did not reduce power drain multiplier to 0.6")
	terminal.interact()
	if not gs.has_upgrade("closed_loop_hydroponics"):
		failures.append("Closed-Loop Hydroponics purchase failed")
	if gs.wisdom_fruit != 0:
		failures.append("Closed-Loop Hydroponics cost was not exactly 6 Wisdom Fruit")
	if gs.water_cap() != 15 or gs.nutrient_cap() != 15:
		failures.append("Closed-Loop Hydroponics did not raise both caps to 15")
	if terminal.get_prompt() != "E - Research Paradox Trellis (3 Chaos)":
		failures.append("Paradox Trellis research prompt missing after Wisdom upgrades")
	terminal.interact()
	if not gs.has_upgrade("paradox_trellis"):
		failures.append("Paradox Trellis purchase failed")
	if gs.chaos != 0:
		failures.append("Paradox Trellis cost was not exactly 3 Chaos")

func _test_mythic_ecology() -> void:
	var gs := _gs()
	_reset_state()
	gs.power = 0.0
	var err := change_scene_to_file("res://scenes/world/GreenhouseSector.tscn")
	if err != OK:
		failures.append("could not load GreenhouseSector for Mythic Ecology test")
		return
	await process_frame
	await process_frame
	var greenhouse := current_scene
	var wisdom := greenhouse.get_node_or_null("CropPlot1")
	var trickster := greenhouse.get_node_or_null("CropPlot2")
	var gardener := greenhouse.get_node_or_null("GardenerDrone")
	if wisdom == null or trickster == null or gardener == null:
		failures.append("Wisdom/Trickster/Gardener ecology fixtures missing")
		return
	gardener.auto_tend = false
	gardener.auto_harvest = false
	root.get_node("Events").resource_changed.emit("power", 0.0)

	wisdom.set("_growth_timer", 20.0)
	wisdom.call("_set_state", 2)
	trickster.set("_growth_timer", 20.0)
	trickster.call("_set_state", 2)

	wisdom.interact()
	var wisdom_saved: Dictionary = gs.get_plot_state("greenhouse_plot_1")
	var trickster_saved: Dictionary = gs.get_plot_state("greenhouse_plot_2")
	if not is_equal_approx(float(wisdom_saved.get("growth_remaining", -1.0)), 20.0):
		failures.append("Trickster steal should cancel the first Wisdom tend")
	if not is_equal_approx(float(trickster_saved.get("growth_remaining", -1.0)), 16.0):
		failures.append("Trickster did not steal the 4-second Wisdom tend pulse")
	if bool(trickster_saved.get("ecology_steal_available", true)):
		failures.append("Trickster should only steal one tend pulse per growth cycle")

	wisdom.interact()
	wisdom_saved = gs.get_plot_state("greenhouse_plot_1")
	trickster_saved = gs.get_plot_state("greenhouse_plot_2")
	if not is_equal_approx(float(wisdom_saved.get("growth_remaining", -1.0)), 16.0):
		failures.append("second Wisdom tend should work after Trickster is sated")
	if not is_equal_approx(float(trickster_saved.get("growth_remaining", -1.0)), 16.0):
		failures.append("Trickster stole more than one tend pulse in one growth cycle")

	err = change_scene_to_file("res://scenes/world/EngineeringBay.tscn")
	if err != OK:
		failures.append("could not leave Greenhouse during ecology persistence test")
		return
	await process_frame
	await process_frame
	err = change_scene_to_file("res://scenes/world/GreenhouseSector.tscn")
	if err != OK:
		failures.append("could not reload Greenhouse during ecology persistence test")
		return
	await process_frame
	await process_frame
	trickster = current_scene.get_node_or_null("CropPlot2")
	if trickster == null:
		failures.append("Trickster plot missing after ecology reload")
		return
	trickster_saved = gs.get_plot_state("greenhouse_plot_2")
	if bool(trickster_saved.get("ecology_steal_available", true)):
		failures.append("Trickster steal availability did not persist across sector reload")
	if bool(trickster.get("_ecology_steal_available")):
		failures.append("reloaded Trickster forgot that its one steal was already spent")

	var reloaded_gardener := current_scene.get_node_or_null("GardenerDrone")
	wisdom = current_scene.get_node_or_null("CropPlot1")
	if reloaded_gardener == null or wisdom == null:
		failures.append("ecology upgrade fixtures missing after reload")
		return
	reloaded_gardener.auto_tend = false
	reloaded_gardener.auto_harvest = false
	gs.upgrades["paradox_trellis"] = true
	wisdom.set("_growth_timer", 20.0)
	wisdom.call("_set_state", 2)
	trickster.call("_set_state", 0)
	trickster.set("_growth_timer", 20.0)
	trickster.call("_set_state", 2)
	wisdom.interact()
	wisdom_saved = gs.get_plot_state("greenhouse_plot_1")
	trickster_saved = gs.get_plot_state("greenhouse_plot_2")
	if not is_equal_approx(float(wisdom_saved.get("growth_remaining", -1.0)), 16.0):
		failures.append("Paradox Trellis did not preserve the Wisdom tend pulse")
	if not is_equal_approx(float(trickster_saved.get("growth_remaining", -1.0)), 16.0):
		failures.append("Paradox Trellis did not preserve the Trickster stolen pulse")
	if bool(trickster_saved.get("ecology_steal_available", true)):
		failures.append("Paradox Trellis should not make Trickster steal more than once")

func _test_trickster_vine() -> void:
	var gs := _gs()
	_reset_state()
	var err := change_scene_to_file("res://scenes/world/GreenhouseSector.tscn")
	if err != OK:
		failures.append("could not load GreenhouseSector for Trickster Vine test")
		return
	await process_frame
	await process_frame
	var greenhouse := current_scene
	var plot := greenhouse.get_node_or_null("CropPlot2")
	if plot == null:
		failures.append("Trickster Vine plot missing")
		return
	if plot.crop_definition == null or plot.crop_definition.crop_id != "trickster_vine":
		failures.append("CropPlot2 is not configured as Trickster Vine")
		return

	plot.call("_set_state", 3)
	if plot.can_drone_harvest():
		failures.append("Gardener must not auto-harvest Trickster Vine")
	plot.interact()
	if int(plot.get_state()) != 3:
		failures.append("first Trickster harvest attempt should leave crop READY")
	if gs.chaos != 0 or gs.wisdom_fruit != 0:
		failures.append("Trickster dodge incorrectly awarded produce")

	var saved: Dictionary = gs.get_plot_state("greenhouse_plot_2")
	if not bool(saved.get("runner_active", false)):
		failures.append("Trickster runner state was not persisted after dodge")
	if int(saved.get("ready_dodges_remaining", -1)) != 0:
		failures.append("Trickster dodge count did not decrement to zero")
	var dodge_offset := float(saved.get("dodge_offset_x", 0.0))
	if not is_equal_approx(absf(dodge_offset), 72.0):
		failures.append("Trickster dodge distance was not exactly 72 pixels")

	var runner := plot.get_node_or_null("TricksterFruit")
	if runner == null:
		failures.append("Trickster flee event did not create a fruit entity")
	else:
		for _i in range(60):
			if bool(runner.call("is_settled")):
				break
			await process_frame
		if not bool(runner.call("is_settled")):
			failures.append("Trickster fruit jump did not settle within 60 frames")
		elif not is_equal_approx(float(runner.position.x), dodge_offset):
			failures.append("Trickster fruit did not land at the persisted flee position")
	var plot_area := plot.get_node_or_null("Area2D") as Area2D
	if plot_area == null or not plot_area.position.is_equal_approx(Vector2.ZERO):
		failures.append("base crop interaction area moved with fleeing fruit")

	err = change_scene_to_file("res://scenes/world/EngineeringBay.tscn")
	if err != OK:
		failures.append("could not leave Greenhouse during Trickster persistence test")
		return
	await process_frame
	await process_frame
	err = change_scene_to_file("res://scenes/world/GreenhouseSector.tscn")
	if err != OK:
		failures.append("could not reload Greenhouse during Trickster persistence test")
		return
	await process_frame
	await process_frame
	plot = current_scene.get_node_or_null("CropPlot2")
	if plot == null:
		failures.append("Trickster Vine plot missing after reload")
		return
	saved = gs.get_plot_state("greenhouse_plot_2")
	dodge_offset = float(saved.get("dodge_offset_x", 0.0))
	runner = plot.get_node_or_null("TricksterFruit")
	if int(plot.get_state()) != 3 or not bool(saved.get("runner_active", false)):
		failures.append("Trickster escaped READY state did not survive scene reload")
	if runner == null:
		failures.append("Trickster fruit entity did not respawn after scene reload")
	elif not is_equal_approx(float(runner.position.x), dodge_offset):
		failures.append("Trickster fruit catch position did not survive scene reload")

	if runner != null:
		runner.interact()
		await process_frame
	if int(plot.get_state()) != 0:
		failures.append("catching Trickster fruit did not reset the crop")
	if gs.chaos != 1:
		failures.append("Trickster harvest did not award exactly 1 Chaos")
	if gs.wisdom_fruit != 0:
		failures.append("Trickster harvest incorrectly awarded Wisdom Fruit")
	saved = gs.get_plot_state("greenhouse_plot_2")
	if str(saved.get("state", "")) != "EMPTY" or bool(saved.get("runner_active", true)):
		failures.append("Trickster plot did not reset cleanly after catch")

func _test_gardener_travel_and_harvest() -> void:
	var gs := _gs()
	_reset_state()
	var err := change_scene_to_file("res://scenes/world/GreenhouseSector.tscn")
	if err != OK:
		failures.append("could not load GreenhouseSector for Gardener test")
		return
	await process_frame
	await process_frame
	var greenhouse := current_scene
	var gardener := greenhouse.get_node_or_null("GardenerDrone")
	var plot := greenhouse.get_node_or_null("CropPlot1")
	if gardener == null or plot == null:
		failures.append("Gardener or target Wisdom CropPlot missing")
		return
	gardener.move_speed = 1000.0
	gardener.interaction_radius = 20.0
	gardener.global_position.x = -300.0
	var start_x: float = gardener.global_position.x
	plot.call("_set_state", 3)
	for _i in range(45):
		await process_frame
	if absf(gardener.global_position.x - start_x) <= 50.0:
		failures.append("Gardener did not travel toward the distant crop")
	if int(plot.get_state()) != 0:
		failures.append("Gardener did not harvest the READY crop")
	if gs.wisdom_fruit != 1:
		failures.append("Gardener harvest did not award exactly 1 Wisdom Fruit")
