
from cairne.commands.base import Command
from dataclasses import dataclass, field
import cairne.model.world as worlds
import cairne.model.character as characters
import cairne.schema.worlds as worlds_schema
import cairne.schema.characters as characters_schema
import uuid
import cairne.commands.export as export

from typing import Optional


# @dataclass
# class CreateCharacter(Command):
#     request: characters_schema.CreateCharacterRequest
    
#     def execute(self) -> characters_schema.CreateCharacterResponse:
#         world = self.datastore.worlds.get(self.request.world_id, None)
#         if world is None:
#             raise ValueError(f"World not found: {self.request.world_id}")
        
#         character = characters.Character()
#         world.characters[character.generatable_id] = character
        
#         self.datastore.save()
        
#         response = characters_schema.CreateCharacterResponse(character_id=character.generatable_id)
#         return response


# @dataclass
# class GetCharacter(Command):
#     request: characters_schema.GetCharacterRequest
    
#     def execute(self) -> characters_schema.GetCharacterResponse:
#         world = self.datastore.worlds.get(self.request.world_id, None)
#         if world is None:
#             raise ValueError(f"World not found: {self.request.world_id}")
        
#         character = world.characters.get(self.request.character_id, None)
#         if character is None:
#             raise ValueError(f"Character not found: {self.request.character_id}")
        
#         exported = export.export_character(character)
#         return characters_schema.GetCharacterResponse(character=exported)


# @dataclass
# class DeleteCharacter(Command):
#     request: characters_schema.DeleteCharacterRequest
    
#     def execute(self) -> characters_schema.DeleteCharacterResponse:
#         world = self.datastore.worlds.get(self.request.world_id, None)
#         if world is None:
#             raise ValueError(f"World not found: {self.request.world_id}")
        
#         character = world.characters.get(self.request.character_id, None)
#         if character is None:
#             raise ValueError(f"Character not found: {self.request.character_id}")
        
#         del world.characters[character.generatable_id]
#         self.datastore.save()
        
#         return characters_schema.DeleteCharacterResponse(character_id=character.generatable_id)
