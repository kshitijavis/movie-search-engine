import React from 'react';
import {Button, Form, Row, Col, ListGroup, FormGroup, FormText} from 'react-bootstrap';
import '../../styles/search_page.css'
import '../../styles/general.css'

/**
 * A Form Component that allows users to movie search criteria
 * Allows users to add criteria for title, keywords, and vote_average
 * Title is added through a simple text input field. Vote average is 
 * added by specifying a lower and upper bound. Keywords are entered
 * as a dynamic list of text inputs. Users can search for any number of 
 * keywords, and can add keywords to their search query through an 
 * "Add Keyword" button.
 */
class SearchForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      // Stores the four search criteria
      title: '',
      keywords: [''],
      vote_lower_bound: '',
      vote_upper_bound: '',
    };
  }

  handleChange = (event) => {
    if (event.target.name === 'keyword') {
      // Handle change to keyword input text fields
      let newKeywords = this.state.keywords.slice()
      newKeywords[event.target.dataset.id] = event.target.value;
      this.setState({ keywords: newKeywords})
    } else {
      // Handle change to all other fields by dynamically gathering state name from event
      this.setState({
        [event.target.name]: event.target.value
      })
    }
  }

  handleSubmit = (event) => {
    event.preventDefault();
    this.props.onSubmit(
      this.state.title, 
      this.state.keywords, 
      this.state.vote_lower_bound, 
      this.state.vote_upper_bound
    )
  }

  addKeyword = (event) => {
    event.preventDefault(); // Keep from calling handleSubmit
    this.setState((prevState) => ({
      // Add empty keyword
      keywords: [...prevState.keywords, ''],
    }));
  }

  deleteKeyword = (event) => {
    event.preventDefault(); // Keep from calling handleSubmit
    let newKeywords = this.state.keywords.slice()
    newKeywords.splice(event.target.dataset.id, 1)
    this.setState({ keywords: newKeywords})
  }

  renderKeywordInput = () => {
    // Generates dynamic list of inputs using keyword state
    const keywords = this.state.keywords;

    return keywords.map((keyword, idx) => (
      <ListGroup.Item 
        className="keyword-group"
        key={idx}>
        <Row>
          <Col>
            <Form.Control
              type='text'
              name='keyword'
              data-id={idx}
              className="keyword-input"
              value={this.state.keywords[idx]}
              placeholder={`Enter Keyword ${idx+1}`}
              onChange={this.handleChange}
            />
          </Col>
          <Col>
            <Button
              id={`delete_keyword${idx}`}
              data-id={idx}
              onClick={this.deleteKeyword}
              variant='danger'
            >
              Delete Keyword
            </Button>
          </Col>
        </Row>
      </ListGroup.Item>
    ))
  }

  render() {
    return (
      <Form 
       className='search-form rounded-border'
       onSubmit={this.handleSubmit}>
        <Form.Group controlId="form_title">
          <Form.Label>Title</Form.Label>
            <Form.Control 
              name='title' 
              type='text' 
              placeholder='Enter title'
              value={this.state.title} 
              onChange={this.handleChange}/>
        </Form.Group>
        <Row id='vote_bounds'>
        <Form.Label>Ratings</Form.Label>
          <Col>
            <Form.Group controlId='form_vote_lower_bound'>
                <Form.Control 
                  name='vote_lower_bound' 
                  type='number'
                  placeholder='Min'
                  value={this.state.vote_lower_bound} 
                  onChange={this.handleChange}/>
                <FormText>Values between 0-10</FormText>
            </Form.Group>
          </Col>
          <Col xs={1}>
            <p className='ratings-middle-text'>to</p>
          </Col>
          <Col>
            <Form.Group controlId='form_vote_upper_bound'>
                <Form.Control 
                  name='vote_upper_bound' 
                  type='number'
                  placeholder='Max'
                  value={this.state.vote_upper_bound} 
                  onChange={this.handleChange}/>
                <FormText>Values between 0-10</FormText>
            </Form.Group>
          </Col>
        </Row>

        <ListGroup variant="flush">
        <Form.Label className='keyword-group-title'>Keywords</Form.Label>
          {this.renderKeywordInput()}
        </ListGroup>
        <Button variant='secondary' onClick={this.addKeyword}>Add Keyword</Button>
        <Button 
         className='pull-right'
         type='primary' 
         onSubmit={this.handleSubmit}
        >
          Search
        </Button>
      </Form>
    );
  }
}

export default SearchForm