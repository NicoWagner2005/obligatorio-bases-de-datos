import "./menudeadmin.css"
import { Navigate, useNavigate } from "react-router-dom"

export default function MenuAdmin(){


    const navigate = useNavigate()

    return(

       <div className="maincontaineradmin">
            <div className="headeradmin">
                    <img src="/assets/images/logo-ucu-blanco.png" alt="logo UCU" className='logoUCUadmin'/>
                <div className="cerrarSesionadmin">
                    <button className="botonCerrarSesionadmin" onClick={ () =>navigate("/login")}>
                        <img className="imagenCerrarSesionadmin" src="../assets/images/cerrarSesion.png"/>
                        Cerrar sesión
                    </button>
                </div>
            </div>
            <div className="contenedorCardsadmin">
                <div className="cardadmin" >
                    <h1>ABMs</h1>
                    <img src="../assets/images/lupa.png" style={{height:85, width:85}}/>
                </div>
                <div className="cardadmin" >
                    <h1>Reportes</h1>
                    <img src="../assets/images/grafico.png"/>
                </div>
            </div>

       </div>
    )
}