import datetime
import json
import typing
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field
from structlog import get_logger

import cairne.model.calls as calls
# rename this to generated_model
import cairne.model.generated as gen
import cairne.model.parsing as parsing
import cairne.model.specification as spec
import cairne.parsing.parse_incomplete_json as parse_incomplete

logger = get_logger(__name__)


@dataclass
class ValidationContext:
    validation_root: gen.GeneratedEntity = field()
    current_path: spec.GeneratablePath = field()
    generated_stack: List[gen.GeneratedBase] = field(default_factory=list)
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
            self.validation_root.validation_errors.append(error)
        self.success = False

    @contextmanager
    def with_path(
        self, path_element: spec.GeneratablePathElement, generated: gen.GeneratedBase
    ) -> None:
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
    parsed: gen.GeneratedValue,
):
    if isinstance(parsed, gen.GeneratedFloat):
        float_value = typing.cast(gen.GeneratedFloat, parsed)
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
    elif isinstance(parsed, gen.GeneratedInteger):
        integer_value = typing.cast(gen.GeneratedInteger, parsed)
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
    parsed: gen.Generated,
):
    pass


def validate_required(
    context: ValidationContext,
    specification: spec.ValidatorSpecification,
    parsed: gen.Generated,
):
    if not parsed.is_generated():
        context.add_error(
            spec.ValidationError(
                path=context.create_path(), message=f"field is required"
            )
        )
        return


def find_option(
    specification: spec.OneOfLiteralValidator, parsed: gen.GeneratedString
) -> Optional[Any]:
    for option, representations in specification.options:
        for repr in representations:
            if repr.lower() == repr.lower():
                return option
    return None


def validate_one_of_literal(
    context: ValidationContext,
    specification: spec.OneOfLiteralValidator,
    parsed: gen.Generated,
) -> None:
    if not isinstance(parsed, gen.GeneratedString):
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


def validate_one_of_generated(
    context: ValidationContext,
    specification: spec.OneOfGeneratedValidator,
    parsed: gen.Generated,
) -> None:
    return
    # We need to get this from the world...
    generated_options: gen.Generated = context.validation_root.get(
        specification.path, 0
    )

    if isinstance(generated_options, gen.GeneratedList):
        generated_list = typing.cast(gen.GeneratedList, generated_options)
        list_specification = typing.cast(spec.ListSpecification, specification)
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
        element_specification = typing.cast(
            spec.ValueSpecification, list_specification.element_specification
        )
        if element_specification.parser.parser_name == spec.ParserName.STRING:
            possible_values = []
            for element in generated_list.elements:
                generated_string = typing.cast(gen.GeneratedString, element)
                if generated_string.parsed is None:
                    continue
                possible_values.append(generated_string.parsed)
            string_to_validate = typing.cast(gen.GeneratedString, parsed).parsed
            if string_to_validate is None:
                # context.add_error(
                # 	spec.ValidationError(
                # 		path=context.create_path(),
                # 		message=f"Value must not be empty, possible values: {possible_values}"
                # 	)
                # )
                return
            for possible_value in possible_values:
                if possible_value.lower() == string_to_validate.lower():
                    parsed.result = possible_value
                    return
            context.add_error(
                spec.ValidationError(
                    path=context.create_path(),
                    message=f"field must be one of [{generated_options}], found {string_to_validate}",
                )
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
    else:
        context.add_error(
            spec.ValidationError(
                path=context.create_path(),
                message=f"Only know how to validate generated lists, not {generated_options}",
            )
        )


def validate_field(
    context: ValidationContext,
    specification: spec.ValidatorSpecification,
    parsed: gen.Generated,
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
            context, specification, typing.cast(gen.GeneratedValue, parsed)
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
    generatable: gen.Generated,
):
    for validator in specification.validators:
        validate_field(context, validator, generatable)

    if isinstance(specification, spec.ValueSpecification):
        if not isinstance(generatable, gen.GeneratedValue):
            context.add_error(
                spec.ValidationError(
                    path=context.create_path(),
                    message=f"expected a value, found {generatable}",
                )
            )
            return
        value = typing.cast(gen.GeneratedValue, generatable)
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
        if not isinstance(generatable, gen.EntityDictionary):
            context.add_error(
                spec.ValidationError(
                    path=context.create_path(),
                    message=f"expected a dictionary, found {generatable}",
                )
            )
            return
        dictionary = typing.cast(gen.EntityDictionary, generatable)
        for key, value in dictionary.entities.items():
            with context.with_path(
                spec.GeneratablePathElement(entity_id=key), generated=value
            ):
                validate_generated(
                    context=context,
                    specification=specification.entity_specification,
                    generatable=value,
                )
    elif isinstance(specification, spec.ListSpecification):
        if not isinstance(generatable, gen.GeneratedList):
            import ipdb

            ipdb.set_trace()
            context.add_error(
                spec.ValidationError(
                    path=context.create_path(),
                    message=f"expected a list, found {generatable}",
                )
            )
            return
        generated_list = typing.cast(gen.GeneratedList, generatable)
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
        if not isinstance(generatable, gen.GeneratedObject):
            context.add_error(
                spec.ValidationError(
                    path=context.create_path(),
                    message=f"expected an object, found {generatable}",
                )
            )
            return
        generated_object = typing.cast(gen.GeneratedObject, generatable)
        for key, value in generated_object.children.items():
            child_specification = specification.children.get(key, None)
            with context.with_path(
                spec.GeneratablePathElement(key=key), generated=value
            ):
                validate_generated(
                    context=context,
                    specification=child_specification,
                    generatable=value,
                )
    else:
        logger.error(f"unknown specification {specification}")
        raise NotImplementedError()
