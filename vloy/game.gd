extends Node2D


var peer = ENetMultiplayerPeer.new()

@onready var player = $Player


# These could just be the global position and scale?
var WORLD_POSITION_TOP_LEFT: Vector2 = Vector2(0.0, 0.0)
var SCALE: float = 1.0


func _ready():
	peer.create_client("127.0.0.1", 5031)
	multiplayer.multiplayer_peer = peer
	
	multiplayer.connected_to_server.connect(_on_connected_ok)
	multiplayer.connection_failed.connect(_on_connected_fail)
	multiplayer.server_disconnected.connect(_on_server_disconnected)


func _process(delta):
	pass


func _unhandled_input(event):
   # Mouse in viewport coordinates.
	if event is InputEventMouseButton and event.pressed:
		match event.button_index:
			MOUSE_BUTTON_LEFT:
				pass
			MOUSE_BUTTON_RIGHT:
				handle_right_click(event.position)
   # Print the size of the viewport.


func map_position_to_world(position: Vector2) -> Vector2:
	var size = get_viewport().get_visible_rect().size
	return WORLD_POSITION_TOP_LEFT + position / size * SCALE;
	
func map_position_to_screen(position: Vector2) -> Vector2:
	var size = get_viewport().get_visible_rect().size
	return (position - WORLD_POSITION_TOP_LEFT) / SCALE * size;

func map_velocity_to_screen(velocity: Vector2) -> Vector2:
	var size = get_viewport().get_visible_rect().size
	return velocity / SCALE * size;


func handle_right_click(position: Vector2):
	var world_coord = map_position_to_world(position)
	print("World coord", world_coord)
	request_move.rpc(world_coord)


func _on_connected_ok():
	var peer_id = multiplayer.get_unique_id()
	print("Connected to server ", peer_id)


func _on_connected_fail():
	multiplayer.multiplayer_peer = null


func _on_server_disconnected():
	multiplayer.multiplayer_peer = null


@rpc("authority", "call_remote", "reliable", 0)
func request_move(position: Vector2):
	pass

# How do we ensure that a client can never call this?
@rpc("authority", "call_local", "unreliable", 0)
func movement_updated(entity_id: int, position: Vector2, velocity: Vector2):
	# TODO: check if the entity_id is us!
	if velocity.length() < 1e-4:
		player.global_position = map_position_to_screen(position)
	player.velocity = map_velocity_to_screen(velocity)
