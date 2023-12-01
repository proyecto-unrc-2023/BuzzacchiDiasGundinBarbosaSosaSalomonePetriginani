import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import App from './App';
import GameScreen from './GameScreen';
import Simulation from './Simulation'
import RepeatSimulation from './RepeatSimulation'
import Finished from './Finished';
import FinishSimulation from './FinishSimulation'

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
        <Route
          path="/game/repeat_simulation"
          element={<RepeatSimulation />}  
        />
        <Route
          path="/game/finish_simulation"
          element={<FinishSimulation />}  
        />
        <Route 
          path="/game/simulation/finished"
          element={<Finished />}
        />
      </Routes>
    </Router>
  );
}

export default AppRouter;
