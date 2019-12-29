import React, { Component } from 'react';
// import cookie from 'react-cookies';
// import axios from 'axios'
import 'whatwg-fetch';

class ProjectCreate extends Component {
    // data = {
    //     companies: []
    // };
    constructor(props) {
        super(props);
        this.state = {
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
            companies: []
        };
        console.log(this.state);
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

  //       this.handleSubmit = this.handleSubmit.bind(this);
  //       this.handleInputChange = this.handleInputChange.bind(this);
  //   }
  //   createPost(data){
  //     const endpoint = 'http://127.0.0.1:8000/api/project/create/' ;
  //     const csrfToken = cookie.load('csrftoken');
  //     // let thisComp = this;
  //
  //     if (csrfToken !== undefined) {
  //         let lookupOptions = {
  //             method: "POST",
  //             headers: {
  //                 'Content-Type': 'application/json',
  //                 'X-CSRFToken': csrfToken,
  //             },
  //             body: JSON.stringify(data),
  //             credentials: 'include'
  //
  //         };
  //
  //         fetch(endpoint, lookupOptions)
  //         .then(function(response){
  //             return response.json()
  //         }).then(function(responseData){
  //             console.log(responseData);
  //
  //         })
  //     }
  //
  // }
  //   handleSubmit(event){
  //       event.preventDefault();
  //       let data = this.state;
  //       this.createPost(data);
  //   }
  //   handleInputChange(event){
  //       event.preventDefault();
  //       let key = event.target.name;
  //       let value = event.target.value;
  //
  //       this.setState({
  //           [key]: value
  //       })
  //   }
  //   componentDidMount() {
  //       this.setState({
  //           "company": null,
  //           "title": "",
  //           "start_date": null,
  //           "end_date": null,
  //           "estimated_design": null,
  //           "actual_design": null,
  //           "estimated_development": null,
  //           "actual_development": null,
  //           "estimated_testing": null,
  //           "actual_testing": null,
  //           "tags": [],
  //
  //       })
  //   }
    async componentDidMount() {
    try {
      const result = await fetch('http://127.0.0.1:8000/api/company/create/');
      const companies = await result.json();
      console.log(companies);
      this.setState({
        companies
      });
    } catch (e) {
      console.log(e);
    }
  }

    render() {

        return (

            <form onSubmit={this.handleSubmit}>
                <div className='form-group'>
                    <label>Project company</label>
                {/*    <input type='text' id='company' name='company'*/}
                {/*           className='form-control' placeholder='company'  onChange={this.changeHandler} required='required'/>*/}
                {/*</div>*/}
                    <select name="company" className="select form-control"
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
                <button className='bnt btn-danger'>Save</button>

            </form>
        )
    }
}

export default ProjectCreate;