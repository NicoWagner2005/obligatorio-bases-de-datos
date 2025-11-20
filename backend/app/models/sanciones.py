from pydantic import BaseModel
from datetime import date

class Sancion(BaseModel):
    fecha_inicio: date
    fecha_fin: date
