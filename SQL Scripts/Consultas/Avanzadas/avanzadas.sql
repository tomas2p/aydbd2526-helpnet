---------------------------------------------------------
-- Consultas avanzadas
---------------------------------------------------------

-- 1. Listar el coste total de recursos alquilados por Proyecto
SELECT p.nombre AS nombre_proyecto, COUNT(ru.id_recurso) AS cantidad_recursos_alquilados,
       COALESCE(SUM(a.costo), 0) AS coste_total
FROM proyecto p JOIN recurso_usado ru ON p.id_proyecto = ru.id_proyecto
JOIN alquilado a ON ru.id_recurso = a.id_recurso
GROUP BY p.id_proyecto, p.nombre
ORDER BY coste_total DESC;

-- 2. Listar las organizaciones con más de un email de contacto 
SELECT o.nombre, COUNT(eo.email) AS total_emails,
       STRING_AGG(eo.email, ', ') AS lista_emails
FROM organizacion o JOIN email_organizacion eo ON o.nombre = eo.nombre_organizacion
GROUP BY o.nombre, o.tipo
HAVING COUNT(eo.email) > 1;

-- 3. Listar las localizaciones en las que han actuado organizaciones médicas
SELECT o.nombre AS organizacion, p.nombre AS proyecto, a.nombre AS actividad, 
       l.descripcion AS lugar, l.latitud, l.longitud
FROM organizacion o JOIN proyecto p ON o.nombre = p.nombre_organizacion
JOIN actividad a ON p.id_proyecto = a.id_proyecto
JOIN localizacion l ON (a.id_proyecto = l.id_proyecto AND a.id_actividad = l.id_actividad)
WHERE o.tipo = 'Médica';

-- 4. Detectar que proyectos deben devolver un recurso alquilado antes de su finalización
SELECT p.nombre AS proyecto_afectado, r.nombre AS recurso_en_riesgo,
       a.fecha_devolucion, p.fecha_fin AS fin_del_proyecto,
       (p.fecha_fin - a.fecha_devolucion) AS dias_sin_cobertura
FROM recurso_usado ru JOIN proyecto p ON ru.id_proyecto = p.id_proyecto
JOIN alquilado a ON ru.id_recurso = a.id_recurso JOIN recurso r ON a.id_recurso = r.id_recurso
WHERE a.fecha_devolucion < p.fecha_fin
ORDER BY dias_sin_cobertura DESC;

-- 5. Listar la nota media de participantes y coordinadores en proyectos
SELECT p.nombre AS proyecto, ROUND(AVG(par.evaluacion), 2) AS media_participantes,
       ROUND(AVG(cor.evaluacion), 2) AS media_coordinadores
FROM proyecto p LEFT JOIN participa par ON p.id_proyecto = par.id_proyecto
LEFT JOIN coordina cor ON p.id_proyecto = cor.id_proyecto
WHERE cor.evaluacion IS NOT NULL AND par.evaluacion IS NOT NULL
GROUP BY p.id_proyecto, p.nombre;

-- 6. Listar los voluntarios, que coordinaron o van a coordinar, jóvenes
SELECT v.nombre AS voluntario, v.edad, p.nombre AS proyecto_que_coordina,
       c.evaluacion AS nota_liderazgo
FROM vista_voluntario_edad v
JOIN coordina c ON v.dni = c.dni_voluntario
JOIN proyecto p ON c.id_proyecto = p.id_proyecto
WHERE v.edad < 30
ORDER BY v.edad ASC;

-- 7. Listar los voluntarios que han sido cedidos, de que organización vienen y a cuál van. 
SELECT v.nombre AS voluntario_cedido, c.nombre_organizacion AS organizacion_origen,
       p.nombre_organizacion AS organizacion_destino, p.nombre AS proyecto_receptor,
       c.fecha_cesion, c.duracion AS dias_prestamo
FROM cesion c JOIN voluntario v ON c.dni_voluntario = v.dni
JOIN proyecto p ON c.id_proyecto = p.id_proyecto;

-- 8. Listar los recursos que estan libres
SELECT r.id_recurso, r.nombre, r.tipo
FROM recurso r LEFT JOIN recurso_usado ru ON r.id_recurso = ru.id_recurso
WHERE ru.id_proyecto IS NULL;

-- 9. Listar los voluntarios con más de una skill
SELECT v.nombre, v.email, COUNT(DISTINCT vs.nombre_skill) AS cantidad_skills,
       STRING_AGG(DISTINCT vs.nombre_skill, ', ') AS lista_skills
FROM voluntario v JOIN voluntario_skill vs ON v.dni = vs.dni_voluntario
LEFT JOIN participa p ON v.dni = p.dni_voluntario LEFT JOIN coordina c ON v.dni = c.dni_voluntario
GROUP BY v.dni, v.nombre, v.email
HAVING COUNT(DISTINCT vs.nombre_skill) > 1
ORDER BY cantidad_skills DESC;

-- Listar todos los proyectos, con el número de actividades, voluntarios involucrados y el coste en recursos
SELECT p.nombre AS proyecto, p.fecha_inicio, p.fecha_fin,
       (SELECT COUNT(*) FROM actividad a WHERE a.id_proyecto = p.id_proyecto) AS total_actividades,
       (SELECT COUNT(DISTINCT dni) FROM (
           SELECT dni_voluntario AS dni FROM participa WHERE id_proyecto = p.id_proyecto
           UNION 
           SELECT dni_voluntario AS dni FROM coordina WHERE id_proyecto = p.id_proyecto
        ) AS unicos) AS total_voluntarios,
    (SELECT COALESCE(SUM(al.costo), 0) 
     FROM recurso_usado ru 
     JOIN alquilado al ON ru.id_recurso = al.id_recurso 
     WHERE ru.id_proyecto = p.id_proyecto) AS coste_recursos
FROM proyecto p
ORDER BY p.fecha_inicio;