import json
from contextlib import contextmanager
from typing import Any, List, Optional, Union, Generator

import cairne.schema.worlds as worlds_schema
import cairne.schema.generated as generated_schema
import cairne.model.specification as spec
import requests
from structlog import get_logger

logger = get_logger(__name__)


HOST = "http://localhost:5000"


@contextmanager
def temporary_world(name: str) -> Generator[generated_schema.GeneratedEntity, None, None]:
	create_request = worlds_schema.CreateWorldRequest(name=name)
	response = requests.post(
		f"{HOST}/world",
		json=create_request.model_dump(),
	)
	assert response.status_code == 200
	create_response = generated_schema.CreateEntityResponse(**response.json())

	world_id = create_response.entity_id
	logger.debug("Created world", name=name, world_id=world_id)

	response = requests.get(f"{HOST}/world/{world_id}")
	assert response.status_code == 200
	get_response = generated_schema.GetEntityResponse(**response.json())

	yield get_response.entity

	response = requests.delete(f"{HOST}/world/{get_response.entity.entity_id}")
	assert response.status_code == 200
	delete_response = generated_schema.DeleteEntityResponse(**response.json())
	# assert delete_response.world_id == create_response.world_id


def find_world(
	worlds: List[generated_schema.GeneratedEntity], world_id: str
) -> Optional[generated_schema.GeneratedEntity]:
	for world in worlds:
		if world.entity_id == world_id:
			return world
	return None


def test_list_worlds():
	with temporary_world("Test World") as world:
		found = find_world(worlds=[world], world_id=world.entity_id)
		assert found is not None


def test_characters():
	with temporary_world(name="Test World") as world:
		request = generated_schema.CreateEntityRequest(
			world_id=world.entity_id,
			entity_type=spec.EntityType.CHARACTER,
			name="Test Character",
		)
		response = requests.post(
			f"{HOST}/world/{world.entity_id}/entities/{spec.EntityType.CHARACTER.value}",
			json=json.loads(request.model_dump_json()),
		)
		assert response.status_code == 200
		create_response = generated_schema.CreateEntityResponse(**response.json())

		response = requests.get(f"{HOST}/world/{world.entity_id}/entity/{create_response.entity_id}")
		assert response.status_code == 200
		character_response = generated_schema.GetEntityResponse(**response.json())
  
		character = character_response.entity
		logger.debug("Got character", character=character)

		response = requests.delete(f"{HOST}/world/{world.entity_id}/entity/{create_response.entity_id}")
		assert response.status_code == 200
		delete_response = generated_schema.DeleteEntityResponse(**response.json())
		# assert delete_response.character_id == create_response.character_id


if __name__ == "__main__":
	test_list_worlds()
	test_characters()
