from typing import Any, Dict
from mysql.connector import Error
from datetime import date, timedelta
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, HTTPException, status
import bcrypt

"""
pip install 
    - email-validator
    - mysql-connector-python
    - fastapi
    - bcrypt
"""
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


# ============== LOGIN Y REGISTRO =================
def hash_password(password):
    hashed = bcrypt.hashpw(password, bcrypt.gensalt(14))
    return hashed


class Credentials(BaseModel):
    email: EmailStr  # Requiere email-validator
    password: str




class RegisterResponse(BaseModel):
    message: str

@app.post('/register', response_model=RegisterResponse)
def register_user(credentials: Credentials):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM login WHERE correo = %s", (credentials.email,))
        user: Dict[str, Any] | None = cursor.fetchone()

        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Usuario ya registrado"
            )

        hashed_password = hash_password(credentials.password.encode())

        cursor.execute("INSERT INTO login (correo, contrasena) VALUES (%s, %s)", (credentials.email, hashed_password))
        conn.commit()

        return {"message": "Usuario registrado exitosamente"}

    finally:
        cursor.close()
        conn.close()



class LoginResponse(BaseModel):
    message: str
    token: str
    user: dict
@app.post("/login", response_model=LoginResponse)
def login_user(credentials: Credentials):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM login WHERE correo = %s", (credentials.email,))
        user: Dict[str, Any] | None = cursor.fetchone()

        if not user or not bcrypt.checkpw(credentials.password.encode(), user["contrasena"].encode()):
            # ✅ 401 para credenciales incorrectas
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos"
            )

        # ✅ 200 automático al retornar exitosamente
        return {
            "message": "Login exitoso",
            "token": "jwt_token_aqui",
            "user": user
        }

    finally:
        cursor.close()
        conn.close()

class SalasResponse(BaseModel):
    salas: list
    edificios: list

# q muestre todas las reservas, disponibles y no disponibles, asi lo usuarios pueden ver si esperan a que quede libre la sala que quieren

# ================== RESERVAR SALA ===============
@app.get("/reservarsala")
# creo que lo mejor es que por defecto esten las salas agrupadas por edificio
def get_all_salas():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # JOIN salas + edificios
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

        # Agrupar por edificio
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
        if cursor: cursor.close()
        if conn: conn.close()


# TODO: filtro para mostrar solo las reservas disponibles

# ============ SANCIONES ===============


# ============================================================
#   1) CONSULTAR SANCIONES DE UN USUARIO
# ============================================================
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
            return {"message": "El usuario no tiene sanciones"}

        return {"sanciones": sanciones}

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# ============================================================
#   2) VALIDAR SI UN USUARIO TIENE SANCIÓN ACTIVA
# ============================================================
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

        activas = cursor.fetchone()["activas"]

        return {
            "bloqueado": activas > 0,
            "message": "Sanción activa" if activas > 0 else "Sin sanciones activas"
        }

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# ============================================================
#   3) CREAR SANCION MANUAL (ALTA)
# ============================================================
@app.post("/sanciones/crear")
def crear_sancion(ci_participante: str, fecha_inicio: date, fecha_fin: date):
    try:
        if fecha_fin <= fecha_inicio:
            raise HTTPException(400, "La fecha fin debe ser mayor a fecha inicio")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin)
            VALUES (%s, %s, %s);
        """, (ci_participante, fecha_inicio, fecha_fin))

        conn.commit()
        return {"message": "Sanción creada correctamente"}

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# ============================================================
#   4) BORRAR SANCION (BAJA)
# ============================================================
@app.delete("/sanciones/{ci}/{fecha_inicio}")
def borrar_sancion(ci: str, fecha_inicio: date):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM sancion_participante
            WHERE ci_participante = %s AND fecha_inicio = %s;
        """, (ci, fecha_inicio))

        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(404, "Sanción no encontrada")

        return {"message": "Sanción eliminada"}

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# ============================================================
#   5) MODIFICAR SANCION (MODIFICACIÓN)
# ============================================================
@app.put("/sanciones/modificar")
def modificar_sancion(ci_participante: str, fecha_inicio: date, nueva_fecha_fin: date):
    try:
        if nueva_fecha_fin <= fecha_inicio:
            raise HTTPException(400, "La nueva fecha fin debe ser mayor a fecha inicio")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE sancion_participante
            SET fecha_fin = %s
            WHERE ci_participante = %s AND fecha_inicio = %s;
        """, (nueva_fecha_fin, ci_participante, fecha_inicio))

        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(404, "Sanción no encontrada")

        return {"message": "Sanción modificada correctamente"}

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
