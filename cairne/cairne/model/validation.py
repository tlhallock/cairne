import datetime
import json
import typing
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union, Generator

from pydantic import BaseModel, Field
from structlog import get_logger

import cairne.model.calls as calls
# rename this to generated_model
import cairne.model.generated as generated_model
import cairne.model.parsing as parsing
import cairne.model.specification as spec
import cairne.parsing.parse_incomplete_json as parse_incomplete
from cairne.model.world_spec import WORLD

logger = get_logger(__name__)


@dataclass
class ValidationContext:
    world: generated_model.GeneratedEntity = field()
    current_path: spec.GeneratablePath = field()
    generated_stack: List[generated_model.GeneratedBase] = field(default_factory=list)
    errors: List[spec.ValidationError] = field(default_factory=list)
    success: bool = field(default=True)
    # validated?

    def create_path(self) -> str:
        return self.current_path.as_str()

    def add_error(self, error: spec.ValidationError) -> None:
        self.errors.append(error)
        if len(self.generated_stack) > 0:
            self.generated_stack[-1].validation_errors.append(error)
        else:
            self.world.validation_errors.append(error)
        self.success = False

    @contextmanager
    def with_path(
        self, path_element: spec.GeneratablePathElement, generated: generated_model.GeneratedBase
    ) -> Generator[None, None, None]:
        old_path = self.current_path
        self.current_path = self.current_path.append(path_element)
        self.generated_stack.append(generated)
        generated.validation_errors = []
        yield
        self.generated_stack.pop()
        self.current_path = old_path

    # required: bool = Field(default=True)
    # options: List[Tuple[Any, List[str]]]


# def parse_value(context: ValidationContext, spec: spec.OneOfLiteralValidator, generated: gen.GeneratedValue) -> None:
#     return None


def validate_nonnegative(
    context: ValidationContext,
    specification: spec.ValidatorSpecification,
    parsed: generated_model.GeneratedValue,
):
    if isinstance(parsed, generated_model.GeneratedFloat):
        float_value = typing.cast(generated_model.GeneratedFloat, parsed)
        parsed_float = float_value.parsed
        if parsed_float is None:
            return
        if parsed_float < 0:
            context.add_error(
                spec.ValidationError(
                    path=context.create_path(),
                    message=f"expected a positive float, found {parsed_float}",
                )
            )
    elif isinstance(parsed, generated_model.GeneratedInteger):
        integer_value = typing.cast(generated_model.GeneratedInteger, parsed)
        parsed_integer = integer_value.parsed
        if parsed_integer is None:
            return
        if parsed_integer < 0:
            context.add_error(
                spec.ValidationError(
                    path=context.create_path(),
                    message=f"expected a positive integer, found {parsed_integer}",
                )
            )
    else:
        context.add_error(
            spec.ValidationError(
                path=context.create_path(),
                message=f"expected an float or integer, found {parsed}",
            )
        )


def validate_name(
    context: ValidationContext,
    specification: spec.ValidatorSpecification,
    parsed: generated_model.GeneratedBase,
):
    pass


def validate_required(
    context: ValidationContext,
    specification: spec.ValidatorSpecification,
    parsed: generated_model.GeneratedBase,
):
    if not parsed.is_generated():
        context.add_error(
            spec.ValidationError(
                path=context.create_path(), message=f"field is required"
            )
        )
        return


def find_option(
    specification: spec.OneOfLiteralValidator, parsed: generated_model.GeneratedString
) -> Optional[Any]:
    for option, representations in specification.options:
        for repr in representations:
            if repr.lower() == repr.lower():
                return option
    return None


def validate_one_of_literal(
    context: ValidationContext,
    specification: spec.OneOfLiteralValidator,
    parsed: generated_model.GeneratedBase,
) -> None:
    if not isinstance(parsed, generated_model.GeneratedString):
        context.add_error(
            spec.ValidationError(
                path=context.create_path(), message=f"expected a value, found {parsed}"
            )
        )
        return

    if not parsed.is_generated():
        context.add_error(
            spec.ValidationError(
                path=context.create_path(), message=f"enumerated field is required"
            )
        )
        return

    option = find_option(specification, parsed)
    if option is not None:
        parsed.result = option
        return

    options_list = ", ".join(
        [f"'{r}'" for _, repr in specification.options for r in repr]
    )
    context.add_error(
        spec.ValidationError(
            path=context.create_path(), message=f"field must be one of [{options_list}]"
        )
    )


def validate_one_of_generated_list_of_strings(
    context: ValidationContext,
    generated_list: generated_model.GeneratedList,
    parsed: generated_model.GeneratedBase,
) -> None:
    possible_values: List[str] = []
    for element in generated_list.elements:
        generated_string = typing.cast(generated_model.GeneratedString, element)
        if generated_string.parsed is None:
            continue
        possible_values.append(generated_string.parsed)
    string_to_validate = typing.cast(generated_model.GeneratedString, parsed).parsed
    if string_to_validate is None:
        # This can have its own required validator
        return
    for possible_value in possible_values:
        if possible_value.lower() == string_to_validate.lower():
            parsed.result = possible_value
            return
    context.add_error(
        spec.ValidationError(
            path=context.create_path(),
            message=f"field must be one of [{possible_values}], found {string_to_validate}",
        )
    )

