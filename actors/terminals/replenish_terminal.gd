# replenish_terminal.gd
# Interactable terminal that restores Water and Nutrient to cap.
# Uses Area2D body_entered/exited to register with the player.
extends Node2D


func interact() -> void:
	var fm := get_tree().get_first_node_in_group("farming_manager")
	if fm != null:
		fm.replenish_consumables()


func get_prompt() -> String:
	return "E — Replenish Water & Nutrients"


func _on_area_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.register_interactable(self)


func _on_area_body_exited(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.unregister_interactable(self)
