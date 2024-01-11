
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import datetime
import uuid
import cairne.model.generated as generated
from cairne.schema.base import Response
from enum import Enum
import cairne.model.generation as generation_model
import cairne.model.specification as spec
import cairne.model.generated as generated_model


class AppendElementRequest(BaseModel):
    world_id: uuid.UUID = Field()
    # entity_id: uuid.UUID = Field()
    value_js: str = Field()
    path: generated_model.GeneratablePath = Field()


class AppendElementResponse(BaseModel):
    pass


class ReplaceRequest(BaseModel):
    world_id: uuid.UUID = Field()
    # entity_id: uuid.UUID = Field()
    new_value_js: str = Field()
    path: generated_model.GeneratablePath = Field()


class ReplaceResponse(BaseModel):
    pass


class RemoveValueRequest(BaseModel):
    world_id: uuid.UUID = Field()
    # entity_id: uuid.UUID = Field()
    path: generated_model.GeneratablePath = Field()


class RemoveValueResponse(BaseModel):
    pass

