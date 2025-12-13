# Documentación de Endpoints de la API HelpNet

Esta tabla documenta todos los endpoints disponibles en la API HelpNet con ejemplos de petición y respuesta.

## Notas Importantes

- **IDs Alfanuméricos**: Los IDs de `proyecto`, `actividad` y `localizacion` son VARCHAR (texto), no numéricos. Ejemplos: `'P1_1'`, `'A1_1_1'`, `'L1_1_1_1'`
- **Paginación**: Todos los endpoints de listado soportan parámetros `?skip=0&limit=20`
- **Cascada DELETE**: Los endpoints DELETE retornan información detallada sobre registros eliminados en cascada
- **Recursos Polimórficos**: Los recursos se discriminan por el campo `tipo`: `'D'` = Donado, `'A'` = Alquilado

---

## 📋 Tabla de Endpoints

### 🏢 ORGANIZACIONES

| Endpoint + Descripción | Método | Ejemplo de Petición | Ejemplo de Respuesta |
|------------------------|--------|---------------------|----------------------|
| **POST /api/organizaciones**<br>Crea una nueva organización con sus emails | POST | `{`<br>`  "nombre": "Cruz Roja",`<br>`  "tipo": "ONG",`<br>`  "emails": ["info@cruzroja.org", "contacto@cruzroja.org"]`<br>`}` | `Status: 201 Created`<br>`{`<br>`  "nombre": "Cruz Roja",`<br>`  "tipo": "ONG",`<br>`  "emails": ["info@cruzroja.org", "contacto@cruzroja.org"]`<br>`}` |
| **GET /api/organizaciones**<br>Lista todas las organizaciones con paginación | GET | `GET /api/organizaciones?skip=0&limit=20` | `Status: 200 OK`<br>`{`<br>`  "items": [`<br>`    {`<br>`      "nombre": "Org1",`<br>`      "tipo": "tipo_1",`<br>`      "emails": ["Org1@mail.com"]`<br>`    }`<br>`  ],`<br>`  "total": 15,`<br>`  "skip": 0,`<br>`  "limit": 20`<br>`}` |
| **GET /api/organizaciones/{nombre}**<br>Obtiene una organización específica | GET | `GET /api/organizaciones/Cruz%20Roja` | `Status: 200 OK`<br>`{`<br>`  "nombre": "Cruz Roja",`<br>`  "tipo": "ONG",`<br>`  "emails": ["info@cruzroja.org"]`<br>`}` |
| **PUT /api/organizaciones/{nombre}**<br>Actualiza una organización | PUT | `{`<br>`  "tipo": "Fundación"`<br>`}` | `Status: 200 OK`<br>`{`<br>`  "nombre": "Cruz Roja",`<br>`  "tipo": "Fundación",`<br>`  "emails": ["info@cruzroja.org"]`<br>`}` |
| **DELETE /api/organizaciones/{nombre}**<br>Elimina organización y registros relacionados en cascada | DELETE | `DELETE /api/organizaciones/Org1` | `Status: 200 OK`<br>`{`<br>`  "message": "Organización eliminada exitosamente",`<br>`  "deleted_id": "Org1",`<br>`  "cascade_info": {`<br>`    "emails": 1,`<br>`    "proyectos": 2,`<br>`    "actividades": 4,`<br>`    "localizaciones": 4,`<br>`    "participaciones": 0,`<br>`    "coordinaciones": 0,`<br>`    "cesiones": 0`<br>`  }`<br>`}` |
| **GET /api/organizaciones/{nombre}/emails**<br>Lista emails de una organización | GET | `GET /api/organizaciones/Org1/emails` | `Status: 200 OK`<br>`["Org1@mail.com"]` |
| **POST /api/organizaciones/{nombre}/emails**<br>Agrega email a organización | POST | `{`<br>`  "email": "nuevo@org1.com"`<br>`}` | `Status: 201 Created`<br>`{`<br>`  "nombre_organizacion": "Org1",`<br>`  "email": "nuevo@org1.com"`<br>`}` |
| **DELETE /api/organizaciones/{nombre}/emails/{email}**<br>Elimina email de organización | DELETE | `DELETE /api/organizaciones/Org1/emails/Org1@mail.com` | `Status: 204 No Content` |

