import { useParams } from "react-router-dom"
import "./menudeusuario.css"
import { useNavigate } from 'react-router-dom';


export default function Menu(){
    const navigate = useNavigate()
    const { id } = useParams()

    const gotoReservarSalon = () =>
    {
        navigate("/reservarsalon")
    }
    const gotoConsultarReservas = () =>
    {
        navigate("/consultarreservas")
    }
    const gotoConsultarSanciones = () =>
    {
        navigate("/consultarsanciones")
    }

    return(
        <div className="mainContainer">
            <div className="header">
                    <img src="/assets/images/logo-ucu-blanco.png" alt="logo UCU" className='logoUCU'/>
                <div className="cerrarSesion">
                    <button className="botonCerrarSesion" onClick={ () =>navigate("/login")}>
                        <img className="imagenCerrarSesion" src="../assets/images/cerrarSesion.png"/>
                        Cerrar sesión
                    </button>
                </div>
            </div>
            <div className="contenedorCards">
                <div className="card" onClick={gotoReservarSalon}>
                    <h1>Reservar un salón</h1>
                    <img src="../assets/images/reservarSalon.png" style={{height:85, width:85}}/>
                </div>
                <div className="card" onClick={gotoConsultarReservas}>
                    <h1>Consultar reservas</h1>
                    <img src="../assets/images/consultarReservas.png"/>
                </div>
                <div className="card" onClick={gotoConsultarSanciones}>
                    <h1>Consultar Sanciones</h1>
                    <img src="../assets/images/consultarSanciones.png"/>
                </div>
            </div>
        </div>
    )
}