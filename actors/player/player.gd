# player.gd
# CharacterBody2D - movement, jumping, animation, and interactable registration.
extends CharacterBody2D

const SPEED := 200.0
const JUMP_VELOCITY := -420.0
const GRAVITY := 980.0
const COYOTE_DURATION := 0.1
const JUMP_BUFFER_DURATION := 0.1

var _coyote_timer := 0.0
var _jump_buffer_timer := 0.0
var _current_interactable: Node = null
var _was_on_floor := true
var _land_timer := 0.0

@onready var _sprite: AnimatedSprite2D = $Visual


func _ready() -> void:
	call_deferred("_apply_spawn_state")


func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity.y += GRAVITY * delta

	if is_on_floor():
		_coyote_timer = COYOTE_DURATION
	else:
		_coyote_timer -= delta

	if Input.is_action_just_pressed("jump"):
		_jump_buffer_timer = JUMP_BUFFER_DURATION
	else:
		_jump_buffer_timer -= delta

	if _jump_buffer_timer > 0.0 and _coyote_timer > 0.0:
		velocity.y = JUMP_VELOCITY
		_coyote_timer = 0.0
		_jump_buffer_timer = 0.0

	velocity.x = Input.get_axis("move_left", "move_right") * SPEED

	move_and_slide()

	if _land_timer > 0.0:
		_land_timer -= delta

	_update_animation()
	_was_on_floor = is_on_floor()


func _update_animation() -> void:
	if _land_timer > 0.0:
		return

	if not _was_on_floor and is_on_floor():
		_sprite.play("land")
		_land_timer = 0.2
		return

	if not is_on_floor():
		if velocity.y < 0:
			_sprite.play("jump")
		else:
			_sprite.play("fall")
	elif absf(velocity.x) > 10.0:
		_sprite.play("walk")
	else:
		_sprite.play("idle")

	if velocity.x < -10.0:
		_sprite.flip_h = true
	elif velocity.x > 10.0:
		_sprite.flip_h = false


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("interact") and _current_interactable != null:
		_current_interactable.interact()
		_sprite.play("interact")
		_land_timer = 0.25


func register_interactable(node: Node) -> void:
	_current_interactable = node
	Events.interaction_prompt_changed.emit(node.get_prompt())


func unregister_interactable(node: Node) -> void:
	if _current_interactable == node:
		_current_interactable = null
		Events.interaction_prompt_changed.emit("")


func _apply_spawn_state() -> void:
	if GameState.has_pending_load():
		global_position = GameState.get_pending_player_position(global_position)
		return

	var current_scene := get_tree().current_scene
	if current_scene == null:
		return
	var spawn := current_scene.find_child(GameState.target_spawn_name, true, false)
	if spawn is Node2D:
		global_position = spawn.global_position
