import './App.css'
import React, { Component } from 'react';
import Dashboard from "./projects/dashboard";
import ProjectCreate from "./projects/CreateProject";
import {BrowserRouter, Route} from "react-router-dom";
import Tag from "./tags/TagsList";
import TagCreate from "./tags/CreateTag";
import Navbar from "./components/Navbar";
import Login from "./accounts/Login";

class App extends Component {
  render() {
    return (
        <BrowserRouter>
            <Navbar/>
          <div className='app-wrapper'>
            <div className='app-wrapper-content'>
              <Route path='/login' component={Login} />
              <Route path='/dashboard' component={Dashboard} />
              <Route path='/project/create' component={ProjectCreate} />
              <Route path='/tags' component={Tag}/>
              <Route path='/tag/create' component={TagCreate}/>
            </div>
          </div>
        </BrowserRouter>
    );
  }
}
export default App;