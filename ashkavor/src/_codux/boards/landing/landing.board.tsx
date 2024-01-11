import { createBoard } from '@wixc3/react-board';
import { Landing } from '../../../components/landing/landing';

export default createBoard({
    name: 'Landing',
    Board: () => <Landing />,
    isSnippet: true,
});
