from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class ParticipanteCreate(BaseModel):
    ci: str
    nombre: str
    apellido: str
    email: str
    password: str
    id_programa: int
    rol: str


class ParticipanteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    id_programa: Optional[int] = None
    rol: Optional[str] = None


class SalaCreate(BaseModel):
    nombre_sala: str
    id_edificio: int
    capacidad: int
    tipo_sala: str


class SalaUpdate(BaseModel):
    nombre_sala: Optional[str] = None
    id_edificio: Optional[int] = None
    capacidad: Optional[int] = None
    tipo_sala: Optional[str] = None


class ReservaCreate(BaseModel):
    id_sala: int
    fecha: date
    id_turno: int
    participantes: List[str]


class ReservaUpdate(BaseModel):
    id_sala: Optional[int] = None
    fecha: Optional[date] = None
    id_turno: Optional[int] = None
    participantes: Optional[List[str]] = None


class AsistenciaRegistro(BaseModel):
    ci_participante: str
    asistencia: bool


class AsistenciaPayload(BaseModel):
    registros: List[AsistenciaRegistro]


class SancionCreate(BaseModel):
    ci_participante: str
    fecha_inicio: date
    fecha_fin: date


class SancionUpdate(BaseModel):
    ci_participante: str
    fecha_inicio: date
    nueva_fecha_fin: date

