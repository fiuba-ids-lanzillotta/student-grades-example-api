CREATE DATABASE IF NOT EXISTS facultad;
USE facultad;

CREATE TABLE IF NOT EXISTS alumnos (
    padron INT PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS materias (
    codigo VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(50),
    carrera VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    padron INT,
    codigo_materia VARCHAR(10),
    nota FLOAT, 
    fecha DATE,
    FOREIGN KEY (padron) REFERENCES alumnos(padron) ON DELETE CASCADE,
    FOREIGN KEY (codigo_materia) REFERENCES materias(codigo) ON DELETE CASCADE
);

INSERT INTO alumnos (padron, nombre, apellido) VALUES
(1, 'Juan', 'Perez'),
(2, 'Maria', 'Garcia'),
(3, 'Pedro', 'Lopez');

INSERT INTO materias (codigo, nombre, carrera) VALUES
('TB022', 'IDS', 'Informatica'),
('TB021', 'Fundamentos', 'Informatica');

INSERT INTO notas (padron, codigo_materia, nota, fecha) VALUES
(1, 'TB022', 8.5, '2023-03-01'),
(1, 'TB021', 7.0, '2023-03-02'),
(2, 'TB022', 9.0, '2023-03-01'),
(2, 'TB021', 6.5, '2023-03-02'),
(3, 'TB022', 5.0, '2023-03-01'),
(3, 'TB021', 4.5, '2023-03-02');