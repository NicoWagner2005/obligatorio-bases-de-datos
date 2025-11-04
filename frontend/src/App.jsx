import React from 'react'
import { BrowserRouter, Routes, Route, Navigate, useParams } from 'react-router-dom';
import Login from './components/login.jsx';
import Admin from './components/admin.jsx';
import Menu from './components/menudeusuario.jsx';
import ConsultarReservas from './components/consultarreservas.jsx';
import ReservarSalon from './components/reservarsalon.jsx'
import ConsultarSanciones from './components/consultarsanciones.jsx'


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
