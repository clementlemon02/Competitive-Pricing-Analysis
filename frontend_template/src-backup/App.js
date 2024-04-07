import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

const Page1 = () => {
  return (
    <div>
      <h2>Page 1</h2>
      <p>This is an empty page.</p>
    </div>
  );
};

const Page2 = () => {
  return (
    <div>
      <h2>Page 2</h2>
      <p>This is another empty page.</p>
    </div>
  );
};

const App = () => {
  return (
    <Router>
      <div>
        <h1>Simple React App</h1>
        <Routes>
          <Route exact path="/" component={Page1} />
          <Route exact path="/page2" component={Page2} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
