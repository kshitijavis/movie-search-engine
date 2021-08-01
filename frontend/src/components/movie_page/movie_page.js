import React from 'react';
import { withRouter } from 'react-router-dom';
import axios from 'axios'
import { Button, ListGroup, Row, Col } from 'react-bootstrap'
import '../../styles/movie_page.css'
import '../../styles/general.css'
import MovieImage from './movie_image';

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
          key={idx}
          id={`${keyword}_${idx}`}
        >
          {keyword}
        </ListGroup.Item>
      ))
    )
  }

  render() {
    return (
      <div className='body'>
        <h1 id='movie_title'>{this.state.title}</h1>
        <h2>{this.state.tagline}</h2>
        <br></br>

        <p id='movie_vote_average'>Average Rating: {this.state.vote_average}</p>
        <h4>Overview</h4>
        <div className='overview rectangle-border'>
          <p>{this.state.overview}</p>
        </div>
        <br></br>

        <Row>
          <Col>
            <h4>Keywords</h4>
            <ListGroup className='keywords'>{this.renderKeywords()}</ListGroup>
            <Button className='back-button' href="/" id='back_to_search'>Back To Search</Button>
          </Col>
          <Col>
            <MovieImage
              movie_id={this.props.match.params.id}
            />
          </Col>
        </Row>
      </div>
    )
  }
}

export default withRouter(MoviePage);