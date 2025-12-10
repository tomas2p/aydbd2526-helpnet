---------------------------------------------------------
-- INSERCIÓN DE DATOS COMPLETA
---------------------------------------------------------

--------------------------------------------------------------------------------
-- 1. ORGANIZACIONES (6 organizaciones variadas)
--------------------------------------------------------------------------------

INSERT INTO organizacion (nombre, tipo) VALUES
('Cruz Roja Española', 'Humanitaria'),
('Médicos Sin Fronteras', 'Médica'),
('Greenpeace', 'Ecologista'),
('WWF', 'Conservación'),
('Caritas', 'Benéfica'),
('Save The Children', 'Infancia');

INSERT INTO email_organizacion (nombre_organizacion, email) VALUES
('Cruz Roja Española', 'contacto@cruzroja.es'),
('Cruz Roja Española', 'voluntariado@cruzroja.es'),
('Médicos Sin Fronteras', 'info@msf.es'),
('Greenpeace', 'spain@greenpeace.org'),
('Greenpeace', 'socios@greenpeace.org'),
('WWF', 'info@wwf.es'),
('Caritas', 'donaciones@caritas.es'),
('Save The Children', 'espana@savethechildren.org');


--------------------------------------------------------------------------------
-- 2. VOLUNTARIOS (15 personas cubriendo todas las edades)
--------------------------------------------------------------------------------

INSERT INTO voluntario (dni, nombre, fecha_nacimiento, fecha_alta, email) VALUES
-- Veteranos (40+ años)
('10000001A', 'Juan Pérez', '1980-01-01', '2010-05-20', 'juan@mail.com'),
('10000002B', 'Ana Gómez', '1985-06-15', '2012-08-10', 'ana@mail.com'),
('10000003C', 'Luis Ruiz', '1975-12-01', '2015-01-01', 'luis@mail.com'),
-- Adultos (30-39 años)
('20000001D', 'María López', '1990-03-20', '2018-02-15', 'maria@mail.com'),
('20000002E', 'Carlos Díaz', '1992-07-07', '2019-11-30', 'carlos@mail.com'),
('20000003F', 'Elena Martínez', '1995-09-09', '2020-03-01', 'elena@mail.com'),
('20000004G', 'Pedro Sánchez', '1988-04-04', '2021-01-10', 'pedro@mail.com'),
-- Jóvenes (20-29 años)
('30000001H', 'Sofía García', '2000-06-15', '2023-06-16', 'sofia@mail.com'),
('30000002I', 'Miguel Torres', '1999-05-05', '2022-05-06', 'miguel@mail.com'),
('30000003J', 'Laura Fernández', '2001-11-11', '2022-11-12', 'laura@mail.com'),
-- Muy jóvenes (18-19 años)
('40000001K', 'David López', '2007-01-15', '2025-01-16', 'david@mail.com'),
('40000002L', 'Clara Rodríguez', '2006-08-20', '2024-08-21', 'clara@mail.com'),
('40000003M', 'Pablo Jiménez', '2006-03-10', '2024-03-11', 'pablo@mail.com'),
-- Internacionales
('50000001N', 'John Smith', '1982-09-30', '2023-01-15', 'john@mail.com'),
('50000002O', 'Marie Curie', '1990-12-25', '2024-02-01', 'marie@mail.com');

-- Skills variadas
INSERT INTO voluntario_skill (dni_voluntario, nombre_skill, descripcion) VALUES
('10000001A', 'Conducción 4x4', 'Experiencia en terreno difícil'),
('10000001A', 'Mecánica', 'Básica'),
('10000002B', 'Medicina', 'Médico generalista colegiado'),
('10000002B', 'Inglés', 'Nivel C1'),
('20000001D', 'Enfermería', 'Grado universitario'),
('20000002E', 'Logística', 'Gestión de almacenes'),
('20000002E', 'Primeros Auxilios', 'Certificado Cruz Roja'),
('30000001H', 'Redes Sociales', 'Gestión de comunidades'),
('30000002I', 'Fotografía', 'Equipo profesional'),
('40000001K', 'Idiomas', 'Francés e inglés'),
('50000001N', 'Traducción', 'Inglés nativo'),
('50000002O', 'Investigación', 'Doctorado en Biología');

--------------------------------------------------------------------------------
-- 3. PROYECTOS (15 proyectos cubriendo todos los estados temporales)
--------------------------------------------------------------------------------
-- NOTA: Fecha al momento de ejecución 09/12/2025


-- PROYECTOS FINALIZADOS (fecha_fin < '2025-12-09')
INSERT INTO proyecto (nombre_organizacion, nombre, descripcion, fecha_inicio, fecha_fin) VALUES
('Cruz Roja Española', 'Vacunación Gripal 2024', 'Campaña invierno rural', '2024-01-01', '2024-03-31'),
('Cruz Roja Española', 'Emergencia Inundaciones 2024', 'Ayuda zonas afectadas', '2024-11-01', '2024-12-15'),
('Médicos Sin Fronteras', 'Respuesta Ébola 2024', 'África occidental', '2024-02-01', '2024-04-30'),
('Greenpeace', 'Limpieza Costera 2024', 'Playas de Galicia', '2024-06-01', '2024-06-30'),
('WWF', 'Censo de Linces 2024', 'Censo anual', '2024-03-01', '2024-03-15');

-- PROYECTOS EN CURSO (fecha_inicio <= '2025-12-09' <= fecha_fin)
INSERT INTO proyecto (nombre_organizacion, nombre, descripcion, fecha_inicio, fecha_fin) VALUES
('Caritas', 'Comedor Social Centro', 'Desayunos y cenas diarias', '2025-01-01', '2025-12-31'),
('Save The Children', 'Apoyo Escolar 2025', 'Refuerzo educativo', '2025-09-15', '2026-06-20'),
('Cruz Roja Española', 'Atención Personas Mayores', 'Acompañamiento semanal', '2025-01-01', '2025-12-31'),
('Greenpeace', 'Reforestación Sierra 2025', 'Plantación 10,000 árboles', '2025-10-01', '2025-11-30'),
('Médicos Sin Fronteras', 'Clínica Móvil Rural', 'Atención primaria itinerante', '2025-03-01', '2026-02-28');

