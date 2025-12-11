---------------------------------------------------------
-- Verificación de Triggers
---------------------------------------------------------

-- Datos maestros para pruebas
INSERT INTO organizacion (nombre, tipo) VALUES ('ORG_TRIGGER_TEST', 'Testing Lab');

INSERT INTO proyecto (id_proyecto, nombre_organizacion, nombre, fecha_inicio, fecha_fin) 
VALUES (100, 'ORG_TRIGGER_TEST', 'Proyecto Base', '2025-01-01', '2025-12-31');

INSERT INTO voluntario (dni, nombre, fecha_alta, fecha_nacimiento, email) 
VALUES ('VOL_TEST', 'Voluntario Test', '2025-01-01', '2000-01-01', 'test@email.com');

---------------------------------------------------------
-- 1. Trigger que verifica que una actividad este comprendida dentro de su proyecto.
---------------------------------------------------------

INSERT INTO actividad (id_actividad, id_proyecto, nombre, fecha_inicio, fecha_fin)
VALUES (1, 100, 'Actividad Futura', '2026-01-01', '2026-01-05');


---------------------------------------------------------
-- 2. Trigger que verifica que, al ceder un voluntario, la fecha de cesión 
--    este comprendida en el nuevo proyecto.
---------------------------------------------------------

INSERT INTO cesion (nombre_organizacion, id_proyecto, dni_voluntario, fecha_cesion, duracion)
VALUES ('ORG_TRIGGER_TEST', 100, 'VOL_TEST', '2024-01-01', 30);


---------------------------------------------------------
-- 3. Trigger que verifica que un voluntario participa o coordina una actividad, pero no ambas.
---------------------------------------------------------

-- Crear actividad válida
INSERT INTO actividad (id_actividad, id_proyecto, nombre, fecha_inicio, fecha_fin)
VALUES (1, 999, 'Actividad_TGR', '2025-01-01', '2025-01-05');

-- Crear localización válida
INSERT INTO localizacion (id_localizacion, id_actividad, id_proyecto, latitud, longitud, descripcion)
VALUES (1, 1, 999, 28.0, -16.0, 'Zona Pruebas');

-- El voluntario participa
INSERT INTO participa (id_localizacion, id_actividad, id_proyecto, dni_voluntario, rol)
VALUES (1, 1, 999, 'VOL_TEST', 'Médico');


-- Intento: Asignar rol de COORDINA (Debe fallar porque ya participa)
INSERT INTO coordina (id_localizacion, id_actividad, id_proyecto, dni_voluntario)
VALUES (1, 1, 999, 'VOL_TEST');


---------------------------------------------------------
-- 4. Trigger que verifica que un recurso es donado o alquilado, pero no puede ser ambas.
---------------------------------------------------------

-- 1. Insertamos un recurso Padre de tipo 'D' (Donado)
INSERT INTO recurso (id_recurso, nombre, fecha_entrega, tipo) 
VALUES (400, 'Mantas Térmicas', '2025-01-01', 'D');

-- 2. INTENTO FALLIDO: Insertarlo en la tabla hija ALQUILADO
INSERT INTO alquilado (id_recurso, proveedor, costo, fecha_devolucion)
VALUES (400, 'Empresa Error', 500.00, '2025-02-01');


---------------------------------------------------------
-- 5. Trigger para la limpieza de datos en recurso_usado cuando se finaliza anticipadamente un proyecto.
---------------------------------------------------------

-- Crear Recurso para la prueba
INSERT INTO recurso (id_recurso, nombre, fecha_entrega, tipo) 
VALUES (500, 'Generador', '2025-01-01', 'A');

INSERT INTO alquilado (id_recurso, proveedor, costo, fecha_devolucion) 
VALUES (500, 'PowerRent', 100.00, '2025-12-31');

-- Asignarlo al Proyecto 100
INSERT INTO recurso_usado (id_proyecto, id_recurso) VALUES (100, 500);

