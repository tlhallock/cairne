import datetime
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

import cairne.model.generated as generated_model
import cairne.model.generation as generation_model
import cairne.model.specification as spec
from cairne.schema.base import Response

# class GenerationProgress(BaseModel):
#     generation_id: uuid.UUID = Field()
#     begin_time: datetime.datetime = Field()
#     end_time: Optional[datetime.datetime] = Field()
#     status: GenerationStatus = Field()
#     # mean_duration: datetime.timedelta = Field(..., description="Mean duration of generation")





class GenerationListItem(BaseModel):
    generation_id: uuid.UUID = Field()
    begin_time: datetime.datetime = Field()
    end_time: Optional[datetime.datetime] = Field()
    status: generation_model.GenerationStatus = Field()


# class GenerationTargetPath(BaseModel):
#     generatable_id: uuid.UUID = Field()
#     field: str = Field()




class GenerationResult(BaseModel):
    raw_text: str = Field()
    validated: generated_model.Generated = Field()


class Generation(BaseModel):
    generation_id: uuid.UUID = Field()
    world_id: uuid.UUID = Field()
    entity_id: uuid.UUID = Field()
    entity_type: spec.EntityType = Field()
    target_path: spec.GeneratablePath = Field()

    begin_time: datetime.datetime = Field()
    end_time: Optional[datetime.datetime] = Field()
    status: generation_model.GenerationStatus = Field()

    result: Optional[GenerationResult] = Field(default=None)


class JsonStructureRequest(BaseModel):
    generate_json: bool = Field(default=True)
    json_schema: Optional[str] = Field(default=None)
    examples: Optional[str] = Field(default=None)


class GenerateRequest(BaseModel):
    # is this required?
    # generation_endpoint: generation_model.GenerationEndpoint = Field()

    world_id: uuid.UUID = Field()
    entity_id: uuid.UUID = Field(default=None)
    fields_to_generate: Optional[generation_model.TargetFields] = Field(default=None)

    generator_model: Optional[generation_model.GeneratorModel] = Field(default=None)
    parameters: Optional[generation_model.GenerationRequestParameters] = Field(
        default=None
    )

    prompt_messages: Optional[List[generation_model.GenerationChatMessage]] = Field(
        default=None
    )
    instructions: Optional[List[generation_model.Instruction]] = Field(default=None)
    json_structure: Optional[JsonStructureRequest] = Field(default=None)

    # validations to fix
    # reveal previous, instructions from previous
    # instructions/prompt/temperature/etc

    # generator_model: generation_model.GeneratorModel = Field(
    # 	default_factory=lambda: generation_model.GeneratorModel(
    # 		generator_type=generation_model.GeneratorType.OPENAI,
    # 		g_model_id="gpt3-turbo",
    # 	)
    # )


class GenerateResponse(Response):
    generation_id: uuid.UUID = Field()


class ListGenerationsResponse(Response):
    generations: List[GenerationListItem] = Field(default_factory=list)


class GetGenerationResponse(Response):
    generation: Generation = Field()


class CancelGenerationRequest(BaseModel):
    generation_id: uuid.UUID = Field()


class CancelGenerationResponse(Response):
    generation_id: uuid.UUID = Field()


class ApplyGenerationRequest(BaseModel):
    generation_id: uuid.UUID = Field()


class ApplyGenerationResponse(Response):
    generation_id: uuid.UUID = Field()
