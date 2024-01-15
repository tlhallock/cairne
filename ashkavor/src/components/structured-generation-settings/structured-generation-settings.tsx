import classNames from 'classnames';
import { useLocation, useNavigate } from 'react-router-dom';
import * as openrpg from '../../openrpg/schema/schema';
import React from 'react';
import { getGenerationSchema } from '../../openrpg/client';
import * as generation from '../../openrpg/generation';

export interface StructuredGenerationSettingsProps {
    className?: string;
    generationState: generation.GenerationState;
    setGenerationState: (state: generation.GenerationState) => void;
}

export const StructuredGenerationSettings = ({
    className,
    generationState,
    setGenerationState,
}: StructuredGenerationSettingsProps) => {
    const location = useLocation();
    const navigate = useNavigate();
    const [generatorModel, setGeneratorModel] = React.useState<string>('gpt-3.5-turbo-1106');
    const [generationSchema, setGenerationSchema] =
        React.useState<openrpg.EntityGenerationSchema>();

    const worldId = location.pathname.split('/')[2];
    const entityType = location.pathname.split('/')[4];
    const entityId = location.pathname.split('/')[5];

    React.useEffect(() => {
        if (!worldId || !entityId) {
            return;
        }
        // Get generator types
    }, []);

    React.useEffect(() => {
        if (!entityType) {
            return;
        }
        getGenerationSchema(worldId, entityType, (response: openrpg.GetEntitySchemaResponse) => {
            setGenerationSchema(response.schema);
        });
    }, [entityType]);

    console.log('schema', generationSchema);

    return (
        <div>
            <label>Generator Type</label>
            <select
                name="generator-type"
                id="generator-type"
                value={generationState.generatorTypeChoice.value}
                onChange={({ target: { value } }) => {
                    for (const generatorType of generation.DEFAULT_GENERATOR_TYPES) {
                        if (generatorType.value === value) {
                            setGenerationState(
                                generation.setGenerationType(generationState, value)
                            );
                        }
                    }
                }}
            >
                {generation.DEFAULT_GENERATOR_TYPES.map((generatorType) => (
                    <option key={generatorType.value} value={generatorType.value}>
                        {generatorType.label}
                    </option>
                ))}
            </select>
            <label>Model</label>
            <select
                name="generator-model"
                id="generator-model"
                value={generatorModel}
                onChange={(e) => {
                    setGeneratorModel(e.target.value);
                }}
            >
                {generationState.generatorTypeChoice.models.map((generatorModel) => (
                    <option key={generatorModel} value={generatorModel}>
                        {generatorModel}
                    </option>
                ))}
            </select>
            <br />

            <label>Instructions</label>
            <textarea />
        </div>
    );
};
