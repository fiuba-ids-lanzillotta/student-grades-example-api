# Student Grades Example - API

> **Aviso:** este proyecto es **codigo de ejemplo** con fines didacticos. Puede contener errores, simplificaciones o decisiones de diseno discutibles. Si se usa como base para un trabajo practico u otro entregable, **debe adaptarse a las buenas practicas y consignas especificas de la materia/catedra** (estilo de codigo, manejo de errores, validaciones, tests, seguridad, persistencia, etc.).

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
├── db/
│   └── init_db.sql                 # Esquema + datos iniciales (lo corre docker-compose)
└── docs/
    └── swagger.yaml                # Documentacion OpenAPI 3.0 de la API
```

## Documentacion (Swagger / OpenAPI)

La especificacion completa de la API en formato OpenAPI 3.0 vive en
[`docs/swagger.yaml`](docs/swagger.yaml). Se puede visualizar de varias formas:

- Pegando el contenido del archivo en [editor.swagger.io](https://editor.swagger.io).
- Abriendolo con la extension "Swagger Viewer" (o similar) en VSCode.
- Sirviendolo con cualquier renderer compatible con OpenAPI 3.

## Requisitos previos

- Python 3.10+
- **Una** de las dos opciones para correr MySQL:
  - Docker + Docker Compose (recomendado), o
  - Una instalacion local de MySQL 8

## Configuracion

### 1. Variables de entorno

Copiar `.env.example` a `.env` (los defaults ya funcionan para desarrollo local):

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

Ajusta los valores segun como tengas configurado MySQL.

### 2. Base de datos MySQL

Eleg **una** de las dos opciones segun lo que tengas instalado.

#### Opcion A: con Docker (recomendado)

`docker-compose.yml` levanta MySQL 8 y monta `db/init_db.sql` como script de inicializacion, creando las tablas e insertando los datos de ejemplo automaticamente la **primera** vez:

```bash
docker compose up -d
```

Verificar que el contenedor este listo (puede tardar unos segundos):

```bash
docker compose logs -f mysql
# Buscar la linea: "ready for connections"
```

Apagar el contenedor manteniendo los datos en el volumen:

```bash
docker compose down
```

Apagar y **borrar** los datos (la proxima vez se vuelven a cargar los datos de `init_db.sql`):

```bash
docker compose down -v
```

#### Opcion B: con MySQL instalado localmente

Si ya tenes MySQL 8 corriendo en tu maquina (puerto `3306` por default):

1. Crear la base de datos y cargar el esquema + datos de ejemplo:

   ```bash
   # Linux / macOS / WSL
   mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS facultad;"
   mysql -u root -p facultad < db/init_db.sql
   ```

   ```powershell
   # Windows PowerShell
   mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS facultad;"
   Get-Content db\init_db.sql | mysql -u root -p facultad
   ```

2. Verificar que las tablas se hayan creado:

   ```bash
   mysql -u root -p -e "USE facultad; SHOW TABLES;"
   ```

   Deberias ver: `alumnos`, `materias`, `notas`.

3. Si tu usuario, password, puerto o nombre de base no coinciden con los defaults, actualiza el `.env` antes de levantar la API.

### 3. Entorno virtual, instalacion y ejecucion

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

Todos los endpoints estan bajo el prefijo `/student_grades_api`. Las respuestas son JSON; los errores siguen el formato:

```json
{
    "errors": [
        {
            "code": "<codigo>",
            "message": "<mensaje breve>",
            "level": "error",
            "description": "<descripcion detallada>"
        }
    ]
}
```

| Metodo | Endpoint                                | Descripcion                                                 |
|--------|-----------------------------------------|-------------------------------------------------------------|
| GET    | `/alumnos`                              | Listar todos los alumnos                                    |
| GET    | `/alumnos/<padron>`                     | Obtener un alumno por padron                                |
| GET    | `/alumnos/<padron>/notas`               | Listar las notas (con materia) de un alumno                 |
| POST   | `/alumnos/<padron>/notas`               | Registrar una nueva nota para un alumno                     |
| GET    | `/materias/<codigo>/alumnos`            | Listar los alumnos que cursaron una materia                 |

### `GET /alumnos`

Lista todos los alumnos.

```bash
curl http://localhost:5000/student_grades_api/alumnos
```

Respuesta `200 OK`:

```json
[
    { "padron": 1, "nombre": "Juan",  "apellido": "Perez" },
    { "padron": 2, "nombre": "Maria", "apellido": "Garcia" },
    { "padron": 3, "nombre": "Pedro", "apellido": "Lopez" }
]
```

Si no hay alumnos cargados, devuelve `204 No Content`.

### `GET /alumnos/<padron>`

Obtiene un alumno por su numero de padron.

```bash
curl http://localhost:5000/student_grades_api/alumnos/1
```

Respuesta `200 OK`:

```json
{ "padron": 1, "nombre": "Juan", "apellido": "Perez" }
```

Posibles errores:

- `400 Bad Request`: el padron no es un entero positivo.
- `404 Not Found`: no existe un alumno con ese padron.

### `GET /alumnos/<padron>/notas`

Lista las notas del alumno con datos de la materia y el flag `aprobada` (`true` si la nota es >= 6).

```bash
curl http://localhost:5000/student_grades_api/alumnos/1/notas
```

Respuesta `200 OK`:

```json
[
    { "codigo": "TB022", "nombre": "IDS",         "nota": 9, "fecha": "2023-03-01", "aprobada": true },
    { "codigo": "TB021", "nombre": "Fundamentos", "nota": 7, "fecha": "2023-03-02", "aprobada": true }
]
```

Posibles errores: `400` (padron invalido), `404` (alumno inexistente).

### `POST /alumnos/<padron>/notas`

Registra una nueva nota para el alumno.

**Headers**: `Content-Type: application/json`

**Body**:

| Campo    | Tipo    | Requerido | Descripcion                              |
|----------|---------|-----------|------------------------------------------|
| `codigo` | string  | si        | Codigo de la materia (debe existir)      |
| `nota`   | int     | si        | Entero entre 1 y 10 (inclusive)          |
| `fecha`  | string  | si        | Fecha en formato `YYYY-MM-DD`            |

```bash
curl -X POST http://localhost:5000/student_grades_api/alumnos/1/notas \
  -H "Content-Type: application/json" \
  -d '{"codigo": "TB022", "nota": 8, "fecha": "2025-03-15"}'