-- PROYECTOS FUTUROS (fecha_inicio > '2025-12-09')
INSERT INTO proyecto (nombre_organizacion, nombre, descripcion, fecha_inicio, fecha_fin) VALUES
('WWF', 'Censo de Oso Pardo 2026', 'Seguimiento población', '2026-03-01', '2026-03-31'),
('Caritas', 'Ropero Solidario 2026', 'Gestión de ropa usada', '2026-01-01', '2026-12-31'),
('Save The Children', 'Campaña Navidad 2025', 'Recogida de juguetes', '2025-12-18', '2026-01-10'),
('Cruz Roja Española', 'Emergencia Frío 2025', 'Plan invierno', '2025-12-20', '2026-02-28'),
('Greenpeace', 'Expedición Antártida 2026', 'Investigación cambio climático', '2026-01-10', '2026-03-31');

TRUNCATE TABLE proyecto CASCADE;

--------------------------------------------------------------------------------
-- 4. ACTIVIDADES (MINIMO 2 por proyecto finalizado/en curso)
--------------------------------------------------------------------------------

-- PROYECTO 1: Vacunación Gripal 2024 (FINALIZADO) - 3 actividades
INSERT INTO actividad (id_proyecto, id_actividad, nombre, descripcion, fecha_inicio, fecha_fin) VALUES
(1, 1, 'Logística y Distribución', 'Transporte neveras y material', '2024-01-02', '2024-01-10'),
(1, 2, 'Vacunación Fase 1', 'Mayores 80 y riesgo', '2024-01-11', '2024-02-10'),
(1, 3, 'Vacunación Fase 2', 'Población general', '2024-02-11', '2024-03-30');

-- PROYECTO 2: Emergencia Inundaciones 2024 (FINALIZADO) - 2 actividades
INSERT INTO actividad (id_proyecto, id_actividad, nombre, descripcion, fecha_inicio, fecha_fin) VALUES
(2, 1, 'Rescate Personas', 'Equipos de rescate acuático', '2024-11-01', '2024-11-10'),
(2, 2, 'Distribución Ayuda', 'Alimentos y mantas', '2024-11-11', '2024-12-15');

-- PROYECTO 3: Respuesta Ébola 2024 (FINALIZADO) - 3 actividades
INSERT INTO actividad (id_proyecto, id_actividad, nombre, descripcion, fecha_inicio, fecha_fin) VALUES
(3, 1, 'Montaje Hospital Campaña', 'Instalación módulos', '2024-02-01', '2024-02-15'),
(3, 2, 'Tratamiento Pacientes', 'Atención médica directa', '2024-02-16', '2024-04-15'),
(3, 3, 'Prevención Comunitaria', 'Educación sanitaria', '2024-03-01', '2024-04-30');

-- PROYECTO 4: Limpieza Costera 2024 (FINALIZADO) - 2 actividades
INSERT INTO actividad (id_proyecto, id_actividad, nombre, descripcion, fecha_inicio, fecha_fin) VALUES
(4, 1, 'Recogida Plásticos', 'Zona arena y rocas', '2024-06-01', '2024-06-15'),
(4, 2, 'Limpieza Submarina', 'Buceo profesional', '2024-06-16', '2024-06-30');

-- PROYECTO 5: Censo de Linces 2024 (FINALIZADO) - 2 actividades
INSERT INTO actividad (id_proyecto, id_actividad, nombre, descripcion, fecha_inicio, fecha_fin) VALUES
(5, 1, 'Instalación Cámaras', 'Trampeo fotográfico', '2024-03-01', '2024-03-08'),
(5, 2, 'Análisis de Datos', 'Procesamiento imágenes', '2024-03-09', '2024-03-15');

-- PROYECTO 6: Comedor Social Centro (EN CURSO) - 3 actividades
INSERT INTO actividad (id_proyecto, id_actividad, nombre, descripcion, fecha_inicio, fecha_fin) VALUES
(6, 1, 'Servicio Desayunos', '7am a 9am diario', '2025-01-01', '2025-12-31'),
(6, 2, 'Servicio Cenas', '8pm a 10pm diario', '2025-01-01', '2025-12-31'),
(6, 3, 'Preparación Alimentos', 'Cocina central', '2025-01-01', '2025-12-31');

-- PROYECTO 7: Apoyo Escolar 2025 (EN CURSO) - 3 actividades
INSERT INTO actividad (id_proyecto, id_actividad, nombre, descripcion, fecha_inicio, fecha_fin) VALUES
(7, 1, 'Refuerzo Matemáticas', 'Lunes y miércoles', '2025-09-15', '2026-06-20'),
(7, 2, 'Refuerzo Lengua', 'Martes y jueves', '2025-09-15', '2026-06-20'),
(7, 3, 'Actividades Lúdicas', 'Viernes por la tarde', '2025-09-15', '2026-06-20');

-- PROYECTO 8: Atención Personas Mayores (EN CURSO) - 2 actividades
INSERT INTO actividad (id_proyecto, id_actividad, nombre, descripcion, fecha_inicio, fecha_fin) VALUES
(8, 1, 'Acompañamiento Domiciliario', 'Visitas a domicilio', '2025-01-01', '2025-12-31'),
(8, 2, 'Talleres Sociales', 'Centros de día', '2025-01-01', '2025-12-31');

-- PROYECTO 9: Reforestación Sierra 2025 (EN CURSO - recién terminado) - 3 actividades
INSERT INTO actividad (id_proyecto, id_actividad, nombre, descripcion, fecha_inicio, fecha_fin) VALUES
(9, 1, 'Preparación Terreno', 'Limpieza y acondicionamiento', '2025-10-01', '2025-10-15'),
(9, 2, 'Plantación Árboles', 'Plantación especies autóctonas', '2025-10-16', '2025-11-20'),
(9, 3, 'Seguimiento Post-plantación', 'Riego y mantenimiento', '2025-11-21', '2025-11-30');

-- PROYECTO 10: Clínica Móvil Rural (EN CURSO) - 2 actividades
INSERT INTO actividad (id_proyecto, id_actividad, nombre, descripcion, fecha_inicio, fecha_fin) VALUES
(10, 1, 'Consultas Médicas', 'Atención primaria', '2025-03-01', '2026-02-28'),
(10, 2, 'Campañas Vacunación', 'Pueblos remotos', '2025-03-01', '2026-02-28');

