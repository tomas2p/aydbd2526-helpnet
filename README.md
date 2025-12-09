# AyDBD 2025/26 -Proyecto HelpNet
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

# 1. Descripción y requisitos

## Descripción general:

**HelpNet** es una plataforma tecnológica diseñada para facilitar la orquestación integral de iniciativas humanitarias, conectando organizaciones sin ánimo de lucro, voluntarios y recursos materiales bajo un entorno unificado. El sistema busca optimizar la asignación de recursos y garantizar la trazabilidad de las acciones solidarias.

## Especificación de requisitos:

El sistema deberá registrar, consultar y gestionar la información basándose en las siguientes reglas de negocio y restricciones técnicas:

### 1. Gestión de organizaciones y proyectos

Las organizaciones son las entidades promotoras del sistema.
* Cada organización tiene **múltiples correos electrónicos de contacto**.
* Es responsable de crear **proyectos**, definidos por un periodo de tiempo y que deben tener una descripción.
* Cada proyecto emplea diversos recursos para su ejecución.

### 2. Estructura jerárquica de actividades

La planificación operativa de los proyectos sigue una estructura estrictamente jerárquica para garantizar la trazabilidad:

* Todo **proyecto** se desglosa en múltiples **actividades**.
* A su vez, cada actividad se despliega físicamente en una o varias **localizaciones** específicas. Se debe modelar esta dependencia de forma que una **localización** no pueda ser identificada ni existir en el sistema sin conocer la **actividad** y el **proyecto** al que pertenece.

### 3. Gestión del voluntariado

Los voluntarios se registran con sus datos personales básicos (nombre, correo electrónico, fecha de nacimiento...). El sistema debe almacenar el conjunto de **habilidades** que posee cada voluntario (ej. "Primeros Auxilios", "Conducción"), permitiendo incluir detalles para cada habilidad.

### 4. Roles y restricciones operativas

La participación de los voluntarios ocurre de dos formas:

* Los **voluntarios** son asignados a **localizaciones** concretas para hacer una **actividad**; con un rol específico y recibiendo una valoración al final.
* Los **voluntarios** son asignados a **localizaciones** concretas para actuar como responsable de la zona, recibiendo una valoración al final. 

De tal manera que en una misma localización específica, un voluntario **nunca puede desempeñar ambos roles simultáneamente**, asegurando así la segregación de funciones entre ejecución y supervisión. 

### 5. Gestión de recursos

El sistema gestiona un inventario de recursos clasificados según su procedencia mediante una **jerarquía total y exclusiva**:

* **Recursos Donados:** Requieren registrar los datos del donante (nombre, email) y el estado del bien.
* **Recursos Alquilados:** Requieren registrar el proveedor, costo y fecha de devolución.

Un recurso debe pertenecer obligatoriamente a una de estas dos categorías y no puede pertenecer a ambas simultáneamente.

### 6. Colaboración inter-organizacional

El sistema debe soportar acuerdos complejos de colaboración. Se requiere registrar cuando una **organización** cede formalmente a un **voluntario**, o un grupo de ellos, específico para colaborar en un **proyecto** gestionado por otra entidad, registrando la fecha y duración de dicho acuerdo de cesión.

# 2. Descripción del modelo E/R

## Descripción de las entidades definidas:

* **Organización:** Representa a las entidades promotoras registradas en el sistema. Su clave primaria es el **Nombre**. Su atributo **Tipo** indica la naturaleza de la organización (e.g., Fundación, Asociación) y posee un atributo multivaluado **Email** para gestionar múltiples puntos de contacto.

* **Proyecto:** Representa las iniciativas humanitarias creadas por las organizaciones. Su clave primaria es su **ID_Proyecto**. Sus atributos incluyen: **Nombre**, **Descripción**, **Fecha_Inicio** y **Fecha_Fin**. Es la entidad fuerte de la cual dependen jerárquicamente las actividades.

