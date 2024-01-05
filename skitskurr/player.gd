extends Node2D


var target_position: Vector2 = Vector2()
var move_speed: float = 0.1
var player_id: int = -1

# TODO: break this into two things / location change vs velocity changed
signal player_movement_changed(player_id: int, position: Vector2, velocity: Vector2)


func _ready():
	pass # Replace with function body.


func _physics_process(delta):
	# TODO: find the right node type
	# TODO: use path queries...
	var d_position = target_position - self.global_position
	var distance = d_position.length()
	if distance < 1e-8:
		return
	var direction = d_position.normalized()
	if move_speed > distance:
		self.global_position = target_position
		player_movement_changed.emit(player_id, target_position, Vector2())
		print("Player stopped")
		# no need to signal if we already there...
	else:
		var velocity = move_speed * direction
		global_translate(delta * velocity)
		# Really only have to send the velocity...
		# This should have a time as well...
		# Check that the global position is already updated...
		player_movement_changed.emit(player_id, global_position, velocity)
		print("Player moving", velocity)
