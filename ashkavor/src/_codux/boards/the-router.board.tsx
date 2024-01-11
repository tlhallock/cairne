import { createBoard } from '@wixc3/react-board';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import * as React from 'react';

const router = createBrowserRouter([
    {
        path: '/',
        element: <div>Loaded Models</div>,
    },
    {
        path: '/worlds',
        element: <div>All Worlds</div>,
    },
    {
        path: '/world/:worldId',
        element: <div>Hello world!</div>,
    },
]);

export default createBoard({
    name: 'TheRouter',
    Board: () => (
        <React.StrictMode>
            <RouterProvider router={router} />
        </React.StrictMode>
    ),
    isSnippet: true,
});
