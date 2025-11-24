import './reservarSala.css'
import { useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { API_URL } from '../constants/api'

export default function ReservarSala() {
    const navigate = useNavigate()
    const userId = localStorage.getItem('user_id')
    const ci = localStorage.getItem('ci')
    const token = localStorage.getItem('token')

    const [edificios, setEdificios] = useState([])
    const [selectedEdificioId, setSelectedEdificioId] = useState(null)
    const [selectedSalaId, setSelectedSalaId] = useState(null)
    const [fecha, setFecha] = useState(new Date().toISOString().slice(0, 10))
    const [startHour, setStartHour] = useState(8)
    const [duration, setDuration] = useState(1)
    const [message, setMessage] = useState("")
    const [loading, setLoading] = useState(true)
    const [reservando, setReservando] = useState(false)

    // ===========================
    //   Cargar edificios
    // ===========================
    useEffect(() => {
        const fetchEdificios = async () => {
            try {
                const res = await fetch(`${API_URL}/salas/`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                })
                if (res.ok) {
                    const data = await res.json()
                    setEdificios(data.edificios || [])
                }
            } catch (err) {
                console.error(err)
            } finally {
                setLoading(false)
            }
        }
        fetchEdificios()
    }, [])

    // ===========================
    //   Reservar sala
    // ===========================
    const handleReservar = async () => {
        setMessage("")

        if (!userId) return setMessage("Debe iniciar sesión para reservar")
        if (!ci) return setMessage("No se pudo obtener la cédula del usuario; vuelva a iniciar sesión")
        if (!selectedSalaId) return setMessage("Seleccione una sala")
        if (!fecha) return setMessage("Seleccione una fecha")

        // Validar sanciones
        try {
            const sancRes = await fetch(`${API_URL}/sanciones/validar_sancion_usuario/${userId}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            })

            if (sancRes.ok) {
                const sancData = await sancRes.json()
                if (sancData.bloqueado) {
                    return setMessage(sancData.message || "Usted está sancionado y no puede reservar")
                }
            }
        } catch (err) {
            console.error("Error validando sanción", err)
        }

        // Validar límite de horas por día
        let existingHours = 0
        try {
            const r = await fetch(`${API_URL}/salas/mis-reservas`, {
                headers: { 'Authorization': `Bearer ${token}` }
            })
            if (r.ok) {
                const data = await r.json()
                existingHours = (data.reservas || []).filter(x => x.fecha === fecha).length
            }
        } catch (err) {
            console.warn("No se pudo obtener reservas previas", err)
        }

        if (existingHours + Number(duration) > 3) {
            return setMessage("No puede reservar más de 3 horas por día")
        }

        // Crear reservas
        setReservando(true)

        try {
            for (let i = 0; i < Number(duration); i++) {
                const turno = (Number(startHour) - 8) + 1 + i;


                const body = {
                    id_sala: selectedSalaId,
                    fecha: fecha,
                    id_turno: turno,
                    user_id: Number(userId)
                }

                const res = await fetch(`${API_URL}/salas/reservar`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(body)
                })

                if (!res.ok) {
                    const err = await res.text()
                    setMessage(`Error al crear reserva (turno ${turno}): ${err}`)
                    return
                }
            }

            setMessage("Reserva(s) creada(s) exitosamente")

        } catch (err) {
            console.error("Error creando la reserva:", err)
            setMessage("Error inesperado al crear la reserva")

        } finally {
            setReservando(false)
        }
    }

    // ===========================
    //   Render
    // ===========================
    const horasOptions = []
    for (let h = 8; h <= 21; h++) horasOptions.push(h)

    const salasToShow = selectedEdificioId
        ? (edificios.find(e => e.id_edificio === Number(selectedEdificioId))?.salas || [])
        : []

    return (
        <div className="mainContainer">
            <div className="header">
                <img src="/assets/images/logo-ucu-blanco.png" alt="logo UCU" className='logoUCU' />
                <div className="volver">
                    <button className="botonVolver" onClick={() => navigate(`/menu`, { state: { userId } })}>
                        <img className="imagenVolver" src="../assets/images/volver.png" />
                        Volver
                    </button>
                </div>
            </div>

            <div className='contenido'>
                <div className='cardReservas'>
                    <div className='filtros'>
                        <p style={{ fontWeight: "bold" }}>Filtros</p>

                        <select className='filtro'
                            value={selectedEdificioId || ''}
                            onChange={e => { setSelectedEdificioId(e.target.value); setSelectedSalaId(null) }}>
                            <option value="">Seleccione edificio</option>
                            {edificios.map(ed => (
                                <option key={ed.id_edificio} value={ed.id_edificio}>
                                    {ed.nombre_edificio}
                                </option>
                            ))}
                        </select>

                        <input className='filtro' type='date' value={fecha} onChange={e => setFecha(e.target.value)} />

                        <select className='filtro' value={startHour} onChange={e => setStartHour(e.target.value)}>
                            {horasOptions.map(h => (
                                <option key={h} value={h}>{`${h}:00 - ${h + 1}:00`}</option>
                            ))}
                        </select>

                        <select className='filtro' value={duration} onChange={e => setDuration(e.target.value)}>
                            <option value={1}>1 hora</option>
                            <option value={2}>2 horas</option>
                            <option value={3}>3 horas</option>
                        </select>

                        <button className='botonsesion' onClick={handleReservar} disabled={reservando}>
                            {reservando ? 'Reservando...' : 'Reservar'}
                        </button>

                        {message &&
                            <p style={{ color: message.includes("exitosamente") ? "green" : "red" }}>
                                {message}
                            </p>
                        }
                    </div>

                    <div className='mostrarSalones'>
                        <h3>Salas</h3>

                        {loading ? <p>Cargando...</p> : (
                            salasToShow.length === 0 ? <p>Seleccione un edificio para ver sus salas</p> : (
                                <ul>
                                    {salasToShow.map(s => (
                                        <li key={s.id_sala} style={{ marginBottom: 8 }}>
                                            <label>
                                                <input
                                                    type="radio"
                                                    name="sala"
                                                    value={s.id_sala}
                                                    checked={Number(selectedSalaId) === s.id_sala}
                                                    onChange={() => setSelectedSalaId(s.id_sala)}
                                                />
                                                <strong>{s.nombre_sala}</strong> — {s.tipo_sala} — cap: {s.capacidad}
                                            </label>
                                        </li>
                                    ))}
                                </ul>
                            )
                        )}

                    </div>
                </div>
            </div>
        </div>
    )
}
