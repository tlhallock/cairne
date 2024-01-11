import { createBoard } from '@wixc3/react-board';
import { CharactersList } from '../../../components/characters-list/characters-list';

export default createBoard({
    name: 'CharactersList',
    Board: () => <CharactersList />,
    isSnippet: true,
});
