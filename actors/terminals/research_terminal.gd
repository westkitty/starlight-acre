extends Node2D

func interact() -> void:
	var fm := get_tree().get_first_node_in_group("farming_manager")
	if fm == null:
		return
	if not GameState.has_upgrade("efficient_grid"):
		if fm.spend_wisdom_fruit(4):
			GameState.unlock_upgrade("efficient_grid")
			Events.station_message.emit("Efficient Grid unlocked: power drain reduced 40%.")
	elif not GameState.has_upgrade("closed_loop_hydroponics"):
		if fm.spend_wisdom_fruit(6):
			GameState.unlock_upgrade("closed_loop_hydroponics")
			Events.station_message.emit("Closed-Loop Hydroponics unlocked: 15-unit caps and free resupply.")
	_refresh_prompt()

func get_prompt() -> String:
	if not GameState.has_upgrade("efficient_grid"):
		return "E - Research Efficient Grid (4 Wisdom Fruit)"
	if not GameState.has_upgrade("closed_loop_hydroponics"):
		return "E - Research Closed-Loop Hydroponics (6 Wisdom Fruit)"
	return "Research complete"

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
