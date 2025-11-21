from fastapi import Header, HTTPException, Depends
from jose import jwt, JWTError
import time

SECRET = "supersecret"
ALGORITHM = "HS256"


# -------------------------------
# CREAR TOKEN
# -------------------------------
def create_access_token(data: dict, expires_minutes: int = 60):
    """
    Crea un JWT con expiración en minutos.
    'data' debe ser un diccionario serializable con user_id, email, admin, etc.
    """
    to_encode = data.copy()
    expire = int(time.time()) + expires_minutes * 60
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return token


# -------------------------------
# DECODIFICAR TOKEN
# -------------------------------
def decode_token(token: str):
    return jwt.decode(token, SECRET, algorithms=[ALGORITHM])


# -------------------------------
# OBTENER USUARIO DESDE TOKEN
# -------------------------------
def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401, "Falta token")

    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Formato de token inválido")

    token = authorization.split(" ")[1]

    try:
        return decode_token(token)
    except JWTError:
        raise HTTPException(401, "Token inválido o expirado")


# -------------------------------
# SOLO ADMIN
# -------------------------------
def require_admin(user=Depends(get_current_user)):
    if not user.get("admin", False):  # flag de admin dentro del token
        raise HTTPException(403, "Solo administradores")
    return user
