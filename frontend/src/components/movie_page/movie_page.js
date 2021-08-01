import React from 'react';
import { withRouter } from 'react-router-dom';
import axios from 'axios'
import { Button, ListGroup } from 'react-bootstrap'

class MoviePage extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      title: '',
      tagline: '',
      overview: '',
      vote_average: '',
      keywords: [],
    }
  }

  componentDidMount() {
    const id = this.props.match.params.id;
    this.fetchData(id)
  }

  fetchData = (id) => {
    axios
    .get(`/api/searchengine/movies/${id}`)
    .then((res) => this.setStateBySearchResponse(res.data))
    .catch((err) => console.log(err))
  }

  setStateBySearchResponse = (response) => {
    this.setState(response)
  }

  renderKeywords = () => {
    return (
      this.state.keywords.map((keyword, idx) => (
        <ListGroup.Item 
          id={`${keyword}_${idx}`}
        >
          {keyword}
        </ListGroup.Item>
      ))
    )
  }

  render() {
    return (
      <div>
        <h1 id='movie_title'>{this.state.title}</h1>
        <h2 id='movie_tagline'>{this.state.tagline}</h2>
        <p id='movie_vote_average'>Average rating: {this.state.vote_average}</p>
        <ListGroup>{this.renderKeywords()}</ListGroup>
        <Button href="/" id='back_to_search'>Back To Search</Button>
      </div>
    )
  }
}

export default withRouter(MoviePage);