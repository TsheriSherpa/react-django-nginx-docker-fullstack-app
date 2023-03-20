import { configureStore } from '@reduxjs/toolkit'
import { logger } from 'redux-logger';

import alertReducer from './reducers/alertReducer'
import counterReducer from './reducers/counterReducer';
import userReducer from './reducers/userReducer';

export const store = configureStore({
    reducer: {
        user: userReducer,
        alert: alertReducer,
        counter: counterReducer
    },
    middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(logger)
});