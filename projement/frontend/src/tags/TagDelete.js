import React, { Component } from 'react';
import axios from 'axios';

import 'whatwg-fetch';

class TagDelete extends Component {

    changeHandler = e => {
      this.setState({id: e.target.value});
    };

    handleSubmit = event => {
        event.preventDefault();
        axios
            .delete(`http://127.0.0.1:8000/api/tag/${this.props.match.params.id}/delete/`)
            .then(res => {
                console.log(res);
            })
    };
    render() {

        return (

            <form onSubmit={this.handleSubmit}>
                <div className='form-group'>
                    <label >Tag title</label>
                    <input  type="number" value={this.props.match.params.id}
                           className='form-control' placeholder='title' onChange={this.changeHandler}  required='required'/>
                </div>
                <button className='bnt btn-danger'>Delete</button>

            </form>
        )
    }
}

export default TagDelete;