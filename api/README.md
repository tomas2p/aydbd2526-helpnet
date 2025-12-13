# HelpNet API

API REST completa para el sistema HelpNet, una plataforma de gestión de voluntariado y proyectos humanitarios. Desarrollada con FastAPI y PostgreSQL, proporciona acceso programático a todas las funcionalidades del modelo de datos relacional.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Inicialización de Base de Datos](#inicialización-de-base-de-datos)
- [Ejecución](#ejecución)
- [Testing](#testing)
- [Documentación de API](#documentación-de-api)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Características Especiales](#características-especiales)

## ✨ Características

- **CRUD Completo**: Operaciones Create, Read, Update y Delete para las 14 tablas del modelo relacional
- **Herencia Polimórfica**: Implementación de recursos donados y alquilados con serialización dinámica
- **Validaciones de Negocio**: Edad mínima 18 años, coordenadas geográficas válidas, consistencia de fechas
- **Paginación Universal**: Todos los endpoints de listado soportan parámetros `skip` y `limit`
- **Información de Cascada**: Los DELETE retornan el conteo exacto de registros eliminados en cascada
- **Relaciones Complejas**: Soporte completo para claves compuestas, relaciones N:M y ternarias
- **Suite de Testing**: 50 tests automatizados con pytest (100% passing)
- **Documentación Interactiva**: Swagger UI y ReDoc integrados automáticamente

## 🛠 Tecnologías

- **FastAPI** >= 0.104.0
- **SQLAlchemy** >= 2.0.0
- **PostgreSQL** 13+
- **Pydantic** >= 2.5.0
- **Pytest** >= 7.0.0
- **Uvicorn** >= 0.24.0

## 📦 Requisitos Previos

- Python 3.10 o superior
- PostgreSQL 13 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación

### 1. Navegar al directorio de la API

```bash
cd helpnet-sql-scripts/api
```

### 2. Crear y activar entorno virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar en Linux/Mac
source venv/bin/activate

# Activar en Windows
venv\\Scripts\\activate
```

### 3. Instalar dependencias

```bash
# Opción recomendada: usando el script
./run_api.sh install

# Alternativa: instalación manual
pip install -r requirements.txt
```

## ⚙️ Configuración

### 1. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Configuración de base de datos
DATABASE_URL=postgresql://usuario:password@localhost:5432/helpnet
DATABASE_URL_TEST=postgresql://usuario:password@localhost:5432/helpnet_test

# Configuración de la aplicación
APP_NAME=HelpNet API
APP_VERSION=1.0.0
DEBUG=True
```

**⚠️ IMPORTANTE**: Reemplazar `usuario` y `password` con tus credenciales de PostgreSQL.

### 2. Crear bases de datos en PostgreSQL

```bash
# Conectar a PostgreSQL
psql -U usuario

# Crear base de datos de desarrollo
CREATE DATABASE helpnet;

# Crear base de datos de testing
CREATE DATABASE helpnet_test;

# Salir
\\q
```

## 🗄️ Inicialización de Base de Datos

### 1. Ejecutar script DDL (crear tablas)

```bash
psql -U usuario -d helpnet -f ddl_helpnet.sql
```

### 2. Cargar datos de ejemplo (opcional)

```bash
psql -U usuario -d helpnet -f dml_helpnet.sql
```

Esto creará:
- 15 organizaciones (Org1 - Org15)
- 30 proyectos
- 60 actividades
- 60 localizaciones
- 15 voluntarios (V1 - V15)
- 15 recursos
- Múltiples participaciones, coordinaciones y cesiones

### 3. Verificar instalación

```bash
psql -U usuario -d helpnet -c "\\dt"
```

Deberías ver 14 tablas creadas.

## ▶️ Ejecución

### Iniciar servidor de desarrollo

```bash
./run_api.sh
```

El servidor estará disponible en:

- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

### Verificar que funciona

```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "service": "helpnet-api"
}
```

## 🧪 Testing

La API incluye una suite completa de 50 tests automatizados que validan todas las funcionalidades.

### Ejecutar todos los tests

```bash
./run_api.sh test
```

**Resultado esperado**: ✅ 50 passed in ~1s

### Ejecutar tests específicos

El script `run_api.sh` acepta todos los parámetros de pytest:

```bash
# Tests de un archivo completo
./run_api.sh test tests/test_voluntarios.py -v

# Tests que coincidan con un patrón de nombre
./run_api.sh test -k "test_create" -v

# Tests relacionados con voluntarios
./run_api.sh test -k "voluntario" -v

# Un test específico por nombre exacto
./run_api.sh test -k "test_create_proyecto" -v

# Tests con salida detallada y sin warnings
./run_api.sh test -v --tb=short
```

### Generar reporte de cobertura

```bash
# Primero instalar pytest-cov si no está instalado
pip install pytest-cov

# Generar reporte HTML
./run_api.sh test --cov=app --cov-report=html

# Ver reporte en navegador
open htmlcov/index.html  # En Mac
xdg-open htmlcov/index.html  # En Linux
```

**Nota**: La cobertura de tests requiere el paquete `pytest-cov`. Si ya ejecutaste `./run_api.sh install`, necesitas reinstalar las dependencias actualizadas con `pip install -r requirements.txt`.

## 📚 Documentación de API

### Documentación Interactiva

Una vez iniciado el servidor, visita:

- **Swagger UI**: http://localhost:8000/docs
  - Interfaz interactiva para probar endpoints
  - Esquemas de request/response
  - Autenticación (si se implementa)

- **ReDoc**: http://localhost:8000/redoc
  - Documentación más legible
  - Mejor para referencia

### Documentación Detallada

Ver [API_ENDPOINTS.md](API_ENDPOINTS.md) para tabla completa con:
- Descripción de cada endpoint
- Método HTTP
- Ejemplos de petición
- Ejemplos de respuesta

## 📁 Estructura del Proyecto

```
helpnet-sql-scripts/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicación FastAPI principal
│   ├── database.py             # Configuración de SQLAlchemy
│   ├── dependencies.py         # Inyección de dependencias
│   │
│   ├── models/                 # Modelos SQLAlchemy (ORM)
│   │   ├── __init__.py
│   │   ├── organizacion.py     # Organizacion + EmailOrganizacion
│   │   ├── proyecto.py         # Proyecto + Actividad + Localizacion
│   │   ├── voluntario.py       # Voluntario + VoluntarioSkill + Vista
│   │   ├── recurso.py          # Recurso + Donado + Alquilado (herencia)
│   │   └── relaciones.py       # Participa, Coordina, Cesion, RecursoUsado
│   │
│   ├── schemas/                # Schemas Pydantic (validación)
│   │   ├── __init__.py
│   │   ├── common.py           # PaginatedResponse, DeleteResponse
│   │   ├── organizacion.py
│   │   ├── proyecto.py
│   │   ├── voluntario.py
│   │   ├── recurso.py
│   │   └── relaciones.py
│   │
│   ├── crud/                   # Lógica de base de datos
│   │   ├── __init__.py
│   │   ├── cascade.py          # Conteo de registros en cascada
│   │   ├── organizacion.py
│   │   ├── proyecto.py
│   │   ├── voluntario.py
│   │   ├── recurso.py
│   │   └── relaciones.py
│   │
│   └── routers/                # Endpoints de la API
│       ├── __init__.py
│       ├── organizaciones.py   # /api/organizaciones/*
│       ├── proyectos.py        # /api/proyectos/*
│       ├── actividades.py      # /api/proyectos/{id}/actividades/*
│       ├── localizaciones.py   # /api/proyectos/{id}/actividades/{id}/localizaciones/*
│       ├── voluntarios.py      # /api/voluntarios/*
│       ├── recursos.py         # /api/recursos/* (polimórfico)
│       └── relaciones.py       # /api/participaciones/*, /api/cesiones/*, etc.
│
├── tests/                      # Tests con pytest
│   ├── conftest.py            # Fixtures compartidos
│   ├── test_voluntarios.py    # Tests de validación de edad
│   ├── test_recursos.py       # Tests de herencia polimórfica
│   └── test_cascade.py        # Tests de DELETE en cascada
│
├── ddl_helpnet.sql            # Script de creación de tablas
├── dml_helpnet.sql            # Script de datos de ejemplo
├── delete_data.sql            # Script de limpieza
├── requirements.txt           # Dependencias Python
├── .env                       # Variables de entorno (NO subir a Git)
├── .gitignore                 # Archivos ignorados por Git
├── README.md                  # Este archivo
└── API_ENDPOINTS.md           # Documentación detallada de endpoints
```

## 🔥 Características Especiales

### 1. IDs como Cadenas de Texto

**⚠️ IMPORTANTE**: Los identificadores de `proyecto`, `actividad` y `localizacion` son de tipo `INTEGER` autoincremental, pero los datos de ejemplo usan cadenas alfanuméricas para facilitar la lectura.

**Ejemplos de IDs en datos de prueba**:
- Proyecto: `1`, `2`, `3`
- Actividad: `1`, `2`, `3`
- Localización: `1`, `2`, `3`

**En producción**: La base de datos asigna automáticamente IDs numéricos secuenciales.

### 2. Herencia Polimórfica en Recursos

Los recursos implementan herencia de tabla única con discriminador `tipo`. La API serializa las respuestas dinámicamente según el subtipo, incluyendo solo los campos relevantes.

**Tipos disponibles**:
- `'D'`: Recurso Donado → incluye `estado`, `nombre_donante`, `email_donante`
- `'A'`: Recurso Alquilado → incluye `proveedor`, `costo`, `fecha_devolucion`

**Ejemplo: Crear recurso donado**:
```json
POST /api/recursos
{
  "tipo": "D",
  "nombre": "Tienda de campaña",
  "fecha_entrega": "2025-01-15",
  "estado": "nuevo",
  "nombre_donante": "Juan Pérez"
}
```

**Crear recurso alquilado**:
```json
POST /api/recursos
{
  "tipo": "A",
  "nombre": "Generador",
  "fecha_entrega": "2025-01-15",
  "proveedor": "Alquileres SA",
  "costo": 250.00,
  "fecha_devolucion": "2025-02-15"
}
```

La respuesta se serializa dinámicamente según el tipo, sin campos null.

### 3. Información de Cascada en DELETE

Todos los endpoints DELETE retornan información detallada sobre los registros eliminados en cascada, proporcionando trazabilidad completa de la operación:

```json
DELETE /api/organizaciones/Org1

Response:
{
  "message": "Organización eliminada exitosamente",
  "deleted_id": "Org1",
  "cascade_info": {
    "emails": 2,
    "proyectos": 5,
    "actividades": 12,
    "localizaciones": 30,
    "participaciones": 45,
    "coordinaciones": 8,
    "cesiones": 3,
    "recursos_usados": 10
  }
}
```

### 4. Validación de Edad Mínima

La API valida automáticamente que los voluntarios tengan **mínimo 18 años cumplidos** en su `fecha_alta`. Esta validación se implementa a nivel de schema con Pydantic:

```python
# Validación automática en el schema VoluntarioCreate
@field_validator('fecha_alta')
@classmethod
def validar_edad_minima(cls, v, info):
    if 'fecha_nacimiento' in info.data:
        edad_años = (v - info.data['fecha_nacimiento']).days / 365.25
        if edad_años < 18:
            raise ValueError('El voluntario debe tener al menos 18 años')
    return v
```

Si se intenta crear un voluntario menor de edad, la API retorna `422 Unprocessable Entity` con mensaje descriptivo.

### 5. Paginación en Todos los Listados

```bash
GET /api/organizaciones?skip=20&limit=10
```

Respuesta:
```json
{
  "items": [...],
  "total": 150,
  "skip": 20,
  "limit": 10
}
```

### 6. Claves Compuestas

Entidades con claves primarias compuestas:

- **Actividad**: `(id_actividad, id_proyecto)`
- **Localización**: `(id_localizacion, id_actividad, id_proyecto)`
- **Participa**: `(id_localizacion, id_actividad, id_proyecto, dni_voluntario)`
- **Coordina**: `(id_localizacion, id_actividad, id_proyecto, dni_voluntario)`
- **Cesión**: `(nombre_organizacion, id_proyecto, dni_voluntario)`

Usar rutas anidadas para acceder:
```
/api/proyectos/{id_proyecto}/actividades/{id_actividad}/localizaciones/{id_localizacion}
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📝 Licencia

Este proyecto es parte de un sistema académico de gestión de voluntariado.

## 👥 Contacto

Para soporte o consultas sobre la API, consultar la documentación interactiva en `/docs`.

---

**Nota**: Este README asume que estás familiarizado con conceptos básicos de REST APIs, PostgreSQL y Python. Para más detalles sobre endpoints específicos, ver [API_ENDPOINTS.md](API_ENDPOINTS.md).
