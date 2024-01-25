import axios from 'axios';
import * as openrpg from './schema/schema';

axios.defaults.baseURL = 'http://127.0.0.1:5000';
// axios.defaults.po = 5000;
axios.defaults.headers.post['Content-Type'] = 'application/octet-stream';
// axios.defaults.headers.post['Accept'] = 'application/octet-stream';

export const getWorlds = (
    onWorlds: (response: openrpg.ListEntitiesResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    axios
        .get('/worlds')
        .then((r) => onWorlds(r.data))
        .catch(onError);
};

export const getWorld = (
    worldId: openrpg.WorldId,
    onWorld: (response: openrpg.GetEntityResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    axios
        .get('/world/' + worldId)
        .then((r) => onWorld(r.data))
        .catch(onError);
};

export const createWorld = (
    worldName: string,
    onWorld: (response: openrpg.CreateEntityResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    console.log('createWorld', worldName);
    const request: openrpg.CreateWorldRequest = {
        name: worldName,
    };
    axios
        .post('/world', request, { headers: { 'Content-Type': 'application/json' } })
        .then((r) => onWorld(r.data))
        .catch(onError);
};

export const deleteWorld = (
    worldId: openrpg.WorldId,
    onDelete: (response: openrpg.DeleteEntityResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    axios
        .delete('/world/' + worldId)
        .then((r) => onDelete(r.data))
        .catch(onError);
};

export const listEntityTypes = (
    onEntityTypes: (response: openrpg.ListEntityTypesResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    axios
        .get('/entity_types')
        .then((r) => onEntityTypes(r.data))
        .catch(onError);
};

export const listEntities = (
    worldId: openrpg.WorldId,
    entityType: string, // openrpg.EntityType,
    onEntityTypes: (response: openrpg.ListEntitiesResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    axios
        .get('/world/' + worldId + '/entities/' + entityType)
        .then((r) => onEntityTypes(r.data))
        .catch(onError);
};

export const getEntity = (
    worldId: openrpg.WorldId,
    entityId: openrpg.EntityId,
    templateId: openrpg.TemplateId | null,
    generationId: openrpg.GenerationId | null,
    onEntity: (response: openrpg.GetEntityResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    const query: openrpg.GetEntityQuery = {
        template_id: templateId,
        generation_id: generationId,
    };
    axios
        .get('/world/' + worldId + '/entity/' + entityId, { params: query })
        .then((r) => onEntity(r.data))
        .catch(onError);
};

export const createEntity = (
    worldId: openrpg.WorldId,
    entityType: openrpg.EntityType,
    entityName: string,
    onEntity: (response: openrpg.CreateEntityResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    const request: openrpg.CreateEntityRequest = {
        world_id: worldId,
        entity_type: entityType,
        name: entityName,
    };
    axios
        .post('/world/' + worldId + '/entities/' + entityType, request, {
            headers: { 'Content-Type': 'application/json' },
        })
        .then((r) => onEntity(r.data))
        .catch(onError);
};

export const deleteEntity = (
    worldId: openrpg.WorldId,
    entityId: openrpg.EntityId,
    onDelete: (response: openrpg.DeleteEntityResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    axios
        .delete('/world/' + worldId + '/entity/' + entityId)
        .then((r) => onDelete(r.data))
        .catch(onError);
};

// export const getGenerationSchema = (
//     worldId: openrpg.WorldId,
//     entityType: openrpg.EntityType,
//     onSchema: (response: openrpg.GetEntitySchemaResponse) => void,
//     onError: (error: Error) => void = (error: Error) => console.log(error)
// ) => {
//     axios
//         .get('/schema/entity/' + entityType)
//         .then((r) => onSchema(r.data))
//         .catch(onError);
// };

export const structuredGenerate = (
    generateRequest: openrpg.GenerateRequest,
    onGenerated: (response: openrpg.GenerateResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    axios
        .post('/generate', generateRequest, { headers: { 'Content-Type': 'application/json' } })
        .then((r) => onGenerated(r.data))
        .catch(onError);
};

export const getGeneration = (
    generationId: openrpg.GenerationId,
    onStatus: (response: openrpg.GetGenerationResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    axios
        .get('/generation/' + generationId)
        .then((r) => onStatus(r.data))
        .catch(onError);
};

export const replaceValue = (
    worldId: openrpg.WorldId,
    path: openrpg.GeneratablePath,
    value_js: string,
    onComplete: (response: openrpg.ReplaceResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    const request: openrpg.ReplaceRequest = {
        world_id: worldId,
        path: path,
        value_js: value_js,
    };
    console.log('Sending request', request);
    axios
        .post('/world/' + worldId + '/update', request, {
            headers: { 'Content-Type': 'application/json' },
        })
        .then((r) => onComplete(r.data))
        .catch(onError);
};

export const createTemplate = (
    name: string,
    worldId: openrpg.WorldId,
    entityId: openrpg.EntityId2,
    generatorModel: openrpg.GeneratorModel | null,
    generationType: openrpg.GenerationType | null,
    onTemplate: (response: openrpg.CreateTemplateResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    const request: openrpg.CreateTemplateRequest = {
        name: name,
        world_id: worldId,
        entity_id: entityId,
        generator_model: generatorModel,
        generation_type: generationType,
    };
    axios
        .post('/templates', request, { headers: { 'Content-Type': 'application/json' } })
        .then((r) => onTemplate(r.data))
        .catch(onError);
};

export const deleteTemplate = (
    templateId: openrpg.TemplateId,
    onDelete: (response: openrpg.DeleteTemplateResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    axios
        .delete('/template/' + templateId)
        .then((r) => onDelete(r.data))
        .catch(onError);
};

export const listTemplates = (
    query: openrpg.ListTemplatesQuery,
    onTemplates: (response: openrpg.ListTemplatesResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    axios
        .get('/templates', { params: query })
        .then((r) => onTemplates(r.data))
        .catch(onError);
};

export const listGenerations = (
    entityId: openrpg.EntityId | null,
    onGenerations: (response: openrpg.ListGenerationsResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    axios
        .get('/generations')
        .then((r) => onGenerations(r.data))
        .catch(onError);
};

export const getTemplate = (
    templateId: openrpg.TemplateId,
    onTemplate: (response: openrpg.GetTemplateResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    axios
        .get('/template/' + templateId)
        .then((r) => onTemplate(r.data))
        .catch(onError);
};

export const updateTemplate = (
    updates: openrpg.UpdateTemplateRequest,
    onUpdate: (response: openrpg.UpdateTemplateResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    axios
        .post('/template/' + updates.template_id, updates, {
            headers: { 'Content-Type': 'application/json' },
        })
        .then((r) => onUpdate(r.data))
        .catch(onError);
};

export const listGeneratorTypes = (
    onGeneratorTypes: (response: openrpg.ListGenerationModels) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    axios
        .get('/templates/generators')
        .then((r) => onGeneratorTypes(r.data))
        .catch(onError);
};
