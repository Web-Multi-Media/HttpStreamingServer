// frontend/src/index.js

import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css'; // add this
import * as serviceWorker from './serviceWorker';
import * as Sentry from '@sentry/browser';
import App from './components/App';

if(process.env.REACT_APP_SENTRY_DSN){
    Sentry.init({dsn: process.env.REACT_APP_SENTRY_DSN});
}

ReactDOM.render(
    <BrowserRouter>
        <App />
    </BrowserRouter>, document.getElementById('root'),
);
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
serviceWorker.unregister();
