import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, HTTPException, status
from mysql.connector import Error
from datetime import date, timedelta

app = FastAPI()

# Configurar CORS : hace falta para que el frontend pueda acceder a la API, por defecto solo se permite el puerto 8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Puerto del docker donde corre el front, cambiar si hace falta
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="reservas_ucu"
    )


# Instala esto si no lo tienes: pip install email-validator

class LoginRequest(BaseModel):
    email: EmailStr  # Requiere email-validator
    password: str


class LoginResponse(BaseModel):
    message: str
    token: str
    user: dict


@app.post("/login", response_model=LoginResponse)
def login_user(credentials: LoginRequest):
    conn = None
    cursor = None


# CONSULTAR SANCIONES DE UN USUARIO
@app.get("/sanciones/{ci_participante}")
def get_sanciones(ci_participante: str):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT fecha_inicio, fecha_fin
            FROM sancion_participante
            WHERE ci_participante = %s
            ORDER BY fecha_inicio DESC;
        """, (ci_participante,))
        sanciones = cursor.fetchall()
        if not sanciones:
            return {"message": "El usuario no tiene sanciones registradas"}

        return {"sanciones": sanciones}

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



# CONTROL AUTOMÁTICO DE SANCIONES (por inasistencia)
@app.post("/control_sanciones")
def control_sanciones():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Buscar reservas finalizadas ayer
        ayer = date.today() - timedelta(days=1)
        cursor.execute("""
            SELECT id_reserva FROM reserva
            WHERE fecha = %s AND estado = 'finalizada';
        """, (ayer,))
        reservas = cursor.fetchall()

        sancionados = []

        for r in reservas:
            # Verificar si nadie asistió
            cursor.execute("""
                SELECT COUNT(*) AS asistentes
                FROM reserva_participante
                WHERE id_reserva = %s AND asistencia = TRUE;
            """, (r["id_reserva"],))
            asistentes = cursor.fetchone()["asistentes"]

            if asistentes == 0:
                # Marcar reserva como sin asistencia
                cursor.execute("""
                    UPDATE reserva SET estado = 'sin_asistencia' WHERE id_reserva = %s;
                """, (r["id_reserva"],))
                conn.commit()

                # Sancionar a todos los participantes de esa reserva
                cursor.execute("""
                    SELECT ci_participante
                    FROM reserva_participante
                    WHERE id_reserva = %s;
                """, (r["id_reserva"],))
                participantes = cursor.fetchall()

                for p in participantes:
                    inicio = date.today()
                    fin = inicio + timedelta(days=60)

                    cursor.execute("""
                        INSERT INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin)
                        VALUES (%s, %s, %s);
                    """, (p["ci_participante"], inicio, fin))
                    sancionados.append(p["ci_participante"])
                conn.commit()

        if len(sancionados) == 0:
            return {"message": "No se aplicaron sanciones hoy"}
        else:
            return {"message": "Sanciones aplicadas a", "usuarios": sancionados}

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# VALIDAR SI UN USUARIO TIENE SANCIONES ACTIVAS
@app.get("/validar_sancion/{ci_participante}")
def validar_sancion(ci_participante: str):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        hoy = date.today()

        cursor.execute("""
            SELECT COUNT(*) AS activas
            FROM sancion_participante
            WHERE ci_participante = %s
            AND %s BETWEEN fecha_inicio AND fecha_fin;
        """, (ci_participante, hoy))

        resultado = cursor.fetchone()["activas"]

        if resultado > 0:
            return {"bloqueado": True, "message": "El usuario tiene una sanción activa y no puede realizar reservas"}
        else:
            return {"bloqueado": False, "message": "El usuario no tiene sanciones activas"}

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
