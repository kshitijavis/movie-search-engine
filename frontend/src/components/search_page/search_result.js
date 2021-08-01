import React from 'react';
import {Table} from 'react-bootstrap'

class SearchResult extends React.Component {
  constructor(props) {
    super(props);
  }

  renderMatchSummary = () => {
    return this.props.result.match_summary.map((summary, idx) => (
      <thead>
        <th className='match-table-col-1'>{summary.type}</th>
        <th>{summary.contents}</th>
      </thead>
    ))
  }

  render() {
    return (
      <div className='search-result'>
        <h4><a href={`movies\\${this.props.result.id}`}>
          {this.props.result.title}
        </a></h4>
        <p className='match-summary'>Match Summary</p>
        <Table striped bordered hover>
          {this.renderMatchSummary()}
        </Table>
        <p className='match-score'>Matches: {this.props.result.match_score}</p>
      </div>
    )
  }
}

export default SearchResult