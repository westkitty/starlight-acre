extends Node2D

@export var sector_id: String = "sector"

var _camera: Camera2D = null
var _background: Sprite2D = null

func _ready() -> void:
	GameState.current_sector = sector_id
	var player := get_node_or_null("Player") as Node2D
	if player != null:
		player.position = GameState.consume_spawn(player.position)
		_camera = player.get_node_or_null("Camera2D") as Camera2D
	_background = get_node_or_null("Background") as Sprite2D
	_sync_background()
	GameState.save_game()

func _process(_delta: float) -> void:
	_sync_background()

func _sync_background() -> void:
	if _camera == null or _background == null:
		return
	_background.global_position = _camera.get_screen_center_position()
