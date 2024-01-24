/** @format */

import { createSlice } from '@reduxjs/toolkit';
import { useSelector, useDispatch } from 'react-redux';
import * as openrpg from '../schema/schema';
import { getTemplate, listTemplates, getGeneration, listGenerations, getEntity } from '../client';

interface EntityTemplateCache {
    [templateId: string]: openrpg.GenerationTemplateView;
}

interface EntityGenerationCache {
    [generationId: string]: openrpg.GenerationView;
}

interface EntityTemplates {
    entity: openrpg.GeneratedEntity | null;

    editingTemplateId: openrpg.TemplateId3 | null;
    availableTemplates: openrpg.TemplateListItem[];

    currentGenerationId: openrpg.GenerationId | null;
    availableGenerations: openrpg.GenerationListItem[];
}

const createEmptyEntityTemplates = (): EntityTemplates => ({
    entity: null,

    editingTemplateId: null,
    availableTemplates: [],

    currentGenerationId: null,
    availableGenerations: [],
});

/**
 * TODO: the templates don't have to be under the entity.
 * This doesn't account for the world either.
 */
export interface TemplatesState {
    worldId: openrpg.WorldId | null;
    entities: {
        [entityId: string]: EntityTemplates;
    };
    generationsCache: EntityGenerationCache;
    templatesCache: EntityTemplateCache;
    currentEntity: openrpg.EntityId | null;
}

const createInitialState = (): TemplatesState => ({
    worldId: null,
    entities: {},
    templatesCache: {},
    generationsCache: {},
    currentEntity: null,
});

const templatesSlice = createSlice({
    name: 'templates',
    initialState: createInitialState(),
    reducers: {
        setTemplate: (state, { payload }) => {
            state.templatesCache[payload.templateId] = payload.template;
        },
        setTemplates: (state, { payload }) => {
            if (!(payload.entityId in state.entities)) {
                state.entities[payload.entityId] = createEmptyEntityTemplates();
            }
            state.entities[payload.entityId].availableTemplates = payload.templates;
        },
        editTemplate: (state, { payload }) => {
            if (!(payload.entityId in state.entities)) {
                state.entities[payload.entityId] = createEmptyEntityTemplates();
            }
            state.entities[payload.entityId].editingTemplateId = payload.templateId;
        },
        setGeneration: (state, { payload }) => {
            state.generationsCache[payload.generationId] = payload.generation;
        },
        viewGeneration: (state, { payload }) => {
            if (!(payload.entityId in state.entities)) {
                state.entities[payload.entityId] = createEmptyEntityTemplates();
            }
            state.entities[payload.entityId].currentGenerationId = payload.generationId;
        },
        setGenerations: (state, { payload }) => {
            if (!(payload.entityId in state.entities)) {
                state.entities[payload.entityId] = createEmptyEntityTemplates();
            }
            state.entities[payload.entityId].availableGenerations = payload.generations;
        },
        setEditingEntity: (state, { payload }) => {
            state.currentEntity = payload.entityId;
        },
        setEntity: (state, { payload }) => {
            const entityId = payload.entity.entity_id;
            if (!(entityId in state.entities)) {
                state.entities[payload.entityId] = createEmptyEntityTemplates();
            }
            state.entities[entityId].entity = payload.entity;
        },
    },
});

export const templatesReducer = templatesSlice.reducer;

export const fetchTemplate = (templateId: openrpg.TemplateId3 | null) => (dispatch) => {
    if (!templateId) {
        return;
    }

    getTemplate(templateId, (response: openrpg.GetTemplateResponse) => {
        if (!response.template) {
            return;
        }
        dispatch(
            templatesSlice.actions.setTemplate({
                templateId,
                template: response.template,
            })
        );
    });
};

export const editTemplate =
    (entityId: openrpg.EntityId, templateId: openrpg.TemplateId3 | null) => (dispatch) => {
        dispatch(
            templatesSlice.actions.editTemplate({
                entityId,
                templateId,
            })
        );

        dispatch(fetchTemplate(templateId));
    };

export const fetchGeneration = (generationId: openrpg.GenerationId) => (dispatch) => {
    if (!generationId) {
        return;
    }

    getGeneration(generationId, (response: openrpg.GetGenerationResponse) => {
        if (!response.generation) {
            return;
        }
        dispatch(
            templatesSlice.actions.setGeneration({
                generationId,
                generation: response.generation,
            })
        );
    });
};

export const viewGeneration =
    (entityId: openrpg.EntityId, generationId: openrpg.GenerationId) => (dispatch) => {
        dispatch(
            templatesSlice.actions.viewGeneration({
                entityId,
                generationId,
            })
        );

        dispatch(fetchGeneration(generationId));
    };

export const listEntityTemplates = (entityId: openrpg.EntityId) => (dispatch) => {
    if (!entityId) {
        return;
    }

    listTemplates(entityId, (response: openrpg.ListTemplatesResponse) => {
        if (!response.templates) {
            return;
        }
        dispatch(
            templatesSlice.actions.setTemplates({
                entityId,
                templates: response.templates,
            })
        );
    });
};

export const listEntityGenerations = (entityId: openrpg.EntityId) => (dispatch) => {
    if (!entityId) {
        return;
    }

    listGenerations(entityId, (response: openrpg.ListGenerationsResponse) => {
        if (!response.generations) {
            return;
        }
        dispatch(
            templatesSlice.actions.setGenerations({
                entityId,
                generations: response.generations,
            })
        );
    });
};

export const editEntity = (entityId: openrpg.EntityId) => (dispatch) => {
    dispatch(
        templatesSlice.actions.setEditingEntity({
            entityId,
        })
    );

    dispatch(listEntityTemplates(entityId));
    dispatch(listEntityGenerations(entityId));
};

export const fetchEntity =
    (worldId: openrpg.WorldId, entityId: openrpg.EntityId) => (dispatch, getState) => {
        dispatch(
            templatesSlice.actions.setEditingEntity({
                entityId,
            })
        );
        const state = getState();
        const templateId = entityId ? state.templates.entities[entityId]?.editingTemplateId : null;
        const generationId = entityId
            ? state.templates.entities[entityId]?.currentGenerationId
            : null;
        getEntity(
            worldId,
            entityId,
            templateId,
            generationId,
            (response: openrpg.GetEntityResponse) => {
                if (!response.entity) {
                    return;
                }
                console.log('Found entity', response.entity);
                dispatch(
                    templatesSlice.actions.setEntity({
                        entity: response.entity,
                    })
                );
            }
        );
    };
