
from dataclasses import dataclass, field
from cairne.serve.data_store import Datastore
from cairne.schema.base import Response


@dataclass
class Command:
    datastore: Datastore
    user: str

    def execute(self) -> Response:
        """
        Execute the command.
        """
        raise NotImplementedError()
