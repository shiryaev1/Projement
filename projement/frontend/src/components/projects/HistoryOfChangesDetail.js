import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

class HistoryOfChangesDetail extends Component {
    constructor(props) {
        super(props);
        this.state = {
            history: [],
            historyDetail: []
        };
    }

  async componentDidMount() {
    try {
      let changeId = this.props.match.params.id;
      const res = await fetch(`http://127.0.0.1:8000/api/project/${changeId}/history/`);
      const historyDetail = await res.json();
      this.setState({
        historyDetail
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
                    <th width="12%">Change delta actual design</th>
                    <th width="12%">Resulting actual design</th>
                    <th width="12%">Change delta actual development</th>
                    <th width="12%">Resulting actual development</th>
                    <th width="12%">Change delta actual testing</th>
                    <th width="12%">Resulting actual testing</th>
                    <th width="12%">Initial data</th>


                </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{this.state.historyDetail.change_delta_actual_design}</td>
                        <td>{this.state.historyDetail.resulting_actual_design}</td>
                        <td>{this.state.historyDetail.change_delta_actual_development}</td>
                        <td>{this.state.historyDetail.resulting_actual_development}</td>
                        <td>{this.state.historyDetail.change_delta_actual_testing}</td>
                        <td>{this.state.historyDetail.resulting_actual_testing}</td>
                        <td><a href={`/project/${this.state.historyDetail.project_id}/initial-data`}>view changes</a></td>


                    </tr>

                </tbody>
            </table>

        </div>
    );
  }
}

export default HistoryOfChangesDetail;
