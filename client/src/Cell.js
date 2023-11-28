import React from 'react';

const Cell = ({ cell }) => {
  const getCellClass = () => {
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

  const renderCellContent = () => {
    const images = [];

    if (cell.spawn) {
      images.push(<img key="spawn" src={`/images/${cell.spawn.type}_spawn.png`} alt="Spawn" />);
    } else if (cell.fire_cells.length > 0) {
      images.push(
        <img
          key={`fire_cell`}
          className="non-spawn-cell"
          src={`/images/fire_cell_level_${cell.fire_cells[0].level}.png`}
          alt={`Fire Cell Level ${cell.fire_cells[0].level}`}
        />
      );
    } else if (cell.ice_cells.length > 0) {
      images.push(
        <img
          key={`ice_cell`}
          className="non-spawn-cell"
          src={`/images/ice_cell_level_${cell.ice_cells[0].level}.png`}
          alt={`Ice Cell Level ${cell.ice_cells[0].level}`}
        />
      );
    }

    if (cell.ice_healing_area || cell.fire_healing_area) {
      images.push(
        <div key="healing" className="healing-images">
          {cell.ice_healing_area && <img src={`/images/ice_healing_area.png`} alt="Ice Healing" />}
          {cell.fire_healing_area && <img src={`/images/fire_healing_area.png`} alt="Fire Healing" />}
        </div>
      );
    }

    return <div className="cell-content">{images}</div>;
  };

  return <div className={`board-cell ${getCellClass()}`}>{renderCellContent()}</div>;
};

export default Cell;