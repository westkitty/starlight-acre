# save_terminal.gd
# Small interactable wrapper around GameState save/load.
extends Node2D

@export_enum("save", "load") var action: String = "save"


func interact() -> void:
	if action == "save":
		GameState.save_game()
	else:
		GameState.load_game()


func get_prompt() -> String:
	if action == "save":
		return "E - Save Station State"
	return "E - Load Station State"


func _on_area_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.register_interactable(self)


func _on_area_body_exited(body: Node2D) -> void:
	if body.is_in_group("player"):
		body.unregister_interactable(self)
