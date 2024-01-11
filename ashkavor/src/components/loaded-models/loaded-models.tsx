import classNames from 'classnames';
import styles from './loaded-models.module.scss';

import { NavigationBar } from '../navigation-bar/navigation-bar';

export interface LoadedModelsProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const LoadedModels = ({ className }: LoadedModelsProps) => {
    return (
        <div className={classNames(styles.root, className)}>
            <NavigationBar />
            LoadedModels
        </div>
    );
};