def validate_one_of_generated(
    context: ValidationContext,
    specification: spec.OneOfGeneratedValidator,
    parsed: generated_model.GeneratedBase,
) -> None:
    # We need to get this from the world...
    generated_options: generated_model.Generated = context.world.get(specification.path, 0)
    generated_options_specification = WORLD.get(specification.path, 0)

    if not isinstance(generated_options, generated_model.GeneratedList):
        context.add_error(
            spec.ValidationError(
                path=context.create_path(),
                message=f"Only know how to validate generated lists, not {generated_options}",
            )
        )
        return
    generated_list = typing.cast(generated_model.GeneratedList, generated_options)
    if not isinstance(generated_options_specification, spec.ListSpecification):
        context.add_error(
            spec.ValidationError(
                path=context.create_path(),
                message=f"Only know how to validate generated lists, not {generated_options_specification}",
            )
        )
    list_specification = typing.cast(spec.ListSpecification, generated_options_specification)
    if not isinstance(
        list_specification.element_specification, spec.ValueSpecification
    ):
        context.add_error(
            spec.ValidationError(
                path=context.create_path(),
                message=f"Only know how to validate generated lists of values, not {list_specification.element_specification}",
            )
        )
        return
    element_specification = typing.cast(spec.ValueSpecification, list_specification.element_specification)
    
    if element_specification.parser.parser_name == spec.ParserName.STRING:
        validate_one_of_generated_list_of_strings(
            context=context,
            generated_list=generated_list,
            parsed=parsed,
        )
    elif element_specification.parser.parser_name == spec.ParserName.FLOAT:
        raise NotImplementedError()
    elif element_specification.parser.parser_name == spec.ParserName.INTEGER:
        raise NotImplementedError()
    elif element_specification.parser.parser_name == spec.ParserName.BOOLEAN:
        raise NotImplementedError()
    else:
        context.add_error(
            spec.ValidationError(
                path=context.create_path(),
                message=f"Only know how to validate generated lists of values, not {list_specification.element_specification}",
            )
        )
        return


def validate_field(
    context: ValidationContext,
    specification: spec.ValidatorSpecification,
    parsed: generated_model.GeneratedBase,
):
    if specification.validator_name == spec.ValidatorName.REQUIRED:
        validate_required(context, specification, parsed)
    elif specification.validator_name == spec.ValidatorName.ONE_OF_LITERAL:
        validate_one_of_literal(
            context, typing.cast(spec.OneOfLiteralValidator, specification), parsed
        )
    elif specification.validator_name == spec.ValidatorName.NAME:
        validate_name(context, specification, parsed)
    elif specification.validator_name == spec.ValidatorName.NONNEGATIVE:
        validate_nonnegative(
            context, specification, typing.cast(generated_model.GeneratedValue, parsed)
        )
    elif specification.validator_name == spec.ValidatorName.ONE_OF_GENERATED:
        validate_one_of_generated(
            context, typing.cast(spec.OneOfGeneratedValidator, specification), parsed
        )
    else:
        logger.error(f"unknown validator {specification.validator_name}")
        raise NotImplementedError()


def validate_generated(
    context: ValidationContext,
    specification: spec.GeneratableSpecification,
    generatable: generated_model.GeneratedBase,
):
    generatable.validation_errors = []
    for validator in specification.validators:
        validate_field(context, validator, generatable)

    if isinstance(specification, spec.ValueSpecification):
        if not isinstance(generatable, generated_model.GeneratedValue):
            context.add_error(
                spec.ValidationError(
                    path=context.create_path(),
                    message=f"expected a value, found {generatable}",
                )
            )
            return
        value = typing.cast(generated_model.GeneratedValue, generatable)
    # elif isinstance(specification, spec.EntitySpecification):
    # 	if not isinstance(generatable, gen.GeneratedEntity):
    # 		context.add_error(
    # 			spec.ValidationError(
    # 				path=context.create_path(),
    # 				message=f"expected an entity, found {generatable}",
    # 			)
    # 		)
    # 		return
    # 	entity = typing.cast(gen.GeneratedEntity, generatable)
    elif isinstance(specification, spec.EntityDictionarySpecification):
        if not isinstance(generatable, generated_model.EntityDictionary):
            context.add_error(
                spec.ValidationError(
                    path=context.create_path(),
                    message=f"expected a dictionary, found {generatable}",
                )
            )
            return
        dictionary = typing.cast(generated_model.EntityDictionary, generatable)
        for uuid_key, child_entity in dictionary.entities.items():
            with context.with_path(
                spec.GeneratablePathElement(entity_id=uuid_key), generated=child_entity
            ):
                validate_generated(
                    context=context,
                    specification=specification.entity_specification,
                    generatable=child_entity,
                )
    elif isinstance(specification, spec.ListSpecification):
        if not isinstance(generatable, generated_model.GeneratedList):
            context.add_error(
                spec.ValidationError(
                    path=context.create_path(),
                    message=f"expected a list, found {generatable}",
                )
            )
            return
        generated_list = typing.cast(generated_model.GeneratedList, generatable)
        for index, element in enumerate(generated_list.elements):
            with context.with_path(
                spec.GeneratablePathElement(index=index), generated=element
            ):
                validate_generated(
                    context=context,
                    specification=specification.element_specification,
                    generatable=element,
                )
    elif isinstance(specification, spec.ObjectSpecification):
        if not isinstance(generatable, generated_model.GeneratedObject):
            context.add_error(
                spec.ValidationError(
                    path=context.create_path(),
                    message=f"expected an object, found {generatable}",
                )
            )
            return
        generated_object = typing.cast(generated_model.GeneratedObject, generatable)
        for child_key, child_field in generated_object.children.items():
            child_specification = specification.children.get(child_key, None)
            if not child_specification:
                context.add_error(
                    spec.ValidationError(
                        path=context.create_path(),
                        message=f"field {child_key} not in the specification",
                    )
                )
                continue
            with context.with_path(
                spec.GeneratablePathElement(key=child_key), generated=child_field
            ):
                validate_generated(
                    context=context,
                    specification=child_specification,
                    generatable=child_field,
                )
    else:
        logger.error(f"unknown specification {specification}")
        raise NotImplementedError()
