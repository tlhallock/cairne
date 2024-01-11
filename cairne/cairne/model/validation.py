

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union, Tuple
import uuid
from enum import Enum
import cairne.model.calls as calls
import datetime
from dataclasses import dataclass
import json
import cairne.parsing.parse_incomplete_json as parse_incomplete
from structlog import get_logger
from contextlib import contextmanager
import cairne.model.generated as gen
import typing

import cairne.model.specification as spec
import cairne.model.parsing as parsing


logger = get_logger(__name__)



@dataclass
class PathElement:
    key: str
    generated: gen.Generated


@dataclass
class ValidationContext(BaseModel):
    source: gen.GenerationSource = Field()
    current_path: List[PathElement] = Field(default_factory=list)
    errors: List[spec.ValidationError] = Field(default_factory=list)
    success: bool = Field(default=True)
    # validated?
    
    def create_path(self) -> str:
        return "".join(field.key for field in self.current_path)
    
    def add_error(self, error: spec.ValidationError) -> None:
        self.errors.append(error)
        self.success = False

    @contextmanager    
    def with_path(self, key: str, generated: gen.Generated):
        path_element = PathElement(key=key, generated=generated)
        self.current_path.append(path_element)
        yield
        self.current_path.pop()


    # required: bool = Field(default=True)
    # options: List[Tuple[Any, List[str]]]
    
# def parse_value(context: ValidationContext, spec: spec.OneOfLiteralValidator, generated: gen.GeneratedValue) -> None:
#     return None


def validate_nonnegative(context: ValidationContext, specification: spec.ValidatorSpecification, parsed: gen.GeneratedValue):
    if isinstance(parsed, gen.GeneratedFloat):
        float_value = typing.cast(gen.GeneratedFloat, parsed)
        parsed_float = float_value.parsed
        if parsed_float is None:
            return
        if parsed_float < 0:
            context.add_error(
                spec.ValidationError(
                    path=context.create_path(),
                    message=f"expected a positive float, found {parsed_float}"
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
                    message=f"expected a positive integer, found {parsed_integer}"
                )
            )
    else:
        context.add_error(
            spec.ValidationError(
                path=context.create_path(),
                message=f"expected an float or integer, found {parsed}"
            )
        )

def validate_name(context: ValidationContext, specification: spec.ValidatorSpecification, parsed: gen.Generated):
    pass

    
def validate_required(context: ValidationContext, specification: spec.ValidatorSpecification, parsed: gen.Generated):
    if not parsed.is_generated():
        context.add_error(
            spec.ValidationError(
                path=context.create_path(),
                message=f"field is required"
            )
        )
        return


def find_option(specification: spec.OneOfLiteralValidator, parsed: gen.GeneratedString) -> Optional[Any]:
    for option, representations in specification.options:
        for repr in representations:
            if repr.lower() == repr.lower():
                return option
    return None

def validate_one_of_literal(context: ValidationContext, specification: spec.OneOfLiteralValidator, parsed: gen.Generated):
    if not isinstance(parsed, gen.GeneratedString):
        context.add_error(
            spec.ValidationError(
                path=context.create_path(),
                message=f"expected a value, found {parsed}"
            )
        )
        return
    
    if not parsed.is_generated():
        context.add_error(
            spec.ValidationError(
                path=context.create_path(),
                message=f"enumerated field is required"
            )
        )
        return
    
    option = find_option(specification, parsed)
    if option is not None:
        parsed.result = option
        return
    
    options_list = ", ".join([f"'{r}'" for _, repr in specification.options for r in repr])
    context.add_error(
        spec.ValidationError(
            path=context.create_path(),
            message=f"field must be one of [{options_list}]"
        )
    )


def validate(context: ValidationContext, specification: spec.ValidatorSpecification, parsed: gen.Generated):
    if specification.validator_name == spec.ValidatorName.REQUIRED:
        validate_required(context, specification, parsed)
    elif specification.validator_name == spec.ValidatorName.ONE_OF_LITERAL:
        validate_one_of_literal(context, typing.cast(spec.OneOfLiteralValidator, specification), parsed)
    elif specification.validator_name == spec.ValidatorName.NAME:
        validate_name(context, specification, parsed)
    elif specification.validator_name == spec.ValidatorName.NONNEGATIVE:
        validate_nonnegative(context, specification, typing.cast(gen.GeneratedValue, parsed))
    else:
        logger.error(f"unknown validator {specification.validator_name}")
        raise NotImplementedError()

