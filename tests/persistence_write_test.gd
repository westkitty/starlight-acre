extends SceneTree

func _initialize() -> void:
	var gs := root.get_node("GameState")
	gs.water = 8
	gs.nutrient = 7
	gs.wisdom_fruit = 11
	gs.chaos = 3
	gs.power = 63.5
	gs.emergency_resupplies = 1
	gs.upgrades = {
		"efficient_grid": true,
		"closed_loop_hydroponics": true,
		"paradox_trellis": true
	}
	gs.plot_states = {
		"greenhouse_plot_1": {
			"state": "GROWING",
			"growth_remaining": 12.25,
			"crop_id": "wisdom_fruit"
		},
		"greenhouse_plot_2": {
			"state": "READY",
			"growth_remaining": 0.0,
			"crop_id": "trickster_vine",
			"ready_dodges_remaining": 0,
			"runner_active": true,
			"dodge_offset_x": 72.0
		}
	}
	gs.current_sector = "engineering"
	gs.save_game()
	print("STARLIGHT_PERSISTENCE_WRITE_PASS")
	quit(0)
