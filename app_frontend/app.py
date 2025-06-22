from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import datetime

app = Flask(__name__)


API_BASE = "http://localhost:5000"

def obtener_alumno(padron):
    response = requests.get(f"{API_BASE}/alumnos/{padron}")
    if response.status_code == 200:
        return response.json()
    return None

def obtener_materias_alumno(padron):
    response = requests.get(f"{API_BASE}/alumnos/{padron}/notas")
    if response.status_code == 200:
        return response.json()
    return []

def agregar_nota(padron, codigo, nota, fecha):
    response = requests.post(
        f"{API_BASE}/alumnos/{padron}/notas",
        json={"codigo": codigo, "nota": nota, "fecha": fecha},
    )
    if response.status_code == 201:
        return True
    return None

def obtener_alumnos_materia(codigo):
    response = requests.get(f"{API_BASE}/materias/{codigo}/alumnos")
    if response.status_code == 200:
        return response.json()
    return []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        padron = request.form["padron"]
        if not padron:
            return redirect(url_for("index"))
        return redirect(url_for("detalle_alumno", padron=padron))

    return render_template("index.html")



@app.route("/detalle/<padron>", methods=["GET", "POST"])
def detalle_alumno(padron):
    if request.method == "POST":
        codigo = request.form["codigo"]
        nota = int(request.form["nota"])
        fecha = request.form["fecha"]
        ok = agregar_nota(padron, codigo, nota, fecha)
        if not ok:
            flash("Error al guardar la nota", "error")
        else:
            flash("Nota agregada con éxito", "success")
        return redirect(url_for("detalle_alumno", padron=padron))

    alumno = obtener_alumno(padron)
    if not alumno:
        return redirect(url_for("index"))
    materias = obtener_materias_alumno(padron)
    return render_template("detalle.html", alumno=alumno, materias=materias)

@app.route("/materias/<codigo>/alumnos")
def alumnos_materia(codigo):
    return obtener_alumnos_materia(codigo)


if __name__ == "__main__":
    app.secret_key = "supersecretkey"
    app.run(port=5001, debug=True)