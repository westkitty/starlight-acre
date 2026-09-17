extends Node2D

@export var sector_id: String = "sector"

func _ready() -> void:
	GameState.current_sector = sector_id
	var player := get_node_or_null("Player") as Node2D
	if player != null:
		player.position = GameState.consume_spawn(player.position)
	GameState.save_game()
