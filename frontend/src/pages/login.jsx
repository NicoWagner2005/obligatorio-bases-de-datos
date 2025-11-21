
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
  const res = await fetch("http://127.0.0.1:8000/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!res.ok) {
    setError(true);
    throw new Error("Credenciales incorrectas");
  }

  setError(false);
  const data = await res.json();  // 👈 acá obtenés el user + token
  return data;
};

const IniciarSesion = (usuario) => {
  navigate("/menu", { state: { usuario } });
};

const intentarIniciarSesion = async (e) => { 
  try {
    const data = await fetchLoginData(usuario, contraseña);
    IniciarSesion(data.user);  // 👈 enviar el usuario devuelto por backend
  } catch (err) {
    console.error(err);
  }
};

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
              <button className='botonsesion' onClick={intentarIniciarSesion}>Iniciar sesión</button>
            </form>
          </div>
          
          
        </div>
      </div>
    )
}
