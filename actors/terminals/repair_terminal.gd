extends Node2D

func interact() -> void:
	var fm := get_tree().get_first_node_in_group("farming_manager")
	if fm != null:
		fm.restore_power()
	_refresh_prompt()

func get_prompt() -> String:
	var fm := get_tree().get_first_node_in_group("farming_manager")
	if fm != null and fm.power < 50.0:
		return "E - Repair Power Systems (1 Wisdom Fruit)"
	return "E - Stabilize Power Systems"

func _refresh_prompt() -> void:
	var player := get_tree().get_first_node_in_group("player")
	if player != null:
		player.register_interactable(self)

func _on_area_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.register_interactable(self)

func _on_area_body_exited(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.unregister_interactable(self)
