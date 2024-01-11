import classNames from 'classnames';
import styles from './regions.module.scss';

export interface RegionsProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const Regions = ({ className }: RegionsProps) => {
    return <div className={classNames(styles.root, className)}>Regions</div>;
};
