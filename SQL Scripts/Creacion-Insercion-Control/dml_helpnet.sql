-- Active: 1760516486489@@127.0.0.1@5432@helpnet
\c helpnet;

DO $$
DECLARE
    -- Cantidades mínimas garantizadas
    add_org INT := 15;
    add_vol INT := 15;
    add_res INT := 15;
    add_proj_per_org INT := 2;
    add_act_per_proj INT := 2;
    add_loc_per_act INT := 1;
    add_res_used_per_proj INT := 2;

    -- Contadores existentes
    last_org INT;
    last_vol INT;
    last_res INT;
    last_proj INT;
    last_act INT;
    last_loc INT;

    -- Variables de IDs
    o INT; p INT; a INT; l INT; v INT; r INT;

    org_name TEXT;
    proj_id TEXT;
    act_id TEXT;
    loc_id TEXT;
BEGIN
    -------------------------------------------------------------------------
    -- 1. DETECTAR ÚLTIMOS NÚMEROS EXISTENTES
    -------------------------------------------------------------------------

    SELECT COALESCE(MAX(regexp_replace(nombre, '\D','','g')::INT),0)
    INTO last_org FROM organizacion;

    SELECT COALESCE(MAX(regexp_replace(dni, '\D','','g')::INT),0)
    INTO last_vol FROM voluntario;

    SELECT COALESCE(MAX(regexp_replace(id_recurso, '\D','','g')::INT),0)
    INTO last_res FROM recurso;

    SELECT COALESCE(MAX(regexp_replace(id_proyecto, '\D','','g')::INT),0)
    INTO last_proj FROM proyecto;

    SELECT COALESCE(MAX(regexp_replace(id_actividad, '\D','','g')::INT),0)
    INTO last_act FROM actividad;

    SELECT COALESCE(MAX(regexp_replace(id_localizacion, '\D','','g')::INT),0)
    INTO last_loc FROM localizacion;

    -------------------------------------------------------------------------
    -- 2. ORGANIZACIONES NUEVAS
    -------------------------------------------------------------------------
    FOR o IN 1..add_org LOOP
        org_name := 'Org' || (last_org + o);

        INSERT INTO organizacion VALUES (org_name, 'tipo_'||(last_org+o));
        INSERT INTO email_organizacion VALUES(org_name, org_name||'@mail.com');
    END LOOP;

    -------------------------------------------------------------------------
    -- 3. PROYECTOS / ACTIVIDADES / LOCALIZACIONES
    -------------------------------------------------------------------------
    FOR o IN 1..add_org LOOP
        org_name := 'Org' || (last_org + o);

        FOR p IN 1..add_proj_per_org LOOP
            proj_id := 'P' || (last_proj + o) || '_' || p;

            INSERT INTO proyecto VALUES(
                proj_id, org_name,
                'Proyecto '||proj_id,
                'Descripcion de '||proj_id,
                CURRENT_DATE - (10+random()*100)::INT,
                CURRENT_DATE + (10+random()*100)::INT
            );

            FOR a IN 1..add_act_per_proj LOOP
                act_id := 'A' || (last_act + o) || '_' || p || '_' || a;

                INSERT INTO actividad VALUES(
                    act_id, proj_id,
                    'Actividad '||act_id,
                    'Descripcion',
                    CURRENT_DATE - (5+random()*50)::INT,
                    CURRENT_DATE + (5+random()*50)::INT
                );

                FOR l IN 1..add_loc_per_act LOOP
                    loc_id := 'L' || (last_loc + o) || '_' || p || '_' || a || '_' || l;

                    INSERT INTO localizacion VALUES(
                        loc_id, act_id, proj_id,
                        -90 + random()*180, -180 + random()*360,
                        'Descripcion localizacion '||loc_id,
                        'Observaciones '||loc_id
                    );
                END LOOP;

            END LOOP;

        END LOOP;
    END LOOP;

    -------------------------------------------------------------------------
    -- 4. VOLUNTARIOS NUEVOS + SKILLS
    -------------------------------------------------------------------------
    FOR v IN 1..add_vol LOOP
        INSERT INTO voluntario VALUES(
            'V'||(last_vol+v),
            'Voluntario '||(last_vol+v),
            DATE '1960-01-01' + (random()*20000)::INT,
            CURRENT_DATE - (random()*2000)::INT,
            'v'||(last_vol+v)||'@mail.com'
        );

        INSERT INTO voluntario_skill VALUES(
            'V'||(last_vol+v),
            'Skill1',
            'Descripcion Skill'
        );
    END LOOP;

    -------------------------------------------------------------------------
    -- 5. CESIONES (aleatorias)
    -------------------------------------------------------------------------
    FOR o IN 1..add_org LOOP
        FOR p IN 1..add_proj_per_org LOOP

            INSERT INTO cesion VALUES(
                'Org'||(last_org + o),
                'P'||(last_proj+o)||'_'||p,
                'V'||(last_vol + ((o+p) % add_vol) + 1),
                CURRENT_DATE - (20+random()*100)::INT,
                'duracion'
            );

        END LOOP;
    END LOOP;

    -------------------------------------------------------------------------
    -- 6. RECURSOS NUEVOS
    -------------------------------------------------------------------------
    FOR r IN 1..add_res LOOP
        INSERT INTO recurso VALUES(
            'R'||(last_res+r),
            'Recurso '||(last_res+r),
            CURRENT_DATE - (10+random()*200)::INT,
            'Descripcion recurso',
            CASE WHEN random() < 0.5 THEN 'donado' ELSE 'alquilado' END
        );

        IF random() < 0.5 THEN
            INSERT INTO recurso_donado VALUES(
                'R'||(last_res+r),
                'bueno',
                'Donante '||(last_res+r),
                'don'||(last_res+r)||'@mail.com'
            );
        ELSE
            INSERT INTO recurso_alquilado VALUES(
                'R'||(last_res+r),
                'Proveedor '||(last_res+r),
                (10+random()*200)::INT,
                CURRENT_DATE + (10+random()*200)::INT
            );
        END IF;
    END LOOP;

    -------------------------------------------------------------------------
    -- 7. RECURSOS USADOS
    -------------------------------------------------------------------------
    FOR o IN 1..add_org LOOP
        FOR p IN 1..add_proj_per_org LOOP
            FOR r IN 1..add_res_used_per_proj LOOP
                INSERT INTO recurso_usado VALUES(
                    'R'||(last_res + ((o+r) % add_res) + 1),
                    'P'||(last_proj+o)||'_'||p
                );
            END LOOP;
        END LOOP;
    END LOOP;

    -------------------------------------------------------------------------
    -- 8. PARTICIPA / COORDINA
    -------------------------------------------------------------------------
    FOR o IN 1..add_org LOOP
        FOR p IN 1..add_proj_per_org LOOP
            FOR a IN 1..add_act_per_proj LOOP
                FOR l IN 1..add_loc_per_act LOOP

                    loc_id := 'L'||(last_loc+o)||'_'||p||'_'||a||'_'||l;
                    act_id := 'A'||(last_act+o)||'_'||p||'_'||a;
                    proj_id := 'P'||(last_proj+o)||'_'||p;

                    INSERT INTO participa VALUES(
                        loc_id, act_id, proj_id,
                        'V'||(last_vol + ((o+a+l) % add_vol) + 1),
                        'trabajo', (1+random()*10)::INT
                    );

                    INSERT INTO coordina VALUES(
                        loc_id, act_id, proj_id,
                        'V'||(last_vol + ((o+a+l+3) % add_vol) + 1),
                        (1+random()*10)::INT
                    );

                END LOOP;
            END LOOP;
        END LOOP;
    END LOOP;

END$$;