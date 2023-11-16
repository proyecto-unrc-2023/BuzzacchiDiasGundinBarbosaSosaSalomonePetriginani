import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

function Simulation() {
  const location = useLocation();
  const [gameState, setGameState] = useState(location.state && location.state.gameState);
  const [winnerTeam, setWinnerTeam] = useState(null);
  const [lastSpawns, setLastSpawns] = useState(null);

  useEffect(() => {
    const fetchAndUpdateGameState = async () => {
      try {
        let updatedSpawns = {};

        if (gameState?.mode === 'FINISHED') {
          // console.log(gameState?.mode);
          clearInterval(intervalId); 
          const winnerResponse = await fetch(`/simulation/get_winner_team`);
          if (winnerResponse.status === 200) {
            const winnerTeam = await winnerResponse.text();
            setWinnerTeam(winnerTeam);
          }
        } else {
          const response = await fetch(`/simulation/update_state`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              id: gameState?.id,
            }),
          });
  
          if (response.status === 200) {
            const responseData = await response.json();
            setGameState(responseData.updated_game_state);
            updatedSpawns = {
              iceSpawn: responseData.updated_game_state.ice_spawn,
              fireSpawn: responseData.updated_game_state.fire_spawn,
            };
          }
        }
        console.log(updatedSpawns)
        setLastSpawns(updatedSpawns);

      } catch (error) {
        console.error('Error updating game state:', error);
      }
    };
  
    // Interval to call fetchAndUpdateGameState each 2 seconds
    const intervalId = setInterval(fetchAndUpdateGameState, 1000);
    return () => clearInterval(intervalId);
  }, [gameState?.id, gameState?.mode]);

  return (
    <div>
      <h2>Simulation</h2>
      {winnerTeam ? (
        <div>
          <h3>Winner Team:</h3>
          <p>{winnerTeam}</p>
        </div>
      ) : (
        gameState && (
          <div>
            <h3>Game State:</h3>
            <pre>{JSON.stringify(gameState, null, 2)}</pre>
            {gameState.board && (
              <div>
                <h3>Formatted Board:</h3>
                <pre>{JSON.stringify(JSON.parse(gameState.board), null, 2)}</pre>
              </div>
            )}

            {lastSpawns && (
              <div>
                <h3>Last Updated Spawns:</h3>
                <pre>{JSON.stringify(lastSpawns, null, 2)}</pre>
              </div>
            )}
          </div>
        )
      )}
    </div>
  );
}

export default Simulation;
