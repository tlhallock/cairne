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
import cairne.schema.worlds as worlds_schema
from cairne.commands.base import Command
from cairne.model.world_spec import WORLD

# The world should probably have been seperate


@dataclass
class CreateWorld(Command):
	request: worlds_schema.CreateWorldRequest

	def execute(self) -> generated_schema.CreateEntityResponse:
		context = parsing.ParseContext(
			source=generated_model.GenerationSource(
				source_type=generated_model.GenerationSourceType.DEFAULT_VALUE
			)
		)
		generated = parsing.parse(context, WORLD, raw={"name": self.request.name})
		entity = typing.cast(generated_model.GeneratedEntity, generated)
		self.datastore.worlds[entity.entity_id] = entity
		child_path = spec.GeneratablePath(path_elements=[])
		self.datastore.save()

		response = generated_schema.CreateEntityResponse(
			entity_id=entity.entity_id, path=child_path
		)
		return response


@dataclass
class ListWorlds(Command):
	def execute(self) -> generated_schema.ListEntitiesResponse:
		entities = [
			export.export_generated_entity_item(
				path=spec.GeneratablePath(path_elements=[]),
				generated_entity=world,
			)
			for world in self.datastore.worlds.values()
		]
		response = generated_schema.ListEntitiesResponse(entities=entities)
		return response


@dataclass
class GetWorld(Command):
	world_id: uuid.UUID

	def execute(self) -> generated_schema.GetEntityResponse:
		world_uuid = self.world_id
		world = self.datastore.worlds.get(world_uuid, None)
		if world is None:
			raise ValueError(f"World not found: {self.world_id}")
		exported = export.export_generated_entity(
			path=spec.GeneratablePath(path_elements=[]),
			generated_entity=world,
		)
		return generated_schema.GetEntityResponse(entity=exported)


@dataclass
class DeleteWorld(Command):
	world_id: uuid.UUID

	def execute(self) -> generated_schema.DeleteEntityResponse:
		world_uuid = self.world_id

		deleted_world = self.datastore.worlds.get(world_uuid, None)
		if deleted_world is None:
			raise ValueError(f"World not found: {world_uuid}")

		deleted_world.deletion = generated_model.Deletion(
			date=datetime.datetime.now(),
			deleted_by=self.user,
		)
		self.datastore.worlds.pop(world_uuid, None)
		self.datastore.save()

		return generated_schema.DeleteEntityResponse()
