import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Board from './Board';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import './Simulation.css'; 


function Simulation() {
  const location = useLocation();
  const [gameState, setGameState] = useState(location.state && location.state.gameState);
  const [winnerTeam, setWinnerTeam] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    let intervalId;

    const fetchAndUpdateGameState = async () => {
      try {
        if (gameState?.mode === 'FINISHED') {
          clearInterval(intervalId);
          navigate('/game/simulation/finished', { state: { gameState } });
        } else {
          const response = await fetch(`/simulation/update_state`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          });
          
          if (response.status === 200) {
            const responseData = await response.json();
            setGameState(responseData.updated_game_state);
          }
        }

      } catch (error) {
        console.error('Error updating game state:', error);
      }
    };

    // Intervalo para llamar a fetchAndUpdateGameState cada 2 segundos
    intervalId = setInterval(fetchAndUpdateGameState, 1000);

    // Limpiar el intervalo cuando el componente se desmonta o gameState cambia
    return () => clearInterval(intervalId);
  }, [gameState?.id, gameState?.mode]);
  // console.log(gameState)

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

export default Simulation;