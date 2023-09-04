import React from 'react';
import Cell from './Cell';

const Grid = () => {
    // Genera una cuadrícula de 50x50 celdas
    const rows = Array.from({ length: 50 }, () => (
      <div className="grid-row">
        {Array.from({ length: 50 }, (_, index) => (
          <Cell key={index} />
        ))}
      </div>
    ));

    return <div className="grid-container">{rows}</div>;
  };

export default Grid;
