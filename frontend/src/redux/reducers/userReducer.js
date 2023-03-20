import { createSlice } from '@reduxjs/toolkit';

let user = JSON.parse(localStorage.getItem('user'));
const initialState = user ? { loggedIn: true, user: user } : { loggedIn: false, user: null};

export const userSlice = createSlice({
    name: 'user',
    initialState: initialState,
    reducers: {
        login: (state, action) => {
            return {
                loggedIn: true,
                user: action.payload
            };
        },
        logout: (state) => {
            return {loggedIn: false, user: null};
        },
        clear: (state) => {
            state.error = "";
            state.success = "";
            state.message = "";
        },
    },
});

export const { login, logout, clear } = userSlice.actions

export default userSlice.reducer