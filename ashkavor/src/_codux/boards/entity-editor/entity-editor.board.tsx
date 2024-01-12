import { createBoard } from '@wixc3/react-board';
import { EntityEditor } from '../../../components/entity-editor/entity-editor';

export default createBoard({
    name: 'EntityEditor',
    Board: () => <EntityEditor />,
    isSnippet: true,
});
