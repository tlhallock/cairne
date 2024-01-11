import { createBoard } from '@wixc3/react-board';
import { Crafting } from '../../../components/crafting/crafting';

export default createBoard({
    name: 'Crafting',
    Board: () => <Crafting />,
    isSnippet: true,
});
