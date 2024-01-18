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

export interface EntityEditorProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const EntityEditor = ({ className }: EntityEditorProps) => {
    const location = useLocation();
    const navigate = useNavigate();
    const [entity, setEntity] = React.useState<openrpg.GeneratedEntity>();
    const [refreshCounter, setRefreshCounter] = React.useState<number>(0);
    const [generationState, setGenerationState] = React.useState<generation.GenerationState>(
        generation.DEFAULT_GENERATION_STATE
    );
    const [generationId, setGenerationId] = React.useState<string>();

    const worldId = location.pathname.split('/')[2];
    const entityType = location.pathname.split('/')[4];
    const entityId = location.pathname.split('/')[5];

    React.useEffect(() => {
        if (!worldId || !entityId) {
            return;
        }
        getEntity(worldId, entityId, (response: openrpg.GetEntityResponse) => {
            if (!response.entity) {
                return;
            }
            setEntity(response.entity);
            console.log('Generated entity', response.entity);
        });
    }, [refreshCounter]);

    const onEdit = () => {
        setRefreshCounter(refreshCounter + 1);
    };

    const onDelete = (response: openrpg.DeleteEntityResponse) => {
        navigate('/world/' + worldId + '/entities/' + entityType);
    };

    const generate = () => {
        const generateRequest: openrpg.GenerateRequest = {
            world_id: worldId,
            entity_id: entityId,
            /*
            world_id: uuid.UUID = Field()
	        entity_id: uuid.UUID = Field(default=None)
	        fields_to_generate: Optional[generation_model.TargetFields] = Field(default=None)

	        generator_model: Optional[generation_model.GeneratorModel] = Field(default=None)
	        parameters: Optional[generation_model.GenerationRequestParameters] = Field(default=None)
            
	        prompt_messages: Optional[List[generation_model.GenerationChatMessage]] = Field(default=None)
	        instructions: Optional[List[generation_model.Instruction]] = Field(default=None)
	        json_structure: Optional[JsonStructureRequest] = Field(default=None)
            */
        };

        structuredGenerate(generateRequest, (response: openrpg.GenerateResponse) => {
            setGenerationId(response.generation_id);
        });
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
            {generationId && <GenerateStatus generationId={generationId} />}
            <div>
                <StructuredGenerationSettings
                    generationState={generationState}
                    setGenerationState={setGenerationState}
                />
                <div>
                    {/* TODO: add disabled field */}
                    <button onClick={generate}>Generate!</button>
                </div>
            </div>
            <FieldsEditor
                fields={entity?.fields || []}
                onEdit={onEdit}
                generationState={generationState}
                setGenerationState={setGenerationState}
            />
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
