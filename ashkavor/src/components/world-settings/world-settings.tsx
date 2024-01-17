import * as React from 'react';

import * as generation from '../../openrpg/generation';
import classNames from 'classnames';
import styles from './world-settings.module.scss';
import { getWorld, deleteWorld, listEntityTypes } from '../../openrpg/client';
import { useNavigate, useLocation } from 'react-router-dom';
import * as openrpg from '../../openrpg/schema/schema';
import { Link, Outlet, useOutletContext } from 'react-router-dom';
import { SPLITTER_STYLES, HEADER_STYLES } from '../editor/base';

import { FieldsEditor, FieldsProps } from '../editor/editor';

export interface WorldSettingsProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const WorldSettings = ({ className }: WorldSettingsProps) => {
    const location = useLocation();
    const navigate = useNavigate();
    const world = useOutletContext<openrpg.GeneratedEntity>();
    const worldId = location.pathname.split('/')[2];
    const [generationState, setGenerationState] = React.useState<generation.GenerationState>(
        generation.DEFAULT_GENERATION_STATE
    );
    const [entity, setEntity] = React.useState<openrpg.GeneratedEntity>();

    React.useEffect(() => {
        if (!worldId) {
            return;
        }
        getWorld(worldId, (response: openrpg.GetEntityResponse) => {
            if (!response.entity) {
                return;
            }
            setEntity(response.entity);

            console.log('Found world', response.entity);
        });
    }, [worldId]);

    const onDelete = (response: openrpg.DeleteEntityResponse) => {
        navigate('/worlds');
    };

    const onEdit = () => {
        console.log('edited');
    };

    return (
        <div className={classNames(styles.root, className)}>
            WorldSettings
            <button onClick={() => deleteWorld(worldId, onDelete)}>Delete</button>
            <ul>
                <li>Created At: {world.created_at}</li>
                <li>Updated At: {world.updated_at}</li>
            </ul>
            <FieldsEditor
                fields={entity?.fields || []}
                onEdit={onEdit}
                generatorState={generationState}
                setGeneratorState={setGenerationState}
            />
        </div>
    );
};
