

import './reportes.css'
import { useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import API_URL from '@/constants/api'

export default function Reportes() {
    const navigate = useNavigate()
    const token = localStorage.getItem('token')
    const userId = localStorage.getItem('user_id')

    const [reports, setReports] = useState({})
    const [loading, setLoading] = useState(true)
    const [selectedReport, setSelectedReport] = useState('salas-mas-reservadas')

    const reportsList = [
        { key: 'salas-mas-reservadas', label: 'Salas Más Reservadas', endpoint: '/salas-mas-reservadas' },
        { key: 'salas-menos-reservadas', label: 'Salas Menos Reservadas', endpoint: '/salas-menos-reservadas' },
        { key: 'turnos-mas-demandados', label: 'Turnos Más Demandados', endpoint: '/turnos-mas-demandados' },
        { key: 'turnos-menos-demandados', label: 'Turnos Menos Demandados', endpoint: '/turnos-menos-demandados' },
        { key: 'promedio-participantes-sala', label: 'Promedio de Asistencia por Sala', endpoint: '/promedio-participantes-sala' },
        { key: 'cantidad-reservas-carrera-y-facultad', label: 'Reservas por Carrera y Facultad', endpoint: '/cantidad-reservas-carrera-y-facultad' },
        { key: 'porcentaje-ocupacion-salas-edificio', label: 'Porcentaje de Ocupación por Edificio', endpoint: '/porcentaje-ocupacion-salas-edificio' },
        { key: 'cantidad-reservas-asistencias-tipo-usuario', label: 'Reservas y Asistencias por Tipo de Usuario', endpoint: '/cantidad-reservas-asistencias-tipo-usuario' },
        { key: 'cantidad-sanciones-tipo-usuario', label: 'Sanciones por Tipo de Usuario', endpoint: '/cantidad-sanciones-tipo-usuario' },
        { key: 'porcentaje-reservas-efectivamente-utilizadas', label: 'Porcentaje de Reservas Utilizadas', endpoint: '/porcentaje-reservas-efectivamente-utilizadas' },
        { key: 'cantidad-reservas-por-sala', label: 'Cantidad de Reservas por Sala', endpoint: '/cantidad-reservas-por-sala' },
    ]

    const cargarReporte = async (endpoint, key) => {
        setLoading(true)
        try {
            const res = await fetch(`${API_URL}/analytics${endpoint}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            })
            if (res.ok) {
                const data = await res.json()
                setReports(prev => ({ ...prev, [key]: data }))
            } else {
                console.error('Error cargando reporte:', endpoint)
            }
        } catch (err) {
            console.error('Error:', err)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        const report = reportsList.find(r => r.key === selectedReport)
        if (report && !reports[selectedReport]) {
            cargarReporte(report.endpoint, selectedReport)
        } else {
            setLoading(false)
        }
    }, [selectedReport])

    const currentReport = reportsList.find(r => r.key === selectedReport)
    const currentData = reports[selectedReport] || []

    const renderTable = (data) => {
        if (!data || data.length === 0) {
            return <p>No hay datos disponibles</p>
        }

        const columns = Object.keys(data[0])
        return (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                    <tr style={{ backgroundColor: '#f0f0f0' }}>
                        {columns.map(col => (
                            <th key={col} style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>
                                {col}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {data.map((row, idx) => (
                        <tr key={idx}>
                            {columns.map(col => (
                                <td key={`${idx}-${col}`} style={{ border: '1px solid #ddd', padding: '8px' }}>
                                    {typeof row[col] === 'number' ? row[col].toFixed(2) : row[col]}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        )
    }

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

            <div className="contenido" style={{ padding: '20px', display: 'flex', gap: '20px' }}>
                {/* Sidebar con lista de reportes */}
                <div style={{
                    width: '250px',
                    backgroundColor: 'white',
                    padding: '15px',
                    borderRadius: '4px',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                    height: 'fit-content'
                }}>
                    <h3 style={{ marginTop: 0 }}>Reportes Disponibles</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        {reportsList.map(report => (
                            <button
                                key={report.key}
                                onClick={() => setSelectedReport(report.key)}
                                style={{
                                    padding: '10px',
                                    textAlign: 'left',
                                    border: 'none',
                                    borderRadius: '4px',
                                    cursor: 'pointer',
                                    backgroundColor: selectedReport === report.key ? '#007bff' : '#f0f0f0',
                                    color: selectedReport === report.key ? 'white' : 'black',
                                    transition: '0.3s',
                                    fontSize: '14px'
                                }}
                            >
                                {report.label}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Contenido principal */}
                <div style={{
                    flex: 1,
                    backgroundColor: 'white',
                    padding: '20px',
                    borderRadius: '4px',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                }}>
                    <h2 style={{ marginTop: 0, color: '#333' }}>
                        {currentReport?.label}
                    </h2>

                    {loading ? (
                        <p style={{ color: '#666' }}>Cargando datos...</p>
                    ) : (
                        <div>
                            {renderTable(currentData)}
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}