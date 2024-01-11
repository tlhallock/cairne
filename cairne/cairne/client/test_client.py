import json
from contextlib import contextmanager
from typing import Any, List, Optional, Union

import cairne.schema.characters as characters_schema
import cairne.schema.worlds as worlds_schema
import requests
from structlog import get_logger

logger = get_logger(__name__)


HOST = "http://localhost:5000"


@contextmanager
def temporary_world(name: str):
	create_request = worlds_schema.CreateWorldRequest(name=name)
	response = requests.post(
		f"{HOST}/world",
		json=create_request.model_dump(),
	)
	assert response.status_code == 200
	create_response = worlds_schema.CreateWorldResponse(**response.json())

	logger.debug("Created world", name=name, world_id=create_response.world_id)

	response = requests.get(f"{HOST}/world/{create_response.world_id}")
	assert response.status_code == 200
	get_response = worlds_schema.GetWorldResponse(**response.json())

	yield get_response.world

	delete_request = worlds_schema.DeleteWorldRequest(world_id=create_response.world_id)
	response = requests.delete(
		f"{HOST}/world",
		json=json.loads(delete_request.model_dump_json()),
	)
	assert response.status_code == 200
	delete_response = worlds_schema.DeleteWorldResponse(**response.json())
	assert delete_response.world_id == create_response.world_id


def find_world(
	worlds: List[worlds_schema.World], world_id: str
) -> Optional[worlds_schema.World]:
	for world in worlds:
		if world.world_id == world_id:
			return world
	return None


def test_list_worlds():
	with temporary_world("Test World") as world:
		found = find_world(worlds=[world], world_id=world.world_id)
		assert found is not None


def test_characters():
	with temporary_world(name="Test World") as world:
		request = characters_schema.CreateCharacterRequest(
			world_id=world.world_id,
			name="Test Character",
		)
		response = requests.post(
			f"{HOST}/world/{world.world_id}/characters",
			json=json.loads(request.model_dump_json()),
		)
		assert response.status_code == 200
		create_response = characters_schema.CreateCharacterResponse(**response.json())

		response = requests.get(
			f"{HOST}/world/{world.world_id}/characters/{create_response.character_id}"
		)
		assert response.status_code == 200
		character_response = characters_schema.GetCharacterResponse(**response.json())
		character = character_response.character
		logger.debug("Got character", character=character)

		response = requests.delete(
			f"{HOST}/world/{world.world_id}/characters/{create_response.character_id}"
		)
		assert response.status_code == 200
		delete_response = characters_schema.DeleteCharacterResponse(**response.json())
		assert delete_response.character_id == create_response.character_id


if __name__ == "__main__":
	test_list_worlds()
	test_characters()
