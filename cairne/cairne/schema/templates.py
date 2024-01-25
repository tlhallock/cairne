import datetime
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

import cairne.model.generated as generated_model
import cairne.model.generation as generation_model
import cairne.schema.worlds as world_schema
import cairne.model.specification as spec
from cairne.schema.base import Response
import cairne.model.templates as template_model


class TemplateListItem(BaseModel):
    template_id: uuid.UUID = Field()
    name: str = Field()
    entity_id: uuid.UUID = Field()
    world_id: uuid.UUID = Field()
    generation_type: template_model.GenerationType = Field()
    entity_type: world_schema.EntityTypeView = Field()
    created_at: datetime.datetime = Field()
    updated_at: datetime.datetime = Field()


class InstructionView(BaseModel):
    name: str = Field()
    label: str = Field()
    preview: str = Field()
    valid: bool = Field()
    included: bool = Field(default=True)
    

class ValidationPreview(BaseModel):
    name: str = Field()
    label: str = Field()
    preview: str = Field()
    valid: bool = Field()
    included: bool = Field(default=True)


class GenerationTemplateView(BaseModel):
    template_id: uuid.UUID = Field()
    name: str = Field()
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    world_id: uuid.UUID = Field()
    entity_id: uuid.UUID = Field()
    target_path: spec.GeneratablePath = Field()
    entity_type: spec.EntityType = Field()
    generation_type: template_model.GenerationType = Field()
    generator_model: template_model.GeneratorModel = Field()
    
    prompt: Optional[str] = Field(default=None)
    
    parameters: template_model.GenerationRequestParameters = Field(
        default_factory=template_model.GenerationRequestParameters
    )
    instructions: List[InstructionView] = Field(default_factory=list)
    json_structure_preview: Optional[str] = Field(default=None)
    
    fields_to_include: List[spec.GeneratablePath] = Field(default_factory=list)
    validations_to_include: List[ValidationPreview] = Field(default_factory=list)


class CreateTemplateRequest(BaseModel):
    name: Optional[str] = Field()

    world_id: uuid.UUID = Field()
    entity_id: uuid.UUID = Field()
    generator_model: Optional[template_model.GeneratorModel] = Field(default=None)
    generation_type: Optional[template_model.GenerationType] = Field()


class CreateTemplateResponse(Response):
    template_id: uuid.UUID = Field()


class GetTemplateResponse(Response):
    template: GenerationTemplateView = Field()


class NumberToGenerate(BaseModel):
    # None indicates to remove it
    number_to_generate: Optional[int] = Field(default=None)
    path: spec.GeneratablePath = Field()


class GenerationRequestParameterUpdates(BaseModel):
    new_values: Optional[template_model.GenerationRequestParameters] = Field(default=None)
    parameters_to_remove: Optional[List[str]] = Field(default=None)
    
    def apply(self, parameters: template_model.GenerationRequestParameters) -> None:
        if self.new_values:
            parameters.update_from(self.new_values)
        if self.parameters_to_remove:
            parameters.remove_parameters(self.parameters_to_remove)


class GeneratorModelUpdates(BaseModel):
    generator_type: Optional[template_model.GeneratorType] = Field(default=None)
    g_model_id: Optional[str] = Field(default=None)
    
    def apply(self, generator_model: template_model.GeneratorModel) -> None:
        if self.generator_type is not None:
            generator_model.generator_type = self.generator_type
            generator_model.g_model_id = self.generator_type.get_default_model()
        if self.g_model_id is None:
            return
        if self.g_model_id not in generator_model.generator_type.get_models():
            raise ValueError(
                f"Model '{self.g_model_id}' not found for generator type "
                f"'{generator_model.generator_type}'. Available models: "
                f"{generator_model.generator_type.get_models()}"
            )
        generator_model.g_model_id = self.g_model_id


class UpdateTemplateRequest(BaseModel):
    template_id: uuid.UUID = Field()
    
    new_name: Optional[str] = Field()
    generator_model: Optional[GeneratorModelUpdates] = Field()
    include_fields: Optional[List[spec.GeneratablePath]] = Field(default_factory=None)
    exclude_fields: Optional[List[spec.GeneratablePath]] = Field(default_factory=None)
    number_to_generate: Optional[List[NumberToGenerate]] = Field(default_factory=None)
    instructions_to_include: Optional[List[str]] = Field(default_factory=None)
    instructions_to_exclude: Optional[List[str]] = Field(default_factory=None)
    prompt: Optional[str] = Field(default=None)
    parameter_updates: Optional[GenerationRequestParameterUpdates] = Field(default=None)


class UpdateTemplateResponse(Response):
    pass


class ListTemplatesQuery(BaseModel):
    world_id: Optional[uuid.UUID] = Field(default=None)
    entity_id: Optional[uuid.UUID] = Field(default=None)
    entity_type: Optional[spec.EntityType] = Field(default=None)


class ListTemplatesResponse(Response):
    templates: List[TemplateListItem] = Field(default_factory=list)


class DeleteTemplateRequest(BaseModel):
    template_id: uuid.UUID = Field()


class DeleteTemplateResponse(Response):
    pass
