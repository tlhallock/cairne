import classNames from 'classnames';
import styles from './world.module.scss';
import { NavigationBar } from '../navigation-bar/navigation-bar';
import { getWorld, deleteWorld } from '../../openrpg/client';
import * as openrpg from '../../openrpg/schema/schema';
import React from 'react';
import { useLocation } from 'react-router-dom';
import { Routes, Route, Link, Outlet } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

export interface WorldProps {
    className?: string;
}

const createInitialWorld = (): openrpg.GeneratedEntity => ({
    entity_id: '',
    name: '',
    created_at: '',
    updated_at: '',
    image_uri: null,
    characters: [],
    path: { path_elements: [] },
    fields: [],
    js: '',
});

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const World = ({ className }: WorldProps) => {
    // use a nested router for the children?
    const location = useLocation();
    const [world, setWorld] = React.useState<openrpg.GeneratedEntity>(createInitialWorld());
    const [breadCrumb, setBreadCrumb] = React.useState<string[]>(['overview']);
    const navigate = useNavigate();

    const worldId = location.pathname.split('/')[2];

    React.useEffect(() => {
        if (!worldId) {
            return;
        }
        getWorld(worldId, (response: openrpg.GetEntityResponse) => {
            setWorld(response.entity);
        });
    }, [worldId]);

    const onDelete = (response: openrpg.DeleteEntityResponse) => {
        navigate('/worlds');
    };

    return (
        <div className={classNames(styles.root, className)}>
            <NavigationBar />
            <nav>
                <Link to="details">Details</Link> | <Link to="characters">Characters</Link> |{' '}
                <Link to="items">Items</Link> | <Link to="resources">Resources</Link> |{' '}
                <Link to="story_elements">Story Elements</Link> | <Link to="regions">Regions</Link>{' '}
                | <Link to="crafting">Crafting</Link>
            </nav>
            {world.name}
            <button onClick={() => deleteWorld(worldId, onDelete)}>Delete</button>
            <ul>
                <li>Created At: {world.created_at}</li>
                <li>Updated At: {world.updated_at}</li>
            </ul>
            <Outlet context={world} />
        </div>
    );
};