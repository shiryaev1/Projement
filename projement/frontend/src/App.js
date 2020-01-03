import './App.css'
import React, { Component } from 'react';
import Dashboard from "./components/projects/dashboard";
import ProjectCreate from "./components/projects/CreateProject";
import {BrowserRouter, HashRouter as Router, Route, Switch, Redirect} from "react-router-dom";
import Tag from "./components/tags/TagsList";
import TagCreate from "./components/tags/CreateTag";
import Navbar from "./components/Navbar";
import HistoryOfChanges from "./components/projects/HistoryOfChanges";
import HistoryOfChangesDetail from "./components/projects/HistoryOfChangesDetail";
import InitialDataOfProject from "./components/projects/InitialDataOfProject";
import TagDelete from "./components/tags/TagDelete";
import TagUpdate from "./components/tags/TagUpdate";
import ProjectUpdate from "./components/projects/ProjectUpdate";
import Login from "./assets/Auth";
// import {HashRouter as Router, Route, Switch, Redirect} from 'react-router-dom';


class App extends Component {
  render() {
    return (
        <BrowserRouter>
            <Navbar/>
          <div className='app-wrapper' style={{width: '40%'}}>
            <div className='app-wrapper-content'>
              <Switch>
              <Route path='/login' component={Login} />
              <Route exact path='/dashboard' component={Dashboard} />
              <Route path='/project/create' component={ProjectCreate} />
              <Route path='/project/:id/update' component={ProjectUpdate} />
              <Route path='/project/history' component={HistoryOfChanges} />
              <Route path='/project/:id/history' component={HistoryOfChangesDetail} />
              <Route path='/project/:id/initial-data' component={InitialDataOfProject} />
              <Route path='/tags' component={Tag}/>
              <Route path='/tag/create' component={TagCreate}/>
              <Route path='/tag/:id/delete' component={TagDelete}/>
              <Route path='/tag/:id/update' component={TagUpdate}/>
              </Switch>

            </div>
          </div>
        </BrowserRouter>
    );
  }
}
export default App;