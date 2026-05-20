from datetime import datetime
from re import sub
import logging
from .constants import (
    ERROR_CODE_INVALID_MIN_VALUE,
    ERROR_CODE_INVALID_MAX_VALUE,
)

logger = logging.getLogger(__name__)


def construir_error_api(code: str, message: str, description: str, level: str = 'error') -> dict:
    """Construye un payload de error compatible con el resto de la API."""
    return {
        'errors': [{
            'code': code,
            'message': message,
            'level': level,
            'description': description
        }]
    }


def validar_formato_fecha(fecha: str, formato: str, nombre: str = 'fecha') -> datetime:
    try:
        return datetime.strptime(fecha, formato)
    except ValueError:
        logger.warning(f"Formato de fecha invalido: '{fecha}' no cumple el formato '{formato}'")

        raise ValueError(construir_error_api(
            code=f'invalid.{nombre}.format',
            message=f"Formato de '{nombre}' invalido",
            description=f"El valor '{fecha}' no cumple el formato esperado '{formato}'"
        ))


def validar_entero(numero, nombre: str = 'numero') -> int:
    valor = str(numero)
    valor_sin_letras = sub('[a-zA-Z]+', '', valor)

    try:
        return int(valor_sin_letras)
    except ValueError:
        logger.warning(f"Valor numerico invalido: '{numero}' no puede convertirse a entero")

        raise ValueError(construir_error_api(
            code=f'invalid.{nombre}.format',
            message=f"Formato de '{nombre}' invalido",
            description=f"El valor '{numero}' no puede convertirse a un numero entero"
        ))


def validar_minimo(valor: int, minimo: int, nombre: str) -> int:
    if valor < minimo:
        logger.warning(f"Valor por debajo del minimo: '{nombre}' es {valor}, minimo esperado {minimo}")

        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_MIN_VALUE,
            message='Valor por debajo del minimo permitido',
            description=f"El parametro '{nombre}' debe ser mayor o igual a {minimo}. Se recibio: {valor}"
        ))

    return valor


def validar_maximo(valor: int, maximo: int, nombre: str) -> int:
    if valor > maximo:
        logger.warning(f"Valor por encima del maximo: '{nombre}' es {valor}, maximo esperado {maximo}")

        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_MAX_VALUE,
            message='Valor por encima del maximo permitido',
            description=f"El parametro '{nombre}' debe ser menor o igual a {maximo}. Se recibio: {valor}"
        ))

    return valor


def validar_string_no_vacio(valor, nombre: str) -> str:
    if valor is None or not str(valor).strip():
        raise ValueError(construir_error_api(
            code=f'required.{nombre}',
            message=f"Campo requerido: '{nombre}'",
            description=f"El campo '{nombre}' es obligatorio y no puede estar vacio"
        ))

    return str(valor).strip()
