"""
HelpNet API - Aplicación principal FastAPI
API REST para gestión de organizaciones, proyectos, voluntarios y recursos
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from app.routers import (
    organizaciones,
    proyectos,
    actividades,
    localizaciones,
    voluntarios,
    recursos,
    relaciones
)

# Cargar variables de entorno
load_dotenv()

# Crear aplicación FastAPI
app = FastAPI(
    title=os.getenv("APP_NAME", "HelpNet API"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="""
    API REST para el sistema HelpNet de gestión de voluntariado y proyectos humanitarios.
    
    ## Características principales:
    
    * **Organizaciones**: Gestión de ONGs y sus proyectos
    * **Proyectos**: Proyectos humanitarios con actividades y localizaciones
    * **Voluntarios**: Registro y gestión de voluntarios con skills
    * **Recursos**: Gestión polimórfica de recursos donados y alquilados
    * **Relaciones**: Participaciones, coordinaciones y cesiones
    
    ## Notas importantes:
    
    * Los IDs de proyecto, actividad y localización son VARCHAR alfanuméricos (ej: 'P1_1', 'A1_1_1')
    * Las operaciones DELETE tienen cascada automática - se reporta el conteo de registros afectados
    * Los endpoints de listado soportan paginación con parámetros `skip` y `limit`
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: especificar orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(organizaciones.router, prefix="/api", tags=["Organizaciones"])
app.include_router(proyectos.router, prefix="/api", tags=["Proyectos"])
app.include_router(actividades.router, prefix="/api", tags=["Actividades"])
app.include_router(localizaciones.router, prefix="/api", tags=["Localizaciones"])
app.include_router(voluntarios.router, prefix="/api", tags=["Voluntarios"])
app.include_router(recursos.router, prefix="/api", tags=["Recursos"])
app.include_router(relaciones.router, prefix="/api", tags=["Relaciones"])


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "HelpNet API - Sistema de gestión de voluntariado",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint para monitoreo"""
    return {"status": "healthy", "service": "helpnet-api"}
