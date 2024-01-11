import classNames from 'classnames';
import styles from './items.module.scss';

export interface ItemsProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const Items = ({ className }: ItemsProps) => {
    return <div className={classNames(styles.root, className)}>Items</div>;
};
