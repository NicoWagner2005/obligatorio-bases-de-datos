import { useNavigate } from "react-router-dom"
import { useState } from "react"
import './consultarreservas.css'
import Reserva from "../components/reserva"

export default function consultarReservas() {
    
    const navigate = useNavigate()
    const [reservas, setReservas] = useState([])
    


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
                        <li>
                            

                        </li>
                    </div>
                </div>
            </div>
            )        
}