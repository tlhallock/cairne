import datetime
import uuid
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

import cairne.model.calls as calls
import cairne.model.character as chars
import cairne.model.generated as gen

# class World(BaseModel):
#     world_id: uuid.UUID = Field(default_factory=uuid.uuid4)
#     name: str
#     image_uri: Optional[str] = Field(default=None)
#     created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
#     updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
#     setting: Optional[str] = Field(default=None)
#     concept: Optional[str] = Field(default=None)
#     theme: Optional[str] = Field(default=None)
#     characters: Dict[uuid.UUID, chars.Character] = Field(default_factory=dict)