---

### 📊 PROYECTOS

| Endpoint + Descripción | Método | Ejemplo de Petición | Ejemplo de Respuesta |
|------------------------|--------|---------------------|----------------------|
| **POST /api/proyectos**<br>Crea un nuevo proyecto | POST | `{`<br>`  "id_proyecto": "PROY2025_1",`<br>`  "nombre_organizacion": "Org1",`<br>`  "nombre": "Ayuda Humanitaria Valencia",`<br>`  "descripcion": "Proyecto de reconstrucción",`<br>`  "fecha_inicio": "2025-01-01",`<br>`  "fecha_fin": "2025-12-31"`<br>`}` | `Status: 201 Created`<br>`{`<br>`  "id_proyecto": "PROY2025_1",`<br>`  "nombre_organizacion": "Org1",`<br>`  "nombre": "Ayuda Humanitaria Valencia",`<br>`  "descripcion": "Proyecto de reconstrucción",`<br>`  "fecha_inicio": "2025-01-01",`<br>`  "fecha_fin": "2025-12-31"`<br>`}` |
| **GET /api/proyectos**<br>Lista todos los proyectos | GET | `GET /api/proyectos?skip=0&limit=20` | `Status: 200 OK`<br>`{`<br>`  "items": [`<br>`    {`<br>`      "id_proyecto": "P1_1",`<br>`      "nombre_organizacion": "Org1",`<br>`      "nombre": "Proyecto P1_1",`<br>`      "descripcion": "Descripcion de P1_1",`<br>`      "fecha_inicio": "2025-05-15",`<br>`      "fecha_fin": "2026-03-20"`<br>`    }`<br>`  ],`<br>`  "total": 30,`<br>`  "skip": 0,`<br>`  "limit": 20`<br>`}` |
| **GET /api/proyectos/{id_proyecto}**<br>Obtiene un proyecto específico | GET | `GET /api/proyectos/P1_1` | `Status: 200 OK`<br>`{`<br>`  "id_proyecto": "P1_1",`<br>`  "nombre_organizacion": "Org1",`<br>`  "nombre": "Proyecto P1_1",`<br>`  "descripcion": "Descripcion de P1_1",`<br>`  "fecha_inicio": "2025-05-15",`<br>`  "fecha_fin": "2026-03-20"`<br>`}` |
| **PUT /api/proyectos/{id_proyecto}**<br>Actualiza un proyecto | PUT | `{`<br>`  "nombre": "Proyecto Actualizado",`<br>`  "descripcion": "Nueva descripción"`<br>`}` | `Status: 200 OK`<br>`{`<br>`  "id_proyecto": "P1_1",`<br>`  "nombre": "Proyecto Actualizado",`<br>`  "descripcion": "Nueva descripción",`<br>`  ...`<br>`}` |
| **DELETE /api/proyectos/{id_proyecto}**<br>Elimina proyecto y registros relacionados | DELETE | `DELETE /api/proyectos/P1_1` | `Status: 200 OK`<br>`{`<br>`  "message": "Proyecto eliminado exitosamente",`<br>`  "deleted_id": "P1_1",`<br>`  "cascade_info": {`<br>`    "actividades": 2,`<br>`    "localizaciones": 2,`<br>`    "participaciones": 0,`<br>`    "coordinaciones": 0,`<br>`    "recursos_usados": 0,`<br>`    "cesiones": 0`<br>`  }`<br>`}` |

---

### 🎯 ACTIVIDADES

