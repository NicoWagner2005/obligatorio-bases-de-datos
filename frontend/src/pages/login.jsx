
import { useState } from 'react';
import { Navigate } from "react-router-dom"
import "./login.css"
import { useNavigate } from 'react-router-dom';




export default function Login() {

    const [usuario, setUsuario] = useState("");       
    const [contraseña, setContraseña] = useState(""); 
    const [error, setError] = useState(false);        
    const navigate = useNavigate()

    const fetchLoginData = async (email, password) => {
    const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
    });
    if (!res.ok) {
      setError(true)
      throw new Error("Credenciales incorrectas");
      
    }
    if (res.ok){
      setError(false)
      IniciarSesion()}
      return res.json();
    };

    const IniciarSesion = (usuario) => {
    navigate("/menu", { state: { usuario } })
    }                                               //Inicio de sesion hard-codeado para progresar con el front; CAMBIAR!!!!!!!!

    const intentarIniciarSesion = (e) => {           
        fetchLoginData(usuario , contraseña)
    }

    return (
      <div className="maincontainer">
        <div className='ParteIzq'>
            <h1 className='titulo'>Reserva de salones</h1>
            <h2 className='subtitulo'>Sistema de reserva de salones para uso compartido, </h2>
            <h2 className='subtitulo'>tanto curricular como extra curricular.</h2> 
            <p className='nombres'>Desarrollado por: <br /> Guillermo González - Bruno Ocampo - Nicolás Wagner</p>
        </div>
        <div className="ParteDer">
          <div className='contenedorLogo'>
            <img src="/assets/images/logo-ucu-blanco.png" alt="logo UCU" className='logoUCU'/>
          </div>
          <div style={{display:"flex", flexDirection:"column", alignItems:"center", height:"75%"  , justifyContent:"center", width:"100%"}}>
            <h2 className='tituloIniciarSesion'>Entrar a reserva de salones</h2>
            <form className='contenedorLogin' onSubmit={intentarIniciarSesion}>
              <input className='inputlogin' type="text" placeholder='usuario'value={usuario}onChange={(e) => setUsuario(e.target.value)}/>
              <input className='inputlogin' type="password" placeholder='contraseña'value={contraseña}onChange={(e) => setContraseña(e.target.value)}/>
              <p className='errorInicioSesion'  style={{opacity: error ? 1 : 0}}>El usuario o contraseña son incorrectos</p>
              <button className='botonsesion' onClick={() => IniciarSesion(usuario)}>Iniciar sesión</button>
            </form>
          </div>
          
          
        </div>
      </div>
    )
}
