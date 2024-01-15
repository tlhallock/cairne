# from pydantic2ts import generate_typescript_defs
import json
import os

from pydantic import BaseModel, Field
from pydantic.json_schema import models_json_schema


class Response(BaseModel):
	pass


# ENTITY_ID = str
# DATE = str


# def generate_typescript():
#     generate_typescript_defs(

#             "cairne.schema.worlds"
#         ,
#         "ashkavor/src/openrpg/schema/schema.tsx",
#     )


def generate_json_schema():
	import cairne.schema.edits
	import cairne.schema.generate
	import cairne.schema.generated
	import cairne.schema.loaded_models
	import cairne.schema.worlds

	models = [        cairne.schema.edits.AppendElementRequest,
        cairne.schema.edits.AppendElementResponse,
        cairne.schema.edits.RemoveValueRequest,
        cairne.schema.edits.RemoveValueResponse,
        cairne.schema.edits.ReplaceRequest,
        cairne.schema.edits.ReplaceResponse,
        cairne.schema.generate.ApplyGenerationRequest,
        cairne.schema.generate.ApplyGenerationResponse,
        cairne.schema.generate.CancelGenerationRequest,
        cairne.schema.generate.CancelGenerationResponse,
        cairne.schema.generate.GenerateRequest,
        cairne.schema.generate.GenerateResponse,
        cairne.schema.generate.Generation,
        cairne.schema.generate.GenerationListItem,
        cairne.schema.generate.GetGenerationResponse,
        cairne.schema.generate.JsonStructureRequest,
        cairne.schema.generate.ListGenerationsResponse,
        cairne.schema.generated.CreateEntityRequest,
        cairne.schema.generated.CreateEntityResponse,
        cairne.schema.generated.DeleteEntityRequest,
        cairne.schema.generated.DeleteEntityResponse,
        cairne.schema.generated.EntityGenerationField,
        cairne.schema.generated.EntityGenerationSchema,
        cairne.schema.generated.GeneratedEntity,
        cairne.schema.generated.GeneratedEntityListItem,
        cairne.schema.generated.GeneratedField,
        cairne.schema.generated.GenerationHistory,
        cairne.schema.generated.GenerationState,
        cairne.schema.generated.GetEntityRequest,
        cairne.schema.generated.GetEntityResponse,
        cairne.schema.generated.GetEntitySchemaResponse,
        cairne.schema.generated.ListEntitiesRequest,
        cairne.schema.generated.ListEntitiesResponse,
        cairne.schema.loaded_models.ListLoadedModelsRequest,
        cairne.schema.loaded_models.ListLoadedModelsResponse,
        cairne.schema.loaded_models.LoadModelRequest,
        cairne.schema.loaded_models.LoadModelResponse,
        cairne.schema.loaded_models.LoadedModel,
        cairne.schema.loaded_models.UnloadModelRequest,
        cairne.schema.loaded_models.UnloadModelResponse,
        cairne.schema.worlds.CreateWorldRequest,
        cairne.schema.worlds.EntityType,
        cairne.schema.worlds.EntityTypeSummary,
        cairne.schema.worlds.ListEntityTypesResponse,
        cairne.schema.worlds.WorldSummary
        
        # cairne.schema.generated.GeneratedValueEditor,
	]
	_, top_level_schema = models_json_schema(
		[(model, "validation") for model in models], title="Cairne Schema"
	)
	with open("ashkavor/src/openrpg/schema/schema.json", "w") as fp:
		json.dump(top_level_schema, fp, indent=2)


def print_classes():
	models = []
	imports = set()
	for root, _, files in os.walk("cairne/cairne/schema"):
		for file in files:
			if not file.endswith(".py"):
				continue
			if file == "base.py":
				continue
			with open(os.path.join(root, file)) as fp:
				for line in fp:
					if "#" in line:
						continue
					if "class " not in line:
						continue
					class_name = line.split("class ")[1].split("(")[0]
					class_path = (
						root[len("cairne/") :].replace("/", ".")
						+ "."
						+ file[:-3]
						+ "."
						+ class_name
					)
					models.append("        " + class_path + ",")  # "\t\t\t" +

					imports.add("    import " + class_path.rsplit(".", 1)[0])
	print("\n".join(sorted(models)))
	print("\n\n\n\n\n")
	print("\n".join(sorted(list(imports))))


if __name__ == "__main__":
	print_classes()
	generate_json_schema()
