
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union, Tuple, Set
import uuid
from enum import Enum
import cairne.model.calls as calls
import datetime
from dataclasses import dataclass
import json
import cairne.parsing.parse_incomplete_json as parse_incomplete
from structlog import get_logger
from contextlib import contextmanager
from typing import TYPE_CHECKING
import typing

if TYPE_CHECKING:
    import cairne.model.parsing as parsing
    import cairne.model.generated as generated_model


logger = get_logger(__name__)


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
    CRAFTING_OPTION = "crafting_option"
    CRAFTING_LOCATION = "crafting_location"
    ANIMAL = "animal"
    
    # LORE = "lore"
    
    def get_field_name(self) -> str:
        return self.value + "s"
    
    def get_dictionary_path(self) -> generated_model.GeneratablePath:
        return generated_model.GeneratablePath(path_elements=[generated_model.GeneratablePathElement(key=self.get_field_name())])
    
    def get_specification(self) -> "GeneratableSpecification":
        from cairne.model.world_spec import WORLD
        return typing.cast(EntityDictionarySpecification, WORLD.children[self.get_field_name()]).entity_specification
    
    
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


class GeneratableSpecification(BaseModel):
    parser: ParserSpecification = Field()
    validators: List[ValidatorSpecification] = Field(default_factory=list)


class ValueSpecification(GeneratableSpecification):
    pass

    @classmethod
    def create_spec(cls, parser_name: ParserName, required: bool = False) -> "ValueSpecification":
        return ValueSpecification(
            parser=ParserSpecification(parser_name=parser_name),
            validators=[ValidatorSpecification(validator_name=ValidatorName.REQUIRED)] if required else []
        )

    @classmethod
    def create_string_value(cls, required: bool = False) -> "ValueSpecification":
        return cls.create_spec(parser_name=ParserName.STRING, required=required)


class ObjectSpecification(GeneratableSpecification):
    parser: ParserSpecification = Field(default_factory=lambda: ParserSpecification(parser_name=ParserName.OBJECT))
    children: Dict[str, GeneratableSpecification] = Field(default=dict)


class ListSpecification(GeneratableSpecification):
    parser: ParserSpecification = Field(default_factory=lambda: ParserSpecification(parser_name=ParserName.LIST))
    element_specification: GeneratableSpecification
    
    @classmethod
    def create_list_of_strings(cls) -> "ListSpecification":
        return ListSpecification(
            # parser=ParserSpecification(parser_name=ParserName.STRING),
            element_specification=ValueSpecification.create_string_value()
        )


class EntitySpecification(ObjectSpecification):
    parser: ParserSpecification = Field(default_factory=lambda: ParserSpecification(parser_name=ParserName.ENTITY))
    entity_type: EntityType = Field()
    

class EntityDictionarySpecification(GeneratableSpecification):
    parser: ParserSpecification = Field(default_factory=lambda: ParserSpecification(parser_name=ParserName.ENTITY_DICTIONARY))
    entity_specification: EntitySpecification


class ReferenceSpecification(GeneratableSpecification):
    pass