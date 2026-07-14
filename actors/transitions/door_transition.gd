# door_transition.gd
# Interactable door that moves the player to another sector scene.
extends Node2D

@export_file("*.tscn") var target_scene_path: String = "res://scenes/world/GreenhouseSector.tscn"
@export var target_spawn_name: String = "PlayerSpawn"
@export var prompt_text: String = "E - Enter"


func interact() -> void:
	GameState.request_transition(target_scene_path, target_spawn_name)


func get_prompt() -> String:
	return prompt_text


func _on_area_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.register_interactable(self)


func _on_area_body_exited(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.unregister_interactable(self)
