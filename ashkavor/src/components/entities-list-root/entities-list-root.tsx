import classNames from 'classnames';
import styles from './entities-list-root.module.scss';
import * as openrpg from '../../openrpg/schema/schema';

import { Link, Outlet, useOutletContext, useLocation } from 'react-router-dom';

export interface EntitiesListRootProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const EntitiesListRoot = ({ className }: EntitiesListRootProps) => {
    const location = useLocation();
    const context = useOutletContext<openrpg.GeneratedEntity>();
    const entityType = location.pathname.split('/')[4];
    return (
        <div className={classNames(styles.root, className)}>
            {entityType}
            <Outlet context={context} />
        </div>
    );
};
