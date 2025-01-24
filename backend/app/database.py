from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# URL de la base de datos desde .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Configurar SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para probar la conexión a la base de datos
def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar()
            print(f"Conexión exitosa: {result}")
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")