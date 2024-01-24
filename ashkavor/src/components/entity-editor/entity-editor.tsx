import classNames from 'classnames';
import styles from './entity-editor.module.scss';
import { useLocation, useNavigate } from 'react-router-dom';
import * as openrpg from '../../openrpg/schema/schema';
import React from 'react';
import { getEntity, deleteEntity, structuredGenerate } from '../../openrpg/client';
import { StructuredGenerationSettings } from '../structured-generation-settings/structured-generation-settings';

import * as generation from '../../openrpg/generation';
import { StructuredGenerationField } from '../structured-generation-field/structured-generation-field';
import { GenerateStatus } from '../generate-status/generate-status';

import { HEADER_STYLES } from '../editor/base';
import { FieldsEditor, FieldsProps } from '../editor/editor';
import { GenerationTemplate } from '../generation-template/generation-template';
import { GenerationTemplates } from '../generation-templates/generation-templates';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../store';
import {
    fetchEntity,
    listEntityTemplates,
    listEntityGenerations,
} from '../../openrpg/reducers/templates';

export interface EntityEditorProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const EntityEditor = ({ className }: EntityEditorProps) => {
    const templatesState = useSelector((state: RootState) => state.templates);
    const dispatch = useDispatch();

    const location = useLocation();
    const navigate = useNavigate();
    // const [entity, setEntity] = React.useState<openrpg.GeneratedEntity>();
    const [refreshCounter, setRefreshCounter] = React.useState<number>(0);

    const worldId = location.pathname.split('/')[2];
    const entityType = location.pathname.split('/')[4];
    const entityId = location.pathname.split('/')[5];

    const entity = templatesState?.entities[entityId]?.entity || null;

    const templateId = templatesState?.entities[entityId]?.editingTemplateId;
    const generationId = templatesState?.entities[entityId]?.currentGenerationId;

    React.useEffect(() => {
        if (!worldId || !entityId) {
            return;
        }
        dispatch(fetchEntity(worldId, entityId));
        dispatch(listEntityTemplates(entityId));
        dispatch(listEntityGenerations(entityId));
        // getEntity(
        //     worldId,
        //     entityId,
        //     templateId,
        //     generationId,
        //     (response: openrpg.GetEntityResponse) => {
        //         if (!response.entity) {
        //             return;
        //         }
        //         setEntity(response.entity);
        //         console.log('Generated entity', response.entity);
        //     }
        // );
    }, [refreshCounter, templateId, generationId]);

    const onDelete = (response: openrpg.DeleteEntityResponse) => {
        navigate('/world/' + worldId + '/entities/' + entityType);
    };

    return (
        <div className={classNames(styles.root, className)}>
            <button onClick={() => navigate('/world/' + worldId + '/entities/' + entityType)}>
                Back
            </button>
            <button onClick={() => deleteEntity(worldId, entityId, onDelete)}>Delete</button>
            <br />
            {entity?.name || entity?.entity_id}
            <br />

            <GenerationTemplates />
            <FieldsEditor fields={entity?.fields || []} />
        </div>
    );
};

// Want to set the language model
// The system prompt
// which instructions to include

// free form editor
//      edit previous messages
//
// structured editor
