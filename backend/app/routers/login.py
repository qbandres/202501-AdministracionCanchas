from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuarios import Usuario
from app.schemas.usuarios import LoginRequest, LoginResponse

router = APIRouter()

@router.post("/", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Buscar el usuario por correo
    usuario = db.query(Usuario).filter(Usuario.correo == request.correo).first()

    # Validar credenciales
    if not usuario or usuario.password != request.password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # Devolver la información del usuario
    return {"id": usuario.id, "nombre": usuario.nombre, "rol": usuario.rol}