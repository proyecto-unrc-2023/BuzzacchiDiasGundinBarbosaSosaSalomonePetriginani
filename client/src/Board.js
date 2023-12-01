import React from 'react';
import Cell from './Cell';

const Board = ({ boardData }) => {
  return (
    <div className="board-container" style={{ gridTemplateColumns: 'repeat(15, 1fr)' }}>
      {boardData.board.map((row, rowIndex) => (
        <div key={rowIndex} className="board-row">
          {row.map((cell, columnIndex) => (
            <Cell key={columnIndex} cell={cell} />
          ))}
        </div>
      ))}
    </div>
  );
};

export default Board;