import { createSlice } from '@reduxjs/toolkit';

export const alertSlice = createSlice({
    name: 'alert',
    initialState: {
        error: "",
        message: "",
        success: "",
    },
    reducers: {
        success: (state, action) => {
            return {...state, success: action.payload};
        },
        error: (state, action) => {
            return {...state, error: action.payload};
        },
        clear: (state) => {
            return {
                error: "",
                message: "",
                success: "",
            }
        },
    },
});

export const { success, error, clear } = alertSlice.actions

export default alertSlice.reducer