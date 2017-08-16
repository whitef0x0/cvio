import {
    FETCH_COVERLETTER_STATS_REQUEST,
    RECEIVE_COVERLETTER_STATS,
    RECEIVE_COVERLETTER_STATS_ERROR,
    SET_COVERLETTER_TEXT,
    CLEAR_COVERLETTER_TEXT,
    CLEAR_COVERLETTER_STATS
} from '../constants/index';

import { parseJSON } from '../utils/misc';
import { get_coverletter_stats } from '../utils/http_functions';

export function receiveCoverLetterStatsError(error) {
    return {
        type: RECEIVE_COVERLETTER_STATS_ERROR,
        payload: {
            error,
        },
    };
}

export function receiveCoverLetterStats(stats) {
    return {
        type: RECEIVE_COVERLETTER_STATS,
        payload: {
            stats,
        },
    };
}

export function fetchCoverLetterStatsRequest() {
    return {
        type: FETCH_COVERLETTER_STATS_REQUEST,
    };
}

export function setCoverLetterTextRequest(coverletter_text) {
    return {
        type: SET_COVERLETTER_TEXT,
        payload: {
            coverletter_text,
        },
    };
}

export function clearCoverLetterTextRequest() {
    return {
        type: CLEAR_COVERLETTER_TEXT
    };
}

export function clearCoverLetterStatsRequest() {
    return {
        type: CLEAR_COVERLETTER_STATS
    };
}


export function setCoverLetterText(coverletter_text){
    return (dispatch) => {
        dispatch(setCoverLetterTextRequest(coverletter_text))
    }
}

export function clearCoverLetterText(){
    return (dispatch) => {
        dispatch(clearCoverLetterTextRequest())
    }
}

export function clearCoverLetterStats(){
    return (dispatch) => {
        dispatch(clearCoverLetterStatsRequest())
    }
}

export const getCoverLetterData = function(state) {
  return state.coverletter.stats;
}

export function fetchCoverLetterStats(coverletter, cb) {
    return (dispatch) => {
        dispatch(fetchCoverLetterStatsRequest());
        get_coverletter_stats(coverletter)
            .then(parseJSON)
            .then(response => {
                console.log(response.results);
                dispatch(receiveCoverLetterStats(response.results));
                cb(null)
            })
            .catch(error => {
                var errorType = 'serverError';
                if(error.response.status === 406 && error.response.data.message === "No paragraphs found in text"){
                  errorType = 'needMoreText';
                }
                dispatch(receiveCoverLetterStatsError(errorType));
                cb(error);
            });
    };
}

