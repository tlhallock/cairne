import json
import typing
import uuid
from dataclasses import dataclass, field
from typing import List, Optional, Union

import cairne.model.character as characters_model
import cairne.model.generated as generated_model
import cairne.model.generation as generate_model
import cairne.model.specification as spec
import cairne.model.world as worlds_model
import cairne.schema.characters as characters_schema
import cairne.schema.generate as generate_schema
import cairne.schema.generated as generated_schema
import cairne.schema.worlds as worlds_schema
from cairne.commands.base import Command
from cairne.model.world_spec import WORLD

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


def export_generated_entity_item(
	path: spec.GeneratablePath,
	generated_entity: generated_model.GeneratedEntity,
) -> generated_schema.GeneratedEntityListItem:
	return generated_schema.GeneratedEntityListItem(
		entity_id=generated_entity.entity_id,
		name=generated_entity.get_name(),
		image_uri=None,
		created_at=generated_entity.get_creation_date(),
		updated_at=generated_entity.metadata.date,
		path=generated_entity.create_path(),
	)


def export_generated_object_child(
	path: spec.GeneratablePath,
	label: str,
	generatable: generated_model.GeneratedObject,
) -> generated_schema.GeneratedField:
	children: list[generated_schema.GeneratedField] = []
	for name, child in generatable.children.items():
		child_path = path.append(spec.GeneratablePathElement(key=name))
		children.append(export_generated_child(child_path, name, child))
	return generated_schema.GeneratedField(
		label=label,
		raw_value=json.dumps(generatable.raw),
		value_js="Fill me in",
		value_type=generated_schema.GeneratedValueEditor.G_OBJECT,
		edit_path=path,
		choices=None, # TODO
		validation_errors=[], # TODO
		children=children,
	)


def get_add_value_type(parser_name: spec.ParserName) -> generated_schema.GeneratedValueEditor:
	if parser_name == spec.ParserName.BOOLEAN:
		return generated_schema.GeneratedValueEditor.G_BOOLEAN
	elif parser_name == spec.ParserName.STRING:
		return generated_schema.GeneratedValueEditor.G_STRING
	elif parser_name == spec.ParserName.INTEGER:
		return generated_schema.GeneratedValueEditor.G_INTEGER
	elif parser_name == spec.ParserName.FLOAT:
		return generated_schema.GeneratedValueEditor.G_FLOAT
	elif parser_name == spec.ParserName.OBJECT:
		return generated_schema.GeneratedValueEditor.G_OBJECT
	elif parser_name == spec.ParserName.LIST:
		return generated_schema.GeneratedValueEditor.G_LIST
	elif parser_name == spec.ParserName.ENTITY_DICTIONARY:
		return generated_schema.GeneratedValueEditor.G_ENTITIES
	else:
		raise NotImplementedError(f"Unknown parser name: {parser_name}")


def export_generated_list_child(
	path: spec.GeneratablePath,
	label: str,
	generatable: generated_model.GeneratedList,
) -> generated_schema.GeneratedField:
	specification = WORLD.get(path, 0)
	if not isinstance(specification, spec.ListSpecification):
		raise NotImplementedError(f"Expected list specification at {path}")
	add_value_type = get_add_value_type(specification.element_specification.parser.parser_name)

	children: list[generated_schema.GeneratedField] = []
	for index, child in enumerate(generatable.elements):
		child_path = path.append(spec.GeneratablePathElement(index=index))
		children.append(export_generated_child(child_path, f"[index]", child))
	return generated_schema.GeneratedField(
		label=label,
		raw_value=json.dumps(generatable.raw),
		value_js="Fill me in",
		value_type=generated_schema.GeneratedValueEditor.G_LIST,
		edit_path=path,
		choices=None, # TODO
		validation_errors=[], # TODO
		children=children,
  		add_value_type=add_value_type,
	)


def export_generated_dictionary_child(
	path: spec.GeneratablePath,
	label: str,
	generatable: generated_model.EntityDictionary,
) -> generated_schema.GeneratedField:
	children: list[generated_schema.GeneratedField] = []
	for key, child in generatable.entities.items():
		label = child.get_name() or str(key)
		child_path = path.append(spec.GeneratablePathElement(entity_id=key))
		children.append(export_generated_child(child_path, label, child))
	return generated_schema.GeneratedField(
		label=label,
		raw_value=json.dumps(generatable.raw),
		value_js="Fill me in",
		value_type=generated_schema.GeneratedValueEditor.G_ENTITIES,
		edit_path=path,
		choices=None, # TODO
		validation_errors=[], # TODO
		children=children,
	)


def export_generated_boolean_child(
	path: spec.GeneratablePath,
	label: str,
	generatable: generated_model.GeneratedBoolean,
) -> generated_schema.GeneratedField:
	return generated_schema.GeneratedField(
		label=label,
		raw_value=json.dumps(generatable.raw),
		value_js=json.dumps(generatable.parsed),
		value_type=generated_schema.GeneratedValueEditor.G_BOOLEAN,
		edit_path=path,
		choices=None, # TODO
		validation_errors=[], # TODO
		children=None,
	)


