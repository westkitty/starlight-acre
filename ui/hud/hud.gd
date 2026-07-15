# hud.gd
# Renders the icon-led resource bar and interaction prompt.
# Driven entirely by Events signals - no direct coupling to game nodes.
extends CanvasLayer

@onready var _water_label: Label = $TopBar/Water/ValueLabel
@onready var _nutrient_label: Label = $TopBar/Nutrient/ValueLabel
@onready var _power_label: Label = $TopBar/Power/ValueLabel
@onready var _fruit_label: Label = $TopBar/Fruit/ValueLabel
@onready var _prompt_bar: Control = $PromptBar
@onready var _prompt_label: Label = $PromptBar/PromptLabel


func _ready() -> void:
	Events.resource_changed.connect(_on_resource_changed)
	Events.interaction_prompt_changed.connect(_on_prompt_changed)
	_prompt_bar.visible = false


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


func _on_prompt_changed(prompt_text: String) -> void:
	_prompt_bar.visible = not prompt_text.is_empty()
	_prompt_label.text = prompt_text
