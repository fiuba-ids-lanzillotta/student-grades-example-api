from sqlalchemy import create_engine, text
from .constants import DB_URL

# Motor de conexion compartido por toda la aplicacion.
# El pool de conexiones lo maneja SQLAlchemy automaticamente.
motor = create_engine(DB_URL, pool_pre_ping=True)


# ---------------------------------------------------------------
# Funciones de soporte
# ---------------------------------------------------------------

def fila_a_dict(fila) -> dict:
    """Convierte una fila del resultado de una query en un diccionario."""
    return dict(fila._mapping)


def ejecutar_consulta(sql: str, parametros: dict = None) -> list[dict]:
    """Ejecuta una SELECT y devuelve todas las filas como lista de dicts."""
    with motor.connect() as conexion:
        resultado = conexion.execute(text(sql), parametros or {})

        return [fila_a_dict(fila) for fila in resultado]


def ejecutar_mutacion(sql: str, parametros: dict = None) -> int:
    """
    Ejecuta un INSERT, UPDATE o DELETE y hace commit.
    Retorna el id autoincremental generado por el INSERT (0 si no aplica).
    """
    with motor.begin() as conexion:
        resultado = conexion.execute(text(sql), parametros or {})

        return resultado.lastrowid or 0


# ---------------------------------------------------------------
# Queries de alumnos
# ---------------------------------------------------------------

def obtener_todos_los_alumnos() -> list[dict]:
    """Retorna todos los alumnos ordenados por padron."""
    sql = 'SELECT padron, nombre, apellido FROM alumnos ORDER BY padron'

    return ejecutar_consulta(sql)


def obtener_alumno_por_padron(padron: int) -> dict:
    """Retorna el alumno con el padron dado, o un dict vacio si no existe."""
    sql   = 'SELECT padron, nombre, apellido FROM alumnos WHERE padron = :padron'
    filas = ejecutar_consulta(sql, {'padron': padron})

    return filas[0] if filas else {}


def obtener_notas_de_alumno(padron: int) -> list[dict]:
    """Retorna las notas de un alumno con los datos de la materia."""
    sql = """
        SELECT m.codigo, m.nombre, n.nota, n.fecha
        FROM notas n
        JOIN materias m ON m.codigo = n.codigo_materia
        WHERE n.padron = :padron
        ORDER BY n.fecha
    """

    return ejecutar_consulta(sql, {'padron': padron})


def insertar_nota(padron: int, codigo_materia: str, nota: int, fecha: str) -> int:
    """Inserta una nueva nota y retorna el id generado."""
    sql = """
        INSERT INTO notas (padron, codigo_materia, nota, fecha)
        VALUES (:padron, :codigo_materia, :nota, :fecha)
    """

    return ejecutar_mutacion(sql, {
        'padron':         padron,
        'codigo_materia': codigo_materia,
        'nota':           nota,
        'fecha':          fecha,
    })


# ---------------------------------------------------------------
# Queries de materias
# ---------------------------------------------------------------

def obtener_materia_por_codigo(codigo: str) -> dict:
    """Retorna la materia con el codigo dado, o un dict vacio si no existe."""
    sql   = 'SELECT codigo, nombre, carrera FROM materias WHERE codigo = :codigo'
    filas = ejecutar_consulta(sql, {'codigo': codigo})

    return filas[0] if filas else {}


def obtener_alumnos_de_materia(codigo: str) -> list[dict]:
    """Retorna los alumnos que cursaron una materia, con su nota y fecha."""
    sql = """
        SELECT a.padron, a.nombre, a.apellido, n.nota, n.fecha
        FROM alumnos a
        JOIN notas n ON a.padron = n.padron
        WHERE n.codigo_materia = :codigo
        ORDER BY a.padron
    """

    return ejecutar_consulta(sql, {'codigo': codigo})
