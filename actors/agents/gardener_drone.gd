# gardener_drone.gd
# Patrols the greenhouse horizontally and periodically tends/harvests crop plots.
# Finds plots via get_tree().get_nodes_in_group("crop_plots").
# Only acts on GROWING (tend) and READY (harvest) states.
class_name GardenerDrone
extends Node2D

const SCAN_INTERVAL := 5.0
const PATROL_SPEED := 80.0
const PATROL_HALF_RANGE := 300.0

var _scan_timer: float = SCAN_INTERVAL
var _patrol_direction: float = 1.0
var _patrol_origin_x: float = 0.0


func _ready() -> void:
	_patrol_origin_x = global_position.x


func _process(delta: float) -> void:
	_patrol(delta)
	_scan_timer -= delta
	if _scan_timer <= 0.0:
		_scan_timer = SCAN_INTERVAL
		_act_on_crops()


func _patrol(delta: float) -> void:
	position.x += PATROL_SPEED * _patrol_direction * delta
	if absf(global_position.x - _patrol_origin_x) >= PATROL_HALF_RANGE:
		_patrol_direction *= -1.0


func _act_on_crops() -> void:
	for plot in get_tree().get_nodes_in_group("crop_plots"):
		var state: CropPlot.State = plot.get_state()
		if state == CropPlot.State.GROWING or state == CropPlot.State.READY:
			plot.interact()
