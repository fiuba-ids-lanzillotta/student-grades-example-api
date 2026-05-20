import logging
from .. import db

logger = logging.getLogger(__name__)


def construir_alumno_en_materia_dto(fila: dict) -> dict:
    """DTO de un alumno que cursa una materia, incluyendo su nota."""
    return {
        'padron':   fila['padron'],
        'nombre':   fila['nombre'],
        'apellido': fila['apellido'],
        'nota':     fila['nota'],
        'fecha':    str(fila['fecha']),
    }


def buscar_materia_por_codigo(codigo: str) -> dict:
    """Busca una materia por codigo. Retorna {} si no existe."""
    materia = db.obtener_materia_por_codigo(codigo)

    if not materia:
        return {}

    return {
        'codigo':  materia['codigo'],
        'nombre':  materia['nombre'],
        'carrera': materia['carrera'],
    }


def listar_alumnos_de_materia(codigo: str) -> list[dict]:
    """Retorna los alumnos que cursaron una materia. La existencia se valida aparte."""
    return [construir_alumno_en_materia_dto(f) for f in db.obtener_alumnos_de_materia(codigo)]
