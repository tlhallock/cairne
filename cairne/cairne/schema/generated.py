import datetime
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

import cairne.model.generated as generated
import cairne.model.generated as generated_model
import cairne.model.generation as generation_model
import cairne.model.specification as spec
import cairne.schema.edits as edits_schema
import cairne.schema.worlds as worlds_schema
from cairne.schema.base import Response


class GeneratedValueEditor(str, Enum):
    G_STRING = "string"
    # Somehow, we need to know if this string is expected to be long.
    #     - That information could also be used to calculate the expected number of tokens within a generation?
    G_TEXT = "text"
    G_FLOAT = "float"
    G_INTEGER = "integer"
    G_BOOLEAN = "boolean"
    G_OBJECT = "object"
    G_LIST = "list"
    G_ENTITIES = "entities_dictionary"


class GenerationHistory(BaseModel):
    pass


class GeneratedFieldChoice(BaseModel):
    label: str = Field()
    value: str = Field()


class NumberToGenerate(BaseModel):
    any: bool = Field(default=False)
    number_to_generate: int = Field()


class GeneratedField(BaseModel):
    label: str = Field()
    raw_value: str = Field()
    value_js: str = Field()
    edit_path: spec.GeneratablePath = Field()
    generated_value_js: Optional[str] = Field(default=None)
    
    validation_errors: List[str] = Field(default_factory=list)
    
    # For object fields:
    generate: Optional[bool] = Field(default=None)
    
    # TODO: remove
    edit_path_key: str = Field()
    # TODO: These should be from the editor specification...
    value_type: GeneratedValueEditor = Field()
    
    # For values
    choices: Optional[List[GeneratedFieldChoice]] = Field(default=None)
    
    # for containers
    children: Optional[List["GeneratedField"]] = Field(default_factory=list)
    
    # for entity dictionaries
    entity_dictionary_type: Optional[worlds_schema.EntityTypeView] = Field(default=None)

    # for lists
    add_value_type: Optional[GeneratedValueEditor] = Field(default=None)
    number_to_generate: Optional[NumberToGenerate] = Field(default=None)

    # TODO: history
    # TODO: all validations


class GeneratedEntity(BaseModel):
    entity_id: uuid.UUID = Field()
    name: Optional[str] = Field()
    image_uri: Optional[str] = Field()
    created_at: datetime.datetime = Field()
    updated_at: datetime.datetime = Field()
    path: spec.GeneratablePath = Field()
    js: str = Field(default=None)
    fields: List[GeneratedField] = Field()


class GeneratedEntityListItem(BaseModel):
    entity_id: uuid.UUID = Field()
    name: Optional[str] = Field()
    image_uri: Optional[str] = Field()
    created_at: datetime.datetime = Field()
    updated_at: datetime.datetime = Field()
    path: spec.GeneratablePath = Field()


###################################################


class ListEntitiesRequest(BaseModel):
    world_id: uuid.UUID = Field()
    entity_type: spec.EntityType = Field()
    # path: generated_model.GeneratablePath = Field()


class ListEntitiesResponse(Response):
    entities: List[GeneratedEntityListItem] = Field(default_factory=list)


class GetEntityQuery(BaseModel):
    template_id: Optional[uuid.UUID] = Field(default=None)
    generation_id: Optional[uuid.UUID] = Field(default=None)


class GetEntityRequest(BaseModel):
    world_id: uuid.UUID = Field()
    entity_id: uuid.UUID = Field()
    template_id: Optional[uuid.UUID] = Field(default=None)
    generation_id: Optional[uuid.UUID] = Field(default=None)

    @staticmethod
    def from_query(world_id: uuid.UUID, entity_id: uuid.UUID, query: Optional[GetEntityQuery]=None) -> "GetEntityRequest":
        return GetEntityRequest(
            world_id=world_id,
            entity_id=entity_id,
            template_id=query.template_id if query is not None else None,
            generation_id=query.generation_id if query is not None else None,
        )


class GetEntityResponse(Response):
    entity: GeneratedEntity = Field()


class CreateEntityRequest(BaseModel):
    world_id: uuid.UUID = Field()
    entity_type: spec.EntityType = Field()
    name: Optional[str] = Field()


class CreateEntityResponse(Response):
    entity_id: uuid.UUID = Field()
    path: spec.GeneratablePath = Field()


class DeleteEntityRequest(BaseModel):
    world_id: uuid.UUID = Field()
    entity_id: uuid.UUID = Field()


class DeleteEntityResponse(Response):
    pass


# class EntityGenerationField(BaseModel):
#     name: str = Field()


# class EntityGenerationSchema(BaseModel):
#     fields: List[EntityGenerationField] = Field()


# class GetEntitySchemaResponse(Response):
#     schema: EntityGenerationSchema = Field()
