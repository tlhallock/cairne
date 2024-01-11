import { createBoard } from '@wixc3/react-board';
import { Characters } from '../../../components/characters/characters';

export default createBoard({
    name: 'Characters',
    Board: () => <Characters />,
    isSnippet: true,
});
