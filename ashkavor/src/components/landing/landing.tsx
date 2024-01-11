import classNames from 'classnames';
import styles from './landing.module.scss';
import { NavigationBar } from '../navigation-bar/navigation-bar';

export interface LandingProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const Landing = ({ className }: LandingProps) => {
    return (
        <div className={classNames(styles.root, className)}>
            <NavigationBar />
            Landing
        </div>
    );
};
