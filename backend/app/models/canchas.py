from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Cancha(Base):
    __tablename__ = "canchas"  # Coincide con la tabla existente

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    ubicacion = Column(String, nullable=True)

    reservas = relationship("Reserva", back_populates="cancha")