import logo from './logo.svg';
import './App.css';
import React from 'react';
import SearchForm from './components/search_form'

class App extends React.Component {
  render() {
    return (
      <div>
        <div>
          <div>
            <h1>Hello World</h1>
            <SearchForm></SearchForm>
          </div>
        </div>
      </div>
    ); 
  }
}

export default App;
