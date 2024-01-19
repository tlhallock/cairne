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
import cairne.model.generated as gen
import cairne.model.specification as spec
import cairne.parsing.parse_incomplete_json as parse_incomplete

logger = get_logger(__name__)


# @dataclass
# class ParseResult:
#     errors: List[ValidationError]
#     success: bool


class PathElement(BaseModel):
    key: str = Field()
    generated: gen.Generated = Field()


class ParseContext(BaseModel):
    source: gen.GenerationSource = Field()
    current_path: List[str] = Field(default_factory=list)
    errors: List[spec.ValidationError] = Field(default_factory=list)
    success: bool = Field(default=True)
    # parsed?

    def create_metadata(self) -> gen.GenerationMetadata:
        return gen.GenerationMetadata(source=self.source)

    def create_path(self) -> str:
        return "".join(elem for elem in self.current_path)

    def add_error(self, error: spec.ValidationError) -> None:
        self.errors.append(error)
        self.success = False

    @contextmanager
    def with_path(self, key: str):
        self.current_path.append(key)
        yield
        self.current_path.pop()


# class BaseValueParser(Parser):
# def parse_value(self, context: ParseContext, generated: gen.GeneratedValue) -> None:
#     raise NotImplementedError()

# def parse(self, context: ParseContext, generated: gen.Generated) -> None:
#     if not isinstance(generated, gen.GeneratedValue):
#         context.add_error(
#             ValidationError(
#                 path=context.create_path(),
#                 message=f"expected a value, found {generated}"
#             )
#         )
#         return
#     value = typing.cast(gen.GeneratedValue, generated)
#     self.parse_value(context, value)

# def create_empty_element(self) -> gen.Generated:
#     return gen.GeneratedValue()


# class BaseListParser(Parser):
#     def parse_list(self, context: ParseContext, generated: gen.GeneratedList) -> None:
#         raise NotImplementedError()

#     def parse(self, context: ParseContext, generated: gen.Generated) -> None:
#         if not isinstance(generated, gen.GeneratedList):
#             context.add_error(
#                 ValidationError(
#                     path=context.create_path(),
#                     message=f"expected a list, found {generated}"
#                 )
#             )
#             return
#         value = typing.cast(gen.GeneratedList, generated)
#         self.parse_list(context, value)

#     def create_empty_element(self) -> gen.Generated:
#         return gen.GeneratedList()


# class BaseObjectParser(Parser):
#     def parse_object(self, context: ParseContext, generated: gen.GeneratedObject) -> None:
#         raise NotImplementedError()

#     def parse(self, context: ParseContext, generated: gen.Generated) -> None:
#         if not isinstance(generated, gen.GeneratedObject):
#             context.add_error(
#                 ValidationError(
#                     path=context.create_path(),
#                     message=f"expected an object, found {generated}"
#                 )
#             )
#             return
#         value = typing.cast(gen.GeneratedObject, generated)
#         self.parse_object(context, value)

#     def create_empty_element(self) -> gen.Generated:
#         return gen.GeneratedObject()


def parse_string(
    context: ParseContext, specification: spec.ValueSpecification, raw: Any
) -> gen.GeneratedString:
    normalized: Optional[str] = None
    if isinstance(raw, str):
        normalized = raw
    elif raw is not None:
        normalized = str(raw)

    return gen.GeneratedString(
        metadata=context.create_metadata(),
        raw=raw,
        parsed=normalized,
    )


def parse_float(
    context: ParseContext, specification: spec.ValueSpecification, raw: Any
) -> gen.GeneratedFloat:
    normalized: Optional[float] = None
    if isinstance(raw, float):
        normalized = raw
    elif isinstance(raw, int):
        normalized = float(raw)
    elif isinstance(raw, str):
        try:
            normalized = float(raw)
        except ValueError:
            pass

    return gen.GeneratedFloat(
        metadata=context.create_metadata(),
        raw=raw,
        parsed=normalized,
    )


