import './reservarSala.css'
import { Navigate, useNavigate } from 'react-router-dom'
import usuario from './login'



export default function ReservarSala() {

    const navigate = useNavigate()

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
            <div className='contenido'>
                <div className='cardReservas'>
                    <div className='filtros'>
                        <img src="" alt="" />
                        <p style={{"fontFamily":"Arial, Helvetica, sans-serif","fontWeight":"bold"}}>Filtros</p>
                        <select className='filtro'>
                            <option value="">Edificio</option>
                        </select>
                        <select className='filtro'>
                            <option value="">Fecha</option>
                        </select>
                    </div>
                    <div className='mostrarSalones'></div>
                </div>
            </div>
        </div>
        )                                            

    }

  
