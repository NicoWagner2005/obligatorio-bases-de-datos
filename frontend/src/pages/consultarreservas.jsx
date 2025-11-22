import { useNavigate } from "react-router-dom"
import { useState, useEffect } from "react"
import './consultarreservas.css'
import API_URL from "@/constants/api"

export default function consultarReservas() {
    
    const navigate = useNavigate()
    const [misreservas, setMisreservas] = useState([])
    const [loading, setLoading] = useState(true)
    const token = localStorage.getItem("token");


    useEffect(() => {
        const fetchReservas = async () => {
            try {
                const res = await fetch(`${API_URL}/mis-reservas`, {
                    headers: { Authorization: `Bearer ${token}` }
                })
                if (res.ok) {
                    const data = await res.json()
                    setMisreservas(data)
                }
            } catch (error) {
                console.error("Error al cargar reservas:", error)
            } finally {
                setLoading(false)
            }
        }
        fetchReservas()
    }, [])
    


        return(
            <div className="mainContainer">
                <div className="header">
                    <img src="/assets/images/logo-ucu-blanco.png" alt="logo UCU" className='logoUCU'/>
                    <div className="volver">
                        <button className="botonVolver" onClick={ () =>navigate(`/menu`)}>         
                            <img className="imagenVolver" src="../assets/images/volver.png"/>   
                            Volver
                        </button>
                    </div>
                </div>
                <div className="contenido">
                    <div className="cardMostrarReservas">
                        {loading ? (
                            <p>Cargando reservas...</p>
                        ) : misreservas.length === 0 ? (
                            <p>No tienes reservas</p>
                        ) : (
                            <ul>
                                {misreservas.map((reserva) => (
                                    <li key={reserva.id}>
                                        <strong>Salón:</strong> {reserva.salon} | 
                                        <strong> Fecha:</strong> {reserva.fecha} | 
                                        <strong> Estado:</strong> {reserva.estado}
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                </div>
            </div>
            )        
}