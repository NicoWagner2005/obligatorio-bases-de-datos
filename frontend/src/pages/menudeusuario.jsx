import "./menudeusuario.css"
import { useNavigate } from 'react-router-dom';


export default function Menu(){

    const userid = localStorage.getItem("user_id")
    const navigate = useNavigate()

    const cerrarSesion = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("admin");
        localStorage.removeItem("user_id");
        navigate("/login");
    }


    const gotoReservarSala = () =>
    {
        navigate("/reservarsala",{state:{userid:userid}})
    }
    const gotoConsultarReservas = () =>
    {
        navigate("/consultarreservas",{state:{userid:userid}})
    }
    const gotoConsultarSanciones = () =>
    {
        navigate("/consultarsanciones",{state:{userid:userid}} )
    }

    return(
        <div className="mainContainer">
            <div className="header">
                    <img src="/assets/images/logo-ucu-blanco.png" alt="logo UCU" className='logoUCU'/>
                <div className="cerrarSesion">
                    <button className="botonCerrarSesion" onClick={ () =>cerrarSesion()}>
                        <img className="imagenCerrarSesion" src="../assets/images/cerrarSesion.png"/>
                        Cerrar sesión
                    </button>
                </div>
            </div>
            <div className="contenedorCards">
                <div className="card" onClick={gotoReservarSala}>
                    <h1>Reservar una sala</h1>
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