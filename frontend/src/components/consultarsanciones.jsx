import { useNavigate } from "react-router-dom"

export default function CosultarSanciones() {
     const navigate = useNavigate()
        
            return(
                <div className="mainContainer">
                    <div className="header">
                        <img src="/assets/images/logo-ucu-blanco.png" alt="logo UCU" className='logoUCU'/>
                        <div className="cerrarSesion">
                            <button className="botonCerrarSesion" onClick={ () =>navigate(`/menu/guille`)}>         
                                <img className="imagenCerrarSesion" src="../assets/images/volver.png"/>   
                                Volver 
                            </button>  
                        </div>
                    </div>
                </div>
                )        
}