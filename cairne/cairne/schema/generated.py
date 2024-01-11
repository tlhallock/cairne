import datetime
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import cairne.model.generated as generated
import cairne.model.generated as generated_model
import cairne.model.generation as generation_model
import cairne.model.specification as spec
import cairne.schema.edits as edits_schema
from cairne.schema.base import Response
from pydantic import BaseModel, Field


class GeneratedValueType(str, Enum):
	STRING = "string"
	FLOAT = "float"
	INT = "int"
	BOOLEAN = "boolean"
	OBJECT = "object"
	LIST = "list"


class GenerationHistory(BaseModel):
	pass


class GenerationState(BaseModel):
	# Use the raw value or the parsed value?
	# Use type specific classes, object vs list or just put everything in json?
	# Include the path for each field
	pass


class GeneratedItem(BaseModel):
	raw_value: str = Field()
	value_js: str = Field()
	display_path: List[str] = Field(default_factory=list)
	value_type: GeneratedValueType = Field()
	edit_path: generated_model.GeneratablePath = Field()
	choices: Optional[List[str]] = Field(default=None)
	validation_errors: List[str] = Field(default_factory=list)
	# history
	# all validations


class GeneratedEntity(BaseModel):
	entity_id: uuid.UUID = Field()
	name: Optional[str] = Field()
	image_uri: Optional[str] = Field()
	created_at: datetime.datetime = Field()
	updated_at: datetime.datetime = Field()
	path: generated_model.GeneratablePath = Field()
	js: str = Field(default=None)
	fields: List[GeneratedItem] = Field()


class GeneratedEntityListItem(BaseModel):
	entity_id: uuid.UUID = Field()
	name: Optional[str] = Field()
	image_uri: Optional[str] = Field()
	created_at: datetime.datetime = Field()
	updated_at: datetime.datetime = Field()
	path: generated_model.GeneratablePath = Field()


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
	path: generated_model.GeneratablePath = Field()


class DeleteEntityRequest(BaseModel):
	world_id: uuid.UUID = Field()
	entity_id: uuid.UUID = Field()


class DeleteEntityResponse(Response):
	pass
