/** @format */
import { configureStore } from '@reduxjs/toolkit';

import { templatesReducer } from './openrpg/reducers/templates';

export const store = configureStore({
    reducer: {
        templates: templatesReducer,
    },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
