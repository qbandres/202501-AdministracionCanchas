from pydantic import BaseModel
from datetime import date, time

class ReservaBase(BaseModel):
    usuario_id: int
    cancha_id: int
    fecha_reserva: date  # Cambiado a date
    hora_inicio: time    # Cambiado a time
    hora_fin: time       # Cambiado a time

class ReservaCreate(ReservaBase):
    pass

class ReservaResponse(ReservaBase):
    id: int
    estado: str

    class Config:
        orm_mode = True