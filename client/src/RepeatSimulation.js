import { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Board from './Board';
import Cell from './Cell';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

function RepeatSimulation() {
  const location = useLocation();
  const [gameState, setGameState] = useState(null);
  const [simulationId, setSimulationId] = useState(location.state && location.state.simulationId);
  const [lastTimestamp, setLastTimestamp] = useState(null);  
  const [winnerTeam, setWinnerTeam] = useState(null);
  const navigate = useNavigate();
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
            navigate('/game/simulation/finished', { state: { gameState } });
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
    }, 1000);


    return () => {
      clearInterval(intervalId);
    };
  }, [simulationId, lastTimestamp]);

  
    
  const ice_life = (spawn) => {
    const SpawnObj = JSON.parse(spawn);
    const ice_spawn = SpawnObj.life;
    console.log(ice_spawn)
    return ice_spawn;
  };

  const fire_life = (spawn) => {
    const SpawnObj = JSON.parse(spawn);
    const fire_spawn = SpawnObj.life;
    console.log(fire_spawn)
    return fire_spawn;
  };

  return (
    <div className="simulation-container">
      <div className="progress-container">
        {gameState && gameState.ice_spawn && (
          <div className="progress-bar">
            <p className="progress-text">
              IceSpawn Life 
            </p>
            <div className="progress-background">
              <CircularProgressbar
                value={ice_life(gameState.ice_spawn)}
                text={`${ice_life(gameState.ice_spawn)}`}
                maxValue={300}
                styles={buildStyles({
                  pathColor: "#000080",
                  textColor: "#000",
                  trailColor: "#f3f3f3",
                  backgroundColor: 'transparent',
                  textSize: '25px'
                })}
              />
            </div>
          </div>
        )}
      </div>
  
      <div className="board-container">
        {gameState && <Board boardData={JSON.parse(gameState.board)} />}
      </div>
  
      <div className="progress-container">
        {gameState && gameState.fire_spawn && (
          <div className="progress-bar">
            <p className="progress-text">
              FireSpawn Life
            </p>
            <div className="progress-background">
              <CircularProgressbar
                value={fire_life(gameState.fire_spawn)}
                text={`${fire_life(gameState.fire_spawn)}`}
                maxValue={300}
                styles={buildStyles({
                  pathColor: "#8B0000",
                  textColor: "#000",
                  trailColor: "#f3f3f3",
                  backgroundColor: 'transparent',
                  textSize: '25px'
                })}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default RepeatSimulation;