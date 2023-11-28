import { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';

function RepeatSimulation() {
  const location = useLocation();
  const [gameState, setGameState] = useState(null);
  const [simulationId, setSimulationId] = useState(location.state && location.state.simulationId);
  const [lastTimestamp, setLastTimestamp] = useState(null);  
  const [winnerTeam, setWinnerTeam] = useState(null);

  const shouldContinueRef = useRef(true);

  useEffect(() => {
    let intervalId;

    const fetchNextGameState = async () => {
      try {
        const response = await fetch(`/simulation/simulation_replay`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            simulation_id: simulationId,
            last_timestamp: lastTimestamp,  
          }),
        });
    
        if (response.status === 200) {
          const responseData = await response.json();
          console.log('Returned game state:', responseData.game_state);
          console.log('Returned last timestamp:', responseData.last_timestamp);
          setGameState(responseData.game_state);
          setLastTimestamp(responseData.last_timestamp);
    
          if (responseData.game_state.mode === 'FINISHED') {
            const winnerResponse = await fetch(`/simulation/get_winner_team_by_id/${responseData.game_state.id}`);
            if (winnerResponse.status === 200) {
              const winnerTeam = await winnerResponse.text();
              setWinnerTeam(winnerTeam);
              console.log(winnerTeam);
              shouldContinueRef.current = false; // Stop the simulation
            }
          }
        } else {
          clearInterval(intervalId);  
        }
      } catch (error) {
        console.error('Error fetching game state:', error);
      }
    };

    intervalId = setInterval(() => {
      if (shouldContinueRef.current) {
        fetchNextGameState();
      } else {
        clearInterval(intervalId);
      }
    }, 100);

    return () => {
      clearInterval(intervalId);
    };
  }, [simulationId, lastTimestamp]);

}

export default RepeatSimulation;