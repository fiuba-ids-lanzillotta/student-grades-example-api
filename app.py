import logging
from flask import Flask
from flask_cors import CORS
from student_grades_example.constants import BASE_URL
from student_grades_example.routes.alumnos import alumnos_bp
from student_grades_example.routes.materias import materias_bp

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(name)s - %(message)s')

app = Flask(__name__)
app.json.sort_keys = False

# Habilitar CORS para que el frontend pueda consumir la API
CORS(app)

app.register_blueprint(alumnos_bp, url_prefix=BASE_URL)
app.register_blueprint(materias_bp, url_prefix=BASE_URL)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
