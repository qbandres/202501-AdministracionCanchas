from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"  # Asegúrate de que coincide con el nombre de la tabla

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String, unique=True, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    rol = Column(String, default="usuario")
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    reservas = relationship("Reserva", back_populates="usuario")