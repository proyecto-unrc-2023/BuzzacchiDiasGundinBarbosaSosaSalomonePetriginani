import { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function FinishSimulation() {
  console.log('Componente montado');

  const location = useLocation();
  const [simulationId] = useState(location.state && location.state.simulationId);
  // Usar useRef como un flag
  const hasEffectRun = useRef(false);
  const navigate = useNavigate();

  const updateState = async () => {
    try {
      const response = await fetch('/simulation/update_state', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          simulation_id: simulationId,
        }),
      });

      if (!response.ok) {
        throw new Error('Error updating state');
      }

      const data = await response.json();
      // console.log(data);

      // Actualizar el estado si es necesario
      // setGameState(data.updated_game_state); // Por ejemplo, asumiendo que la respuesta contiene el nuevo estado
      console.log(data.updated_game_state)
      navigate(`/game/simulation`, { state: { gameState: data.updated_game_state } });
    } catch (error) {
      console.error('Error:', error);
    }
  };

  // Este efecto se ejecutará solo cuando simulationId cambie
  useEffect(() => {
    console.log('Efecto ejecutado');

    // Verificar el flag antes de ejecutar el código del efecto
    if (!hasEffectRun.current) {
      updateState();

      // Establecer el flag a true después de ejecutar el código del efecto
      hasEffectRun.current = true;
    }
  }, [simulationId]);
}
export default FinishSimulation;
