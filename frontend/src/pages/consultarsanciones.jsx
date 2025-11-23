import { useNavigate } from "react-router-dom"
import { useState, useEffect } from "react"
import {API_URL} from "../constants/api"

export default function CosultarSanciones() {
    const navigate = useNavigate()
    const ci = localStorage.getItem("ci");
    const [sancion, setSancion] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const cargarSanciones = async () => {
            try {
                const res = await fetch(`${API_URL}/sanciones/${ci}`, {
                    method: "GET",
                    headers: { "Content-Type": "application/json", Authorization: `Bearer ${localStorage.getItem("token")}` },
                })
                if (res.ok) {
                    const data = await res.json()
                    const sanciones = data.sanciones || []
                    setSancion(sanciones.length > 0 ? sanciones[0] : null)
                }
            } catch (error) {
                console.error("Error al cargar sanciones:", error)
            } finally {
                setLoading(false)
            }
        }
        cargarSanciones()
    }, [ci])

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
            <div style={{"alignItems":"center","justifyContent":"center", "display":"flex", "flexDirection":"column", "height":"80%"}}>
                {loading ? (
                    <p>Cargando información de sanciones...</p>
                ) : sancion ? (
                    <div style={{"textAlign":"center"}}>
                        <h1 style={{"color":"red"}}>Usted está sancionado</h1>
                        <p style={{"fontSize":"18px"}}>No podrá reservar salas hasta <strong>{sancion.fecha_fin}</strong></p>
                    </div>
                ) : (
                    <div style={{"textAlign":"center"}}>
                        <h1 style={{"color":"green"}}>Usted no tiene sanciones activas</h1>
                    </div>
                )}
            </div>
        </div>
    )
}
        
               
