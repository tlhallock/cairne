from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union

from structlog import get_logger

logger = get_logger()


class JsonTokenType(Enum):
	BEGIN_OBJECT = auto()
	END_OBJECT = auto()
	BEGIN_ARRAY = auto()
	END_ARRAY = auto()
	NAME_SEPARATOR = auto()
	VALUE_SEPARATOR = auto()
	STRING = auto()
	NUMBER = auto()
	TRUE = auto()
	FALSE = auto()
	NULL = auto()


class StackStateType(Enum):
	IN_OBJECT = auto()
	IN_ARRAY = auto()


@dataclass
class StackState:
	state_type: StackStateType
	current_key: Optional[str] = None
	current_value: Union[None, dict, list, float, int, bool] = None


@dataclass
class ParseNextTokenResult:
	json_token_type: JsonTokenType
	string_value: Optional[str] = None
	number_value: Optional[float] = None


@dataclass
class ParsingContext:
	json_str: str
	position: int = field(default_factory=int)
	parsing_stack: List[StackState] = field(default_factory=list)

	def get_current_object(self) -> Any:
		if (
			len(self.parsing_stack) == 0
			or self.parsing_stack[-1].state_type != StackStateType.IN_OBJECT
		):
			return None
		return self.parsing_stack[-1].current_value

	def set_key(self, key: str):
		if (
			len(self.parsing_stack) == 0
			or self.parsing_stack[-1].state_type != StackStateType.IN_OBJECT
		):
			return
		self.parsing_stack[-1].current_key = key

	def get_current_key(self) -> Optional[str]:
		if (
			len(self.parsing_stack) == 0
			or self.parsing_stack[-1].state_type != StackStateType.IN_OBJECT
		):
			return None
		return self.parsing_stack[-1].current_key

	def add_value(self, value):
		if len(self.parsing_stack) == 0:
			return
		if self.parsing_stack[-1].state_type == StackStateType.IN_OBJECT:
			self.parsing_stack[-1].current_value[
				self.parsing_stack[-1].current_key
			] = value
		elif self.parsing_stack[-1].state_type == StackStateType.IN_ARRAY:
			self.parsing_stack[-1].current_value.append(value)
		else:
			return


def parse_string(context: ParsingContext) -> Optional[ParseNextTokenResult]:
	# TODO: save as much of the string as possible
	end_quote_pos = context.json_str.find('"', context.position + 1)
	while end_quote_pos != -1 and context.json_str[end_quote_pos - 1] == "\\":
		end_quote_pos = context.json_str.find('"', end_quote_pos + 1)
	if end_quote_pos == -1:
		# print(f"Could not find end quote for string starting at position {context.position}")
		return None
	ret = ParseNextTokenResult(
		JsonTokenType.STRING, context.json_str[context.position + 1 : end_quote_pos]
	)
	context.position = end_quote_pos + 1
	return ret


def parse_number(context: ParsingContext) -> Optional[ParseNextTokenResult]:
	end_pos = context.position + 1
	has_decimal_point = False
	has_exponent = False
	has_exponent_sign = False
	has_exponent_digits = False
	while end_pos < len(context.json_str):
		if context.json_str[end_pos].isdigit():
			if has_exponent:
				has_exponent_digits = True
			end_pos += 1
		elif context.json_str[end_pos] == ".":  # Decimal point
			if has_decimal_point:
				# print(f"Unexpected decimal point at position {end_pos}")
				return None
			has_decimal_point = True
			end_pos += 1
		elif context.json_str[end_pos] == "e" or context.json_str[end_pos] == "E":
			if has_exponent:
				# print(f"Unexpected exponent at position {end_pos}")
				return None
			has_exponent = True
			end_pos += 1
		elif context.json_str[end_pos] == "+" or context.json_str[end_pos] == "-":
			if not has_exponent or has_exponent_sign:
				# print(f"Unexpected sign at position {end_pos}")
				return None
			has_exponent_sign = True
			end_pos += 1
		else:
			break
	if has_exponent and not has_exponent_sign:
		# print(f"Expected sign at position {end_pos}")
		return None
	if has_exponent and not has_exponent_digits:
		# print(f"Expected digits at position {end_pos}")
		return None
	if has_decimal_point or has_exponent:
		ret = ParseNextTokenResult(
			JsonTokenType.NUMBER, float(context.json_str[context.position : end_pos])
		)
	else:
		ret = ParseNextTokenResult(
			JsonTokenType.NUMBER, int(context.json_str[context.position : end_pos])
		)
	context.position = end_pos
	return ret


