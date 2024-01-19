import json
from contextlib import contextmanager
from typing import Any, Generator, List, Optional, Union

import requests
from structlog import get_logger

import cairne.model.specification as spec
import cairne.schema.generate as generate_schema
import cairne.schema.generated as generated_schema
import cairne.schema.worlds as worlds_schema
import cairne.model.generation as generation_model
import time

logger = get_logger(__name__)


HOST = "http://localhost:5000"


@contextmanager
def temporary_world(
    name: str,
) -> Generator[generated_schema.GeneratedEntity, None, None]:
    create_request = worlds_schema.CreateWorldRequest(name=name)
    response = requests.post(
        f"{HOST}/world",
        json=create_request.model_dump(),
    )
    assert response.status_code == 200
    create_response = generated_schema.CreateEntityResponse.model_validate(response.json())

    world_id = create_response.entity_id
    logger.debug("Created world", name=name, world_id=world_id)

    response = requests.get(f"{HOST}/world/{world_id}")
    assert response.status_code == 200
    get_response = generated_schema.GetEntityResponse.model_validate(response.json())

    yield get_response.entity

    response = requests.delete(f"{HOST}/world/{get_response.entity.entity_id}")
    assert response.status_code == 200
    delete_response = generated_schema.DeleteEntityResponse.model_validate(response.json())
    # assert delete_response.world_id == create_response.world_id


def find_world(
    worlds: List[generated_schema.GeneratedEntity], world_id: str
) -> Optional[generated_schema.GeneratedEntity]:
    for world in worlds:
        if world.name is None:
            logger.error("Found invalid world", world=world)
        if world.entity_id == world_id:
            return world
    return None


def test_list_worlds():
    with temporary_world("Test World") as world:
        response = requests.get(f"{HOST}/worlds")
        list_response = generated_schema.ListEntitiesResponse.model_validate(response.json())
        assert response.status_code == 200

        found = find_world(worlds=list_response.entities, world_id=world.entity_id)
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
        create_response = generated_schema.CreateEntityResponse.model_validate(response.json())

        response = requests.get(
            f"{HOST}/world/{world.entity_id}/entity/{create_response.entity_id}"
        )
        assert response.status_code == 200
        character_response = generated_schema.GetEntityResponse.model_validate(response.json())

        character = character_response.entity
        logger.debug("Got character", character=character)

        generate_request = generate_schema.GenerateRequest(
            world_id=world.entity_id,
            entity_id=character.entity_id,
        )
        """
	fields_to_generate: Optional[generation_model.TargetFields] = Field(default=None)
 
	generator_model: Optional[generation_model.GeneratorModel] = Field(default=None)
	parameters: Optional[generation_model.GenerationRequestParameters] = Field(default=None)
 
	prompt_messages: Optional[List[generation_model.GenerationChatMessage]] = Field(default=None)
	instructions: Optional[List[generation_model.Instruction]] = Field(default=None)
	json_structure: Optional[JsonStructureRequest] = Field(default=None)
		"""
        response = requests.post(
            f"{HOST}/generate",
            json=json.loads(generate_request.model_dump_json()),
        )
        assert response.status_code == 200
        generate_response = generate_schema.GenerateResponse.model_validate(response.json())
        
        generation_id = generate_response.generation_id
        while True:
            response = requests.get(f"{HOST}/generation/{generation_id}")
            assert response.status_code == 200
            
            time.sleep(5)
            
            generation_response = generate_schema.GetGenerationResponse.model_validate(response.json())
            generation = generation_response.generation
            
            if generation.status in [
                generation_model.GenerationStatus.COMPLETE,
                generation_model.GenerationStatus.ERROR,
            ]:
                logger.debug("Generation complete", generation=generation)
                break
            
            logger.debug("Waiting for generation", status=generation.status)

        response = requests.delete(
            f"{HOST}/world/{world.entity_id}/entity/{create_response.entity_id}"
        )
        assert response.status_code == 200
        delete_response = generated_schema.DeleteEntityResponse.model_validate(response.json())
        # assert delete_response.character_id == create_response.character_id


if __name__ == "__main__":
    test_list_worlds()
    test_characters()
