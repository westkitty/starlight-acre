extends Node

const SECTOR_SCENES := {
	"greenhouse": "res://scenes/world/GreenhouseSector.tscn",
	"engineering": "res://scenes/world/EngineeringBay.tscn"
}

func _ready() -> void:
	var target: String = SECTOR_SCENES.get(GameState.current_sector, SECTOR_SCENES["greenhouse"])
	if not SECTOR_SCENES.has(GameState.current_sector):
		GameState.current_sector = "greenhouse"
	GameState.next_player_position = Vector2.ZERO
	call_deferred("_enter_sector", target)

func _enter_sector(target: String) -> void:
	var error := get_tree().change_scene_to_file(target)
	if error != OK:
		push_error("Failed to load startup sector: %s" % target)
