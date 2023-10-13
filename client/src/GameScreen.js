import React, { useState, useEffect } from 'react';

function GameScreen() {
  const [userData, setUserData] = useState({ username: '', team: '' });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/init_game/get_game_data'); // GET request to backend
        if (!response.ok) {
          throw new Error('Error loading data');
        }
        const data = await response.json();
        setUserData(data); // Update state
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchData(); // Call the data fetching function when the component mounts
  }, []);

  return (
    <div>
      <h2>Welcome, {userData.username}!</h2>
      <p>You are part of the {userData.team}.</p>
    </div>
  );
}

export default GameScreen;
