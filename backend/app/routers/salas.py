from fastapi import APIRouter
from app.database import get_connection
from app.models.salas import EdificiosResponse

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
