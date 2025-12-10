---------------------------------------------------------
-- Consultas básicas
---------------------------------------------------------

-- 1. GESTIÓN DE ORGANIZACIONES Y PROYECTOS
-- Ver organizaciones registradas
SELECT * FROM organizacion;

-- Ver correos de contacto de las organizaciones
SELECT * FROM email_organizacion;

-- Ver proyectos creados
SELECT * FROM proyecto;

-- Ver el desglose de actividades por proyecto
SELECT * FROM actividad;

-- Ver las localizaciones físicas de cada actividad
SELECT * FROM localizacion;


-- 2. GESTIÓN DE VOLUNTARIADO
-- Ver datos crudos de voluntarios
SELECT * FROM voluntario;

-- Ver voluntarios con la EDAD calculada (Usando la Vista)
SELECT * FROM vista_voluntario_edad;

-- Ver habilidades (skills) de los voluntarios
SELECT * FROM voluntario_skill;


-- 3. ROLES Y ASIGNACIONES
-- Ver voluntarios participando (Rol operativo)
SELECT * FROM participa;

-- Ver voluntarios coordinando (Rol responsable)
SELECT * FROM coordina;

-- Ver acuerdos de cesión de voluntarios entre organizaciones
SELECT * FROM cesion;


-- 4. GESTIÓN DE RECURSOS (INVENTARIO)
-- Ver tabla padre (todos los recursos)
SELECT * FROM recurso;

-- Ver detalle de recursos DONADOS
SELECT * FROM donado;

-- Ver detalle de recursos ALQUILADOS
SELECT * FROM alquilado;

-- Ver qué recursos se están usando en qué proyecto
SELECT * FROM recurso_usado;