-- PROYECTOS FUTUROS (11-15): Estos PUEDEN no tener actividades aún
-- O puedes añadir actividades planeadas (opcional)
INSERT INTO actividad (id_proyecto, id_actividad, nombre, descripcion, fecha_inicio, fecha_fin) VALUES
-- Proyecto 11: Censo de Oso Pardo 2026 (FUTURO)
(11, 1, 'Preparación Expedición', 'Logística y equipo', '2026-02-15', '2026-02-28'),
(11, 2, 'Trabajo Campo', 'Rastreo y observación', '2026-03-01', '2026-03-20'),
-- Proyecto 13: Campaña Navidad 2025 (FUTURO - pero fecha_inicio cercana)
(13, 1, 'Recogida de Juguetes', 'Puntos de donación', '2025-12-18', '2026-01-05'),
(13, 2, 'Distribución Regalos', 'Entregas a familias', '2025-12-20', '2026-01-10'),
-- Proyecto 14: Emergencia Frío 2025 (FUTURO - pero muy pronto)
(14, 1, 'Distribución Mantas', 'Puntos calientes ciudad', '2025-12-20', '2026-01-20'),
(14, 2, 'Albergues Nocturnos', 'Apertura espacios calefactados', '2025-12-20', '2026-02-20'),
(14, 3, 'Atención Calle', 'Rutas personas sin hogar', '2025-12-20', '2026-02-28');

--------------------------------------------------------------------------------
-- 5. LOCALIZACIONES
--------------------------------------------------------------------------------

-- PROYECTO 1: Vacunación Gripal 2024
-- Actividad 1.1: Logística y Distribución (2 localizaciones)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(1, 1, 1, 'Almacén Central - Recepción', 40.4168, -3.7038, '24h acceso autorizado'),
(1, 1, 2, 'Centro Distribución Norte', 40.4500, -3.6900, 'Neveras especiales');

-- Actividad 1.2: Vacunación Fase 1 (3 localizaciones - MAYORES)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(1, 2, 1, 'Carpa Plaza Mayor - Centro', 40.4168, -3.7038, 'Acceso ambulancias prioritario'),
(1, 2, 2, 'Centro de Salud Norte', 40.4500, -3.6900, 'Sala de espera habilitada'),
(1, 2, 3, 'Residencia Tercera Edad', 40.3800, -3.7500, 'Vacunación in situ');

-- Actividad 1.3: Vacunación Fase 2 (2 localizaciones - GENERAL)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(1, 3, 1, 'Polideportivo Municipal Sur', 40.3800, -3.7500, 'Parking gratuito 500 plazas'),
(1, 3, 2, 'Centro Cultural Este', 40.4200, -3.6700, 'Metro directo');

-- PROYECTO 2: Emergencia Inundaciones 2024
-- Actividad 2.1: Rescate Personas (3 localizaciones críticas)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(2, 1, 1, 'Zona Industrial Inundada', 41.6500, -0.8800, 'Riesgo eléctrico'),
(2, 1, 2, 'Barrio Las Flores', 41.6550, -0.8850, 'Evacuación urgente'),
(2, 1, 3, 'Puente Viejo', 41.6600, -0.8900, 'Estructura comprometida');

-- Actividad 2.2: Distribución Ayuda (2 localizaciones)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(2, 2, 1, 'Pabellón Deportivo Refugio', 41.6500, -0.8750, 'Capacidad 500 personas'),
(2, 2, 2, 'Colegio Público Acogida', 41.6450, -0.8800, 'Solo material');

-- PROYECTO 3: Respuesta Ébola 2024
-- Actividad 3.1: Montaje Hospital Campaña (1 localización)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(3, 1, 1, 'Campo Base MSF - Conakry', 9.6412, -13.5784, 'Zona de cuarentena nivel 4');

-- Actividad 3.2: Tratamiento Pacientes (2 localizaciones)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(3, 2, 1, 'Hospital de Campaña - Zona Roja', 9.6450, -13.5800, 'Acceso restringido'),
(3, 2, 2, 'Centro de Tratamiento Comunitario', 9.6350, -13.5850, 'Casos leves');

-- Actividad 3.3: Prevención Comunitaria (3 localizaciones)

INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(3, 3, 1, 'Mercado Central - Punto Información', 9.6400, -13.5750, 'Gran afluencia'),
(3, 3, 2, 'Escuela Primaria', 9.6300, -13.5900, 'Talleres niños'),
(3, 3, 3, 'Centro de Salud Rural', 9.6200, -13.6000, 'Formación personal');

-- PROYECTO 4: Limpieza Costera 2024
-- Actividad 4.1: Recogida Plásticos (3 playas diferentes)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(4, 1, 1, 'Playa de Rodas - Cíes', 42.2220, -8.9000, 'Zona natural protegida'),
(4, 1, 2, 'Playa de Samil', 42.2100, -8.7800, 'Acceso fácil, mucha basura'),
(4, 1, 3, 'Playa de Langosteira', 42.9050, -9.2600, 'Corrientes fuertes');

-- Actividad 4.2: Limpieza Submarina (2 localizaciones submarinas)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(4, 2, 1, 'Fondeadero Bahía San Simón', 42.3200, -8.6500, 'Profundidad 8-12m'),
(4, 2, 2, 'Zona Puertos Deportivos', 42.2400, -8.7200, 'Redes abandonadas');

-- PROYECTO 5: Censo de Linces 2024
-- Actividad 5.1: Instalación Cámaras (3 localizaciones en Sierra Morena)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(5, 1, 1, 'Sector Norte - Corredor Ecológico', 38.1500, -4.1000, 'Zona paso linces'),
(5, 1, 2, 'Sector Centro - Zona Alimentación', 38.1200, -4.0800, 'Punto agua permanente'),
(5, 1, 3, 'Sector Sur - Área Reproducción', 38.1000, -4.0600, 'Madrigueras observadas');

-- Actividad 5.2: Análisis de Datos (1 localización)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(5, 2, 1, 'Centro de Investigación WWF', 38.1300, -4.0900, 'Oficina principal');

-- PROYECTO 6: Comedor Social Centro
-- Actividad 6.1: Servicio Desayunos (2 localizaciones)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(6, 1, 1, 'Parroquia San Juan - Cocina', 41.3851, 2.1734, 'Cocina industrial completa'),
(6, 1, 2, 'Parroquia San Juan - Comedor', 41.3850, 2.1735, 'Aforo 50 personas, calefacción');

-- Actividad 6.2: Servicio Cenas (1 localización - misma cocina, comedor diferente)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(6, 2, 1, 'Parroquia San Juan - Comedor Noche', 41.3850, 2.1735, 'Mismo local, turno noche');

-- Actividad 6.3: Preparación Alimentos (1 localización)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(6, 3, 1, 'Cocina Central - Zona Preparación', 41.3851, 2.1734, 'Exclusivo personal');

