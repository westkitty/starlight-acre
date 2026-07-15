# hud.gd
# Renders the resource bar (Water, Nutrient, Power, Wisdom Fruit)
# and the interaction prompt label.
# Driven entirely by Events signals — no direct coupling to game nodes.
extends CanvasLayer

@onready var _water_label: Label = $TopBar/WaterLabel
@onready var _nutrient_label: Label = $TopBar/NutrientLabel
@onready var _power_label: Label = $TopBar/PowerLabel
@onready var _fruit_label: Label = $TopBar/FruitLabel
@onready var _prompt_label: Label = $PromptLabel


func _ready() -> void:
	Events.resource_changed.connect(_on_resource_changed)
	Events.interaction_prompt_changed.connect(_on_prompt_changed)
	_prompt_label.visible = false


func _on_resource_changed(resource_name: String, value: float) -> void:
	match resource_name:
		"water":
			_water_label.text = "Water: %d/10" % int(value)
		"nutrient":
			_nutrient_label.text = "Nutrient: %d/10" % int(value)
		"power":
			_power_label.text = "Power: %d%%" % int(value)
		"wisdom_fruit":
			_fruit_label.text = "Wisdom Fruit: %d" % int(value)


func _on_prompt_changed(prompt_text: String) -> void:
	_prompt_label.visible = not prompt_text.is_empty()
	_prompt_label.text = prompt_text
