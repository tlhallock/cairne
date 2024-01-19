import datetime
import json
import string
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union, Literal, Annotated

from pydantic import BaseModel, Field
from structlog import get_logger

import cairne.model.calls as calls
import cairne.model.generated as generated_model
import cairne.model.specification as spec
import cairne.parsing.parse_incomplete_json as parse_incomplete

# TODO: rename this file to generate...

logger = get_logger(__name__)


class GenerationEndpoint(str, Enum):
    CHARACTER = "character"
    CHARACTERS = "characters"


class ChatRole(str, Enum):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"


class GenerationChatMessage(BaseModel):
    role: ChatRole = Field()
    message: str = Field()


class GenerationStatus(str, Enum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    STREAMING = "streaming"
    ERROR = "error"
    COMPLETE = "complete"


class GenerationStopReason(str, Enum):
    SUCCESS = "success"
    RATE_LIMIT = "rate_limit"
    CONTENT_FILTER = "content_filter"
    TIMEOUT = "timeout"
    ERROR = "error"


class GeneratorType(str, Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    HUGGING_FACE = "hugging_face"


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


class Instruction(BaseModel):
    message: str = Field()

    def format(self, variables: Dict[str, str]) -> str:
        return self.message.format(**variables)


class GenerationVariables(BaseModel):
    variables: Dict[str, str] = Field(default_factory=dict)

    @classmethod
    def get_required_variables(cls, prompt: str) -> List[str]:
        return [
            arg[1] for arg in string.Formatter().parse(prompt) if arg[1] is not None
        ]

    def can_evaluate(self, instruction: Instruction) -> bool:
        for req in GenerationVariables.get_required_variables(instruction.message):
            if req in self.variables:
                continue
            return False
        return True

    # TODO: maybe a filled instruction is different?
    def format(self, unfilled_instructions: List[Instruction]) -> List[Instruction]:
        filled_instructions: List[Instruction] = []
        # Should this be a set?

        while True:
            remaining_instructions: List[Instruction] = []
            for instruction in unfilled_instructions:
                if not self.can_evaluate(instruction):
                    remaining_instructions.append(instruction)
                    continue

                formatted = instruction.format(self.variables)
                # self.variables[variable.name] = variable.value.format(**variables)
                filled_instructions.append(Instruction(message=formatted))
            if len(remaining_instructions) == len(unfilled_instructions):
                break
            unfilled_instructions = remaining_instructions
        if len(remaining_instructions) > 0:
            logger.warning(f"Could not fill instructions: {remaining_instructions}")
        return filled_instructions


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
    
    


class Generation(BaseModel):
    # assumes a chat model...

    generation_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    world_id: uuid.UUID = Field()
    entity_id: uuid.UUID = Field()
    generation_type: GenerationType = Field()
    entity_type: spec.EntityType = Field()
    target_path: spec.GeneratablePath = Field()

    generator_model: GeneratorModel = Field()
    parameters: GenerationRequestParameters = Field(
        default_factory=GenerationRequestParameters
    )

    prompt_messages: List[GenerationChatMessage] = Field(default=None)
    filled_instructions: List[Instruction] = Field(default=None)
    generation_variables: GenerationVariables = Field(
        default_factory=GenerationVariables
    )
    json_structure: Optional[JsonStructure] = Field(default=None)

    # endpoint: GenerationEndpoint = Field()
    # request...

    begin_time: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    end_time: Optional[datetime.datetime] = Field(default=None)
    # Time for llm calls as separate fields?
    status: GenerationStatus = Field(default=GenerationStatus.QUEUED)

    input_tokens: Optional[int] = Field(default=None)
    output_tokens: Optional[int] = Field(default=None)
    
    result: Optional[GenerateResult] = Field(default=None)

    # Need to store the result
    # TODO: need to store the location to put the result? world id, entity id
    
    def as_source(self) -> generated_model.GenerationSource:
        return generated_model.GenerationSource(
            source_type=generated_model.GenerationSourceType.MODEL_CALL,
        )

