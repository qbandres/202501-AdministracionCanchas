from pydantic import BaseModel

class CanchaBase(BaseModel):
    nombre: str
    ubicacion: str | None = None

class CanchaCreate(CanchaBase):
    pass

class CanchaResponse(CanchaBase):
    id: int

    class Config:
        orm_mode = True