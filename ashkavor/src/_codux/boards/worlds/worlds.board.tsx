import { createBoard } from '@wixc3/react-board';
import { Worlds } from '../../../components/worlds/worlds';

export default createBoard({
    name: 'Worlds',
    Board: () => <Worlds />,
    isSnippet: true,
});
