import React, { Component } from 'react';

import 'whatwg-fetch';
// import * as ReactRouterDOM from "react-router-dom";

// const Redirect = ReactRouterDOM.Redirect;
// let logged = false;

class ProjectCreate extends Component {

    constructor(props) {
        super(props);
        this.state = {
            "tags": [],
            "title": "",
            "start_date": null,
            "end_date": null,
            "estimated_design": null,
            "actual_design": null,
            "estimated_development": null,
            "actual_development": null,
            "estimated_testing": null,
            "actual_testing": null,
            "company": null,

            companies: [],
            tagList: [],
        };
    }
    changeHandler = e => {
      this.setState({[e.target.name]: e.target.value})
    };

    handleSubmit = e => {
        let url = 'http://127.0.0.1:8000/api/project/create/';
        let data = this.state;

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

    async componentDidMount() {
    try {
      const responseCompanies = await fetch('http://127.0.0.1:8000/api/company/create/');
      const companies = await responseCompanies.json();
      // const responseTagList = await fetch('http://127.0.0.1:8000/api/tag/create/');
      // const tagList = await responseTagList.json();
      this.setState({
        companies,
        // tagList,
      });
      console.log(this.state);
    } catch (e) {
      console.log(e);
    }
  }

    render() {
        // if (logged === true)
            return (

                <form onSubmit={this.handleSubmit} style={{width: '25%'}}>
                    <div className='form-group'>
                        <label>Project company</label>
                        <select name="company"  className="select form-control"
                               id="company"  onChange={this.changeHandler} required='required'>
                            <option value="" selected="">---------</option>
                            {this.state.companies.map(item => (
                                <option value={item.id}>{item.name}</option>
                            ))}

                        </select>
                    </div>

                    <div className='form-group'>
                        <label>Project title</label>
                        <input type='text' id='title' name='title'
                               className='form-control' placeholder='title'  onChange={this.changeHandler} required='required'/>
                    </div>
                    <div className='form-group'>
                        <label >Project start date</label>
                        <input type='date' id='start' name='start_date'
                               className='form-control' placeholder='start'  onChange={this.changeHandler} required='required'/>
                    </div>
                    <div className='form-group'>
                        <label >Project end date</label>
                        <input type='date' id='end' name='end_date'
                               className='form-control' placeholder='end'  onChange={this.changeHandler} />
                    </div>
                    <div className='form-group'>
                        <label >Estimated design hours</label>
                        <input type='number' id='design' name='estimated_design'
                               className='form-control' placeholder='0' onChange={this.changeHandler}  required='required'/>
                    </div>
                    <div className='form-group'>
                        <label >Actual design hours</label>
                        <input type='number' id='ac-design' name='actual_design'
                               className='form-control' placeholder='0'  onChange={this.changeHandler} required='required'/>
                    </div>
                    <div className='form-group'>
                        <label >Estimated development hours</label>
                        <input type='number' id='est-dev' name='estimated_development'
                               className='form-control' placeholder='0' onChange={this.changeHandler} required='required'/>
                    </div>
                     <div className='form-group'>
                        <label >Actual development hours</label>
                        <input type='number' id='dev' name='actual_development'
                               className='form-control' placeholder='0' onChange={this.changeHandler} required='required'/>
                    </div>
                    <div className='form-group'>
                        <label>Estimated testing hours</label>
                        <input type='number' id='test' name='estimated_testing'
                               className='form-control' placeholder='0' onChange={this.changeHandler} required='required'/>
                    </div>
                    <div className='form-group'>
                        <label >Actual testing hours</label>
                        <input type='number' id='ac-test' name='actual_testing'
                               className='form-control' placeholder='0' onChange={this.changeHandler}  required='required'/>
                    </div>
                    {/*<div className='form-group'>*/}
                    {/*    <label>Tags</label>*/}
                    {/*    <select name="tags" className="select form-control"*/}
                    {/*           id="tags"  onChange={this.changeHandler} required='required'>*/}
                    {/*        <option value="" selected="">---------</option>*/}

                            {/*{this.state.tagList.map(item => (*/}
                            {/*    <option value={Array([item.id])}>{item.title}</option>*/}
                            {/*))}*/}

                    {/*    </select>*/}
                    {/*</div>*/}
                    <button className='bnt btn-outline-primary'>Save</button>

                </form>
            );
        // return <Redirect to="/login"/>
    }
}

export default ProjectCreate;