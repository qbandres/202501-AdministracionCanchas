from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import usuarios, canchas, reservas, login

app = FastAPI(title="Administración de Canchas")

# Configuración de CORS
origins = [
    "http://localhost:5173",  # URL del frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas con el prefijo /api
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(canchas.router, prefix="/api/canchas", tags=["Canchas"])
app.include_router(reservas.router, prefix="/api/reservas", tags=["Reservas"])
app.include_router(login.router, prefix="/api/login", tags=["Autenticación"])


@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de Administración de Canchas!"}