extends Node

const BASE_POWER_DRAIN_PER_SECOND := 0.333

var water: int:
	get: return GameState.water
	set(value): GameState.water = clampi(value, 0, GameState.water_cap())
var nutrient: int:
	get: return GameState.nutrient
	set(value): GameState.nutrient = clampi(value, 0, GameState.nutrient_cap())
var wisdom_fruit: int:
	get: return GameState.wisdom_fruit
	set(value): GameState.wisdom_fruit = maxi(0, value)
var chaos: int:
	get: return GameState.chaos
	set(value): GameState.chaos = maxi(0, value)
var power: float:
	get: return GameState.power
	set(value): GameState.power = clampf(value, 0.0, 100.0)

func _ready() -> void:
	add_to_group("farming_manager")
	_broadcast_all()

func _process(delta: float) -> void:
	if power <= 0.0:
		return
	power -= BASE_POWER_DRAIN_PER_SECOND * GameState.power_drain_multiplier() * GameState.hazard_power_drain_multiplier() * delta
	Events.resource_changed.emit("power", power)

func can_plant(water_cost: int, nutrient_cost: int) -> bool:
	return water >= water_cost and nutrient >= nutrient_cost

func spend_water(amount: int) -> void:
	water -= amount
	_commit_resource("water", float(water))

func spend_nutrient(amount: int) -> void:
	nutrient -= amount
	_commit_resource("nutrient", float(nutrient))

func add_wisdom_fruit(amount: int) -> void:
	wisdom_fruit += amount
	_commit_resource("wisdom_fruit", float(wisdom_fruit))

func add_chaos(amount: int) -> void:
	chaos += amount
	_commit_resource("chaos", float(chaos))

func spend_chaos(amount: int) -> bool:
	if chaos < amount:
		return false
	chaos -= amount
	_commit_resource("chaos", float(chaos))
	return true

func add_crop_yield(resource_id: String, amount: int) -> bool:
	match resource_id:
		"wisdom_fruit":
			add_wisdom_fruit(amount)
		"chaos":
			add_chaos(amount)
		_:
			push_error("Unknown crop harvest resource: %s" % resource_id)
			return false
	return true

func spend_wisdom_fruit(amount: int) -> bool:
	if wisdom_fruit < amount:
		return false
	wisdom_fruit -= amount
	_commit_resource("wisdom_fruit", float(wisdom_fruit))
	return true

func restore_power() -> void:
	var cost := 1 if power < 50.0 else 0
	if cost > 0 and not spend_wisdom_fruit(cost):
		Events.station_message.emit("Repair requires 1 Wisdom Fruit.")
		return
	power = 100.0
	_commit_resource("power", power)

func can_replenish() -> bool:
	return GameState.emergency_resupplies > 0 or wisdom_fruit >= 1 or GameState.has_upgrade("closed_loop_hydroponics")

func replenish_consumables() -> bool:
	if GameState.has_upgrade("closed_loop_hydroponics"):
		pass
	elif GameState.emergency_resupplies > 0:
		GameState.emergency_resupplies -= 1
	elif not spend_wisdom_fruit(1):
		Events.station_message.emit("Resupply requires 1 Wisdom Fruit.")
		return false
	water = GameState.water_cap()
	nutrient = GameState.nutrient_cap()
	_commit_resource("water", float(water), false)
	_commit_resource("nutrient", float(nutrient), false)
	GameState.save_game()
	return true

func replenish_prompt() -> String:
	if GameState.has_upgrade("closed_loop_hydroponics"):
		return "E - Replenish Water & Nutrients (closed loop)"
	if GameState.emergency_resupplies > 0:
		return "E - Emergency Resupply (%d remaining)" % GameState.emergency_resupplies
	return "E - Resupply Water & Nutrients (1 Wisdom Fruit)"

func _commit_resource(resource_name: String, value: float, save := true) -> void:
	Events.resource_changed.emit(resource_name, value)
	if save:
		GameState.save_game()

func _broadcast_all() -> void:
	Events.resource_changed.emit("water", float(water))
	Events.resource_changed.emit("nutrient", float(nutrient))
	Events.resource_changed.emit("wisdom_fruit", float(wisdom_fruit))
	Events.resource_changed.emit("chaos", float(chaos))
	Events.resource_changed.emit("power", power)
