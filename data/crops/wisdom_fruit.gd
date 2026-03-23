# wisdom_fruit.gd
# CropDefinition Resource — defines all data for a crop type.
# Phase 1: this file IS the CropDefinition class AND the Wisdom Fruit data.
# Phase 2: split into CropDefinition base class + separate .tres resource files per crop.
class_name CropDefinition
extends Resource

## Human-readable name shown in HUD and logs.
var crop_name: String = "Wisdom Fruit"

## Time in seconds for the crop to grow from PLANTED to READY.
var growth_time: float = 30.0

## Fraction of remaining growth_timer removed when tending (0.2 = 20% faster).
var tend_bonus: float = 0.2

## Resources spent at planting time.
var water_cost: int = 1
var nutrient_cost: int = 1

## Number of harvest items produced per harvest.
var harvest_yield: int = 1
