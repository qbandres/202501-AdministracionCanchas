from sqlalchemy import Column, Integer, ForeignKey, Date, Time, String
from sqlalchemy.orm import relationship
from app.database import Base

class Reserva(Base):
    __tablename__ = "reservas"  # Coincide con la tabla existente

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cancha_id = Column(Integer, ForeignKey("canchas.id"), nullable=False)
    fecha_reserva = Column(Date, nullable=False)  # Cambiado a Date
    hora_inicio = Column(Time, nullable=False)    # Cambiado a Time
    hora_fin = Column(Time, nullable=False)       # Cambiado a Time
    estado = Column(String, default="confirmada")

    usuario = relationship("Usuario", back_populates="reservas")
    cancha = relationship("Cancha", back_populates="reservas")