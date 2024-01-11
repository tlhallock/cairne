from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import datetime
import uuid
from cairne.schema.base import Response

# # from cairne.schema.base import ENTITY_ID, DATE


# class ListWorldsElement(BaseModel):
#     world_id: uuid.UUID = Field(..., description="UUID of the world")
#     name: str = Field(..., description="Name of the world")
#     image_uri: Optional[str] = Field(..., description="Image of the character")
#     created_at: datetime.datetime = Field(..., description="Creation date of the world")
#     updated_at: datetime.datetime = Field(..., description="Last update date of the world")
#     # description: str = Field(..., description="Description of the world")


# class ListWorldsResponse(Response):
#     worlds: List[ListWorldsElement] = Field(..., description="List of worlds")


# class CharacterListElement(BaseModel):
#     character_id: uuid.UUID = Field(..., description="UUID of the character")
#     name: str = Field(..., description="Name of the character")
#     image_uri: Optional[str] = Field(..., description="Image of the character")
#     created_at: datetime.datetime = Field(..., description="Creation date of the character")
#     updated_at: datetime.datetime = Field(..., description="Last update date of the character")


# class World(BaseModel):
#     world_id: uuid.UUID = Field(..., description="UUID of the world")
#     name: str = Field(..., description="Name of the world")
#     image_uri: Optional[str] = Field(..., description="Image of the character")
#     created_at: datetime.datetime = Field(..., description="Creation date of the world")
#     updated_at: datetime.datetime = Field(..., description="Last update date of the world")
#     characters: List[CharacterListElement] = Field(..., description="List of characters in the world")
    

# class GetWorldResponse(Response):
#     world: World = Field(..., description="World")


class CreateWorldRequest(BaseModel):
    name: str = Field(..., description="Name of the world")

# class CreateWorldResponse(Response):
#     world_id: uuid.UUID = Field(..., description="UUID of the world")

# class DeleteWorldRequest(BaseModel):
#     world_id: uuid.UUID = Field(..., description="UUID of the world")

# class DeleteWorldResponse(Response):
#     world_id: uuid.UUID = Field(..., description="UUID of the world")