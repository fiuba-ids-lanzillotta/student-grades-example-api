# Student Grades Example - API

## Motivacion

Este proyecto es un **ejemplo practico** de como construir una pequena **API REST en Flask** que expone datos de una facultad (alumnos, materias y notas) usando **MySQL** como base de datos, levantada con `docker-compose`.

El objetivo es servir de referencia para cualquier proyecto que necesite estructurar un backend Python con separacion clara entre **routes / services / validators / db**, usando **queries literales con SQLAlchemy** (sin ORM) y configuracion via variables de entorno.

Este es el backend del ejemplo integrador; el frontend que lo consume vive en el repositorio `student-grades-example-web`.

## Arquitectura

```
Flujo de una request:

  Frontend (Web)
       |
       |  HTTP (JSON)
       v
  Flask API (este proyecto, puerto 5000)
       |
       v
  MySQL (contenedor docker, puerto 3306)
```

## Estructura del proyecto

```
student-grades-example-api/
├── app.py                          # Entry point Flask (puerto 5000)
├── docker-compose.yml              # MySQL 8 + volumen + datos iniciales
├── requirements.txt                # Dependencias Python
├── .env.example                    # Template para configurar la DB
├── student_grades_example/
│   ├── constants.py                # Configuracion (DB + reglas de dominio)
│   ├── db.py                       # Capa de acceso a datos (queries literales)
│   ├── utils.py                    # Funciones de validacion reutilizables
│   ├── routes/
│   │   ├── alumnos.py              # Endpoints REST de alumnos y notas
│   │   └── materias.py             # Endpoints REST de materias
│   ├── services/
│   │   ├── alumnos.py              # Logica de negocio de alumnos / notas
│   │   └── materias.py             # Logica de negocio de materias
│   └── validators/
│       ├── alumnos.py              # Validacion de entrada para alumnos
│       └── materias.py             # Validacion de entrada para materias
└── db/
    └── init_db.sql                 # Esquema + datos iniciales (lo corre docker-compose)
```

## Requisitos previos

- Python 3.10+
- Docker + Docker Compose

## Configuracion

### 1. Base de datos MySQL via Docker

1. Copiar `.env.example` a `.env` (los defaults ya funcionan para desarrollo local):

   ```bash
   cp .env.example .env
   ```

   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=root
   DB_NAME=facultad
   ```

2. Levantar el contenedor de MySQL. `docker-compose` lee `.env` y monta `db/init_db.sql` como script de inicializacion (crea las tablas e inserta los datos de ejemplo):

   ```bash
   docker compose up -d
   ```

3. Para apagar la base (manteniendo los datos en el volumen):

   ```bash
   docker compose down
   ```

   Para borrar los datos:

   ```bash
   docker compose down -v
   ```

### 2. Entorno virtual, instalacion y ejecucion

El proyecto incluye scripts de setup que crean el entorno virtual, instalan las dependencias y levantan la API.

**Con virtualenv:**

```bash
# Windows
setup_virtualenv.bat

# Linux / macOS
chmod +x setup_virtualenv.sh
./setup_virtualenv.sh
```

**Con pipenv:**

```bash
# Windows
setup_pipenv.bat

# Linux / macOS
chmod +x setup_pipenv.sh
./setup_pipenv.sh
```

Una vez iniciada, la API estara disponible en `http://localhost:5000/student_grades_api`

## Endpoints

| Metodo | Endpoint                                | Descripcion                                                 |
|--------|-----------------------------------------|-------------------------------------------------------------|
| GET    | `/alumnos`                              | Listar todos los alumnos                                    |
| GET    | `/alumnos/<padron>`                     | Obtener un alumno por padron                                |
| GET    | `/alumnos/<padron>/notas`               | Listar las notas (con materia) de un alumno                 |
| POST   | `/alumnos/<padron>/notas`               | Registrar una nueva nota para un alumno                     |
| GET    | `/materias/<codigo>/alumnos`            | Listar los alumnos que cursaron una materia                 |

Todos los endpoints estan bajo el prefijo `/student_grades_api`.

### Ejemplo: registrar una nota

```bash
curl -X POST http://localhost:5000/student_grades_api/alumnos/1/notas \
  -H "Content-Type: application/json" \
  -d '{"codigo": "TB022", "nota": 8, "fecha": "2025-03-15"}'
```

Respuesta `201 Created`:

```json
{
    "codigo": "TB022",
    "nombre": "IDS",
    "nota": 8,
    "fecha": "2025-03-15",
    "aprobada": true
}
```

## Patron de queries literales

Este proyecto usa SQLAlchemy **sin ORM**, ejecutando SQL directamente con `text()`:

```python
from sqlalchemy import create_engine, text

motor = create_engine(DB_URL)

# SELECT
with motor.connect() as conexion:
    resultado = conexion.execute(text(sql), {'padron': 1})

# INSERT/UPDATE/DELETE (con commit automatico)
with motor.begin() as conexion:
    resultado = conexion.execute(text(sql), parametros)
```

Ver `student_grades_example/db.py` para todos los ejemplos de queries.
