import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

class Tag extends Component {
  constructor(props) {
    super(props);
    this.state = {
      tags: []
    };

  }

  async componentDidMount() {
    try {
      const result = await fetch('http://127.0.0.1:8000/api/tag/create/');
      const tags = await result.json();
      this.setState({
        tags
      });
    } catch (e) {
      console.log(e);
    }
  }

  render() {
    return (
        // <div className="table-responsive">
        //    {this.state.tags.map(item => (
        //
        //        <a href={`tag/${item.id}/delete`}><h1>{item.title}</h1>
        //          <a href={`tag/${item.id}/update`}>edit</a>
        //        </a>
        //
        //    ))}
        //
        //  </div>
         <div className="table-responsive" style={{width: '53%'}}>
          <table className="table table-bordered table-striped table-hover">
            <thead>
            <tr>
              <th width="40%">Tags</th>
              <th width="10%">Tags edit</th>
              <th width="10%">Tags delete</th>

            </tr>
            </thead>
            <tbody>
        {this.state.tags.map(item => (
            <tr>
              <td>{ item.title }</td>
              <td><a href={`tag/${item.id}/update`}>edit</a></td>
              <td><a href={`tag/${item.id}/delete`}>delete</a></td>
            </tr>
        ))}
         </tbody>
        </table>
       </div>
    );
  }
}

export default Tag;
