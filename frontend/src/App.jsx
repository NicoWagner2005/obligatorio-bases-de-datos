import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/login.jsx';
import Admin from './components/admin.jsx';
import Reservas from './components/reservas.jsx';

function App() {
  return (
    <div className="app">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/admin" element={<Admin />} />
          <Route path="/reservas" element={<Reservas />} />
        </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App
