import datetime
import json
import typing
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Tuple, Union


import random
import cairne.model.calls as calls
import cairne.parsing.parse_incomplete_json as parse_incomplete
from pydantic import BaseModel, Field
from structlog import get_logger


logger = get_logger(__name__)

  

class GeneratablePathElement(BaseModel):
	key: Optional[str] = Field(default=None)
	index: Optional[int] = Field(default=None)
	entity_id: Optional[uuid.UUID] = Field(default=None)


class GeneratablePath(BaseModel):
	path_elements: List[GeneratablePathElement] = Field(default_factory=list)

	def at(self, index: int) -> GeneratablePathElement:
		if index >= len(self.path_elements):
			raise InvalidPathError(
				path=self,
				index=index,
				message=f"Descended out of bounds for path {self.path_elements}",
			)
		return self.path_elements[index]

	def append(self, element: GeneratablePathElement) -> "GeneratablePath":
		return GeneratablePath(
			path_elements=[element.model_copy() for element in self.path_elements]
			+ [element]
		)


class InvalidPathError(Exception):
	path: "GeneratablePath"
	index: int
	message: str

	def __init__(self, path: "GeneratablePath", index: int, message: str):
		self.path = path
		self.index = index
		self.message = message


@dataclass
class ValidationError:
	path: str
	# label: str
	message: str

	def create_instruction(self):
		return f"{self.path} {self.label} {self.message}"


class BaseGenerationResult(BaseModel):
	pass


GenerationResult = Union[BaseGenerationResult, str, int, float, bool, None]


class GenerationOption(BaseModel):
	name: str
	value: Any


class ParserName(str, Enum):
	STRING = "string"
	LIST = "list"
	FLOAT = "float"
	INTEGER = "integer"
	BOOLEAN = "boolean"
	OBJECT = "object"
	ENTITY = "entity"
	ENTITY_DICTIONARY = "entity_dictionary"


class EntityType(str, Enum):
	WORLD = "world"
	CHARACTER = "character"
	ITEM = "item"
	RESOURCE_TYPE = "resource"
	REGION = "region"
	PLOT_STAGE = "plot_stage"
	DIALOGUE = "dialogue"
	TOOL = "tool"
	VEHICLE = "vehicle"
	BUILDING = "building"
	CRAFTING_RECIPE = "crafting_recipe"
	CRAFTING_LOCATION = "crafting_location"
	ANIMAL = "animal"

	# LORE = "lore"
 
	def get_label(self) -> str:
		if self == EntityType.WORLD:
			return "Worlds"
		elif self == EntityType.CHARACTER:
			return "Characters"
		elif self == EntityType.ITEM:
			return "Items"
		elif self == EntityType.RESOURCE_TYPE:
			return "Resource Types"
		elif self == EntityType.REGION:
			return "Regions"
		elif self == EntityType.PLOT_STAGE:
			return "Plot Stages"
		elif self == EntityType.DIALOGUE:
			return "Dialogues"
		elif self == EntityType.TOOL:
			return "Tools"
		elif self == EntityType.VEHICLE:
			return "Vehicles"
		elif self == EntityType.BUILDING:
			return "Buildings"
		elif self == EntityType.CRAFTING_RECIPE:
			return "Crafting Recipes"
		elif self == EntityType.CRAFTING_LOCATION:
			return "Crafting Locations"
		elif self == EntityType.ANIMAL:
			return "Animals"
		else:
			raise NotImplementedError(f"Invalid entity type: {self}")

	@staticmethod
	def get(name: str) -> "EntityType":
		for entity_type in EntityType:
			if entity_type.value == name:
				return entity_type
		raise ValueError(f"Invalid entity type: {name}")

	def get_field_name(self) -> str:
		return self.value + "s"

	# Is this needed?
	def get_dictionary_path(self) -> GeneratablePath:
		return GeneratablePath(
			path_elements=[
				GeneratablePathElement(key=self.get_field_name())
			]
		)

	def get_specification(self) -> "EntitySpecification":
		from cairne.model.world_spec import WORLD

		return typing.cast(
			EntityDictionarySpecification, WORLD.children[self.get_field_name()]
		).entity_specification


