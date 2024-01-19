import json
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from flask_pydantic import validate
from pydantic import BaseModel, Field
from structlog import get_logger

import cairne.model.generated as model_generated

SAVE_PATH = "output/datastore.json"

from cairne.model.generated import Generated


class Datastore(BaseModel):
    worlds: Dict[uuid.UUID, model_generated.GeneratedEntity] = Field(
        default_factory=dict
    )
    generations: Dict[uuid.UUID, Any] = Field(default_factory=dict)
    generation_threads: Dict[uuid.UUID, Any] = Field(default_factory=dict, ignore=True)

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