| Endpoint + Descripción | Método | Ejemplo de Petición | Ejemplo de Respuesta |
|------------------------|--------|---------------------|----------------------|
| **POST /api/proyectos/{id_proyecto}/actividades**<br>Crea actividad en un proyecto | POST | `{`<br>`  "id_actividad": "ACT_001",`<br>`  "nombre": "Distribución de alimentos",`<br>`  "descripcion": "Entrega de alimentos básicos",`<br>`  "fecha_inicio": "2025-02-01",`<br>`  "fecha_fin": "2025-02-15"`<br>`}` | `Status: 201 Created`<br>`{`<br>`  "id_actividad": "ACT_001",`<br>`  "id_proyecto": "P1_1",`<br>`  "nombre": "Distribución de alimentos",`<br>`  "descripcion": "Entrega de alimentos básicos",`<br>`  "fecha_inicio": "2025-02-01",`<br>`  "fecha_fin": "2025-02-15"`<br>`}` |
| **GET /api/proyectos/{id_proyecto}/actividades**<br>Lista actividades de un proyecto | GET | `GET /api/proyectos/P1_1/actividades?skip=0&limit=10` | `Status: 200 OK`<br>`{`<br>`  "items": [`<br>`    {`<br>`      "id_actividad": "A1_1_1",`<br>`      "id_proyecto": "P1_1",`<br>`      "nombre": "Actividad A1_1_1",`<br>`      "fecha_inicio": "2025-04-01",`<br>`      "fecha_fin": "2025-07-15"`<br>`    }`<br>`  ],`<br>`  "total": 2,`<br>`  "skip": 0,`<br>`  "limit": 10`<br>`}` |
| **GET /api/proyectos/{id_proyecto}/actividades/{id_actividad}**<br>Obtiene actividad específica | GET | `GET /api/proyectos/P1_1/actividades/A1_1_1` | `Status: 200 OK`<br>`{`<br>`  "id_actividad": "A1_1_1",`<br>`  "id_proyecto": "P1_1",`<br>`  "nombre": "Actividad A1_1_1",`<br>`  ...`<br>`}` |
| **DELETE /api/proyectos/{id_proyecto}/actividades/{id_actividad}**<br>Elimina actividad y localizaciones relacionadas | DELETE | `DELETE /api/proyectos/P1_1/actividades/A1_1_1` | `Status: 200 OK`<br>`{`<br>`  "message": "Actividad eliminada exitosamente",`<br>`  "deleted_id": "A1_1_1 (proyecto: P1_1)",`<br>`  "cascade_info": {`<br>`    "localizaciones": 1,`<br>`    "participaciones": 0,`<br>`    "coordinaciones": 0`<br>`  }`<br>`}` |

---

### 📍 LOCALIZACIONES

| Endpoint + Descripción | Método | Ejemplo de Petición | Ejemplo de Respuesta |
|------------------------|--------|---------------------|----------------------|
| **POST /api/proyectos/{id_p}/actividades/{id_a}/localizaciones**<br>Crea localización geográfica | POST | `{`<br>`  "id_localizacion": "LOC_001",`<br>`  "latitud": 39.4699,`<br>`  "longitud": -0.3763,`<br>`  "descripcion": "Valencia Centro",`<br>`  "observaciones": "Plaza del Ayuntamiento"`<br>`}` | `Status: 201 Created`<br>`{`<br>`  "id_localizacion": "LOC_001",`<br>`  "id_actividad": "A1_1_1",`<br>`  "id_proyecto": "P1_1",`<br>`  "latitud": "39.46990000",`<br>`  "longitud": "-0.37630000",`<br>`  "descripcion": "Valencia Centro",`<br>`  "observaciones": "Plaza del Ayuntamiento"`<br>`}` |
| **GET /api/proyectos/{id_p}/actividades/{id_a}/localizaciones**<br>Lista localizaciones de actividad | GET | `GET /api/proyectos/P1_1/actividades/A1_1_1/localizaciones` | `Status: 200 OK`<br>`{`<br>`  "items": [`<br>`    {`<br>`      "id_localizacion": "L1_1_1_1",`<br>`      "id_actividad": "A1_1_1",`<br>`      "id_proyecto": "P1_1",`<br>`      "latitud": "12.34567890",`<br>`      "longitud": "98.76543210",`<br>`      "descripcion": "Descripcion localizacion L1_1_1_1"`<br>`    }`<br>`  ],`<br>`  "total": 1,`<br>`  "skip": 0,`<br>`  "limit": 20`<br>`}` |
| **DELETE /api/proyectos/{id_p}/actividades/{id_a}/localizaciones/{id_l}**<br>Elimina localización | DELETE | `DELETE /api/proyectos/P1_1/actividades/A1_1_1/localizaciones/L1_1_1_1` | `Status: 200 OK`<br>`{`<br>`  "message": "Localización eliminada exitosamente",`<br>`  "deleted_id": "L1_1_1_1 (actividad: A1_1_1, proyecto: P1_1)",`<br>`  "cascade_info": {`<br>`    "participaciones": 0,`<br>`    "coordinaciones": 0`<br>`  }`<br>`}` |

