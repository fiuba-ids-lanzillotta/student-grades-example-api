from flask import Blueprint, jsonify, request
from app_backend.db import get_connection

alumnos_bp = Blueprint("alumnos", __name__)

@alumnos_bp.route("/")
def get_alumnos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alumnos")
    alumnos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(alumnos)

@alumnos_bp.route("/<int:padron>")
def get_alumno(padron):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alumnos WHERE padron = %s", (padron,))
    alumno = cursor.fetchone()
    cursor.close()
    conn.close()
    if not alumno:
        return ("Alumno no encontrado", 404)
    return jsonify(alumno)


@alumnos_bp.route("/<int:padron>/notas", methods=["POST"])
def add_nota_alumno(padron):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = request.json
    codigo_materia = data.get("codigo_materia")
    nota = data.get("nota")
    fecha = data.get("fecha")

    cursor.execute("""
                   INSERT INTO notas (padron, codigo_materia, nota, fecha)
                   VALUES (%s, %s, %s, %s)
                   """, (padron, codigo_materia, nota, fecha))
    
    conn.commit()
    cursor.close()
    conn.close()
    return ("Nota agregada correctamente", 201)


@alumnos_bp.route("/<int:padron>/notas")
def get_notas_alumno(padron):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT materias.codigo, materias.nombre, notas.nota, notas.fecha
        FROM notas
        JOIN materias ON materias.codigo = notas.codigo_materia
        WHERE notas.padron = %s
        """, (padron,)
    )
    alumnos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(alumnos)
