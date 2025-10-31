import { useState } from 'react'
import './App.css'

function App() {
  
  return (
      <div className="maincontainer">
        <div className='ParteIzq'>
            <h1 className='titulo'>Reserva de salones</h1>
            <h2 className='subtitulo'>Sistema de reserva de salones para uso compartido, </h2>
            <h2 className='subtitulo'>tanto curricular como extra curricular.</h2> 
            
        </div>
        <div className="ParteDer">
          <img src="../assets/images/logo-ucu-blanco.png" alt="logo UCU" className='logoUCU'/>
          <div className='contenedorLogin'>
              <input className='inputlogin' type="text" placeholder='usuario'/>
              <input className='inputlogin' type="text" placeholder='contraseña'/>
              <button className='botonsesion'>Iniciar sesión</button>
          </div>
        </div>
      </div>
  )
}

export default App
