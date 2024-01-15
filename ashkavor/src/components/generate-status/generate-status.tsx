//

import { Link, useLocation, useNavigate } from 'react-router-dom';
import * as openrpg from '../../openrpg/schema/schema';
import React from 'react';
import { getGeneration } from '../../openrpg/client';

export interface GenerateStatusProps {
    generationId?: string;
}

const getGenerationStatusLabel = (generationStatus: openrpg.GenerationStatus | undefined) => {
    if (!generationStatus) {
        return 'Loading...';
    }

    // 'queued' | 'in_progress' | 'streaming' | 'error' | 'complete';
    switch (generationStatus) {
        case 'queued':
            return 'Queued';
        case 'in_progress':
            return 'In Progress';
        case 'streaming':
            return 'Streaming';
        case 'error':
            return 'Error';
        case 'complete':
            return 'Complete';
        default:
            return 'Unknown';
    }
};

export const GenerateStatus = ({ generationId }: GenerateStatusProps) => {
    const [refreshCounter, setRefreshCounter] = React.useState<number>(0);
    const [generation, setGeneration] = React.useState<openrpg.Generation>();

    setTimeout(() => {
        setRefreshCounter(refreshCounter + 1);
    }, 1000);

    React.useEffect(() => {
        if (!generationId) {
            return;
        }
        getGeneration(generationId, (response: openrpg.GetGenerationResponse) => {
            if (!response.generation) {
                return;
            }
            setGeneration(response.generation);
        });
    }, [refreshCounter]);

    console.log('Got generation', generation);

    return (
        <>
            <progress id="file" value="50" max="100">
                {' '}
                50%{' '}
            </progress>
            <label>{generation?.status}</label>
            <Link to={`/generation/${generationId}`}>View Generation</Link>
        </>
    );
};
