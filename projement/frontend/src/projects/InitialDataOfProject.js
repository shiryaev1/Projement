import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

class InitialDataOfProject extends Component {
    constructor(props) {
        super(props);
        this.state = {
            initialData: []
        };
    }

  async componentDidMount() {
    try {
      let projectId = this.props.match.params.id;
      const res = await fetch(`http://127.0.0.1:8000/api/project/${projectId}/initial-data/`);
      const initialData = await res.json();
      this.setState({
        initialData
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
                    <th width="12%">Initial actual design</th>
                    <th width="12%">Initial actual development</th>
                    <th width="12%">Initial actual testing:</th>

                </tr>
                </thead>
                <tbody>
                    {this.state.initialData.map(item => (
                    <tr>

                        <td>{item.project}</td>
                        <td>{item.initial_actual_design}</td>
                        <td>{item.initial_actual_development}</td>
                        <td>{item.initial_actual_testing}</td>

                        {/*<td>-</td>*/}
                        {/*<td>-</td>*/}
                        {/*<td>-</td>*/}

                    </tr>
                    ))}
                </tbody>
            </table>

        </div>
    );
  }
}

export default InitialDataOfProject;