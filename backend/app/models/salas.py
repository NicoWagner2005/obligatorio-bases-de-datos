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

class EstadoReserva(str, Enum):
    activa = "activa"
    cancelada = "cancelada"
    finalizada = "finalizada"

class Reserva(BaseModel):
    id_sala: int
    fecha: str
    id_turno: int
    estado: EstadoReserva


class Edificio(BaseModel):
    id_edificio: int
    nombre_edificio: str
    salas: List[Sala]

class EdificiosResponse(BaseModel):
    edificios: List[Edificio]
