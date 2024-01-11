import axios from 'axios';
import * as openrpg from './schema/schema';

axios.defaults.baseURL = 'http://127.0.0.1:5000';
// axios.defaults.po = 5000;
axios.defaults.headers.post['Content-Type'] = 'application/octet-stream';
// axios.defaults.headers.post['Accept'] = 'application/octet-stream';

export const getWorlds = (
    onWorlds: (response: openrpg.ListEntitiesResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    axios
        .get('/worlds')
        .then((r) => onWorlds(r.data))
        .catch(onError);
};

export const getWorld = (
    worldId: openrpg.WorldId,
    onWorld: (response: openrpg.GetEntityResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    axios
        .get('/world/' + worldId)
        .then((r) => onWorld(r.data))
        .catch(onError);
};

export const createWorld = (
    worldName: string,
    onWorld: (response: openrpg.CreateEntityResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    console.log('createWorld', worldName);
    const request: openrpg.CreateWorldRequest = {
        name: worldName,
    };
    axios
        .post('/world', request, { headers: { 'Content-Type': 'application/json' } })
        .then((r) => onWorld(r.data))
        .catch(onError);
};

export const deleteWorld = (
    worldId: openrpg.WorldId,
    onDelete: (response: openrpg.DeleteEntityResponse) => void,
    onError: (error: Error) => void = (error: Error) => console.log(error)
) => {
    axios
        .delete('/world/' + worldId)
        .then((r) => onDelete(r.data))
        .catch(onError);
};
