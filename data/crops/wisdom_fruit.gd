# wisdom_fruit.gd
# CropDefinition Resource plus the default Wisdom Fruit data.
class_name CropDefinition
extends Resource

## Stable ID used by save data and scripted crop behavior.
var crop_id: String = "wisdom_fruit"

## Human-readable name shown in prompts and logs.
var crop_name: String = "Wisdom Fruit"

## Resource key awarded by FarmingManager on harvest.
var harvest_resource: String = "wisdom_fruit"

## Time in seconds for the crop to grow from PLANTED to READY.
var growth_time: float = 30.0

## Fraction of remaining growth_timer removed when tending (0.2 = 20% faster).
var tend_bonus: float = 0.2

## Resources spent at planting time.
var water_cost: int = 1
var nutrient_cost: int = 1

## Number of harvest items produced per harvest.
var harvest_yield: int = 1

## Optional behavior key used by CropPlot for small crop-specific rules.
var behavior: String = "standard"
