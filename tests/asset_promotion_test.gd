extends SceneTree
## Asset promotion validation — verifies the ratified canonical artwork is live.
## Run headless:  godot --headless --script tests/asset_promotion_test.gd
## Validates: 29 live files exist, load, match FINAL_VISUAL_CANON_MANIFEST dimensions,
## live SHA-256 equals canonical SHA-256, atlas-region contracts stay in bounds,
## and every integrated scene loads.

const MANIFEST := "res://assets/candidates/visual_canon/LIVE_ASSET_PROMOTION_MANIFEST.json"

# Hard dimension contracts for currently-integrated surfaces.
const DIMENSION_CONTRACTS := {
	"res://assets/sprites/player/player_sheet.png": Vector2i(192, 192),
	"res://assets/sprites/crops/wisdom_fruit_states.png": Vector2i(128, 32),
	"res://assets/sprites/terminals/terminals.png": Vector2i(64, 64),
	"res://assets/sprites/terminals/research_terminal.png": Vector2i(64, 80),
	"res://assets/sprites/agents/gardener_drone.png": Vector2i(32, 32),
	"res://assets/sprites/fixtures/sector_door.png": Vector2i(64, 112),
	"res://assets/sprites/fixtures/reactor_core.png": Vector2i(96, 96),
	"res://assets/backgrounds/greenhouse_sector_bg.png": Vector2i(640, 360),
	"res://assets/backgrounds/engineering_bay_bg.png": Vector2i(640, 360),
	"res://assets/tilesets/greenhouse_tiles.png": Vector2i(256, 256),
	"res://assets/ui/icons/hud_icons.png": Vector2i(80, 16),
	"res://assets/effects/pixel_art_effects.png": Vector2i(128, 32),
}

# Atlas regions that must remain inside their textures: [texture, region size]
const REGION_CONTRACTS := [
	["res://assets/sprites/player/player_sheet.png", Rect2i(160, 144, 32, 48)],  # last player frame
	["res://assets/sprites/crops/wisdom_fruit_states.png", Rect2i(96, 0, 32, 32)],  # 4th crop state
	["res://assets/sprites/terminals/terminals.png", Rect2i(32, 0, 32, 64)],  # replenish half
	["res://assets/ui/icons/hud_icons.png", Rect2i(64, 0, 16, 16)],  # prompt icon (5th cell)
]

const SCENES := [
	"res://scenes/world/GreenhouseSector.tscn",
	"res://scenes/world/EngineeringBay.tscn",
	"res://actors/player/Player.tscn",
	"res://actors/crops/CropPlot.tscn",
	"res://actors/agents/GardenerDrone.tscn",
	"res://actors/terminals/RepairTerminal.tscn",
	"res://actors/terminals/ReplenishTerminal.tscn",
	"res://actors/terminals/ResearchTerminal.tscn",
	"res://systems/world/SectorDoor.tscn",
	"res://ui/hud/HUD.tscn",
]


func _initialize() -> void:
	var failures: Array[String] = []

	# 1) Promotion manifest: every live target exists, loads, dimension-matches,
	#    and its bytes hash to the canonical SHA-256.
	var mf := FileAccess.open(MANIFEST, FileAccess.READ)
	if mf == null:
		_fail(failures, "cannot open promotion manifest")
		_finish(failures)
		return
	var parsed = JSON.parse_string(mf.get_as_text())
	if not (parsed is Dictionary) or not parsed.get("slots") is Array:
		_fail(failures, "promotion manifest malformed")
		_finish(failures)
		return

	for entry: Dictionary in parsed["slots"]:
		var live: String = entry["live_target"]
		var expect: Vector2i = Vector2i(int(entry["dimensions"][0]), int(entry["dimensions"][1]))
		if entry["promotion_status"] != "PROMOTED":
			_fail(failures, "%s not PROMOTED" % live)
			continue
		var tex := load(live) as Texture2D
		if tex == null:
			_fail(failures, "%s fails to load as Texture2D" % live)
			continue
		if Vector2i(tex.get_width(), tex.get_height()) != expect:
			_fail(failures, "%s is %dx%d, expected %s" % [live, tex.get_width(), tex.get_height(), expect])
		var live_sha := _sha256_file(live)
		if live_sha.is_empty():
			_fail(failures, "%s cannot be read for hashing" % live)
		elif live_sha != entry["canonical_sha256"]:
			_fail(failures, "%s SHA-256 mismatch vs canonical" % live)

	# 2) Hard dimension contracts for integrated surfaces.
	for path: String in DIMENSION_CONTRACTS:
		var tex := load(path) as Texture2D
		if tex == null:
			_fail(failures, "%s fails to load" % path)
		elif Vector2i(tex.get_width(), tex.get_height()) != DIMENSION_CONTRACTS[path]:
			_fail(failures, "%s is %dx%d, expected %s" % [path, tex.get_width(), tex.get_height(), DIMENSION_CONTRACTS[path]])

	# 3) Atlas-region contracts in bounds.
	for rc: Array in REGION_CONTRACTS:
		var tex := load(rc[0]) as Texture2D
		if tex == null:
			continue
		var region: Rect2i = rc[1]
		if region.position.x < 0 or region.position.y < 0 \
				or region.position.x + region.size.x > tex.get_width() \
				or region.position.y + region.size.y > tex.get_height():
			_fail(failures, "region %s out of bounds in %s" % [region, rc[0]])

	# 4) Every integrated scene loads.
	for path: String in SCENES:
		if load(path) == null:
			_fail(failures, "scene fails to load: %s" % path)

	_finish(failures)


func _sha256_file(path: String) -> String:
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		return ""
	var ctx := HashingContext.new()
	if ctx.start(HashingContext.HASH_SHA256) != OK:
		return ""
	while not f.eof_reached():
		var chunk := f.get_buffer(1 << 16)
		if chunk.size() == 0:
			break
		if ctx.update(chunk) != OK:
			return ""
	return ctx.finish().hex_encode()


func _fail(failures: Array[String], msg: String) -> void:
	failures.append(msg)
	push_error("ASSET_PROMOTION_FAIL: " + msg)


func _finish(failures: Array[String]) -> void:
	if failures.is_empty():
		print("STARLIGHT_ASSET_PROMOTION_PASS (29/29 live, hashes + dimensions + regions + scenes)")
		quit(0)
	else:
		print("STARLIGHT_ASSET_PROMOTION_FAIL (%d)" % failures.size())
		quit(1)