-- Finalizamos el proyecto anticipadamente (ayer)
UPDATE proyecto SET fecha_fin = CURRENT_DATE - 1 WHERE id_proyecto = 100;

-- Esta consulta debe dar 0 filas (se liberó el recurso):
SELECT * FROM recurso_usado WHERE id_proyecto = 100 AND id_recurso = 500;


---------------------------------------------------------
-- 6. Trigger que verifica que no se puede añadir una localización a una actividad finalizada.
---------------------------------------------------------

-- Creamos un proyecto y una actividad que ya terminaron
INSERT INTO proyecto (id_proyecto, nombre_organizacion, nombre, fecha_inicio, fecha_fin) 
VALUES (700, 'ORG_TRIGGER_TEST', 'Proyecto Antiguo', '2020-01-01', '2020-12-31');

INSERT INTO actividad (id_actividad, id_proyecto, nombre, fecha_inicio, fecha_fin)
VALUES (1, 700, 'Actividad Cerrada', '2020-02-01', '2020-02-10');

-- Intentamos añadir una nueva localización HOY a esa actividad de 2020.
INSERT INTO localizacion (id_localizacion, id_actividad, id_proyecto, latitud, longitud, descripcion)
VALUES (1, 1, 700, 28.5, -16.5, 'Puesto Olvidado');


---------------------------------------------------------
-- 7. Trigger que verifica que un voluntario no puede hacer actividades que se solapen.
---------------------------------------------------------

-- Creamos un proyecto nuevo
INSERT INTO proyecto (id_proyecto, nombre_organizacion, nombre, fecha_inicio, fecha_fin) 
VALUES (800, 'ORG_TRIGGER_TEST', 'Proyecto Agenda', '2026-01-01', '2026-12-31');

-- Creamos DOS actividades que se solapan en el tiempo

-- Actividad A: Del 1 al 10 de Junio
INSERT INTO actividad (id_actividad, id_proyecto, nombre, fecha_inicio, fecha_fin)
VALUES (10, 800, 'Misión Junio A', '2026-06-01', '2026-06-10');

INSERT INTO localizacion (id_localizacion, id_actividad, id_proyecto, latitud, longitud, descripcion)
VALUES (10, 10, 800, 28.0, -16.0, 'Base A');

-- Actividad B: Del 5 al 15 de Junio
INSERT INTO actividad (id_actividad, id_proyecto, nombre, fecha_inicio, fecha_fin)
VALUES (11, 800, 'Misión Junio B', '2026-06-05', '2026-06-15');

INSERT INTO localizacion (id_localizacion, id_actividad, id_proyecto, latitud, longitud, descripcion)
VALUES (11, 11, 800, 28.1, -16.1, 'Base B');

--Asignamos al voluntario a la primera misión (Esto funciona bien)
INSERT INTO participa (id_localizacion, id_actividad, id_proyecto, dni_voluntario, rol)
VALUES (10, 10, 800, 'VOL_TEST', 'Conductor');

-- Intentamos asignarlo a la segunda actividad, que choca en fechas.
INSERT INTO participa (id_localizacion, id_actividad, id_proyecto, dni_voluntario, rol)
VALUES (11, 11, 800, 'VOL_TEST', 'Enfermero');


---------------------------------------------------------
-- LIMPIEZA TOTAL DE DATOS DE PRUEBA DE TRIGGERS
---------------------------------------------------------

-- 1. Eliminar al Voluntario de prueba
DELETE FROM voluntario 
WHERE dni = 'VOL_TEST';

-- 2. Eliminar la Organización de prueba
DELETE FROM organizacion 
WHERE nombre = 'ORG_TRIGGER_TEST';

-- 3. Eliminar el Proyecto 999 (Usado en el Trigger 3)
DELETE FROM proyecto 
WHERE id_proyecto = 999;

-- 4. Eliminar los Recursos de prueba
DELETE FROM recurso 
WHERE id_recurso IN (400, 500);