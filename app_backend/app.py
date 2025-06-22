from flask import Flask
from flask_cors import CORS
from app_backend.routes.alumnos import alumnos_bp
from app_backend.routes.materias import materias_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(alumnos_bp, url_prefix="/alumnos")
app.register_blueprint(materias_bp, url_prefix="/materias")


if __name__ == "__main__":
    app.run(port=5000, debug=True)