---

### 👥 VOLUNTARIOS

| Endpoint + Descripción | Método | Ejemplo de Petición | Ejemplo de Respuesta |
|------------------------|--------|---------------------|----------------------|
| **POST /api/voluntarios**<br>Crea voluntario (valida edad >= 18 años) | POST | `{`<br>`  "dni": "12345678A",`<br>`  "nombre": "María García",`<br>`  "fecha_nacimiento": "1995-05-20",`<br>`  "fecha_alta": "2024-01-10",`<br>`  "email": "maria@email.com"`<br>`}` | `Status: 201 Created`<br>`{`<br>`  "dni": "12345678A",`<br>`  "nombre": "María García",`<br>`  "fecha_nacimiento": "1995-05-20",`<br>`  "fecha_alta": "2024-01-10",`<br>`  "email": "maria@email.com"`<br>`}` |
| **POST /api/voluntarios** *(menor de 18)*<br>Intenta crear voluntario menor de edad (ERROR) | POST | `{`<br>`  "dni": "99999999Z",`<br>`  "nombre": "Juan Menor",`<br>`  "fecha_nacimiento": "2010-01-01",`<br>`  "fecha_alta": "2024-01-01",`<br>`  "email": "juan@email.com"`<br>`}` | `Status: 422 Unprocessable Entity`<br>`{`<br>`  "detail": "El voluntario debe tener al menos 18 años. Edad calculada: 14.0 años"`<br>`}` |
| **GET /api/voluntarios**<br>Lista todos los voluntarios | GET | `GET /api/voluntarios?skip=0&limit=20` | `Status: 200 OK`<br>`{`<br>`  "items": [`<br>`    {`<br>`      "dni": "V1",`<br>`      "nombre": "Voluntario 1",`<br>`      "fecha_nacimiento": "1980-06-15",`<br>`      "fecha_alta": "2023-01-10",`<br>`      "email": "v1@mail.com"`<br>`    }`<br>`  ],`<br>`  "total": 15,`<br>`  "skip": 0,`<br>`  "limit": 20`<br>`}` |
| **GET /api/voluntarios/{dni}/edad**<br>Obtiene voluntario con edad calculada | GET | `GET /api/voluntarios/V1/edad` | `Status: 200 OK`<br>`{`<br>`  "dni": "V1",`<br>`  "nombre": "Voluntario 1",`<br>`  "fecha_nacimiento": "1980-06-15",`<br>`  "fecha_alta": "2023-01-10",`<br>`  "email": "v1@mail.com",`<br>`  "edad": 45`<br>`}` |
| **DELETE /api/voluntarios/{dni}**<br>Elimina voluntario y sus relaciones | DELETE | `DELETE /api/voluntarios/V1` | `Status: 200 OK`<br>`{`<br>`  "message": "Voluntario eliminado exitosamente",`<br>`  "deleted_id": "V1",`<br>`  "cascade_info": {`<br>`    "skills": 1,`<br>`    "participaciones": 0,`<br>`    "coordinaciones": 0,`<br>`    "cesiones": 0`<br>`  }`<br>`}` |
| **GET /api/voluntarios/{dni}/skills**<br>Lista habilidades del voluntario | GET | `GET /api/voluntarios/V1/skills` | `Status: 200 OK`<br>`[`<br>`  {`<br>`    "dni_voluntario": "V1",`<br>`    "nombre_skill": "skill_1",`<br>`    "descripcion": null`<br>`  }`<br>`]` |
| **POST /api/voluntarios/{dni}/skills**<br>Agrega habilidad a voluntario | POST | `{`<br>`  "nombre_skill": "Primeros Auxilios",`<br>`  "descripcion": "Certificado Cruz Roja"`<br>`}` | `Status: 201 Created`<br>`{`<br>`  "dni_voluntario": "V1",`<br>`  "nombre_skill": "Primeros Auxilios",`<br>`  "descripcion": "Certificado Cruz Roja"`<br>`}` |

