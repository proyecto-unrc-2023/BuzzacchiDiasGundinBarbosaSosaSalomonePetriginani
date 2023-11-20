
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css'; 

function App() {
  const [username, setUsername] = useState('');
  const [team, setTeam] = useState('FireTeam');
  const navigate = useNavigate();

  const handleTeamChange = (event) => {
    setTeam(event.target.value);
  };

  const handleGoogleSignOut = () => {
    window.google.accounts.id.disableAutoSelect();
    window.google.accounts.id.revoke(localStorage.getItem('email'), (done) => {
      localStorage.clear();
      window.location.reload();
    });
  };

  useEffect(() => {
    window.onGoogleScriptLoad = () => {
      const params = {
        client_id: "450042762936-gsjdaj4lh1ftmac3md1nvs1dufhbprgt.apps.googleusercontent.com",
        callback: window.handleCredentialResponse,
        auto_prompt: false,
      };
      window.google.accounts.id.initialize(params);
      window.google.accounts.id.renderButton(
        document.getElementById("my-signin2"),
        { theme: "outline", size: "large", shape: "rectangular", text: "sign_in_with", logo_alignment: "left" }
      );
    };

    const script = document.createElement("script");
    script.src = "https://accounts.google.com/gsi/client";
    script.async = true;
    script.defer = true;
    script.onload = window.onGoogleScriptLoad;
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  useEffect(() => {
    if (username) {
      const formData = {
        username: username,
        team: team,
      };

      fetch('/simulation/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })
        .then((response) => response.json())
        .then((data) => {
          const gameId = data.game_state.id;
          navigate(`/game/${gameId}`);
        })
        .catch((error) => {
          console.error('Error sending data:', error);
        });
    }
  }, [username, team, navigate]);

  window.handleCredentialResponse = (response) => {
    const body = {
      id_token: response.credential,
      authenticatedWithGoogle: true,
    };

    fetch('/simulation/google', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })
      .then((r) => r.json())
      .then((resp) => {
        localStorage.setItem('email', resp.correo);
        setUsername(resp.name);
      })
      .catch(console.warn);
  };

return (

  <div className={`container ${team === 'FireTeam' ? 'fire' : 'ice'}`}>
      <header>
        <h1>War Of Element</h1>
      </header>
      <main>
        <form className="login-form" onSubmit={(event) => event.preventDefault()}>
          <label htmlFor="team">Select Your Team:</label>
          <select id="team" name="team" value={team} onChange={handleTeamChange} required>
            <option value="IceTeam">Ice Team</option>
            <option value="FireTeam">Fire Team</option>
          </select>
          <br />
          <div id="my-signin2" className="google-signin"></div>
          <br />
          <button type="button" id="google_sign_out" className="sign-out-btn" onClick={handleGoogleSignOut}>
            Sign Out
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;
