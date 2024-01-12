import classNames from 'classnames';
import styles from './world-entities-list.module.scss';
import { Link, Outlet, useOutletContext } from 'react-router-dom';
import * as openrpg from '../../openrpg/schema/schema';
import { useLocation } from 'react-router-dom';
import React from 'react';
import { createEntity, listEntities } from '../../openrpg/client';
import { useNavigate } from 'react-router-dom';

export interface WorldEntitiesListProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const WorldEntitiesList = ({ className }: WorldEntitiesListProps) => {
    const location = useLocation();
    const navigate = useNavigate();
    const world = useOutletContext<openrpg.GeneratedEntity>();

    const [newEntityName, setNewEntityName] = React.useState<string>('');
    const [editOnCreate, setEditOnCreate] = React.useState<boolean>(true);
    const [entities, setEntities] = React.useState<openrpg.GeneratedEntityListItem[]>([]);
    const [refreshCounter, setRefreshCounter] = React.useState<number>(0);

    const worldId = location.pathname.split('/')[2];
    const entityType = location.pathname.split('/')[4];
    const entityLabel = entityType; // TODO

    const createLink = (entityId: string) =>
        '/world/' + worldId + '/entities/' + entityType + '/' + entityId;

    React.useEffect(() => {
        if (!worldId || !entityType) {
            return;
        }
        listEntities(worldId, entityType, (response: openrpg.ListEntitiesResponse) => {
            if (!response.entities) {
                return;
            }
            setEntities(response.entities);
        });
    }, [refreshCounter]);

    const onNewEntity = (response: openrpg.CreateEntityResponse) => {
        setNewEntityName('');
        if (!editOnCreate) {
            setRefreshCounter(refreshCounter + 1);
            return;
        }
        navigate(createLink(response.entity_id));
    };

    return (
        <div className={classNames(styles.root, className)}>
            <ul>
                {entities?.map((entity) => (
                    <li key={entity.entity_id}>
                        <Link to={createLink(entity.entity_id)}>
                            {entity.name || entity.entity_id}
                        </Link>
                    </li>
                ))}
            </ul>
            <Outlet context={world} />
            <label>New {entityLabel} name:</label>
            <input
                type="text"
                value={newEntityName}
                onChange={(event) => setNewEntityName(event.target.value)}
            />
            <button
                onClick={() => createEntity(worldId, entityType, newEntityName, onNewEntity)}
                disabled={newEntityName.length === 0}
            >
                Create!
            </button>
            <input
                type="checkbox"
                checked={editOnCreate}
                onChange={(event) => setEditOnCreate(event.target.checked)}
            />
            <label>Edit</label>
        </div>
    );
};