-- PROYECTO 7: Apoyo Escolar 2025
-- Actividad 7.1: Refuerzo Matemáticas (3 aulas diferentes)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(7, 1, 1, 'Aula 101 - Primaria', 40.4300, -3.7000, 'Material específico matemáticas'),
(7, 1, 2, 'Aula 102 - Secundaria', 40.4300, -3.7000, 'Pizarras digitales'),
(7, 1, 3, 'Biblioteca - Grupo Avanzado', 40.4300, -3.7000, 'Máximo 8 alumnos');

-- Actividad 7.2: Refuerzo Lengua (2 aulas)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(7, 2, 1, 'Aula 201 - Primaria', 40.4300, -3.7000, 'Rincon lectura'),
(7, 2, 2, 'Aula 202 - Secundaria', 40.4300, -3.7000, 'Ordenadores disponibles');

-- Actividad 7.3: Actividades Lúdicas (2 localizaciones)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(7, 3, 1, 'Patio Cubierto', 40.4300, -3.7000, 'Zona juegos exteriores'),
(7, 3, 2, 'Sala Multiusos', 40.4300, -3.7000, 'Proyector y sonido');

-- PROYECTO 8: Atención Personas Mayores
-- Actividad 8.1: Acompañamiento Domiciliario (3 domicilios ejemplo)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(8, 1, 1, 'Domicilio Sra. Carmen - Centro', 40.4200, -3.7100, '3º piso sin ascensor'),
(8, 1, 2, 'Domicilio Sr. Antonio - Norte', 40.4500, -3.6900, 'Planta baja, jardín'),
(8, 1, 3, 'Domicilio Sra. Rosa - Oeste', 40.4100, -3.7500, 'Necesita ayuda compras');

-- Actividad 8.2: Talleres Sociales (2 centros)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(8, 2, 1, 'Centro de Día "Los Álamos"', 40.4300, -3.7000, 'Taller manualidades'),
(8, 2, 2, 'Residencia "Buen Anciano"', 40.4400, -3.7200, 'Actividades grupales');

-- PROYECTO 9: Reforestación Sierra 2025
-- Actividad 9.1: Preparación Terreno (2 sectores)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(9, 1, 1, 'Sector Norte - Limpieza Matorral', 40.5000, -3.8000, 'Pendiente moderada, maquinaria'),
(9, 1, 2, 'Sector Sur - Eliminación Especies Invasoras', 40.5100, -3.7900, 'Trabajo manual');

-- Actividad 9.2: Plantación Árboles (4 localizaciones en la sierra)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(9, 2, 1, 'Sector Norte - Ladera Robles', 40.5000, -3.8000, 'Pendiente moderada, 500 árboles'),
(9, 2, 2, 'Sector Centro - Valle Fresnos', 40.5100, -3.7900, 'Cerca arroyo, 300 árboles'),
(9, 2, 3, 'Sector Sur - Meseta Encinas', 40.5200, -3.7800, 'Zona más seca, 200 árboles'),
(9, 2, 4, 'Área Recreativa - Mixto', 40.5050, -3.7950, 'Plantación educativa, 100 árboles');

-- Actividad 9.3: Seguimiento Post-plantación (3 localizaciones de seguimiento)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(9, 3, 1, 'Punto Control Norte - Riego', 40.5000, -3.8000, 'Depósito agua 5000L'),
(9, 3, 2, 'Punto Control Centro - Supervivencia', 40.5100, -3.7900, 'Muestreo estadístico'),
(9, 3, 3, 'Punto Control Sur - Protección', 40.5200, -3.7800, 'Protección contra herbívoros');

-- PROYECTO 10: Clínica Móvil Rural
-- Actividad 10.1: Consultas Médicas (3 pueblos atendidos)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(10, 1, 1, 'Pueblo Valverde - Plaza Ayuntamiento', 40.3000, -3.9000, '1er martes cada mes'),
(10, 1, 2, 'Aldea Los Pinos - Antigua Escuela', 40.2800, -3.9500, '3er jueves cada mes'),
(10, 1, 3, 'Caserío El Monte - Consultorio', 40.3200, -3.8500, 'Fines de semana alternos');

-- Actividad 10.2: Campañas Vacunación (2 localizaciones principales)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(10, 2, 1, 'Centro de Salud Comarcal', 40.3500, -3.8800, 'Campaña masiva'),
(10, 2, 2, 'Colegio Rural Agrupado', 40.3300, -3.9200, 'Vacunación escolar');

-- PROYECTO 11: Censo de Oso Pardo 2026 (FUTURO)
-- Actividad 11.1: Preparación Expedición (2 localizaciones)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(11, 1, 1, 'Base Operaciones - Potes', 43.1500, -4.6200, 'Centro logístico'),
(11, 1, 2, 'Almacén Equipamiento', 43.1600, -4.6300, 'Material especializado');

-- Actividad 11.2: Trabajo Campo (3 localizaciones en Picos de Europa)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(11, 2, 1, 'Sector Liébana - Zona Osera', 43.1800, -4.6500, 'Rastros frecuentes'),
(11, 2, 2, 'Valle de Cereceda', 43.2000, -4.6800, 'Área alimentación'),
(11, 2, 3, 'Puerto de San Glorio', 43.2200, -4.7000, 'Paso migratorio');

-- PROYECTO 13: Campaña Navidad 2025 (FUTURO)
-- Actividad 13.1: Recogida de Juguetes (3 puntos de donación)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(13, 1, 1, 'Centro Comercial Norte', 40.4700, -3.6900, 'Punto información'),
(13, 1, 2, 'Mercado Municipal', 40.4200, -3.7000, 'Carpa recogida'),
(13, 1, 3, 'Oficinas Save The Children', 40.4300, -3.7100, 'Recogida permanente');


-- Actividad 13.2: Distribución Regalos (2 localizaciones)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(13, 2, 1, 'Almacén Regalos - Logística', 40.4400, -3.7200, 'Clasificación y empaquetado'),
(13, 2, 2, 'Puntos de Entrega Familias', 40.4500, -3.7300, 'Distribución directa');

-- PROYECTO 14: Emergencia Frío 2025 (FUTURO)
-- Actividad 14.1: Distribución Mantas (3 puntos calientes)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(14, 1, 1, 'Estación de Atocha - Vestíbulo', 40.4068, -3.6894, '24h, personal rotativo'),
(14, 1, 2, 'Plaza Callao - Carpa', 40.4194, -3.7038, '19:00-23:00'),
(14, 1, 3, 'Mercado de San Miguel - Exterior', 40.4151, -3.7084, 'Fin de semana');

