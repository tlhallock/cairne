import classNames from 'classnames';
import styles from './story-elements.module.scss';

export interface StoryElementsProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const StoryElements = ({ className }: StoryElementsProps) => {
    return <div className={classNames(styles.root, className)}>StoryElements</div>;
};
