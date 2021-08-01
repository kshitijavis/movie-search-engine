import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import SearchPage from './components/search_page/search_page';
import MoviePage from './components/movie_page/movie_page';

class App extends React.Component {
  render() {
    return (
      <div className="App">
        <Router>
          <Switch>
            <Route path="/movies/:id" exact component={() => <MoviePage />} />
            <Route path="/" exact component={() => <SearchPage />} />
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;