"""
def _get_specification(world_field: str) -> Tuple[spec.GeneratableSpecification, generated_model.GeneratablePath]:
	return WORLD.children[world_field], 


def get_specification(world_id: Optional[uuid.UUID], entity_type: spec.EntityType) -> Tuple[spec.GeneratableSpecification, generated_model.GeneratablePath]:
	if entity_type == spec.EntityType.WORLD:
		return WORLD, generated_model.GeneratablePath(path=[])
	elif entity_type == spec.EntityType.CHARACTER:
		return _get_specification("characters")
	elif entity_type == spec.EntityType.ITEM:
		return _get_specification("items")
	elif entity_type == spec.EntityType.RESOURCE_TYPE:
		return _get_specification("resource_types")
	elif entity_type == spec.EntityType.REGION:
		return _get_specification("regions")
	elif entity_type == spec.EntityType.PLOT_STAGE:
		return _get_specification("plot_stages")
	elif entity_type == spec.EntityType.DIALOGUE:
		return _get_specification("dialogues")
	elif entity_type == spec.EntityType.TOOL:
		return _get_specification("tools")
	elif entity_type == spec.EntityType.VEHICLE:
		return _get_specification("vehicles")
	elif entity_type == spec.EntityType.BUILDING:
		return _get_specification("buildings")
	elif entity_type == spec.EntityType.CRAFTING_OPTION:
		return _get_specification("crafting_options")
	elif entity_type == spec.EntityType.CRAFTING_LOCATION:
		return _get_specification("crafting_locations")
	elif entity_type == spec.EntityType.ANIMAL:
		return _get_specification("animals")
	else:
		raise NotImplementedError(f"Invalid entity type: {entity_type}")
"""


class ParserSpecification(BaseModel):
	parser_name: ParserName = Field()


class ValidatorName(str, Enum):
	REQUIRED = "required"
	ONE_OF_LITERAL = "one_of_literal"
	ONE_OF_FIELD = "one_of"
	NAME = "name"
	NONNEGATIVE = "nonnegative"
	LIST_OF_ARBITRARY_STRINGS = "list_of_arbitrary_strings"


class ValidatorSpecification(BaseModel):
	validator_name: ValidatorName = Field()


class OneOfLiteralValidator(ValidatorSpecification):
	options: List[Tuple[GenerationResult, Set[str]]] = Field(default_factory=list)


class EditorName(str, Enum):
	LONG_STRING = "LONG_STRING"
	SHORT_STRING = "short_string"
	NUMBER_INPUT = "number_input"
	BOOLEAN_INPUT = "boolean_input"
	ENUMERATED = "enumerated"


class EditorSpecification(BaseModel):
	# Maybe this should be one of generated_schema.GeneratedValueEditor...
	editor_name: str = Field()
	# TODO: Create instructions for the add to list method, somehow


class GenerationSpecification(BaseModel):
	instructions: List[str] = Field(default_factory=list)
	
	expected_num_tokens: Optional[int] = Field(default=None)
	num_examples: Optional[int] = Field(default=None)
 
 
 	# example_json_values: Optional[List[str]] = Field(default=None)
	# Can this be generated from pydantic?
	# json_schema: Dict[str, str] = Field(default_factory=dict)

	
	# TODO: move this somewhere where it can accept fields: generate_model.TargetFields and world
	# def create_json_schema(self, root_fields: List[str]) -> str:
	# 	schema = {}
	# 	for field in root_fields:
	# 		if field not in self.json_schema:
	# 			logger.warning(f"Field {field} not found in json schema")
	# 			continue
	# 		schema[field] = self.json_schema[field]
	# 	return json.dumps(schema, indent=2)


class GeneratableSpecification(BaseModel):
	parser: ParserSpecification = Field()
	validators: List[ValidatorSpecification] = Field(default_factory=list)
	generation: GenerationSpecification = Field(default_factory=lambda: GenerationSpecification())
	# Options for how to add to a list

	def create_example(self) -> Any:
		raise NotImplementedError()
 
	def get(self, path: GeneratablePath, path_index: int) -> "GeneratableSpecification":
		raise NotImplementedError()

	def create_schema(self) -> str:
		# TODO
		return ""



class ValueSpecification(GeneratableSpecification):
	editor: EditorSpecification = Field()
 
	# @classmethod
	# def create_spec(
	# 	cls,
  	# 	parser_name: ParserName,
	# 	required: bool = False,
	#  	example_json_values: Optional[List[str]] = None,
	# 	# editor_name: EditorName = EditorName.TEXT_AREA,
	# ) -> "ValueSpecification":
	# 	return ValueSpecification(
	# 		parser=ParserSpecification(parser_name=parser_name),
	# 		generation=GenerationSpecification(
	# 			example_json_values=example_json_values
	# 		) if example_json_values is not None else GenerationSpecification(),
	# 		validators=[ValidatorSpecification(validator_name=ValidatorName.REQUIRED)]
	# 		if required
	# 		else [],
	# 	)

	# @classmethod
	# def create_string_value(cls, required: bool = False, example_json_values: Optional[List[str]] = None) -> "ValueSpecification":
	# 	return cls.create_spec(parser_name=ParserName.STRING, required=required, example_json_values=example_json_values)

	def create_example(self) -> Any:
		if self.parser.parser_name == ParserName.STRING:
			return "Example string"
		elif self.parser.parser_name == ParserName.FLOAT:
			return 29.4
		elif self.parser.parser_name == ParserName.INTEGER:
			return 13
		elif self.parser.parser_name == ParserName.BOOLEAN:
			if random.random() < 0.5:
				return True
			else:
				return False
		else:
			raise NotImplementedError(f"Unknown parser name: {self.parser.parser_name}")

	def get(self, path: GeneratablePath, path_index: int) -> "GeneratableSpecification":
		if path_index != len(path.path_elements):
			raise InvalidPathError(
				path=path,
				index=path_index,
				message=f"Descended out of bounds for path {path.path_elements}",
			)
		return self