def export_generated_string_child(
	path: spec.GeneratablePath,
	label: str,
	generatable: generated_model.GeneratedString,
) -> generated_schema.GeneratedField:
	return generated_schema.GeneratedField(
		label=label,
		raw_value=json.dumps(generatable.raw),
		value_js=json.dumps(generatable.parsed),
		value_type=generated_schema.GeneratedValueEditor.G_STRING,
		edit_path=path,
		choices=None, # TODO
		validation_errors=[], # TODO
		children=None,
	)


def export_generated_integer_child(
	path: spec.GeneratablePath,
	label: str,
	generatable: generated_model.GeneratedInteger,
) -> generated_schema.GeneratedField:
	return generated_schema.GeneratedField(
		label=label,
		raw_value=json.dumps(generatable.raw),
		value_js=json.dumps(generatable.parsed),
		value_type=generated_schema.GeneratedValueEditor.G_INTEGER,
		edit_path=path,
		choices=None, # TODO
		validation_errors=[], # TODO
		children=None,
	)


def export_generated_float_child(
	path: spec.GeneratablePath,
	label: str,
	generatable: generated_model.GeneratedFloat,
) -> generated_schema.GeneratedField:
	return generated_schema.GeneratedField(
		label=label,
		raw_value=json.dumps(generatable.raw),
		value_js=json.dumps(generatable.parsed),
		value_type=generated_schema.GeneratedValueEditor.G_FLOAT,
		edit_path=path,
		choices=None, # TODO
		validation_errors=[], # TODO
		children=None,
	)



# TODO: We could improt exprting into the model itself
def export_generated_child(
	path: spec.GeneratablePath,
	label: str,
	generatable: generated_model.Generated,
) -> generated_schema.GeneratedField:
	if isinstance(generatable, generated_model.GeneratedEntity):
		entity = typing.cast(generated_model.GeneratedEntity, generatable)
		return export_generated_object_child(path, label, entity)
	elif isinstance(generatable, generated_model.GeneratedObject):
		object = typing.cast(generated_model.GeneratedObject, generatable)
		return export_generated_object_child(path, label, object)
	elif isinstance(generatable, generated_model.GeneratedList):
		gen_list = typing.cast(generated_model.GeneratedList, generatable)
		return export_generated_list_child(path, label, gen_list)
	elif isinstance(generatable, generated_model.EntityDictionary):
		gen_dict = typing.cast(generated_model.EntityDictionary, generatable)
		return export_generated_dictionary_child(path, label, gen_dict)
	elif isinstance(generatable, generated_model.GeneratedBoolean):
		gen_bool = typing.cast(generated_model.GeneratedBoolean, generatable)
		return export_generated_boolean_child(path, label, gen_bool)
	elif isinstance(generatable, generated_model.GeneratedString):
		gen_string = typing.cast(generated_model.GeneratedString, generatable)
		return export_generated_string_child(path, label, gen_string)
	elif isinstance(generatable, generated_model.GeneratedInteger):
		gen_int = typing.cast(generated_model.GeneratedInteger, generatable)
		return export_generated_integer_child(path, label, gen_int)
	elif isinstance(generatable, generated_model.GeneratedFloat):
		gen_float = typing.cast(generated_model.GeneratedFloat, generatable)
		return export_generated_float_child(path, label, gen_float)
	else:
		raise NotImplementedError("Unknown generatable type: " + str(type(generatable)))


def export_generated_entity(
	path: spec.GeneratablePath,
	generated_entity: generated_model.GeneratedEntity,
) -> generated_schema.GeneratedEntity:
	fields = export_generated_object_child(path, "", generated_entity).children
	if fields is None:
		raise NotImplementedError("No fields found for entity: " + str(generated_entity))
	return generated_schema.GeneratedEntity(
		entity_id=generated_entity.entity_id,
		name=generated_entity.get_name(),
		image_uri=None,
		created_at=generated_entity.get_creation_date(),
		updated_at=generated_entity.metadata.date,
		path=generated_entity.create_path(),
		js=generated_entity.model_dump_json(),
		fields=fields,
	)


def export_generation_list_item(generation: generate_model.Generation) -> generate_schema.GenerationListItem:
	return generate_schema.GenerationListItem(
		generation_id=generation.generation_id,
		begin_time=generation.begin_time,
		end_time=generation.end_time,
		status=generation.status,
	)


def export_generation(generation: generate_model.Generation) -> generate_schema.Generation:
	return generate_schema.Generation(
		generation_id=generation.generation_id,
		begin_time=generation.begin_time,
		end_time=generation.end_time,
		status=generation.status,
		world_id=generation.world_id,
		entity_id=generation.entity_id,
		entity_type=generation.entity_type,
	)


def export_entity_specification_field(name: str, specification: spec.EntitySpecification) -> generated_schema.EntityGenerationField:
	return generated_schema.EntityGenerationField(
		name=name,
	)


def export_entity_specification(specification: spec.EntitySpecification) -> generated_schema.EntityGenerationSchema:
	return generated_schema.EntityGenerationSchema(
		fields=[
			export_entity_specification_field(name, specification)
			for name, specification in specification.children.items()
		],
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
