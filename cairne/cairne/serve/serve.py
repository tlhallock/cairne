import datetime
import uuid
from typing import Any, Dict, List, Optional, Union

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_pydantic import validate
from structlog import get_logger

import cairne.commands.edits as edits_commands
import cairne.commands.generate.base as base_generate_commands
import cairne.commands.generate.openai.generate as openai_generate
import cairne.commands.generated as generated_commands
import cairne.commands.generation as generate_commands
import cairne.commands.worlds as world_commands
import cairne.model.generation as generate_model
import cairne.model.specification as spec
import cairne.schema.edits as edits_schema
import cairne.schema.generate as generate_schema
import cairne.schema.generated as generated_schema
import cairne.schema.worlds as worlds_schema
from cairne.serve.data_store import Datastore

# Story idea: the last human as ais take over
# add editor settings (like include field in generation)
# add a sort index to the lists
# add options for generated values


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


@app.route("/entity_types", methods=["GET", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def list_entity_types() -> worlds_schema.ListEntityTypesResponse:
    logger.info("List entity types")
    command = world_commands.ListEntityTypes(datastore=datastore, user="test")
    response = command.execute()
    return response


# @app.route("/schema/entity/<entity_type>", methods=["GET", "OPTIONS"])
# @cross_origin(origins=["*"])
# @validate()
# def get_generation_schema(entity_type: str) -> generated_schema.GetEntitySchemaResponse:
#     logger.info("Get entity schema", entity_type=entity_type)
#     validated_entity_type = spec.EntityType.get(entity_type)
#     command = generate_commands.GetEntitySchema(
#         datastore=datastore, user="test", entity_type=validated_entity_type
#     )
#     response = command.execute()
#     return response


def create_generate_command(
    datastore: Datastore, user: str, request: generate_schema.GenerateRequest
) -> base_generate_commands.BaseGenerate:
    generation_builder = base_generate_commands.GenerationBuilder(
        request=request, user=user, datastore=datastore
    )
    generation = generation_builder.create_generation()
    if generation.generator_model.generator_type == generate_model.GeneratorType.OPENAI:
        return openai_generate.OpenAIGenerate(
            datastore=datastore,
            user=user,
            request=request,
            generation=generation,
            world=generation_builder.get_world(),
            entity=generation_builder.get_entity(),
            specification=generation_builder.get_specification(),
        )
    else:
        raise NotImplementedError(
            f"Unknown or not implemented generator type {generation.generator_model.generator_type}"
        )


# Descriptive path?
@app.route("/generate", methods=["POST", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def generate(body: generate_schema.GenerateRequest) -> generate_schema.GenerateResponse:
    logger.info("Generate", body=body)
    command = create_generate_command(datastore=datastore, user="test", request=body)
    response = command.execute()
    return response


# Descriptive paths?
@app.route("/world/<world_id>/update", methods=["POST", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def replace_value(
    world_id: uuid.UUID, body: edits_schema.ReplaceRequest
) -> edits_schema.ReplaceResponse:
    logger.info("Replace value", world_id=world_id, body=body)
    command = edits_commands.ReplaceValue(
        datastore=datastore, user="test", request=body
    )
    response = command.execute()
    return response


@app.route("/world/<world_id>/append", methods=["POST", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def append_value(
    world_id: uuid.UUID, body: edits_schema.AppendElementRequest
) -> edits_schema.AppendElementResponse:
    logger.info("Append value", world_id=world_id, body=body)
    command = edits_commands.AppendValue(datastore=datastore, user="test", request=body)
    response = command.execute()
    return response


@app.route("/world/<world_id>/clear", methods=["POST", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def remove_value(
    world_id: uuid.UUID, body: edits_schema.RemoveValueRequest
) -> edits_schema.RemoveValueResponse:
    logger.info("Remove value", world_id=world_id, body=body)
    command = edits_commands.RemoveValue(datastore=datastore, user="test", request=body)
    response = command.execute()
    return response


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
