import React, { useState, useEffect } from 'react';

import { useParams } from 'react-router-dom';

function GameScreen() {
  const [userData, setUserData] = useState({ username: '', team: '', id: '' });
  const [spawnCoords, setSpawnCoords] = useState({ row: 1, column: 1 }); 
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

      if (!response.ok) {
        throw new Error('Error creating new game');
      }

      const responseData = await response.json();
      console.log(responseData); 

    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h2>Welcome, {userData.username}!</h2>
      <p>You are part of the {userData.team} team.</p>
      <div>
        <p>Enter Spawn Coordinates (1-13):</p>
        <label>Row:</label>
        <input
          type="number"
          value={spawnCoords.row}
          onChange={(e) => setSpawnCoords({ ...spawnCoords, row: parseInt(e.target.value) || 1 })}
        />
        <label>Column:</label>
        <input
          type="number"
          value={spawnCoords.column}
          onChange={(e) => setSpawnCoords({ ...spawnCoords, column: parseInt(e.target.value) || 1 })}
        />
        <button onClick={handleSpawnSubmit}>Set Spawn</button>
      </div>
    </div>
  );
}

export default GameScreen;