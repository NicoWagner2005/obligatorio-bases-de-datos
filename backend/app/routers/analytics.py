from fastapi import APIRouter
from app.database import get_connection

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("salas-mas-reservadas")
def get_sala_mas_reservada():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
                SELECT s.nombre_sala, r.total_reservas
                FROM sala s
                JOIN (
                    SELECT id_sala, COUNT(*) AS total_reservas
                    FROM reserva
                    GROUP BY id_sala
                    ORDER BY total_reservas DESC
                    LIMIT 3
                ) AS r
                ON s.id_sala = r.id_sala
                ORDER BY r.total_reservas DESC;
            """
        )

    finally:
        cursor.close()
        conn.close()


@router.get("/turnos-mas-demandados")
def get_turnos_mas_demandados():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
                SELECT t.hora_inicio, r.total_reservas
                FROM turno t
                JOIN (
                    SELECT id_turno, COUNT(*) as total_reservas
                    FROM reserva
                    GROUP BY id_turno
                    ORDER BY total_reservas DESC
                    LIMIT 3
                ) AS r
                ON t.id_turno = r.id_turno
                ORDER BY r.total_reservas DESC;
            """
        )

    finally:
        cursor.close()
        conn.close()

@router.get("/promedio-participantes-sala")
def get_promedio_participantes_sala():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
                SELECT
                    s.nombre_sala,
                    AVG(CASE
                            WHEN rp.asistencia IS NOT NULL THEN rp.asistencia
                            ELSE 0
                        END) AS promedio_asistencia
                FROM sala s
                JOIN reserva r ON s.id_sala = r.id_sala
                JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
                GROUP BY s.nombre_sala
                ORDER BY promedio_asistencia DESC
                LIMIT 3
            """
        )

    finally:
        cursor.close()
        conn.close()

@router.get("/cantidad-reservas-carrera-y-facultad")
def get_cantidad_reservas_por_carrera_y_facultad():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
                SELECT f.nombre as facultad, pa.nombre_programa as carrera, COUNT(r.id_reserva) as cantidad
                FROM reserva r JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
                JOIN participante_programa_academico ppa ON ppa.ci_participante = rp.ci_participante
                JOIN programa_academico pa ON pa.id_programa = ppa.id_programa
                JOIN facultad f ON pa.id_facultad = f.id_facultad
                GROUP BY f.nombre, pa.nombre_programa
            """
        )

    finally:
        cursor.close()
        conn.close()


@router.get("/porcentaje-ocupacion-salas-edificio")
def get_porcentaje_ocupacion_sala_por_edificio():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
                SELECT
                    e.nombre_edificio,
                    ROUND(
                        (COUNT(DISTINCT r.id_sala) / COUNT(DISTINCT s.id_sala)) * 100,
                        2
                    ) AS porcentaje_ocupacion
                FROM edificio e
                JOIN sala s
                    ON s.id_edificio = e.id_edificio
                LEFT JOIN reserva r
                    ON r.id_sala = s.id_sala
                GROUP BY
                    e.nombre_edificio;
            """
        )

    finally:
        cursor.close()
        conn.close()
