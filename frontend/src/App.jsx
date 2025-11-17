import React from 'react'
import { BrowserRouter, Routes, Route, Navigate, useParams } from 'react-router-dom';
import Login from './pages/login.jsx';
import Admin from './pages/admin.jsx';
import Menu from './pages/menudeusuario.jsx';
import ConsultarReservas from './pages/consultarreservas.jsx';
import ReservarSalon from './pages/reservarsalon.jsx'
import ConsultarSanciones from './pages/consultarsanciones.jsx'


function App() {
  return (
    <div className="app">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/admin" element={<Admin />} />
          <Route path="/menu/:id" element={<Menu/>}/>
          <Route path="/reservarsalon" element={<ReservarSalon />}/>
          <Route path="/consultarreservas" element={<ConsultarReservas />} />
          <Route path="/consultarsanciones" element={<ConsultarSanciones />}/>
        </Routes> 
      </BrowserRouter>
    </div>
  )
}

export default App
