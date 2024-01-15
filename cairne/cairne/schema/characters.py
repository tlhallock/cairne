import datetime
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

import cairne.model.generated as generated
from cairne.schema.base import Response

# class GenerationStateField(BaseModel):
#     name: str
#     value: Union[str, int, float, bool, None]


# class ObjectGenerationState(BaseModel):
#     generatable_id: uuid.UUID = Field(default_factory=uuid.uuid4)
#     fields: List[GenerationStateField] = Field(default_factory=list)
#     updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
#     created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
#     # source: GenerationSource
#     # previous: Optional["Generatable"] = Field(default=None)


# class Character(BaseModel):
#     character_id: uuid.UUID = Field()
#     generation_state: ObjectGenerationState = Field()


# class GetCharacterRequest(BaseModel):
#     world_id: uuid.UUID = Field()
#     character_id: uuid.UUID = Field()


# class GetCharacterResponse(Response):
#     character: Character = Field()


# class CreateCharacterRequest(BaseModel):
# This is not actually needed because the world id is in the URL
# world_id: uuid.UUID = Field()


# class CreateCharacterResponse(Response):
#     character_id: uuid.UUID = Field()


# class DeleteCharacterRequest(BaseModel):
#     world_id: uuid.UUID = Field()
#     character_id: uuid.UUID = Field()


# class DeleteCharacterResponse(Response):
#     character_id: uuid.UUID = Field()


# class CompleteCharacterRequest(BaseModel):
#     world_id: uuid.UUID = Field()
#     character_id: uuid.UUID = Field()
#     # TODO


# class CompleteCharacterResponse(Response):
#     generation_id: uuid.UUID = Field()
