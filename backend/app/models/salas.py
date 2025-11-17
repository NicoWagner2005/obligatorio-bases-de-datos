from pydantic import BaseModel
from typing import List

class Sala(BaseModel):
    id_sala: int
    nombre_sala: str
    capacidad: int
    tipo_sala: str

class Edificio(BaseModel):
    id_edificio: int
    nombre_edificio: str
    salas: List[Sala]

class EdificiosResponse(BaseModel):
    edificios: List[Edificio]
