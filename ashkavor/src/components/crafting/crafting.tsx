import classNames from 'classnames';
import styles from './crafting.module.scss';

export interface CraftingProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const Crafting = ({ className }: CraftingProps) => {
    return <div className={classNames(styles.root, className)}>Crafting</div>;
};
