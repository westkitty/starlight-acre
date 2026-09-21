class_name TricksterFruit
extends Node2D

signal caught

var _harvest_name := "Trickster Fruit"
var _player_in_range: Node = null
var _landing_position := Vector2.ZERO
var _settled := false

@onready var _sprite: Sprite2D = $Sprite

func configure(source_texture: Texture2D, harvest_name: String, target_offset_x: float, animate_jump: bool) -> void:
	_harvest_name = harvest_name
	_landing_position = Vector2(target_offset_x, -20.0)
	_settled = false
	if source_texture != null and source_texture.get_width() >= 128 and source_texture.get_height() >= 32:
		var atlas := AtlasTexture.new()
		atlas.atlas = source_texture
		atlas.region = Rect2(96, 0, 32, 24)
		_sprite.texture = atlas
	if animate_jump:
		position = Vector2(0.0, -20.0)
		var tween := create_tween()
		tween.tween_property(self, "position", Vector2(target_offset_x * 0.5, -52.0), 0.12).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tween.tween_property(self, "position", _landing_position, 0.16).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
		tween.finished.connect(_finish_jump)
	else:
		_finish_jump()

func _finish_jump() -> void:
	position = _landing_position
	_settled = true

func is_settled() -> bool:
	return _settled

func interact() -> void:
	if is_instance_valid(_player_in_range):
		_player_in_range.unregister_interactable(self)
	caught.emit()
	queue_free()

func get_prompt() -> String:
	return "E - Catch %s" % _harvest_name

func _on_area_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		_player_in_range = body
		body.register_interactable(self)

func _on_area_body_exited(body: Node2D) -> void:
	if body.is_in_group("player"):
		_player_in_range = null
		body.unregister_interactable(self)
