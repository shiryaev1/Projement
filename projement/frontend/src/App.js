// import './App.css'
// import React, { Component } from 'react';
// import Dashboard from "./components/projects/dashboard";
// import ProjectCreate from "./components/projects/CreateProject";
// import {BrowserRouter, Route} from "react-router-dom";
// import Tag from "./components/tags/TagsList";
// import TagCreate from "./components/tags/CreateTag";
// import Navbar from "./components/Navbar";
// import HistoryOfChanges from "./components/projects/HistoryOfChanges";
// import HistoryOfChangesDetail from "./components/projects/HistoryOfChangesDetail";
// import InitialDataOfProject from "./components/projects/InitialDataOfProject";
// import TagDelete from "./components/tags/TagDelete";
// import TagUpdate from "./components/tags/TagUpdate";
// import ProjectUpdate from "./components/projects/ProjectUpdate";
// import Login from "./assets/Auth";
//
//
// class App extends Component {
//   render() {
//     return (
//         <BrowserRouter>
//             <Navbar/>
//           <div className='app-wrapper' style={{width: '40%'}}>
//             <div className='app-wrapper-content'>
//               <Route path='/login' component={Login} />
//               <Route path='/dashboard' component={Dashboard} />
//               <Route path='/project/create' component={ProjectCreate} />
//               <Route path='/project/:id/update' component={ProjectUpdate} />
//               <Route path='/project/history' component={HistoryOfChanges} />
//               <Route path='/project/:id/history' component={HistoryOfChangesDetail} />
//               <Route path='/project/:id/initial-data' component={InitialDataOfProject} />
//               <Route path='/tags' component={Tag}/>
//               <Route path='/tag/create' component={TagCreate}/>
//               <Route path='/tag/:id/delete' component={TagDelete}/>
//               <Route path='/tag/:id/update' component={TagUpdate}/>
//
//             </div>
//           </div>
//         </BrowserRouter>
//     );
//   }
// }
// export default App;
import React, { Component } from 'react';
import Nav from './components/Nav';
import LoginForm from './components/LoginForm';
import SignupForm from './components/SignupForm';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      displayed_form: '',
      logged_in: localStorage.getItem('token') ? true : false,
      username: ''
    };
  }

  componentDidMount() {
    if (this.state.logged_in) {
      fetch('http://localhost:8000/api/current_user/', {
        headers: {
          Authorization: `JWT ${localStorage.getItem('token')}`
        }
      })
        .then(res => res.json())
        .then(json => {
          this.setState({ username: json.username });
        });
    }
  }

  handle_login = (e, data) => {
    e.preventDefault();
    fetch('http://localhost:8000/token-auth/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(res => res.json())
      .then(json => {
        localStorage.setItem('token', json.token);
        this.setState({
          logged_in: true,
          displayed_form: '',
          username: json.user.username
        });
      });
  };

  handle_signup = (e, data) => {
    e.preventDefault();
    fetch('http://localhost:8000/api/users/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(res => res.json())
      .then(json => {
        localStorage.setItem('token', json.token);
        this.setState({
          logged_in: true,
          displayed_form: '',
          username: json.username
        });
      });
  };

  handle_logout = () => {
    localStorage.removeItem('token');
    this.setState({ logged_in: false, username: '' });
  };

  display_form = form => {
    this.setState({
      displayed_form: form
    });
  };

  render() {
    let form;
    switch (this.state.displayed_form) {
      case 'login':
        form = <LoginForm handle_login={this.handle_login} />;
        break;
      case 'signup':
        form = <SignupForm handle_signup={this.handle_signup} />;
        break;
      default:
        form = null;
    }

    return (
      <div className="App">
        <Nav
          logged_in={this.state.logged_in}
          display_form={this.display_form}
          handle_logout={this.handle_logout}
        />
        {form}
        <h3>
          {this.state.logged_in
            ? `Hello, ${this.state.username}`
            : 'Please Log In'}
        </h3>
      </div>
    );
  }
}

export default App;