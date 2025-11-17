import { useNavigate } from "react-router-dom"

export default function CosultarSanciones() {
     const navigate = useNavigate()
        
            return(
                <div className="mainContainer">
                    <div className="header">
                        <img src="/assets/images/logo-ucu-blanco.png" alt="logo UCU" className='logoUCU'/>
                        <div className="cerrarSesion">
                            <button className="botonVolver" onClick={ () =>navigate(`/menu/guille`)}>         
                                <img className="imagenVolver" src="../assets/images/volver.png"/>   
                                Volver 
                            </button>  
                        </div>
                    </div>
                    <div style={{"alignItems":"center","justifyContent":"center", "display":"flex", "flexDirection":"column"}}>
                        <h1 style={{"color":"red"}}>SANCIONADO POR WACHIN!</h1>
                        <img style={{"height":500, "width":500}} src="../assets/images/wachin.jpg" alt="" />
                    </div>
                </div>
                )        
}