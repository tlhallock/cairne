import { createBoard } from '@wixc3/react-board';
import { WorldEntitiesList } from '../../../components/world-entities-list/world-entities-list';

export default createBoard({
    name: 'WorldEntitiesList',
    Board: () => <WorldEntitiesList />,
    isSnippet: true,
});
