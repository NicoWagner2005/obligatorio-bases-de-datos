import { useState } from 'react'
import './App.css'

function App() {
  
  return (
      <div className="maincontainer">
        <div className='ParteIzq'>
            <h1 className='titulo'>Reserva de salones</h1>
            <h2 className='subtitulo'>Sistema de reserva de salones para uso compartido, </h2>
            <h2 className='subtitulo'>tanto curricular como extra curricular.</h2> 
            <p className='nombres'>Guillermo González - Bruno Ocampo - Nicolás Wagner</p>
        </div>
        <div className="ParteDer">
          <div style={{height:"25%", width:"100%"}}>
            <img src="../assets/images/logo-ucu-blanco.png" alt="logo UCU" className='logoUCU'/>
          </div>
          <div style={{display:"flex", flexDirection:"column", alignItems:"center", height:"75%"  , justifyContent:"center", width:"100%"}}>
            <h2 className='tituloIniciarSesion'>Iniciar sesión</h2>
            <div className='contenedorLogin'>
              <input className='inputlogin' type="text" placeholder='usuario'/>
              <input className='inputlogin' type="text" placeholder='contraseña'/>
              <button className='botonsesion'>Iniciar sesión</button>
            </div>
          </div>
          
          
        </div>
      </div>
  )
}

export default App
