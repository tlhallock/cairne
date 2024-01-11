import { createBoard } from '@wixc3/react-board';
import { World } from '../../../components/world/world';

export default createBoard({
    name: 'World',
    Board: () => <World />,
    isSnippet: true,
});
