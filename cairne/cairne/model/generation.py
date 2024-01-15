import datetime
import json
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

import cairne.model.calls as calls
import cairne.parsing.parse_incomplete_json as parse_incomplete
from pydantic import BaseModel, Field
from structlog import get_logger
import string
import cairne.model.specification as spec


# TODO: rename this file to generate?

logger = get_logger(__name__)


class GenerationEndpoint(str, Enum):
	CHARACTER = "character"
	CHARACTERS = "characters"


class ChatRole(str, Enum):
	SYSTEM = "system"
	ASSISTANT = "assistant"
	USER = "user"


class GenerationChatMessage(BaseModel):
	role: ChatRole = Field()
	message: str = Field()


class GenerationStatus(str, Enum):
	QUEUED = "queued"
	IN_PROGRESS = "in_progress"
	STREAMING = "streaming"
	ERROR = "error"
	COMPLETE = "complete"


class GenerationStopReason(str, Enum):
	SUCCESS = "success"
	RATE_LIMIT = "rate_limit"
	CONTENT_FILTER = "content_filter"
	TIMEOUT = "timeout"
	ERROR = "error"


class GeneratorType(str, Enum):
	OLLAMA = "ollama"
	OPENAI = "openai"
	HUGGING_FACE = "hugging_face"


class GenerationType(str, Enum):
	TEXT = "text"
	# Should I have a different type for json?
	IMAGE = "image"
	AUDIO = "audio"


class JsonStructure(BaseModel):
	json_schema: Optional[str] = Field(default=None)
	examples: Optional[str] = Field(default=None)


class GeneratorModel(BaseModel):
	generator_type: GeneratorType = Field()
	g_model_id: str = Field()


class GenerationRequestParameters(BaseModel):
	max_tokens: Optional[int] = Field(default=None)
	temperature: Optional[float] = Field(default=None)
	top_p: Optional[float] = Field(default=None)
	frequency_penalty: Optional[float] = Field(default=None)
	presence_penalty: Optional[float] = Field(default=None)
	seed: Optional[int] = Field(default=None)


class Instruction(BaseModel):
	message: str = Field()
 
	def format(self, variables: Dict[str, str]) -> str:
		return self.message.format(**variables)


class GenerationVariables(BaseModel):
	variables: Dict[str, str] = Field(default_factory=dict)
 
	@classmethod
	def get_required_variables(cls, prompt: str) -> List[str]:
		return [arg[1] for arg in string.Formatter().parse(prompt) if arg[1] is not None]

	def can_evaluate(self, instruction: Instruction) -> bool:
		for req in GenerationVariables.get_required_variables(instruction.message):
			if req in self.variables:
				continue
			return False
		return True	


	# TODO: maybe a filled instruction is different?
	def format(self, unfilled_instructions: List[Instruction]) -> List[Instruction]:
		filled_instructions = []
		# Should this be a set?
		remaining_instructions = unfilled_instructions.copy()

		while True:
			to_remove: List[Instruction] = []
			for instruction in unfilled_instructions:
				if self.can_evaluate(instruction):
					to_remove.append(instruction)
					formatted = instruction.format(self.variables)
					# self.variables[variable.name] = variable.value.format(**variables)
					filled_instructions.append(Instruction(message=formatted))
			for instruction in to_remove:
				remaining_instructions.remove(instruction)
			if len(remaining_instructions) == 0:
				break
		if len(remaining_instructions) > 0:
			logger.warning(f"Could not fill instructions: {remaining_instructions}")
		return filled_instructions


class TargetFields(BaseModel):
	all: Optional[bool] = Field(default=None)
	fields: List[str] = Field(default_factory=list)




class Generation(BaseModel):
	# assumes a chat model...
 
	generation_id: uuid.UUID = Field(default_factory=uuid.uuid4)
	world_id: uuid.UUID = Field()
	entity_id: uuid.UUID = Field()
	generation_type: GenerationType = Field()
	entity_type: spec.EntityType = Field()
 
	generator_model: GeneratorModel = Field()
	parameters: GenerationRequestParameters = Field(default_factory=GenerationRequestParameters)
 
	prompt_messages: List[GenerationChatMessage] = Field(default=None)
	filled_instructions: List[Instruction] = Field(default=None)
	generation_variables: GenerationVariables = Field(default_factory=GenerationVariables)
	json_structure: Optional[JsonStructure] = Field(default=None)
 
	
	# endpoint: GenerationEndpoint = Field()
	# request...

	begin_time: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
	end_time: Optional[datetime.datetime] = Field(default=None)
	# Time for llm calls as separate fields?
	status: GenerationStatus = Field(default=GenerationStatus.QUEUED)

	input_tokens: Optional[int] = Field(default=None)
	output_tokens: Optional[int] = Field(default=None)

	# Need to store the result
	# TODO: need to store the location to put the result? world id, entity id