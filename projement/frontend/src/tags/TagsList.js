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
        <div className="table-responsive">
           {this.state.tags.map(item => (
               <h1>{item.title}</h1>
           ))}

         </div>
    );
  }
}

export default Tag;
