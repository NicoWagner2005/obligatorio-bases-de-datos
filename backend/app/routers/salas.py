from fastapi import APIRouter
from app.database import get_connection
from app.models.salas import EdificiosResponse
from app.models.salas import ReservaResponse
from app.models.salas import Reserva
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
        cursor.close()
        conn.close()


@router.post('/reservar', response_model=ReservaResponse)
def reservar_sala(datos_reserva : Reserva):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO reserva(id_sala, fecha, id_turno, estado)
               VALUES (%s, %s, %s, %s)""",
            (datos_reserva.id_sala, datos_reserva.fecha, datos_reserva.id_turno, datos_reserva.estado.value)
        )
        conn.commit()


        id_reserva = cursor.lastrowid

        return {
            "message": "Reserva creada exitosamente",
            "id_reserva": id_reserva,
            "estado": datos_reserva.estado.value
        }

    finally:
        cursor.close()
        conn.close()
