# player.gd
# CharacterBody2D — handles movement, jumping, and interactable registration.
# Interactables (CropPlot, terminals) call register/unregister_interactable()
# when the player enters or exits their Area2D.
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


func _physics_process(delta: float) -> void:
	# Apply gravity when airborne.
	if not is_on_floor():
		velocity.y += GRAVITY * delta

	# Coyote time: allows jumping briefly after walking off a ledge.
	if is_on_floor():
		_coyote_timer = COYOTE_DURATION
	else:
		_coyote_timer -= delta

	# Jump buffer: queues a jump if Space is pressed slightly before landing.
	if Input.is_action_just_pressed("jump"):
		_jump_buffer_timer = JUMP_BUFFER_DURATION
	else:
		_jump_buffer_timer -= delta

	# Execute jump when buffer is active and coyote window is open.
	if _jump_buffer_timer > 0.0 and _coyote_timer > 0.0:
		velocity.y = JUMP_VELOCITY
		_coyote_timer = 0.0
		_jump_buffer_timer = 0.0

	# Horizontal movement.
	velocity.x = Input.get_axis("move_left", "move_right") * SPEED

	move_and_slide()

	# Tick land timer.
	if _land_timer > 0.0:
		_land_timer -= delta

	_update_animation()
	_was_on_floor = is_on_floor()


func _update_animation() -> void:
	# Detect landing transition (air → ground).
	if not _was_on_floor and is_on_floor():
		_sprite.play("land")
		_land_timer = 0.2
		return

	# Hold land animation while timer is active.
	if _land_timer > 0.0:
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
		_land_timer = 0.25  # 2 frames at 8fps


## Called by an interactable's Area2D body_entered signal.
## Sets this as the active interactable and updates the interaction prompt.
func register_interactable(node: Node) -> void:
	_current_interactable = node
	Events.interaction_prompt_changed.emit(node.get_prompt())


## Called by an interactable's Area2D body_exited signal.
## Clears the active interactable only if it is the one that just exited.
func unregister_interactable(node: Node) -> void:
	if _current_interactable == node:
		_current_interactable = null
		Events.interaction_prompt_changed.emit("")
