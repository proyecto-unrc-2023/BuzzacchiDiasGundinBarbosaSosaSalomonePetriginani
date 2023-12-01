
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css'; 

function App() {
  const [username, setUsername] = useState('');
  const [team, setTeam] = useState('FireTeam');
  const [size, setSize] = useState(15);

  const navigate = useNavigate();

  const handleTeamChange = (event) => {
    setTeam(event.target.value);
  };

  const handleSizeChange = (event) => {
    const selectedSize = event.target.value;
    setSize(selectedSize);
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
          navigate(`/game/${gameId}`, { state: { size: size } });
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
      <header style={{ textAlign: 'center', marginBottom: '20px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <h1 style={{ fontSize: '24px' }}>War Of Element</h1>
      </header>
      <main>
        <form className="login-form" onSubmit={(event) => event.preventDefault()}>
          <div style={{ display: 'flex', justifyContent: 'space-between', width: '300px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: '10px' }}>
              <label htmlFor="team" style={{ fontWeight: 'bold', marginBottom: '5px' }}>Select Your Team:</label>
              <select
                id="team"
                name="team"
                value={team}
                onChange={handleTeamChange}
                required
                style={{
                  border: '1px solid #ccc',
                  borderRadius: '3px',
                  padding: '5px 8px',
                  backgroundColor: '#fafafa',
                  width: '100%',
                  boxSizing: 'border-box',
                  appearance: 'none',
                  textAlign: 'center', 
                }}
              >
                <option value="IceTeam">Ice Team</option>
                <option value="FireTeam">Fire Team</option>
              </select>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: '10px' }}>
              <label htmlFor="size" style={{ fontWeight: 'bold', marginBottom: '5px' }}>Select Size:</label>
              <select
                id="size"
                name="size"
                value={size}
                onChange={handleSizeChange}
                required
                style={{
                  border: '1px solid #ccc',
                  borderRadius: '3px',
                  padding: '5px 8px',
                  backgroundColor: '#fafafa',
                  width: '100%',
                  boxSizing: 'border-box',
                  appearance: 'none',
                  textAlign: 'center', 
                }}
              >
                <option value="15">15x15</option>
                <option value="20">20x20</option>
                <option value="25">25x25</option>
              </select>
            </div>
          </div>
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
