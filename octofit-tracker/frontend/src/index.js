
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import reportWebVitals from './reportWebVitals';
import 'bootstrap/dist/css/bootstrap.min.css';

// Ustaw zmienną środowiskową REACT_APP_CODESPACE_NAME jeśli nie jest ustawiona (dla dev/test)
if (!process.env.REACT_APP_CODESPACE_NAME) {
  const url = window.location.hostname;
  // Wyciągnij nazwę codespace z hosta, np. "nazwa-8000.app.github.dev" => "nazwa"
  const match = url.match(/^(.*)-8000\.app\.github\.dev$/);
  if (match) {
    process.env.REACT_APP_CODESPACE_NAME = match[1];
  }
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

reportWebVitals();