-- Actividad 14.2: Albergues Nocturnos (2 albergues)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(14, 2, 1, 'Albergue Municipal Centro', 40.4100, -3.7000, 'Capacidad 100 camas'),
(14, 2, 2, 'Albergue Iglesia San Francisco', 40.4250, -3.7150, 'Capacidad 50 camas');

-- Actividad 14.3: Atención Calle (3 rutas diferentes)
INSERT INTO localizacion (id_proyecto, id_actividad, id_localizacion, descripcion, latitud, longitud, observaciones) VALUES
(14, 3, 1, 'Ruta Centro Histórico', 40.4150, -3.7050, 'Equipo 1, 22:00-02:00'),
(14, 3, 2, 'Ruta Estaciones Transporte', 40.4200, -3.6900, 'Equipo 2, 21:00-01:00'),
(14, 3, 3, 'Ruta Parques y Jardines', 40.4300, -3.7100, 'Equipo 3, 23:00-03:00');

--------------------------------------------------------------------------------
-- 6. PARTICIPA (Voluntarios en TODAS las localizaciones de proyectos PASADOS/EN CURSO)
--------------------------------------------------------------------------------

-- PROYECTO 1: Vacunación Gripal 2024 (FINALIZADO - TODAS las localizaciones cubiertas)
INSERT INTO participa (dni_voluntario, id_proyecto, id_actividad, id_localizacion, rol, evaluacion) VALUES
-- Localización 1.1.1
('10000001A', 1, 1, 1, 'Responsable Logística', 9),
('20000002E', 1, 1, 1, 'Operario Almacén', 8),
-- Localización 1.1.2
('20000003F', 1, 1, 2, 'Conductor Frigorífico', 7),
('30000001H', 1, 1, 2, 'Ayudante Carga', 6),
('40000001K', 1, 1, 2, 'Control Temperatura', 8),
-- Localización 1.2.1
('10000002B', 1, 2, 1, 'Médico Responsable', 10),
('20000001D', 1, 2, 1, 'Enfermera Jefe', 9),
('30000002I', 1, 2, 1, 'Auxiliar Vacunación', 8),
('40000002L', 1, 2, 1, 'Recepcionista', 7),
-- Localización 1.2.2
('20000004G', 1, 2, 2, 'Médico Sustituto', 9),
('30000003J', 1, 2, 2, 'Enfermera', 8),
('40000003M', 1, 2, 2, 'Registro Pacientes', 7),
-- Localización 1.2.3
('50000001N', 1, 2, 3, 'Médico Geriátrico', 9),
('50000002O', 1, 2, 3, 'Apoyo Psicológico', 8),
-- Localización 1.3.1
('10000003C', 1, 3, 1, 'Coordinador Vacunación', 10),
('20000001D', 1, 3, 1, 'Enfermera', 9),
('30000001H', 1, 3, 1, 'Auxiliar', 8),
-- Localización 1.3.2
('20000002E', 1, 3, 2, 'Logística Punto', 8),
('40000001K', 1, 3, 2, 'Información', 7);

-- PROYECTO 2: Emergencia Inundaciones 2024 (FINALIZADO)
INSERT INTO participa (dni_voluntario, id_proyecto, id_actividad, id_localizacion, rol, evaluacion) VALUES
-- Localización 2.1.1
('10000001A', 2, 1, 1, 'Rescatista', 10),
('10000003C', 2, 1, 1, 'Líder Equipo', 9),
-- Localización 2.1.2
('20000003F', 2, 1, 2, 'Rescatista', 8),
('30000002I', 2, 1, 2, 'Ayudante Rescate', 7),
-- Localización 2.1.3
('20000002E', 2, 1, 3, 'Ingeniero Estructuras', 9),
('40000001K', 2, 1, 3, 'Asistente', 7),
-- Localización 2.2.1
('10000002B', 2, 2, 1, 'Coordinadora Ayuda', 10),
('20000001D', 2, 2, 1, 'Distribución', 9),
-- Localización 2.2.2
('30000003J', 2, 2, 2, 'Almacenera', 8),
('40000002L', 2, 2, 2, 'Clasificación', 7);

-- PROYECTO 3: Respuesta Ébola 2024 (FINALIZADO)
INSERT INTO participa (dni_voluntario, id_proyecto, id_actividad, id_localizacion, rol, evaluacion) VALUES
-- Localización 3.1.1
('50000001N', 3, 1, 1, 'Coordinador Montaje', 10),
('20000004G', 3, 1, 1, 'Técnico', 9),
-- Localización 3.2.1
('10000002B', 3, 2, 1, 'Médico Zona Roja', 10),
('20000001D', 3, 2, 1, 'Enfermera', 10),
-- Localización 3.2.2
('30000001H', 3, 2, 2, 'Auxiliar Médico', 8),
('40000003M', 3, 2, 2, 'Registro', 7),
-- Localización 3.3.1
('50000002O', 3, 3, 1, 'Educadora Salud', 9),
('10000001A', 3, 3, 1, 'Logística', 8),
-- Localización 3.3.2
('20000002E', 3, 3, 2, 'Coordinador Talleres', 9),
('30000002I', 3, 3, 2, 'Monitor', 8),
-- Localización 3.3.3
('10000003C', 3, 3, 3, 'Formador', 9),
('40000001K', 3, 3, 3, 'Traductor', 8);

-- PROYECTO 4: Limpieza Costera 2024 (FINALIZADO)
INSERT INTO participa (dni_voluntario, id_proyecto, id_actividad, id_localizacion, rol, evaluacion) VALUES
-- Localización 4.1.1
('30000003J', 4, 1, 1, 'Coordinadora Playa', 9),
('40000002L', 4, 1, 1, 'Recogida', 8),
-- Localización 4.1.2
('30000001H', 4, 1, 2, 'Coordinación Redes', 8),
('20000003F', 4, 1, 2, 'Voluntaria', 7),
-- Localización 4.1.3
('10000001A', 4, 1, 3, 'Conductor Camión', 9),
('50000001N', 4, 1, 3, 'Supervisor', 8),
-- Localización 4.2.1
('10000003C', 4, 2, 1, 'Buceador Jefe', 10),
('20000002E', 4, 2, 1, 'Buceador', 9),
-- Localización 4.2.2
('10000002B', 4, 2, 2, 'Médico de Apoyo', 9),
('30000002I', 4, 2, 2, 'Fotógrafo Submarino', 8);

