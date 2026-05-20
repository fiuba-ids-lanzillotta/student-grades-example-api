from ..constants import FORMATO_FECHA, MIN_NOTA, MAX_NOTA
from ..utils import (
    construir_error_api,
    validar_formato_fecha,
    validar_entero,
    validar_minimo,
    validar_maximo,
    validar_string_no_vacio,
)


def validar_padron(padron_raw) -> int:
    """Valida que el padron recibido sea un entero positivo."""
    padron = validar_entero(padron_raw, 'padron')

    return validar_minimo(padron, 1, 'padron')


def validar_body_nueva_nota(body: dict) -> dict:
    """
    Valida el body del POST /alumnos/{padron}/notas.
    Acepta `codigo` (codigo de materia), `nota` y `fecha`.
    """
    if body is None:
        raise ValueError(construir_error_api(
            code='invalid.body',
            message='Cuerpo de la solicitud invalido',
            description='El cuerpo debe ser un JSON valido con Content-Type application/json'
        ))

    errores = []

    codigo = None
    nota   = None
    fecha  = None

    try:
        codigo = validar_string_no_vacio(body.get('codigo'), 'codigo')
    except ValueError as e:
        errores.extend(e.args[0]['errors'])

    try:
        nota = validar_entero(body.get('nota'), 'nota')
        nota = validar_minimo(nota, MIN_NOTA, 'nota')
        nota = validar_maximo(nota, MAX_NOTA, 'nota')
    except ValueError as e:
        errores.extend(e.args[0]['errors'])

    try:
        fecha_str = validar_string_no_vacio(body.get('fecha'), 'fecha')
        validar_formato_fecha(fecha_str, FORMATO_FECHA, 'fecha')
        fecha = fecha_str
    except ValueError as e:
        errores.extend(e.args[0]['errors'])

    if errores:
        raise ValueError({'errors': errores})

    return {
        'codigo': codigo,
        'nota':   nota,
        'fecha':  fecha,
    }