---

### 📦 RECURSOS (Polimórficos: Donado/Alquilado)

| Endpoint + Descripción | Método | Ejemplo de Petición | Ejemplo de Respuesta |
|------------------------|--------|---------------------|----------------------|
| **POST /api/recursos** *(Donado)*<br>Crea recurso donado (tipo='D') | POST | `{`<br>`  "tipo": "D",`<br>`  "nombre": "Tienda de campaña",`<br>`  "descripcion": "Tienda 4 personas",`<br>`  "fecha_entrega": "2025-01-15",`<br>`  "estado": "nuevo",`<br>`  "nombre_donante": "Juan Pérez",`<br>`  "email_donante": "juan@email.com"`<br>`}` | `Status: 201 Created`<br>`{`<br>`  "id_recurso": 1,`<br>`  "tipo": "D",`<br>`  "nombre": "Tienda de campaña",`<br>`  "descripcion": "Tienda 4 personas",`<br>`  "fecha_entrega": "2025-01-15",`<br>`  "estado": "nuevo",`<br>`  "nombre_donante": "Juan Pérez",`<br>`  "email_donante": "juan@email.com"`<br>`}` |
| **POST /api/recursos** *(Alquilado)*<br>Crea recurso alquilado (tipo='A') | POST | `{`<br>`  "tipo": "A",`<br>`  "nombre": "Generador 5000W",`<br>`  "descripcion": "Generador eléctrico",`<br>`  "fecha_entrega": "2025-02-01",`<br>`  "proveedor": "Alquileres SA",`<br>`  "costo": 250.50,`<br>`  "fecha_devolucion": "2025-03-01"`<br>`}` | `Status: 201 Created`<br>`{`<br>`  "id_recurso": 2,`<br>`  "tipo": "A",`<br>`  "nombre": "Generador 5000W",`<br>`  "descripcion": "Generador eléctrico",`<br>`  "fecha_entrega": "2025-02-01",`<br>`  "proveedor": "Alquileres SA",`<br>`  "costo": "250.50",`<br>`  "fecha_devolucion": "2025-03-01"`<br>`}` |
| **GET /api/recursos**<br>Lista todos los recursos (mixto donados y alquilados) | GET | `GET /api/recursos?skip=0&limit=20` | `Status: 200 OK`<br>`{`<br>`  "items": [`<br>`    {`<br>`      "id_recurso": 1,`<br>`      "tipo": "D",`<br>`      "nombre": "Recurso 1",`<br>`      "estado": "bueno",`<br>`      ...`<br>`    },`<br>`    {`<br>`      "id_recurso": 2,`<br>`      "tipo": "A",`<br>`      "nombre": "Recurso 2",`<br>`      "proveedor": "Proveedor 2",`<br>`      ...`<br>`    }`<br>`  ],`<br>`  "total": 15,`<br>`  "skip": 0,`<br>`  "limit": 20`<br>`}` |
| **GET /api/recursos?tipo=D**<br>Lista solo recursos donados | GET | `GET /api/recursos?tipo=D&skip=0&limit=20` | `Status: 200 OK`<br>`{`<br>`  "items": [`<br>`    {`<br>`      "id_recurso": 1,`<br>`      "tipo": "D",`<br>`      "nombre": "Recurso Donado",`<br>`      "estado": "nuevo",`<br>`      "nombre_donante": "Donante",`<br>`      ...`<br>`    }`<br>`  ],`<br>`  "total": 8,`<br>`  "skip": 0,`<br>`  "limit": 20`<br>`}` |
| **GET /api/recursos?tipo=A**<br>Lista solo recursos alquilados | GET | `GET /api/recursos?tipo=A&skip=0&limit=20` | `Status: 200 OK`<br>`{`<br>`  "items": [`<br>`    {`<br>`      "id_recurso": 2,`<br>`      "tipo": "A",`<br>`      "nombre": "Recurso Alquilado",`<br>`      "proveedor": "Proveedor SA",`<br>`      "costo": "100.00",`<br>`      ...`<br>`    }`<br>`  ],`<br>`  "total": 7,`<br>`  "skip": 0,`<br>`  "limit": 20`<br>`}` |
| **GET /api/recursos/{id}**<br>Obtiene recurso específico (serializado según tipo) | GET | `GET /api/recursos/1` | `Status: 200 OK`<br>`{`<br>`  "id_recurso": 1,`<br>`  "tipo": "D",`<br>`  "nombre": "Tienda de campaña",`<br>`  "estado": "nuevo",`<br>`  "nombre_donante": "Juan Pérez"`<br>`}` |
| **GET /api/recursos/donados**<br>Endpoint específico para listar solo donados | GET | `GET /api/recursos/donados?skip=0&limit=10` | `Status: 200 OK`<br>`{ "items": [...], "total": 8, ... }` |
| **GET /api/recursos/alquilados**<br>Endpoint específico para listar solo alquilados | GET | `GET /api/recursos/alquilados?skip=0&limit=10` | `Status: 200 OK`<br>`{ "items": [...], "total": 7, ... }` |
| **DELETE /api/recursos/{id}**<br>Elimina recurso (cualquier tipo) | DELETE | `DELETE /api/recursos/1` | `Status: 200 OK`<br>`{`<br>`  "message": "Recurso eliminado exitosamente",`<br>`  "deleted_id": 1,`<br>`  "cascade_info": {`<br>`    "recursos_usados": 2`<br>`  }`<br>`}` |

