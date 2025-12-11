---------------------------------------------------------
-- Verificación de los Checks
---------------------------------------------------------

-- Se crea una organización de prueba
INSERT INTO organizacion (nombre, tipo) VALUES ('ORG_TEST', 'Pruebas');

---------------------------------------------------------
-- 1. La fecha de inicio de un proyecto debe ser anterior a la fecha de fin
---------------------------------------------------------
INSERT INTO proyecto (id_proyecto, nombre_organizacion, nombre, fecha_inicio, fecha_fin)
VALUES (777, 'ORG_TEST', 'Proy Check', '2025-12-31', '2025-01-01');

-- corrección
INSERT INTO proyecto (id_proyecto, nombre_organizacion, nombre, fecha_inicio, fecha_fin)
VALUES (777, 'ORG_TEST', 'Proy Check', '2025-01-01', '2025-12-31');

---------------------------------------------------------
-- 2. La fecha de inicio de una actividad debe ser anterior a la fecha de fin
---------------------------------------------------------
INSERT INTO actividad (id_actividad, id_proyecto, nombre, fecha_inicio, fecha_fin) 
VALUES (1, 777, 'Act Check', '2025-01-30', '2025-01-01');

-- corrección
INSERT INTO actividad (id_actividad, id_proyecto, nombre, fecha_inicio, fecha_fin) 
VALUES (1, 777, 'Act Check', '2025-01-01', '2025-01-30');

---------------------------------------------------------
-- 3. La latitud no puede ser mayor a 90
---------------------------------------------------------
INSERT INTO localizacion (id_localizacion, id_actividad, id_proyecto, latitud, longitud, descripcion)
VALUES (2, 1, 777, 91.00000000, -16.0, 'Latitud Mala');

-- corrección
INSERT INTO localizacion (id_localizacion, id_actividad, id_proyecto, latitud, longitud, descripcion)
VALUES (2, 1, 777, 90.00000000, -16.0, 'Latitud Buena');

---------------------------------------------------------
-- 4. La longitud no puede ser mayor a 180
---------------------------------------------------------
INSERT INTO localizacion (id_localizacion, id_actividad, id_proyecto, latitud, longitud, descripcion)
VALUES (3, 1, 777, 28.0, -181.00000000, 'Longitud Mala');

-- corrección
INSERT INTO localizacion (id_localizacion, id_actividad, id_proyecto, latitud, longitud, descripcion)
VALUES (3, 1, 777, 28.0, -180.00000000, 'Longitud Buena');

---------------------------------------------------------
-- 5. Los voluntarios deben ser mayores de edad
---------------------------------------------------------
INSERT INTO voluntario (dni, nombre, fecha_alta, fecha_nacimiento, email)
VALUES ('DNI_MENOR', 'Pepe Niño', '2025-01-01', '2010-01-01', 'kid@mail.com');

-- corrección
INSERT INTO voluntario (dni, nombre, fecha_alta, fecha_nacimiento, email)
VALUES ('DNI_MAYOR', 'Pepe', '2025-01-01', '2007-01-01', 'kid@mail.com');

---------------------------------------------------------
-- 6. La fecha de alta debe ser posterior a la fecha de nacimiento de un voluntario
---------------------------------------------------------
INSERT INTO voluntario (dni, nombre, fecha_alta, fecha_nacimiento, email)
VALUES ('DNI_FUT', 'Viajero Tiempo', '2023-01-01', '2025-01-01', 'fail@mail.com');

-- corrección
INSERT INTO voluntario (dni, nombre, fecha_alta, fecha_nacimiento, email)
VALUES ('DNI_FUT', 'Viajero Tiempo', '2023-01-01', '2000-01-01', 'fail@mail.com');

---------------------------------------------------------
-- 7. El tipo de un recurso esta comprendido en {A, D}
---------------------------------------------------------
INSERT INTO recurso (nombre, fecha_entrega, tipo) 
VALUES ('Cosa Rara', '2025-01-01', 'X');

-- correción
INSERT INTO recurso (nombre, fecha_entrega, tipo) 
VALUES ('Cosa Rara', '2025-01-01', 'A');

---------------------------------------------------------
-- 8. Un recurso alquilado no puede tener costo negativo
---------------------------------------------------------
INSERT INTO alquilado (id_recurso, proveedor, costo, fecha_devolucion)
VALUES (17, 'Proveedor Malo', -50.00, '2025-02-01');

-- corrección
INSERT INTO alquilado (id_recurso, proveedor, costo, fecha_devolucion)
VALUES (17, 'Proveedor Bueno', 50.00, '2025-02-01');

---------------------------------------------------------
-- 9. La evaluación de un voluntario debe estar entre 0 y 10;
---------------------------------------------------------
INSERT INTO participa (id_localizacion, id_actividad, id_proyecto, dni_voluntario, rol, evaluacion)
VALUES (2, 1, 777, 'DNI_MAYOR', 'Rol X', 11);

-- corrección 
INSERT INTO participa (id_localizacion, id_actividad, id_proyecto, dni_voluntario, rol, evaluacion)
VALUES (2, 1, 777, 'DNI_MAYOR', 'Rol X', 10);

---------------------------------------------------------
-- 10. La duración de la cesión no puede ser menor o igual a cero
---------------------------------------------------------
INSERT INTO cesion (nombre_organizacion, id_proyecto, dni_voluntario, fecha_cesion, duracion)
VALUES ('ORG_TEST', 2, 'DNI_MAYOR', '2025-01-01', 0);

-- corrección
INSERT INTO cesion (nombre_organizacion, id_proyecto, dni_voluntario, fecha_cesion, duracion)
VALUES ('ORG_TEST', 2, 'DNI_MAYOR', '2025-01-01', 10);

---------------------------------------------------------
-- LIMPIEZA DE DATOS DE PRUEBA
-- (Esta sección elimina todos los registros creados exitosamente arriba)
---------------------------------------------------------

-- 1. Eliminar Voluntarios
-- Al tener ON DELETE CASCADE, esto borrará también sus entradas en:
-- 'participa', 'coordina' y 'cesion'.
DELETE FROM voluntario 
WHERE dni IN ('DNI_MAYOR', 'DNI_FUT');

-- 2. Eliminar Organización
-- Al tener ON DELETE CASCADE, esto borrará en cadena:
-- Proyecto 777 -> Actividad 1 -> Localizaciones 2 y 3.
DELETE FROM organizacion 
WHERE nombre = 'ORG_TEST';

-- ya no existe el proyecto 777
SELECT * FROM proyecto WHERE id_proyecto = 777;

-- ya no existen actividades asociadas al proyecto 777
SELECT * FROM actividad WHERE id_proyecto = 777;

-- ya no existen localizaciones asociadas al proyecto 777
SELECT * FROM localizacion WHERE id_proyecto = 777;

-- 3. Eliminar Recursos
-- Borramos el recurso con ID 17 explícito (Caso 8)
DELETE FROM recurso 
WHERE id_recurso = 17;

-- Borramos el recurso "Cosa Rara" que se insertó con ID automático (Caso 7)
DELETE FROM recurso 
WHERE nombre = 'Cosa Rara' AND tipo = 'A';