-- PROYECTO 5: Censo de Linces 2024 (FINALIZADO)
INSERT INTO participa (dni_voluntario, id_proyecto, id_actividad, id_localizacion, rol, evaluacion) VALUES
-- Localización 5.1.1
('50000002O', 5, 1, 1, 'Bióloga Investigadora', 10),
('30000002I', 5, 1, 1, 'Fotógrafo', 9),
-- Localización 5.1.2
('10000001A', 5, 1, 2, 'Técnico Campo', 9),
('40000001K', 5, 1, 2, 'Asistente', 8),
-- Localización 5.1.3
('20000001D', 5, 1, 3, 'Observadora', 9),
('30000003J', 5, 1, 3, 'Registradora', 8),
-- Localización 5.2.1
('10000003C', 5, 2, 1, 'Analista Jefe', 10),
('20000004G', 5, 2, 1, 'Programador', 9);

-- PROYECTO 6: Comedor Social Centro (EN CURSO)
INSERT INTO participa (dni_voluntario, id_proyecto, id_actividad, id_localizacion, rol, evaluacion) VALUES
-- Localización 6.1.1
('10000001A', 6, 1, 1, 'Jefe de Cocina', NULL),
('20000003F', 6, 1, 1, 'Cocinera', NULL),
('30000002I', 6, 1, 1, 'Ayudante Cocina', NULL),
-- Localización 6.1.2
('10000002B', 6, 1, 2, 'Responsable Comedor', NULL),
('20000004G', 6, 1, 2, 'Atención Mesas', NULL),
('30000003J', 6, 1, 2, 'Limpieza', NULL),
('40000002L', 6, 1, 2, 'Reparto Bandejas', NULL),
-- Localización 6.2.1
('20000001D', 6, 2, 1, 'Supervisora Noche', NULL),
('40000003M', 6, 2, 1, 'Ayudante Noche', NULL),
-- Localización 6.3.1
('50000001N', 6, 3, 1, 'Dietista', NULL);

-- PROYECTO 7: Apoyo Escolar 2025 (EN CURSO - NUEVOS VOLUNTARIOS no usados antes en EN CURSO)
INSERT INTO participa (dni_voluntario, id_proyecto, id_actividad, id_localizacion, rol, evaluacion) VALUES
-- Localización 7.1.1
('40000001K', 7, 1, 1, 'Profesor Matemáticas', NULL),
('50000002O', 7, 1, 1, 'Asistente', NULL),
-- Localización 7.1.2
('10000003C', 7, 1, 2, 'Profesor Secundaria', NULL),
('20000002E', 7, 1, 2, 'Tutor', NULL),
-- Localización 7.1.3
('10000002B', 7, 1, 3, 'Coordinadora Avanzado', NULL),
('30000001H', 7, 1, 3, 'Monitor', NULL),
-- Localización 7.2.1
('20000001D', 7, 2, 1, 'Profesora Lengua', NULL),
('40000002L', 7, 2, 1, 'Asistente', NULL),
-- Localización 7.2.2
('20000003F', 7, 2, 2, 'Profesor Informática', NULL),
('30000002I', 7, 2, 2, 'Técnico', NULL),
-- Localización 7.3.1
('20000004G', 7, 3, 1, 'Monitor Juegos', NULL),
('40000003M', 7, 3, 1, 'Ayudante', NULL),
-- Localización 7.3.2
('10000001A', 7, 3, 2, 'Coordinador Actividades', NULL),
('30000003J', 7, 3, 2, 'Animadora', NULL);

-- PROYECTO 8: Atención Personas Mayores (EN CURSO)
INSERT INTO participa (dni_voluntario, id_proyecto, id_actividad, id_localizacion, rol, evaluacion) VALUES
-- Localización 8.1.1
('50000001N', 8, 1, 1, 'Acompañante', NULL),
('40000001K', 8, 1, 1, 'Asistente', NULL),
-- Localización 8.1.2
('10000003C', 8, 1, 2, 'Acompañante', NULL),
('30000001H', 8, 1, 2, 'Ayudante', NULL),
-- Localización 8.1.3
('10000002B', 8, 1, 3, 'Médico Visita', NULL),
('20000001D', 8, 1, 3, 'Enfermera', NULL),
-- Localización 8.2.1
('20000002E', 8, 2, 1, 'Monitor Talleres', NULL),
('40000002L', 8, 2, 1, 'Asistente', NULL),
-- Localización 8.2.2
('20000003F', 8, 2, 2, 'Coordinadora Residencia', NULL),
('30000002I', 8, 2, 2, 'Animador', NULL);

-- PROYECTO 9: Reforestación Sierra 2025
INSERT INTO participa (dni_voluntario, id_proyecto, id_actividad, id_localizacion, rol, evaluacion) VALUES
-- Localización 9.1.1
('10000003C', 9, 1, 1, 'Capataz Terreno', 9),
('20000002E', 9, 1, 1, 'Operario Maquinaria', 8),
('30000001H', 9, 1, 1, 'Ayudante', 7),
-- Localización 9.1.2
('40000001K', 9, 1, 2, 'Especialista Botánico', 8),
('50000002O', 9, 1, 2, 'Investigadora', 9),
-- Localización 9.2.1
('10000001A', 9, 2, 1, 'Líder Equipo Norte', 9),
('20000003F', 9, 2, 1, 'Plantadora', 8),
('30000002I', 9, 2, 1, 'Transporte Plantones', 7),
('40000002L', 9, 2, 1, 'Registro Plantación', 8),
-- Localización 9.2.2
('10000002B', 9, 2, 2, 'Supervisora Calidad', 9),
('20000004G', 9, 2, 2, 'Operario', 8),
('30000003J', 9, 2, 2, 'Medición Terreno', 7),
-- Localización 9.2.3
('20000001D', 9, 2, 3, 'Especialista Especies', 9),
('40000003M', 9, 2, 3, 'Ayudante', 7),
-- Localización 9.2.4
('50000001N', 9, 2, 4, 'Guía Educativo', 10),
('10000003C', 9, 2, 4, 'Monitor Grupos', 9),
('30000001H', 9, 2, 4, 'Apoyo Didáctico', 8),
('20000002E', 9, 2, 4, 'Logística Material', 8),
-- Localización 9.3.1
('40000001K', 9, 3, 1, 'Responsable Riego', 8),
('50000002O', 9, 3, 1, 'Control Humedad', 9),
-- Localización 9.3.2
('10000001A', 9, 3, 2, 'Estadístico', 8),
-- Localización 9.3.3
('20000003F', 9, 3, 3, 'Protección Plantas', 8),
('30000002I', 9, 3, 3, 'Vigilancia Fauna', 7);

