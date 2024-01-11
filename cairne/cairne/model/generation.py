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

logger = get_logger(__name__)


class GenerationEndpoint(str, Enum):
	CHARACTER = "character"
	CHARACTERS = "characters"


class MessageSourceRole(str, Enum):
	SYSTEM = "system"
	USER = "user"
	ASSISTANT = "assistant"


class GenerationMessage(BaseModel):
	source: MessageSourceRole = Field()
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
	IMAGE = "image"
	AUDIO = "audio"


class GeneratorModel(BaseModel):
	generator_type: GeneratorType = Field()
	g_model_id: str = Field()


class GenerationRequestParameters(BaseModel):
	max_tokens: Optional[int] = Field(default=None)
	temperature: Optional[float] = Field(default=None)
	top_p: Optional[float] = Field(default=None)
	frequency_penalty: Optional[float] = Field(default=None)
	presence_penalty: Optional[float] = Field(default=None)


class Generation(BaseModel):
	generation_id: uuid.UUID = Field(default_factory=uuid.uuid4)
	endpoint: GenerationEndpoint = Field()
	generation_type: GenerationType = Field()
	generator_model: GeneratorModel = Field()
	# request...

	begin_time: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
	end_time: Optional[datetime.datetime] = Field(default=None)
	status: GenerationStatus = Field(default=GenerationStatus.QUEUED)

	# assumes a chat model...
	prompt_messages: List[GenerationMessage] = Field(default_factory=list)
	json_schema: Optional[str] = Field(default=None)

	parameters: GenerationRequestParameters = Field(
		default_factory=GenerationRequestParameters
	)
	input_tokens: Optional[int] = Field(default=None)
	output_tokens: Optional[int] = Field(default=None)


class Instruction(BaseModel):
	message: str = Field()

	# def format(self, world: Gen
