import datetime
import json
import string
import typing
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field
from structlog import get_logger

import cairne.model.calls as calls
import cairne.model.generated as generated_model
import cairne.model.specification as spec
import cairne.parsing.parse_incomplete_json as parse_incomplete


logger = get_logger(__name__)


def get_factions(world: generated_model.GeneratedEntity) -> List[str]:
    factions_list = typing.cast(generated_model.GeneratedList, world.children["factions"])
    factions: List[str] = []
    for faction in factions_list.elements:
        if not isinstance(faction, generated_model.GeneratedString):
            logger.warning(
                "Unexpected type of faction to be string",
                type=type(faction),
                faction=faction,
            )
            continue
        if faction.parsed is None:
            continue
        factions.append(faction.parsed)
    return factions


def get_theme(world: generated_model.GeneratedEntity) -> Optional[str]:
    generated_theme = typing.cast(
        generated_model.GeneratedString, world.children["theme"]
    )
    return generated_theme.parsed


def describe_existing_characters(world: generated_model.GeneratedEntity) -> str:
    result = []
    characters_dict = typing.cast(
        generated_model.EntityDictionary, world.children["characters"]
    )
    for incomplete in characters_dict.entities.values():
        generated_name = typing.cast(
            generated_model.GeneratedString, incomplete.children["name"]
        )
        generated_faction = typing.cast(
            generated_model.GeneratedString, incomplete.children["faction"]
        )
        name = (
            generated_name.parsed
            if generated_name.parsed is not None
            else f"Unnamed character ({incomplete.entity_id})"
        )
        if generated_faction.parsed is None:
            result.append(f"{name} has no faction yet")
            continue

        result.append(f"{name} has faction {generated_faction.parsed}")
    return ", ".join(result)


class CharacterGenerationTarget(BaseModel):
    number_of_total_characters: int = Field(default=20)
    number_of_characters_per_faction: int = Field(default=4)


class CharacterCounts(BaseModel):
    total: int = Field(default=0)
    per_faction: Dict[str, int]

    def as_content(self) -> str:
        content = []
        for key, value in self.per_faction.items():
            content.append(f"There are {value} characters in the faction {key}\n")
        content.append(f"There are a total of {self.total} characters in the world.")
        return "".join(content)

    def as_raw(self) -> Dict[str, Any]:
        return self.model_dump()

    def format_count_instructions(self, target: CharacterGenerationTarget) -> List[str]:
        instructions = []
        for faction, count in self.per_faction.items():
            if count < target.number_of_characters_per_faction:
                remaining = target.number_of_characters_per_faction - count
                # could just take abs value?
                instructions.append(
                    f"You need to create {remaining} more characters of faction {faction}."
                )
            else:
                instructions.append(
                    f"You do not have to create any more characters for faction {faction}."
                )

        target_total = target.number_of_total_characters - self.total
        if target_total > 0:
            instructions.append(
                f"You need to generate at least {target_total} more characters in total."
            )
        return instructions

    def get_incomplete_faction_names(
        self, target: CharacterGenerationTarget
    ) -> List[str]:
        result = []
        for faction, count in self.per_faction.items():
            if count < target.number_of_characters_per_faction:
                result.append(faction)
        return result

    @staticmethod
    def get_character_counts(
        world: generated_model.GeneratedEntity,
    ) -> "CharacterCounts":
        factions = get_factions(world)
        ret = CharacterCounts(per_faction={faction: 0 for faction in factions})

        characters = typing.cast(generated_model.EntityDictionary, world.children["characters"])
        for incomplete in characters.entities.values():
            if not isinstance(incomplete, generated_model.GeneratedEntity):
                logger.warning(
                    "Unexpected type of incomplete character to be an entity",
                    type=type(incomplete),
                    incomplete=incomplete,
                )
                continue
            ret.total += 1
            faction = incomplete.children["faction"]
            if not isinstance(faction, generated_model.GeneratedString):
                logger.warning(
                    "Unexpected type of faction to be string",
                    type=type(faction),
                    faction=faction,
                )
                continue
            if faction.parsed is None:
                continue
            if faction.parsed not in factions:
                continue
            ret.per_faction[faction.parsed] += 1
        return ret
