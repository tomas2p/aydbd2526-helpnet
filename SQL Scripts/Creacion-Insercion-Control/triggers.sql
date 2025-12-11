---------------------------------------------------------
-- DISPARADORES
---------------------------------------------------------

---------------------------------------------------------
-- 1. Se debe verificar que una actividad este comprendida dentro de su proyecto.
---------------------------------------------------------
create or replace function verificar_fechas_actividad()
returns trigger as $$
declare
    v_inicio_proy date;
    v_fin_proy date;
begin
    select fecha_inicio, fecha_fin into v_inicio_proy, v_fin_proy
    from proyecto
    where id_proyecto = new.id_proyecto;

    if new.fecha_inicio < v_inicio_proy then
        raise exception 'Error de Integridad: La actividad no puede iniciar antes que el proyecto (Inicio Proyecto: %)', v_inicio_proy;
    end if;
    if new.fecha_fin > v_fin_proy then
        raise exception 'Error de Integridad: La actividad no puede finalizar después que el proyecto (Fin Proyecto: %)', v_fin_proy;
    end if;
    return new;
end;
$$ language plpgsql;

create trigger trg_verificar_fechas_actividad
before insert or update on actividad
for each row
execute function verificar_fechas_actividad();


---------------------------------------------------------
-- 2. Se debe verificar que, al ceder un voluntario, la fecha de cesión este comprendida en el nuevo proyecto.
---------------------------------------------------------
create or replace function verificar_fecha_cesion()
returns trigger as $$
declare
    v_inicio_proy date;
    v_fin_proy date;
begin
    select fecha_inicio, fecha_fin into v_inicio_proy, v_fin_proy
    from proyecto
    where id_proyecto = new.id_proyecto;
    if new.fecha_cesion < v_inicio_proy or new.fecha_cesion > v_fin_proy then
        raise exception 'Error de Integridad: La fecha de cesión (%) debe estar dentro del periodo del proyecto (% a %)', 
                        new.fecha_cesion, v_inicio_proy, v_fin_proy;
    end if;
    return new;
end;
$$ language plpgsql;

create trigger trg_verificar_fecha_cesion
before insert or update on cesion
for each row
execute function verificar_fecha_cesion();


---------------------------------------------------------
-- 3. Un voluntario participa o coordina una actividad, pero no ambas.
---------------------------------------------------------
create or replace function verificar_exclusion_roles()
returns trigger as $$
begin
    if (TG_TABLE_NAME = 'participa') then
        if exists (
            select 1 from coordina 
            where dni_voluntario = new.dni_voluntario
            and id_localizacion = new.id_localizacion
            and id_actividad = new.id_actividad
            and id_proyecto = new.id_proyecto
        ) then
            raise exception 'Error de Exclusión: El voluntario % ya figura como Coordinador en esta localización. No puede participar simultáneamente.', new.dni_voluntario;
        end if;
    elsif (TG_TABLE_NAME = 'coordina') then
        if exists (
            select 1 from participa 
            where dni_voluntario = new.dni_voluntario
            and id_localizacion = new.id_localizacion
            and id_actividad = new.id_actividad
            and id_proyecto = new.id_proyecto
        ) then
            raise exception 'Error de Exclusión: El voluntario % ya figura como Participante en esta localización. No puede coordinar simultáneamente.', new.dni_voluntario;
        end if;
    end if;

    return new;
end;
$$ language plpgsql;

-- Trigger para la tabla PARTICIPA
create trigger trg_exclusion_participa
before insert or update on participa
for each row
execute function verificar_exclusion_roles();

-- Trigger para la tabla COORDINA
create trigger trg_exclusion_coordina
before insert or update on coordina
for each row
execute function verificar_exclusion_roles();


---------------------------------------------------------
-- 4. Un recurso es donado o alquilado, pero no puede ser ambas.
---------------------------------------------------------
create or replace function verificar_tipo_recurso()
returns trigger as $$
declare
    v_tipo char(1);
begin
    select tipo into v_tipo
    from recurso
    where id_recurso = new.id_recurso;
    if (TG_TABLE_NAME = 'donado') then
        if v_tipo <> 'D' then
            raise exception 'Error de Jerarquía: El recurso % está definido como tipo ''%'' en la tabla padre, no puede insertarse en DONADO.', new.id_recurso, v_tipo;
        end if;
    elsif (TG_TABLE_NAME = 'alquilado') then
        if v_tipo <> 'A' then
            raise exception 'Error de Jerarquía: El recurso % está definido como tipo ''%'' en la tabla padre, no puede insertarse en ALQUILADO.', new.id_recurso, v_tipo;
        end if;
    end if;
    return new;
end;
$$ language plpgsql;

-- Trigger para la tabla DONADO
create trigger trg_verificar_tipo_donado
before insert or update on donado
for each row
execute function verificar_tipo_recurso();

