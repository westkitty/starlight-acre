# farming_manager.gd
# Owns session resource state and passive power drain.
# Lives as a child Node of the active sector, not as an autoload.
extends Node

const WATER_MAX := 10
const NUTRIENT_MAX := 10
const POWER_DRAIN_PER_SECOND := 0.333  # ~1% per 3 seconds

var water: int = 5
var nutrient: int = 5
var wisdom_fruit: int = 0
var trickster_vine: int = 0
var power: float = 100.0


func _ready() -> void:
	add_to_group("farming_manager")
	_apply_pending_save_data()
	_broadcast_all()


func _process(delta: float) -> void:
	if power <= 0.0:
		return
	power -= POWER_DRAIN_PER_SECOND * delta
	if power < 0.0:
		power = 0.0
	Events.resource_changed.emit("power", power)


# --- Read ---

func can_plant(water_cost: int, nutrient_cost: int) -> bool:
	return water >= water_cost and nutrient >= nutrient_cost


func get_resource_value(resource_name: String) -> int:
	match resource_name:
		"water": return water
		"nutrient": return nutrient
		"wisdom_fruit": return wisdom_fruit
		"trickster_vine": return trickster_vine
	return 0


func get_save_data() -> Dictionary:
	return {
		"water": water,
		"nutrient": nutrient,
		"wisdom_fruit": wisdom_fruit,
		"trickster_vine": trickster_vine,
		"power": power,
	}


# --- Write ---

func spend_water(amount: int) -> void:
	water = maxi(0, water - amount)
	Events.resource_changed.emit("water", float(water))


func spend_nutrient(amount: int) -> void:
	nutrient = maxi(0, nutrient - amount)
	Events.resource_changed.emit("nutrient", float(nutrient))


func spend_resource(resource_name: String, amount: int) -> bool:
	if get_resource_value(resource_name) < amount:
		return false
	match resource_name:
		"water":
			water -= amount
		"nutrient":
			nutrient -= amount
		"wisdom_fruit":
			wisdom_fruit -= amount
		"trickster_vine":
			trickster_vine -= amount
		_:
			return false
	Events.resource_changed.emit(resource_name, float(get_resource_value(resource_name)))
	return true


func add_wisdom_fruit(amount: int) -> void:
	add_harvest("wisdom_fruit", amount)


func add_harvest(resource_name: String, amount: int) -> void:
	match resource_name:
		"wisdom_fruit":
			wisdom_fruit += amount
		"trickster_vine":
			trickster_vine += amount
		_:
			return
	Events.resource_changed.emit(resource_name, float(get_resource_value(resource_name)))


func restore_power() -> void:
	power = 100.0
	Events.resource_changed.emit("power", power)


func replenish_consumables() -> void:
	water = WATER_MAX
	nutrient = NUTRIENT_MAX
	Events.resource_changed.emit("water", float(water))
	Events.resource_changed.emit("nutrient", float(nutrient))


func _apply_pending_save_data() -> void:
	if not GameState.has_pending_load():
		return
	var data := GameState.get_pending_resources()
	if data.is_empty():
		return
	water = int(data.get("water", water))
	nutrient = int(data.get("nutrient", nutrient))
	wisdom_fruit = int(data.get("wisdom_fruit", wisdom_fruit))
	trickster_vine = int(data.get("trickster_vine", trickster_vine))
	power = float(data.get("power", power))


func _broadcast_all() -> void:
	Events.resource_changed.emit("water", float(water))
	Events.resource_changed.emit("nutrient", float(nutrient))
	Events.resource_changed.emit("wisdom_fruit", float(wisdom_fruit))
	Events.resource_changed.emit("trickster_vine", float(trickster_vine))
	Events.resource_changed.emit("power", power)
