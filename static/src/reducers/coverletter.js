import { FETCH_COVERLETTER_STATS_REQUEST, RECEIVE_COVERLETTER_STATS, RECEIVE_COVERLETTER_STATS_ERROR, SET_COVERLETTER_TEXT, CLEAR_COVERLETTER_TEXT, CLEAR_COVERLETTER_STATS } from '../constants';
import { createReducer } from '../utils/misc';

const initialState = {
    stats: null,
    isFetching: false,
    loaded: false,
    text: '',
    title: ''
};

export default createReducer(initialState, {
    [RECEIVE_COVERLETTER_STATS_ERROR]: (state, payload) =>
        Object.assign({}, state, {
            error: payload.error,
            isFetching: false,
            loaded: true,
        }),
    [RECEIVE_COVERLETTER_STATS]: (state, payload) =>
        Object.assign({}, state, {
            stats: payload.stats,
            isFetching: false,
            loaded: true,
        }),
    [FETCH_COVERLETTER_STATS_REQUEST]: (state) =>
        Object.assign({}, state, {
            isFetching: true,
        }),

    [SET_COVERLETTER_TEXT]: (state, payload) =>
        Object.assign({}, state, {
            text: payload.coverletter_text,
        }),

    [CLEAR_COVERLETTER_TEXT]: (state) =>
        Object.assign({}, state, {
            text: '',
        }),
    [CLEAR_COVERLETTER_STATS]: (state) =>
        Object.assign({}, state, {
            stats: null,
        }),
});
