import { useState } from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { LoadedModels } from './components/loaded-models/loaded-models';
import { Worlds } from './components/worlds/worlds';
import { World } from './components/world/world';
import { Landing } from './components/landing/landing';
import { Characters } from './components/characters/characters';
import { Items } from './components/items/items';
import { Resources } from './components/resources/resources';
import { StoryElements } from './components/story-elements/story-elements';
import { WorldSettings } from './components/world-settings/world-settings';
import { Regions } from './components/regions/regions';
import { Character } from './components/character/character';
import { Crafting } from './components/crafting/crafting';
import { CharactersList } from './components/characters-list/characters-list';
import { WorldEntitiesList } from './components/world-entities-list/world-entities-list';
import { EntityEditor } from './components/entity-editor/entity-editor';
import { EntitiesListRoot } from './components/entities-list-root/entities-list-root';
import { Generation } from './components/generation/generation';

import './App.module.scss';

import { Routes, Route, Link, Outlet, BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './store';

import * as React from 'react';

// I could have the world be under worlds...
function App() {
    return (
        <React.StrictMode>
            <Provider store={store}>
                <BrowserRouter>
                    <Routes>
                        <Route path="/" element={<Landing />} />
                        <Route path="/models" element={<LoadedModels />} />
                        <Route path="/worlds" element={<Worlds />} />
                        <Route path="/world/:worldId" element={<World />}>
                            <Route index element={<WorldSettings />} />
                            {/* <Route path="characters" element={<Characters />}>
                            <Route index element={<CharactersList />} />
                            <Route path=":characterId" element={<Character />} />
                        </Route> */}
                            <Route path="entities/:entityType" element={<EntitiesListRoot />}>
                                <Route index element={<WorldEntitiesList />} />
                                <Route path=":entityId" element={<EntityEditor />} />
                            </Route>
                        </Route>
                        <Route path="/generation/:generationId" element={<Generation />} />
                    </Routes>
                </BrowserRouter>
                {/* <RouterProvider router={router} /> */}
            </Provider>
        </React.StrictMode>
    );
}

export default App;
