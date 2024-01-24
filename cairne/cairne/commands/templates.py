import datetime
import typing
import uuid
from dataclasses import dataclass, field
from typing import (Any, Callable, Dict, List, Literal, Optional, Tuple, Type,
                    Union, Generator)

from pydantic import BaseModel, Field
from structlog import get_logger

import cairne.commands.export as export
import cairne.model.character as characters
import cairne.model.character as character_model
import cairne.model.generated as generated_model
import cairne.model.generation as generate_model
import cairne.model.templates as template_model
import cairne.model.specification as spec
import cairne.model.world as worlds
import cairne.openrpg.world_helpers as world_helpers
import cairne.schema.characters as characters_schema
import cairne.schema.generate as generate_schema
import cairne.schema.worlds as worlds_schema
from cairne.commands.base import Command
from cairne.model.world_spec import WORLD
from cairne.serve.data_store import Datastore
import cairne.model.parsing as parsing
import cairne.model.validation as validation
import threading
from contextlib import contextmanager
import cairne.schema.templates as templates_schema
import cairne.model.templates as templates_model

logger = get_logger()


@dataclass
class CreateTemplate(Command):
    request: templates_schema.CreateTemplateRequest

    def execute(self) -> templates_schema.CreateTemplateResponse:
        world = self.datastore.worlds.get(self.request.world_id, None)
        if not world:
            raise ValueError(f"World '{self.request.world_id}' not found")
        
        located_entity = world.search_for_entity(entity_id=self.request.entity_id, path=spec.GeneratablePath(path_elements=[]))
        if not located_entity:
            raise ValueError(f"Entity '{self.request.entity_id}' not found in world '{self.request.world_id}'")
        
        name = (
            self.request.name
            if self.request.name is not None
            else ("Unnamed Template " + datetime.datetime.now().strftime("%m%d%Y%H%M%S"))
        )
        generation_type = (
            self.request.generation_type
            if self.request.generation_type is not None
            else templates_model.GenerationType.TEXT
        )
        generator_model = (
            self.request.generator_model
            if self.request.generator_model is not None
            else templates_model.GeneratorModel(
                generator_type=templates_model.GeneratorType.OPENAI,
                g_model_id="gpt-3.5-turbo-1106",
            )
        )
        template = templates_model.GenerationTemplate(
            name=name,
            generation_type=generation_type,
            world_id=self.request.world_id,
            entity_id=self.request.entity_id,
            target_path=located_entity.path,
            entity_type=located_entity.entity.entity_type,
            generator_model=generator_model,
            parameters=templates_model.GenerationRequestParameters(),
            additional_prompt=None,
            excluded_instruction_names=[],
            fields_to_include=[],
            numbers_to_generate=[],
        )
        
        self.datastore.generation_templates[template.template_id] = template
        self.datastore.save()
        return templates_schema.CreateTemplateResponse(
            template_id=template.template_id
        )

@dataclass
class ListTemplates(Command):
    request: templates_schema.ListTemplatesQuery
    
    def execute(self) -> templates_schema.ListTemplatesResponse:
        templates = [
            export.export_template_list_item(template)
            for template in self.datastore.generation_templates.values()
            if template.deletion is None
            if self.request.world_id is None or template.world_id == self.request.world_id
            if self.request.entity_id is None or template.entity_id == self.request.entity_id
        ]
        return templates_schema.ListTemplatesResponse(templates=templates)


@dataclass
class UpdateTemplate(Command):
    request: templates_schema.UpdateTemplateRequest
    
    def execute(self) -> templates_schema.UpdateTemplateResponse:
        template = self.datastore.generation_templates.get(self.request.template_id, None)
        if not template:
            raise ValueError(f"Template '{self.request.template_id}' not found")
        
        if self.request.new_name is not None:
            template.name = self.request.new_name
        
        if self.request.generator_model is not None:
            self.request.generator_model.apply(template.generator_model)
        
        if self.request.include_fields is not None:
            template.fields_to_include.extend([
                templates_model.FieldToInclude(path=path)
                for path in self.request.include_fields
            ])
        
        if self.request.exclude_fields is not None:
            exclude_strings = set(
                path.as_str()
                for path in self.request.exclude_fields
            )
            template.fields_to_include = [
                field
                for field in template.fields_to_include
                if field.path.as_str() not in exclude_strings
            ]
            print("new fields to include", template.fields_to_include)
        
        if self.request.number_to_generate is not None:
            logger.info("TODO: Update number to generate")
        
        if self.request.instructions_to_include is not None:
            template.excluded_instruction_names = [
                instruction_name
                for instruction_name in template.excluded_instruction_names
                if instruction_name not in self.request.instructions_to_include
            ]
        
        if self.request.instructions_to_exclude is not None:
            template.excluded_instruction_names = list(set(
                template.excluded_instruction_names + self.request.instructions_to_exclude
            ))
        
        if self.request.prompt is not None:
            template.additional_prompt = self.request.prompt
        
        if self.request.parameter_updates is not None:
            self.request.parameter_updates.apply(template.parameters)
        
        self.datastore.save()
        
        return templates_schema.UpdateTemplateResponse()


@dataclass
class GetTemplate(Command):
    template_id: uuid.UUID

    def execute(self) -> templates_schema.GetTemplateResponse:
        template = self.datastore.generation_templates.get(self.template_id, None)
        if not template:
            raise ValueError(f"Template '{self.template_id}' not found")
        
        world = self.datastore.worlds.get(template.world_id, None)
        if not world:
            raise ValueError(f"World '{template.world_id}' not found")
        
        exported = export.export_template(template=template, world=world)
        return templates_schema.GetTemplateResponse(template=exported)


@dataclass
class DeleteTemplate(Command):
    template_id: uuid.UUID

    def spawn_generation(self) -> None:
        raise NotImplementedError()

    def execute(self) -> templates_schema.DeleteTemplateResponse:
        template = self.datastore.generation_templates.get(self.template_id, None)
        if not template:
            raise ValueError(f"Template '{self.template_id}' not found")
        
        template.deletion = generated_model.Deletion(
            date=datetime.datetime.utcnow(),
            deleted_by=self.user
        )
        self.datastore.save()

        return templates_schema.DeleteTemplateResponse()
