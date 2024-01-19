import datetime
import json
import sys
import threading
import typing
import uuid
from dataclasses import dataclass, field
from typing import (Any, Callable, Dict, List, Literal, Optional, Tuple, Type,
                    Union)

import openai
from pydantic import BaseModel, Field
from structlog import get_logger

import cairne.commands.export as export
import cairne.model.character as characters
import cairne.model.generated as generated_model
import cairne.model.generation as generate_model
import cairne.model.generation as generation_model
import cairne.model.specification as spec
import cairne.model.world as worlds
import cairne.schema.characters as characters_schema
import cairne.schema.generate as generate_schema
import cairne.schema.worlds as worlds_schema
from cairne.commands.base import Command
from cairne.commands.generate.base import BaseGenerate

logger = get_logger()


class OpenAIGenerationResult(BaseModel):
    response: str = Field()
    input_tokens: int = Field()
    output_tokens: int = Field()
    time_taken: datetime.timedelta = Field()
    finish_reason: str = Field()


class OpenAIService:
    client: openai.OpenAI
    last_call_time: Optional[datetime.datetime] = None

    @classmethod
    def translate_message(
        cls, message: generate_model.GenerationChatMessage
    ) -> Dict[str, Any]:
        return {
            "role": message.role.value,
            "content": message.message,
        }

    def generate_json(
        self, generation: generate_model.Generation
    ) -> OpenAIGenerationResult:
        kwargs = dict(
            model="gpt-3.5-turbo-1106",  # TODO: This is set on the generation
            messages=[
                self.translate_message(message)
                for message in generation.prompt_messages
            ],
            response_format={"type": "json_object"},
            temperature=generation.parameters.temperature,
            seed=generation.parameters.seed,
            max_tokens=generation.parameters.max_tokens,
        )
        logger.info("Calling openai", kwargs=kwargs, generation=generation)
        import ipdb

        ipdb.set_trace()

        start_time = datetime.datetime.now()
        from openai.types.chat.chat_completion import ChatCompletion

        completion = typing.cast(ChatCompletion, self.client.chat.completions.create(**kwargs))  # type: ignore
        generation_time = datetime.datetime.now() - start_time

        finish_reason = completion.choices[0].finish_reason
        complete = completion.choices[0].finish_reason == "stop"
        content = completion.choices[0].message.content

        logger.info(
            "Generated JSON:",
            generation_time=generation_time,
            finish_reason=finish_reason,
            content=content,
        )
        # TODO: add generation results...

        # finish reason can be "stop" or hopefully not "length".
        # record used tokens
        return OpenAIGenerationResult(
            response=content,  # type: ignore
            input_tokens=0,  # TODO
            output_tokens=0,  # TODO
            time_taken=generation_time,
            finish_reason=finish_reason,
        )


openai_service: Optional[OpenAIService] = None


def get_openai_service() -> OpenAIService:
    global openai_service
    if openai_service is not None:
        return openai_service
    service = OpenAIService()
    service.client = openai.OpenAI()
    openai_service = service
    return service


def run_openai_generation(generation: generate_model.Generation):
    try:
        logger.info("Running OpenAI generation", generation_id=generation.generation_id)
        generation.status = generate_model.GenerationStatus.IN_PROGRESS

        service = get_openai_service()

        result = service.generate_json(generation)
        # TODO: parse the results...

        generation.end_time = datetime.datetime.utcnow()
        generation.status = generate_model.GenerationStatus.COMPLETE
        logger.info(
            "Completed OpenAI generation", generation_id=generation.generation_id
        )
    except Exception as e:
        logger.exception(
            "Error running OpenAI generation",
            generation_id=generation.generation_id,
            excepttion=e,
        )
        generation.status = generate_model.GenerationStatus.ERROR
        generation.end_time = datetime.datetime.utcnow()
        raise


class OpenAIGenerate(BaseGenerate):
    def spawn_generation(self) -> None:
        # Should rate limit this somehow...
        # We need to remember this thread so we can cancel it later
        threading.Thread(target=run_openai_generation, args=(self.generation,)).start()


# class InstructionGenerationContext:
#     generation_state: state.GenerationState
#     incomplete_entity: Optional[spec.IncompleteGeneration]
#     # include validation errors?


# class GenerationSpecification(BaseModel):
#     instructions: List[Callable[[InstructionGenerationContext], List[str]]]
#     initial_example: Dict[str, Any]
#     complete_example: Dict[str, Any]


class Settings:
    TEMPERATURE = 0.5
    # MAX_TOKENS = 2000
    SEED = 1776
