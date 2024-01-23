
import uuid
from dataclasses import dataclass, field

import cairne.commands.export as export
import cairne.schema.generate as generate_schema
from cairne.commands.base import Command
from cairne.model.world_spec import WORLD
import cairne.model.generated as generated_model
from typing import Optional
import datetime


@dataclass
class ListGenerations(Command):
    request: generate_schema.ListGenerationsQuery
    
    def execute(self) -> generate_schema.ListGenerationsResponse:
        generations = []
        for generation in self.datastore.generations.values():
            if generation.deletion is not None:
                continue
            if not self.request.includes(generation):
                continue
            generations.append(export.export_generation_list_item(generation))
        return generate_schema.ListGenerationsResponse(generations=generations)


@dataclass
class GetGeneration(Command):
    generation_id: uuid.UUID

    def execute(self) -> generate_schema.GetGenerationResponse:
        generation = self.datastore.generations.get(self.generation_id, None)
        if generation is None:
            raise ValueError(f"Generation not found: {self.generation_id}")
        world = self.datastore.worlds.get(generation.template_snapshot.world_id, None)
        if world is None:
            raise ValueError(f"World not found: {generation.template_snapshot.world_id}")

        exported = export.export_generation(generation, world)
        return generate_schema.GetGenerationResponse(generation=exported)


@dataclass
class CancelGeneration(Command):
    request: generate_schema.CancelGenerationRequest

    def execute(self) -> generate_schema.CancelGenerationResponse:
        raise NotImplementedError()
        # world = self.datastore.worlds.get(self.request.world_id, None)
        # if world is None:
        #     raise ValueError(f"World not found: {self.request.world_id}")

        # character = world.characters.get(self.request.character_id, None)
        # if character is None:
        #     raise ValueError(f"Character not found: {self.request.character_id}")

        # exported = export.export_character(character)
        # return generate_schema.GetCharacterResponse(character=exported)


@dataclass
class ApplyGeneration(Command):
    request: generate_schema.ApplyGenerationRequest

    def execute(self) -> generate_schema.ApplyGenerationResponse:
        raise NotImplementedError()
        # world = self.datastore.worlds.get(self.request.world_id, None)
        # if world is None:
        #     raise ValueError(f"World not found: {self.request.world_id}")

        # character = world.characters.get(self.request.character_id, None)
        # if character is None:
        #     raise ValueError(f"Character not found: {self.request.character_id}")

        # exported = export.export_character(character)
        # return generate_schema.ApplyGenerationResponse(character=exported)


# @dataclass
# class GetEntitySchema(Command):
#     entity_type: spec.EntityType

#     def execute(self) -> generated_schema.GetEntitySchemaResponse:
#         entity_specification = self.entity_type.get_specification()
#         schema = export.export_entity_specification(entity_specification)
#         return generated_schema.GetEntitySchemaResponse(schema=schema)

@dataclass
class DeleteGeneration(Command):
    generation_id: uuid.UUID
    
    def execute(self) -> generate_schema.DeleteGenerationResponse:
        generation = self.datastore.generations.pop(self.generation_id, None)
        if generation is None:
            raise ValueError(f"Generation not found: {self.generation_id}")
        generation.deletion = generated_model.Deletion(
            date=datetime.datetime.utcnow(),
            deleted_by=self.user,
        )
        return generate_schema.DeleteGenerationResponse()