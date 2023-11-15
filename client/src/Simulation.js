import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

function Simulation() {
  const location = useLocation();
  const [gameState, setGameState] = useState(location.state && location.state.gameState);

  useEffect(() => {
    const fetchAndUpdateGameState = async () => {
      try {
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
        }
      } catch (error) {
        console.error('Error updating game state:', error);
      }
    };

    // Interval to call fetchAndUpdateGameState each 2 seconds
    const intervalId = setInterval(fetchAndUpdateGameState, 2000);
    return () => clearInterval(intervalId);
  }, [gameState?.id]); 

  return (
    <div>
      <h2>Simulation</h2>
      {gameState && (
        <div>
          <h3>Game State:</h3>
          <pre>{JSON.stringify(gameState, null, 2)}</pre>
          {gameState.board && (
            <div>
              <h3>Formatted Board:</h3>
              <pre>{JSON.stringify(JSON.parse(gameState.board), null, 2)}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Simulation;
