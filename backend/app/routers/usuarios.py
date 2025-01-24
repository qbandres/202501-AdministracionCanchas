from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCreate, UsuarioResponse

router = APIRouter()

# Crear un usuario
@router.post("/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Validar que el correo o teléfono no estén duplicados
    if db.query(Usuario).filter((Usuario.correo == usuario.correo) | (Usuario.telefono == usuario.telefono)).first():
        raise HTTPException(status_code=400, detail="El correo o teléfono ya están registrados")
    
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        telefono=usuario.telefono,
        correo=usuario.correo,
        password=usuario.password,
        rol=usuario.rol
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# Listar todos los usuarios
@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return usuarios

# Actualizar un usuario
@router.put("/{id}", response_model=UsuarioResponse)
def actualizar_usuario(id: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario_existente.nombre = usuario.nombre
    usuario_existente.telefono = usuario.telefono
    usuario_existente.correo = usuario.correo
    usuario_existente.password = usuario.password
    usuario_existente.rol = usuario.rol
    db.commit()
    db.refresh(usuario_existente)
    return usuario_existente

# Eliminar un usuario
@router.delete("/{id}")
def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado correctamente"}

@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).order_by(Usuario.nombre).all()
    return usuarios