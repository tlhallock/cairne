import classNames from 'classnames';
import styles from './entity-editor.module.scss';
import { useLocation, useNavigate } from 'react-router-dom';
import * as openrpg from '../../openrpg/schema/schema';
import React from 'react';
import { getTemplate, createTemplate, deleteTemplate, listGenerations } from '../../openrpg/client';
import { StructuredGenerationSettings } from '../structured-generation-settings/structured-generation-settings';

import * as generation from '../../openrpg/generation';
import { StructuredGenerationField } from '../structured-generation-field/structured-generation-field';
import { GenerateStatus } from '../generate-status/generate-status';

import { HEADER_STYLES } from '../editor/base';
import { FieldsEditor, FieldsProps } from '../editor/editor';
import { GenerationTemplate } from '../generation-template/generation-template';
import { RootState } from '../../store';
import { useDispatch, useSelector } from 'react-redux';
import {
    listEntityTemplates,
    listEntityTypeTemplates,
    listEntityGenerations,
    editTemplate,
    viewGeneration,
    fetchEntity,
} from '../../openrpg/reducers/templates';

export interface GenerationTemplatesProps {}

export const GenerationTemplates = ({}: GenerationTemplatesProps) => {
    const templatesState = useSelector((state: RootState) => state.templates);
    const dispatch = useDispatch();
    const location = useLocation();
    const navigate = useNavigate();

    const [newTemplateName, setNewTemplateName] = React.useState<string>('');
    const [filterTemplates, setFilterTemplates] = React.useState<boolean>(false);

    const worldId = location.pathname.split('/')[2];
    const entityType = location.pathname.split('/')[4];
    const entityId = location.pathname.split('/')[5];

    const templatesList = filterTemplates
        ? templatesState?.entities[entityId]?.availableTemplates || []
        : templatesState?.entityTypeTemplates[entityType] || [];
    const currentTemplateId = templatesState?.entities[entityId]?.editingTemplateId;

    React.useEffect(() => {
        if (!currentTemplateId) {
            return;
        }
        for (const template of templatesList) {
            if (template.template_id === currentTemplateId) {
                return;
            }
        }
        dispatch(editTemplate(entityId, null));
    }, [filterTemplates, worldId, entityId]);

    const refreshTemplatesList = () => {
        if (!worldId || !entityId) {
            return;
        }
        dispatch(listEntityTemplates(worldId, entityId));
        dispatch(listEntityTypeTemplates(worldId, entityType));
    };

    React.useEffect(() => {
        if (!worldId || !entityId) {
            return;
        }

        refreshTemplatesList();
    }, []);

    const create = () => {
        if (!newTemplateName) {
            return;
        }
        createTemplate(
            newTemplateName,
            worldId,
            entityId,
            null,
            'text',
            (response: openrpg.CreateTemplateResponse) => {
                if (!response.template_id) {
                    return;
                }
                setNewTemplateName('');
                refreshTemplatesList();
                dispatch(editTemplate(entityId, response.template_id));
            }
        );
    };

    return (
        <div style={{ backgroundColor: 'red' }}>
            <input
                type="text"
                value={newTemplateName}
                onChange={(e) => {
                    setNewTemplateName(e.target.value);
                }}
            />
            <button onClick={create} disabled={!newTemplateName}>
                Create
            </button>
            <br />
            <label>Template:</label>
            <select
                onChange={(e) => dispatch(editTemplate(entityId, e.target.value))}
                value={currentTemplateId || ''}
            >
                <option value="">Select a template</option>
                {templatesList.map((template) => {
                    return (
                        <option key={template.template_id} value={template.template_id}>
                            {template.name}
                        </option>
                    );
                })}
            </select>
            <label>Filter templates to current entity:</label>
            <input
                type="checkbox"
                checked={filterTemplates}
                onChange={(e) => setFilterTemplates(e.target.checked)}
            />
            <br />
            <label>Generation:</label>
            <select
                onChange={(e) => {
                    dispatch(viewGeneration(entityId, e.target.value));
                    dispatch(fetchEntity(worldId, entityId));
                }}
                value={templatesState?.entities[entityId]?.currentGenerationId || ''}
            >
                <option value="">Select a Generation</option>
                {(templatesState?.entities[entityId]?.availableGenerations || []).map(
                    (generation) => {
                        return (
                            <option key={generation.generation_id} value={generation.generation_id}>
                                {generation.label}
                            </option>
                        );
                    }
                )}
            </select>
            <br />
            <GenerationTemplate />
        </div>
    );
};
