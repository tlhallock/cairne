import { createBoard } from '@wixc3/react-board';
import { WorldSettings } from '../../../components/world-settings/world-settings';

export default createBoard({
    name: 'WorldSettingsBoard',
    Board: () => <WorldSettings />,
    isSnippet: true,
});