---

### 🔗 RELACIONES

#### Participaciones (Voluntario con Rol Operativo)

| Endpoint + Descripción | Método | Ejemplo de Petición | Ejemplo de Respuesta |
|------------------------|--------|---------------------|----------------------|
| **POST /api/participaciones**<br>Asigna voluntario a localización con rol | POST | `{`<br>`  "id_localizacion": "L1_1_1_1",`<br>`  "id_actividad": "A1_1_1",`<br>`  "id_proyecto": "P1_1",`<br>`  "dni_voluntario": "V1",`<br>`  "rol": "Operador Logística",`<br>`  "evaluacion": 8`<br>`}` | `Status: 201 Created`<br>`{`<br>`  "id_localizacion": "L1_1_1_1",`<br>`  "id_actividad": "A1_1_1",`<br>`  "id_proyecto": "P1_1",`<br>`  "dni_voluntario": "V1",`<br>`  "rol": "Operador Logística",`<br>`  "evaluacion": 8`<br>`}` |
| **GET /api/participaciones**<br>Lista todas las participaciones | GET | `GET /api/participaciones?skip=0&limit=20` | `Status: 200 OK`<br>`{`<br>`  "items": [...],`<br>`  "total": 10,`<br>`  "skip": 0,`<br>`  "limit": 20`<br>`}` |
| **GET /api/participaciones?dni_voluntario=V1**<br>Lista participaciones de un voluntario | GET | `GET /api/participaciones?dni_voluntario=V1` | `Status: 200 OK`<br>`{`<br>`  "items": [`<br>`    {`<br>`      "dni_voluntario": "V1",`<br>`      "rol": "Operador",`<br>`      "evaluacion": 8,`<br>`      ...`<br>`    }`<br>`  ],`<br>`  "total": 3,`<br>`  ...`<br>`}` |
| **DELETE /api/participaciones/{id_loc}/{id_act}/{id_proy}/{dni}**<br>Elimina participación | DELETE | `DELETE /api/participaciones/L1_1_1_1/A1_1_1/P1_1/V1` | `Status: 204 No Content` |

