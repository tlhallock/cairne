import { createBoard } from '@wixc3/react-board';
import { LoadedModels } from '../../../components/loaded-models/loaded-models';

export default createBoard({
    name: 'LoadedModels',
    Board: () => <LoadedModels />,
    isSnippet: true,
});
