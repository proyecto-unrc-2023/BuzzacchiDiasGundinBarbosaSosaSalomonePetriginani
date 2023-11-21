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

  return (
    <div className="simulation-container">
      {/* Renderizar el componente Board y pasarle el JSON del tablero */}
      {gameState && <Board boardData={JSON.parse(gameState.board)} />}
    </div>
  );
}

const Board = ({ boardData }) => {
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

  return (
    <div className="board-container">
      {boardData.board.map((row, rowIndex) => (
        <div key={rowIndex} className="board-row">
          {row.map((cell, columnIndex) => (
            <div key={columnIndex} className={`board-cell ${getCellClass(cell)}`}>
              {/* Puedes personalizar el contenido de cada celda según tus necesidades */}
              <span>Row: {rowIndex}, Col: {columnIndex}</span>
              {cell.spawn && (
                <div>
                  Spawn: Life {cell.spawn.life}, Type {cell.spawn.type}
                </div>
              )}
              {cell.fire_cells.length > 0 && (
                <div>
                  Fire Cells: {JSON.stringify(cell.fire_cells)}
                </div>
              )}
              {cell.ice_cells.length > 0 && (
                <div>
                  Ice Cells: {JSON.stringify(cell.ice_cells)}
                </div>
              )}
              {cell.fire_healing_area && (
                <div>
                  Fire Healing Area: {JSON.stringify(cell.fire_healing_area)}
                </div>
              )}
              {cell.ice_healing_area && (
                <div>
                  Ice Healing Area: {JSON.stringify(cell.ice_healing_area)}
                </div>
              )}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default Simulation;