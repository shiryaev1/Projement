import React, { Component } from 'react';
import axios from 'axios';

import 'whatwg-fetch';

class ProjectUpdate extends Component {
    constructor(props) {
        super(props);
        this.state = {
            "actual_design": "",
            "actual_development": "",
            "actual_testing": ""
        };
    }

    changeHandler = e => {
      this.setState({[e.target.name]: e.target.value});
    };

    handleSubmit = event => {
        event.preventDefault();
        // const tags = {
        //     title: this.state.title
        // };
        axios
            .put(`http://127.0.0.1:8000/api/project/${this.props.match.params.id}/update/`, this.state)
            .then(res => {
                console.log(res);
            })
    };
    render() {

        return (

           <form onSubmit={this.handleSubmit} style={{width: '25%'}}>

                    <div className='form-group'>
                        <label>Actual design</label>
                        <input type='number' id='design' name='actual_design'
                               className='form-control' placeholder='0'  onChange={this.changeHandler} />
                    </div>

                    <div className='form-group'>
                        <label >Actual development</label>
                        <input type='number' id='development' name='actual_development'
                               className='form-control' placeholder='0' onChange={this.changeHandler} />
                    </div>
                    <div className='form-group'>
                        <label >Actual testing</label>
                        <input type='number' id='testing' name='actual_testing'
                               className='form-control' placeholder='0'  onChange={this.changeHandler} />
                    </div>

                    <button className='bnt btn-outline-primary'>Update</button>

                </form>
        )
    }
}

export default ProjectUpdate;