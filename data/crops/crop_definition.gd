class_name CropDefinition
extends Resource

@export var crop_id: String = "crop"
@export var crop_name: String = "Crop"
@export var mythic_domain: String = ""
@export_multiline var mythic_note: String = ""
@export var growth_time: float = 30.0
@export_range(0.0, 0.9, 0.05) var tend_bonus: float = 0.2
@export var water_cost: int = 1
@export var nutrient_cost: int = 1
@export var harvest_yield: int = 1
@export var harvest_name: String = "Produce"
@export var harvest_resource_id: String = "wisdom_fruit"
@export_range(0, 3, 1) var ready_dodge_count: int = 0
@export_range(0.0, 128.0, 8.0) var ready_dodge_distance: float = 0.0
@export var drone_can_harvest: bool = true
@export var station_effect_id: String = ""
