import datetime
import json
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field
from structlog import get_logger

import cairne.model.calls as calls
import cairne.parsing.parse_incomplete_json as parse_incomplete


class DialogueActionType(str, Enum):
    PLOT_TRIGGER = "plot_trigger"
    TRADE = "trade"
    BATTLE = "battle"
    END_DIALOGUE = "end_dialogue"
    CHANGE_OPINION = "change_stance"
    SET_AI_FOLLOW = "set_ai"


class DialogueAction(BaseModel):
    dialoge_action_type: DialogueActionType = Field()


class DialogueConditionType(str, Enum):
    HAS_ITEM = "has_item"
    HAS_RELATIONSHIP = "has_relationship"
    LOCATION = "location"
    HAS_PLOT_STAGE = "has_plot_stage"
    # information revealed?
    # someone still alive/dead?


class DialogueCondition(BaseModel):
    dialogue_condition_type: DialogueConditionType = Field()


class DialogeOption(BaseModel):
    label: str = Field()
    text: str = Field()
    actions: List[DialogueAction] = Field(default_factory=list)
    next_node: Optional[uuid.UUID] = Field()
    conditions: List[DialogueCondition] = Field(default_factory=list)
    weight: float = Field(default=1.0)  # ?
    narration: Optional[str] = Field()


class DialogueNode(BaseModel):
    node_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    participant: uuid.UUID = Field()
    text: str = Field()
    options: List[DialogeOption] = Field(default_factory=list)


class Dialogue(BaseModel):
    dialoge_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    nodes: Dict[uuid.UUID, DialogueNode] = Field(default_factory=dict)
    introduction_node: uuid.UUID = Field()
    default_node: uuid.UUID = Field()
