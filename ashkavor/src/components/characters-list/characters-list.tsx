import classNames from 'classnames';
import styles from './characters-list.module.scss';
import { Link, Outlet, useOutletContext } from 'react-router-dom';
import * as openrpg from '../../openrpg/schema/schema';

export interface CharactersListProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const CharactersList = ({ className }: CharactersListProps) => {
    const value = useOutletContext<openrpg.World>();
    return (
        <div className={classNames(styles.root, className)}>
            CharactersList
            <ul>
                {value?.characters?.map((character) => (
                    <li key={character.character_id}>
                        <Link to={character.character_id}>{character.name}</Link>
                    </li>
                ))}
            </ul>
        </div>
    );
};
