import classNames from 'classnames';
import styles from './entity-editor.module.scss';
import { useLocation, useNavigate } from 'react-router-dom';
import * as openrpg from '../../openrpg/schema/schema';
import React from 'react';
import { getEntity, deleteEntity } from '../../openrpg/client';

export interface FreeFormChatProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const FreeFormChat = ({ className }: FreeFormChatProps) => {
    const location = useLocation();
    const navigate = useNavigate();
    const [entity, setEntity] = React.useState<openrpg.GeneratedEntity>();
    const [refreshCounter, setRefreshCounter] = React.useState<number>(0);

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
        });
    }, [refreshCounter]);

    const onEdit = () => {
        setRefreshCounter(refreshCounter + 1);
    };

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
            <ul>
                <li>
                    <div style={HEADER_STYLES}>
                        <label>Field</label>
                        <label>Current value</label>
                        <label>Updates</label>
                    </div>
                </li>
                {entity?.fields?.map((field) => (
                    <li key={field.label}>
                        <Field field={field} onEdit={onEdit} />
                    </li>
                ))}
            </ul>
            {entity?.name || entity?.entity_id}
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
