import React, { Component } from 'react';

import 'whatwg-fetch';

class TagCreate extends Component {

    constructor(props) {
        super(props);
        this.state = {
            "title": "",
        };
    }
    changeHandler = e => {
      this.setState({[e.target.name]: e.target.value});
    };

    handleSubmit = e => {
        let url = 'http://127.0.0.1:8000/api/tag/create/';
        let data = this.state;
        console.log(data);
        fetch(url, {
          method: "POST",
          headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
          },
          body: JSON.stringify(data)
        }).then((result)=>{
            result.json().then((resp)=>{
              console.warn('resp', resp)
            }).catch(function (error) {
                console.log(error);
            })
        })
    };
    render() {

        return (

            <form onSubmit={this.handleSubmit}>
                <div className='form-group'>
                    <label >Tag title</label>
                    <input  type="text" name="title" id="id_title"
                           className='form-control' placeholder='title' onChange={this.changeHandler}  required='required'/>
                </div>
                <button className='bnt btn-danger'>Save</button>

            </form>
        )
    }
}

export default TagCreate;