#### Coordinaciones (Voluntario Responsable)

| Endpoint + Descripción | Método | Ejemplo de Petición | Ejemplo de Respuesta |
|------------------------|--------|---------------------|----------------------|
| **POST /api/coordinaciones**<br>Asigna voluntario como coordinador | POST | `{`<br>`  "id_localizacion": "L1_1_1_1",`<br>`  "id_actividad": "A1_1_1",`<br>`  "id_proyecto": "P1_1",`<br>`  "dni_voluntario": "V2",`<br>`  "evaluacion": 9`<br>`}` | `Status: 201 Created`<br>`{`<br>`  "id_localizacion": "L1_1_1_1",`<br>`  "id_actividad": "A1_1_1",`<br>`  "id_proyecto": "P1_1",`<br>`  "dni_voluntario": "V2",`<br>`  "evaluacion": 9`<br>`}` |
| **GET /api/coordinaciones**<br>Lista todas las coordinaciones | GET | `GET /api/coordinaciones?skip=0&limit=20` | `Status: 200 OK`<br>`{ "items": [...], "total": 5, ... }` |

#### Cesiones (Relación Ternaria: Org-Proyecto-Voluntario)

| Endpoint + Descripción | Método | Ejemplo de Petición | Ejemplo de Respuesta |
|------------------------|--------|---------------------|----------------------|
| **POST /api/cesiones**<br>Crea cesión de voluntario entre organización y proyecto | POST | `{`<br>`  "nombre_organizacion": "Org1",`<br>`  "id_proyecto": "P1_1",`<br>`  "dni_voluntario": "V1",`<br>`  "fecha_cesion": "2025-02-01",`<br>`  "duracion": 30`<br>`}` | `Status: 201 Created`<br>`{`<br>`  "nombre_organizacion": "Org1",`<br>`  "id_proyecto": "P1_1",`<br>`  "dni_voluntario": "V1",`<br>`  "fecha_cesion": "2025-02-01",`<br>`  "duracion": 30`<br>`}` |
| **GET /api/cesiones**<br>Lista cesiones con filtros opcionales | GET | `GET /api/cesiones?nombre_organizacion=Org1&skip=0&limit=20` | `Status: 200 OK`<br>`{ "items": [...], "total": 3, ... }` |
| **DELETE /api/cesiones/{org}/{proyecto}/{dni}**<br>Elimina cesión | DELETE | `DELETE /api/cesiones/Org1/P1_1/V1` | `Status: 204 No Content` |

#### Recursos Usados en Proyectos

| Endpoint + Descripción | Método | Ejemplo de Petición | Ejemplo de Respuesta |
|------------------------|--------|---------------------|----------------------|
| **POST /api/proyectos/{id_proyecto}/recursos**<br>Asigna recurso a proyecto | POST | `?id_recurso=5` | `Status: 201 Created`<br>`{`<br>`  "id_proyecto": "P1_1",`<br>`  "id_recurso": 5`<br>`}` |
| **GET /api/proyectos/{id_proyecto}/recursos**<br>Lista recursos usados en proyecto | GET | `GET /api/proyectos/P1_1/recursos` | `Status: 200 OK`<br>`[`<br>`  {`<br>`    "id_proyecto": "P1_1",`<br>`    "id_recurso": 5`<br>`  }`<br>`]` |
| **DELETE /api/proyectos/{id_proyecto}/recursos/{id_recurso}**<br>Desasigna recurso de proyecto | DELETE | `DELETE /api/proyectos/P1_1/recursos/5` | `Status: 204 No Content` |

