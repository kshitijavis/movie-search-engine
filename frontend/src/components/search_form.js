import React from 'react';

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
      vote_lower_bound: 0,
      vote_upper_bound: 10,
    };
  }

  handleChange = (event) => {
    if (event.target.className === 'keyword input') {
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
    console.log(this.state) // Will be used to send API call
  }

  addKeyword = (event) => {
    event.preventDefault(); // Keep from calling handleSubmit
    this.setState((prevState) => ({
      // Add empty keyword
      keywords: [...prevState.keywords, ''],
    }));
  }

  renderKeywordInput = () => {
    // Generates dynamic list of inputs using keyword state
    const keywords = this.state.keywords;

    return keywords.map((keyword, idx) => (
      <li key={idx}>
        <label>
          Keyword:
          <input
            type='text'
            name='keyword'
            data-id={idx}
            className="keyword input"
            onChange={this.handleChange}
          />
        </label>
      </li>
    ))
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Title: 
          <input 
            name='title' 
            type='text' 
            value={this.state.title} 
            onChange={this.handleChange}/>
        </label>
        <br />
        <label>
          Vote average lower bound:
          <input 
            name='vote_lower_bound' 
            type='number' 
            value={this.state.vote_lower_bound} 
            onChange={this.handleChange}/>
        </label>
        <label>
          Vote average upper bound:
          <input 
            name='vote_upper_bound'
            type='number' 
            value={this.state.vote_upper_bound} 
            onChange={this.handleChange}/>
        </label>
        <br />
        <ul>
          {this.renderKeywordInput()}
        </ul>
        <button onClick={this.addKeyword}>Add Keyword</button>
        <input type='submit' onSubmit={this.handleSubmit}/>
      </form>
    );
  }
}

export default SearchForm