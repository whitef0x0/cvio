/* eslint new-cap: 0 */

import React from 'react';
import { Route } from 'react-router';

/* containers */
import { App } from './containers/App';
import { HomeContainer } from './containers/HomeContainer';
import LoginView from './components/LoginView';
import RegisterView from './components/RegisterView';
import ProtectedView from './components/ProtectedView';
import cvEditor from './components/cvEditor';
import NotFound from './components/NotFound';

import { DetermineAuth } from './components/DetermineAuth';
import { requireAuthentication } from './components/AuthenticatedComponent';
import { requireNoAuthentication } from './components/notAuthenticatedComponent';

export default (
    <div>
        <App>
        {/*<Route exact path="/main" component={requireAuthentication(ProtectedView)} />
        <Route path="/login" component={requireNoAuthentication(LoginView)} />
        <Route path="/register" component={requireNoAuthentication(RegisterView)} />
        <Route path="/home" component={requireNoAuthentication(HomeContainer)} />*/}
        <Route path="/" component={requireNoAuthentication(cvEditor)} />
        <Route path="*" component={DetermineAuth(NotFound)} />
        </App>
    </div>
);
