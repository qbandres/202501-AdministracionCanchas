from pydantic import BaseModel, EmailStr

class UsuarioBase(BaseModel):
    nombre: str
    telefono: str
    correo: EmailStr
    rol: str = "usuario"

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        orm_mode = True

# Clase para manejar las solicitudes de login
class LoginRequest(BaseModel):
    correo: EmailStr
    password: str

# Clase para manejar las respuestas de login
class LoginResponse(BaseModel):
    id: int
    nombre: str
    rol: str

    class Config:
        orm_mode = True