class_name GardenerDrone
extends Node2D

@export var move_speed := 90.0
@export var interaction_radius := 28.0
@export var auto_tend := true
@export var auto_harvest := true

var _target: CropPlot = null

func _process(delta: float) -> void:
	if not is_instance_valid(_target) or not _target_is_actionable():
		_target = _choose_target()
	if _target == null:
		return
	var dx := _target.global_position.x - global_position.x
	if absf(dx) > interaction_radius:
		position.x += signf(dx) * move_speed * delta
		return
	_target.drone_interact()
	_target = null

func _target_is_actionable() -> bool:
	if _target == null:
		return false
	return (auto_harvest and _target.can_drone_harvest()) or (auto_tend and _target.can_drone_tend())

func _choose_target() -> CropPlot:
	var best: CropPlot = null
	var best_distance := INF
	for node in get_tree().get_nodes_in_group("crop_plots"):
		var plot := node as CropPlot
		if plot == null:
			continue
		var actionable := (auto_harvest and plot.can_drone_harvest()) or (auto_tend and plot.can_drone_tend())
		if not actionable:
			continue
		var distance := absf(plot.global_position.x - global_position.x)
		if distance < best_distance:
			best = plot
			best_distance = distance
	return best
