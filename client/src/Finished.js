import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';


function Finished()  {
  const location = useLocation();
  const [winnerTeam, setWinnerTeam] = useState(null);
  const navigate = useNavigate();
  const gameState = location.state?.gameState;
  useEffect(() => {
    const winnerTeam = () => {
      const fire_spawn = JSON.parse(gameState.fire_spawn);
      const ice_spawn = JSON.parse(gameState.ice_spawn);
      const ice_life = ice_spawn.life;
      const fire_life = fire_spawn.life;
      
      if (ice_life === 0 || ice_life < 0) {
        return 'Fire-Team';
      } else if (fire_life === 0 || fire_life < 0) {
        return 'Ice-Team';
      } else {
        return 'Draw';
      }
    };

    setWinnerTeam(winnerTeam());
  }, [gameState]);

  const handleGoLogIn = () => {
    navigate(`/`);
  };

  return (
    <div className="winner-team">
      <h1>The winner is: {winnerTeam} !</h1>
      <p>Return to the Log in</p>
      <button className="go-login" onClick={handleGoLogIn}>
        Go to log in
      </button>
    </div>
  );
}

export default Finished;