* **Actividad:** Representa las tareas lógicas en las que se desglosa un proyecto. Es una **entidad débil en identificación** respecto a **Proyecto**. Su clave primaria está compuesta por **ID_Actividad** e **ID_Proyecto**. Sus atributos son: **Nombre**, **Descripción**, **Fecha_Inicio** y **Fecha_Fin**.

* **Localización:** Representa el punto físico o despliegue operativo donde ocurre una actividad. Es una **entidad débil en identificación** respecto a **Actividad** (y transitivamente a Proyecto). Su clave primaria se compone de **ID_Localizacion**, **ID_Actividad** y **ID_Proyecto**. Sus atributos son: **Descripción**, **Observaciones**, **Latitud** y **Longitud**.

* **Voluntario:** Representa a las personas naturales que colaboran en el sistema. Su clave primaria es el **DNI**. Sus atributos son: **Nombre**, **Fecha_Nacimiento**, **Fecha_Alta**, **Email** (multivaluado) y **Skills** (multivaluado compuesto, que incluye **Nombre** y **Descripción**). Posee un atributo derivado **Edad**, calculado a partir de la fecha de nacimiento.

* **Recurso:** Entidad superclase que representa cualquier material o fondo monetario utilizado en los proyectos. Su clave primaria es su **ID_Recurso**. Sus atributos comunes son: **Nombre**, **Descripción**, **Fecha_Entrega** y **Tipo** (discriminador de la jerarquía).

* **Donado:** Subclase que representa los recursos obtenidos gratuitamente. Hereda de **Recurso**. Sus atributos específicos son: **Nombre_Donante**, **Email_Donante** y **Estado**.

* **Alquilado:** Subclase que representa los recursos obtenidos mediante pago temporal. Hereda de **Recurso**. Sus atributos específicos son: **Proveedor**, **Costo** y **Fecha_Devolución**.

## Descripción de las relaciones definidas:

* **Crea:** Relaciona a la **Organización** con el **Proyecto**.
    * **Cardinalidad:** Una **Organización** puede crear uno o más **Proyectos (1:N)**, y un **Proyecto** es creado por exactamente una **Organización (1:1)**.

* **Tiene:** Relación de dependencia entre **Proyecto** y **Actividad**. Indica que un proyecto esta compuesto por actividades, y que estas se identifican en base al proyecto del que son parte.
    * **Cardinalidad:** Un **Proyecto** tiene una o más **Actividades (1:N)** y una **Actividad** pertenece a un solo **Proyecto (1:1)**.

* **Se realiza:** Relación de dependencia entre **Actividad** y **Localización**. Indica la o las localizaciones en las que se realiza una actividad; también que las localizaciones se identifican por su actividad.
    * **Cardinalidad:** Una **Actividad** se desarrolla en una o más **Localizaciones (1:N)** y una **Localización** pertenece a una sola **Actividad (1:1)**.

* **Emplea:** Relaciona **Proyecto** con **Recurso**, indicando el uso de materiales.
    * **Cardinalidad:** Un **Proyecto** emplea uno o más **Recursos (1:N)** y un **Recurso** a lo largo del tiempo es empleado en varios **Proyectos (1:N)** durante su ciclo de vida registrado.

* **Participa:** Relaciona al **Voluntario** con el **Localización**.
    * **Atributos:** Posee **Rol** (cargo general en el proyecto) y **Evaluación** (nota final de desempeño).
    * **Cardinalidad:** Un **Voluntario** participa en uno o varias **Actividades desarrolladas en alguna localización (1:N)** y a us vez estas tienen inscritos a varios **Voluntarios (1:N)**.

* **Coordina:** Relaciona al **Voluntario** con la **Localización**, indicando que actúa como responsable o jefe de zona.
    * **Atributos:** **Valoración** (desempeño específico como líder).
    * **Cardinalidad:** Un **Voluntario** coordina una o varias **Actividades desarrolladas en alguna localización (1:N)** y a us vez estas tienen como coordinadores a varios **Voluntarios (1:N)**.
    * **Restricción:** Un **Voluntario** coordina o participa en alguna actividad, pero no ambas.

