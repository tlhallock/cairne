import { createBoard } from '@wixc3/react-board';
import { Items } from '../../../components/items/items';

export default createBoard({
    name: 'Items',
    Board: () => <Items />,
    isSnippet: true,
});
