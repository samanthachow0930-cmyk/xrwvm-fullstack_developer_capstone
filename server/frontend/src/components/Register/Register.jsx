import React, { useState } from "react";
import "./Register.css";
import user_icon from "../assets/person.png"
import email_icon from "../assets/email.png"
import password_icon from "../assets/password.png"
import close_icon from "../assets/close.png"

const Register = () => {
  // State variables for form inputs
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState({ text: "", type: "" });

  // Redirect to home
  const gohome = (e) => {
    e.preventDefault();
    window.location.href = window.location.origin;
  }

  // Handle form submission
  const register = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage({ text: "", type: "" });

    let register_url = window.location.origin + "/djangoapp/register";

    try {
      // Send POST request to register endpoint
      const res = await fetch(register_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          "userName": userName,
          "password": password,
          "firstName": firstName,
          "lastName": lastName,
          "email": email
        }),
      });

      const json = await res.json();
      
      if (json.status) {
        // Save username in session and reload home
        sessionStorage.setItem('username', json.userName);
        setMessage({ text: "Registration successful! Redirecting...", type: "success" });
        setTimeout(() => {
          window.location.href = window.location.origin;
        }, 1500);
      }
      else if (json.error === "Already Registered") {
        setMessage({ text: "The user with this username is already registered.", type: "error" });
      } else {
        setMessage({ text: "Registration failed. Please try again.", type: "error" });
      }
    } catch (error) {
      setMessage({ text: "Network error. Please check your connection.", type: "error" });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="register_container">
      <div className="header">
        <span className="text">Create Account</span>
        <a href="/" onClick={gohome} className="close_button">
          <img src={close_icon} alt="Close" />
        </a>
      </div>

      <form onSubmit={register}>
        <div className="inputs">
          {/* Username */}
          <div className="input_row">
            <div className="img_icon">
              <img src={user_icon} alt="Username" />
            </div>
            <input 
              type="text" 
              name="username" 
              placeholder="Username" 
              className="input_field" 
              onChange={(e) => setUserName(e.target.value)}
              required
            />
          </div>

          {/* First Name */}
          <div className="input_row">
            <div className="img_icon">
              <img src={user_icon} alt="First Name" />
            </div>
            <input 
              type="text" 
              name="first_name" 
              placeholder="First Name" 
              className="input_field" 
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
          </div>

          {/* Last Name */}
          <div className="input_row">
            <div className="img_icon">
              <img src={user_icon} alt="Last Name" />
            </div>
            <input 
              type="text" 
              name="last_name" 
              placeholder="Last Name" 
              className="input_field" 
              onChange={(e) => setLastName(e.target.value)}
              required
            />
          </div>

          {/* Email */}
          <div className="input_row">
            <div className="img_icon">
              <img src={email_icon} alt="Email" />
            </div>
            <input 
              type="email" 
              name="email" 
              placeholder="Email Address" 
              className="input_field" 
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          {/* Password */}
          <div className="input_row">
            <div className="img_icon">
              <img src={password_icon} alt="Password" />
            </div>
            <input 
              name="password" 
              type="password" 
              placeholder="Password" 
              className="input_field" 
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength="6"
            />
          </div>
        </div>

        {/* Message Display */}
        {message.text && (
          <div className={`form_message ${message.type}`}>
            {message.text}
          </div>
        )}

        <div className="submit_panel">
          <button 
            type="submit" 
            className={`submit ${isLoading ? 'loading' : ''}`}
            disabled={isLoading}
          >
            {isLoading ? "Creating Account..." : "Create Account"}
          </button>

          <div className="login_link">
            Already have an account? <a href="/login">Sign In</a>
          </div>
        </div>
      </form>
    </div>
  )
}

export default Register;