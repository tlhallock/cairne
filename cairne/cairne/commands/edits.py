import datetime
import json
import typing
import uuid
from dataclasses import dataclass, field
from typing import Optional, Tuple, Union

from pydantic import BaseModel, Field
from structlog import get_logger

import cairne.commands.export as export
import cairne.model.character as characters
import cairne.model.generated as generated_model
import cairne.model.parsing as parsing
import cairne.model.specification as spec
import cairne.schema.edits as edits_schema
import cairne.schema.generated as generated_schema
from cairne.commands.base import Command
from cairne.model.world_spec import WORLD

logger = get_logger()


class PathSplit(BaseModel):
    parent_path: spec.GeneratablePath = Field()
    key: spec.GeneratablePathElement = Field()


def split_path(path: spec.GeneratablePath) -> PathSplit:
    if len(path.path_elements) == 0:
        print("uh oh")
    path_elements = path.model_copy(deep=True).path_elements

    return PathSplit(
        parent_path=spec.GeneratablePath(path_elements=path_elements[:-1]),
        key=path_elements[-1],
    )


@dataclass
class Edit(Command):
    def parse(
        self,
        request: Union[edits_schema.ReplaceRequest, edits_schema.AppendElementRequest],
        specification: Optional[spec.GeneratableSpecification] = None,
    ) -> generated_model.Generated:
        if specification is None:
            specification = WORLD.get(request.path, 0)
        raw_value = json.loads(request.value_js)

        source_type = generated_model.GenerationSourceType.USER_EDIT
        source = generated_model.GenerationSource(source_type=source_type)
        context = parsing.ParseContext(source=source)
        generated = parsing.parse(
            context=context, specification=specification, raw=raw_value
        )
        return generated


@dataclass
class ReplaceValue(Edit):
    request: edits_schema.ReplaceRequest

    def execute(self) -> edits_schema.ReplaceResponse:
        world = self.datastore.worlds.get(self.request.world_id, None)
        if world is None:
            raise ValueError(f"World not found: {self.request.world_id}")

        path_split = split_path(self.request.path)
        parent = world.get(path_split.parent_path, 0)
        generated = self.parse(self.request)
        parent.replace_child(path_split.key, generated)
        self.datastore.save()

        return edits_schema.ReplaceResponse()


@dataclass
class AppendValue(Edit):
    request: edits_schema.AppendElementRequest

    def execute(self) -> edits_schema.AppendElementResponse:
        world = self.datastore.worlds.get(self.request.world_id, None)
        if world is None:
            raise ValueError(f"World not found: {self.request.world_id}")

        parent = world.get(self.request.path, 0)
        if not isinstance(parent, generated_model.GeneratedList):
            raise ValueError(f"Cannot append to non-list: {self.request.path}")

        specification = WORLD.get(self.request.path, 0)
        if not isinstance(specification, spec.ListSpecification):
            raise ValueError(f"Cannot append to non-list: {self.request.path}")

        # TODO: is this necessary?
        # list_parent = typing.cast(generated_model.GeneratedList, parent)

        generated = self.parse(
            self.request, specification=specification.element_specification
        )
        parent.append_child(generated)
        self.datastore.save()

        return edits_schema.AppendElementResponse()


@dataclass
class RemoveValue(Command):
    request: edits_schema.RemoveValueRequest

    def execute(self) -> edits_schema.RemoveValueResponse:
        # world = self.datastore.worlds.get(self.request.world_id, None)
        # if world is None:
        #     raise ValueError(f"World not found: {self.request.world_id}")

        # located_entity = world.search_for_entity(self.request.entity_id, path=generated_model.GeneratablePath(path_elements=[]))
        # if located_entity is None:
        #     raise ValueError(f"Entity not found: {self.request.entity_id}")

        # located_entity.entity.deletion = generated_model.Deletion(
        #     date=datetime.datetime.now(),
        #     deleted_by="test",
        # )
        # self.datastore.save()
        logger.info("TODO: implement remove value", request=self.request)

        return edits_schema.RemoveValueResponse()
