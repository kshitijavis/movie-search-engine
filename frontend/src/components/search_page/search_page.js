import React from 'react'
import SearchForm from './search_form'
import axios from 'axios'
import SearchResult from './search_result'
import PageNavigator from '../page_navigator'
import {ListGroup, ListGroupItem} from 'react-bootstrap'

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
    let params = new URLSearchParams();
    // Empty inputs shouldn't be added to query string
    if (title !== '') params.append("title", title);
    if (vote_lower_bound !== '') params.append("vote_lower_bound", vote_lower_bound)
    if (vote_upper_bound !== '') params.append("vote_upper_bound", vote_upper_bound)
    keywords.forEach(keyword => params.append("keyword", keyword))

    // Send GET request and update state based on request
    axios
      .get('/api/searchengine/search/', { params: params })
      .then((res) => {console.log(res); return this.setStateBySearchResponse(res.data)})
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
      <ListGroupItem
        key={`result_movie_${result.id}`}
      >
        <SearchResult
          result={result}
        />
      </ListGroupItem>
    ))
  }

  render() {
    return (
      <div>
        <h1>Movie Search Engine</h1>
        <SearchForm
          onSubmit={this.searchAndUpdateMovies}
        />
        <ListGroup className='search-result-group'>
          {this.renderSearchResults()}
        </ListGroup>
        <PageNavigator
          className='page-navigator'
          nextPageUrl={this.state.nextPageUrl}
          prevPageUrl={this.state.prevPageUrl}
          onChangePage={this.searchAndUpdateMoviesUrl}
        />
      </div>
    );
  }
}

export default SearchPage