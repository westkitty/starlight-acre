extends Node2D

@export_file("*.tscn") var target_scene: String
@export var target_sector: String = ""
@export var target_spawn := Vector2.ZERO
@export var label := "Travel"

func interact() -> void:
	if target_scene.is_empty():
		return
	GameState.set_transition(target_sector, target_spawn)
	get_tree().change_scene_to_file(target_scene)

func get_prompt() -> String:
	return "E - %s" % label

func _on_area_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.register_interactable(self)

func _on_area_body_exited(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.unregister_interactable(self)