-- PROYECTO 10: Clínica Móvil Rural (EN CURSO)
INSERT INTO participa (dni_voluntario, id_proyecto, id_actividad, id_localizacion, rol, evaluacion) VALUES
-- Localización 10.1.1
('10000002B', 10, 1, 1, 'Médico Rural', NULL),
('20000001D', 10, 1, 1, 'Enfermera', NULL),
-- Localización 10.1.2
('10000001A', 10, 1, 2, 'Conductor Clínica', NULL),
('30000001H', 10, 1, 2, 'Auxiliar', NULL),
-- Localización 10.1.3
('10000003C', 10, 1, 3, 'Médico Visitante', NULL),
('40000001K', 10, 1, 3, 'Traductor', NULL),
-- Localización 10.2.1
('20000003F', 10, 2, 1, 'Coordinadora Vacunación', NULL),
('30000002I', 10, 2, 1, 'Registro', NULL),
-- Localización 10.2.2
('20000004G', 10, 2, 2, 'Enfermero Escolar', NULL),
('40000002L', 10, 2, 2, 'Asistente', NULL);

-- PROYECTOS 11, 12, 13, 15 (FUTUROS): Pueden no tener participantes aún o tener planeados
-- PROYECTO 14: Emergencia Frío 2025 (FUTURO pero cercano - ya tiene voluntarios asignados)
INSERT INTO participa (dni_voluntario, id_proyecto, id_actividad, id_localizacion, rol, evaluacion) VALUES
-- Localización 14.1.1
('10000001A', 14, 1, 1, 'Coordinador Punto', NULL),
('20000002E', 14, 1, 1, 'Distribución Mantas', NULL),
('30000001H', 14, 1, 1, 'Atención Público', NULL),
-- Localización 14.1.2
('10000002B', 14, 1, 2, 'Médico de Guardia', NULL),
('20000001D', 14, 1, 2, 'Enfermera', NULL),
('40000001K', 14, 1, 2, 'Intérprete', NULL),
-- Localización 14.1.3
('10000003C', 14, 1, 3, 'Jefe Equipo', NULL),
('50000001N', 14, 1, 3, 'Traductor Inglés', NULL),
-- Localización 14.2.1
('20000003F', 14, 2, 1, 'Recepción Nocturna', NULL),
('30000002I', 14, 2, 1, 'Asistente Social', NULL),
('40000002L', 14, 2, 1, 'Limpieza', NULL),
('50000002O', 14, 2, 1, 'Psicóloga', NULL),
-- Localización 14.2.2
('20000004G', 14, 2, 2, 'Responsable Turno', NULL),
('30000003J', 14, 2, 2, 'Ayudante', NULL),
-- Localización 14.3.1
('10000001A', 14, 3, 1, 'Conductor Equipo', NULL),
('20000001D', 14, 3, 1, 'Enfermera Ruta', NULL),
('40000003M', 14, 3, 1, 'Auxiliar', NULL),
-- Localización 14.3.2
('10000002B', 14, 3, 2, 'Médico Ruta', NULL),
('30000001H', 14, 3, 2, 'Acompañante', NULL),
-- Localización 14.3.3
('10000003C', 14, 3, 3, 'Líder Equipo', NULL),
('20000002E', 14, 3, 3, 'Logística', NULL),
('50000001N', 14, 3, 3, 'Observador', NULL);

--------------------------------------------------------------------------------
-- 7. COORDINA
--------------------------------------------------------------------------------

-- PROYECTO 1: Vacunación Gripal 2024 (FINALIZADO)
INSERT INTO coordina (dni_voluntario, id_proyecto, id_actividad, id_localizacion, evaluacion) VALUES
('10000003C', 1, 1, 1, 10),
('10000002B', 1, 1, 2, 9),
('10000001A', 1, 2, 1, 10),
('20000001D', 1, 2, 2, 9),
('10000003C', 1, 2, 3, 9),
('10000002B', 1, 3, 1, 10),
('20000004G', 1, 3, 2, 8);

-- PROYECTO 2: Emergencia Inundaciones 2024
INSERT INTO coordina (dni_voluntario, id_proyecto, id_actividad, id_localizacion, evaluacion) VALUES
('10000003C', 2, 1, 2, 10),
('10000002B', 2, 2, 1, 10);

-- PROYECTO 3: Respuesta Ébola 2024
INSERT INTO coordina (dni_voluntario, id_proyecto, id_actividad, id_localizacion, evaluacion) VALUES
('50000001N', 3, 1, 1, 9);

-- PROYECTO 4: Limpieza Costera 2024
INSERT INTO coordina (dni_voluntario, id_proyecto, id_actividad, id_localizacion, evaluacion) VALUES
('20000002E', 4, 1, 1, 9);

-- PROYECTO 5: Censo de Linces 2024
INSERT INTO coordina (dni_voluntario, id_proyecto, id_actividad, id_localizacion, evaluacion) VALUES
('10000001A', 5, 1, 1, 9);

-- PROYECTO 6: Comedor Social Centro (EN CURSO)
INSERT INTO coordina (dni_voluntario, id_proyecto, id_actividad, id_localizacion, evaluacion) VALUES
('20000002E', 6, 1, 1, NULL),
('30000001H', 6, 1, 2, NULL),
('40000001K', 6, 2, 1, NULL),
('50000002O', 6, 3, 1, NULL);

-- PROYECTO 7: Apoyo Escolar 2025 (EN CURSO)
INSERT INTO coordina (dni_voluntario, id_proyecto, id_actividad, id_localizacion, evaluacion) VALUES
('40000001K', 7, 1, 1, NULL),
('10000003C', 7, 1, 2, NULL),
('10000002B', 7, 1, 3, NULL),
('20000001D', 7, 2, 1, NULL),
('20000003F', 7, 2, 2, NULL),
('20000004G', 7, 3, 1, NULL),
('10000001A', 7, 3, 2, NULL);

-- PROYECTO 8: Atención Personas Mayores (EN CURSO)
INSERT INTO coordina (dni_voluntario, id_proyecto, id_actividad, id_localizacion, evaluacion) VALUES
('50000001N', 8, 1, 1, NULL),
('10000003C', 8, 1, 2, NULL),
('10000002B', 8, 1, 3, NULL),
('20000002E', 8, 2, 1, NULL),
('20000003F', 8, 2, 2, NULL);

