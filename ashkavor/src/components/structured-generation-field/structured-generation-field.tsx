import { useLocation, useNavigate } from 'react-router-dom';
import * as openrpg from '../../openrpg/schema/schema';
import React from 'react';
import { getGenerationSchema } from '../../openrpg/client';
import * as generation from '../../openrpg/generation';

const findGenerationField = (
    generationSchema: openrpg.EntityGenerationSchema | undefined,
    generatedField: openrpg.GeneratedField
) => {
    if (!generationSchema) {
        return undefined;
    }
    return generationSchema.fields.find((f) => f.name === generatedField.label);
};

export interface StructuredGenerationFieldProps {
    generatedField: openrpg.GeneratedField;
    generationState: generation.GenerationState;
    setGenerationState: (state: generation.GenerationState) => void;
}

export const StructuredGenerationField = ({
    generatedField,
    generationState,
    setGenerationState,
}: StructuredGenerationFieldProps) => {
    const location = useLocation();
    const navigate = useNavigate();

    const worldId = location.pathname.split('/')[2];
    const entityType = location.pathname.split('/')[4];
    const entityId = location.pathname.split('/')[5];

    const [generationSchema, setGenerationSchema] =
        React.useState<openrpg.EntityGenerationSchema>();
    React.useEffect(() => {
        if (!entityType) {
            return;
        }
        getGenerationSchema(worldId, entityType, (response: openrpg.GetEntitySchemaResponse) => {
            setGenerationSchema(response.schema);
        });
    }, [entityType]);

    const field = findGenerationField(generationSchema, generatedField);
    const isGenerated = generation.isFieldGenerated(generationState, field?.name);
    const toggleGenerate = () => {
        setGenerationState(generation.toggleField(generationState, field?.name));
    };

    // Need to also get the generation result....

    return (
        <div>
            <label>Generate</label>
            <input
                type="checkbox"
                checked={isGenerated}
                onChange={toggleGenerate}
                disabled={!field}
            />
        </div>
    );
};
