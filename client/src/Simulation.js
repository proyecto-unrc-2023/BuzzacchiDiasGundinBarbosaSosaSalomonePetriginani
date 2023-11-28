import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Board from './Board';


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
          const winnerResponse = await fetch(`/simulation/get_winner_team`);
          navigate('/game/simulation/finished', { state: { gameState } });
          if (winnerResponse.status === 200) {
            const winnerTeam = await winnerResponse.text();
            console.log(winnerTeam)
            setWinnerTeam(winnerTeam);
          }        
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
  console.log(gameState)

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
      {/* Renderizar el componente Board y pasarle el JSON del tablero */}
      {gameState && gameState.ice_spawn && (
      <h1>IceSpawn life: {ice_life(gameState.ice_spawn)}</h1>
    )}
    {gameState && gameState.fire_spawn && (
      <h1>FireSpawn life: {fire_life(gameState.fire_spawn)}</h1>
    )}
      {gameState && <Board boardData={JSON.parse(gameState.board)} />}
    </div>
  );
}
export default Simulation;