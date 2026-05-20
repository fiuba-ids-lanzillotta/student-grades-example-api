from ..utils import validar_string_no_vacio


def validar_codigo_materia(codigo_raw) -> str:
    """Valida que el codigo de materia sea una cadena no vacia."""
    return validar_string_no_vacio(codigo_raw, 'codigo')
