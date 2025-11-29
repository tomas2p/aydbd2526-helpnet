# AyDBD 2025/26 - Proyecto HelpNet

**Fecha:** 16 de noviembre de 2025
**Autores:** alu0101474311@ull.edu.es (Tomás Pino Pérez)

# 0. Introducción
El proyecto consiste en diseñar e implementar una base de datos relacional completa junto con un API REST que permita gestionar un escenario original con entidades, relaciones y reglas de negocio. Se requiere elaborar un modelo conceptual ER que incluya entidades débiles, relaciones triples, jerarquías IS_A, relaciones 1:N y M:N, y al menos un caso de inclusión o exclusión; derivar el grafo relacional con claves, dominios y restricciones; implementar los scripts SQL en PostgreSQL con carga de datos de ejemplo, consultas de prueba y triggers/checks/assertions; y desarrollar un API REST en Flask documentando los endpoints con descripción, método HTTP y ejemplos de petición y respuesta.

# 1. Descripción del modelo
**Idea general:** HelpNet gestiona **organizaciones sin ánimo de lucro**, **proyectos sociales**, **voluntarios**, **actividades**, **localizaciones**, **recursos (donados o alquilados)** y **colaboraciones con voluntarios externos**. Permite registrar participaciones, uso de recursos y relaciones entre organizaciones y voluntarios.

**Entidades fuertes:**
- **Organización:** id, nombre, tipo, contacto
- **Proyecto:** id, nombre, descripción, fechas, FK→Organización
- **Voluntario:** id, datos personales, habilidades/rol
- **Actividad:** id, nombre, fecha, FK→Proyecto
- **Localización:** id, dirección, ciudad, tipo
- **Recurso (IS_A):** id, nombre, descripción, tipo

**Subtipos IS_A (mutuamente excluyentes):**
- **RecursoDonado:** donante, fecha entrega
- **RecursoAlquilado:** proveedor, costo, fecha devolución

**Entidades débiles:**
- **ParticipaciónVoluntario (Voluntario–Proyecto):** rol, evaluación
- **ActividadLocalización (Actividad–Localización)**

**Relaciones:**
- **CREA:** Organización→Proyecto (1:N)
- **TIENE:** Proyecto→Actividad (1:N)
- **SE_REALIZA_EN:** Actividad→Localización (M:N)
- **PARTICIPA:** Voluntario→Proyecto (M:N, atributos: rol, evaluación)
- **USA:** Proyecto→Recurso (M:N)
- **COLABORA:** Organización–Proyecto–VoluntarioExterno (triple, con fecha y tipo de ayuda)

**Restricciones clave:**
- Exclusividad en recursos (donado o alquilado)
- Dependencia total en entidades débiles
- Inclusividad en actividades con localizaciones

# 2. Modelo Entidad-Relación
```mermaid
flowchart LR
    %% Entidades Fuertes
    ORG[Organización]
    PRO[Proyecto]
    VOL[Voluntario]
    ACT[Actividad]
    LOC[Localización]
    REC[Recurso]
    A@{ shape: flip-tri, label: "­" }
    RDO[RecursoDonado]
    RAL[RecursoAlquilado]    

    %% Atributos ORG
    ORG --- ORG_PK((🔑 id))
    style ORG_PK fill:#3333,stroke-width:4px
    ORG --- ORG_nombre((nombre))
    ORG --- ORG_tipo((tipo))
    ORG --- ORG_contacto((contacto))

    %% Atributos PRO
    PRO --- PRO_PK((🔑 id))
    style PRO_PK fill:#3333,stroke-width:4px
    PRO --- PRO_nombre((nombre))
    PRO --- PRO_descripcion((descripción))
    PRO --- PRO_fechas((fechas))
    
    %% Atributos VOL
    VOL --- VOL_PK((🔑 id))
    style VOL_PK fill:#3333,stroke-width:4px
    VOL --- VOL_datos_personales((datos_personales))
    VOL --- VOL_rol((rol))
    
    %% Atributos ACT
    ACT --- ACT_PK((🔑 id))
    style ACT_PK fill:#3333,stroke-width:4px
    ACT --- ACT_nombre((nombre))
    ACT --- ACT_fecha((fecha))
    
    %% Atributos LOC
    LOC --- LOC_PK((🔑 id))
    style LOC_PK fill:#3333,stroke-width:4px
    LOC --- LOC_direccion((dirección))
    LOC --- LOC_ciudad((ciudad))
    LOC --- LOC_tipo((tipo))
    
    %% Atributos REC
    REC --- REC_PK((🔑 id))
    style REC_PK fill:#3333,stroke-width:4px
    REC --- REC_nombre((nombre))
    REC --- REC_descripcion((descripción))
    REC --- REC_tipo((tipo))
    
    %% Atributos RDO
    RDO --- RDO_donante((donante))
    RDO --- RDO_fecha_entrega((fecha_entrega))
    
    %% Atributos RAL
    RAL --- RAL_proveedor((proveedor))
    RAL --- RAL_costo((costo))
    RAL --- RAL_fecha_devolcucion((fecha_devolución))
	
	%% Herencia REC - RDO y REC - RAL
    REC --- A --- RDO
    A --- RAL
    
    %% Relaciones
    ORG -- "1" --> R1{CREA} -- "N" --> PRO
    PRO -- "1" --> R2{TIENE} -- "N" --> ACT
    ACT -- "M" --> R3{SE_REALIZA_EN} -- "N" --> LOC
    VOL -- "M" --> R4{PARTICIPA} -- "N" --> PRO
    R4 --- R4_rol((rol))
    R4 --- R4_evalucacion((evaluación))
    PRO -- "M" --> R4{USA} -- "N" --> REC
    
```