class ObjectSpecification(GeneratableSpecification):
	parser: ParserSpecification = Field(
		default_factory=lambda: ParserSpecification(parser_name=ParserName.OBJECT)
	)
	children: Dict[str, GeneratableSpecification] = Field(default=dict)
 
	def create_example(self) -> Any:
		example = {}
		for key, child in self.children.items():
			example[key] = child.create_example()
		return example
 
	def get(self, path: GeneratablePath, path_index: int) -> "GeneratableSpecification":
		if path_index == len(path.path_elements):
			return self
		if path_index > len(path.path_elements):
			raise InvalidPathError(
				path=path,
				index=path_index,
				message=f"Descended out of path bounds for path {path.path_elements}",
			)
		path_element = path.at(path_index)
		if path_element.key is None:
			raise InvalidPathError(
				path=path,
				index=path_index,
				message=f"Expected key for path element {path_element} at index {path_index}",
			)
		if path_element.key not in self.children:
			raise InvalidPathError(
				path=path,
				index=path_index,
				message=f"Key {path_element.key} not present at index {path_index}. keys: {self.children.keys()}",
			)
		return self.children[path_element.key].get(path, path_index + 1)


class ListSpecification(GeneratableSpecification):
	parser: ParserSpecification = Field(
		default_factory=lambda: ParserSpecification(parser_name=ParserName.LIST)
	)
	element_specification: GeneratableSpecification
 
	def create_example(self) -> Any:
		num_examples = self.generation.num_examples
		if num_examples is None:
			num_examples = 2
		return [self.element_specification.create_example() for _ in range(num_examples)]

	# @classmethod
	# def create_list_of_strings(cls) -> "ListSpecification":
	# 	return ListSpecification(
	# 		# parser=ParserSpecification(parser_name=ParserName.STRING),
	# 		element_specification=ValueSpecification.create_string_value()
	# 	)
 
	def get(self, path: GeneratablePath, path_index: int) -> "GeneratableSpecification":
		if path_index == len(path.path_elements):
			return self
		if path_index > len(path.path_elements):
			raise InvalidPathError(
				path=path,
				index=path_index,
				message=f"Descended out of path bounds for path {path.path_elements}",
			)
		path_element = path.at(path_index)
		if path_element.index is None:
			raise InvalidPathError(
				path=path,
				index=path_index,
				message=f"Expected index for path element {path_element} at index {path_index}",
			)
		return self.element_specification.get(path, path_index + 1)


class EntitySpecification(ObjectSpecification):
	parser: ParserSpecification = Field(default_factory=lambda: ParserSpecification(parser_name=ParserName.ENTITY))
	entity_type: EntityType = Field()


class EntityDictionarySpecification(GeneratableSpecification):
	parser: ParserSpecification = Field(
		default_factory=lambda: ParserSpecification(
			parser_name=ParserName.ENTITY_DICTIONARY
		)
	)
	entity_specification: EntitySpecification
 
	def get(self, path: GeneratablePath, path_index: int) -> "GeneratableSpecification":
		if path_index == len(path.path_elements):
			return self
		if path_index > len(path.path_elements):
			raise InvalidPathError(
				path=path,
				index=path_index,
				message=f"Descended out of path bounds for path {path.path_elements}",
			)
		path_element = path.at(path_index)
		if path_element.entity_id is None:
			raise InvalidPathError(
				path=path,
				index=path_index,
				message=f"Expected entity id for path element {path_element} at index {path_index}",
			)
		return self.entity_specification.get(path, path_index + 1)


class ReferenceSpecification(GeneratableSpecification):
	def get(self, path: GeneratablePath, path_index: int) -> "GeneratableSpecification":
		if path_index == len(path.path_elements):
			return self
		raise InvalidPathError(
			path=path,
			index=path_index,
			message=f"Cannot descend into a reference.",
		)
