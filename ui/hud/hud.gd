extends CanvasLayer

@onready var _water_label: Label = $TopBar/Water/ValueLabel
@onready var _nutrient_label: Label = $TopBar/Nutrient/ValueLabel
@onready var _power_label: Label = $TopBar/Power/ValueLabel
@onready var _fruit_label: Label = $TopBar/Fruit/ValueLabel
@onready var _prompt_bar: Control = $PromptBar
@onready var _prompt_label: Label = $PromptBar/PromptLabel
@onready var _status_label: Label = $StatusLabel
var _status_timer := 0.0

func _ready() -> void:
	Events.resource_changed.connect(_on_resource_changed)
	Events.interaction_prompt_changed.connect(_on_prompt_changed)
	Events.station_message.connect(_on_station_message)
	Events.upgrade_unlocked.connect(_on_upgrade_unlocked)
	_prompt_bar.visible = false
	_status_label.visible = false

func _process(delta: float) -> void:
	if _status_timer <= 0.0:
		return
	_status_timer -= delta
	if _status_timer <= 0.0:
		_status_label.visible = false

func _on_resource_changed(resource_name: String, value: float) -> void:
	match resource_name:
		"water":
			_water_label.text = "%d/%d" % [int(value), GameState.water_cap()]
		"nutrient":
			_nutrient_label.text = "%d/%d" % [int(value), GameState.nutrient_cap()]
		"power":
			_power_label.text = "%d%%" % int(value)
		"wisdom_fruit":
			_fruit_label.text = "%d" % int(value)

func _on_prompt_changed(prompt_text: String) -> void:
	_prompt_bar.visible = not prompt_text.is_empty()
	_prompt_label.text = prompt_text

func _on_station_message(text: String) -> void:
	_status_label.text = text
	_status_label.visible = true
	_status_timer = 3.5

func _on_upgrade_unlocked(upgrade_id: String) -> void:
	_on_station_message("Station upgrade unlocked: %s" % upgrade_id.replace("_", " ").capitalize())
