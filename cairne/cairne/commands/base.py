from dataclasses import dataclass, field

from cairne.schema.base import Response
from cairne.serve.data_store import Datastore


@dataclass
class Command:
	datastore: Datastore
	user: str

	def execute(self) -> Response:
		"""
		Execute the command.
		"""
		raise NotImplementedError()
