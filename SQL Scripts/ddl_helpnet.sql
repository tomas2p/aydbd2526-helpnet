-- Active: 1760516486489@@127.0.0.1@5432@helpnet
DROP DATABASE IF EXISTS helpnet;
CREATE DATABASE helpnet;
\c helpnet;

---------------------------------------------------------
-- TABLAS
---------------------------------------------------------

-- Tabla organizacion
CREATE TABLE organizacion (
    nombre VARCHAR(100) PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL
);

-- Tabla email_organizacion
CREATE TABLE email_organizacion (
    nombre_organizacion VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    PRIMARY KEY (nombre_organizacion, email),
    FOREIGN KEY (nombre_organizacion) REFERENCES organizacion(nombre) ON DELETE CASCADE
);

-- Tabla proyecto
CREATE TABLE proyecto (
    id_proyecto SERIAL PRIMARY KEY,
    nombre_organizacion VARCHAR(100) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    FOREIGN KEY (nombre_organizacion) REFERENCES organizacion(nombre) ON DELETE CASCADE,
    CHECK (fecha_inicio <= fecha_fin)
);

-- Tabla actividad
CREATE TABLE actividad (
    id_actividad INTEGER NOT NULL,
    id_proyecto INTEGER NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    PRIMARY KEY (id_actividad, id_proyecto),
    FOREIGN KEY (id_proyecto) REFERENCES proyecto(id_proyecto) ON DELETE CASCADE,
    CHECK (fecha_inicio <= fecha_fin)
);

-- Tabla localizacion
CREATE TABLE localizacion (
    id_localizacion INTEGER NOT NULL,
    id_actividad INTEGER NOT NULL,
    id_proyecto INTEGER NOT NULL,
    latitud DECIMAL(10, 8) NOT NULL,
    longitud DECIMAL(11, 8) NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    observaciones TEXT,
    PRIMARY KEY (id_localizacion, id_actividad, id_proyecto),
    FOREIGN KEY (id_actividad, id_proyecto) REFERENCES actividad(id_actividad, id_proyecto) ON DELETE CASCADE,
    CHECK (latitud >= -90 AND latitud <= 90),
    CHECK (longitud >= -180 AND longitud <= 180)
);

-- Tabla voluntario
CREATE TABLE voluntario (
    dni VARCHAR(9) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_alta DATE NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    email VARCHAR(100) NOT NULL,
    CHECK (fecha_nacimiento < fecha_alta),
    CHECK (fecha_alta >= fecha_nacimiento + INTERVAL '18 years')
);

-- Tabla voluntario_skill
CREATE TABLE voluntario_skill (
    dni_voluntario VARCHAR(9) NOT NULL,
    nombre_skill VARCHAR(100) NOT NULL,
    descripcion TEXT,
    PRIMARY KEY (dni_voluntario, nombre_skill),
    FOREIGN KEY (dni_voluntario) REFERENCES voluntario(dni) ON DELETE CASCADE
);

-- Tabla participa (Rol Operativo en una Localización)
CREATE TABLE participa (
    id_localizacion INTEGER NOT NULL,
    id_actividad INTEGER NOT NULL,
    id_proyecto INTEGER NOT NULL,
    dni_voluntario VARCHAR(9) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    evaluacion INTEGER,
    PRIMARY KEY (id_localizacion, id_actividad, id_proyecto, dni_voluntario),
    FOREIGN KEY (dni_voluntario) REFERENCES voluntario(dni) ON DELETE CASCADE,
    FOREIGN KEY (id_localizacion, id_actividad, id_proyecto) 
        REFERENCES localizacion(id_localizacion, id_actividad, id_proyecto) ON DELETE CASCADE,
    CHECK (evaluacion >= 0 AND evaluacion <= 10)
);

-- Tabla coordina (Rol de Responsable en una Localización)
CREATE TABLE coordina (
    id_localizacion INTEGER NOT NULL,
    id_actividad INTEGER NOT NULL,
    id_proyecto INTEGER NOT NULL,
    dni_voluntario VARCHAR(9) NOT NULL,
    evaluacion INTEGER,
    PRIMARY KEY (id_localizacion, id_actividad, id_proyecto, dni_voluntario),
    FOREIGN KEY (dni_voluntario) REFERENCES voluntario(dni) ON DELETE CASCADE,
    FOREIGN KEY (id_localizacion, id_actividad, id_proyecto) 
        REFERENCES localizacion(id_localizacion, id_actividad, id_proyecto) ON DELETE CASCADE,
    CHECK (evaluacion >= 0 AND evaluacion <= 10)
);

-- Tabla cesion (relación ternaria)
CREATE TABLE cesion (
    nombre_organizacion VARCHAR(100) NOT NULL,
    id_proyecto INTEGER NOT NULL,
    dni_voluntario VARCHAR(9) NOT NULL,
    fecha_cesion DATE NOT NULL,
    duracion INTEGER NOT NULL, 
    PRIMARY KEY (nombre_organizacion, id_proyecto, dni_voluntario),
    FOREIGN KEY (nombre_organizacion) REFERENCES organizacion(nombre) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_proyecto) REFERENCES proyecto(id_proyecto) ON DELETE CASCADE,
    FOREIGN KEY (dni_voluntario) REFERENCES voluntario(dni) ON DELETE CASCADE,
    CHECK (duracion > 0)
);

-- Tabla Padre: recurso
CREATE TABLE recurso (
    id_recurso SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_entrega DATE NOT NULL,
    tipo CHAR(1) NOT NULL,
    CHECK (tipo IN ('D', 'A'))
);

-- Subclase: donado
CREATE TABLE donado (
    id_recurso INTEGER PRIMARY KEY,
    estado VARCHAR(50) NOT NULL,
    nombre_donante VARCHAR(100),
    email_donante VARCHAR(100),
    FOREIGN KEY (id_recurso) REFERENCES recurso(id_recurso) ON DELETE CASCADE
);

-- Subclase: alquilado
CREATE TABLE alquilado (
    id_recurso INTEGER PRIMARY KEY,
    proveedor VARCHAR(100) NOT NULL,
    costo DECIMAL(10, 2) NOT NULL,
    fecha_devolucion DATE NOT NULL,
    FOREIGN KEY (id_recurso) REFERENCES recurso(id_recurso) ON DELETE CASCADE,
    CHECK (costo >= 0)
);

-- Tabla recurso_usado
CREATE TABLE recurso_usado (
    id_proyecto INTEGER NOT NULL,
    id_recurso INTEGER NOT NULL,
    PRIMARY KEY (id_proyecto, id_recurso),
    FOREIGN KEY (id_proyecto) REFERENCES proyecto(id_proyecto) ON DELETE CASCADE,
    FOREIGN KEY (id_recurso) REFERENCES recurso(id_recurso) ON DELETE CASCADE
);

---------------------------------------------------------
-- VISTAS
---------------------------------------------------------

-- Vista de edad calculada
CREATE VIEW vista_voluntario_edad AS
SELECT *,
    DATE_PART('year', AGE(CURRENT_DATE, fecha_nacimiento)) AS edad
FROM voluntario;