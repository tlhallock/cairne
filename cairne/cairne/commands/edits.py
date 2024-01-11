import datetime
import typing
import uuid
from dataclasses import dataclass, field
from typing import Optional, Tuple

import cairne.commands.export as export
import cairne.model.character as characters
import cairne.model.generated as generated_model
import cairne.model.parsing as parsing
import cairne.model.specification as spec
import cairne.schema.generated as generated_schema
from cairne.commands.base import Command
from cairne.model.world_spec import WORLD

# The world should probably have been seperate


@dataclass
class AppendValue(Command):
	request: generated_schema.CreateEntityRequest

	def execute(self) -> generated_schema.CreateEntityResponse:
		raise NotImplementedError()
		# if self.request.entity_type == spec.EntityType.WORLD:
		#     raise ValueError("Cannot create a world, use CreateWorld instead")

		# specification = self.request.entity_type.get_specification()
		# context = parsing.ParseContext(source=generated_model.GenerationSource(source_type=generated_model.GenerationSourceType.DEFAULT_VALUE))
		# generated = parsing.parse(context, specification, raw = None)
		# entity = typing.cast(generated_model.GeneratedEntity, generated)

		# world = self.datastore.worlds.get(self.request.world_id, None)
		# if world is None:
		#     raise ValueError(f"World not found: {self.request.world_id}")
		# entity_dictionary = typing.cast(generated_model.EntityDictionary, world.get(insert_path, 0))
		# entity_dictionary.entities[entity.entity_id] = entity

		# insert_path = self.request.entity_type.get_dictionary_path()
		# child_path = insert_path.append(generated_model.GeneratablePathElement(entity.entity_id))
		# self.datastore.save()

		# response = generated_schema.CreateEntityResponse(entity_id=entity.entity_id, path=child_path)
		# return response


@dataclass
class ReplaceValue(Command):
	request: generated_schema.ListEntitiesRequest

	def execute(self) -> generated_schema.ListEntitiesResponse:
		# world = self.datastore.worlds.get(self.request.world_id, None)
		raise NotImplementedError()
		# if world is None:
		#     raise ValueError(f"World not found: {self.request.world_id}")
		# path = self.request.entity_type.get_dictionary_path()
		# entity_dictionary = typing.cast(generated_model.EntityDictionary, world.get(path, 0))

		# entities = [
		#     export.export_generated_entity_item(
		#         path=path.append(generated_model.GeneratablePathElement(entity_id=entity.entity_id)),
		#         generated_entity=entity
		#     )
		#     for entity in entity_dictionary.entities.values()
		# ]

		# response = generated_schema.ListEntitiesResponse(entities=entities)
		# return response


@dataclass
class RemoveValue(Command):
	request: generated_schema.DeleteEntityRequest

	def execute(self) -> generated_schema.DeleteEntityResponse:
		raise NotImplementedError()
		# world = self.datastore.worlds.get(self.request.world_id, None)
		# if world is None:
		#     raise ValueError(f"World not found: {self.request.world_id}")

		# located_entity = world.search_for_entity(self.request.entity_id, path=generated_model.GeneratablePath(path_elements=[]))
		# if located_entity is None:
		#     raise ValueError(f"Entity not found: {self.request.entity_id}")

		# located_entity.entity.deletion = generated_model.Deletion(
		#     date=datetime.datetime.now(),
		#     deleted_by="test",
		# )
		# self.datastore.save()

		# return generated_schema.DeleteEntityResponse()