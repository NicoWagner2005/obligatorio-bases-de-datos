from fastapi import APIRouter, HTTPException, status
from mysql.connector import IntegrityError, Error
from datetime import date
from app.database import get_connection, close_connection
from app.models.salas import EdificiosResponse, ReservaResponse, Reserva, AsistenciaResponse, AsistenciaRequest
router = APIRouter(prefix="/salas", tags=["Salas"])


@router.get("/", response_model=EdificiosResponse)
def get_salas():

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
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 1) Verificar límite de 3 reservas activas del participante
        cursor.execute("""
                       SELECT COUNT(*) AS total
                       FROM reserva_participante rp
                                JOIN reserva r ON rp.id_reserva = r.id_reserva
                       WHERE rp.ci_participante = %s
                         AND r.estado = 'activa'
                       """, (datos_reserva.ci_participante,))

        total_reservas = cursor.fetchone()["total"]

        if total_reservas >= 3:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="El usuario ya tiene 3 reservas activas"
            )

        # 2) Obtener sala
        cursor.execute("""SELECT *
                          FROM sala
                          WHERE id_sala = %s""",
                       (datos_reserva.id_sala,))
        sala = cursor.fetchone()

        if sala is None:
            raise HTTPException(404, "La sala no existe")

        tipo_sala = sala["tipo_sala"]



        # 4) Obtener rol del participante
        cursor.execute("""
                       SELECT rol
                       FROM participante_programa_academico
                       WHERE ci_participante = %s
                       """, (datos_reserva.ci_participante,))

        participante = cursor.fetchone()

        if participante is None:
            raise HTTPException(404, "El participante no existe")

        rol = participante["rol"]

        # Regla: estudiantes no pueden reservar salas exclusivas
        if tipo_sala != "libre" and rol == "estudiante":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Los estudiantes no pueden reservar salas exclusivas"
            )

        # Chequear máximo de 2 reservas activas por sala/día
        cursor.execute("""
                       SELECT COUNT(*) AS total
                       FROM reserva
                       WHERE id_sala = %s
                         AND fecha = %s
                         AND estado = 'activa'
                       """, (datos_reserva.id_sala, datos_reserva.fecha))

        cantidad = cursor.fetchone()["total"]

        if cantidad >= 2 and rol == "estudiante":
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Esta sala ya tiene 2 reservas activas para este día"
            )

        # 5) Insertar reserva (UNIQUE en la base de datos controla disponibilidad)
        cursor.execute("""
                       INSERT INTO reserva(id_sala, fecha, id_turno, estado)
                       VALUES (%s, %s, %s, %s)
                       """, (datos_reserva.id_sala, datos_reserva.fecha, datos_reserva.id_turno, "activa"))

        id_reserva = cursor.lastrowid

        # 6) Insertar relación participante-reserva con fecha actual
        cursor.execute("""
                       INSERT INTO reserva_participante(id_reserva, fecha_solicitud_reserva, ci_participante)
                       VALUES (%s, %s, %s)
                       """, (id_reserva, date.today(), datos_reserva.ci_participante))

        conn.commit()

        return {
            "message": "Reserva creada exitosamente",
            "id_reserva": id_reserva,
            "estado": "activa"
        }

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="La sala ya está reservada en ese horario"
        )

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

        cursor.execute(
            """
                SELECT s.capacidad
                FROM sala s JOIN reserva r ON s.id_sala = r.id_sala
                WHERE r.id_reserva = %s
            """, (reserva.id_reserva,)
        )
        capacidad = cursor.fetchone()["capacidad"]

        asistencia = cursor.fetchone()["asistencia"]

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

