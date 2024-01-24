import { useLocation, useNavigate } from 'react-router-dom';
import * as openrpg from '../../openrpg/schema/schema';
import React from 'react';
import { getWorlds, updateTemplate } from '../../openrpg/client';
import * as generation from '../../openrpg/generation';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store';
import { fetchEntity, fetchTemplate } from '../../openrpg/reducers/templates';

export interface StructuredGenerationFieldProps {
    generatedField: openrpg.GeneratedField;
}

export const StructuredGenerationField = ({ generatedField }: StructuredGenerationFieldProps) => {
    const location = useLocation();
    const worldId = location.pathname.split('/')[2];
    const entityType = location.pathname.split('/')[4];
    const entityId = location.pathname.split('/')[5];

    const navigate = useNavigate();

    const templatesState = useSelector((state: RootState) => state.templates);
    const templateId = templatesState?.entities[entityId]?.editingTemplateId;

    const dispatch = useDispatch();

    const isGenerated = generatedField?.generate || false;
    const toggleGenerate = () => {
        if (!templateId) {
            return;
        }

        const updates: openrpg.UpdateTemplateRequest = {
            template_id: templateId,
            new_name: null,
            generator_model: null,
            include_fields: isGenerated ? null : [generatedField.edit_path],
            exclude_fields: isGenerated ? [generatedField.edit_path] : null,
            number_to_generate: null,
            instructions_to_include: [],
            instructions_to_exclude: null,
            prompt: null,
            parameter_updates: null,
        };
        updateTemplate(updates, (response: openrpg.UpdateTemplateResponse) => {
            dispatch(fetchTemplate(templateId));
            dispatch(fetchEntity(worldId, entityId));
        });
    };

    // Need to also get the generation result....

    return (
        <div
            style={{
                display: 'grid',
                gridTemplateColumns: '25% 75%',
            }}
        >
            <div>
                <label>Generate</label>
                <input
                    type="checkbox"
                    checked={isGenerated}
                    onChange={toggleGenerate}
                    disabled={!templateId}
                />
            </div>
            <div>
                <label>{generatedField.generated_value_label}</label>
                <br />
                <button>Apply</button>
            </div>
        </div>
    );
};
