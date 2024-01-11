import { createBoard } from '@wixc3/react-board';
import { Resources } from '../../../components/resources/resources';

export default createBoard({
    name: 'Resources',
    Board: () => <Resources />,
    isSnippet: true,
});
