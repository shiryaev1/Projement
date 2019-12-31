import './App.css'
import React, { Component } from 'react';
import Dashboard from "./projects/dashboard";
import ProjectCreate from "./projects/CreateProject";
import {BrowserRouter, Route} from "react-router-dom";
import Tag from "./tags/TagsList";
import TagCreate from "./tags/CreateTag";
import Navbar from "./components/Navbar";
import Login from "./accounts/Login";
import HistoryOfChanges from "./projects/HistoryOfChanges";
import HistoryOfChangesDetail from "./projects/HistoryOfChangesDetail";
import InitialDataOfProject from "./projects/InitialDataOfProject";
import TagDelete from "./tags/TagDelete";
import TagUpdate from "./tags/TagUpdate";

class App extends Component {
  render() {
    return (
        <BrowserRouter>
            <Navbar/>
          <div className='app-wrapper' style={{width: '40%'}}>
            <div className='app-wrapper-content'>
              <Route path='/login' component={Login} />
              <Route path='/dashboard' component={Dashboard} />
              <Route path='/project/create' component={ProjectCreate} />
              <Route path='/project/history' component={HistoryOfChanges} />
              <Route path='/project/:id/history' component={HistoryOfChangesDetail} />
              <Route path='/project/:id/initial-data' component={InitialDataOfProject} />
              <Route path='/tags' component={Tag}/>
              <Route path='/tag/create' component={TagCreate}/>
              <Route path='/tag/:id/delete' component={TagDelete}/>
              <Route path='/tag/:id/update' component={TagUpdate}/>
            </div>
          </div>
        </BrowserRouter>
    );
  }
}
export default App;