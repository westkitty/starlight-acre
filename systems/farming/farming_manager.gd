# farming_manager.gd
# Owns all session resource state and the passive power drain.
# Lives as a child Node of GreenhouseSector (not an autoload).
# Added to group "farming_manager" so interactables can find it without direct wiring.
extends Node

const WATER_MAX := 10
const NUTRIENT_MAX := 10
const POWER_DRAIN_PER_SECOND := 0.333  # ~1% per 3 seconds

var water: int = 5
var nutrient: int = 5
var wisdom_fruit: int = 0
var power: float = 100.0


func _ready() -> void:
	add_to_group("farming_manager")
	_broadcast_all()


func _process(delta: float) -> void:
	power = maxf(0.0, power - POWER_DRAIN_PER_SECOND * delta)
	Events.resource_changed.emit("power", power)


# --- Read ---

func can_plant(water_cost: int, nutrient_cost: int) -> bool:
	return water >= water_cost and nutrient >= nutrient_cost


# --- Write ---

func spend_water(amount: int) -> void:
	water = maxi(0, water - amount)
	Events.resource_changed.emit("water", float(water))


func spend_nutrient(amount: int) -> void:
	nutrient = maxi(0, nutrient - amount)
	Events.resource_changed.emit("nutrient", float(nutrient))


func add_wisdom_fruit(amount: int) -> void:
	wisdom_fruit += amount
	Events.resource_changed.emit("wisdom_fruit", float(wisdom_fruit))


func restore_power() -> void:
	power = 100.0
	Events.resource_changed.emit("power", power)


func replenish_consumables() -> void:
	water = WATER_MAX
	nutrient = NUTRIENT_MAX
	Events.resource_changed.emit("water", float(water))
	Events.resource_changed.emit("nutrient", float(nutrient))


func _broadcast_all() -> void:
	Events.resource_changed.emit("water", float(water))
	Events.resource_changed.emit("nutrient", float(nutrient))
	Events.resource_changed.emit("wisdom_fruit", float(wisdom_fruit))
	Events.resource_changed.emit("power", power)
