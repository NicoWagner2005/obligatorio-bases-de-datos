import './abms.css'
import { useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import {API_URL} from '../constants/api'

export default function ABMs() {
    const navigate = useNavigate()
    const token = localStorage.getItem('token')
    const userId = localStorage.getItem('user_id')

    // Estado de tabs
    const [activeTab, setActiveTab] = useState('participantes')

    // Estado para Participantes
    const [participantes, setParticipantes] = useState([])
    const [formParticipante, setFormParticipante] = useState({
        ci: '', nombre: '', apellido: '', email: '', password: '', id_programa: 1, rol: 'estudiante'
    })
    const [editingParticipante, setEditingParticipante] = useState(null)

    // Estado para Salas
    const [salas, setSalas] = useState([])
    const [formSala, setFormSala] = useState({
        nombre_sala: '', id_edificio: 1, capacidad: 30, tipo_sala: 'estudio'
    })
    const [editingSala, setEditingSala] = useState(null)

    // Estado para Reservas
    const [reservas, setReservas] = useState([])
    const [formReserva, setFormReserva] = useState({
        id_sala: 1, fecha: '', id_turno: 1, participantes: []
    })
    const [editingReserva, setEditingReserva] = useState(null)

    // Estado para Sanciones
    const [sanciones, setSanciones] = useState([])
    const [formSancion, setFormSancion] = useState({
        ci_participante: '', fecha_inicio: '', fecha_fin: ''
    })
    const [editingSancion, setEditingSancion] = useState(null)

    const [loading, setLoading] = useState(false)
    const [message, setMessage] = useState('')

    // ===================== PARTICIPANTES =====================
    const cargarParticipantes = async () => {
        setLoading(true)
        try {
            // Nota: necesitarías un endpoint GET para listar participantes
            // Por ahora asumimos que existe /admin/participantes
            const res = await fetch(`${API_URL}/admin/participantes`, {
                headers: { 'Authorization': `Bearer ${token}` }
            })
            if (res.ok) {
                const data = await res.json()
                setParticipantes(data)
            }
        } catch (err) {
            console.error('Error cargando participantes:', err)
        } finally {
            setLoading(false)
        }
    }

    const crearParticipante = async () => {
        if (!formParticipante.ci || !formParticipante.email) {
            setMessage('Completa todos los campos requeridos')
            return
        }
        try {
            const res = await fetch(`${API_URL}/admin/participantes`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify(formParticipante)
            })
            if (res.ok) {
                setMessage('Participante creado exitosamente')
                setFormParticipante({ ci: '', nombre: '', apellido: '', email: '', password: '', id_programa: 1, rol: 'estudiante' })
                cargarParticipantes()
            } else {
                setMessage('Error al crear participante')
            }
        } catch (err) {
            setMessage(`Error: ${err.message}`)
        }
    }

    const actualizarParticipante = async () => {
        if (!editingParticipante?.ci) return
        try {
            const res = await fetch(`${API_URL}/admin/participantes/${editingParticipante.ci}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify(editingParticipante)
            })
            if (res.ok) {
                setMessage('Participante actualizado exitosamente')
                setEditingParticipante(null)
                cargarParticipantes()
            } else {
                setMessage('Error al actualizar participante')
            }
        } catch (err) {
            setMessage(`Error: ${err.message}`)
        }
    }

    const eliminarParticipante = async (ci) => {
        if (!window.confirm('¿Estás seguro de que deseas eliminar este participante?')) return
        try {
            const res = await fetch(`${API_URL}/admin/participantes/${ci}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            })
            if (res.ok) {
                setMessage('Participante eliminado exitosamente')
                cargarParticipantes()
            } else {
                setMessage('Error al eliminar participante')
            }
        } catch (err) {
            setMessage(`Error: ${err.message}`)
        }
    }

    // ===================== SALAS =====================
    const cargarSalas = async () => {
        setLoading(true)
        try {
            const res = await fetch(`${API_URL}/salas/`, {
                headers: { 'Authorization': `Bearer ${token}` }
            })
            if (res.ok) {
                const data = await res.json()
                // Aplanar salas de la respuesta estructurada
                const allSalas = (data.edificios || []).flatMap(e => e.salas || [])
                setSalas(allSalas)
            }
        } catch (err) {
            console.error('Error cargando salas:', err)
        } finally {
            setLoading(false)
        }
    }

    const crearSala = async () => {
        if (!formSala.nombre_sala) {
            setMessage('Completa todos los campos requeridos')
            return
        }
        try {
            const res = await fetch(`${API_URL}/admin/salas`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify(formSala)
            })
            if (res.ok) {
                setMessage('Sala creada exitosamente')
                setFormSala({ nombre_sala: '', id_edificio: 1, capacidad: 30, tipo_sala: 'estudio' })
                cargarSalas()
            } else {
                setMessage('Error al crear sala')
            }
        } catch (err) {
            setMessage(`Error: ${err.message}`)
        }
    }

    const actualizarSala = async () => {
        if (!editingSala?.id_sala) return
        try {
            const res = await fetch(`${API_URL}/admin/salas/${editingSala.id_sala}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify(editingSala)
            })
            if (res.ok) {
                setMessage('Sala actualizada exitosamente')
                setEditingSala(null)
                cargarSalas()
            } else {
                setMessage('Error al actualizar sala')
            }
        } catch (err) {
            setMessage(`Error: ${err.message}`)
        }
    }

    const eliminarSala = async (id) => {
        if (!window.confirm('¿Estás seguro de que deseas eliminar esta sala?')) return
        try {
            const res = await fetch(`${API_URL}/admin/salas/${id}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            })
            if (res.ok) {
                setMessage('Sala eliminada exitosamente')
                cargarSalas()
            } else {
                setMessage('Error al eliminar sala')
            }
        } catch (err) {
            setMessage(`Error: ${err.message}`)
        }
    }

    // ===================== RESERVAS =====================
    const cargarReservas = async () => {
        setLoading(true)
        try {
            // Nota: necesitarías un endpoint GET para listar todas las reservas (admin)
            const res = await fetch(`${API_URL}/admin/reservas`, {
                headers: { 'Authorization': `Bearer ${token}` }
            })
            if (res.ok) {
                const data = await res.json()
                setReservas(data)
            }
        } catch (err) {
            console.error('Error cargando reservas:', err)
        } finally {
            setLoading(false)
        }
    }

    const actualizarReserva = async () => {
        if (!editingReserva?.id_reserva) return
        try {
            const res = await fetch(`${API_URL}/admin/reservas/${editingReserva.id_reserva}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify(editingReserva)
            })
            if (res.ok) {
                setMessage('Reserva actualizada exitosamente')
                setEditingReserva(null)
                cargarReservas()
            } else {
                setMessage('Error al actualizar reserva')
            }
        } catch (err) {
            setMessage(`Error: ${err.message}`)
        }
    }

    // ===================== SANCIONES =====================
    const cargarSanciones = async () => {
        setLoading(true)
        try {
            // Nota: necesitarías un endpoint GET para listar sanciones
            const res = await fetch(`${API_URL}/admin/sanciones`, {
                headers: { 'Authorization': `Bearer ${token}` }
            })
            if (res.ok) {
                const data = await res.json()
                setSanciones(data)
            }
        } catch (err) {
            console.error('Error cargando sanciones:', err)
        } finally {
            setLoading(false)
        }
    }

    const crearSancion = async () => {
        if (!formSancion.ci_participante || !formSancion.fecha_inicio || !formSancion.fecha_fin) {
            setMessage('Completa todos los campos')
            return
        }
        try {
            const params = new URLSearchParams({
                ci_participante: formSancion.ci_participante,
                fecha_inicio: formSancion.fecha_inicio,
                fecha_fin: formSancion.fecha_fin
            })
            const res = await fetch(`${API_URL}/sanciones/crear?${params}`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            })
            if (res.ok) {
                setMessage('Sanción creada exitosamente')
                setFormSancion({ ci_participante: '', fecha_inicio: '', fecha_fin: '' })
                cargarSanciones()
            } else {
                setMessage('Error al crear sanción')
            }
        } catch (err) {
            setMessage(`Error: ${err.message}`)
        }
    }

    const eliminarSancion = async (ci, fechaInicio) => {
        if (!window.confirm('¿Estás seguro de que deseas eliminar esta sanción?')) return
        try {
            const res = await fetch(`${API_URL}/sanciones/${ci}/${fechaInicio}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            })
            if (res.ok) {
                setMessage('Sanción eliminada exitosamente')
                cargarSanciones()
            } else {
                setMessage('Error al eliminar sanción')
            }
        } catch (err) {
            setMessage(`Error: ${err.message}`)
        }
    }

    useEffect(() => {
        if (activeTab === 'participantes') cargarParticipantes()
        else if (activeTab === 'salas') cargarSalas()
        else if (activeTab === 'reservas') cargarReservas()
        else if (activeTab === 'sanciones') cargarSanciones()
    }, [activeTab])

    return (
        <div className="mainContainer">
            <div className="header">
                <img src="/assets/images/logo-ucu-blanco.png" alt="logo UCU" className='logoUCU' />
                <div className="volver">
                    <button className="botonVolver" onClick={() => navigate(`/menuadmin`, { state: { userId } })}>
                        <img className="imagenVolver" src="../assets/images/volver.png" />
                        Volver
                    </button>
                </div>
            </div>

            <div className="contenido" style={{ padding: '20px' }}>
                <h1>Administración</h1>

                {/* Tabs */}
                <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', borderBottom: '2px solid #ccc', paddingBottom: '10px' }}>
                    {['participantes', 'salas', 'reservas', 'sanciones'].map(tab => (
                        <button
                            key={tab}
                            onClick={() => setActiveTab(tab)}
                            style={{
                                padding: '10px 20px',
                                backgroundColor: activeTab === tab ? '#007bff' : '#ddd',
                                color: activeTab === tab ? 'white' : 'black',
                                border: 'none',
                                cursor: 'pointer',
                                borderRadius: '4px',
                                textTransform: 'capitalize'
                            }}
                        >
                            {tab}
                        </button>
                    ))}
                </div>

                {message && (
                    <p style={{ color: message.includes('Error') || message.includes('error') ? 'red' : 'green', marginBottom: '10px' }}>
                        {message}
                    </p>
                )}

                {/* ===================== PARTICIPANTES ===================== */}
                {activeTab === 'participantes' && (
                    <div>
                        <h2>Gestionar Participantes</h2>
                        <div style={{ marginBottom: '20px', padding: '10px', border: '1px solid #ddd', borderRadius: '4px' }}>
                            <h3>{editingParticipante ? 'Editar' : 'Crear'} Participante</h3>
                            <input
                                type="text"
                                placeholder="CI"
                                value={editingParticipante?.ci || formParticipante.ci}
                                onChange={e => editingParticipante ? setEditingParticipante({ ...editingParticipante, ci: e.target.value }) : setFormParticipante({ ...formParticipante, ci: e.target.value })}
                                disabled={!!editingParticipante}
                                style={{ marginRight: '10px', padding: '5px' }}
                            />
                            <input
                                type="text"
                                placeholder="Nombre"
                                value={editingParticipante?.nombre || formParticipante.nombre}
                                onChange={e => editingParticipante ? setEditingParticipante({ ...editingParticipante, nombre: e.target.value }) : setFormParticipante({ ...formParticipante, nombre: e.target.value })}
                                style={{ marginRight: '10px', padding: '5px' }}
                            />
                            <input
                                type="text"
                                placeholder="Apellido"
                                value={editingParticipante?.apellido || formParticipante.apellido}
                                onChange={e => editingParticipante ? setEditingParticipante({ ...editingParticipante, apellido: e.target.value }) : setFormParticipante({ ...formParticipante, apellido: e.target.value })}
                                style={{ marginRight: '10px', padding: '5px' }}
                            />
                            <input
                                type="email"
                                placeholder="Email"
                                value={editingParticipante?.email || formParticipante.email}
                                onChange={e => editingParticipante ? setEditingParticipante({ ...editingParticipante, email: e.target.value }) : setFormParticipante({ ...formParticipante, email: e.target.value })}
                                style={{ marginRight: '10px', padding: '5px' }}
                            />
                            <input
                                type="password"
                                placeholder="Contraseña"
                                value={editingParticipante?.password || formParticipante.password}
                                onChange={e => editingParticipante ? setEditingParticipante({ ...editingParticipante, password: e.target.value }) : setFormParticipante({ ...formParticipante, password: e.target.value })}
                                style={{ marginRight: '10px', padding: '5px' }}
                            />
                            <select
                                value={editingParticipante?.rol || formParticipante.rol}
                                onChange={e => editingParticipante ? setEditingParticipante({ ...editingParticipante, rol: e.target.value }) : setFormParticipante({ ...formParticipante, rol: e.target.value })}
                                style={{ marginRight: '10px', padding: '5px' }}
                            >
                                <option value="estudiante">Estudiante</option>
                                <option value="docente">Docente</option>
                                <option value="admin">Admin</option>
                            </select>
                            <button onClick={editingParticipante ? actualizarParticipante : crearParticipante} style={{ padding: '5px 15px', backgroundColor: '#28a745', color: 'white', border: 'none', cursor: 'pointer' }}>
                                {editingParticipante ? 'Actualizar' : 'Crear'}
                            </button>
                            {editingParticipante && (
                                <button onClick={() => setEditingParticipante(null)} style={{ marginLeft: '5px', padding: '5px 15px', backgroundColor: '#6c757d', color: 'white', border: 'none', cursor: 'pointer' }}>
                                    Cancelar
                                </button>
                            )}
                        </div>

                        <h3>Participantes Existentes</h3>
                        {loading ? <p>Cargando...</p> : (
                            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                                <thead>
                                    <tr style={{ backgroundColor: '#f0f0f0' }}>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>CI</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Nombre</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Apellido</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Email</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Rol</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {participantes.map(p => (
                                        <tr key={p.ci}>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{p.ci}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{p.nombre}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{p.apellido}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{p.email}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{p.rol}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                                                <button onClick={() => setEditingParticipante(p)} style={{ marginRight: '5px', padding: '5px 10px', backgroundColor: '#ffc107', cursor: 'pointer' }}>Editar</button>
                                                <button onClick={() => eliminarParticipante(p.ci)} style={{ padding: '5px 10px', backgroundColor: '#dc3545', color: 'white', cursor: 'pointer' }}>Eliminar</button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        )}
                    </div>
                )}

                {/* ===================== SALAS ===================== */}
                {activeTab === 'salas' && (
                    <div>
                        <h2>Gestionar Salas</h2>
                        <div style={{ marginBottom: '20px', padding: '10px', border: '1px solid #ddd', borderRadius: '4px' }}>
                            <h3>{editingSala ? 'Editar' : 'Crear'} Sala</h3>
                            <input
                                type="text"
                                placeholder="Nombre de Sala"
                                value={editingSala?.nombre_sala || formSala.nombre_sala}
                                onChange={e => editingSala ? setEditingSala({ ...editingSala, nombre_sala: e.target.value }) : setFormSala({ ...formSala, nombre_sala: e.target.value })}
                                style={{ marginRight: '10px', padding: '5px' }}
                            />
                            <input
                                type="number"
                                placeholder="Edificio ID"
                                value={editingSala?.id_edificio || formSala.id_edificio}
                                onChange={e => editingSala ? setEditingSala({ ...editingSala, id_edificio: parseInt(e.target.value) }) : setFormSala({ ...formSala, id_edificio: parseInt(e.target.value) })}
                                style={{ marginRight: '10px', padding: '5px' }}
                            />
                            <input
                                type="number"
                                placeholder="Capacidad"
                                value={editingSala?.capacidad || formSala.capacidad}
                                onChange={e => editingSala ? setEditingSala({ ...editingSala, capacidad: parseInt(e.target.value) }) : setFormSala({ ...formSala, capacidad: parseInt(e.target.value) })}
                                style={{ marginRight: '10px', padding: '5px' }}
                            />
                            <select
                                value={editingSala?.tipo_sala || formSala.tipo_sala}
                                onChange={e => editingSala ? setEditingSala({ ...editingSala, tipo_sala: e.target.value }) : setFormSala({ ...formSala, tipo_sala: e.target.value })}
                                style={{ marginRight: '10px', padding: '5px' }}
                            >
                                <option value="estudio">Estudio</option>
                                <option value="laboratorio">Laboratorio</option>
                                <option value="aula">Aula</option>
                            </select>
                            <button onClick={editingSala ? actualizarSala : crearSala} style={{ padding: '5px 15px', backgroundColor: '#28a745', color: 'white', border: 'none', cursor: 'pointer' }}>
                                {editingSala ? 'Actualizar' : 'Crear'}
                            </button>
                            {editingSala && (
                                <button onClick={() => setEditingSala(null)} style={{ marginLeft: '5px', padding: '5px 15px', backgroundColor: '#6c757d', color: 'white', border: 'none', cursor: 'pointer' }}>
                                    Cancelar
                                </button>
                            )}
                        </div>

                        <h3>Salas Existentes</h3>
                        {loading ? <p>Cargando...</p> : (
                            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                                <thead>
                                    <tr style={{ backgroundColor: '#f0f0f0' }}>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>ID</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Nombre</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Edificio</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Capacidad</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Tipo</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {salas.map(s => (
                                        <tr key={s.id_sala}>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{s.id_sala}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{s.nombre_sala}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{s.id_edificio}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{s.capacidad}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{s.tipo_sala}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                                                <button onClick={() => setEditingSala(s)} style={{ marginRight: '5px', padding: '5px 10px', backgroundColor: '#ffc107', cursor: 'pointer' }}>Editar</button>
                                                <button onClick={() => eliminarSala(s.id_sala)} style={{ padding: '5px 10px', backgroundColor: '#dc3545', color: 'white', cursor: 'pointer' }}>Eliminar</button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        )}
                    </div>
                )}

                {/* ===================== RESERVAS ===================== */}
                {activeTab === 'reservas' && (
                    <div>
                        <h2>Gestionar Reservas</h2>
                        <p style={{ color: '#666' }}>Editar reservas existentes (modificar sala, fecha, turno, participantes)</p>

                        {editingReserva && (
                            <div style={{ marginBottom: '20px', padding: '10px', border: '1px solid #ddd', borderRadius: '4px' }}>
                                <h3>Editar Reserva</h3>
                                <input
                                    type="number"
                                    placeholder="ID Sala"
                                    value={editingReserva.id_sala}
                                    onChange={e => setEditingReserva({ ...editingReserva, id_sala: parseInt(e.target.value) })}
                                    style={{ marginRight: '10px', padding: '5px' }}
                                />
                                <input
                                    type="date"
                                    value={editingReserva.fecha}
                                    onChange={e => setEditingReserva({ ...editingReserva, fecha: e.target.value })}
                                    style={{ marginRight: '10px', padding: '5px' }}
                                />
                                <input
                                    type="number"
                                    placeholder="Turno"
                                    value={editingReserva.id_turno}
                                    onChange={e => setEditingReserva({ ...editingReserva, id_turno: parseInt(e.target.value) })}
                                    style={{ marginRight: '10px', padding: '5px' }}
                                />
                                <button onClick={actualizarReserva} style={{ padding: '5px 15px', backgroundColor: '#28a745', color: 'white', border: 'none', cursor: 'pointer' }}>
                                    Actualizar
                                </button>
                                <button onClick={() => setEditingReserva(null)} style={{ marginLeft: '5px', padding: '5px 15px', backgroundColor: '#6c757d', color: 'white', border: 'none', cursor: 'pointer' }}>
                                    Cancelar
                                </button>
                            </div>
                        )}

                        <h3>Reservas Existentes</h3>
                        {loading ? <p>Cargando...</p> : (
                            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                                <thead>
                                    <tr style={{ backgroundColor: '#f0f0f0' }}>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>ID</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Sala</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Fecha</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Turno</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {reservas.map(r => (
                                        <tr key={r.id_reserva}>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{r.id_reserva}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{r.id_sala}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{r.fecha}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{r.id_turno}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                                                <button onClick={() => setEditingReserva(r)} style={{ padding: '5px 10px', backgroundColor: '#ffc107', cursor: 'pointer' }}>Editar</button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        )}
                    </div>
                )}

                {/* ===================== SANCIONES ===================== */}
                {activeTab === 'sanciones' && (
                    <div>
                        <h2>Gestionar Sanciones</h2>
                        <div style={{ marginBottom: '20px', padding: '10px', border: '1px solid #ddd', borderRadius: '4px' }}>
                            <h3>Crear Sanción</h3>
                            <input
                                type="text"
                                placeholder="CI Participante"
                                value={formSancion.ci_participante}
                                onChange={e => setFormSancion({ ...formSancion, ci_participante: e.target.value })}
                                style={{ marginRight: '10px', padding: '5px' }}
                            />
                            <input
                                type="date"
                                placeholder="Fecha Inicio"
                                value={formSancion.fecha_inicio}
                                onChange={e => setFormSancion({ ...formSancion, fecha_inicio: e.target.value })}
                                style={{ marginRight: '10px', padding: '5px' }}
                            />
                            <input
                                type="date"
                                placeholder="Fecha Fin"
                                value={formSancion.fecha_fin}
                                onChange={e => setFormSancion({ ...formSancion, fecha_fin: e.target.value })}
                                style={{ marginRight: '10px', padding: '5px' }}
                            />
                            <button onClick={crearSancion} style={{ padding: '5px 15px', backgroundColor: '#28a745', color: 'white', border: 'none', cursor: 'pointer' }}>
                                Crear Sanción
                            </button>
                        </div>

                        <h3>Sanciones Existentes</h3>
                        {loading ? <p>Cargando...</p> : (
                            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                                <thead>
                                    <tr style={{ backgroundColor: '#f0f0f0' }}>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>CI Participante</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Fecha Inicio</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Fecha Fin</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {sanciones.map((s, idx) => (
                                        <tr key={idx}>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{s.ci_participante}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{s.fecha_inicio}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{s.fecha_fin}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                                                <button onClick={() => eliminarSancion(s.ci_participante, s.fecha_inicio)} style={{ padding: '5px 10px', backgroundColor: '#dc3545', color: 'white', cursor: 'pointer' }}>Eliminar</button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        )}
                    </div>
                )}
            </div>
        </div>
    )
}