* **Ceder (Relación Ternaria):** Relación simultánea entre **Organización**, **Proyecto** y **Voluntario**. Representa un acuerdo especial donde una organización externa "presta" un voluntario a un proyecto ajeno.
    * **Cardinalidad:** Muchas **Organizaciones** pueden ceder muchos **Voluntarios** a muchos otros **Proyectos (N:M:P)**.

## Descripción y ejemplos ilustrativos del dominio de cada uno de los atributos:

* **Organización:**
    * **Nombre:** Identificador único. VARCHAR(100), ejemplo: "Cruz Roja Española".
    * **Tipo:** Categoria legal. VARCHAR(50), ejemplo: "Asociación".
    * **Email (multivaluado):** Direcciones de contacto. VARCHAR(100), ejemplo: "contacto@cruzroja.es".

* **Proyecto:**
    * **ID:** Código numérico único. INTEGER, ejemplo: 202501.
    * **Nombre:** Título del proyecto. VARCHAR(100), ejemplo: "Campaña Vacunación 2025".
    * **Descripción:** Detalle del proyecto. TEXT, ejemplo: "Inmunización masiva contra la gripe en zonas rurales". Puede ser nula.
    * **Fecha_Inicio:** DATE, ejemplo: 2025-01-01.
    * **Fecha_Fin** DATE, ejemplo: 2025-11-30.

* **Actividad:**
    * **ID:** Código numérico único. INTEGER, ejemplo: 1.
    * **Nombre:** Título de la actividad. VARCHAR(100), ejemplo: "Logística de distribución".
    * **Descripción:** Detalle de la tarea. TEXT, ejemplo: "Transporte de neveras médicas a los puntos de vacunación". Puede ser nula.
    * **Fecha_Inicio:** DATE, ejemplo: 2025-01-05.
    * **Fecha_Fin** DATE, ejemplo: 2025-01-06.

* **Localización:**
    * **ID:** Identificador secuencial del lugar (dependiente de la actividad). INTEGER, ejemplo: 1.
    * **Descripción:** Nombre o referencia del sitio físico. VARCHAR(200), ejemplo: "Carpa Médica Plaza Central".
    * **Observaciones:** Notas sobre acceso o seguridad. TEXT, ejemplo: "Acceso habilitado para ambulancias por calle trasera". Puede ser nula.
    * **Latitud:** Coordenada geográfica decimal. DECIMAL(10,8), ejemplo: 28.4636.
    * **Longitud:** Coordenada geográfica decimal. DECIMAL(11,8), ejemplo: -16.2518.

* **Voluntario:**
    * **DNI:** Documento Nacional de Identidad. VARCHAR(9), ejemplo: "12345678Z".
    * **Nombre:** Nombre completo del voluntario. VARCHAR(100), ejemplo: "Laura Mateo Ruiz".
    * **Skills (multivaluado):** Habilidades o certificaciones. VARCHAR(100), ejemplo: "Enfermería Pediátrica".
    * **Fecha Alta:** Fecha de registro en el sistema. DATE, ejemplo: 2023-05-20.
    * **Fecha Nacimiento:** Fecha de nacimiento. DATE, ejemplo: 1998-03-15.
    * **Edad:** Atributo derivado/calculado a partir de la fecha de nacimiento. INTEGER, ejemplo: 26.
    * **Email:** Correo de contacto personal. VARCHAR(100), ejemplo: "laura.m@email.com".

* **Recurso (Superclase):**
    * **ID:** Identificador único del recurso. INTEGER, ejemplo: 500.
    * **Nombre:** Nombre del material. VARCHAR(100), ejemplo: "Nevera Portátil".
    * **Descripción:** Características técnicas. TEXT, ejemplo: "Capacidad 50L, control de temperatura digital". Puede ser nula.
    * **Fecha Entrega:** Fecha en la que el recurso entra en inventario. DATE, ejemplo: 2024-01-10.
    * **Tipo:** Discriminador de la jerarquía. CHAR(1), ejemplo: 'D' (Donado) o 'A' (Alquilado).

