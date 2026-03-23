# repair_terminal.gd
# Interactable terminal that restores power to 100% when activated.
# Uses Area2D body_entered/exited to register with the player.
extends Node2D


func interact() -> void:
	var fm := get_tree().get_first_node_in_group("farming_manager")
	if fm != null:
		fm.restore_power()


func get_prompt() -> String:
	return "E — Repair Power Systems"


func _on_area_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.register_interactable(self)


func _on_area_body_exited(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.unregister_interactable(self)
