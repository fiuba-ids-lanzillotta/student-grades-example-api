from flask import Blueprint, jsonify
from ..constants import ERROR_CODE_MATERIA_NOT_FOUND
from ..utils import construir_error_api
from ..validators.materias import validar_codigo_materia
from ..services.materias import buscar_materia_por_codigo, listar_alumnos_de_materia

materias_bp = Blueprint('materias', __name__)


@materias_bp.route('/materias/<codigo>/alumnos', methods=['GET'])
def get_alumnos_de_materia(codigo):
    try:
        codigo_validado = validar_codigo_materia(codigo)
    except ValueError as e:
        return jsonify(e.args[0]), 400

    if not buscar_materia_por_codigo(codigo_validado):
        return jsonify(construir_error_api(
            code=ERROR_CODE_MATERIA_NOT_FOUND,
            message='Materia no encontrada',
            description=f"No existe una materia con codigo '{codigo_validado}'"
        )), 404

    return jsonify(listar_alumnos_de_materia(codigo_validado))
