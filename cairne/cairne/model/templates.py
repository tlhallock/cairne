import datetime
import json
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union, Literal, Annotated

from pydantic import BaseModel, Field
from structlog import get_logger

import cairne.model.generated as generated_model
import cairne.model.specification as spec
from cairne.model.world_spec import WORLD
import typing

# TODO: rename this file to generate...


logger = get_logger(__name__)


class GeneratorType(str, Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    HUGGING_FACE = "hugging_face"

    def get_label(self):
        if self == GeneratorType.OLLAMA:
            return "Ollama"
        elif self == GeneratorType.OPENAI:
            return "Open AI"
        elif self == GeneratorType.HUGGING_FACE:
            return "Hugging Face"
        else:
            raise ValueError(f"Unknown generator type: {self}")
    
    def get_models(self) -> List[str]:
        if self == GeneratorType.OLLAMA:
            return ["not implemented"]
        elif self == GeneratorType.OPENAI:
            return [
                'gpt-4-1106-preview',
                'gpt-4-vision-preview',
                'gpt-4',
                'gpt-4-0314',
                'gpt-4-0613',
                'gpt-4-32k',
                'gpt-4-32k-0314',
                'gpt-4-32k-0613',
                'gpt-3.5-turbo',
                'gpt-3.5-turbo-16k',
                'gpt-3.5-turbo-0301',
                'gpt-3.5-turbo-0613',
                'gpt-3.5-turbo-1106',
                'gpt-3.5-turbo-16k-0613',
            ]
        elif self == GeneratorType.HUGGING_FACE:
            return ["not implemented"]
        else:
            raise ValueError(f"Unknown generator type: {self}")
    
    def get_default_model(self) -> str:
        if self == GeneratorType.OLLAMA:
            return "not implemented"
        elif self == GeneratorType.OPENAI:
            return "gpt-3.5-turbo-1106"
        elif self == GeneratorType.HUGGING_FACE:
            return "not implemented"
        else:
            raise ValueError(f"Unknown generator type: {self}")


class GenerationType(str, Enum):
    TEXT = "text"
    # Should I have a different type for json?
    IMAGE = "image"
    AUDIO = "audio"


class JsonStructure(BaseModel):
    json_schema: Optional[str] = Field(default=None)
    examples: Optional[str] = Field(default=None)


class GeneratorModel(BaseModel):
    generator_type: GeneratorType = Field()
    g_model_id: str = Field()


class GenerationRequestParameters(BaseModel):
    max_tokens: Optional[int] = Field(default=None)
    temperature: Optional[float] = Field(default=None)
    top_p: Optional[float] = Field(default=None)
    frequency_penalty: Optional[float] = Field(default=None)
    presence_penalty: Optional[float] = Field(default=None)
    seed: Optional[int] = Field(default=1776)
    
    def update_from(self, parameter_updates: "GenerationRequestParameters") -> None:
        if parameter_updates.max_tokens is not None:
            self.max_tokens = parameter_updates.max_tokens
        if parameter_updates.temperature is not None:
            self.temperature = parameter_updates.temperature
        if parameter_updates.top_p is not None:
            self.top_p = parameter_updates.top_p
        if parameter_updates.frequency_penalty is not None:
            self.frequency_penalty = parameter_updates.frequency_penalty
        if parameter_updates.presence_penalty is not None:
            self.presence_penalty = parameter_updates.presence_penalty
        if parameter_updates.seed is not None:
            self.seed = parameter_updates.seed
    
    def remove_parameters(self, parameters_to_remove: List[str]) -> None:
        for parameter in parameters_to_remove:
            if parameter == "max_tokens":
                self.max_tokens = None
            elif parameter == "temperature":
                self.temperature = None
            elif parameter == "top_p":
                self.top_p = None
            elif parameter == "frequency_penalty":
                self.frequency_penalty = None
            elif parameter == "presence_penalty":
                self.presence_penalty = None
            elif parameter == "seed":
                self.seed = None
            else:
                raise ValueError(f"Unknown parameter: {parameter}")


class FilledInstruction(BaseModel):
    name: str = Field()
    message: str = Field()

    @staticmethod
    def format(instruction: spec.PredefinedInstruction, variables: Dict[str, str]) -> "FilledInstruction":
        return FilledInstruction(
            name=instruction.name,
            message=instruction.template.format(**variables)
        )


class GenerationVariables(BaseModel):
    variables: Dict[str, str] = Field(default_factory=dict)

    def can_evaluate(self, instruction: spec.PredefinedInstruction) -> bool:
        for req in instruction.get_required_variables():
            if req in self.variables:
                continue
            return False
        return True

    def fill_instructions(self, unfilled_instructions: List[spec.PredefinedInstruction]) -> List[FilledInstruction]:
        filled_instructions: List[FilledInstruction] = []
        # Should this be a set?

        while True:
            remaining_instructions: List[spec.PredefinedInstruction] = []
            for instruction in unfilled_instructions:
                if not self.can_evaluate(instruction):
                    remaining_instructions.append(instruction)
                    continue

                filled = FilledInstruction.format(instruction, self.variables)
                # self.variables[variable.name] = variable.value.format(**variables)
                filled_instructions.append(filled)
            if len(remaining_instructions) == len(unfilled_instructions):
                break
            unfilled_instructions = remaining_instructions
        if len(remaining_instructions) > 0:
            logger.warning(f"Could not fill instructions: {remaining_instructions}")
        return filled_instructions

    @staticmethod
    def create(world: generated_model.GeneratedEntity) -> "GenerationVariables":
        import cairne.openrpg.world_helpers as world_helpers
        import cairne.model.character as character_model
        
        variables: Dict[str, str] = dict(
            possible_factions=", ".join(
                faction for faction in world_helpers.get_factions(world)
            ),
            possible_genders=", ".join(
                gender.value for gender in character_model.Gender
            ),
            possible_archetypes=", ".join(
                archetype.value for archetype in character_model.Archetype
            ),
            existing_characters=world_helpers.describe_existing_characters(world),
        )
        theme = world_helpers.get_theme(world)
        if theme is not None:
            variables["theme"] = theme
        character_counts = world_helpers.CharacterCounts.get_character_counts(world)

        # TODO: when we generate more than one character:
        generation_target = world_helpers.CharacterGenerationTarget(
            number_of_total_characters=20,
            number_of_characters_per_faction=4,
        )
        character_counts.format_count_instructions(generation_target)
        "Do not generate more than what is needed."

        return GenerationVariables(variables=variables)


class TargetFields(BaseModel):
    all: Optional[bool] = Field(default=None)
    fields: List[str] = Field(default_factory=list)
    

class BaseGenerationResult(BaseModel):
    raw_text: str = Field()
    parsed: Optional[generated_model.Generated] = Field(default=None)


class OpenAIGenerationResult(BaseGenerationResult):
    result_type: Literal["openai"] = Field(default_factory=lambda: "openai")

    completion_tokens: int = Field()
    prompt_tokens: int = Field()
    total_tokens: int = Field()
    finish_reason: str = Field()


class HuggingFaceGenerationResult(BaseGenerationResult):
    result_type: Literal["hugging_face"] = Field(default_factory=lambda: "hugging_face")


GenerateResult = Annotated[
    Union[
        OpenAIGenerationResult,
        HuggingFaceGenerationResult,
    ],
    Field(discriminator="result_type"),
]

class IncludableInstruction(BaseModel):
    name: str = Field()
    include: bool = Field(default=True)
    # part of the schema only...
    preview: str = Field(default=None)


class FieldToInclude(BaseModel):
    path: spec.GeneratablePath = Field()


class NumberToGenerate(BaseModel):
    path: spec.GeneratablePath = Field()
    number: Optional[int] = Field(default=None)


class GenerationTemplate(BaseModel):
    template_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = Field()
    generation_type: GenerationType = Field()
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    world_id: uuid.UUID = Field()
    entity_id: uuid.UUID = Field()
    target_path: spec.GeneratablePath = Field()
    entity_type: spec.EntityType = Field()
    
    generator_model: GeneratorModel = Field()
    
    parameters: GenerationRequestParameters = Field(default_factory=GenerationRequestParameters)
    additional_prompt: Optional[str] = Field(default=None)
    excluded_instruction_names: List[str] = Field(default_factory=list)
    # validations_to_include: List[Instruction] = Field(default_factory=list)
    # Should think about if they should all be included by default
    fields_to_include: List[FieldToInclude] = Field(default_factory=list)
    numbers_to_generate: List[NumberToGenerate] = Field(default_factory=list)
    deletion: Optional[generated_model.Deletion] = Field(default=None)
    
    def get_instructions(self) -> List[spec.PredefinedInstruction]:
        specification = WORLD.get(self.target_path, 0)
        return [
            instruction
            for instruction in specification.generation.instructions
            if instruction.name not in self.excluded_instruction_names
        ]

    def create_json_schema(self) -> str:
        specification = WORLD.get(self.target_path, 0)
        return json.dumps(specification.create_schema(
            [field.path for field in self.fields_to_include]
        ))

    def apply(self, world: generated_model.GeneratedEntity) -> None:
        for field_to_include in self.fields_to_include:
            world.get(field_to_include.path, 0).generate = True
        for number_to_generate in self.numbers_to_generate:
            field = world.get(number_to_generate.path, 0)
            if not isinstance(field, generated_model.GeneratedList):
                raise ValueError(f"Can only set number to generate on lists, not {field}")
            list_field = typing.cast(generated_model.GeneratedList, field)
            list_field.generation_settings = generated_model.GenerateListSettings(
                number_to_generate=number_to_generate.number
            )
