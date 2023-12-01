import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Board from './Board';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import './Simulation.css'; 
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';


function Simulation() {
  const location = useLocation();
  const [gameState, setGameState] = useState(location.state && location.state.gameState);
  const [simulationId] = useState(gameState.simulation_id)
  const navigate = useNavigate();

  console.log('simulation game staste', gameState)
  let size = 15; // Valor predeterminado
  if (gameState && gameState.board) {
    size = JSON.parse(gameState.board).rows;
  }
  let bottomIce, bottomFire;
  switch (size) {
    case 25:
      bottomIce = '-600px';
      bottomFire = '-750px';
      break;
    case 20:
      bottomIce = '-400px';
      bottomFire = '-550px';
      break;
    case 15:
      bottomIce = '-50px';
      bottomFire = '-200px';
      break;
    default:
      bottomIce = '0px';
      bottomFire = '-200px';
  }
    
  useEffect(() => {
    let intervalId;

    const fetchAndUpdateGameState = async () => {
      try {
        if (gameState?.mode === 'FINISHED') {
          clearInterval(intervalId);
          navigate('/game/simulation/finished', { state: { gameState } });
        } else {
          const response = await fetch('/simulation/update_state', {
            method: 'POST',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              simulation_id: simulationId,
            }),
          })
          
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

  const spawn_life = (spawn) => {
    const SpawnObj = JSON.parse(spawn);
    const spawn_life = SpawnObj.life;
    return spawn_life;
  };

  
  const HealingAreaInfo = ({ healingArea }) => {
    healingArea = JSON.parse(healingArea)
    return ( 
      <TableContainer component={Paper} style={{
        color: '#333',
        fontFamily: 'Arial, sans-serif',
        fontSize: '14px', 
        backgroundColor: '#fff', 
      }}>
        <Table style={{ borderCollapse: 'collapse' }}>
          <TableHead>
            <TableRow style={{ borderBottom: '1px solid #333' }}>
              <TableCell style={{ padding: '10px', margin: '0' }}>Positions</TableCell>
              <TableCell style={{ padding: '10px', margin: '0' }}>Duration</TableCell>
              <TableCell style={{ padding: '10px', margin: '0' }}>Healing Rate</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell style={{ padding: '10px', margin: '0' }}>{healingArea.positions.map((pos) => `(${pos[0]}, ${pos[1]})`).join(', ')}</TableCell>
              <TableCell style={{ padding: '10px', margin: '0' }}>{healingArea.duration}</TableCell>
              <TableCell style={{ padding: '10px', margin: '0' }}>{healingArea.healing_rate}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
    );
  };

  return (
    <div className="simulation-container" style={{ position: 'relative' }}>
      <div className="progress-container">
        {gameState && gameState.ice_spawn && (
          <div className="progress-bar">
            <p className="progress-text">
              IceSpawn Life 
            </p>
            <div className="progress-background">
              <CircularProgressbar
                value={spawn_life(gameState.ice_spawn)}
                text={`${spawn_life(gameState.ice_spawn)}`}
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
      
      <div style={{ position: 'absolute', bottom: bottomIce, width: '50%', left: '25%' }}>
        <h2 className="h2-minimalist">Ice Healing Area Info:</h2>
        <HealingAreaInfo
          healingArea={gameState.ice_healing_area}
        />
      </div>

      <div style={{ position: 'absolute', bottom: bottomFire, width: '50%', left: '25%' }}>
        <h2 className="h2-minimalist">Fire Healing Area Info:</h2>
        <HealingAreaInfo
          healingArea={gameState.fire_healing_area}
        />
      </div>
      <div className="progress-container">
        {gameState && gameState.fire_spawn && (
          <div className="progress-bar">
            <p className="progress-text">
              FireSpawn Life
            </p>
            <div className="progress-background">
              <CircularProgressbar
                value={spawn_life(gameState.fire_spawn)}
                text={`${spawn_life(gameState.fire_spawn)}`}
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