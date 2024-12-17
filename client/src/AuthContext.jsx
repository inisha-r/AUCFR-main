// AuthContext.js
import React, { createContext, useState, useContext } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); // { email: '', role: '' }

  const login = (email, password) => {
    // Dummy authentication logic
    if (email === 'admin@gmail.com' && password === '123') {
      setUser({ email, role: 'admin' });
    } else if (email === 'user@gmail.com' && password === '123') {
      setUser({ email, role: 'user' });
    } else {
      alert('Invalid credentials');
    }
  };

  const logout = () => setUser(null);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