---

## 📊 Códigos de Estado HTTP

| Código | Significado | Cuándo se usa |
|--------|-------------|---------------|
| 200 | OK | Operación exitosa (GET, PUT, DELETE con info) |
| 201 | Created | Recurso creado exitosamente (POST) |
| 204 | No Content | Eliminación exitosa sin contenido de respuesta |
| 400 | Bad Request | Datos inválidos, recurso ya existe, tipo inválido |
| 404 | Not Found | Recurso no encontrado |
| 422 | Unprocessable Entity | Validación falló (edad < 18, fechas inválidas, etc.) |
| 500 | Internal Server Error | Error del servidor |

---

## 💡 Ejemplos de Uso Completos

### Caso 1: Crear Organización con Proyecto y Voluntarios

```bash
# 1. Crear organización
curl -X POST http://localhost:8000/api/organizaciones \\
  -H "Content-Type: application/json" \\
  -d '{
    "nombre": "Ayuda Comunitaria",
    "tipo": "Asociación",
    "emails": ["info@ayuda.org"]
  }'

# 2. Crear proyecto
curl -X POST http://localhost:8000/api/proyectos \\
  -H "Content-Type: application/json" \\
  -d '{
    "id_proyecto": "AYUDA_2025",
    "nombre_organizacion": "Ayuda Comunitaria",
    "nombre": "Reconstrucción Valencia",
    "descripcion": "Ayuda post-DANA",
    "fecha_inicio": "2025-01-01",
    "fecha_fin": "2025-12-31"
  }'

# 3. Crear voluntario
curl -X POST http://localhost:8000/api/voluntarios \\
  -H "Content-Type: application/json" \\
  -d '{
    "dni": "11111111A",
    "nombre": "Ana Martínez",
    "fecha_nacimiento": "1990-03-15",
    "fecha_alta": "2025-01-10",
    "email": "ana@email.com"
  }'
```

### Caso 2: Recursos Polimórficos

```bash
# Crear recurso donado
curl -X POST http://localhost:8000/api/recursos \\
  -H "Content-Type: application/json" \\
  -d '{
    "tipo": "D",
    "nombre": "Bomba de agua",
    "fecha_entrega": "2025-01-20",
    "estado": "nuevo",
    "nombre_donante": "Ferretería López"
  }'

# Crear recurso alquilado
curl -X POST http://localhost:8000/api/recursos \\
  -H "Content-Type: application/json" \\
  -d '{
    "tipo": "A",
    "nombre": "Excavadora",
    "fecha_entrega": "2025-02-01",
    "proveedor": "Maquinaria Pérez",
    "costo": 800.00,
    "fecha_devolucion": "2025-03-01"
  }'

# Listar todos (mixto)
curl http://localhost:8000/api/recursos

# Filtrar solo donados
curl http://localhost:8000/api/recursos?tipo=D

# Filtrar solo alquilados
curl http://localhost:8000/api/recursos?tipo=A
```

---

## 🔍 Notas Finales

- **Documentación Interactiva**: Visitar http://localhost:8000/docs para probar endpoints en vivo
- **Validación Automática**: Todos los endpoints validan datos con Pydantic
- **Transacciones**: Todas las operaciones usan transacciones de base de datos
- **Eager Loading**: Consultas optimizadas con `joinedload()` para evitar N+1
- **Código Abierto**: Ver código fuente en `app/routers/` para más detalles

Para más información, consultar [README.md](README.md).
