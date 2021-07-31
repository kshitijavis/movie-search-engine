import './App.css';
import React from 'react';
import SearchPage from './components/search_page';

class App extends React.Component {
  render() {
    return (
      <div>
        <div>
          <div>
            <h1>Hello World</h1>
            <SearchPage id='search_page'></SearchPage>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
