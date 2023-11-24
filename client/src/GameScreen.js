import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './GameScreen.css'; 

function GameScreen() {
  const [userData, setUserData] = useState({ username: '', team: '', id: '' });
  const [spawnCoords, setSpawnCoords] = useState({ row: 1, column: 1 });
  const [spawnSetSuccess, setSpawnSetSuccess] = useState(false);
  const [gameState, setGameState] = useState(null);  

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

  const handleStartSimulation = () => {
    //console.log(gameState)
    navigate(`/game/simulation`, { state: { gameState } });
  };

// En tu componente GameScreen

return (
  <div className="game-screen-container">
    <h2 className="game-screen-header">Welcome, {userData.username}!</h2>
    <p className="game-screen-info">You are part of the {userData.team} team.</p>
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
      {spawnSetSuccess ? (
        <div className="spawn-success-container">
          <p className="spawn-success-message">Spawn was set successfully.</p>
          <button className="start-simulation-button" onClick={handleStartSimulation}>Start Simulation</button>
        </div>
      ) : null}
    </div>
  </div>
);

}

export default GameScreen;