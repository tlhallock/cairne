import { createBoard } from '@wixc3/react-board';
import { StoryElements } from '../../../components/story-elements/story-elements';

export default createBoard({
    name: 'StoryElements',
    Board: () => <StoryElements />,
    isSnippet: true,
});