* **Donado (Subclase):**
    * **Nombre Donante:** Persona o entidad que cede el bien. VARCHAR(100), ejemplo: "Farmacias Unidas". Puede ser nulo.
    * **Email Donante:** Contacto del donante. VARCHAR(100), ejemplo: "rsc@farmaciasunidas.com". Puede ser nulo.
    * **Estado:** Condición del recurso. VARCHAR(50), ejemplo: "Nuevo".

* **Alquilado (Subclase):**
    * **Proveedor:** Empresa propietaria. VARCHAR(100), ejemplo: "Eventos S.L.".
    * **Costo:** Coste en euros del alquiler. DECIMAL(10,2), ejemplo: 150.00.
    * **Fecha Devolución:** Fecha límite para devolver el bien. DATE, ejemplo: 2025-03-01.

* **Atributos de las Relaciones:**
  * **Rol:** Función general en el proyecto. VARCHAR(50), ejemplo: "Enfermero".
  * **Evaluación (en Participa):** Nota de desempeño (0-10). INTEGER, ejemplo: 9. Puede ser nulo.
  * **Evaluación (en Coordina):** Nota específica como líder de zona (0-10). INTEGER, ejemplo: 10. Puede ser nulo.
  * **Fecha_Cesión:** Fecha del acuerdo de cesión. DATE, ejemplo: 2025-01-15.
  * **Duración:** Tiempo del préstamo inter-organizacional en días. INTEGER, ejemplo: 30.

## Restricciones semánticas:

* La **Fecha_Inicio** de un proyecto o actividad no puede ser posterior a su **Fecha_Fin**.
* El intervalo de tiempo de una **Actividad** debe estar comprendido estrictamente dentro del intervalo de tiempo del **Proyecto** al que pertenece.
* Un **Voluntario** no puede figurar simultáneamente en las relaciones **Coordina** y **Participa** para una misma **Localización**.
* Los **Voluntarios** deben ser mayores de edad al momento de darse de alta.
* El atributo **Evaluación** debe ser números enteros comprendidos en un rango definido (e.g., 0 ≤ Nota ≤ 10).
* El **Costo** de un recurso alquilado debe ser siempre mayor o igual a cero.
* Si el atributo discriminador **Tipo** de un recurso indica 'Donado', debe existir obligatoriamente una correspondencia en la entidad **Donado** y no en **Alquilado** (y viceversa).
* La **Edad** del voluntario debe ser consistente con la diferencia entre la fecha actual y su **Fecha_Nacimiento**.
* La **Fecha_Cesión** en la relación ternaria debe estar comprendida dentro del periodo de vigencia del **Proyecto** receptor.
* Las coordenadas de una **Localización** (Latitud y Longitud) deben estar dentro de los rangos geográficos válidos (−90 ≤ Latitud ≤ 90 y −180 ≤ Longitud ≤ 180).

# 3. Modelo E/R
![](Modelos/Modelo_E_R/HelpNet_E_R.png)

# 4. Modelo Relacional
![](Modelos/Modelo_Relacional/HelpNet_Relacional.png)

# 5. SQL Scripts
A continuación se presenta una descripción de los archivos SQL incluidos en el proyecto, indicando el propósito de cada uno y cómo contribuyen a la gestión y manipulación de la base de datos:
- `ddl_helpnet.sql`: Contiene sentencias DDL (Data Definition Language), como CREATE, ALTER y DROP. Se usa para definir y modificar la estructura de las tablas, vistas, índices y otros objetos de la base de datos.
- `dml_helpnet.sql`: Incluye sentencias DML (Data Manipulation Language), como INSERT, UPDATE y DELETE. Sirve para manipular los datos dentro de las tablas ya existentes.
- `delete_data.sql`: Normalmente contiene instrucciones para eliminar datos específicos de las tablas, generalmente usando sentencias DELETE. No modifica la estructura, solo borra registros.