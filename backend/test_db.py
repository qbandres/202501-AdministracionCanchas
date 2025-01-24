from app.database import SessionLocal
from app.models.canchas import Cancha

# Crear una sesión
db = SessionLocal()

try:
    # Leer todas las canchas
    canchas = db.query(Cancha).all()
    for cancha in canchas:
        print(f"ID: {cancha.id}, Nombre: {cancha.nombre}, Ubicación: {cancha.ubicacion}")
except Exception as e:
    print(f"Error al consultar las canchas: {e}")
finally:
    # Cerrar la sesión
    db.close()  