-- PROYECTO 9: Reforestación Sierra 2025 (FINALIZADO)
INSERT INTO coordina (dni_voluntario, id_proyecto, id_actividad, id_localizacion, evaluacion) VALUES
('10000002B', 9, 1, 1, 10),
('20000001D', 9, 1, 2, 9),
('10000001A', 9, 2, 1, 9),
('10000003C', 9, 2, 1, 10),
('20000004G', 9, 2, 2, 8),
('30000002I', 9, 2, 3, 8),
('40000002L', 9, 2, 4, 9),
('50000001N', 9, 3, 1, 9),
('30000003J', 9, 3, 2, 8),
('40000003M', 9, 3, 3, 7);

-- PROYECTO 10: Clínica Móvil Rural (EN CURSO)
INSERT INTO coordina (dni_voluntario, id_proyecto, id_actividad, id_localizacion, evaluacion) VALUES
('10000002B', 10, 1, 1, NULL),
('10000001A', 10, 1, 2, NULL),
('10000003C', 10, 1, 3, NULL),
('20000003F', 10, 2, 1, NULL),
('20000004G', 10, 2, 2, NULL);

-- PROYECTO 14: Emergencia Frío 2025 (FUTURO)
INSERT INTO coordina (dni_voluntario, id_proyecto, id_actividad, id_localizacion, evaluacion) VALUES
('20000003F', 14, 1, 1, NULL),
('30000001H', 14, 1, 2, NULL),
('40000001K', 14, 1, 3, NULL),
('10000002B', 14, 2, 1, NULL),
('20000001D', 14, 2, 2, NULL),
('10000003C', 14, 3, 1, NULL),
('20000002E', 14, 3, 2, NULL),
('30000002I', 14, 3, 3, NULL);


--------------------------------------------------------------------------------
-- 8. CESIÓN
--------------------------------------------------------------------------------

INSERT INTO cesion (nombre_organizacion, id_proyecto, dni_voluntario, fecha_cesion, duracion) VALUES
('Médicos Sin Fronteras', 1, '10000002B', '2024-01-15', 25),
('Cruz Roja Española', 3, '10000001A', '2024-02-05', 70),
('Greenpeace', 5, '30000001H', '2024-03-10', 10),
('Save The Children', 6, '50000001N', '2025-02-01', 120),
('WWF', 9, '50000002O', '2025-10-05', 56);

--------------------------------------------------------------------------------
-- 9. RECURSOS (15 recursos: 10 donados, 5 alquilados)
--------------------------------------------------------------------------------

INSERT INTO recurso (nombre, descripcion, fecha_entrega, tipo) VALUES 
('Jeringuillas Estériles 5ml', 'Pack 1000 unidades', '2024-01-10', 'D'),
('Mascarillas FFP2', '50 cajas x 20 unidades', '2024-02-01', 'D'),
('Ropa de Abrigo Invierno', '200 prendas segunda mano', '2024-11-15', 'D'),
('Alimentos No Perecederos', '500kg arroz, pasta, legumbres', '2024-03-10', 'D'),
('Juguetes Educativos', '300 unidades campaña navidad', '2024-11-01', 'D'),
('Mantas Térmicas', '150 unidades aluminizadas', '2024-12-01', 'D'),
('Material Escolar Básico', '100 kits cuadernos, lápices', '2025-09-01', 'D'),
('Kits Higiene Personal', '200 kits jabón, cepillo, pasta', '2025-05-01', 'D'),
('Sillas Plegables', '50 unidades para eventos', '2024-06-01', 'D'),
('Termómetros Digitales', '30 unidades clínicas', '2024-01-20', 'D'),
('Generador Electricidad 5000W', 'Gasolina, para emergencias', '2025-01-01', 'A'),
('Carpa Eventos 10x10 metros', 'Impermeable, incluye suelo', '2025-03-15', 'A'),
('Furgoneta Refrigerada', 'Ford Transit 2023', '2025-06-01', 'A'),
('Sistema Megafonía Portátil', 'Altavoces + 2 micrófonos', '2025-03-01', 'A'),
('Vehículo Todo Terreno', 'Toyota Land Cruiser 2022', '2025-12-01', 'A');

INSERT INTO donado (id_recurso, estado, nombre_donante, email_donante) VALUES
(1, 'Nuevo', 'Farmacia Central SL', 'farmacia@central.com'),
(2, 'Nuevo', 'Suministros Médicos SA', 'suministros@medicos.es'),
(3, 'Usado', 'Asociación Vecinal Centro', 'vecinos@centro.org'),
(4, 'Nuevo', 'Supermercados DIA', 'rsc@dia.es'),
(5, 'Nuevo', 'Campaña Empresarial', 'empresas@solidarias.org'),
(6, 'Nuevo', 'Fábrica Textil Norte', 'fabrica@textil.com'),
(7, 'Nuevo', 'Papelería Educativa', 'info@papeleria.edu'),
(8, 'Nuevo', 'Laboratorios Higiene', 'contacto@labhigiene.es'),
(9, 'Usado', 'Hotel Plaza Mayor', 'donaciones@hotelplaza.es'),
(10, 'Nuevo', 'Clínica San Juan', 'administracion@clinicasj.es');

INSERT INTO alquilado (id_recurso, proveedor, costo, fecha_devolucion) VALUES
(11, 'PowerRent Solutions', 200.00, '2025-12-31'),
(12, 'Eventos Profesionales SA', 500.00, '2025-11-30'),
(13, 'RentACar Express', 1200.00, '2025-12-15'),
(14, 'Sonido Profesional SL', 150.00, '2025-06-01'),
(15, 'Alquiler Vehículos 4x4', 1800.00, '2026-03-01');

INSERT INTO recurso_usado (id_proyecto, id_recurso) VALUES
(6, 11),  -- Comedor Social usa Generador
(7, 12),  -- Apoyo Escolar usa Carpa
(8, 13),  -- Atención Mayores usa Furgoneta
(9, 14),  -- Reforestación usa Megafonía
(10, 15), -- Clínica Móvil usa 4x4
(6, 4),   -- Comedor Social usa Alimentos
(6, 8),   -- Comedor Social usa Kits Higiene
(7, 7),   -- Apoyo Escolar usa Material Escolar
(8, 3),   -- Atención Mayores usa Ropa Abrigo
(9, 5),   -- Reforestación usa Juguetes
(10, 1),  -- Clínica Móvil usa Jeringuillas
(10, 2);  -- Clínica Móvil usa Mascarillas