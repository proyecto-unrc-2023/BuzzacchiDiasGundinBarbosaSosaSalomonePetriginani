import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import App from './App';
import GameScreen from './GameScreen';
import Simulation from './Simulation'

function AppRouter() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<App />} exact />
        <Route path="/game/:gameId" element={<GameScreen />} />
        <Route
          path="/game/simulation"
          element={<Simulation />}  
        />
      </Routes>
    </Router>
  );
}

export default AppRouter;
