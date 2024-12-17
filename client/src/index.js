import React from 'react';
import ReactDOM from 'react-dom';
import './index.css'; // Ensure this file contains Tailwind CSS imports
import App from './App';
import { AuthProvider } from './AuthContext';

ReactDOM.render(
  <AuthProvider>
    <App />
  </AuthProvider>,
  document.getElementById('root')
);
