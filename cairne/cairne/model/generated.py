
import datetime
import json
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union, Literal

from typing_extensions import Annotated
import cairne.model.calls as calls
import cairne.model.specification as spec
import cairne.parsing.parse_incomplete_json as parse_incomplete
from pydantic import BaseModel, Field
from structlog import get_logger
import abc

logger = get_logger(__name__)


"""
TODO: rename generated -> state
TODO: break off the generatable into the schema vs state vs validator
How should I have versions

Should I have keep previous versions of each field
I want to be able to see which options someone selected...


I should have a bark (trigger random dialogue near player) as well



Views:
generate several
	generation target
generate one
add fields
free-form inspiration
generate options

the user should be able to modify the output of an llm call before validating...

"""


"""
Support generation sessions later


GeneratableEntity

"""



class GenerationOption(BaseModel):
	name: str
	value: Any


class GenerationSourceType(str, Enum):
	MODEL_CALL = "model_call"
	USER_INPUT = "user_input"
	USER_CHOICE = "user_choice"
	USER_EDIT = "user_edit"
	RANDOM = "random"
	DEFAULT_VALUE = "default_value"
	UNINITIALIZED = "uninitialized"


class GenerationSource(BaseModel):
	source_type: GenerationSourceType = Field(default=GenerationSourceType.UNINITIALIZED)
	model_call: Optional[calls.ModelCall] = Field(default=None)
	# user selection of language model output
	pass


class GeneratedVersion(BaseModel):
	source: GenerationSource = Field(default_factory=GenerationSource)
	date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
	value_js: str = Field(default=None)


class GenerationMetadata(BaseModel):
	source: GenerationSource = Field(default_factory=GenerationSource)
	previous: List["GeneratedVersion"] = Field(default_factory=list)
	date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class Deletion(BaseModel):
	date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
	deleted_by: Optional[str] = Field(default=None)


class LocatedEntity(BaseModel):
	entity: "GeneratedEntity" = Field()
	path: spec.GeneratablePath = Field()


class GeneratedBase(BaseModel):
	metadata: GenerationMetadata = Field(default_factory=GenerationMetadata)
	raw: Union[str, int, float, bool, None, dict, list] = Field(default=None)
	result: Optional[
		spec.BaseGenerationResult | str | int | float | bool | None
	] = Field(default=None)
	deletion: Optional[Deletion] = Field(default=None)

	def is_generated(self) -> bool:
		raise NotImplementedError()

	def get_creation_date(self) -> datetime.datetime:
		if len(self.metadata.previous) == 0:
			return self.metadata.date
		return self.metadata.previous[-1].date

	def search_for_entity(
		self, entity_id: uuid.UUID, path: spec.GeneratablePath
	) -> Optional[LocatedEntity]:
		raise NotImplementedError

	def get(self, path: spec.GeneratablePath, path_index: int) -> "Generated":
		raise NotImplementedError


class GeneratedValue(GeneratedBase):
	# choices presented to the user?
	def search_for_entity(
		self, entity_id: uuid.UUID, path: spec.GeneratablePath
	) -> Optional[LocatedEntity]:
		return None

	def get(self, path: spec.GeneratablePath, path_index: int) -> "Generated":
		if path_index == len(path.path_elements):
			return self  # type: ignore
		raise spec.InvalidPathError(
			path=path, index=path_index, message="Cannot traverse into a value"
		)


class GeneratedString(GeneratedValue):
	generated_type: Literal["string"] = Field(default_factory=lambda: "string")
	parsed: Optional[str] = Field(default=None)

	def is_generated(self) -> bool:
		return self.parsed is not None


class GeneratedFloat(GeneratedValue):
	generated_type: Literal["float"] = Field(default_factory=lambda: "float")
	parsed: Optional[float] = Field(default=None)

	def is_generated(self) -> bool:
		return self.parsed is not None


class GeneratedInteger(GeneratedValue):
	generated_type: Literal["integer"] = Field(default_factory=lambda: "integer")
	parsed: Optional[int] = Field(default=None)

	def is_generated(self) -> bool:
		return self.parsed is not None


class GeneratedBoolean(GeneratedValue):
	generated_type: Literal["boolean"] = Field(default_factory=lambda: "boolean")
	parsed: Optional[bool] = Field(default=False)

	def is_generated(self) -> bool:
		return self.parsed is not None


class GeneratedObject(GeneratedBase):
	generated_type: Literal["object"] = Field(default_factory=lambda: "object")
	children: Dict[str, "Generated"] = Field(default=dict)
	parsed: Optional[dict] = Field(default=dict)

	def is_generated(self) -> bool:
		return self.parsed is not None and len(self.parsed) > 0

	def get(self, path: spec.GeneratablePath, path_index: int) -> "Generated":
		if path_index == len(path.path_elements):
			return self
		path_element = path.at(path_index)
		if path_element.key is None:
			raise spec.InvalidPathError(
				path=path, index=path_index, message="Expected a key for an object"
			)
		child = self.children.get(path_element.key, None)
		if child is None:
			raise spec.InvalidPathError(
				path=path,
				index=path_index,
				message=f"Could not find child with key {path_element.key}",
			)
		return child.get(path=path, path_index=path_index + 1)

	def search_for_entity(
		self, entity_id: uuid.UUID, path: spec.GeneratablePath
	) -> Optional[LocatedEntity]:
		for key, child in self.children.items():
			located = child.search_for_entity(
				entity_id, path.append(spec.GeneratablePathElement(key=key))
			)
			if located is not None:
				return located
		return None


