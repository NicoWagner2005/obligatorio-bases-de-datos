import { useNavigate, useLocation } from "react-router-dom"
import React from "react"

export default function CosultarSanciones() {
    const navigate = useNavigate()
    const location = useLocation()
    const usuario = location.state?.usuario
    const [estaSancionado,setEstaSancionado] = React.useState(false) 
    const [fechaFin,setFechaFin] = React.useState("")

    const fetchSanciones = async (usuario) => {
    const res = await fetch(`${API_URL}/sanciones/${usuario}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ fecha_inicio, fecha_fin }),
    });
    if (!res.ok) {
    setError(true)
    throw new Error("No se ha podido cargar los datos de sanciones");}
    if (res.ok) {
        setFechaFin(fecha_fin)
    }
    }


    const validarSancion = async (usuario) => {
    const res = await fetch(`${API_URL}/sanciones/validar_sancion/${usuario}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ bloqueado, message }),
    });
    if (!res.ok) {
    setError(true)
    throw new Error("No se ha podido cargar los datos de sanciones");}
    if (res.ok) {
        setEstaSancionado(bloqueado)
    }
    }

     return(
                <div className="mainContainer">
                    <div className="header">
                        <img src="/assets/images/logo-ucu-blanco.png" alt="logo UCU" className='logoUCU'/>
                        <div className="cerrarSesion">
                            <button className="botonVolver" onClick={ () =>navigate(`/menu`)}>         
                                <img className="imagenVolver" src="../assets/images/volver.png"/>   
                                Volver 
                            </button>  
                        </div>
                    </div>
                    <div style={{"alignItems":"center","justifyContent":"center", "display":"flex", "flexDirection":"column"}}>
                        <h1>{}</h1>
                    </div>
                </div>
                )    

    };
        
               
