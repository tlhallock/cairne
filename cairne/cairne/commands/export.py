import json
import typing
import uuid
from dataclasses import dataclass, field
from typing import List, Optional, Union, Sized

from structlog import get_logger

import cairne.model.generated as generated_model
import cairne.model.generation as generate_model
import cairne.model.specification as spec
import cairne.model.validation as validation
import cairne.schema.generate as generate_schema
import cairne.schema.generated as generated_schema
import cairne.schema.worlds as worlds_schema
from cairne.model.world_spec import WORLD
import cairne.model.templates as template_model
import cairne.schema.templates as template_schema


logger = get_logger(__name__)


def export_validation_errors(
    validation_errors: List[spec.ValidationError],
) -> List[str]:
    return [validation_error.message for validation_error in validation_errors]


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
        children.append(export_generated_child(child_path, name, typing.cast(generated_model.Generated, child)))
    return generated_schema.GeneratedField(
        label=label,
        raw_value=json.dumps(generatable.raw),
        value_js=json.dumps(""),
        value_type=generated_schema.GeneratedValueEditor.G_OBJECT,
        edit_path=path,
        edit_path_key=path.as_str(),
        choices=None,  # TODO
        validation_errors=export_validation_errors(generatable.validation_errors),
        children=children,
        generate=generatable.generate,
        generated_value_label=generatable.generated_label,
        generated_value_js=generatable.generated_js,
    )


def get_add_value_type(
    parser_name: spec.ParserName,
) -> generated_schema.GeneratedValueEditor:
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
    add_value_type = get_add_value_type(
        specification.element_specification.parser.parser_name
    )

    children: list[generated_schema.GeneratedField] = []
    for index, child in enumerate(generatable.elements):
        child_path = path.append(spec.GeneratablePathElement(index=index))
        children.append(export_generated_child(child_path, f"[{index}]", typing.cast(generated_model.Generated, child)))
    return generated_schema.GeneratedField(
        label=label,
        raw_value=json.dumps(generatable.raw),
        value_js=json.dumps(f"Number of elements: {len(generatable.elements)}"),
        value_type=generated_schema.GeneratedValueEditor.G_LIST,
        edit_path=path,
        edit_path_key=path.as_str(),
        choices=None,  # TODO
        validation_errors=export_validation_errors(generatable.validation_errors),
        children=children,
        add_value_type=add_value_type,
        generate=generatable.generate,
        generated_value_label=generatable.generated_label,
        generated_value_js=generatable.generated_js,
        number_to_generate=generated_schema.NumberToGenerate(
            number_to_generate=generatable.generation_settings.number_to_generate,
        )
        if generatable.generation_settings is not None and generatable.generation_settings.number_to_generate is not None
        else None,
    )


def export_generated_dictionary_child(
    path: spec.GeneratablePath,
    label: str,
    generatable: generated_model.EntityDictionary,
) -> generated_schema.GeneratedField:
    specification = WORLD.get(path, 0)
    if not isinstance(specification, spec.EntityDictionarySpecification):
        raise NotImplementedError(f"Expected entity dictionary specification at {path}")

    children: list[generated_schema.GeneratedField] = []
    if False:
        for key, child in generatable.entities.items():
            label = child.get_name() or str(key)
            child_path = path.append(spec.GeneratablePathElement(entity_id=key))
            children.append(export_generated_child(child_path, label, child))
    return generated_schema.GeneratedField(
        label=label,
        raw_value=json.dumps(generatable.raw),
        value_js=json.dumps(f"Number of entities: {len(generatable.entities)}"),
        value_type=generated_schema.GeneratedValueEditor.G_ENTITIES,
        edit_path=path,
        edit_path_key=path.as_str(),
        choices=None,  # TODO
        validation_errors=export_validation_errors(generatable.validation_errors),
        children=children,
        generated_value_label=generatable.generated_label,
        generated_value_js=generatable.generated_js,
        entity_dictionary_type=export_entity_type(
            specification.entity_specification.entity_type
        ),
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
        edit_path_key=path.as_str(),
        choices=None,  # TODO
        validation_errors=export_validation_errors(generatable.validation_errors),
        children=None,
        generate=generatable.generate,
        generated_value_label=generatable.generated_label,
        generated_value_js=generatable.generated_js,
    )