class GeneratedList(GeneratedBase):
	generated_type: Literal["list"] = Field(default_factory=lambda: "list")
	elements: List["Generated"] = Field(default=list)
	parsed: Optional[list] = Field(default=dict)

	def is_generated(self) -> bool:
		return self.parsed is not None and len(self.parsed) > 0

	def search_for_entity(
		self, entity_id: uuid.UUID, path: spec.GeneratablePath
	) -> Optional[LocatedEntity]:
		for index, child in enumerate(self.elements):
			located = child.search_for_entity(
				entity_id, path.append(spec.GeneratablePathElement(index=index))
			)
			if located is not None:
				return located
		return None

	def get(self, path: spec.GeneratablePath, path_index: int) -> "Generated":
		if path_index == len(path.path_elements):
			return self
		path_element = path.at(path_index)
		if path_element.index is None:
			raise spec.InvalidPathError(
				path=path, index=path_index, message="Expected an index for a list"
			)
		if path_element.index >= len(self.elements):
			raise spec.InvalidPathError(
				path=path,
				index=path_index,
				message=f"Index {path_element.index} out of bounds for list of length {len(self.elements)}",
			)
		if path_element.index < 0:
			raise spec.InvalidPathError(
				path=path,
				index=path_index,
				message=f"Index {path_element.index} cannot be negative",
			)
		child = self.elements[path_element.index]
		return child.get(path=path, path_index=path_index + 1)


class GeneratedEntity(GeneratedObject):
	generated_type: Literal["entity"] = Field(default_factory=lambda: "entity")
	entity_id: uuid.UUID = Field(default_factory=uuid.uuid4)
	entity_type: spec.EntityType = Field()
	# entity type?

	def search_for_entity(
		self, entity_id: uuid.UUID, path: spec.GeneratablePath
	) -> Optional[LocatedEntity]:
		if self.entity_id == entity_id:
			return LocatedEntity(entity=self, path=path)
		return super().search_for_entity(entity_id, path)

	def get_name(self) -> Optional[str]:
		name = self.children.get("name", None)
		if name is None:
			return None
		if not isinstance(name, GeneratedString):
			return None
		return name.parsed

	def create_path(self) -> spec.GeneratablePath:
		parent_path = self.entity_type.get_dictionary_path()
		return parent_path.append(spec.GeneratablePathElement(entity_id=self.entity_id))


class EntityDictionary(GeneratedBase):
	generated_type: Literal["entity_dictionary"] = Field(default_factory=lambda: "entity_dictionary")
	entities: Dict[uuid.UUID, GeneratedEntity] = Field(default_factory=dict)

	def is_generated(self) -> bool:
		return len(self.entities) > 0

	def search_for_entity(
		self, entity_id: uuid.UUID, path: spec.GeneratablePath
	) -> Optional[LocatedEntity]:
		# if entity_id in self.entities:
		#     return LocatedEntity(entity=self.entities[entity_id], path=path.append(GeneratablePathElement(entity_id=entity_id)))
		for entity in self.entities.values():
			located = entity.search_for_entity(
				entity_id,
				path.append(spec.GeneratablePathElement(entity_id=entity.entity_id)),
			)
			if located is not None:
				return located
		return None

	def get(self, path: spec.GeneratablePath, path_index: int) -> "Generated":
		if path_index == len(path.path_elements):
			return self
		path_element = path.at(path_index)
		if path_element.entity_id is None:
			raise spec.InvalidPathError(
				path=path,
				index=path_index,
				message="Expected an entity_id for an entity dictionary",
			)
		entity = self.entities.get(path_element.entity_id, None)
		if entity is None:
			raise spec.InvalidPathError(
				path=path,
				index=path_index,
				message=f"Could not find entity with id {path_element.entity_id}",
			)
		return entity.get(path=path, path_index=path_index + 1)


class GeneratedReference(GeneratedBase):
	generated_type: Literal["reference"] = Field(default_factory=lambda: "reference")
	entity_type: Optional[spec.EntityType] = Field(default_factory=None)
	entity_id: Optional[uuid.UUID] = Field(default_factory=None)
	entity_name: Optional[str] = Field(default_factory=None)

	located_entity: Optional[uuid.UUID] = Field(default=None)

	def is_generated(self) -> bool:
		return (
			self.entity_id is not None
			or self.entity_name is not None
			or self.located_entity is not None
		)

	def search_for_entity(
		self, entity_id: uuid.UUID, path: spec.GeneratablePath
	) -> Optional[LocatedEntity]:
		return None

	def get(self, path: spec.GeneratablePath, path_index: int) -> "Generated":
		if path_index == len(path.path_elements):
			return self
		raise spec.InvalidPathError(
			path=path, index=path_index, message="Cannot descend into a reference"
		)



Generated = Annotated[
	Union[
		GeneratedString,
		GeneratedFloat,
		GeneratedInteger,
		GeneratedBoolean,
		GeneratedObject,
		GeneratedList,
		GeneratedEntity,
		EntityDictionary,
		GeneratedReference
	],
	Field(discriminator='generated_type')
]

# class Generatable(BaseModel):
# choices
# call_ids: List[uuid.UUID]

