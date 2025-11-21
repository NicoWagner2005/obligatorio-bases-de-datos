from fastapi import APIRouter, HTTPException, status
from app.database import get_connection, close_connection
from app.models.auth import RegistrationCredentials, RegistrationResponse, LoginResponse, LoginCredentials
from app.utils.hash import hash_password
import bcrypt

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post('/register', response_model=RegistrationResponse)
def register_user(credentials: RegistrationCredentials):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 1️⃣ Verificar si ya existe el correo
        cursor.execute(
            "SELECT * FROM participante WHERE email = %s",
            (credentials.email,)
        )
        user = cursor.fetchone()

        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Usuario ya registrado"
            )

        # 2️⃣ Hashear contraseña
        hashed_password = hash_password(credentials.password)

        # 3️⃣ Crear login → genera user_id
        cursor.execute(
            "INSERT INTO login (contrasena) VALUES (%s)",
            (hashed_password,)
        )
        user_id = cursor.lastrowid

        # 4️⃣ Crear participante vinculado al user_id
        cursor.execute(
            """INSERT INTO participante (ci, nombre, apellido, email, user_id)
               VALUES (%s, %s, %s, %s, %s)""",
            (credentials.ci, credentials.name, credentials.surname, credentials.email, user_id)
        )

        conn.commit()

        return {"message": "Usuario registrado exitosamente"}

    finally:
        close_connection(cursor, conn)


@router.post("/login", response_model=LoginResponse)
def login_user(credentials: LoginCredentials):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 1️⃣ Buscar participante por email
        cursor.execute(
            "SELECT user_id, ci, nombre, apellido FROM participante WHERE email = %s",
            (credentials.email,)
        )
        participante = cursor.fetchone()

        if not participante:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos"
            )

        # 2️⃣ Buscar hash de contraseña
        cursor.execute(
            "SELECT contrasena FROM login WHERE user_id = %s",
            (participante["user_id"],)
        )
        login_data = cursor.fetchone()

        if not login_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos"
            )

        # 3️⃣ Verificar contraseña
        if not bcrypt.checkpw(credentials.password.encode(), login_data["contrasena"].encode()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos"
            )

        # 4️⃣ Login OK
        return {
            "message": "Login exitoso",
            "user_id": participante["user_id"],
        }

    finally:
        close_connection(cursor, conn)
