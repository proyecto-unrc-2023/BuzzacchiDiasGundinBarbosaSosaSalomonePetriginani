import React, { useState } from 'react';

const Cell = () => {
  const [backgroundColor, setBackgroundColor] = useState('white');

  const handleClick = () => {
    // Cambia el color de fondo a verde cuando se hace clic
    setBackgroundColor(prevColor =>
        prevColor === 'white' ? 'green' : prevColor === 'green' ? 'red' : 'white'
      );
  };

  return (
    <div
      className="grid-item"
      style={{ backgroundColor }}
      onClick={handleClick}
    ></div>
  );
};

export default Cell;
