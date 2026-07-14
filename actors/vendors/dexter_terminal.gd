# dexter_terminal.gd
# Prototype vendor encounter: one small trade, no rotating inventory yet.
extends Node2D

const WISDOM_COST := 2


func interact() -> void:
	var fm := get_tree().get_first_node_in_group("farming_manager")
	if fm == null:
		return
	if not fm.spend_resource("wisdom_fruit", WISDOM_COST):
		return
	fm.replenish_consumables()
	fm.restore_power()


func get_prompt() -> String:
	return "E - Trade 2 Wisdom Fruit with Dexter"


func _on_area_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.register_interactable(self)


func _on_area_body_exited(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.unregister_interactable(self)
