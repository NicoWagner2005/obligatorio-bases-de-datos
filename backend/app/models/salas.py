from pydantic import BaseModel
from typing import List
from enum import Enum



class Sala(BaseModel):
    id_sala: int
    nombre_sala: str
    capacidad: int
    tipo_sala: str

class ReservaResponse(BaseModel):
    message: str
    id_reserva: int
    estado: str

class EstadoReserva(str, Enum):
    activa = "activa"
    cancelada = "cancelada"
    finalizada = "finalizada"

class Reserva(BaseModel):
    id_sala: int
    fecha: str
    id_turno: int
    ci_participante: str


class Edificio(BaseModel):
    id_edificio: int
    nombre_edificio: str
    salas: List[Sala]

class EdificiosResponse(BaseModel):
    edificios: List[Edificio]

class AsistenciaResponse(BaseModel):
    message: str

class AsistenciaRequest(BaseModel):
    id_reserva: int