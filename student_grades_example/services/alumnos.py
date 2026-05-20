import logging
from ..constants import ERROR_CODE_ALUMNO_NOT_FOUND, ERROR_CODE_MATERIA_NOT_FOUND, NOTA_APROBADA
from ..utils import construir_error_api
from ..validators.alumnos import validar_body_nueva_nota
from .. import db

logger = logging.getLogger(__name__)


def construir_alumno_dto(alumno: dict) -> dict:
    """DTO publico de un alumno."""
    return {
        'padron':   alumno['padron'],
        'nombre':   alumno['nombre'],
        'apellido': alumno['apellido'],
    }


def construir_nota_dto(nota: dict) -> dict:
    """DTO publico de una nota con datos de la materia y estado calculado."""
    valor = nota['nota']

    return {
        'codigo':   nota['codigo'],
        'nombre':   nota['nombre'],
        'nota':     valor,
        'fecha':    str(nota['fecha']),
        'aprobada': valor >= NOTA_APROBADA,
    }


def listar_alumnos() -> list[dict]:
    """Retorna todos los alumnos."""
    return [construir_alumno_dto(a) for a in db.obtener_todos_los_alumnos()]


def buscar_alumno_por_padron(padron: int) -> dict:
    """Busca un alumno por padron. Retorna {} si no existe."""
    alumno = db.obtener_alumno_por_padron(padron)

    if not alumno:
        return {}

    return construir_alumno_dto(alumno)


def listar_notas_de_alumno(padron: int) -> list[dict]:
    """Retorna las notas de un alumno. La existencia del alumno debe validarse aparte."""
    return [construir_nota_dto(n) for n in db.obtener_notas_de_alumno(padron)]


def agregar_nota_a_alumno(padron: int, body: dict) -> dict:
    """
    Valida el body, verifica que existan el alumno y la materia, e inserta la nota.
    Retorna el DTO de la nota recien creada.
    """
    if not db.obtener_alumno_por_padron(padron):
        raise ValueError(construir_error_api(
            code=ERROR_CODE_ALUMNO_NOT_FOUND,
            message='Alumno no encontrado',
            description=f"No existe un alumno con padron '{padron}'"
        ), 404)

    datos = validar_body_nueva_nota(body)

    if not db.obtener_materia_por_codigo(datos['codigo']):
        raise ValueError(construir_error_api(
            code=ERROR_CODE_MATERIA_NOT_FOUND,
            message='Materia no encontrada',
            description=f"No existe una materia con codigo '{datos['codigo']}'"
        ), 404)

    db.insertar_nota(
        padron=padron,
        codigo_materia=datos['codigo'],
        nota=datos['nota'],
        fecha=datos['fecha'],
    )

    materia = db.obtener_materia_por_codigo(datos['codigo'])

    return construir_nota_dto({
        'codigo': datos['codigo'],
        'nombre': materia['nombre'],
        'nota':   datos['nota'],
        'fecha':  datos['fecha'],
    })
