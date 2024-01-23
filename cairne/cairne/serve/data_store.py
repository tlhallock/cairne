import json
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field
from structlog import get_logger

import threading
import cairne.model.generated as generated_model
import cairne.model.generation as generate_model
import cairne.model.templates as template_model


logger = get_logger()


SAVE_PATH = "output/datastore.json"



class Datastore(BaseModel):
    worlds: Dict[uuid.UUID, generated_model.GeneratedEntity] = Field(
        default_factory=dict
    )
    generation_templates: Dict[uuid.UUID, template_model.GenerationTemplate] = Field(default_factory=dict)
    generations: Dict[uuid.UUID, generate_model.Generation] = Field(default_factory=dict)
    
    generation_threads: Dict[uuid.UUID, threading.Thread] = Field(default_factory=dict, exclude=True)

    @staticmethod
    def load() -> "Datastore":
        with open(SAVE_PATH, "r") as f:
            js = f.read()
        datastore = Datastore.model_validate_json(js)
        return datastore

    def save(self):
        js = self.model_dump_json(indent=2)
        with open(SAVE_PATH, "w") as f:
            f.write(js)
    
    
    class Config:
        arbitrary_types_allowed = True
