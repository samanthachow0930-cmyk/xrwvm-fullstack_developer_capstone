import React, { useState } from 'react';
import "./Login.css";
import Header from '../Header/Header';
import close_icon from "../assets/close.png"; // Make sure you have this icon

const Login = ({ onClose }) => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [open, setOpen] = useState(true);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const login_url = window.location.origin + "/djangoapp/login";

  const login = async (e) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const res = await fetch(login_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          "userName": userName,
          "password": password
        }),
      });
      
      const json = await res.json();
      
      if (json.status !== null && json.status === "Authenticated") {
        sessionStorage.setItem('username', json.userName);
        setOpen(false);        
      } else {
        setError("Invalid username or password. Please try again.");
      }
    } catch (err) {
      setError("Unable to connect to server. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleClose = () => {
    setOpen(false);
    if (onClose) onClose();
  };

  if (!open) {
    window.location.href = "/";
    return null;
  };

  return (
    <div style={{ background: '#ffffff', minHeight: '100vh' }}>
      <Header />
      <div className="login_container">
        <div className="login_header">
          <div className="login_text">Sign In</div>
          <a href="/" onClick={(e) => {
            e.preventDefault();
            handleClose();
          }}>
            <img src={close_icon} alt="Close" />
          </a>
        </div>
        
        {error && (
          <div className="login_error show">
            {error}
          </div>
        )}
        
        <form onSubmit={login}>
          <div className="login_inputs">
            <div className="login_input">
              <div className="login_img_icon">
                <span>👤</span>
              </div>
              <input 
                type="text" 
                name="username" 
                placeholder="Enter your username" 
                className="login_input_field" 
                onChange={(e) => setUserName(e.target.value)}
                required
              />
            </div>
            
            <div className="login_input">
              <div className="login_img_icon">
                <span>🔒</span>
              </div>
              <input 
                name="password" 
                type="password" 
                placeholder="Enter your password" 
                className="login_input_field" 
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>
          
          <div className="login_button_panel">
            <div className="login_buttons">
              <button 
                type="submit" 
                className={`login_button login_submit ${isLoading ? 'loading' : ''}`}
                disabled={isLoading}
              >
                {isLoading ? "Signing in..." : "Sign In"}
              </button>
              <button 
                type="button" 
                className="login_button login_cancel"
                onClick={handleClose}
              >
                Cancel
              </button>
            </div>
            
            <a className="login_register_link" href="/register">
              Don't have an account? Register Now
            </a>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;