def parse_integer(
    context: ParseContext, specification: spec.ValueSpecification, raw: Any
) -> gen.GeneratedInteger:
    normalized: Optional[int] = None
    if isinstance(raw, int):
        normalized = raw
    elif isinstance(raw, float):
        normalized = int(raw)
    elif isinstance(raw, str):
        try:
            normalized = int(raw)
        except ValueError:
            pass

    return gen.GeneratedInteger(
        metadata=context.create_metadata(),
        raw=raw,
        parsed=normalized,
    )


def prefixes(s: str) -> List[str]:
    return [s[:i] for i in range(len(s) + 1)]


def parse_boolean(
    context: ParseContext, specification: spec.ValueSpecification, raw: Any
) -> gen.GeneratedBoolean:
    normalized: Optional[bool] = None
    if isinstance(raw, bool):
        normalized = raw
    elif isinstance(raw, str):
        if raw.lower() in ["1"] + prefixes("true") + prefixes("yes"):
            normalized = True
        elif raw.lower() in ["0"] + prefixes("false") + prefixes("no") + prefixes(
            "null"
        ) + prefixes("none"):
            normalized = False

    return gen.GeneratedBoolean(
        metadata=context.create_metadata(),
        raw=raw,
        parsed=normalized,
    )


def parse_dict(context: ParseContext, raw: Any) -> Optional[Dict[str, Any]]:
    if raw is None:
        return None
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            logger.error("Failed to parse json", raw_input=raw)

        try:
            incomplete_context = parse_incomplete.ParsingContext(json_str=raw)
            return parse_incomplete.parse_incomplete_json(incomplete_context)
        except Exception as e:
            logger.error("Failed to parse incomplete json", raw_input=raw, error=e)

    context.add_error(
        spec.ValidationError(
            path=context.create_path(),
            message=f"field must be a valid json object, found {type(raw)}",
        )
    )
    return None


def get_child_input(
    context: ParseContext, dict_value: Optional[Dict[str, Any]], key: str
) -> Any:
    if dict_value is None:
        return None
    # TODO: check if the key is somewhere else in the dict
    return dict_value.get(key, None)


def parse_object(
    context: ParseContext, specification: spec.ObjectSpecification, raw: Any
) -> gen.GeneratedObject:
    dict_value = parse_dict(context, raw)
    if dict_value is None:
        dict_value = {}

    children: Dict[str, gen.Generated] = {}
    for key, child_spec in specification.children.items():
        child_input = get_child_input(context, dict_value, key)
        with context.with_path(key=f".{key}"):
            child = parse(context, child_spec, child_input)
        children[key] = child

    kwargs = dict(
        metadata=context.create_metadata(),
        raw=raw,
        parsed=dict_value,
        children=children,
    )
    if "entity_id" in dict_value:
        kwargs["entity_id"] = uuid.UUID(dict_value["entity_id"])

    if specification.parser.parser_name == spec.ParserName.ENTITY:
        entity_specification = typing.cast(spec.EntitySpecification, specification)
        kwargs["entity_type"] = entity_specification.entity_type
        return gen.GeneratedEntity(**kwargs)
    elif specification.parser.parser_name == spec.ParserName.OBJECT:
        return gen.GeneratedObject(**kwargs)
    else:
        raise NotImplementedError(
            f"Unknown parser name: {specification.parser.parser_name}"
        )


def parse_entity_dictionary(
    context: ParseContext, specification: spec.EntityDictionarySpecification, raw: Any
) -> gen.EntityDictionary:
    if raw is None:
        raw = {}
    assert isinstance(raw, dict)

    # dict_value = parse_dict(context, raw)
    if raw is None:
        return

    entities: Dict[uuid.UUID, gen.GeneratedEntity] = {}
    for key, child_input in raw.items():
        entity_uuid = uuid.UUID(key)

        with context.with_path(key=f'["{uuid}"]'):
            untyped_child = parse(
                context, specification.entity_specification, child_input
            )
            child = typing.cast(gen.GeneratedEntity, untyped_child)
        entities[entity_uuid] = child

    return gen.EntityDictionary(
        metadata=context.create_metadata(),
        raw=raw,
        entities=entities,
    )


