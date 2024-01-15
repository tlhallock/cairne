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


class GenerationState(BaseModel):
	# Use the raw value or the parsed value?
	# Use type specific classes, object vs list or just put everything in json?
	# Include the path for each field
	pass


class GeneratedField(BaseModel):
	label: str = Field()
	raw_value: str = Field()
	value_js: str = Field()
	# display_path: List[str] = Field(default_factory=list)
	value_type: GeneratedValueEditor = Field()
	edit_path: spec.GeneratablePath = Field()
	choices: Optional[List[str]] = Field(default=None)
	validation_errors: List[str] = Field(default_factory=list)
	children: Optional[List["GeneratedField"]] = Field(default_factory=list)
	add_value_type: Optional[GeneratedValueEditor] = Field(default=None)

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


class GetEntityRequest(BaseModel):
	world_id: uuid.UUID = Field()
	entity_id: Optional[uuid.UUID] = Field(default=None)


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


class EntityGenerationField(BaseModel):
    name: str = Field()


class EntityGenerationSchema(BaseModel):
	fields: List[EntityGenerationField] = Field()


class GetEntitySchemaResponse(Response):
	schema: EntityGenerationSchema = Field()
