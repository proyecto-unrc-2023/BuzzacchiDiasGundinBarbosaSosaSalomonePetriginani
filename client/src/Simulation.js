import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';


function Simulation() {
  const location = useLocation();
  const [gameState, setGameState] = useState(location.state && location.state.gameState);
  const [winnerTeam, setWinnerTeam] = useState(null);

  useEffect(() => {
    let intervalId;

    const fetchAndUpdateGameState = async () => {
      try {
        if (gameState?.mode === 'FINISHED') {
          clearInterval(intervalId);
          const winnerResponse = await fetch(`/simulation/get_winner_team`);
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

const Board = ({ boardData }) => {
  const columns = boardData.columns;

  const getCellClass = (cell) => {
    // Lógica para determinar la clase de la celda según su contenido
    if (cell.spawn) {
      return 'spawn-cell';
    } else if (cell.fire_cells.length > 0) {
      return 'fire-cell';
    } else if (cell.ice_cells.length > 0) {
      return 'ice-cell';
    } else {
      return 'empty-cell';
    }
  };
  
  const renderCellContent = (cell) => {
    // Crear un array para almacenar las imágenes
    const images = [];

    // Renderizar el contenido de cada celda según su tipo
    if (cell.spawn) {
      // Representar el spawn con una imagen
      images.push(<img key="spawn" src={`/images/${cell.spawn.type}_spawn.png`} alt="Spawn" />);
    } else if (cell.ice_healing_area) {
      images.push(<img key="healing" src={`/images/ice_healing_area.png`} alt="healing"/>);  
    } else if (cell.fire_healing_area) {
      images.push(<img key="healing" src={`/images/fire_healing_area.png`} alt="healing"/>);  
    } else if (cell.fire_cells.length > 0) {
      // Representar las células de fuego con imágenes
        images.push(
          <img
            key={`fire_cell`}
            src={`/images/fire_cell_level_${ cell.fire_cells[0].level}.png`}
            alt={`Fire Cell Level ${ cell.fire_cells[0].level}`}
          />
        );
    } else if (cell.ice_cells.length > 0) {
      // Representar las células de hielo con imágenes
        images.push(
          <img
            key={`ice_cell`}
            src={`/images/ice_cell_level_${cell.ice_cells[0].level}.png`}
            alt={`Ice Cell Level ${cell.ice_cells[0].level}`}
          />
        );
    }
  
    // Devolver un solo div que contiene todas las imágenes
    return <div className="cell-content">{images}</div>;
  };

  return (
    <div className="board-container" style={{ gridTemplateColumns: 'repeat(15, 1fr)' }}>
      {boardData.board.map((row, rowIndex) => (
        <div key={rowIndex} className="board-row">
          {row.map((cell, columnIndex) => (
            <div key={columnIndex} className={`board-cell ${getCellClass(cell)}`}>
              {/* <span>Row: {rowIndex}, Col: {columnIndex}</span> */}
              {renderCellContent(cell)}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default Simulation;