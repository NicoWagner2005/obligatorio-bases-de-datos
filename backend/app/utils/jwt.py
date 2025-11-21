import base64
import hashlib
import hmac
import json
import os
import time
from typing import Dict

from fastapi import Header, HTTPException, status


SECRET_KEY = os.getenv("JWT_SECRET", "change_me")
ALGORITHM = "HS256"


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def create_access_token(data: Dict, expires_minutes: int = 60) -> str:
    payload = data.copy()
    payload["exp"] = int(time.time()) + expires_minutes * 60

    header = {"alg": ALGORITHM, "typ": "JWT"}

    header_b64 = _b64encode(json.dumps(header, separators=(",", ":")).encode())
    payload_b64 = _b64encode(json.dumps(payload, separators=(",", ":")).encode())

    signing_input = f"{header_b64}.{payload_b64}".encode()
    signature = hmac.new(SECRET_KEY.encode(), signing_input, hashlib.sha256).digest()
    signature_b64 = _b64encode(signature)

    return f"{header_b64}.{payload_b64}.{signature_b64}"


def decode_token(token: str) -> Dict:
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
    except ValueError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token inválido")

    signing_input = f"{header_b64}.{payload_b64}".encode()
    expected_signature = hmac.new(SECRET_KEY.encode(), signing_input, hashlib.sha256).digest()
    actual_signature = _b64decode(signature_b64)

    if not hmac.compare_digest(expected_signature, actual_signature):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Firma inválida")

    try:
        payload = json.loads(_b64decode(payload_b64))
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Payload inválido")

    if payload.get("exp") is None or int(time.time()) > int(payload["exp"]):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expirado")

    return payload


def require_admin(authorization: str = Header(None)) -> Dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Falta el token de autorización")

    token = authorization.split(" ", 1)[1]
    payload = decode_token(token)

    if payload.get("role") != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Se requieren privilegios de administrador")

    return payload
