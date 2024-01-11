import classNames from 'classnames';
import styles from './worlds.module.scss';
import { NavigationBar } from '../navigation-bar/navigation-bar';
import { getWorlds, createWorld } from '../../openrpg/client';
import * as openrpg from '../../openrpg/schema/schema';
import React from 'react';

export interface WorldsProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const Worlds = ({ className }: WorldsProps) => {
    const [worlds, setWorlds] = React.useState<openrpg.GeneratedEntityListItem[]>([]);
    const [worldName, setWorldName] = React.useState<string>('');
    const [refreshCounter, setRefreshCounter] = React.useState<number>(0);

    React.useEffect(() => {
        const onWorlds = (response: openrpg.ListEntitiesResponse) => {
            setWorlds(response.entities);
        };
        getWorlds(onWorlds);
    }, [refreshCounter]);

    const onWorld = (response: openrpg.CreateEntityResponse) => {
        setWorldName('');
        setRefreshCounter(refreshCounter + 1);
    };

    return (
        <div className={classNames(styles.root, className)}>
            <NavigationBar />
            Worlds
            <ul>
                {worlds?.map((world) => (
                    <li key={world.entity_id}>
                        <a href={'/world/' + world.entity_id}>{world.name}</a>
                    </li>
                ))}
            </ul>
            <label>Name:</label>
            <input
                type="text"
                value={worldName}
                onChange={(event) => setWorldName(event.target.value)}
            />
            <button
                onClick={() => createWorld(worldName, onWorld)}
                disabled={worldName.length === 0}
            >
                Create World!
            </button>
        </div>
    );
};
