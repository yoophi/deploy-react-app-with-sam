import axios from "axios";
import React, { useEffect, useState } from "react";
import "./App.css";
import logo from "./logo.svg";
import pic from "./i-can-do-it.jpg";

function App() {
  const [message, setMessage] = useState("");
  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_PUBLIC_URL}/api/hello-world`)
      .then((res) => {
        setMessage(res.data.message);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          {message}
        </a>
        <img
          src={pic}
          style={{ width: 128, height: 128, marginTop: 8 }}
          alt="pic"
        />
      </header>
    </div>
  );
}

export default App;
