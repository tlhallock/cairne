import datetime
import uuid
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from cairne.schema.base import Response


class CreateWorldRequest(BaseModel):
	name: str = Field(..., description="Name of the world")


class EntityType(BaseModel):
    name: str = Field()
    label: str = Field()


class ListEntityTypesResponse(Response):
	entity_types: List[EntityType] = Field(..., description="List of entity types")


class EntityTypeSummary(BaseModel):
    name: str = Field()
    label: str = Field()
    total_number: int = Field()


class WorldSummary(BaseModel):
    id: uuid.UUID = Field(..., description="ID of the world")
    name: str = Field(..., description="Name of the world")
    entity_type_summaries: List[EntityTypeSummary] = Field()
    generation_goals: List[str] = Field()
    