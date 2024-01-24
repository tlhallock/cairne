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
import cairne.model.templates as template_model
from cairne.model.world_spec import WORLD
import cairne.model.parsing as parsing

# TODO: rename this file to generate...

logger = get_logger(__name__)


# class GenerationEndpoint(str, Enum):
#     CHARACTER = "character"
#     CHARACTERS = "characters"


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
    template_snapshot: template_model.GenerationTemplate = Field()

    # TODO: these should only be additional?
    # TODO: maybe remove this, more for a chat...
    prompt_messages: List[GenerationChatMessage] = Field(default=None)
    filled_instructions: List[template_model.FilledInstruction] = Field(default=None)
    
    # Not really needed
    json_structure: Optional[template_model.JsonStructure] = Field(default=None)

    begin_time: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    end_time: Optional[datetime.datetime] = Field(default=None)
    status: GenerationStatus = Field(default=GenerationStatus.QUEUED)
    
    result: Optional[GenerateResult] = Field(default=None)
    deletion: Optional[generated_model.Deletion] = Field(default=None)
    
    def as_source(self) -> generated_model.GenerationSource:
        return generated_model.GenerationSource(
            source_type=generated_model.GenerationSourceType.MODEL_CALL,
        )
    
    def apply(self, world: generated_model.GeneratedEntity, parsed: generated_model.GeneratedEntity) -> None:
        if not self.result:
            return
        destination = world.get(self.template_snapshot.target_path, 0)
        if not isinstance(destination, generated_model.GeneratedEntity):
            raise ValueError(f"Expected generated entity, got {destination}")
        destination.apply_generation(parsed)

    @staticmethod
    def create(
        template: template_model.GenerationTemplate,
        world: generated_model.GeneratedEntity,
    ) -> "Generation":
        specification = WORLD.get(template.target_path, 0)
        generation_variables = template_model.GenerationVariables.create(world)
        instruction_templates = template.get_instructions()
        filled_instructions = generation_variables.fill_instructions(instruction_templates)
        generate_json = True
        if generate_json:
            json_schema = template.create_json_schema()
            json_example = specification.create_example()
            json_structure = template_model.JsonStructure(
                json_schema=json_schema,
                example_str=json.dumps(json_example),
            )
            # TODO: This is actually only for openai...
            filled_instructions.append(
                template_model.FilledInstruction(
                    name="json-example",
                    message=f"Please format your response as JSON. For example:\n{json_example}"
                )
            )
        else:
            json_structure = None

        prompt_messages = [
            GenerationChatMessage(
                role=ChatRole.SYSTEM,
                message="You are a game developer, skilled in creating engaging, open-world plots full of suspense.",
            ),
            GenerationChatMessage(
                role=ChatRole.ASSISTANT,
                message="\n".join(instruction.message for instruction in filled_instructions),
            ),
        ]
        if template.additional_prompt:
            prompt_messages.append(GenerationChatMessage(
                role=ChatRole.USER,
                message=template.additional_prompt,
            ))
        return Generation(
            template_snapshot=template.model_copy(deep=True),
            filled_instructions=filled_instructions,
            json_structure=json_structure,
            prompt_messages=prompt_messages,
            status=GenerationStatus.QUEUED,
        )

