extends Node

const HAZARD_ID := "solar_flare"
const INITIAL_DELAY := 30.0
const WARNING_DURATION := 5.0
const ACTIVE_DURATION := 8.0
const COOLDOWN_DURATION := 45.0

func _ready() -> void:
	add_to_group("solar_flare_controller")
	if GameState.solar_flare_phase not in ["calm", "warning", "active"]:
		GameState.reset_transient_hazards()
	if GameState.solar_flare_time_remaining <= 0.0:
		_advance_phase()
	else:
		_emit_state()

func _process(delta: float) -> void:
	GameState.solar_flare_time_remaining = maxf(0.0, GameState.solar_flare_time_remaining - delta)
	if GameState.solar_flare_time_remaining <= 0.0:
		_advance_phase()

func _advance_phase() -> void:
	match GameState.solar_flare_phase:
		"calm":
			_enter_warning()
		"warning":
			_enter_active()
		"active":
			_enter_calm()
		_:
			GameState.reset_transient_hazards()
			_emit_state()

func _enter_warning() -> void:
	GameState.solar_flare_phase = "warning"
	GameState.solar_flare_time_remaining = WARNING_DURATION
	Events.station_message.emit("Solar flare warning - impact in 5 seconds.")
	_emit_state()

func _enter_active() -> void:
	GameState.solar_flare_phase = "active"
	GameState.solar_flare_time_remaining = ACTIVE_DURATION
	Events.station_message.emit("Solar flare active - power drain accelerating.")
	_emit_state()

func _enter_calm() -> void:
	GameState.solar_flare_phase = "calm"
	GameState.solar_flare_time_remaining = COOLDOWN_DURATION
	Events.station_message.emit("Solar flare passed. Station load normalizing.")
	_emit_state()

func _emit_state() -> void:
	Events.hazard_state_changed.emit(
		HAZARD_ID,
		GameState.solar_flare_phase,
		GameState.solar_flare_time_remaining
	)
