import datetime
import uuid
from typing import Any, Dict, List, Optional, Union

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_pydantic import validate
from structlog import get_logger

import cairne.model.generation as generate_model
import cairne.model.templates as template_model
import cairne.schema.edits as edits_schema
import cairne.schema.generated as generated_schema
import cairne.schema.generate as generate_schema
import cairne.schema.worlds as worlds_schema
import cairne.commands.edits as edits_commands
import cairne.commands.generate.base as base_generate_commands
import cairne.commands.generated as generated_commands
import cairne.commands.generation as generate_commands
import cairne.schema.templates as template_schema
import cairne.commands.templates as template_commands
import cairne.commands.worlds as world_commands


from cairne.serve.data_store import Datastore

# Story idea: the last human as ais take over
# add editor settings (like include field in generation)
# add a sort index to the lists
# add options for generated values
# TODO: maybe add a date to the generation name for a generation template


logger = get_logger(__name__)


app = Flask(__name__)
cors = CORS(app)


sessions: Dict[str, str] = {}
Datastore.model_rebuild()
datastore: Datastore = Datastore.load()


##############################################################
# Worlds
##############################################################



@app.route("/worlds", methods=["GET", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def list_worlds(*args, **kwargs) -> generated_schema.ListEntitiesResponse:
    logger.info("List worlds", args=args, kwargs=kwargs)
    command = world_commands.ListWorlds(datastore=datastore, user="test")
    response = command.execute()
    return response


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
# Entities
##############################################################

# Do we need to have the world id in the url?
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


@app.route("/world/<world_id>/entity/<entity_id>", methods=["GET", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def get_entity(
    world_id: uuid.UUID,
    entity_id: uuid.UUID,
    query: generated_schema.GetEntityQuery,
) -> generated_schema.GetEntityResponse:
    logger.info("Get entity", word_id=world_id, entity_id=entity_id, query=query)
    entity_request = generated_schema.GetEntityRequest.from_query(
        world_id=world_id,
        entity_id=entity_id,
        query=query,
    )
    command = generated_commands.GetEntity(
        datastore=datastore, user="test", request=entity_request
    )
    response = command.execute()
    return response


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

##############################################################
# Templates
##############################################################


@app.route("/templates", methods=["GET", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def list_templates(
    query: template_schema.ListTemplatesQuery,
) -> template_schema.ListTemplatesResponse:
    logger.info("List templates", query=query)
    command = template_commands.ListTemplates(datastore=datastore, user="test", request=query)
    response = command.execute()
    return response


@app.route("/template/<template_id>", methods=["GET", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def get_template(
    template_id: uuid.UUID,
) -> template_schema.GetTemplateResponse:
    logger.info("Get template", template_id=template_id)
    command = template_commands.GetTemplate(datastore=datastore, user="test", template_id=template_id)
    response = command.execute()
    return response


@app.route("/templates", methods=["POST", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def create_template(
    body: template_schema.CreateTemplateRequest,
) -> template_schema.CreateTemplateResponse:
    logger.info("Create template", body=body)
    command = template_commands.CreateTemplate(datastore=datastore, user="test", request=body)
    response = command.execute()
    return response


@app.route("/template/<template_id>", methods=["POST", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def update_template(
    template_id: uuid.UUID,
    body: template_schema.UpdateTemplateRequest,
) -> template_schema.UpdateTemplateResponse:
    logger.info("Update template", template_id=template_id, body=body)
    assert body.template_id == template_id
    command = template_commands.UpdateTemplate(datastore=datastore, user="test", request=body)
    response = command.execute()
    return response


@app.route("/template/<template_id>", methods=["DELETE", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def delete_template(
    template_id: uuid.UUID,
) -> template_schema.DeleteTemplateResponse:
    logger.info("Delete template", template_id=template_id)
    command = template_commands.DeleteTemplate(datastore=datastore, user="test", template_id=template_id)
    response = command.execute()
    return response


@app.route("/templates/generators", methods=["GET", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def list_generator_types() -> generate_schema.ListGenerationModels:
    logger.info("List generator types")
    response = generate_schema.ListGenerationModels()
    return response




##############################################################
# Generation
##############################################################


@app.route("/generations", methods=["GET", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def list_generations(
    query: generate_schema.ListGenerationsQuery,
) -> generate_schema.ListGenerationsResponse:
    logger.info("List generations", query=query)
    command = generate_commands.ListGenerations(datastore=datastore, user="test", request=query)
    response = command.execute()
    return response


@app.route("/generation/<generation_id>", methods=["GET", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def get_generation(
    generation_id: uuid.UUID,
) -> generate_schema.GetGenerationResponse:
    logger.info("Get generation", generation_id=generation_id)
    command = generate_commands.GetGeneration(
        datastore=datastore, user="test", generation_id=generation_id
    )
    response = command.execute()
    return response


# Descriptive path?
@app.route("/generate", methods=["POST", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def generate(body: generate_schema.GenerateRequest) -> generate_schema.GenerateResponse:
    logger.info("Generate", body=body)
    
    template = datastore.generation_templates.get(body.template_id, None)
    if template is None:
        raise ValueError(f"Template {body.template_id} not found")
    world = datastore.worlds.get(template.world_id, None)
    if world is None:
        raise ValueError(f"World {template.world_id} not found") 
    template = template.for_entity(body.target_entity_id)
    generation = generate_model.Generation.create(template, world)
    command_class = base_generate_commands.get_command_class(generation=generation)
    command = command_class(datastore=datastore, user="test", generation=generation)
    command.generation = generation
    response = command.execute()
    return response


@app.route("/generation/<generation_id>", methods=["DELETE", "OPTIONS"])
@cross_origin(origins=["*"])
@validate()
def delete_generation(
    generation_id: uuid.UUID,
) -> generate_schema.DeleteGenerationResponse:
    logger.info("Delete generation", generation_id=generation_id)
    command = generate_commands.DeleteGeneration(datastore=datastore, user="test", generation_id=generation_id)
    response = command.execute()
    return response


##############################################################
# Edits
##############################################################


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


##############################################################
# Other
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


def serve():
    app.run(debug=True)
