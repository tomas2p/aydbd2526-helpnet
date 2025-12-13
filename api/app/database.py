"""
Configuración de la base de datos usando SQLAlchemy
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener URL de base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://usuario:password@localhost:5432/helpnet")

# Crear engine de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verificar conexiones antes de usarlas
    echo=False  # Cambiar a True para debug de SQL
)

# Crear SessionLocal para transacciones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos ORM
Base = declarative_base()


def get_database_url():
    """Retorna la URL de la base de datos actual"""
    return DATABASE_URL


def init_db():
    """
    Inicializa la base de datos creando todas las tablas.
    Nota: En producción usar Alembic para migraciones.
    """
    from app.models import organizacion, proyecto, voluntario, recurso, relaciones
    Base.metadata.create_all(bind=engine)
