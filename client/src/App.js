import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function App() {
  const [username, setUsername] = useState('');
  const [team, setTeam] = useState('Water Team');
  const navigate = useNavigate(); // Get the 'navigate' function to redirect to other pages

  // Handle changes in the username field
  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  // Handle changes in the team selection field
  const handleTeamChange = (event) => {
    setTeam(event.target.value);
  };

  // Handle form submission
  const handleSubmit = (event) => {
    event.preventDefault(); // Prevents the default form behavior

    // Object with the form data
    const formData = {
      username: username,
      team: team,
    };

    // Send to backend
    fetch('/init_game/start', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        // Backend response
        console.log(data);
        navigate('/game'); // Redirect
      })
      .catch((error) => {
        console.error('Error sending data:', error);
      });
  };

  return (
    <div>
      <h1>Welcome to the Game</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="username">Username:</label>
        <input
          type="text"
          id="username"
          name="username"
          value={username}
          onChange={handleUsernameChange}
          required
        />
        <br />
        <label htmlFor="team">Select Your Team:</label>
        <select id="team" name="team" value={team} onChange={handleTeamChange} required>
          <option value="Water Team">Water Team</option>
          <option value="Fire Team">Fire Team</option>
        </select>
        <br />
        <button type="submit">Start Game</button>
      </form>
    </div>
  );
}

export default App;
