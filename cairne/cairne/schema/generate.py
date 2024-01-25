import datetime
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

import cairne.model.generated as generated_model
import cairne.model.generation as generation_model
import cairne.model.templates as template_model
import cairne.model.specification as spec
from cairne.schema.base import Response
import cairne.schema.templates as template_schema

# class GenerationProgress(BaseModel):
#     generation_id: uuid.UUID = Field()
#     begin_time: datetime.datetime = Field()
#     end_time: Optional[datetime.datetime] = Field()
#     status: GenerationStatus = Field()
#     # mean_duration: datetime.timedelta = Field(..., description="Mean duration of generation")


class GenerateModelChoice(BaseModel):
    label: str = Field()
    value: template_model.GeneratorType = Field()
    defaultModel: str = Field()
    models: List[str] = Field()
    
    @classmethod
    def from_model(cls, model: template_model.GeneratorType) -> 'GenerateModelChoice':
        return cls(
            label=model.get_label(),
            value=model.value,
            defaultModel=model.get_default_model(),
            models=model.get_models(),
        )


class ApplyGenerationType(str, Enum):
    REPLACE = "replace"
    APPEND = "append"


class GenerationApplicationOption(BaseModel):
    label: str = Field()
    source: generated_model.GenerationSource = Field()
    path: spec.GeneratablePath = Field()
    application_type: ApplyGenerationType = Field()
    children: List['GenerationApplicationOption'] = Field(default_factory=list)
    
    addToAdderFields: str = Field(default=None)


class GenerationListItem(BaseModel):
    generation_id: uuid.UUID = Field()
    label: str = Field()
    begin_time: datetime.datetime = Field()
    end_time: Optional[datetime.datetime] = Field()
    status: generation_model.GenerationStatus = Field()


class GenerationView(BaseModel):
    generation_id: uuid.UUID = Field()
    template: template_schema.GenerationTemplateView = Field()

    begin_time: datetime.datetime = Field()
    end_time: Optional[datetime.datetime] = Field()
    status: generation_model.GenerationStatus = Field()
    raw_generated_text: Optional[str] = Field()


class JsonStructureRequest(BaseModel):
    generate_json: bool = Field(default=True)
    json_schema: Optional[str] = Field(default=None)
    examples: Optional[str] = Field(default=None)


class GenerateRequest(BaseModel):
    template_id: uuid.UUID = Field()
    target_entity_id: Optional[uuid.UUID] = Field(default=None)


class GenerateResponse(Response):
    generation_id: uuid.UUID = Field()


class ListGenerationsResponse(Response):
    generations: List[GenerationListItem] = Field(default_factory=list)


class GetGenerationResponse(Response):
    generation: GenerationView = Field()


class CancelGenerationRequest(BaseModel):
    generation_id: uuid.UUID = Field()


class CancelGenerationResponse(Response):
    generation_id: uuid.UUID = Field()


class DeleteGenerationResponse(Response):
    pass


class ApplyGenerationRequest(BaseModel):
    generation_id: uuid.UUID = Field()


class ApplyGenerationResponse(Response):
    generation_id: uuid.UUID = Field()


# TODO: rename this to reponse
class ListGenerationModels(Response):
    default_generator_type: template_model.GeneratorType = Field(default_factory=lambda: template_model.GeneratorType.OPENAI)
    models: List[GenerateModelChoice] = Field(default_factory=lambda: [
        GenerateModelChoice.from_model(
            template_model.GeneratorType.OPENAI
        ),
        GenerateModelChoice.from_model(
            template_model.GeneratorType.HUGGING_FACE
        ),
        GenerateModelChoice.from_model(
            template_model.GeneratorType.OLLAMA
        ),
    ])


class ListGenerationsQuery(BaseModel):
    entity_id: Optional[uuid.UUID] = None
    
    def includes(self, generation: generation_model.Generation) -> bool:
        if self.entity_id is None:
            return True
        return generation.template_snapshot.entity_id == self.entity_id
