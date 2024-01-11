
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import datetime
import uuid
import cairne.model.generated as generated
from cairne.schema.base import Response
from enum import Enum
import cairne.model.generation as generation_model



# class GenerationProgress(BaseModel):
#     generation_id: uuid.UUID = Field()
#     begin_time: datetime.datetime = Field()
#     end_time: Optional[datetime.datetime] = Field()
#     status: GenerationStatus = Field()
#     # mean_duration: datetime.timedelta = Field(..., description="Mean duration of generation")



# class GenerationResult(BaseModel):
#     generation_id: uuid.UUID = Field()
#     begin_time: datetime.datetime = Field()
#     end_time: datetime.datetime = Field()
#     prompt: str = Field()  # could be a list of messages...
#     raw_text: str = Field()
    
#     json_text: Optional[str] = Field()
#     completed_json: Optional[str] = Field()
#     # options: List[GeneratedItem] = Field(default_factory=list)
#     # parsed: "Generatable" = Field()



# class GenerationTargetPath(BaseModel):
#     generatable_id: uuid.UUID = Field()
#     field: str = Field()


class GenerateRequest(BaseModel):
    generation_endpoint: generation_model.GenerationEndpoint = Field()
    entity_to_generate: Optional[uuid.UUID] = Field(default=None)
    generator_model: generation_model.GeneratorModel = Field(default_factory=lambda: generation_model.GeneratorModel(
        generator_type=generation_model.GeneratorType.OPENAI,
        g_model_id="gpt3-turbo",
    ))
    
    # model to use...
    # fields to generate...
    # validations to fix
    # reveal previous, instructions from previous
    # instructions/prompt/temperature/etc


class GenerateResponse(Response):
    generation_id: uuid.UUID = Field()


class GenerationListItem(BaseModel):
    generation_id: uuid.UUID = Field()
    begin_time: datetime.datetime = Field()
    end_time: Optional[datetime.datetime] = Field()
    status: generation_model.GenerationStatus = Field()
    

class ListGenerationsResponse(Response):
    generations: List[GenerationListItem] = Field(default_factory=list)


class GetGenerationResponse(Response):
    generation: generation_model.Generation = Field()


class CancelGenerationRequest(BaseModel):
    generation_id: uuid.UUID = Field()


class CancelGenerationResponse(Response):
    generation_id: uuid.UUID = Field()


class ApplyGenerationRequest(BaseModel):
    generation_id: uuid.UUID = Field()


class ApplyGenerationResponse(Response):
    generation_id: uuid.UUID = Field()

