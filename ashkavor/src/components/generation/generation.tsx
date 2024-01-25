//

import { Link, useLocation, useNavigate } from 'react-router-dom';
import * as openrpg from '../../openrpg/schema/schema';
import React from 'react';
import { getGeneration } from '../../openrpg/client';
import { NavigationBar } from '../navigation-bar/navigation-bar';

export interface GenerateStatusProps {}

export const getGenerationStatusLabel = (
    generationStatus: openrpg.GenerationStatus | undefined
) => {
    if (!generationStatus) {
        return 'Loading...';
    }
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

export const Generation = ({}: GenerateStatusProps) => {
    const location = useLocation();
    const [generation, setGeneration] = React.useState<openrpg.GenerationView>();
    const generationId = location.pathname.split('/')[2];

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
    }, [generationId]);

    const worldId = generation?.template.world_id;
    const entityId = generation?.template.entity_id;
    const entityType = generation?.template.entity_type;
    const link = `/world/${worldId}/entities/${entityType}/${entityId}`;

    http: return (
        <>
            <NavigationBar />
            {generation?.status === 'in_progress' && (
                <progress id="file" value="50" max="100">
                    {' '}
                    50%{' '}
                </progress>
            )}
            <label>Name:</label>
            <label>{generation?.template.name}</label>
            <br />
            <label>Created:</label>
            <label>{generation?.template.created_at}</label>
            <br />
            <label>Status:</label>
            <label>{getGenerationStatusLabel(generation?.status)}</label>
            <br />
            <label>Entity type:</label>
            <label>{entityType}</label>
            <br />
            <Link to={link}>View Entity</Link>
            <br />
            <label>Raw text:</label>
            <br />
            <textarea
                style={{
                    width: '100%',
                    whiteSpace: 'pre-wrap',
                    // overflowWrap: 'break-word',
                }}
                value={generation?.raw_generated_text || ''}
                disabled={true}
                rows={20}
                cols={100}
            />
        </>
    );
};
