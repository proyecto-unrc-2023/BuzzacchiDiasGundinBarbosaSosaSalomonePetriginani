import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import App from './App';
import GameScreen from './GameScreen';

function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<App />} exact />
        <Route path="/game" element={<GameScreen />} />
      </Routes>
    </Router>
  );
}

export default AppRouter;
