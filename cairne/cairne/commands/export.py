
from cairne.commands.base import Command
from dataclasses import dataclass, field
import cairne.model.generated as generated_model
import cairne.model.world as worlds_model
import cairne.model.character as characters_model
import cairne.schema.worlds as worlds_schema
import cairne.schema.characters as characters_schema
import cairne.schema.generated as generated_schema
import uuid



# def export_world(world: generated_model.GeneratedEntity) -> worlds_schema.World:
#     return worlds_schema.World(
#         world_id=world.world_id,
#         name=world.name,
#         image_uri=world.image_uri,
#         created_at=world.created_at,
#         updated_at=world.updated_at,
#         characters=[export_character_item(character) for character in world.characters.values()],
#     )


# def export_world_item(world: generated_model.GeneratedEntity) -> worlds_schema.ListWorldsElement:
#     return worlds_schema.ListWorldsElement(
#         world_id=world.world_id,
#         name=world.name,
#         image_uri=world.image_uri,
#         created_at=world.created_at,
#         updated_at=world.updated_at,
#     )


# def export_generation_field(name: str, generatable: generated.Generatable) -> characters_schema.GenerationStateField:
#     return characters_schema.GenerationStateField(
#         name=name,
#         value=generatable.parsed,  # type: ignore
#     )


def export_generated_entity_item(path: generated_model.GeneratablePath, generated_entity: generated_model.GeneratedEntity) -> generated_schema.GeneratedEntityListItem:
    return generated_schema.GeneratedEntityListItem(
        entity_id=generated_entity.entity_id,
        name=generated_entity.get_name(),
        image_uri=None,
        created_at=generated_entity.get_creation_date(),
        updated_at=generated_entity.metadata.date,
        path=generated_entity.create_path(),
    )


def export_generated_entity(path: generated_model.GeneratablePath, generated_entity: generated_model.GeneratedEntity) -> generated_schema.GeneratedEntity:
    return generated_schema.GeneratedEntity(
        entity_id=generated_entity.entity_id,
        name=generated_entity.get_name(),
        image_uri=None,
        created_at=generated_entity.get_creation_date(),
        updated_at=generated_entity.metadata.date,
        path=generated_entity.create_path(),
        js=generated_entity.model_dump_json(),
        fields=[]
    )


# def export_generation(path: generated_model.GeneratablePath, generated_entity: generated_model.GeneratedEntity) -> generated_schema.GeneratedEntity:
#     return generated_schema.GeneratedEntity(
#         entity_id=generated_entity.entity_id,
#         name=generated_entity.get_name(),
#         image_uri=None,
#         created_at=generated_entity.get_creation_date(),
#         updated_at=generated_entity.metadata.date,
#         path=generated_entity.create_path(),
#         js=generated_entity.model_dump_json(),
#     )










# def export_object_generation_state(character: generated.GeneratableObject) -> characters_schema.Ge:
#     return characters_schema.ObjectGenerationState(
#         generatable_id=character.generatable_id,
#         fields=sorted(
#             [
#                 export_generation_field(name=name, generatable=generatable)
#                 for name, generatable in character.children.items()
#             ],
#             key=lambda field: field.name
#         ),
#         updated_at=character.date,
#         created_at=character.get_creation_date(),
#     )


# def export_generated(generated: generated_model.Generated) -> generated_schema.Generated:
#     return generated_schema.Generated(
#         js_value=generated.model_dump_json()
#     )