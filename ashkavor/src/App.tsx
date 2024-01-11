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

import { Routes, Route, Link, Outlet, BrowserRouter } from 'react-router-dom';

import * as React from 'react';

// I could have the world be under worlds...
function App() {
    return (
        <React.StrictMode>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Landing />} />
                    <Route path="/models" element={<LoadedModels />} />
                    <Route path="/worlds" element={<Worlds />} />
                    <Route path="/world/:worldId" element={<World />}>
                        <Route path="details" element={<WorldSettings />} />
                        <Route path="characters" element={<Characters />}>
                            <Route index element={<CharactersList />} />
                            <Route path=":characterId" element={<Character />} />
                        </Route>
                        <Route path="items" element={<Items />} />
                        <Route path="resources" element={<Resources />} />
                        <Route path="story_elements" element={<StoryElements />} />
                        <Route path="regions" element={<Regions />} />
                        <Route path="crafting" element={<Crafting />} />
                    </Route>
                </Routes>
            </BrowserRouter>
            {/* <RouterProvider router={router} /> */}
        </React.StrictMode>
    );
}

export default App;
