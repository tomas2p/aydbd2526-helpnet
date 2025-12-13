"""
Dependencias de FastAPI para inyección de dependencias
"""
from typing import Generator
from sqlalchemy.orm import Session
from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Generador de sesiones de base de datos.
    Se usa como dependencia en los endpoints para obtener una sesión DB.
    La sesión se cierra automáticamente al terminar la petición.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
