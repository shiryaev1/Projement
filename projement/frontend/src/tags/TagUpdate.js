import React, { Component } from 'react';
import axios from 'axios';

import 'whatwg-fetch';

class TagUpdate extends Component {
    constructor(props) {
        super(props);
        this.state = {
            title: "",
        };
    }

    changeHandler = e => {
      this.setState({[e.target.name]: e.target.value});
    };

    handleSubmit = event => {
        event.preventDefault();
        const tags = {
            title: this.state.title
        };
        axios
            .put(`http://127.0.0.1:8000/api/tag/${this.props.match.params.id}/update/`, tags)
            .then(res => {
                console.log(res);
            })
    };
    render() {

        return (

            <form onSubmit={this.handleSubmit}>
                <div className='form-group'>
                    <label >Tag title</label>
                    <input  type="text"
                           className='form-control' name='title' placeholder='title' onChange={this.changeHandler}  required='required'/>
                </div>
                <button className='bnt btn-danger'>Update</button>

            </form>
        )
    }
}

export default TagUpdate;