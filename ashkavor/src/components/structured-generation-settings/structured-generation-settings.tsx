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

    const worldId = location.pathname.split('/')[2];
    const entityType = location.pathname.split('/')[4];
    const entityId = location.pathname.split('/')[5];

    React.useEffect(() => {
        if (!worldId || !entityId) {
            return;
        }
        // Get generator types
    }, []);

    return <div></div>;
};
