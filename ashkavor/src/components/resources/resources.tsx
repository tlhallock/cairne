import classNames from 'classnames';
import styles from './resources.module.scss';

export interface ResourcesProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const Resources = ({ className }: ResourcesProps) => {
    return <div className={classNames(styles.root, className)}>Resources</div>;
};
