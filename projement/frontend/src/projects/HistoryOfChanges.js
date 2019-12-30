import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

class HistoryOfChanges extends Component {
  state = {
    history: []
  };

  async componentDidMount() {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/project/history/');
      const history = await res.json();
      this.setState({
        history
      });
    } catch (e) {
      console.log(e);
    }
  }

  render() {

    return (
        <div className="table-responsive">
            <table className="table table-bordered table-striped table-hover">
                <thead>
                <tr>
                    <th width="12%">Project</th>
                    <th width="12%">Owner</th>
                    <th width="12%">Change time</th>
                    <th width="12%">Changes</th>
                </tr>
                </thead>
                <tbody>
                {this.state.history.map(item => (
                    <tr>
                        <td>
                            <a href="">{item.project}</a>
                        </td>
                        <td>{item.owner}</td>
                        <td>{item.change_time}</td>
                        {/*{for item of this.}*/}
                        <td><a href={`/project/${item.id}/history`}>view changes</a></td>
                    </tr>
                 ))}
                </tbody>
            </table>

        </div>
    );
  }
}

export default HistoryOfChanges;
