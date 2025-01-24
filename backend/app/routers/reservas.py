from fastapi import APIRouter, HTTPException, Depends, Request, Query
from sqlalchemy.orm import Session
from datetime import date, time, datetime, timedelta, datetime as dt
from app.database import get_db
from app.models.reservas import Reserva
from app.models.canchas import Cancha
from app.models.usuarios import Usuario
from app.schemas.reservas import ReservaCreate, ReservaResponse
from sqlalchemy.sql import cast
from sqlalchemy import Time
from typing import Optional

router = APIRouter()

# Crear una reserva
@router.post("/", response_model=ReservaResponse)
def crear_reserva(
    reserva: ReservaCreate, 
    db: Session = Depends(get_db), 
    admin: bool = Query(False)
):
    # Validar que el usuario existe
    usuario = db.query(Usuario).filter(Usuario.id == reserva.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Validar que la cancha existe
    cancha = db.query(Cancha).filter(Cancha.id == reserva.cancha_id).first()
    if not cancha:
        raise HTTPException(status_code=404, detail="Cancha no encontrada")

    # Validar que el horario está dentro del rango permitido (7:00 AM a 11:00 PM)
    horario_apertura = time(7, 0)  # 7:00 AM
    horario_cierre = time(23, 0)   # 11:00 PM

    if not (horario_apertura <= reserva.hora_inicio <= horario_cierre and 
            horario_apertura <= reserva.hora_fin <= horario_cierre):
        raise HTTPException(
            status_code=400, 
            detail="El horario debe estar entre las 7:00 AM y las 11:00 PM"
        )

    # Validaciones adicionales para usuarios no administradores
    if not admin:
        # Validar solapamiento de horarios
        solapamiento = db.query(Reserva).filter(
            Reserva.cancha_id == reserva.cancha_id,
            Reserva.fecha_reserva == reserva.fecha_reserva,
            Reserva.hora_inicio < cast(reserva.hora_fin, Time),
            Reserva.hora_fin > cast(reserva.hora_inicio, Time)
        ).first()

        if solapamiento:
            raise HTTPException(status_code=400, detail="El horario ya está reservado")

        # Validar que el usuario no tiene otra reserva en el mismo día
        reserva_existente = db.query(Reserva).filter(
            Reserva.usuario_id == reserva.usuario_id,
            Reserva.fecha_reserva == reserva.fecha_reserva
        ).first()

        if reserva_existente:
            raise HTTPException(
                status_code=400,
                detail="El usuario ya tiene una reserva para este día"
            )

    # Crear nueva reserva
    nueva_reserva = Reserva(
        usuario_id=reserva.usuario_id,
        cancha_id=reserva.cancha_id,
        fecha_reserva=reserva.fecha_reserva,
        hora_inicio=reserva.hora_inicio,
        hora_fin=reserva.hora_fin,
        estado="confirmada"
    )
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)
    return nueva_reserva

# Listar reservas por usuario o todas las reservas
@router.get("/", response_model=list[ReservaResponse])
def listar_reservas(
    usuario_id: Optional[int] = Query(None),
    cancha_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    # Consulta inicial
    query = db.query(Reserva)

    # Aplicar filtros si se proporcionan
    if usuario_id:
        query = query.filter(Reserva.usuario_id == usuario_id)
    if cancha_id:
        query = query.filter(Reserva.cancha_id == cancha_id)

    # Ordenar por cancha, fecha y hora
    reservas = query.order_by(Reserva.cancha_id, Reserva.fecha_reserva, Reserva.hora_inicio).all()
    return reservas

# Actualizar una reserva
@router.put("/{id}", response_model=ReservaResponse)
def actualizar_reserva(id: int, reserva: ReservaCreate, db: Session = Depends(get_db)):
    reserva_existente = db.query(Reserva).filter(Reserva.id == id).first()
    if not reserva_existente:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    # Actualizar datos de la reserva
    reserva_existente.usuario_id = reserva.usuario_id
    reserva_existente.cancha_id = reserva.cancha_id
    reserva_existente.fecha_reserva = reserva.fecha_reserva
    reserva_existente.hora_inicio = reserva.hora_inicio
    reserva_existente.hora_fin = reserva.hora_fin
    db.commit()
    db.refresh(reserva_existente)
    return reserva_existente

# Eliminar una reserva
@router.delete("/{id}")
def eliminar_reserva(id: int, db: Session = Depends(get_db)):
    reserva = db.query(Reserva).filter(Reserva.id == id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    db.delete(reserva)
    db.commit()
    return {"message": "Reserva eliminada correctamente"}

# Endpoint: Consultar horarios disponibles
@router.get("/disponibilidad/")
def obtener_horarios_disponibles(
    request: Request,
    cancha_id: int,
    fecha: date,
    db: Session = Depends(get_db)
):
    print(f"Solicitud recibida con método: {request.method}")
    print(f"Cancha ID: {cancha_id}, Fecha: {fecha}")
    """
    Consulta los horarios disponibles para una cancha en una fecha específica.
    """
    # Validar que la cancha existe
    cancha_reservas = db.query(Reserva).filter(
        Reserva.cancha_id == cancha_id,
        Reserva.fecha_reserva == fecha
    ).all()

    # Horarios de inicio y fin del rango permitido
    hora_inicio_dia = time(7, 0)  # 7:00 AM
    hora_fin_dia = time(23, 0)    # 11:00 PM
    rango_horarios = []

    # Construir el rango de horarios por bloques de 1 hora
    actual = datetime.combine(fecha, hora_inicio_dia)
    fin_dia = datetime.combine(fecha, hora_fin_dia)
    now = datetime.now()  # Obtener la fecha y hora actuales
    while actual < fin_dia:
        siguiente = actual + timedelta(hours=1)
        # Excluir horarios pasados
        if actual > now:
            rango_horarios.append((actual.time(), siguiente.time()))
        actual = siguiente

    # Eliminar horarios ocupados
    for reserva in cancha_reservas:
        rango_horarios = [
            (inicio, fin) for inicio, fin in rango_horarios
            if not (reserva.hora_inicio < fin and reserva.hora_fin > inicio)
        ]

    return {"cancha_id": cancha_id, "fecha": fecha, "horarios_disponibles": rango_horarios}