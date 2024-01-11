import classNames from 'classnames';
import styles from './characters.module.scss';
import { Link, Outlet, useOutletContext } from 'react-router-dom';
import * as openrpg from '../../openrpg/schema/schema';

export interface CharactersProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const Characters = ({ className }: CharactersProps) => {
    const value = useOutletContext<openrpg.World>();
    return (
        <div className={classNames(styles.root, className)}>
            <Outlet context={value} />
        </div>
    );
};
