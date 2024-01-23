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
import cairne.commands.generate.base as base_generate_commands
from cairne.serve.data_store import Datastore


logger = get_logger()


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
    ) -> generate_model.OpenAIGenerationResult:
        kwargs = dict(
            model="gpt-3.5-turbo-1106",  # TODO: This is set on the generation
            messages=[
                self.translate_message(message)
                for message in generation.prompt_messages
            ],
            response_format={"type": "json_object"},
            temperature=generation.template_snapshot.parameters.temperature,
            seed=generation.template_snapshot.parameters.seed,
            max_tokens=generation.template_snapshot.parameters.max_tokens,
        )
        logger.info("Calling openai", kwargs=kwargs, generation=generation)

        start_time = datetime.datetime.now()
        from openai.types.chat.chat_completion import ChatCompletion

        if False:
            completion = typing.cast(ChatCompletion, self.client.chat.completions.create(**kwargs))  # type: ignore
            generation_time = datetime.datetime.now() - start_time

            finish_reason = completion.choices[0].finish_reason
            complete = completion.choices[0].finish_reason == "stop"
            content = completion.choices[0].message.content
            
            
            completion_tokens=completion.usage.completion_tokens,
            prompt_tokens=completion.usage.prompt_tokens,
            total_tokens=completion.usage.total_tokens,
        
            with open("output/reponses.txt", "a") as f:
                f.write(content + "\n")
        else:
            generation_time = datetime.timedelta(seconds=0)
            finish_reason = "stop"
            complete = True
            content = '{\n  "name": "Rhiannon Blackwood",\n  "faction": "cowboys",\n  "archetype": "explorer",\n  "gender": "female",\n  "description": "A sharpshooting outlaw known for her quick wit and daring heists.",\n  "appearance": "Tall and lean with raven-black hair and piercing green eyes. Wears a tattered leather duster and a wide-brimmed hat.",\n  "history": "Born into a family of cattle rustlers, Rhiannon learned to ride and shoot from a young age. After a conflict with a rival gang, she went solo, making a name for herself as the fastest draw in the West.",\n  "origin": "Grew up in the desolate Badlands, where she honed her survival skills and developed a fierce independence.",\n  "strengths": ["Deadly accuracy with a revolver", "Navigates the treacherous desert terrain with ease"],\n  "weaknesses": ["Stubborn and distrustful of others", "Haunted by a tragic event from her past"],\n  "fears": ["Betrayal by those she trusts", "Losing her freedom to the law"],\n  "goals": ["To uncover the truth behind her family\'s feud with a notorious outlaw gang", "Find a place where she can live without constantly looking over her shoulder"]\n}'
            
            completion_tokens=0
            prompt_tokens=0
            total_tokens=0
        
        generation.end_time = datetime.datetime.utcnow()
        
        # finish reason can be "stop" or hopefully not "length".
        logger.info(
            "Generated JSON:",
            generation_time=generation_time,
            finish_reason=finish_reason,
            content=content,
        )

        return generate_model.OpenAIGenerationResult(
            raw_text=content,
            validated=None,
            response=content,  # type: ignore
            completion_tokens=completion_tokens,
            prompt_tokens=prompt_tokens,
            total_tokens=total_tokens,
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


def run_openai_generation(data_store: Datastore, generation: generate_model.Generation):
    with base_generate_commands.generate_thread_entry(data_store, generation):
        try:
            logger.info("Running OpenAI generation", generation_id=generation.generation_id)
            generation.status = generate_model.GenerationStatus.IN_PROGRESS

            service = get_openai_service()

            result = service.generate_json(generation)
            base_generate_commands.parse_results(generation, result)

            # TODO: move this into the base class
            generation.end_time = datetime.datetime.utcnow()
            generation.status = generate_model.GenerationStatus.COMPLETE
            logger.info("Completed OpenAI generation", generation_id=generation.generation_id)
            data_store.save()
        except Exception as e:
            logger.exception(
                "Error running OpenAI generation",
                generation_id=generation.generation_id,
                exception=e,
            )
            generation.end_time = datetime.datetime.utcnow()
            generation.status = generate_model.GenerationStatus.ERROR
            raise
        


class OpenAIGenerate(base_generate_commands.BaseGenerate):
    def spawn_generation(self) -> None:
        # Should rate limit this somehow...
        # We need to remember this thread so we can cancel it later
        threading.Thread(target=run_openai_generation, args=(self.datastore, self.generation,)).start()


class Settings:
    TEMPERATURE = 0.5
    # MAX_TOKENS = 2000
    SEED = 1776
