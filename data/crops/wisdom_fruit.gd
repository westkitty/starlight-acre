class_name WisdomFruitDefinition
extends CropDefinition

func _init() -> void:
	crop_id = "wisdom_fruit"
	crop_name = "Wisdom Fruit"
	mythic_domain = "Athena / knowledge"
	mythic_note = "Cultivation converts station stewardship into research progress."
	growth_time = 30.0
	tend_bonus = 0.2
	water_cost = 1
	nutrient_cost = 1
	harvest_yield = 1
	station_effect_id = "research_currency"
