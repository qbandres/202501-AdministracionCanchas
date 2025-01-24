from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.canchas import Cancha
from app.schemas.canchas import CanchaCreate, CanchaResponse

router = APIRouter()

# Crear una cancha
@router.post("/", response_model=CanchaResponse)
def crear_cancha(cancha: CanchaCreate, db: Session = Depends(get_db)):
    nueva_cancha = Cancha(nombre=cancha.nombre, ubicacion=cancha.ubicacion)
    db.add(nueva_cancha)
    db.commit()
    db.refresh(nueva_cancha)
    return nueva_cancha

# Leer todas las canchas
@router.get("/", response_model=list[CanchaResponse])
def listar_canchas(db: Session = Depends(get_db)):
    canchas = db.query(Cancha).all()
    return canchas

# Actualizar una cancha
@router.put("/{id}", response_model=CanchaResponse)
def actualizar_cancha(id: int, cancha: CanchaCreate, db: Session = Depends(get_db)):
    cancha_existente = db.query(Cancha).filter(Cancha.id == id).first()
    if not cancha_existente:
        raise HTTPException(status_code=404, detail="Cancha no encontrada")
    cancha_existente.nombre = cancha.nombre
    cancha_existente.ubicacion = cancha.ubicacion
    db.commit()
    db.refresh(cancha_existente)
    return cancha_existente

# Eliminar una cancha
@router.delete("/{id}")
def eliminar_cancha(id: int, db: Session = Depends(get_db)):
    cancha = db.query(Cancha).filter(Cancha.id == id).first()
    if not cancha:
        raise HTTPException(status_code=404, detail="Cancha no encontrada")
    db.delete(cancha)
    db.commit()
    return {"message": "Cancha eliminada correctamente"}