//

import { Link, useLocation, useNavigate } from 'react-router-dom';
import * as openrpg from '../../openrpg/schema/schema';
import React from 'react';
import { getGeneration } from '../../openrpg/client';

import { getGenerationStatusLabel } from '../generation/generation';

export interface GenerateStatusProps {
    generationId?: string;
}

export const GenerateStatus = ({ generationId }: GenerateStatusProps) => {
    const [refreshCounter, setRefreshCounter] = React.useState<number>(0);
    const [generation, setGeneration] = React.useState<openrpg.GenerationView>();

    React.useEffect(() => {
        if (!generationId) {
            return;
        }
        if (generation?.status !== 'in_progress') {
            return;
        }
        const timeoutID = setTimeout(() => {
            setRefreshCounter(refreshCounter + 1);
        }, 1000);

        return () => {
            clearTimeout(timeoutID);
        };
    }, [refreshCounter]);

    React.useEffect(() => {
        if (!generationId) {
            return;
        }
        console.log('Refreshing generation');
        getGeneration(generationId, (response: openrpg.GetGenerationResponse) => {
            if (!response.generation) {
                return;
            }
            setGeneration(response.generation);
        });
    }, [refreshCounter]);

    return (
        <>
            {generation?.status === 'in_progress' && (
                <progress id="file" value="50" max="100">
                    {' '}
                    50%{' '}
                </progress>
            )}
            <label>Status:</label>
            <label>{getGenerationStatusLabel(generation?.status)}</label>
            <br />
            <Link to={`/generation/${generationId}`}>View Generation</Link>
        </>
    );
};
