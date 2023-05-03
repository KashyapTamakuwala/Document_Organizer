import React from "react";
import {Router, Route, Switch} from "react-router-dom";
import createHistory from "history/createBrowserHistory";
import Login from '../pages/Login'
import Register from "../pages/Register";
import Main from '../pages/Main';
import dD from "../components/drop-file-input/dropdialog";




export const history = createHistory()

export const AppRouter = () => (

    <Router history={history} >

    <Switch>
        <Route path = "/" exact={true} component={Login}/>
        <Route path = "/register" component={Register}/>
        <Route path = "/homepage" component={Main}/>
        <Route path = '/temp' component={dD}/>
    </Switch>

    </Router>
)

export default AppRouter;

