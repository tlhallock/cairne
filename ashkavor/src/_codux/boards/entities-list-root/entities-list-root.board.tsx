import { createBoard } from '@wixc3/react-board';
import { EntitiesListRoot } from '../../../components/entities-list-root/entities-list-root';

export default createBoard({
    name: 'EntitiesListRoot',
    Board: () => <EntitiesListRoot />,
    isSnippet: true,
});
