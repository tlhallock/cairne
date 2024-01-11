import datetime
import uuid
from dataclasses import dataclass, field
from typing import Optional

import cairne.commands.export as export
import cairne.model.character as characters
import cairne.model.generation as generation_model
import cairne.model.world as worlds
import cairne.schema.characters as characters_schema
import cairne.schema.generate as generate_schema
import cairne.schema.worlds as worlds_schema
from cairne.commands.base import Command


def create_character_generation(
	request: generate_schema.GenerateRequest,
) -> generation_model.Generation:
	return generation_model.Generation(
		generation_id=uuid.uuid4(),
		endpoint=request.generation_endpoint,
		generation_type=generation_model.GenerationType.TEXT,
		generator_model=request.generator_model,
		begin_time=datetime.datetime.utcnow(),
		end_time=None,
		# status=generation_model.GenerationStatus.QUEUED,
		# prompt_messages=[],
		# json_schema=None,
		# parameters=generation_model.GenerationRequestParameters(),
	)


def create_characters_generation(
	request: generate_schema.GenerateRequest,
) -> generation_model.Generation:
	raise NotImplementedError()
	# return generation_model.Generation(
	#     generation_type=request.generation_type,

	# generation_type: GenerationType = Field()
	# generator_model: GeneratorModel = Field()
	# # request...

	# begin_time: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
	# end_time: Optional[datetime.datetime] = Field(default=None)
	# status: GenerationStatus = Field(default=GenerationStatus.QUEUED)

	# # assumes a chat model...
	# prompt_messages: List[GenerationMessage] = Field(default_factory=list)
	# json_schema: Optional[str] = Field(default=None)

	# parameters: GenerationRequestParameters = Field(default_factory=GenerationRequestParameters)
	# input_tokens: int = Field()
	# output_tokens: int = Field()
	# )


def create_generation(
	request: generate_schema.GenerateRequest,
) -> generation_model.Generation:
	if request.generation_endpoint == generation_model.GenerationEndpoint.CHARACTER:
		generation = create_character_generation(request)
	elif request.generation_endpoint == generation_model.GenerationEndpoint.CHARACTERS:
		generation = create_characters_generation(request)
	else:
		raise ValueError(f"Invalid generation endpoint: {request.generation_endpoint}")

	# TODO: run the generation...

	return generation


@dataclass
class Generate(Command):
	request: generate_schema.GenerateRequest

	def execute(self) -> generate_schema.GenerateResponse:
		raise NotImplementedError()
		# generation = create_generation(self.request)

		# generation = generation_model.Generation(
		#     generation_type=self.request.generation_type,
		#     generated_entity_id=self.request.generated_entity_id,
		# )

		# world = self.datastore.worlds.get(self.request.world_id, None)
		# if world is None:
		#     raise ValueError(f"World not found: {self.request.world_id}")

		# character = characters.Character()
		# world.characters[character.generatable_id] = character

		# self.datastore.save()

		# response = generate_schema.GenerateResponse(character_id=character.generatable_id)
		# return response


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