-- Trigger para la tabla ALQUILADO
create trigger trg_verificar_tipo_alquilado
before insert or update on alquilado
for each row
execute function verificar_tipo_recurso();


---------------------------------------------------------
-- 5. Limpieza de datos en recurso_usado cuando se finaliza anticipadamente un proyecto
---------------------------------------------------------
CREATE OR REPLACE FUNCTION limpiar_recursos_proyecto()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.fecha_fin < OLD.fecha_fin AND NEW.fecha_fin <= CURRENT_DATE THEN
        DELETE FROM recurso_usado
        WHERE id_proyecto = NEW.id_proyecto;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_limpiar_recursos
AFTER UPDATE OF fecha_fin ON proyecto
FOR EACH ROW
EXECUTE FUNCTION limpiar_recursos_proyecto();


---------------------------------------------------------
-- 6. No se puede añadir una localización a una actividad finalizada
---------------------------------------------------------
CREATE OR REPLACE FUNCTION verificar_actividad_activa()
RETURNS TRIGGER AS $$
DECLARE
    v_fecha_fin_actividad DATE;
BEGIN
    SELECT fecha_fin INTO v_fecha_fin_actividad
    FROM actividad
    WHERE id_actividad = NEW.id_actividad 
      AND id_proyecto = NEW.id_proyecto;
    IF v_fecha_fin_actividad < CURRENT_DATE THEN
        RAISE EXCEPTION 'Error de Negocio: No se puede añadir una localización a la actividad % porque ya ha finalizado (Fecha fin: %)', 
                        NEW.id_actividad, v_fecha_fin_actividad;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_verificar_actividad_activa
BEFORE INSERT OR UPDATE ON localizacion
FOR EACH ROW
EXECUTE FUNCTION verificar_actividad_activa();


---------------------------------------------------------
-- 7. Un voluntario no puede hacer actividades que se solapen
---------------------------------------------------------
CREATE OR REPLACE FUNCTION verificar_agenda_voluntario()
RETURNS TRIGGER AS $$
DECLARE
    v_inicio_nueva DATE;
    v_fin_nueva DATE;
    v_conflicto RECORD;
BEGIN
    SELECT fecha_inicio, fecha_fin INTO v_inicio_nueva, v_fin_nueva
    FROM actividad
    WHERE id_proyecto = NEW.id_proyecto 
      AND id_actividad = NEW.id_actividad;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Actividad no encontrada: Proyecto=%, Actividad=%', 
                        NEW.id_proyecto, NEW.id_actividad;
    END IF;
    SELECT a.nombre, a.fecha_inicio, a.fecha_fin, 'PARTICIPA' as tabla
    INTO v_conflicto
    FROM participa p
    JOIN actividad a ON p.id_proyecto = a.id_proyecto AND p.id_actividad = a.id_actividad
    WHERE p.dni_voluntario = NEW.dni_voluntario
      AND NOT (p.id_proyecto = NEW.id_proyecto 
               AND p.id_actividad = NEW.id_actividad 
               AND p.id_localizacion = NEW.id_localizacion)
      AND a.fecha_inicio <= v_fin_nueva
      AND a.fecha_fin >= v_inicio_nueva
    UNION ALL
    SELECT a.nombre, a.fecha_inicio, a.fecha_fin, 'COORDINA' as tabla
    FROM coordina c
    JOIN actividad a ON c.id_proyecto = a.id_proyecto AND c.id_actividad = a.id_actividad
    WHERE c.dni_voluntario = NEW.dni_voluntario
      AND NOT (c.id_proyecto = NEW.id_proyecto 
               AND c.id_actividad = NEW.id_actividad 
               AND c.id_localizacion = NEW.id_localizacion)
      AND a.fecha_inicio <= v_fin_nueva
      AND a.fecha_fin >= v_inicio_nueva
    LIMIT 1;
    IF FOUND THEN
        RAISE EXCEPTION 
            'Conflicto de agenda: El voluntario % ya % en "%" (% a %). No disponible del % al %.',
            NEW.dni_voluntario,
            v_conflicto.tabla,
            v_conflicto.nombre,
            v_conflicto.fecha_inicio,
            v_conflicto.fecha_fin,
            v_inicio_nueva,
            v_fin_nueva;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para PARTICIPA
CREATE TRIGGER trg_verificar_agenda_participa
BEFORE INSERT OR UPDATE ON participa
FOR EACH ROW
EXECUTE FUNCTION verificar_agenda_voluntario();

-- Trigger para COORDINA
CREATE TRIGGER trg_verificar_agenda_coordina
BEFORE INSERT OR UPDATE ON coordina
FOR EACH ROW
EXECUTE FUNCTION verificar_agenda_voluntario();