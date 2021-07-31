import React from 'react';

class SearchResult extends React.Component {
  constructor(props) {
    super(props);
  }

  renderMatchSummary = () => {
    return this.props.result.match_summary.map((summary, idx) => (
      <li
        key={idx}
      >
        <div>
          {summary.type}: {summary.contents}
        </div>
      </li>
    ))
  }

  render() {
    return (
      <div>
        <h4>{this.props.result.title}</h4>
        <p>Match score: {this.props.result.match_score}</p>
        <ul>{this.renderMatchSummary()}</ul>
      </div>
    )
  }
}

export default SearchResult