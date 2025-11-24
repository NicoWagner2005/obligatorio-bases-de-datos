from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from mysql.connector import IntegrityError, Error
from datetime import date
from ..database import close_connection, get_connection
from ..models.salas import (
    AsistenciaRequest,
    AsistenciaResponse,
    EdificiosResponse,
    Reserva,
    ReservaResponse,
)
from ..utils.jwt import get_current_user
router = APIRouter(prefix="/salas", tags=["Salas"])


@router.get("/", response_model=EdificiosResponse)
def get_salas():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
                       SELECT e.id_edificio,
                              e.nombre_edificio,
                              s.id_sala,
                              s.nombre_sala,
                              s.capacidad,
                              s.tipo_sala
                       FROM sala s
                                JOIN edificio e ON s.id_edificio = e.id_edificio
                       ORDER BY e.id_edificio;
                       """)

        rows = cursor.fetchall()
        edificios = {}

        for row in rows:
            eid = row["id_edificio"]

            if eid not in edificios:
                edificios[eid] = {
                    "id_edificio": eid,
                    "nombre_edificio": row["nombre_edificio"],
                    "salas": []
                }

            edificios[eid]["salas"].append({
                "id_sala": row["id_sala"],
                "nombre_sala": row["nombre_sala"],
                "capacidad": row["capacidad"],
                "tipo_sala": row["tipo_sala"]
            })

        return {"edificios": list(edificios.values())}

    finally:
        close_connection(cursor, conn)


@router.post("/reservar", response_model=ReservaResponse)
def reservar_sala(datos_reserva: Reserva):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 0️⃣ Verificar que el turno exista
        cursor.execute("SELECT * FROM turno WHERE id_turno = %s", (datos_reserva.id_turno,))
        turno_row = cursor.fetchone()
        if not turno_row:
            raise HTTPException(404, "El turno no existe")

        # 1️⃣ Obtener CI del participante
        cursor.execute("SELECT ci FROM participante WHERE user_id = %s", (datos_reserva.user_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(404, "Usuario no encontrado")
        ci_participante = row["ci"]

        # 2️⃣ Límite de 3 reservas activas
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM reserva r
            JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
            WHERE rp.ci_participante = %s AND r.estado = 'activa'
        """, (ci_participante,))
        if cursor.fetchone()["total"] >= 3:
            raise HTTPException(429, "El usuario ya tiene 3 reservas activas")

        # 3️⃣ Obtener sala
        cursor.execute("SELECT * FROM sala WHERE id_sala = %s", (datos_reserva.id_sala,))
        sala = cursor.fetchone()
        if sala is None:
            raise HTTPException(404, "La sala no existe")

        # 4️⃣ Rol del participante
        cursor.execute("""
            SELECT rol FROM participante_programa_academico
            WHERE ci_participante = %s
        """, (ci_participante,))
        participante = cursor.fetchone()
        if participante is None:
            raise HTTPException(404, "Participante no encontrado")

        rol = participante["rol"]

        # reglas de salas exclusivas
        if sala["tipo_sala"] != "libre" and rol == "estudiante":
            raise HTTPException(403, "Los estudiantes no pueden reservar salas exclusivas")

        # 5️⃣ Insertar reserva
        cursor.execute("""
            INSERT INTO reserva(id_sala, fecha, id_turno, estado)
            VALUES (%s, %s, %s, %s)
        """, (datos_reserva.id_sala, datos_reserva.fecha, datos_reserva.id_turno, "activa"))

        id_reserva = cursor.lastrowid

        # 6️⃣ Insertar participante
        cursor.execute("""
            INSERT INTO reserva_participante(id_reserva, fecha_solicitud_reserva, ci_participante)
            VALUES (%s, %s, %s)
        """, (id_reserva, date.today(), ci_participante))

        conn.commit()

        return {
            "message": "Reserva creada exitosamente",
            "id_reserva": id_reserva,
            "estado": "activa"
        }

    finally:
        close_connection(cursor, conn)



@router.get("/mis-reservas")
def get_mis_reservas(user_id: Optional[int] = None, user = Depends(get_current_user)):
    resolved_user_id = user_id if user_id is not None else user["user_id"]  # solo esto viene en el token

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 1️⃣ Obtener la CI real usando el user_id
        cursor.execute("SELECT ci FROM participante WHERE user_id = %s", (resolved_user_id,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(404, "Usuario no encontrado")

        ci_participante = row["ci"]

        # 2️⃣ Obtener las reservas asociadas a esa CI
        cursor.execute("""
            SELECT *
            FROM reserva r 
            JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
            WHERE rp.ci_participante = %s
        """, (ci_participante,))

        reservas = cursor.fetchall()

        return {"reservas": reservas}

    finally:
        close_connection(cursor, conn)


@router.put("/asistir", response_model=AsistenciaResponse)
def marcar_asistencia(reserva: AsistenciaRequest):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
                SELECT asistencia FROM reserva_participante
                WHERE id_reserva = %s
            """, (reserva.id_reserva,)
        )

        asistencia_row = cursor.fetchone()

        if asistencia_row is None:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")

        cursor.execute(
            """
                SELECT s.capacidad
                FROM sala s JOIN reserva r ON s.id_sala = r.id_sala
                WHERE r.id_reserva = %s
            """, (reserva.id_reserva,)
        )
        capacidad_row = cursor.fetchone()

        if capacidad_row is None:
            raise HTTPException(status_code=404, detail="Sala no encontrada para la reserva")

        capacidad = capacidad_row["capacidad"]
        asistencia = asistencia_row["asistencia"] or 0

        if asistencia + 1 > capacidad:
            raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, detail="La cantidad de participantes excede la capacidad de la sala")

        cursor.execute(
            """
            UPDATE reserva_participante
            SET asistencia = asistencia + 1
            WHERE id_reserva = %s
            """, (reserva.id_reserva,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")

        conn.commit()

        return {"message": "Asistencia marcada exitosamente"}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(cursor, conn)