def skip_whitespace(context: ParsingContext):
	while (
		context.position < len(context.json_str)
		and context.json_str[context.position].isspace()
	):
		context.position += 1


def parse_next_json_token(context: ParsingContext) -> Optional[ParseNextTokenResult]:
	skip_whitespace(context)
	if context.position >= len(context.json_str):
		return None

	char = context.json_str[context.position]

	if char == "{":
		context.position += 1
		return ParseNextTokenResult(JsonTokenType.BEGIN_OBJECT)
	elif char == "}":
		context.position += 1
		return ParseNextTokenResult(JsonTokenType.END_OBJECT)
	elif char == "[":
		context.position += 1
		return ParseNextTokenResult(JsonTokenType.BEGIN_ARRAY)
	elif char == "]":
		context.position += 1
		return ParseNextTokenResult(JsonTokenType.END_ARRAY)
	elif char == ":":
		context.position += 1
		return ParseNextTokenResult(JsonTokenType.NAME_SEPARATOR)
	elif char == ",":
		context.position += 1
		return ParseNextTokenResult(JsonTokenType.VALUE_SEPARATOR)
	elif char == '"':
		return parse_string(context)
	elif char == "t":
		if context.json_str[context.position : context.position + 4] == "true":
			# TODO: still return true if it is the end of the string
			context.position += 4
			return ParseNextTokenResult(JsonTokenType.TRUE)
		else:
			# print(f"Expected 'true' at position {context.position}")
			return None
	elif char == "f":
		if context.json_str[context.position : context.position + 5] == "false":
			context.position += 5
			# TODO: still return false if it is the end of the string
			return ParseNextTokenResult(JsonTokenType.FALSE)
		else:
			# print(f"Expected 'false' at position {context.position}")
			return None
	elif char == "n":
		if context.json_str[context.position : context.position + 4] == "null":
			context.position += 4
			return ParseNextTokenResult(JsonTokenType.NULL)
		else:
			# print(f"Expected 'null' at position {context.position}")
			return None
	elif char.isdigit() or char == "-":
		return parse_number(context)
	else:
		# print(f"Unexpected character {char} at position {context.position}")
		return None


