from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union




class LoadedModel(BaseModel):
    model_name: str
    # Needs to support:
    #    memory used?
    #    language model vs image generator vs sound generator
    #    Huggingface models
    #       model name
    #       
    #       json schema for the transformer used?
    #    open ai model?



class LoadModelRequest(BaseModel):
    model_name: str

class LoadModelResponse(BaseModel):
    loaded_model_id: str

class UnloadModelRequest(BaseModel):
    loaded_model_id: str

class UnloadModelResponse(BaseModel):
    pass

class ListLoadedModelsRequest(BaseModel):
    pass

class ListLoadedModelsResponse(BaseModel):
    loaded_models: List[LoadedModel]

