import datetime
import typing
import uuid
from dataclasses import dataclass, field
from typing import (Any, Callable, Dict, List, Literal, Optional, Tuple, Type,
                    Union)

from pydantic import BaseModel, Field
from structlog import get_logger

import cairne.commands.export as export
import cairne.model.character as characters
import cairne.model.character as character_model
import cairne.model.generated as generated_model
import cairne.model.generation as generate_model
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

logger = get_logger()


@dataclass
class GenerationBuilder:
    user: str
    datastore: Datastore
    request: generate_schema.GenerateRequest = field()
    _world: Optional[generated_model.GeneratedEntity] = field(default=None)
    _entity: Optional[generated_model.GeneratedEntity] = field(default=None)
    _specification: Optional[spec.GeneratableSpecification] = field(default=None)
    _target_path: Optional[spec.GeneratablePath] = field(default=None)

    def get_world(self) -> generated_model.GeneratedEntity:
        if self._world is None:
            self._world = self.datastore.worlds.get(self.request.world_id, None)
            if self._world is None:
                raise ValueError(f"World '{self.request.world_id}' not found")
        return self._world

    def get_entity(self) -> generated_model.GeneratedEntity:
        if self._entity is None:
            located_entity = self.get_world().search_for_entity(
                self.request.entity_id,
                spec.GeneratablePath(path_elements=[]),
            )
            if located_entity is None:
                raise ValueError(f"Entity '{self.request.entity_id}' not found")
            self._target_path = located_entity.path
            self._entity = located_entity.entity
            self._specification = WORLD.get(located_entity.path, 0)
        return self._entity

    def get_specification(self) -> spec.GeneratableSpecification:
        if self._specification is None:
            self.get_entity()
        return self._specification  # type: ignore
    
    def get_target_path(self) -> spec.GeneratablePath:
        if self._target_path is None:
            self.get_entity()
        return self._target_path

    def create_json_structure(self) -> Optional[generate_model.JsonStructure]:
        fields = self.request.fields_to_generate
        if fields is not None and fields.all:
            logger.info("Should generate all fields")
            # fields = None

        json_structure_request = self.request.json_structure
        if json_structure_request is None or not json_structure_request.generate_json:
            return None

        if json_structure_request.json_schema is not None:
            schema = json_structure_request.json_schema
        else:
            schema = self.get_specification().create_schema()

        if json_structure_request.examples is not None:
            examples = json_structure_request.examples
        else:
            examples = self.get_specification().create_example()

        return generate_model.JsonStructure(
            json_schema=schema,
            examples=examples,
        )

    def create_parameters(self) -> generate_model.GenerationRequestParameters:
        requested_parameters = self.request.parameters
        default_parameters = generate_model.GenerationRequestParameters()
        if requested_parameters is None:
            return default_parameters

        if requested_parameters.seed is None:
            requested_parameters.seed = default_parameters.seed
        # if requested_parameters.top_p is None:
        #     requested_parameters.top_p = default_parameters.top_p
        # if requested_parameters.frequency_penalty is None:
        #     requested_parameters.frequency_penalty = default_parameters.frequency_penalty
        # if requested_parameters.presence_penalty is None:
        #     requested_parameters.presence_penalty = default_parameters.presence_penalty
        if requested_parameters.max_tokens is not None:
            default_parameters.max_tokens = requested_parameters.max_tokens
        else:
            # TODO: calculate max tokens
            pass
        if requested_parameters.temperature is None:
            default_parameters.temperature = requested_parameters.temperature
        if requested_parameters.seed is None:
            default_parameters.seed = requested_parameters.seed
        return default_parameters

    def create_prompt_messages(
        self, instructions: List[generate_model.Instruction]
    ) -> List[generate_model.GenerationChatMessage]:
        requested_messages = self.request.prompt_messages
        if requested_messages is not None:
            return requested_messages

        return [
            generate_model.GenerationChatMessage(
                role=generate_model.ChatRole.SYSTEM,
                message="You are a game developer, skilled in creating engaging, open-world plots full of suspense.",
            ),
            generate_model.GenerationChatMessage(
                role=generate_model.ChatRole.USER,
                message="\n".join(instruction.message for instruction in instructions),
            ),
        ]

    def create_generation_variables(self) -> generate_model.GenerationVariables:
        world = self.get_world()
        variables: Dict[str, str] = dict(
            possible_factions=", ".join(
                faction for faction in world_helpers.get_factions(world)
            ),
            possible_genders=", ".join(
                gender.value for gender in character_model.Gender
            ),
            possible_archetypes=", ".join(
                archetype.value for archetype in character_model.Archetype
            ),
            existing_characters=world_helpers.describe_existing_characters(world),
        )
        theme = world_helpers.get_theme(world)
        if theme is not None:
            variables["theme"] = theme
        character_counts = world_helpers.CharacterCounts.get_character_counts(world)

        # TODO: when we generate more than one character:
        generation_target = world_helpers.CharacterGenerationTarget(
            number_of_total_characters=20,
            number_of_characters_per_faction=4,
        )
        character_counts.format_count_instructions(generation_target)
        "Do not generate more than what is needed."

        return generate_model.GenerationVariables(variables=variables)

    def create_instructions(
        self,
        generation_variables: generate_model.GenerationVariables,
    ) -> List[generate_model.Instruction]:
        requested_instructions = self.request.instructions
        if requested_instructions is not None:
            instructions = requested_instructions
        else:
            instructions = [
                generate_model.Instruction(message=instruction)
                for instruction in self.get_specification().generation.instructions
            ]

        formatted = generation_variables.format(instructions)

        if True:  # TODO: Check if we are generating json
            example = self.get_specification().create_example()
            instruction = generate_model.Instruction(
                message=f"Please format your response as JSON. For example: {example}"
            )
            formatted.append(instruction)
        return formatted

    def create_generator_model(self) -> generate_model.GeneratorModel:
        requested_model = self.request.generator_model
        if requested_model is not None:
            return requested_model
        return generate_model.GeneratorModel(
            generator_type=generate_model.GeneratorType.OPENAI,
            g_model_id="gpt-3.5-turbo-1106",
        )

    def create_generation(self) -> generate_model.Generation:
        generation_variables = self.create_generation_variables()
        # Are there differences between instructions and prompt messages?
        instructions = self.create_instructions(generation_variables)
        prompt_messages = self.create_prompt_messages(instructions=instructions)
        json_structure = self.create_json_structure()
        parameters = self.create_parameters()
        generator_model = self.create_generator_model()

        return generate_model.Generation(
            generation_id=uuid.uuid4(),
            world_id=self.get_world().entity_id,
            entity_id=self.get_entity().entity_id,
            entity_type=self.get_entity().entity_type,
            generation_type=generate_model.GenerationType.TEXT,
            status=generate_model.GenerationStatus.QUEUED,
            generator_model=generator_model,
            json_structure=json_structure,
            prompt_messages=prompt_messages,
            input_tokens=None,
            output_tokens=None,
            parameters=parameters,
            begin_time=datetime.datetime.utcnow(),
            end_time=None,
            filled_instructions=instructions,
            generation_variables=generation_variables,
            target_path=self.get_target_path(),
        )

def parse_results(
    generation: generate_model.Generation,
    result: generate_model.BaseGenerationResult,
) -> None:
    context = parsing.ParseContext(source=generation.as_source())
    generated = parsing.parse(context, WORLD, raw=result.raw_text)
    result.parsed = generated
    generation.result = result


@dataclass
class BaseGenerate(Command):
    request: generate_schema.GenerateRequest
    generation: generate_model.Generation
    world: Optional[generated_model.GeneratedEntity] = Field(default=None)
    entity: Optional[generated_model.GeneratedEntity] = Field(default=None)
    specification: Optional[spec.GeneratableSpecification] = Field(default=None)

    def spawn_generation(self) -> threading.Thread:
        raise NotImplementedError()

    def execute(self) -> generate_schema.GenerateResponse:
        self.datastore.generations[self.generation.generation_id] = self.generation
        # self.datastore.save()

        thread = self.spawn_generation()
        self.datastore.generation_threads[self.generation.generation_id] = thread
        # TODO: Where is this removed? Maybe the thread should add itself with a context manager?
        self.datastore.save()

        return generate_schema.GenerateResponse(
            generation_id=self.generation.generation_id
        )
