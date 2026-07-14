# hud.gd
# Renders resources and interaction prompt from Events signals.
extends CanvasLayer

@onready var _water_label: Label = $TopBar/Water/Value
@onready var _nutrient_label: Label = $TopBar/Nutrient/Value
@onready var _power_label: Label = $TopBar/Power/Value
@onready var _fruit_label: Label = $TopBar/WisdomFruit/Value
@onready var _trickster_label: Label = $TopBar/TricksterVine/Value
@onready var _prompt_label: Label = $PromptLabel


func _ready() -> void:
	Events.resource_changed.connect(_on_resource_changed)
	Events.interaction_prompt_changed.connect(_on_prompt_changed)
	_prompt_label.visible = false


func _on_resource_changed(resource_name: String, value: float) -> void:
	match resource_name:
		"water":
			_water_label.text = "%d/10" % int(value)
		"nutrient":
			_nutrient_label.text = "%d/10" % int(value)
		"power":
			_power_label.text = "%d%%" % int(value)
		"wisdom_fruit":
			_fruit_label.text = "%d" % int(value)
		"trickster_vine":
			_trickster_label.text = "%d" % int(value)


func _on_prompt_changed(prompt_text: String) -> void:
	_prompt_label.visible = not prompt_text.is_empty()
	_prompt_label.text = prompt_text