def parse_js_list(context: ParseContext, raw: Any) -> Optional[List[Any]]:
    if raw is None:
        return None

    if isinstance(raw, list):
        return raw

    if isinstance(raw, str):
        if raw == "":
            return []
        try:
            ret = json.loads(raw)
            if isinstance(ret, list):
                return ret
        except json.JSONDecodeError:
            logger.error("Failed to parse json", raw=raw)

        try:
            incomplete_context = parse_incomplete.ParsingContext(json_str=raw)
            ret = parse_incomplete.parse_incomplete_json(incomplete_context)
            if isinstance(ret, list):
                return ret
        except Exception as e:
            logger.error("Failed to parse incomplete json", raw_input=raw, error=e)
        # Could try splitting the string based on ","

    return None


def parse_list(
    context: ParseContext, specification: spec.ListSpecification, raw: Any
) -> gen.GeneratedList:
    parsed = parse_js_list(context, raw)
    if parsed:
        elements = []
        for index, raw_element in enumerate(parsed):
            with context.with_path(key=f"[{index}]"):
                element = parse(
                    context, specification.element_specification, raw_element
                )
            elements.append(element)
    else:
        elements = []

    return gen.GeneratedList(
        metadata=context.create_metadata(),
        raw=raw,
        parsed=parsed,
        elements=elements,
    )


def parse(
    context: ParseContext, specification: spec.GeneratableSpecification, raw: Any
) -> gen.Generated:
    if specification.parser.parser_name == spec.ParserName.LIST:
        if not isinstance(specification, spec.ListSpecification):
            raise ValueError(f"Expected ListSpecification, found {specification}")
        list_spec = typing.cast(spec.ListSpecification, specification)
        return parse_list(context, list_spec, raw)
    elif specification.parser.parser_name == spec.ParserName.OBJECT:
        if not isinstance(specification, spec.ObjectSpecification):
            raise ValueError(f"Expected ObjectSpecification, found {specification}")
        object_spec = typing.cast(spec.ObjectSpecification, specification)
        return parse_object(context, object_spec, raw)
    elif specification.parser.parser_name == spec.ParserName.ENTITY:
        if not isinstance(specification, spec.EntitySpecification):
            raise ValueError(f"Expected EntitySpecification, found {specification}")
        entity_spec = typing.cast(spec.EntitySpecification, specification)
        return parse_object(context, entity_spec, raw)
    elif specification.parser.parser_name == spec.ParserName.ENTITY_DICTIONARY:
        if not isinstance(specification, spec.EntityDictionarySpecification):
            raise ValueError(
                f"Expected EntityDictionarySpecification, found {specification}"
            )
        entity_dict_spec = typing.cast(
            spec.EntityDictionarySpecification, specification
        )
        return parse_entity_dictionary(context, entity_dict_spec, raw)
    elif specification.parser.parser_name == spec.ParserName.STRING:
        if not isinstance(specification, spec.ValueSpecification):
            raise ValueError(f"Expected ValueSpecification, found {specification}")
        str_spec = typing.cast(spec.ValueSpecification, specification)
        return parse_string(context, str_spec, raw)
    elif specification.parser.parser_name == spec.ParserName.FLOAT:
        if not isinstance(specification, spec.ValueSpecification):
            raise ValueError(f"Expected ValueSpecification, found {specification}")
        value_spec = typing.cast(spec.ValueSpecification, specification)
        return parse_float(context, value_spec, raw)
    elif specification.parser.parser_name == spec.ParserName.INTEGER:
        if not isinstance(specification, spec.ValueSpecification):
            raise ValueError(f"Expected ValueSpecification, found {specification}")
        value_spec = typing.cast(spec.ValueSpecification, specification)
        return parse_integer(context, value_spec, raw)
    elif specification.parser.parser_name == spec.ParserName.BOOLEAN:
        if not isinstance(specification, spec.ValueSpecification):
            raise ValueError(f"Expected ValueSpecification, found {specification}")
        value_spec = typing.cast(spec.ValueSpecification, specification)
        return parse_boolean(context, value_spec, raw)
    else:
        raise NotImplementedError()
