import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

class Dashboard extends Component {
  state = {
    projects: []
  };

  async componentDidMount() {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/dashboard/');
      const projects = await res.json();
      this.setState({
        projects
      });
    } catch (e) {
      console.log(e);
    }
  }

  render() {
    return (
        <div className="table-responsive" style={{width: '53%'}}>
          <table className="table table-bordered table-striped table-hover">
            <thead>
            <tr>
              <th width="40%">Project</th>
              <th width="30%">Company</th>
              <th width="15%">Estimated</th>
              <th width="15%">Actual</th>
            </tr>
            </thead>
            <tbody>
        {this.state.projects.map(item => (
            <tr>
              <td>{ item.title }</td>
              <td>{ item.company }</td>
              <td>{ item.estimated }</td>
              <td>{ item.actual }</td>
            </tr>
        ))}
         </tbody>
        </table>
            <a href="/project/create">
                <input type="button" value="Project create"/>
            </a>
          </div>
    );
  }
}

export default Dashboard;
