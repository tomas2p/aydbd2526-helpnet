# AyDBD 2025/26 - Proyecto HelpNet
![Fecha](https://img.shields.io/badge/Fecha-16/11/2025-white?style=for-the-badge&logo=datefns&logoColor=white)
[![ModeloER](https://img.shields.io/badge/Modelo-Entidad/Relación-white?style=for-the-badge&logo=cachet&logoColor=white)](Modelos/Modelo_E_R/HelpNet_E_R.png)
[![ModeloR](https://img.shields.io/badge/Modelo-Relacional-white?style=for-the-badge&logo=cachet&logoColor=white)](Modelos/Modelo_Relacional/HelpNet_Relacional.png)
[![BD](https://img.shields.io/badge/BD-helpnet-white?style=for-the-badge&logo=postgresql&logoColor=white)](SQL%20Scripts/ddl_helpnet.sql)
[![API](https://img.shields.io/badge/Api-FastApi-white?style=for-the-badge&logo=fastapi&logoColor=white)](por_hacer)

## Autores
[![Integrante1](https://img.shields.io/badge/Tomás_Pino_Pérez-alu0101474311-white?style=for-the-badge&logo=maildotru&logoColor=white)](https://github.com/tomas2p)
[![Integrante1](https://img.shields.io/badge/Juan_Esteban_Tamayo_Marmolejo-alu0101592916-white?style=for-the-badge&logo=maildotru&logoColor=white)](https://github.com/Juanes-TM)

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
![](Modelos/Modelo_E_R/HelpNet_E_R.png)

# 3. Modelo Relacional
![](Modelos/Modelo_Relacional/HelpNet_Relacional.png)

# 4. SQL Scripts
A continuación se presenta una descripción de los archivos SQL incluidos en el proyecto, indicando el propósito de cada uno y cómo contribuyen a la gestión y manipulación de la base de datos:
- `ddl_helpnet.sql`: Contiene sentencias DDL (Data Definition Language), como CREATE, ALTER y DROP. Se usa para definir y modificar la estructura de las tablas, vistas, índices y otros objetos de la base de datos.
- `dml_helpnet.sql`: Incluye sentencias DML (Data Manipulation Language), como INSERT, UPDATE y DELETE. Sirve para manipular los datos dentro de las tablas ya existentes.
- `delete_data.sql`: Normalmente contiene instrucciones para eliminar datos específicos de las tablas, generalmente usando sentencias DELETE. No modifica la estructura, solo borra registros.
