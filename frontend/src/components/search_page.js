import React from 'react'
import SearchForm from './search_form'
import axios from 'axios'
import SearchResult from './search_result';

class SearchPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      search_results: []
    }
  }

  componentDidMount() {
    this.searchMovies('', '', '', '');
  }

  searchMovies = (title, keywords, vote_lower_bound, vote_upper_bound) => {
    let params = {}
    // Empty inputs shouldn't be added to query string
    if (title !== '') params.title = title
    if (keywords !== []) params.keywords = keywords
    if (vote_lower_bound !== '') params.vote_lower_bound = vote_lower_bound
    if (vote_upper_bound !== '') params.vote_lower_bound = vote_upper_bound

    axios
      .get('http://localhost:8000/api/searchengine/search/', { params: params })
      // .then((res) => console.log([res.data.results]))
      .then((res) => this.setState({ search_results: res.data.results }))
      .catch((err) => console.log(err))
  }

  renderSearchResults = () => {
    return this.state.search_results.map((result) => (
      <li
        key={result.id}
      >
        <SearchResult
          result={result}
        />
      </li>
    ))
  }

  render() {
    return (
      <div>
        <h1>Movie Search Engine</h1>
        <SearchForm
          onSubmit={this.searchMovies}
        />
        <ul>
          {this.renderSearchResults()}
        </ul>
      </div>
    );
  }
}

export default SearchPage