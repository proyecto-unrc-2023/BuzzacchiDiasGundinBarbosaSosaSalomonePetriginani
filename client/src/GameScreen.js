
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './GameScreen.css'; 

function GameScreen() {
  const [userData, setUserData] = useState({ username: '', team: '', id: '' });
  const [spawnCoords, setSpawnCoords] = useState({ row: 1, column: 1 });
  const [spawnSetSuccess, setSpawnSetSuccess] = useState(false);
  const [gameState, setGameState] = useState(null);  
  const [simulationHistory, setSimulationHistory] = useState([]);
  const [selectedSimulationId, setSelectedSimulationId] = useState(null);
  const [showSimulationHistory, setShowSimulationHistory] = useState(false);

  const navigate = useNavigate();
  const { gameId } = useParams();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/simulation/get_username_and_team', {
          method: 'GET',
          credentials: 'include',
        });

        if (!response.ok) {
          throw new Error('Error loading data');
        }

        const data = await response.json();
        setUserData(data);
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchData();
  }, []);

  const handleSpawnSubmit = async () => {
    if (!(0 <= spawnCoords.row && spawnCoords.row <= 13) || !(0 <= spawnCoords.column && spawnCoords.column <= 13)) {
      alert('Row and column must be integers between 0 and 14.');
      return;
    }

    try {
      const response = await fetch('/simulation/new_game', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          row: spawnCoords.row,
          column: spawnCoords.column,
          game_state_id: gameId,
        }),
      });

      if (response.status === 200) {
        const responseData = await response.json();
        // Almacenar el game state en el estado
        setGameState(responseData.game_state);
        setSpawnSetSuccess(true);
      } else {
        setSpawnSetSuccess(false);
      }

    } catch (error) {
      console.error('Error:', error);
    }
  };

  const toggleSimulationHistory = async () => {
    setShowSimulationHistory(!showSimulationHistory);
    
    if (!showSimulationHistory) {
      await fetchSimulationHistory();
    }
  };

  const fetchSimulationHistory = async () => {
    try {
      const response = await fetch('/simulation/simulation_history', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: userData.username,
        }),
        credentials: 'include',
      });
  
      if (!response.ok) {
        throw new Error('Error loading data');
      }
  
      const data = await response.json();
      setSimulationHistory(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleStartSimulation = () => {
    navigate(`/game/simulation`, { state: { gameState } });
  };

  const handleRepeatSimulation = (simulationId) => {
    navigate(`/game/repeat_simulation`, { state: { simulationId } });
  };

  return (
    <div className="game-screen-container">
      <h2 className="game-screen-header">Welcome, {userData.username}!</h2>
      <p className="game-screen-info">You are part of the {userData.team} team.</p>
      {!spawnSetSuccess && (
        <div className="spawn-coordinates-container">
          <p>Enter Spawn Coordinates (1-13):</p>
          <label className="spawn-coordinates-label">Row:</label>
          <input
            className="spawn-coordinates-input"
            type="number"
            value={spawnCoords.row}
            onChange={(e) => setSpawnCoords({ ...spawnCoords, row: parseInt(e.target.value) || 1 })}
          />
          <label className="spawn-coordinates-label">Column:</label>
          <input
            className="spawn-coordinates-input"
            type="number"
            value={spawnCoords.column}
            onChange={(e) => setSpawnCoords({ ...spawnCoords, column: parseInt(e.target.value) || 1 })}
          />
          <button className="spawn-coordinates-button" onClick={handleSpawnSubmit}>Set Spawn</button>
        </div>
      )}
      {spawnSetSuccess && (
        <div className="spawn-success-container">
          <p className="spawn-success-message">Spawn was set successfully.</p>
          <button className="start-simulation-button" onClick={handleStartSimulation}>Start Simulation</button>
        </div>
      )}
      <p>Would you like to see a replay of a previous simulation?</p>
      <button className="spawn-coordinates-button" onClick={toggleSimulationHistory}>
        {showSimulationHistory ? 'Hide Simulation History' : 'See Simulation History'}
      </button>
      {showSimulationHistory && simulationHistory.length > 0 && (
        <>
          <ul style={{ maxHeight: '300px', overflowY: 'scroll' }}>
            {simulationHistory.map((simulation) => (
              <li key={simulation.simulation_id} className="simulation-list-item">
                <div 
                  style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }} 
                  onClick={() => setSelectedSimulationId(simulation.simulation_id)}
                >
                  <input
                    type="radio"
                    id={simulation.simulation_id}
                    name="simulation"
                    value={simulation.simulation_id}
                    checked={selectedSimulationId === simulation.simulation_id}
                    readOnly
                  />
                  <div>
                    <strong>ID:</strong> {simulation.simulation_id.split('-')[0]}
                    <br />
                    <strong>Start of the simulation:</strong>{' '}
                    {new Date(simulation.start_time).toLocaleString()}
                    <br />
                    <strong>Team:</strong> {simulation.team}
                  </div>
                </div>
                <hr />
              </li>
            ))}
          </ul>
          <button
            className="spawn-coordinates-button"
            onClick={() => handleRepeatSimulation(selectedSimulationId)}
          >
            Repeat Simulation
          </button>
        </>
      )}
    </div>
  );
}

export default GameScreen;
