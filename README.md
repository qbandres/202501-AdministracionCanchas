# 202501-AdministracionCanchas
Esta aplicación será para adminsatrar canchas de fultbito

# 202501-AdministracionCanchas

Sistema de administración de reservas para canchas deportivas. Este proyecto permite a los usuarios reservar canchas, mientras que los administradores tienen control total sobre la gestión de las reservas, usuarios y estadísticas.

---

## Características

### Usuario
- Registro de reservas con horarios disponibles.
- Visualización de reservas existentes.
- Restricción de una reserva por usuario al día.
- Interfaz amigable para seleccionar cancha, fecha y horario.

### Administrador
- Crear reservas sin restricciones (horarios solapados, múltiples reservas por día, etc.).
- Editar y eliminar cualquier reserva.
- Visualización de estadísticas como:
  - Horarios más reservados.
  - Reservas por día y cancha.
- Filtros para buscar reservas por usuario o cancha.

---

## Tecnologías utilizadas

### Frontend
- **Framework**: Vue.js
- **Herramienta de desarrollo**: Vite
- **Librerías adicionales**:
  - Axios (para solicitudes HTTP)
  - Chart.js (para gráficos)
  - Pinia (gestión de estado global)

### Backend
- **Framework**: FastAPI
- **Base de datos**: PostgreSQL
- **ORM**: SQLAlchemy
- **Gestión de dependencias**: pip

---

## Instalación y configuración

### Requisitos previos
- Python 3.9 o superior.
- Node.js 16 o superior.
- PostgreSQL.
- Clave SSH configurada para GitHub.

---

### Clonar el repositorio

```bash
git clone git@github.com:qbandres/202501-AdministracionCanchas.git
cd 202501-AdministracionCanchas

###Estructura edl Proyecto
202501-AdministracionCanchas/
│
├── backend/
│   ├── app/
│   │   ├── main.py          # Archivo principal de la aplicación.
│   │   ├── models/          # Modelos de la base de datos.
│   │   ├── schemas/         # Esquemas Pydantic.
│   │   ├── routes/          # Endpoints del backend.
│   │   ├── database.py      # Conexión a la base de datos.
│   │   └── __init__.py      # Configuración del módulo principal.
│   ├── requirements.txt     # Dependencias del backend.
│   ├── .env                 # Configuración de variables de entorno.
│   └── venv/                # Entorno virtual de Python.
│
├── frontend/
│   ├── public/              # Archivos estáticos del frontend.
│   ├── src/
│   │   ├── components/      # Componentes reutilizables de Vue.js.
│   │   ├── views/           # Vistas principales (reservas, estadísticas, etc.).
│   │   ├── App.vue          # Componente raíz.
│   │   └── main.js          # Archivo principal del frontend.
│   ├── .env                 # Configuración de variables de entorno.
│   ├── package.json         # Dependencias del frontend.
│   └── vite.config.js       # Configuración de Vite.


Endpoints principales

Reservas
	•	Crear reserva (usuario): POST /api/reservas/
	•	Crear reserva (administrador): POST /api/reservas/admin/
	•	Listar reservas: GET /api/reservas/ (filtros opcionales: usuario_id, cancha_id)
	•	Consultar horarios disponibles: GET /api/reservas/disponibilidad/
	•	Actualizar reserva: PUT /api/reservas/{id}
	•	Eliminar reserva: DELETE /api/reservas/{id}

Usuarios
	•	Listar usuarios: GET /api/usuarios/

Instalar dependencias:
pip install -r requirements.txt

Crear un archivo .env en la carpeta backend con las siguientes variables:
DATABASE_URL=postgresql://usuario:contraseña@localhost/nombre_base_datos

5.	Ejecutar el servidor:
uvicorn app.main:app --reload

6.	Verifica los endpoints disponibles navegando a:
http://127.0.0.1:8000/docs

3.	Crear un archivo .env en la carpeta frontend con la siguiente variable:
VITE_BACKEND_URL=http://127.0.0.1:8000/api