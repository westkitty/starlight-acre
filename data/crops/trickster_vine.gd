# trickster_vine.gd
# Second crop prototype. Uses the shared CropDefinition shape with erratic growth behavior.
extends CropDefinition


func _init() -> void:
	crop_id = "trickster_vine"
	crop_name = "Trickster Vine"
	harvest_resource = "trickster_vine"
	growth_time = 24.0
	tend_bonus = 0.12
	water_cost = 1
	nutrient_cost = 2
	harvest_yield = 1
	behavior = "erratic_growth"
