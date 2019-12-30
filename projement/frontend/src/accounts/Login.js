import React, { Component } from 'react';
import axios from 'axios';
import 'whatwg-fetch';

class Login extends Component {

    constructor(props) {
        super(props);
        this.state = {
            "username": "",
            "password": "",
        };
    }

    changeHandler = event => {
      this.setState({[event.target.id]: event.target.value})
    };

    handleSubmit = e => {
        e.preventDefault();
        axios
            .post('http://127.0.0.1:8000/api/login/', this.state)
            .then(response => {
                console.log(response);
            })
};

    render() {
        // if (logged === true)
        const {username, password} = this.state;
            return (
                <form onSubmit={this.handleSubmit}>
                    <div className="form-group">
                        <label>Email
                            address</label>
                        <input type="text" name='username' className="form-control"
                               id="username"
                               aria-describedby="emailHelp" value={username} onChange={this.changeHandler}/>
                            <small id="emailHelp"
                                   className="form-text text-muted">We'll never
                                share your email with anyone else.</small>
                    </div>
                    <div className="form-group">
                        <label>Password</label>
                        <input type="password" name='password' className="form-control"
                               id="password" value={password} onChange={this.changeHandler}/>
                    </div>

                    <button type="submit" className="btn btn-primary">Submit
                    </button>
                </form>

            );
        // return <Redirect to="/login"/>
    }
}

export default Login;