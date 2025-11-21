import React from 'react'
import { BrowserRouter, Routes, Route, Navigate, useParams } from 'react-router-dom';
import Login from './pages/login.jsx';
import MenuAdmin from './pages/menudeadmin.jsx';
import Menu from './pages/menudeusuario.jsx';
import ConsultarReservas from './pages/consultarreservas.jsx';
import ReservarSala from './pages/reservarsala.jsx'
import ConsultarSanciones from './pages/consultarsanciones.jsx'
import ABMs from './pages/abms.jsx'
import Reportes from './pages/reportes.jsx'


function App() {
  return (
    <div className="app">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/menu" element={<Menu/>} />
          <Route path="/reservarsala" element={<ReservarSala />} />
          <Route path="/consultarreservas" element={<ConsultarReservas />} />
          <Route path="/consultarsanciones" element={<ConsultarSanciones />} />
          <Route path='/menuadmin' element={<MenuAdmin />} />
          <Route path='/abms' element={<ABMs/>} />
          <Route path='reportes' element={<Reportes/>} />
        </Routes> 
      </BrowserRouter>
    </div>
  )
}

export default App
