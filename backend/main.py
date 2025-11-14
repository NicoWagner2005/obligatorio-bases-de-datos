import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, HTTPException, status

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

@app.get("/")
def read_root():
    return {"Hello": "World"}


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

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM login WHERE correo = %s AND contrasena = %s"
        cursor.execute(query, (credentials.email, credentials.password))
        user = cursor.fetchone() # recupera solo una fila

        if not user:
            # ✅ 401 para credenciales incorrectas
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos"
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
# logica de reservas

# creo que lo mejor es que por defecto esten las salas agrupadas por edificio
