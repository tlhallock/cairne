import { createBoard } from '@wixc3/react-board';
import { Character } from '../../../components/character/character';

export default createBoard({
    name: 'Character',
    Board: () => <Character />,
    isSnippet: true,
});
