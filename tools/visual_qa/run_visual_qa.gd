extends SceneTree

## Starlight Acre — Visual QA capture harness (post-promotion phase).
##
## Run from the repository root (windowed, NOT --headless):
##   godot --path . --script res://tools/visual_qa/run_visual_qa.gd
##
## What it does:
##   1. Captures at the canonical 640x360 internal pixel-art viewport.
##   2. Instantiates the REAL GreenhouseSector and EngineeringBay scenes
##      (player, HUD, drone, terminals, doors — the true live composition),
##      lets each settle, and saves a screenshot of the game view.
##   3. Extracts the exact atlas regions the live scenes consume (player
##      animation frames, Wisdom Fruit states, terminal sprites, HUD icons)
##      plus a true-scale reference set, from the canonical live PNGs,
##      into visual_qa_output/crops/.
##   4. Writes visual_qa_output/report.json describing the whole run.
##
## QA isolation: this harness never simulates input and never calls any
## gameplay function; the launcher runs it with an isolated HOME, so real
## user data and saves cannot be touched. No production scene or script is
## modified.

func _initialize() -> void:
	var runner := QARunner.new()
	root.add_child(runner)


class QARunner extends Node:
	const WINDOW_SIZE := Vector2i(640, 360)
	const SETTLE_FRAMES := 45
	const OUTPUT_DIR := "res://visual_qa_output"
	const CROPS_DIR := "res://visual_qa_output/crops"

	const SCENES := [
		{"id": "greenhouse", "file": "greenhouse.png", "path": "res://scenes/world/GreenhouseSector.tscn"},
		{"id": "engineering", "file": "engineering.png", "path": "res://scenes/world/EngineeringBay.tscn"},
	]

	## Exact atlas regions consumed by the live scenes:
	## Player.tscn (192x192 sheet, 32x48 frames), CropPlot.tscn (hframes=4),
	## RepairTerminal/ReplenishTerminal (64x64 halves), ResearchTerminal,
	## HUD.tscn (five 16x16 cells), plus whole canonical sprites.
	const CROPS := [
		{"id": "player_idle_0", "group": "player_frames", "src": "res://assets/sprites/player/player_sheet.png", "rect": [0, 0, 32, 48]},
		{"id": "player_idle_1", "group": "player_frames", "src": "res://assets/sprites/player/player_sheet.png", "rect": [32, 0, 32, 48]},
		{"id": "player_idle_2", "group": "player_frames", "src": "res://assets/sprites/player/player_sheet.png", "rect": [64, 0, 32, 48]},
		{"id": "player_idle_3", "group": "player_frames", "src": "res://assets/sprites/player/player_sheet.png", "rect": [96, 0, 32, 48]},
		{"id": "player_walk_0", "group": "player_frames", "src": "res://assets/sprites/player/player_sheet.png", "rect": [0, 48, 32, 48]},
		{"id": "player_walk_1", "group": "player_frames", "src": "res://assets/sprites/player/player_sheet.png", "rect": [32, 48, 32, 48]},
		{"id": "player_walk_2", "group": "player_frames", "src": "res://assets/sprites/player/player_sheet.png", "rect": [64, 48, 32, 48]},
		{"id": "player_walk_3", "group": "player_frames", "src": "res://assets/sprites/player/player_sheet.png", "rect": [96, 48, 32, 48]},
		{"id": "player_walk_4", "group": "player_frames", "src": "res://assets/sprites/player/player_sheet.png", "rect": [128, 48, 32, 48]},
		{"id": "player_walk_5", "group": "player_frames", "src": "res://assets/sprites/player/player_sheet.png", "rect": [160, 48, 32, 48]},
		{"id": "player_jump", "group": "player_frames", "src": "res://assets/sprites/player/player_sheet.png", "rect": [0, 96, 32, 48]},
		{"id": "player_fall", "group": "player_frames", "src": "res://assets/sprites/player/player_sheet.png", "rect": [32, 96, 32, 48]},
		{"id": "player_land", "group": "player_frames", "src": "res://assets/sprites/player/player_sheet.png", "rect": [64, 96, 32, 48]},
		{"id": "player_interact_0", "group": "player_frames", "src": "res://assets/sprites/player/player_sheet.png", "rect": [0, 144, 32, 48]},
		{"id": "player_interact_1", "group": "player_frames", "src": "res://assets/sprites/player/player_sheet.png", "rect": [32, 144, 32, 48]},
		{"id": "fruit_empty", "group": "fruit_states", "src": "res://assets/sprites/crops/wisdom_fruit_states.png", "rect": [0, 0, 32, 32]},
		{"id": "fruit_planted", "group": "fruit_states", "src": "res://assets/sprites/crops/wisdom_fruit_states.png", "rect": [32, 0, 32, 32]},
		{"id": "fruit_growing", "group": "fruit_states", "src": "res://assets/sprites/crops/wisdom_fruit_states.png", "rect": [64, 0, 32, 32]},
		{"id": "fruit_ready", "group": "fruit_states", "src": "res://assets/sprites/crops/wisdom_fruit_states.png", "rect": [96, 0, 32, 32]},
		{"id": "terminal_repair", "group": "terminals", "src": "res://assets/sprites/terminals/terminals.png", "rect": [0, 0, 32, 64]},
		{"id": "terminal_replenish", "group": "terminals", "src": "res://assets/sprites/terminals/terminals.png", "rect": [32, 0, 32, 64]},
		{"id": "terminal_research", "group": "terminals", "src": "res://assets/sprites/terminals/research_terminal.png", "rect": [0, 0, 64, 80]},
		{"id": "hud_water", "group": "hud_icons", "src": "res://assets/ui/icons/hud_icons.png", "rect": [0, 0, 16, 16]},
		{"id": "hud_nutrient", "group": "hud_icons", "src": "res://assets/ui/icons/hud_icons.png", "rect": [16, 0, 16, 16]},
		{"id": "hud_power", "group": "hud_icons", "src": "res://assets/ui/icons/hud_icons.png", "rect": [32, 0, 16, 16]},
		{"id": "hud_fruit", "group": "hud_icons", "src": "res://assets/ui/icons/hud_icons.png", "rect": [48, 0, 16, 16]},
		{"id": "hud_prompt", "group": "hud_icons", "src": "res://assets/ui/icons/hud_icons.png", "rect": [64, 0, 16, 16]},
		{"id": "scale_player", "group": "scale_row", "src": "res://assets/sprites/player/player_sheet.png", "rect": [0, 0, 32, 48]},
		{"id": "scale_gardener_drone", "group": "scale_row", "src": "res://assets/sprites/agents/gardener_drone.png", "rect": [0, 0, 32, 32]},
		{"id": "scale_wisdom_fruit", "group": "scale_row", "src": "res://assets/sprites/crops/wisdom_fruit_states.png", "rect": [96, 0, 32, 32]},
		{"id": "scale_repair_terminal", "group": "scale_row", "src": "res://assets/sprites/terminals/terminals.png", "rect": [0, 0, 32, 64]},
		{"id": "scale_research_terminal", "group": "scale_row", "src": "res://assets/sprites/terminals/research_terminal.png", "rect": [0, 0, 64, 80]},
		{"id": "scale_sector_door", "group": "scale_row", "src": "res://assets/sprites/fixtures/sector_door.png", "rect": [0, 0, 64, 112]},
		{"id": "scale_reactor_core", "group": "scale_row", "src": "res://assets/sprites/fixtures/reactor_core.png", "rect": [0, 0, 96, 96]},
	]

	var scene_results := {}
	var crop_results := {}
	var run_error := ""

	func _ready() -> void:
		_run()

	func _run() -> void:
		DisplayServer.window_set_size(WINDOW_SIZE)
		var dir := DirAccess.open("res://")
		if dir == null:
			run_error = "could not open the res:// base directory"
			_finish(false)
			return
		if not dir.dir_exists("visual_qa_output"):
			dir.make_dir_recursive("visual_qa_output")
		if not dir.dir_exists("visual_qa_output/crops"):
			dir.make_dir_recursive("visual_qa_output/crops")
		# Let the tree finish initializing (autoloads etc.) before touching scenes.
		await get_tree().process_frame

		var scenes_ok := true
		for spec in SCENES:
			var ok := await _capture_scene(spec)
			if not ok:
				scenes_ok = false

		var crops_ok := _extract_crops()
		_finish(scenes_ok and crops_ok)

	func _capture_scene(spec: Dictionary) -> bool:
		var entry := {"scene": spec["path"], "file": spec["file"], "status": "FAIL", "error": ""}
		scene_results[spec["id"]] = entry
		var packed_res := load(spec["path"])
		if not (packed_res is PackedScene):
			entry["error"] = "scene failed to load"
			push_error("VISUAL_QA: cannot load " + String(spec["path"]))
			return false
		var packed := packed_res as PackedScene
		var instance := packed.instantiate()
		get_tree().root.add_child(instance)
		for i in SETTLE_FRAMES:
			await get_tree().process_frame
		var image := get_viewport().get_texture().get_image()
		instance.queue_free()
		await get_tree().process_frame
		if image == null or image.is_empty():
			entry["error"] = "the captured image was empty (was Godot started with --headless?)"
			return false
		var path := OUTPUT_DIR + "/" + String(spec["file"])
		var err := image.save_png(path)
		if err != OK:
			entry["error"] = "save_png failed with error %d" % err
			return false
		entry["status"] = "OK"
		entry["size"] = [image.get_width(), image.get_height()]
		return true

	func _extract_crops() -> bool:
		var groups := {
			"player_frames": {"expected": 15, "written": 0, "errors": []},
			"fruit_states": {"expected": 4, "written": 0, "errors": []},
			"terminals": {"expected": 3, "written": 0, "errors": []},
			"hud_icons": {"expected": 5, "written": 0, "errors": []},
			"scale_row": {"expected": 7, "written": 0, "errors": []},
		}
		var cache := {}
		for crop in CROPS:
			var group: Dictionary = groups[crop["group"]]
			var src := String(crop["src"])
			if not cache.has(src):
				var tex := load(src) as Texture2D
				if tex == null:
					group["errors"].append("%s: cannot load %s" % [crop["id"], src])
					continue
				cache[src] = tex.get_image()
			var image: Image = cache[src]
			var r: Array = crop["rect"]
			var rect := Rect2i(r[0], r[1], r[2], r[3])
			if rect.position.x < 0 or rect.position.y < 0 \
					or rect.position.x + rect.size.x > image.get_width() \
					or rect.position.y + rect.size.y > image.get_height():
				group["errors"].append("%s: region %s is outside %s (%d x %d)" % [crop["id"], rect, src, image.get_width(), image.get_height()])
				continue
			var piece := image.get_region(rect)
			var err := piece.save_png(CROPS_DIR + "/" + String(crop["id"]) + ".png")
			if err != OK:
				group["errors"].append("%s: save_png failed with error %d" % [crop["id"], err])
				continue
			group["written"] += 1
		var all_ok := true
		for g in groups.values():
			var group: Dictionary = g
			group["status"] = "OK" if group["written"] == group["expected"] else "FAIL"
			if group["status"] != "OK":
				all_ok = false
		crop_results = groups
		return all_ok

	func _finish(ok: bool) -> void:
		var report := {
			"project": "starlight-acre",
			"qa_phase": "post-promotion-visual",
			"generated_at": Time.get_datetime_string_from_system(true),
			"godot_version": Engine.get_version_info().get("string", "unknown"),
			"window_size": [WINDOW_SIZE.x, WINDOW_SIZE.y],
			"settle_frames": SETTLE_FRAMES,
			"run_error": run_error,
			"captures": scene_results,
			"extractions": crop_results,
			"status": "OK" if ok else "FAIL",
		}
		var f := FileAccess.open(OUTPUT_DIR + "/report.json", FileAccess.WRITE)
		if f != null:
			f.store_string(JSON.stringify(report, "  "))
		get_tree().quit(0 if ok else 1)
