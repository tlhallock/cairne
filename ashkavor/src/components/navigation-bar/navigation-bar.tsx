import classNames from 'classnames';
import styles from './navigation-bar.module.scss';
import { Link } from 'react-router-dom';

export interface NavigationBarProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const NavigationBar = ({ className }: NavigationBarProps) => {
    return (
        <div className={classNames(styles.root, className)}>
            <nav>
                <Link to="/">Home</Link> | <Link to="/worlds">Worlds</Link> |{' '}
                <Link to="/models">Loaded Models</Link>
            </nav>
        </div>
    );
};
