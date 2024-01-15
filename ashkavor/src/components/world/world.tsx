import classNames from 'classnames';
import styles from './world.module.scss';
import { NavigationBar } from '../navigation-bar/navigation-bar';
import { getWorld, deleteWorld, listEntityTypes } from '../../openrpg/client';
import * as openrpg from '../../openrpg/schema/schema';
import React from 'react';
import { useLocation } from 'react-router-dom';
import { Routes, Route, Link, Outlet } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

export interface EntityLinkProps {
    entityType: openrpg.EntityType1;
}

const EntityLink = ({ entityType }: EntityLinkProps) => {
    return (
        <>
            <span> | </span>
            <Link to={'entities/' + entityType.name}>{entityType.label}</Link>
            {/* {index < entityTypes.length - 1 && ' | '} */}
        </>
    );
};

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
    // TODO: this should not have a 1 in the name
    const [entityTypes, setEntityTypes] = React.useState<openrpg.EntityType1[]>([]);
    // const [breadCrumb, setBreadCrumb] = React.useState<string[]>(['overview']);
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

    React.useEffect(() => {
        listEntityTypes((response: openrpg.ListEntityTypesResponse) => {
            setEntityTypes(
                response.entity_types.filter((entityType) => entityType.name !== 'world')
            );
        });
    }, []);

    return (
        <div className={classNames(styles.root, className)}>
            <NavigationBar />
            <nav>
                <Link to=".">Overview</Link>
                {entityTypes.map((entityType) => (
                    <EntityLink key={entityType.name} entityType={entityType} />
                ))}
            </nav>
            {world.name}
            <Outlet context={world} />
        </div>
    );
};
