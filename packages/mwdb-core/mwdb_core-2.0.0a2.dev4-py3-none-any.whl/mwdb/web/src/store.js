import { createStore, applyMiddleware, combineReducers } from "redux";
import reduxThunk from "redux-thunk";
import { connectRouter, routerMiddleware } from 'connected-react-router'
import { composeWithDevTools } from 'redux-devtools-extension';

import api from "@malwarefront/api";
import {authActions, authService, authReducer} from "@malwarefront/auth";
import {configReducer} from "@malwarefront/config";
import history from "@malwarefront/history";
import { fromPlugin } from "@malwarefront/extensions";

let reducers = combineReducers({
    auth: authReducer,
    config: configReducer,
    router: connectRouter(history)
});

for(let extraReducers of fromPlugin("reducers"))
    reducers = {...reducers, ...extraReducers}

let middlewares = [
    reduxThunk,
    routerMiddleware(history),
    ...fromPlugin("middlewares")
];

let store = createStore(
    reducers,
    {},
    composeWithDevTools(
        applyMiddleware(
            ...middlewares
        )
    ),
);

if(store.getState().auth.loggedUser)
{
    let token = store.getState().auth.loggedUser.token;
    api.axios.defaults.headers.common['Authorization'] = 'Bearer ' + token
}

authService.refreshService.refreshToken();

api.axios.interceptors.response.use(_=>_, error =>
{
    if (error.response && error.response.status === 401)
    {
        store.dispatch(authActions.logout({error: "Session expired. Please authenticate before accessing this page"}, history.location))
    }
    return Promise.reject(error)
});

export default store;