def export_choices(path: spec.GeneratablePath) -> Optional[List[generated_schema.GeneratedFieldChoice]]:
    specification = WORLD.get(path, 0)
    choices = None
    for validator in specification.validators:
        if isinstance(validator, spec.OneOfLiteralValidator):
            validator_choices = set(
                [option[1][0] for option in validator.options if isinstance(option[0], Sized) and len(option[0]) > 0]
            )
            if choices is None:
                choices = set(validator_choices)
            else:
                choices = choices.intersection(validator_choices)
        elif isinstance(validator, spec.OneOfGeneratedValidator):
            logger.info("TODO: OneOfGeneratedValidator choices")
    if not choices:
        return None
    return [
        generated_schema.GeneratedFieldChoice(
            label=choice,
            value=choice,
        )
        for choice in choices
    ]


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
        edit_path_key=path.as_str(),
        choices=export_choices(path),
        validation_errors=export_validation_errors(generatable.validation_errors),
        children=None,
        generate=generatable.generate,
        generated_value_label=generatable.generated_label,
        generated_value_js=generatable.generated_js,
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
        edit_path_key=path.as_str(),
        choices=None,  # TODO
        validation_errors=export_validation_errors(generatable.validation_errors),
        children=None,
        generate=generatable.generate,
        generated_value_label=generatable.generated_label,
        generated_value_js=generatable.generated_js,
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
        edit_path_key=path.as_str(),
        choices=None,  # TODO
        validation_errors=export_validation_errors(generatable.validation_errors),
        children=None,
        generate=generatable.generate,
        generated_value_label=generatable.generated_label,
        generated_value_js=generatable.generated_js,
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
    world: generated_model.GeneratedEntity,
    path: spec.GeneratablePath,
    generated_entity: generated_model.GeneratedEntity,
) -> generated_schema.GeneratedEntity:

    # TODO: This doesn't return the validation errors for the entity itself
    fields = export_generated_object_child(path, "", generated_entity).children
    if fields is None:
        raise NotImplementedError(
            "No fields found for entity: " + str(generated_entity)
        )

    # dictionary_path = generated_entity.entity_type.get_dictionary_path()
    # entity_path = dictionary_path.append(spec.GeneratablePathElement(entity_id=generated_entity.entity_id))

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


def export_generation_list_item(
    generation: generate_model.Generation,
) -> generate_schema.GenerationListItem:
    return generate_schema.GenerationListItem(
        label=generation.template_snapshot.name,
        generation_id=generation.generation_id,
        begin_time=generation.begin_time,
        end_time=generation.end_time,
        status=generation.status,
    )


# def export_generation_result(result: Optional[generate_model.GenerateResult]) -> Optional[generate_schema.GenerationResultView]:
#     if not result:
#         return None

#     return generate_schema.GenerationResultView(
#         raw_text=result.raw_text,
#         # validated=export_generated_entity(result.parsed),
#     )


def export_generation(
    generation: generate_model.Generation,
    world: generated_model.GeneratedEntity,
) -> generate_schema.GenerationView:
    return generate_schema.GenerationView(
        generation_id=generation.generation_id,
        template=export_template(generation.template_snapshot, world),
        begin_time=generation.begin_time,
        end_time=generation.end_time,
        status=generation.status,
        raw_generated_text=generation.result.raw_text if generation.result else None,
    )


def export_entity_type(entity_type: spec.EntityType) -> worlds_schema.EntityTypeView:
    return worlds_schema.EntityTypeView(
        name=entity_type.value,
        label=entity_type.get_label(),
    )



def export_template_list_item(
    template: template_model.GenerationTemplate,
) -> template_schema.TemplateListItem:
    return template_schema.TemplateListItem(
        template_id=template.template_id,
        name=template.name,
        entity_id=template.entity_id,
        world_id=template.world_id,
        generation_type=template.generation_type,
        entity_type=export_entity_type(template.entity_type),
        created_at=template.created_at,
        updated_at=template.updated_at,
    )


def export_instructions(
    world: generated_model.GeneratedEntity,
    template: template_model.GenerationTemplate,
) -> List[template_schema.InstructionView]:
    specification = WORLD.get(template.target_path, 0)
    unfilled_instructions = [
        instruction.model_copy(deep=True)
        for instruction in specification.generation.instructions
    ]
    instructions_by_name = {
        instruction.name: template_schema.InstructionView(
            name=instruction.name,
            label=instruction.label or instruction.name,
            preview=instruction.template,
            valid=False,
            included=True,
        )
        for instruction in unfilled_instructions
    }
    for excluded in template.excluded_instruction_names:
        instructions_by_name[excluded].included = False
    
    generation_variables = template_model.GenerationVariables.create(world)
    filled_instructions = generation_variables.fill_instructions(unfilled_instructions)
    for instruction in filled_instructions:
        instructions_by_name[instruction.name].preview = instruction.message
        instructions_by_name[instruction.name].valid = True
    
    return list(instructions_by_name.values())


def export_template(
    template: template_model.GenerationTemplate,
    world: generated_model.GeneratedEntity,
) -> template_schema.GenerationTemplateView:
    return template_schema.GenerationTemplateView(
        template_id=template.template_id,
        name=template.name,
        created_at=template.created_at,
        updated_at=template.updated_at,
        world_id=template.world_id,
        entity_id=template.entity_id,
        target_path=template.target_path,
        entity_type=template.entity_type,
        generation_type=template.generation_type,
        generator_model=template.generator_model,
        prompt=template.additional_prompt,
        parameters=template.parameters,
        fields_to_include=[field.path for field in template.fields_to_include],
        instructions=export_instructions(world, template),
        json_structure_preview=template.create_json_schema(),
        validations_to_include=[],  # TODO
    )


# def export_entity_specification_field(
#     name: str, specification: spec.GeneratableSpecification
# ) -> generated_schema.EntityGenerationField:
#     return generated_schema.EntityGenerationField(
#         name=name,
#    )

# def export_entity_specification(
#     specification: spec.EntitySpecification,
# ) -> generated_schema.EntityGenerationSchema:
#     return generated_schema.EntityGenerationSchema(
#         fields=[
#             export_entity_specification_field(name, specification)
#             for name, specification in specification.children.items()
#         ],
#     )




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
