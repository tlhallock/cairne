extends Node

var peer = ENetMultiplayerPeer.new()

var player_nodes: Dictionary = {}


func _ready():
	peer.create_server(5031, 10)
	multiplayer.multiplayer_peer = peer
	
	multiplayer.peer_connected.connect(_on_player_connected)
	multiplayer.peer_disconnected.connect(_on_player_disconnected)
	print("Listening")


func _process(delta):
	pass


func _on_player_connected(player_id: int):
	var scene = preload("res://player.tscn")
	var instance = scene.instantiate()
	player_nodes[player_id] = instance
	instance.player_movement_changed.connect(on_entity_movement_updated)
	add_child(instance)
	print("Player connected ", player_id)

func _on_player_disconnected(player_id: int):
	var instance = player_nodes[player_id]
	if instance != null:
		instance.queue_free()
	player_nodes.erase(player_id)
	# do we need to disconnect the signal?
	print("Player disconnected ", player_id)


func on_entity_movement_updated(entity_id: int, position: Vector2, velocity: Vector2):
	# TODO: only send to listeners...
	movement_updated.rpc(entity_id, position, velocity)


@rpc("any_peer", "call_local", "reliable", 0)
func request_move(position: Vector2):
	var player_id = multiplayer.get_remote_sender_id()
	var instance = player_nodes[player_id]
	if instance == null:
		print("Requested move but no player node.")
	#var player_node := instance as PlayerNode
	instance.target_position = position
	print("Move Requested: player_id=%s destination=%s" % [player_id, position])


# How do we ensure that a client can never call this?
@rpc("authority", "call_remote", "unreliable", 0)
func movement_updated(entity_id: int, position: Vector2, velocity: Vector2):
	pass