def parse_incomplete_json(context: ParsingContext) -> Optional[Dict[str, Any]]:
	while True:
		result = parse_next_json_token(context)
		if result is None:
			break
		elif result.json_token_type == JsonTokenType.BEGIN_OBJECT:
			context.parsing_stack.append(StackState(StackStateType.IN_OBJECT))
		elif result.json_token_type == JsonTokenType.END_OBJECT:
			if (
				len(context.parsing_stack) == 0
				or context.parsing_stack[-1].state_type != StackStateType.IN_OBJECT
			):
				# print(f"Unexpected end of object at position {context.position}")
				return None
			context.parsing_stack.pop()
		elif result.json_token_type == JsonTokenType.BEGIN_ARRAY:
			context.parsing_stack.append(StackState(StackStateType.IN_ARRAY))
		elif result.json_token_type == JsonTokenType.END_ARRAY:
			if (
				len(context.parsing_stack) == 0
				or context.parsing_stack[-1].state_type != StackStateType.IN_ARRAY
			):
				# print(f"Unexpected end of array at position {context.position}")
				return None
			context.parsing_stack.pop()
		elif result.json_token_type == JsonTokenType.NAME_SEPARATOR:
			if (
				len(context.parsing_stack) == 0
				or context.parsing_stack[-1].state_type != StackStateType.IN_OBJECT
			):
				# print(f"Unexpected name separator at position {context.position}")
				return None
		elif result.json_token_type == JsonTokenType.VALUE_SEPARATOR:
			if (
				len(context.parsing_stack) == 0
				or context.parsing_stack[-1].state_type != StackStateType.IN_ARRAY
			):
				# print(f"Unexpected value separator at position {context.position}")
				return None
			context.parsing_stack[-1].current_key = None
		elif result.json_token_type == JsonTokenType.STRING:
			if len(context.parsing_stack) == 0:
				# print(f"Unexpected string at position {context.position}")
				return None
			if context.parsing_stack[-1].state_type == StackStateType.IN_OBJECT:
				context.parsing_stack[-1].current_key = result.string_value
			elif context.parsing_stack[-1].state_type == StackStateType.IN_ARRAY:
				context.parsing_stack[-1].current_value.append(result.string_value)
			else:
				# print(f"Unexpected string at position {context.position}")
				return None
		elif result.json_token_type == JsonTokenType.NUMBER:
			if len(context.parsing_stack) == 0:
				# print(f"Unexpected number at position {context.position}")
				return None
			if context.parsing_stack[-1].state_type == StackStateType.IN_OBJECT:
				context.parsing_stack[-1].current_key = result.number_value
			elif context.parsing_stack[-1].state_type == StackStateType.IN_ARRAY:
				context.parsing_stack[-1].current_value.append(result.number_value)
			else:
				# print(f"Unexpected number at position {context.position}")
				return None
	return context.get_current_object()


def test_tokenizer():
	invalid_json = """{"""
	context = ParsingContext(json_str=invalid_json, position=0, parsing_stack=[])
	result = parse_next_json_token(context=context)
	assert result == ParseNextTokenResult(JsonTokenType.BEGIN_OBJECT)
	result = parse_next_json_token(context=context)
	assert result is None

	invalid_json = """{"a" """
	context = ParsingContext(json_str=invalid_json, position=0, parsing_stack=[])
	result = parse_next_json_token(context=context)
	assert result == ParseNextTokenResult(JsonTokenType.BEGIN_OBJECT)
	result = parse_next_json_token(context=context)
	assert result.json_token_type == JsonTokenType.STRING
	assert result.string_value == "a"
	result = parse_next_json_token(context=context)
	assert result is None

	invalid_json = """{"a": false """
	context = ParsingContext(json_str=invalid_json, position=0, parsing_stack=[])
	result = parse_next_json_token(context=context)
	assert result == ParseNextTokenResult(JsonTokenType.BEGIN_OBJECT)
	result = parse_next_json_token(context=context)
	assert result.json_token_type == JsonTokenType.STRING
	assert result.string_value == "a"
	result = parse_next_json_token(context=context)
	assert result == ParseNextTokenResult(JsonTokenType.NAME_SEPARATOR)
	result = parse_next_json_token(context=context)
	assert result == ParseNextTokenResult(JsonTokenType.FALSE)
	result = parse_next_json_token(context=context)
	assert result is None


if __name__ == "__main__":
	# invalid_json = completion.choices[0].message.content
	invalid_json = """{"a": false, "b":\v1., "c": 1E-3, "d":\ttrue,\n"e": null,"f\\f": [1.45, 2e+2,"""
	context = ParsingContext(json_str=invalid_json, position=0, parsing_stack=[])
	while True:
		result = parse_next_json_token(context)
		if result is None:
			break
		print(
			result.json_token_type.name,
			result.string_value
			if result.string_value is not None
			else (result.number_value if result.number_value is not None else ""),
		)

	test_tokenizer()


# def parse_failed_json(json_str: str, position: int):
#     pass

# def parse_as_much_as_possible(json_str: str):
#     pass
