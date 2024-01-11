import { createBoard } from '@wixc3/react-board';
import { Regions } from '../../../components/regions/regions';

export default createBoard({
    name: 'Regions',
    Board: () => <Regions />,
    isSnippet: true,
});
