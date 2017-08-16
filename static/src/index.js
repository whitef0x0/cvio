import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { Router, Redirect } from 'react-router';
import { ConnectedRouter, syncHistoryWithStore } from 'react-router-redux';
import { createBrowserHistory } from 'history';

import configureStore from './store/configureStore';
import routes from './routes';
import './style.scss';

require('expose-loader?$!expose-loader?jQuery!jquery');
require('bootstrap-webpack');

const store = configureStore();
const history = syncHistoryWithStore(createBrowserHistory(), store);

const renderAll = () => {
    ReactDOM.render(
        <Provider store={store}>
            <Router history={history}>
            {routes}
            </Router>
        </Provider>,
        document.getElementById('root')
    );
}

store.subscribe(renderAll);
renderAll();