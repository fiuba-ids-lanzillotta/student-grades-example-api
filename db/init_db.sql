-- =============================================================
--  Student Grades Example - Script DDL para MySQL
-- =============================================================
--  docker-compose lo ejecuta automaticamente al levantar el contenedor
--  (volumen montado en /docker-entrypoint-initdb.d).
--
--  La base `facultad` la crea el propio contenedor via MYSQL_DATABASE.
-- =============================================================

CREATE TABLE IF NOT EXISTS alumnos (
    padron   INT          PRIMARY KEY,
    nombre   VARCHAR(50)  NOT NULL,
    apellido VARCHAR(50)  NOT NULL
);

CREATE TABLE IF NOT EXISTS materias (
    codigo  VARCHAR(10) PRIMARY KEY,
    nombre  VARCHAR(50) NOT NULL,
    carrera VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS notas (
    id             INT          AUTO_INCREMENT PRIMARY KEY,
    padron         INT          NOT NULL,
    codigo_materia VARCHAR(10)  NOT NULL,
    nota           INT          NOT NULL CHECK (nota BETWEEN 1 AND 10),
    fecha          DATE         NOT NULL,
    FOREIGN KEY (padron)         REFERENCES alumnos(padron)  ON DELETE CASCADE,
    FOREIGN KEY (codigo_materia) REFERENCES materias(codigo) ON DELETE CASCADE
);

-- =============================================================
--  Datos de ejemplo
-- =============================================================
INSERT INTO alumnos (padron, nombre, apellido) VALUES
    (1, 'Juan',  'Perez'),
    (2, 'Maria', 'Garcia'),
    (3, 'Pedro', 'Lopez');

INSERT INTO materias (codigo, nombre, carrera) VALUES
    ('TB022', 'IDS',         'Informatica'),
    ('TB021', 'Fundamentos', 'Informatica');

INSERT INTO notas (padron, codigo_materia, nota, fecha) VALUES
    (1, 'TB022', 9, '2023-03-01'),
    (1, 'TB021', 7, '2023-03-02'),
    (2, 'TB022', 9, '2023-03-01'),
    (2, 'TB021', 7, '2023-03-02'),
    (3, 'TB022', 5, '2023-03-01'),
    (3, 'TB021', 5, '2023-03-02');
