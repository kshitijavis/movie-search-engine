import React from 'react';
import axios from 'axios';

class MovieImage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      image_url: '',
    }
  }

  componentDidMount() {
    this.fetchImage();
  }

  fetchImage = () => {
    console.log('here')
    const movie_id = this.props.movie_id;
    axios
      .get(`/api/searchengine/movies/image/${movie_id}`)
      .then((res) => {
        const results = res.data.items;
        if (results !== null && results.length > 0) {
          this.setState({ image_url: results[0].link })
        }
      })
  }

  render() {
    return (
      <div>
        <img
          src={this.state.image_url}
          alt={`Movie`}
        />
      </div>
    )
  }
}

export default MovieImage;