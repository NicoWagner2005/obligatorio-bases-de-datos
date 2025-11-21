import {useState, useEffect} from 'react';
import {useNavigate} from 'react-router-dom';
import "./login.css";
import {API_URL} from "../constants/api.js";

export default function Login() {

    const [usuario, setUsuario] = useState("");
    const [contraseña, setContraseña] = useState("");
    const [error, setError] = useState(false);
    const navigate = useNavigate();

    const login = async () => {
        try {
            const res = await fetch(`${API_URL}/auth/login`, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    email: usuario,
                    password: contraseña
                })
            })
            if (!res.ok) {
                throw Error(`HTTP Error: ${res.status} ${res.statusText}`);
            }

            const data = await res.json()
            console.log(data.user_id) //borrar despues console log

            // GUARDAR USER_ID PARA USAR EN LA APP
            // seria algo tipo : user_id = data.user_id

            navigate("/menu")

        } catch (err) {
            throw Error(`Error fetching login data: ${err.message ?? err} `);
        }
    }


    return (
        <div className="maincontainer">
            <div className='ParteIzq'>
                <h1 className='titulo'>Reserva de salones</h1>
                <h2 className='subtitulo'>Sistema de reserva de salones para uso compartido,</h2>
                <h2 className='subtitulo'>tanto curricular como extra curricular.</h2>
                <p className='nombres'>
                    Desarrollado por: <br/> Guillermo González - Bruno Ocampo - Nicolás Wagner
                </p>
            </div>

            <div className="ParteDer">
                <div className='contenedorLogo'>
                    <img src="/assets/images/logo-ucu-blanco.png" alt="logo UCU" className='logoUCU'/>
                </div>

                <div style={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    height: "75%",
                    justifyContent: "center",
                    width: "100%"
                }}>
                    <h2 className='tituloIniciarSesion'>Entrar a reserva de salones</h2>

                    <div className='contenedorLogin'>
                        <input
                            className='inputlogin'
                            type="text"
                            placeholder='usuario'
                            value={usuario}
                            onChange={(e) => setUsuario(e.target.value)}
                        />

                        <input
                            className='inputlogin'
                            type="password"
                            placeholder='contraseña'
                            value={contraseña}
                            onChange={(e) => setContraseña(e.target.value)}
                        />

                        <p
                            className='errorInicioSesion'
                            style={{opacity: error ? 1 : 0}}
                        >
                            El usuario o contraseña son incorrectos
                        </p>

                        {/* ESTE ES EL BOTÓN CORRECTO */}
                        <button className='botonsesion' onClick={login}>
                            Iniciar sesión
                        </button>

                    </div>
                </div>
            </div>
        </div>
    );
}
