import datetime
import uuid
from typing import Any, Dict, List, Optional, Union

import cairne.commands.generated as generated_commands
import cairne.commands.worlds as world_commands
import cairne.model.specification as spec
import cairne.schema.generated as generated_schema
import cairne.schema.worlds as worlds_schema
from cairne.serve.data_store import Datastore
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_pydantic import validate
from structlog import get_logger


# Story idea: the last human


logger = get_logger(__name__)


app = Flask(__name__)
cors = CORS(app)


sessions: Dict[str, str] = {}
datastore: Datastore = Datastore.load()


##############################################################
# LIST
##############################################################


@app.route("/worlds", methods=["GET", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def list_worlds(*args, **kwargs) -> generated_schema.ListEntitiesResponse:
	logger.info("List worlds", args=args, kwargs=kwargs)
	command = world_commands.ListWorlds(datastore=datastore, user="test")
	response = command.execute()
	return response


@app.route("/world/<world_id>/entities/<entity_type>", methods=["GET", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
# Can the entity_type be a EntityType?
def list_entities(
	world_id: uuid.UUID, entity_type: str
) -> generated_schema.ListEntitiesResponse:
	logger.info("List entities", world_id=world_id, entity_type=entity_type)
	request = generated_schema.ListEntitiesRequest.model_validate(
		dict(world_id=world_id, entity_type=entity_type)
	)
	command = generated_commands.ListEntities(
		datastore=datastore, user="test", request=request
	)
	response = command.execute()
	return response


##############################################################
# GET
##############################################################


@app.route("/world/<world_id>", methods=["GET", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def get_world(world_id: uuid.UUID) -> generated_schema.GetEntityResponse:
	logger.info("Get world", world_id=world_id)
	command = world_commands.GetWorld(
		datastore=datastore, user="test", world_id=world_id
	)
	response = command.execute()
	return response


@app.route("/world/<world_id>/entity/<entity_id>", methods=["GET", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def get_entity(
	world_id: uuid.UUID, entity_id: uuid.UUID
) -> generated_schema.GetEntityResponse:
	logger.info("Get entity", world_id=world_id, entity_id=entity_id)
	command = generated_commands.GetEntity(
		datastore=datastore, user="test", world_id=world_id, entity_id=entity_id
	)
	response = command.execute()
	return response


##############################################################
# CREATE
##############################################################


@app.route("/world", methods=["POST", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def create_world(
	body: worlds_schema.CreateWorldRequest,
) -> generated_schema.CreateEntityResponse:
	logger.info("Create world", request=body)
	command = world_commands.CreateWorld(datastore=datastore, user="test", request=body)
	response = command.execute()
	return response


@app.route("/world/<world_id>/entities/<entity_type>", methods=["POST", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def create_entity(
	world_id: uuid.UUID,
	entity_type: str,
	body: generated_schema.CreateEntityRequest,
) -> generated_schema.CreateEntityResponse:
	logger.info(
		"Create entity", world_id=world_id, entity_type=entity_type, request=body
	)
	request = generated_schema.CreateEntityRequest.model_validate(
		dict(world_id=world_id, entity_type=entity_type, name=body.name)
	)
	assert body.entity_type == entity_type
	assert body.world_id == world_id
	command = generated_commands.CreateEntity(
		datastore=datastore, user="test", request=request
	)
	response = command.execute()
	return response


##############################################################
# DELETE
##############################################################


@app.route("/world/<world_id>/entity/<entity_id>", methods=["DELETE", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def delete_entity(
	world_id: uuid.UUID,
	entity_id: uuid.UUID,
) -> generated_schema.DeleteEntityResponse:
	logger.info("Delete entity", world_id=world_id, entity_id=entity_id)
	request = generated_schema.DeleteEntityRequest.model_validate(
		dict(world_id=world_id, entity_id=entity_id)
	)
	command = generated_commands.DeleteEntity(
		datastore=datastore, user="test", request=request
	)
	response = command.execute()
	return response


@app.route("/world/<world_id>", methods=["DELETE", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def delete_world(world_id: uuid.UUID) -> generated_schema.DeleteEntityResponse:
	logger.info("Delete world", world_id=world_id)
	command = world_commands.DeleteWorld(
		datastore=datastore, user="test", world_id=world_id
	)
	response = command.execute()
	return response


##############################################################


# @app.route('/world/<world_id>/characters/<character_id>', methods=['GET', 'OPTIONS'])
# @cross_origin(origins=['*'])
# @validate()
# def get_character(
#     world_id: str,
#     character_id: str,
#     # query: characters_schema.GetCharacterRequest
# ) -> characters_schema.GetCharacterResponse:
#     request = characters_schema.GetCharacterRequest.model_validate(dict(world_id=world_id, character_id=character_id))
#     logger.info("Get character", query=request)
#     command = character_commands.GetCharacter(datastore=datastore, user="test", request=request)
#     response = command.execute()
#     return response


# @app.route('/world/<world_id>/characters', methods=['POST', 'OPTIONS'])
# # @app.route('/characters', methods=['POST', 'OPTIONS'])
# @cross_origin(origins=['*'])
# @validate()
# def create_character(
#     world_id: str,
#     body: characters_schema.CreateCharacterRequest,
# ) -> characters_schema.CreateCharacterResponse:
#     logger.info("Create character", world_id=world_id, request=body)

#     # if world_id != body.world_id:
#     #     # Ha ha
#     #     raise ValueError(f"World ID mismatch: {world_id} != {body.world_id}")

#     command = character_commands.CreateCharacter(datastore=datastore, user="test", request=body)
#     response = command.execute()
#     return response


# @app.route('/world/<world_id>/characters/<character_id>', methods=['DELETE', 'OPTIONS'])
# @cross_origin(origins=['*'])
# @validate()
# def delete_character(
#     world_id: str,
#     character_id: str,
#     # query: characters_schema.DeleteCharacterRequest
# ) -> characters_schema.DeleteCharacterResponse:
#     request = characters_schema.DeleteCharacterRequest.model_validate(dict(world_id=world_id, character_id=character_id))
#     logger.info("Delete character", request=request)
#     command = character_commands.DeleteCharacter(
#         datastore=datastore, user="test", request=request
#     )
#     response = command.execute()
#     return response


def serve():
	app.run(debug=True)
