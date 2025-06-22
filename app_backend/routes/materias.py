from flask import Blueprint, jsonify
from app_backend.db import get_connection

materias_bp = Blueprint("materias", __name__)


@materias_bp.route("/<codigo>/alumnos", methods=["GET"])
def get_alumnos(codigo):
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT a.padron, a.nombre, a.apellido, n.nota, n.fecha
            FROM alumnos a
            JOIN notas n ON a.padron = n.padron
            WHERE n.codigo_materia = %s
        """, (codigo,))
        alumnos = cur.fetchall()
        return jsonify(alumnos)
    except Exception as e:
        print(e)
        return jsonify({"error": "Error al obtener los alumnos"}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()