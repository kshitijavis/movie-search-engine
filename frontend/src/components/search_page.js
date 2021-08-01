import React from 'react'
import SearchForm from './search_form'
import axios from 'axios'
import SearchResult from './search_result'
import PageNavigator from './page_navigator'

class SearchPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      searchResults: [],
      nextPageUrl: null,
      prevPageUrl: null,
    }
  }

  searchAndUpdateMovies = (title, keywords, vote_lower_bound, vote_upper_bound) => {
    let params = {}
    // Empty inputs shouldn't be added to query string
    if (title !== '') params.title = title
    if (keywords !== []) params.keywords = keywords
    if (vote_lower_bound !== '') params.vote_lower_bound = vote_lower_bound
    if (vote_upper_bound !== '') params.vote_lower_bound = vote_upper_bound

    // Send GET request and update state based on request
    axios
      .get('http://localhost:8000/api/searchengine/search/', { params: params })
      .then((res) => this.setStateBySearchResponse(res.data))
      .catch((err) => console.log(err))
  }

  // Sends GET request by URL. Useful for pagination by links
  searchAndUpdateMoviesUrl = (url) => {
    axios
      .get(url)
      .then((res) => this.setState(this.setStateBySearchResponse(res.data)))
  }

  setStateBySearchResponse = (response) => {
    this.setState({
      searchResults: response.results,
      nextPageUrl: response.next,
      prevPageUrl: response.previous,
    })
  }

  renderSearchResults = () => {
    return this.state.searchResults.map((result) => (
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
          onSubmit={this.searchAndUpdateMovies}
        />
        <ul>
          {this.renderSearchResults()}
        </ul>
        <PageNavigator
          nextPageUrl={this.state.nextPageUrl}
          prevPageUrl={this.state.prevPageUrl}
          onChangePage={this.searchAndUpdateMoviesUrl}
        />
      </div>
    );
  }
}

export default SearchPage