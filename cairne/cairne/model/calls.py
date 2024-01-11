

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union, Tuple
import uuid
from enum import Enum
import datetime



class LanguageModelType(str, Enum):
    OPENAI = "openai"
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"


class LanguageModel(BaseModel):
    language_model_type: LanguageModelType
    model_id: str
    # transformer


class ModelCallType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"


class ModelCall(BaseModel):
    call_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    model_call_type: ModelCallType
    language_model: LanguageModel
    begin_time: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    end_time: Optional[datetime.datetime] = Field(default=None)
    prompt: str
    response: Optional[str]
    
    json_schema: Optional[str]
    input_tokens: Optional[int]
    output_tokens: Optional[int]
    
    