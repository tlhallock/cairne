import datetime
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

import cairne.model.generated as generated
import cairne.model.generated as generated_model
import cairne.model.generation as generation_model
import cairne.model.specification as spec
from cairne.schema.base import Response


class AppendElementRequest(BaseModel):
    world_id: uuid.UUID = Field()
    value_js: str = Field()
    path: spec.GeneratablePath = Field()


class AppendElementResponse(Response):
    pass


class ReplaceRequest(BaseModel):
    world_id: uuid.UUID = Field()
    value_js: str = Field()
    path: spec.GeneratablePath = Field()


class ReplaceResponse(Response):
    pass


class RemoveValueRequest(BaseModel):
    world_id: uuid.UUID = Field()
    path: spec.GeneratablePath = Field()


class RemoveValueResponse(Response):
    pass
