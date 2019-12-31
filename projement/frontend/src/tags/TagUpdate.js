import React, { Component } from 'react';
import axios from 'axios';

import 'whatwg-fetch';

class TagUpdate extends Component {
    constructor(props) {
        super(props);
        this.state = {
            "title": "",
        };
    }

    changeHandler = e => {
      this.setState({[e.target.name]: e.target.value});
    };

    handleSubmit = event => {
        event.preventDefault();
        const tags = {
            title: this.props.title
        };
        axios
            .put(`http://127.0.0.1:8000/api/tag/${this.props.match.params.id}/update/`, tags);
            console.log(this.props.match.params.id)
            .then(res => {
                console.log(res);
            })
    };
    render() {

        return (

            <form onSubmit={this.handleSubmit}>
                <div className='form-group'>
                    <label >Tag title</label>
                    <input  type="text" value={this.state.value}
                           className='form-control' placeholder='title' onChange={this.changeHandler}  required='required'/>
                </div>
                <button className='bnt btn-danger'>Update</button>

            </form>
        )
    }
}

export default TagUpdate;