```

Respuesta `201 Created`:

```json
{
    "codigo":   "TB022",
    "nombre":   "IDS",
    "nota":     8,
    "fecha":    "2025-03-15",
    "aprobada": true
}
```

Posibles errores:

- `400 Bad Request`: padron invalido, body invalido o campos con formato/rango incorrecto (la respuesta puede incluir varios errores acumulados en `errors[]`).
- `404 Not Found`: el alumno o la materia no existen.

### `GET /materias/<codigo>/alumnos`

Lista los alumnos que tienen una nota cargada para esa materia.

```bash
curl http://localhost:5000/student_grades_api/materias/TB022/alumnos
```

Respuesta `200 OK`:

```json
[
    { "padron": 1, "nombre": "Juan",  "apellido": "Perez",  "nota": 9, "fecha": "2023-03-01" },
    { "padron": 2, "nombre": "Maria", "apellido": "Garcia", "nota": 9, "fecha": "2023-03-01" },
    { "padron": 3, "nombre": "Pedro", "apellido": "Lopez",  "nota": 5, "fecha": "2023-03-01" }
]
```

Posibles errores:

- `400 Bad Request`: codigo invalido (vacio).
- `404 Not Found`: no existe una materia con ese codigo.

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

## Glosario de terminos

- **API REST**: estilo de arquitectura para servicios web que expone recursos via HTTP (GET, POST, PUT, DELETE) usando, en general, JSON como formato de intercambio.
- **Endpoint**: ruta concreta de la API (por ejemplo `GET /alumnos/<padron>`) que responde a un metodo HTTP y realiza una accion sobre un recurso.
- **Request / Response**: par de mensajes HTTP. La **request** es lo que envia el cliente (metodo, headers, body); la **response** es lo que devuelve el servidor (status code, headers, body).
- **Status code**: codigo numerico de la respuesta HTTP. Por ejemplo: `200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `404 Not Found`.
- **Body**: contenido (payload) de una request o response. En esta API es JSON.
- **JSON**: formato de texto para representar datos estructurados (objetos y arrays). Es el formato usado para los bodies de request y response.
- **Flask**: micro framework web de Python. En este ejemplo se usa tanto en el frontend (renderizado server-side) como en la API backend.
- **Frontend**: aplicacion que renderiza las paginas HTML del lado del servidor y consume la API. En este ejemplo integrador corre en el puerto 5001 (`student-grades-example-web`).
- **Backend / API**: servicio HTTP REST (este proyecto) que expone los endpoints de alumnos, notas y materias. Corre en el puerto 5000.
- **Blueprint (Flask)**: mecanismo de Flask para agrupar rutas relacionadas en modulos (por ejemplo `routes/alumnos.py`, `routes/materias.py`).
- **Validator**: funcion que verifica que el body de la request cumple las reglas (campos requeridos, formato, rangos). Viven en `validators/`.
- **Service**: capa con la **logica de negocio** (listar alumnos, agregar nota). Vive en `services/` y es invocada desde las routes.
- **DTO (Data Transfer Object)**: estructura usada para pasar datos entre capas. En este proyecto se modelan como `dict` de Python (estilo funcional, sin clases).
- **SQLAlchemy**: libreria de Python para hablar con bases SQL. Aca se usa **sin ORM**, ejecutando SQL literal con `text()`.
- **ORM (Object Relational Mapper)**: capa que mapea tablas a clases/objetos. Este proyecto **no** lo usa para mantener el SQL explicito.
- **Query parametrizada**: query SQL en la que los valores se pasan como parametros (`:padron`) y no concatenados al string, evitando **SQL injection**.
- **SQL injection**: vulnerabilidad por la que un atacante inyecta SQL malicioso a traves de inputs no sanitizados.
- **Migracion / esquema**: definicion de la estructura de la base (tablas, columnas). Aca vive en `db/init_db.sql`.
- **MySQL**: motor de base de datos relacional usado en este proyecto. Se levanta en un contenedor via Docker Compose.
- **Docker / Docker Compose**: herramientas para correr servicios (en este caso MySQL) en contenedores aislados, definidos en `docker-compose.yml`.
- **Contenedor**: instancia en ejecucion de una imagen Docker (por ejemplo el contenedor de MySQL).
- **Volumen (Docker)**: almacenamiento persistente del contenedor; permite hacer `down` sin perder los datos.
- **`.env` / variables de entorno**: archivo con configuracion sensible (credenciales, secretos) que **no** se commitea al repo. `.env.example` es la plantilla.
- **CORS (Cross-Origin Resource Sharing)**: mecanismo del navegador que controla que dominios pueden consumir la API. Relevante cuando el frontend corre en otro origen.
- **Entorno virtual**: directorio aislado con la version de Python y las dependencias del proyecto, para no mezclarlas con las del sistema.
- **virtualenv / `venv`**: herramienta estandar de Python para crear entornos virtuales. Las dependencias se declaran en `requirements.txt` y se instalan con `pip install -r requirements.txt`. En este proyecto lo levantan los scripts `setup_virtualenv.sh` / `setup_virtualenv.bat`.
- **pipenv**: herramienta alternativa que combina la gestion del entorno virtual con la de dependencias en un solo flujo. Usa `Pipfile` (declaracion) y `Pipfile.lock` (versiones exactas resueltas) en vez de `requirements.txt`. En este proyecto lo levantan los scripts `setup_pipenv.sh` / `setup_pipenv.bat`.
- **`pip`**: gestor de paquetes de Python. Instala librerias desde PyPI dentro del entorno activo.
- **Padron**: identificador unico del alumno (entero positivo). Es la clave primaria de la tabla `alumnos`.
- **Materia**: asignatura identificada por un `codigo` corto (por ejemplo `TB022`).
- **Nota**: calificacion entera entre 1 y 10 asociada a un alumno y una materia en una fecha determinada. Se considera **aprobada** cuando es `>= 6`.
