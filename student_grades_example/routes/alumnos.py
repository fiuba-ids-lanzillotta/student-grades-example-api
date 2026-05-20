from flask import Blueprint, jsonify, request
from ..constants import ERROR_CODE_ALUMNO_NOT_FOUND
from ..utils import construir_error_api
from ..validators.alumnos import validar_padron
from ..services.alumnos import (
    listar_alumnos,
    buscar_alumno_por_padron,
    listar_notas_de_alumno,
    agregar_nota_a_alumno,
)

alumnos_bp = Blueprint('alumnos', __name__)


@alumnos_bp.route('/alumnos', methods=['GET'])
def get_alumnos():
    alumnos = listar_alumnos()

    if not alumnos:
        return '', 204

    return jsonify(alumnos)


@alumnos_bp.route('/alumnos/<padron>', methods=['GET'])
def get_alumno(padron):
    try:
        padron_id = validar_padron(padron)
    except ValueError as e:
        return jsonify(e.args[0]), 400

    alumno = buscar_alumno_por_padron(padron_id)

    if not alumno:
        return jsonify(construir_error_api(
            code=ERROR_CODE_ALUMNO_NOT_FOUND,
            message='Alumno no encontrado',
            description=f"No existe un alumno con padron '{padron_id}'"
        )), 404

    return jsonify(alumno)


@alumnos_bp.route('/alumnos/<padron>/notas', methods=['GET'])
def get_notas_alumno(padron):
    try:
        padron_id = validar_padron(padron)
    except ValueError as e:
        return jsonify(e.args[0]), 400

    if not buscar_alumno_por_padron(padron_id):
        return jsonify(construir_error_api(
            code=ERROR_CODE_ALUMNO_NOT_FOUND,
            message='Alumno no encontrado',
            description=f"No existe un alumno con padron '{padron_id}'"
        )), 404

    return jsonify(listar_notas_de_alumno(padron_id))


@alumnos_bp.route('/alumnos/<padron>/notas', methods=['POST'])
def post_nota_alumno(padron):
    try:
        padron_id = validar_padron(padron)
    except ValueError as e:
        return jsonify(e.args[0]), 400

    body = request.get_json(silent=True)

    try:
        nota = agregar_nota_a_alumno(padron_id, body)
    except ValueError as e:
        status = e.args[1] if len(e.args) > 1 else 400

        return jsonify(e.args[0]), status

    return jsonify(nota), 201
