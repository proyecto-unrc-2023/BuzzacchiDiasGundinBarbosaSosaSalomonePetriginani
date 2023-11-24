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
  console.log(gameState.board)

  return (
    <div className="simulation-container">
      {/* Renderizar el componente Board y pasarle el JSON del tablero */}
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
      images.push(<img key="spawn" src={`/images/${cell.spawn.type}_spawn.jpg`} alt="Spawn" />);
    } else if (cell.fire_cells.length > 0) {
      // Representar las células de fuego con imágenes
      cell.fire_cells.forEach((fireCell, index) => {
        images.push(
          <img
            key={`fire_cell_${index}`}
            src={`/images/fire_cell_level_${fireCell.level}.png`}
            alt={`Fire Cell Level ${fireCell.level}`}
          />
        );
      });
    } else if (cell.ice_cells.length > 0) {
      // Representar las células de hielo con imágenes
      cell.ice_cells.forEach((iceCell, index) => {
        images.push(
          <img
            key={`ice_cell_${index}`}
            src={`/images/ice_cell_level_${iceCell.level}.png`}
            alt={`Ice Cell Level ${iceCell.level}`}
          />
        );
      });
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