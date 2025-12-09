---------------------------------------------------------
-- DISPARADORES
---------------------------------------------------------

-- Se debe verificar que una actividad este comprendida dentro de su proyecto.
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



-- Se debe verificar que, al ceder un voluntario, la fecha de cesión este comprendida en el nuevo proyecto.
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



-- Un voluntario participa o coordina una actividad, pero no ambas.
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



-- Un recurso es donado o alquilado, pero no puede ser ambas.
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



-- Limpieza de datos en recurso_usado
CREATE OR REPLACE FUNCTION limpiar_recursos_proyecto()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.fecha_fin <= CURRENT_DATE THEN
        DELETE FROM recurso_usado
        WHERE id_proyecto = NEW.id_proyecto
          AND id_recurso IN (
              SELECT id_recurso FROM recurso
              WHERE tipo = 'D'
          );
        DELETE FROM recurso_usado
        WHERE id_proyecto = NEW.id_proyecto
          AND id_recurso IN (
              SELECT id_recurso FROM alquilado
              WHERE fecha_devolucion <= CURRENT_DATE
          );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_limpiar_recursos
AFTER UPDATE OF fecha_fin ON proyecto
FOR EACH ROW
EXECUTE FUNCTION limpiar_recursos_proyecto();