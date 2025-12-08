-- Active: 1760516486489@@127.0.0.1@5432@helpnet
DROP DATABASE IF EXISTS helpnet;
CREATE DATABASE helpnet;
\c helpnet;

---------------------------------------------------------
-- TABLAS
---------------------------------------------------------

CREATE TABLE organizacion (
    nombre VARCHAR PRIMARY KEY,
    tipo VARCHAR NOT NULL
);

CREATE TABLE email_organizacion (
    nombre_organizacion VARCHAR REFERENCES organizacion(nombre),
    email VARCHAR,
    PRIMARY KEY (nombre_organizacion, email)
);

CREATE TABLE proyecto (
    id_proyecto VARCHAR PRIMARY KEY,
    nombre_organizacion VARCHAR REFERENCES organizacion(nombre),
    nombre VARCHAR NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE
);

CREATE TABLE actividad (
    id_actividad VARCHAR,
    id_proyecto VARCHAR REFERENCES proyecto(id_proyecto),
    nombre VARCHAR NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    PRIMARY KEY (id_actividad, id_proyecto)
);

CREATE TABLE localizacion (
    id_localizacion VARCHAR,
    id_actividad VARCHAR,
    id_proyecto VARCHAR,
    latitud FLOAT,
    longitud FLOAT,
    descripcion TEXT,
    observaciones TEXT,
    PRIMARY KEY (id_localizacion, id_actividad, id_proyecto),
    FOREIGN KEY (id_actividad, id_proyecto)
        REFERENCES actividad(id_actividad, id_proyecto)
);

CREATE TABLE voluntario (
    dni VARCHAR PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    fecha_alta DATE NOT NULL,
    email VARCHAR NOT NULL
);

-- Vista de edad calculada
CREATE VIEW vista_voluntarios_edad AS
SELECT 
    dni, nombre, fecha_nacimiento, fecha_alta, email,
    DATE_PART('year', AGE(CURRENT_DATE, fecha_nacimiento)) AS edad
FROM voluntario;

CREATE TABLE voluntario_skill (
    dni_voluntario VARCHAR REFERENCES voluntario(dni),
    nombre VARCHAR,
    descripcion TEXT,
    PRIMARY KEY (dni_voluntario, nombre)
);

CREATE TABLE cesion (
    nombre_organizacion VARCHAR REFERENCES organizacion(nombre),
    id_proyecto VARCHAR REFERENCES proyecto(id_proyecto),
    dni_voluntario VARCHAR REFERENCES voluntario(dni),
    fecha_cesion DATE,
    duracion VARCHAR,
    PRIMARY KEY (nombre_organizacion, id_proyecto, dni_voluntario)
);

CREATE TABLE participa (
    id_localizacion VARCHAR,
    id_actividad VARCHAR,
    id_proyecto VARCHAR,
    dni_voluntario VARCHAR REFERENCES voluntario(dni),
    rol VARCHAR,
    evaluacion INT,
    PRIMARY KEY (id_localizacion, id_actividad, id_proyecto, dni_voluntario),
    FOREIGN KEY (id_localizacion, id_actividad, id_proyecto)
        REFERENCES localizacion(id_localizacion, id_actividad, id_proyecto)
);

CREATE TABLE coordina (
    id_localizacion VARCHAR,
    id_actividad VARCHAR,
    id_proyecto VARCHAR,
    dni_voluntario VARCHAR REFERENCES voluntario(dni),
    evaluacion INT,
    PRIMARY KEY (id_localizacion, id_actividad, id_proyecto, dni_voluntario),
    FOREIGN KEY (id_localizacion, id_actividad, id_proyecto)
        REFERENCES localizacion(id_localizacion, id_actividad, id_proyecto)
);

CREATE TABLE recurso (
    id_recurso VARCHAR PRIMARY KEY,
    nombre VARCHAR,
    fecha_entrega DATE,
    descripcion TEXT,
    tipo VARCHAR CHECK (tipo IN ('donado','alquilado'))
);

CREATE TABLE recurso_usado (
    id_recurso VARCHAR REFERENCES recurso(id_recurso),
    id_proyecto VARCHAR REFERENCES proyecto(id_proyecto),
    PRIMARY KEY (id_recurso, id_proyecto)
);

CREATE TABLE recurso_donado (
    id_recurso VARCHAR PRIMARY KEY REFERENCES recurso(id_recurso),
    estado VARCHAR,
    nombre_donante VARCHAR,
    email_donante VARCHAR
);

CREATE TABLE recurso_alquilado (
    id_recurso VARCHAR PRIMARY KEY REFERENCES recurso(id_recurso),
    proveedor VARCHAR,
    costo FLOAT,
    fecha_devolucion DATE
);

---------------------------------------------------------
-- TRIGGER LIMPIEZA DE RECURSOS AL TERMINAR PROYECTOS
---------------------------------------------------------

CREATE OR REPLACE FUNCTION limpiar_recursos_proyecto()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM recurso_usado
    WHERE id_proyecto = OLD.id_proyecto
      AND id_recurso IN (
          SELECT id_recurso FROM recurso
          WHERE tipo = 'donado'
      );

    DELETE FROM recurso_usado
    WHERE id_proyecto = OLD.id_proyecto
      AND id_recurso IN (
          SELECT id_recurso FROM recurso_alquilado
          WHERE fecha_devolucion <= CURRENT_DATE
      );

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_limpiar_recursos
AFTER UPDATE OF fecha_fin OR DELETE ON proyecto
FOR EACH ROW EXECUTE FUNCTION limpiar_recursos_proyecto();